# Kotlin 协程

---

## 一、协程不是线程，是编译器生成的状态机

很多人第一次听到"协程"会以为它是某种轻量级线程。但协程的本质完全不同——它是 **Kotlin 编译器在编译阶段对你的代码做的一次变换**。

看这段代码：

```kotlin
suspend fun loadPage(): PageData {
    val user = fetchUser()                     // 第1步
    val checklists = fetchChecklists(user.id)  // 第2步
    return PageData(user, checklists)          // 第3步
}
```

Kotlin 编译器看到 `suspend` 关键字后，会把这个函数自动变换成一个状态机，大致相当于：

```kotlin
// 编译器生成的伪代码（你不需要手写）
fun loadPage(continuation: Continuation) {
    when (continuation.label) {
        0 -> {
            continuation.label = 1
            fetchUser(continuation)  // 注册回调，把 continuation 传下去
            // 函数返回！线程空出来了
        }
        1 -> {
            val user = continuation.result  // 上一步的结果
            continuation.label = 2
            fetchChecklists(user.id, continuation)  // 注册下一个回调
            // 函数再次返回！
        }
        2 -> {
            val checklists = continuation.result
            continuation.resume(PageData(user, checklists))  // 最终结果
        }
    }
}
```

你写的每一行顺序代码，在编译后都变成了一个状态。`Continuation` 对象就是那个保存"我现在在第几步、上一步结果是什么"的小本本。

这就是协程的核心把戏：**你写同步风格的代码，编译器帮你生成回调链。**

---

## 二、协程 vs 线程 vs JDK 21 虚拟线程

这三者解决的是同一个问题——线程在等 I/O 时白白占着资源——但方式各不相同。

| 对比维度 | OS 线程 | JDK 21 虚拟线程 | Kotlin 协程 |
|:---|:---|:---|:---|
| 谁来管理 | 操作系统 | JVM | Kotlin 编译器 + 调度器 |
| 实现方式 | OS 内核调度 | JVM 透明挂起 | 状态机 + 回调 |
| 代码改动 | 无 | 无 | 需要 `suspend` 关键字 |
| 内存占用 | ~1MB / 线程 | ~几 KB / 线程 | 极小（几个对象） |
| 数量上限 | 几千 | 百万级 | 理论无限 |
| 调度方式 | 抢占式（OS 决定） | 抢占式（JVM 决定） | 协作式（自己让出） |

**JDK 21 虚拟线程**的最大优点是完全透明：你的代码不用改，Spring Boot 3.2+ 加一行配置就能启用：

```properties
spring.threads.virtual.enabled=true
```

然后你原来阻塞的代码照常跑，JVM 在阻塞时自动"卸载"虚拟线程，载体线程空出来处理别的请求。

**Kotlin 协程**需要你主动标记 `suspend`，但换来更多控制权。两者的根本区别可以用一句话概括：**虚拟线程是"聪明地阻塞"，协程是"根本不阻塞"。**

虚拟线程中阻塞还是会发生，只是 JVM 在阻塞时把虚拟线程"停车"，等 I/O 完成再"取车"继续开。而协程配合非阻塞 I/O 时，I/O 发出去后函数直接返回，操作系统完成 I/O 后触发回调继续执行。

---

## 三、`suspend` 到底意味着什么

`suspend` 不是魔法，它不会让函数里的所有代码都变成异步的。**协程只在调用另一个 `suspend` 函数的地方才会"挂起"**，其他代码照常在当前线程上顺序执行。

```kotlin
suspend fun loadPage(): PageData {
    val user = fetchUser()          // ← 挂起点（fetchUser 是 suspend 函数）
    println(user)                   // ← 普通代码，同步执行，不挂起
    val checklists = fetchChecklists(user.id)  // ← 挂起点
    println(checklists)             // ← 普通代码，同步执行
    return PageData(user, checklists)          // ← 普通代码
}
```

编译器生成的状态机，只在 `suspend` 函数调用处分割状态。`println` 夹在状态转换之间，拿到结果后立刻执行，跟普通函数没有区别。

### 它怎么知道哪些是阻塞的？

**答案是：它不知道，也不会自动判断。** 这是协程最容易踩坑的地方。

`suspend` 关键字只是一个声明——"这个函数可能会挂起"，而不是"这个函数内部所有 I/O 都会自动变成非阻塞的"。

```kotlin
suspend fun dangerousFunction() {
    Thread.sleep(5000)           // 真实阻塞！协程不知道，线程被卡死 5 秒
    File("big.txt").readText()   // 真实阻塞！同上
}
```

这段代码虽然在 `suspend` 函数里，但 `Thread.sleep` 和文件读取是普通的阻塞调用，会直接阻塞 EventLoop 线程。正确做法是显式告诉协程"这段代码是阻塞的，切到 IO 线程池去执行"：

```kotlin
suspend fun safeFunction() {
    withContext(Dispatchers.IO) {   // 明确切换到 IO 线程池
        Thread.sleep(5000)          // 在 IO 线程上阻塞，不影响 EventLoop
        File("big.txt").readText()
    }
}
```

### `suspend` 和 `withContext` 是两回事

| | 作用 | 类比 |
|:---|:---|:---|
| `suspend` | 标记"这个函数可以被挂起"，是一个**声明** | 贴标签说"我可能需要等待" |
| `withContext(IO)` | 实际把代码切换到另一个线程池执行，是一个**动作** | 真的换人去做这件事 |

真正触发挂起的不是 `suspend` 关键字本身，而是函数内部调用的那些"真正会挂起"的原语：`delay()`、`withContext()`、`Mono.await()`、非阻塞数据库驱动的调用、`Channel.receive()` 等。

`suspend` 的真实意义是："我的内部某处会调用真正的挂起原语，所以调用我的人也需要能处理挂起。"这就是为什么 `suspend` 会"传染"——它在告诉编译器：调用我的地方需要是协程上下文。

---

## 四、协程的入口：谁来"开门"

`suspend` 函数只能被另一个 `suspend` 函数或协程作用域调用。那第一个 `suspend` 函数从哪里开始？答案是**协程构建器**——它们是普通函数，可以被任何地方调用：

```kotlin
launch { }      // 启动协程，不关心返回值（fire-and-forget）
async { }       // 启动协程，返回 Deferred<T>（有返回值）
runBlocking { } // 启动协程并阻塞当前线程直到完成（主要用于测试，生产慎用）
```

调用链看起来像这样：

```
普通世界
    │
    │  launch { }  ← 这是门
    ▼
协程世界（只有在这里才能调用 suspend 函数）
    │
    ├── suspend fun A()
    │       └── suspend fun B()
    │               └── suspend fun C()
```

在 Spring WebFlux 中，Spring 就是那个"开门的人"。当你的 Controller 方法标记为 `suspend` 时，Spring 内部会用协程构建器将其包装成 `Mono`，在 Reactor 调度器上执行：

```kotlin
@GetMapping("/templates")
suspend fun getTemplates(): List<Template> {   // Spring 看到 suspend
    return service.getTemplates()              // Spring 自动处理协程入口
}
```

你不需要自己写 `launch` 或 `runBlocking`，框架替你完成了。

---

## 五、Dispatcher 的选择

协程需要一个 Dispatcher 来决定在哪个线程（池）上运行：

- `Dispatchers.IO` — 数据库查询、文件读写等阻塞 I/O，线程池较大
- `Dispatchers.Default` — CPU 密集计算，线程数 = CPU 核心数
- `Dispatchers.Main` — Android UI 线程，后端不用

实际编码时的判断规则很简单：调用的是 `suspend` 函数（非阻塞数据库驱动、WebClient 等）就不需要额外操作，自动挂起没问题；调用的是普通阻塞代码，就必须手动包 `withContext(Dispatchers.IO)` 来隔离影响。

---

## 六、并行执行：`async` / `await`

这是协程最实用的能力之一。假设要并行加载三个数据源：

```kotlin
suspend fun loadSpaceDashboard(spaceId: Long): SpaceDashboard {
    return coroutineScope {
        val spaceInfoDeferred = async { fetchSpaceInfo(spaceId) }       // 立刻启动
        val templatesDeferred = async { fetchChecklistTemplates(spaceId) } // 立刻启动
        val countDeferred = async { fetchMemberCount(spaceId) }         // 立刻启动

        val spaceInfo = spaceInfoDeferred.await()
        val templates = templatesDeferred.await()
        val count = countDeferred.await()

        SpaceDashboard(
            spaceInfo = spaceInfo,
            templates = templates,
            memberCount = count,
            summary = "Space ${spaceInfo.name} 有 ${count} 个成员，${templates.size} 个模板"
        )
    }
}
```

这里的关键在于：**并行发生在 `async { }` 这一行，不是在 `await()` 这一行。**

`async { }` 的行为是立刻启动协程并返回，就像按下了启动按钮，任务已经在后台跑了，你拿到的只是一张"取件单"（`Deferred`）。三个 `async` 连续按下三个启动键，三个任务同时在跑。之后的三个 `await` 只是依次去取已经在后台运行的结果——如果还没好就挂起等，已经好了就直接拿。

用时间线来看：

```
t=0ms    async { fetchSpaceInfo }    ← 启动，立刻返回 Deferred
t=0ms    async { fetchTemplates }    ← 启动，立刻返回 Deferred（SpaceInfo 还在跑）
t=0ms    async { fetchMemberCount }  ← 启动，立刻返回 Deferred（三个同时在跑）

         [三个任务同时在后台执行中...]

t=0ms    spaceInfoDeferred.await()   ← 要取件了，包裹还没到，挂起等待
t=150ms  fetchMemberCount 完成       ← 结果存进 countDeferred，没人取先放着
t=200ms  fetchTemplates 完成         ← 结果存进 templatesDeferred，先放着
t=300ms  fetchSpaceInfo 完成         ← await() 拿到结果，继续往下
t=300ms  templatesDeferred.await()   ← 早就完成了，立刻返回
t=300ms  countDeferred.await()       ← 早就完成了，立刻返回
                              总计：300ms（最慢那个的时间）
```

如果写成 `async { }.await()` 紧跟在一起，就退化成了顺序执行，等于没有并行。

### `coroutineScope` 的作用

`coroutineScope { }` 创建一个局部 Scope，它会等块内所有子协程完成后才返回。同时它也自动处理了结构化并发——如果任意一个 `async` 抛出异常，其他的会被自动取消，整个块向上传播异常。

---

## 七、Eager vs Lazy：和 Reactor 的本质区别

如果你用过 JavaScript 的 Promise，会发现 `async` 的行为和 Promise 一模一样——创建即启动（Eager）：

```javascript
// JavaScript：Promise 在 new 的瞬间就开始执行了
const p1 = fetch('/api/user')       // 请求已经发出去了
const p2 = fetch('/api/templates')  // 请求已经发出去了
const [user, templates] = await Promise.all([p1, p2])
// Promise.all 只是"等两个都完成"，不是它让请求并行的
```

但 Reactor（WebFlux 底层）是完全不同的模式——**懒执行（Lazy）**：

```kotlin
// Reactor：定义了一条流水线，但什么都没发生
val mono = webClient.get("/api/user").retrieve().bodyToMono(User::class.java)
// 此时没有任何网络请求！

// 只有 subscribe() 之后，流水线才真正启动
mono.subscribe { user -> println(user) }  // ← 这才是触发器
```

| | Kotlin `async` | JavaScript Promise | Java CompletableFuture | Reactor Mono/Flux |
|:---|:---|:---|:---|:---|
| 何时启动 | 创建时立刻 | 创建时立刻 | 创建时立刻 | `subscribe()` 时 |
| 模式 | Eager | Eager | Eager | Lazy |

Reactor 设计成 Lazy 是有原因的：它让你可以先组装好整条处理流水线，再决定什么时候触发，并且支持背压（下游处理不过来可以告诉上游慢一点）。而 `async { }` 一旦写下去请求就发出去了，没有这种"先组装后触发"的能力。

---

## 八、协程与 WebFlux 的桥梁

两者的桥梁是 `kotlinx-coroutines-reactor` 库，它提供了互转方法：

```kotlin
// Mono → 协程
val result: String = someMono.await()

// 协程 → Mono
val mono: Mono<String> = mono { fetchData() }

// Flux → Flow（Kotlin 协程的流）
val flow: Flow<String> = someFlux.asFlow()
```

简单记忆这几个概念：`Mono` 代表"未来会有一个值"，`Flux` 代表"未来会有多个值一个一个来"，`Flow` 是 Kotlin 协程原生的流（Flux 的协程版本）。它们都是"还没到的数据"的容器。

Spring WebFlux 在检测到 Controller 方法是 `suspend` 函数时，会自动把它包装成 `Mono`，整个执行仍然在 Netty 的 EventLoop 上调度，非阻塞的性质完全保留。所以很多 Kotlin 项目选择 WebFlux + Coroutines 的组合——既有非阻塞的性能优势，又保留同步代码的可读性和 debug 友好性。

---

## 九、协程的三个陷阱

### 陷阱一："颜色传染"

`suspend` 函数只能被另一个 `suspend` 函数或协程作用域调用。一旦某个底层函数变成 `suspend`，调用链往上的函数都要跟着变：

```kotlin
suspend fun getTemplates(): List<Template> { ... }

// 普通函数想调用它 → 编译错误
fun normalFunction() {
    getTemplates()  // ❌ suspend 函数不能在非 suspend 上下文调用
}

// 必须包在协程里
fun normalFunction() {
    CoroutineScope(Dispatchers.IO).launch {
        getTemplates()  // ✅
    }
}
```

这就是所谓的"函数颜色"问题——suspend 函数和普通函数是两种"颜色"，不能随意混用。

### 陷阱二：结构化并发与生命周期

每个协程都属于某个 `CoroutineScope`，Scope 就是协程的"家"。父 Scope 取消时，所有子协程自动取消。

```kotlin
// ❌ 危险：GlobalScope 的协程没有生命周期约束
fun handleRequest(spaceId: Long) {
    GlobalScope.launch {
        val result = heavyDatabaseQuery(spaceId)
        // 请求已经超时，客户端断开了
        // 但这个协程还在跑，浪费资源，结果没人要
    }
}
```

`GlobalScope` 的协程生命周期等于整个 JVM 进程，一旦启动没有任何东西能自动取消它。请求来来去去，内存里可能堆积大量孤儿协程。

正确做法是用 `coroutineScope { }` 创建局部 Scope，让协程与请求生命周期绑定：

```kotlin
suspend fun handleRequest(spaceId: Long) {
    coroutineScope {
        val templatesJob = launch { fetchTemplates(spaceId) }
        val membersJob = launch { fetchMembers(spaceId) }
        // 请求取消 → 两个子协程自动取消
        // 块结束时等待两个都完成
    }
}
```

在 Spring WebFlux 中，框架会帮你管理 Scope——`suspend` Controller 方法的 Scope 和 HTTP 请求绑定，请求取消协程就自动取消。你需要担心 `GlobalScope` 的场景主要是在框架管理之外手动启动后台任务时。

### 陷阱三：异常处理的反直觉行为

`launch` 和 `async` 对异常的处理方式不同：

```kotlin
coroutineScope {
    // launch：异常立即传播给父 Scope
    launch {
        throw RuntimeException("出错了")
        // 异常立刻传播，整个 coroutineScope 崩溃
    }

    // async：异常被"存"在 Deferred 里，await() 时才释放
    val deferred = async {
        throw RuntimeException("出错了")
    }
    println("这行还会执行")   // async 不立即崩溃 Scope
    deferred.await()          // 异常在这里才抛出
}
```

`launch` 的异常直接向上传播，`async` 的异常被暂存起来等 `await()` 时才抛出。这和大多数人的直觉不一致，容易让异常被静默吞掉。

如果你在自己管理的 Scope 里使用 `launch`，可以绑定一个 `CoroutineExceptionHandler` 来兜底。Handler 不是全局单例，而是绑定在具体 Scope 上的：

```kotlin
val handler = CoroutineExceptionHandler { _, exception ->
    println("捕获到异常：$exception")
}

val scope = CoroutineScope(Dispatchers.IO + handler)
scope.launch { throw RuntimeException("A") }  // handler 处理
```

这里的 `+` 号是 Kotlin 的运算符重载。`CoroutineContext` 接口定义了 `plus` 运算符，`Dispatchers.IO`、`CoroutineExceptionHandler`、`CoroutineName` 都是 `CoroutineContext` 的元素，`+` 把它们合并成一个复合 Context。

不过在 Spring WebFlux 中，**你几乎不需要 `CoroutineExceptionHandler`**。`suspend` Controller 的异常处理和 MVC 完全一致，用 `@ExceptionHandler` 和 `@ControllerAdvice` 就可以：

```kotlin
@ControllerAdvice
class GlobalExceptionHandler {
    @ExceptionHandler(NotFoundException::class)
    fun handleNotFound(e: NotFoundException): ResponseEntity<ErrorResponse> {
        return ResponseEntity.status(404).body(ErrorResponse(e.message))
    }
}

@GetMapping("/templates")
suspend fun getTemplates(@PathVariable spaceId: Long): List<Template> {
    return service.getTemplates(spaceId)
        ?: throw NotFoundException("Space $spaceId 不存在")  // 和 MVC 写法一样
}
```

---

## 十、全景图

```
Spring MVC（阻塞）
  └─ 简单直接，debug 友好，线程数是天花板

Spring MVC + JDK 21 虚拟线程
  └─ 代码完全不改，JVM 自动处理挂起
     性能略低于真正非阻塞（阻塞还是会发生，只是代价变小了）

Spring WebFlux + Reactor（纯响应式）
  └─ 极致性能，但 Mono/Flux 链式代码学习成本高，debug 难

Spring WebFlux + Kotlin 协程
  └─ 性能和 Reactor 相同，代码看起来像同步，debug 相对友好
     代价是 suspend 传染、Dispatcher 选择等学习成本
```

选哪个取决于你的场景：如果是从现有 MVC 项目迁移，Spring MVC + 虚拟线程是代价最小的路径；如果是 Kotlin 技术栈追求性能最优，WebFlux + 协程是当前的最佳组合。