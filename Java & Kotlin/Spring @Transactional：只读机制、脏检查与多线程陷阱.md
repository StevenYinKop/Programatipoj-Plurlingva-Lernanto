# Spring `@Transactional`：只读机制、脏检查与多线程陷阱

## 1. 读写分离：`readOnly = true` 与默认配置的区别

在服务层（Service）编写方法时，我们通常会面临是使用 `@Transactional(readOnly = true)` 还是默认 `@Transactional` 的选择。

规则很简单：**读操作只查询数据，使用 `readOnly = true`；写操作涉及修改或删除，使用默认的 `@Transactional`。**

```kotlin
@Transactional(readOnly = true)   // getTemplates → 只查询
fun getTemplates(spaceId: Long): List<ChecklistTemplateResponse> { ... }

@Transactional                     // createTemplate → 有写入
fun createTemplate(spaceId: Long, request: CreateChecklistTemplateRequest): ChecklistTemplateResponse { ... }
```

开启 `readOnly = true` 并非只是一个心理安慰，它在底层带来了切实的性能提升：
* **关闭脏检查（Dirty Checking）**：JPA/Hibernate 将不再追踪实体的状态变化，大幅节省内存和 CPU 消耗。
* [cite_start]**路由到从库（Read Replica）**：在配置了读写分离的生产环境中，某些数据库驱动或 Spring 配置会将标记了只读的事务自动路由到只读副本，从而减轻主库压力 [cite: 37, 38]。

> **注意**：如果在 `readOnly = true` 的事务中意外执行了写操作（例如 `save()`），根据底层数据库和驱动的不同，Hibernate 可能会直接忽略该操作或抛出异常。

### 1.1 `@Transactional` 的高频参数指南

除了 `readOnly`，还有几个至关重要的参数需要掌握：

* **`propagation` (传播行为)**：
    * `REQUIRED` (默认)：如果当前有事务就加入，没有就新建。
    * [cite_start]`REQUIRES_NEW`：无论当前是否有事务，都挂起当前事务并开启一个全新的事务 [cite: 27]。
* **`rollbackFor` (回滚控制)**：
    * Spring 默认**仅对 `RuntimeException` 和 `Error` 回滚**。受检异常（如 `IOException`）发生时，默认是**不回滚**的！
    * 如果你希望所有异常都触发回滚，务必显式声明：`@Transactional(rollbackFor = [Exception::class])`。
* **`isolation` (隔离级别)**：
    * 多数数据库默认为 `READ_COMMITTED`（读已提交）。
    * [cite_start]最高级别为 `SERIALIZABLE`（串行化），能避免所有并发问题但性能最差 [cite: 28]。

### 1.2 避坑指南：事务为什么失效了？

使用 `@Transactional` 最容易犯的错就是**同类内部调用**：

```kotlin
@Service
class ChecklistService {
    fun outerMethod() {
        innerMethod()  // ❌ 事务不生效！绕过了 Spring AOP 代理
    }

    @Transactional
    fun innerMethod() { ... }
}
```
**解法**：将内部方法剥离到另一个 Service 类中，或者在类中自我注入。
[cite_start]此外，还需要注意：`@Transactional` 默认只对 `public` 方法生效，且如果在方法内用 `try-catch` 吞掉了异常而没有重新抛出，事务同样不会触发回滚 [cite: 29]。

---

## 2. 什么是“脏检查”（Dirty Checking）？

前面提到 `readOnly = true` 会关闭脏检查，那到底什么是脏检查？

在事务范围内，Hibernate 会追踪所有被管理的实体对象。当查询出一条数据时，Hibernate 会将其放入“一级缓存”，并拍一张**“快照”**。

```kotlin
@Transactional
fun updateTemplate(templateId: Long, request: UpdateChecklistTemplateRequest) {
    // 1. 查询，Hibernate 拍下快照：{ name="旧名字", description="旧描述" }
    val template = checklistTemplateRepository.findById(templateId).get()

    // 2. 修改实体属性
    template.name = "新名字"

    // 3. 事务提交前，Hibernate 逐字段对比当前实体与快照
    //    发现 name 发生改变 → 自动执行 UPDATE SQL
}
[cite_start]// 事务提交 → UPDATE checklist_template SET name='新名字' WHERE id=? [cite: 36]
```

[cite_start]**脏检查的性能代价**：如果你的查询返回了 1000 条记录，事务提交前 Hibernate 就必须对比 1000 个对象的所有字段。对于纯查询的场景，这完全是资源浪费。加入 `readOnly = true` 后，Hibernate 直接跳过快照生成和逐字比对的过程，内存占用和 CPU 开销立减 [cite: 40]。

---

## 3. 核心解惑：SQL 执行了就等于数据更新了吗？

[cite_start]许多开发者在观察日志时会有这样的疑惑：*“如果在事务提交前，数据库就已经执行了 `UPDATE` SQL，那为什么还要 Commit 提交事务？数据不是已经被修改了吗？”* [cite: 41]

这里存在一个关键误区：**SQL 的执行** 与 **事务的提交** 是两个截然不同的概念。

### 事务的真实生命周期

> 💡 **核心比喻：**
> * **SQL 执行** = 在草稿纸上写字
> * **COMMIT** = 把草稿正式归档盖章
> * **ROLLBACK** = 把草稿纸揉成一团扔进垃圾桶

[cite_start]当 Hibernate 执行 flush 并发送 `UPDATE` SQL 时，数据库接收了指令，但**并没有将变化写入正式的数据文件中**。这些变化被暂存在一个**事务私有的缓冲区**内 [cite: 52]。

在 `COMMIT` 触发之前：
1.  当前连接（当前事务）能够看到这些暂存的变化。
2.  **其他所有连接和用户完全看不到这些变化**（在 Read Committed 隔离级别下）。
3.  [cite_start]如果抛出异常，触发 `ROLLBACK`，所有暂存的 SQL 执行结果会被全部撤销，就像从未发生过一样 [cite: 53]。

[cite_start]事务的核心价值并不是仅仅“执行 SQL”，而是保证这批 SQL 的**原子性**——要么全部成功归档，要么全部撤销 [cite: 54]。

---

## 4. 事务的高阶陷阱：多线程与可见性

理解了前面的概念，我们再来看两个非常经典的进阶问题。

### 4.1 在同一个事务内，能查到自己刚修改但未提交的数据吗？

[cite_start]**答案是：能。** [cite: 57]

* **如果根据 ID 查相同实体**：Hibernate 会直接从一级缓存中返回你修改后的内存对象，根本不会发 SQL 查询数据库。
* [cite_start]**如果使用条件查询（如 findByName）**：Hibernate 会先触发内部的 flush，把刚才的修改变成 UPDATE SQL 发给数据库，然后再执行 SELECT。因为使用的是同一个数据库连接，所以在隔离的私有缓冲区里，你能准确查到刚刚修改的值 [cite: 61]。

### 4.2 父子线程中的事务是如何传递的？

[cite_start]这是微服务和并发编程中的重灾区。**Spring 的事务上下文是绑定在当前线程上的（通过 `ThreadLocal` 实现）。** [cite: 58]

[cite_start]这意味着**子线程无法继承父线程的事务。** [cite: 62]

**场景 A：父线程修改未提交，子线程去查**
```kotlin
@Transactional
fun parentMethod() {
    val template = repository.findById(1L).get()
    template.name = "新名字" // 修改未提交

    Thread {
        // 子线程是全新的上下文，拿不到父线程的 ThreadLocal
        // 只能看到数据库里的"旧名字"，因为父事务还没 COMMIT
        val t = repository.findById(1L).get() 
    }.start()
}
```

**场景 B：子线程执行完毕，父线程抛出异常回滚**
[cite_start]如果你在事务中开启了一个异步任务去保存数据：子线程会自己开启一个独立事务并直接提交。如果随后父线程的业务逻辑出错导致父事务回滚，**子线程已经提交的数据是不会随着父线程撤销的**！这就造成了严重的数据不一致 [cite: 63, 65]。

**核心结论：**
| 场景 | 结果可见性 |
| :--- | :--- |
| 同一线程同一事务，查自己刚改的数据 | **能看到** |
| 不同线程，看别人未提交的变化 | [cite_start]**看不到** [cite: 64] |
| 子线程拥有独立的 `@Transactional` | 独立事务，独立提交/回滚 |
| 子线程已提交，父线程最终回滚 | [cite_start]**父线程回滚不影响子线程已写入的数据** [cite: 65] |

涉及多线程时，永远不要假设事务会自动跨越线程边界。需要强一致性和原子性的业务操作，必须在同一个线程内闭环完成。