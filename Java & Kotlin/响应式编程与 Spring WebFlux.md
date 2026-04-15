# 响应式编程与 Spring WebFlux

---

## 一、先搞清楚我们在解决什么问题

Spring MVC 的工作方式简单而直观：一个 HTTP 请求进来，线程池分配一个线程，这个线程一路走到数据库，拿到数据，组装响应，返回。整条链路同步、阻塞、线性。

```
HTTP请求 → 线程池分配线程 → 线程等待数据库 → 线程返回响应
```

这很好理解，也很好 debug。但问题在于——**线程在等数据库的那段时间，什么都没做**。

这就像你在公司食堂打饭，窗口阿姨帮你盛菜的 30 秒里，你就站在那里发呆。一个人发呆没什么，但如果同时有 500 个人在排队，而食堂只有 200 个窗口（Tomcat 默认线程池上限），第 201 个人就只能站在门外等窗口空出来。

瓶颈不在厨房，**瓶颈在窗口数量**。

---

## 二、用餐厅理解两种线程模型

### Spring MVC：一人跟单制

想象一家餐厅，规则是——**每来一个顾客，就分配一个专属服务员，全程跟到底**。

```
顾客A进门 → 服务员1接待 → 去厨房等菜（服务员站在厨房门口等）→ 菜好了端回来 → 顾客A离开 → 服务员1才能接下一个人
顾客B进门 → 服务员2接待 → 去厨房等菜（站着等）→ ...
顾客C进门 → 服务员3接待 → ...
```

关键在于：服务员等菜的时候，什么都不做，就站在那里。这就是 Spring MVC 的线程在等 I/O 返回时的状态——线程活着，占着内存，但什么有意义的工作都没做。专业术语叫 **blocking（阻塞）**。

餐厅只有 200 个服务员。同时来了 300 个顾客，第 201 个只能在门口排队。

### WebFlux：呼叫器模型

换一家餐厅。规则变了：**只有几个服务员，但厨房有呼叫器。**

```
顾客A进门 → 服务员记下订单 → 传给厨房 → 给顾客A一个呼叫器 → 服务员立刻去接顾客B
顾客B进门 → 记订单 → 传厨房 → 给呼叫器 → 去接顾客C
...
[厨房做好A的菜] → 呼叫器响 → 服务员取菜端给A → 继续处理其他事情
```

服务员**从不站着等**，一直在处理事情。3 个服务员就能服务 300 个顾客。

这就是**事件循环（Event Loop）**。

"事件"指的是呼叫器响了、新顾客来了、有人要结账这类信号。"循环"意味着服务员一直在转，不停地看：有没有新顾客？有没有菜做好了？有没有人要结账？

| 餐厅里的角色 | 对应的程序概念 |
|:---|:---|
| 服务员 | 线程 |
| 顾客 | HTTP 请求 |
| 厨房做菜 | 数据库查询 / 外部 API 调用 |
| 服务员站着等菜 | 线程阻塞（blocking） |
| 呼叫器 | 回调 / 异步通知 |
| 服务员不停巡视 | 事件循环（Event Loop） |

---

## 三、一次请求的完整生命周期对比

假设用户请求「获取 Checklist 列表」，数据库查询耗时 50ms。

### MVC 的流程

```
t=0ms    请求进来，从线程池拿出线程#42
t=0ms    线程#42 执行代码，发送数据库查询
t=0ms    【线程#42 停下来等】← blocking，50ms 里什么都不做
t=50ms   数据库返回结果
t=50ms   线程#42 继续执行，组装数据，返回响应
t=51ms   线程#42 归还线程池
```

整个过程线程#42 被占用了 51ms，其中 50ms 在等待。**98% 的时间是浪费的。**

### WebFlux 的流程

```
t=0ms    请求进来，事件循环线程#1 接收
t=0ms    线程#1 发送数据库查询，注册回调（"查好了告诉我"），立刻去干别的
t=1ms    线程#1 接收了另一个请求，发出另一个查询...
t=50ms   数据库通知：第一个查询的结果来了（事件触发）
t=50ms   线程#1（或其他空闲线程）执行回调，组装数据，返回响应
```

线程#1 在这 50ms 里可能已经处理了几十个其他请求。

---

## 四、底层实现：从操作系统到你的代码

"事件循环"听起来很巧妙，但它到底是怎么做到的？分三层来看。

### 第一层：操作系统的 I/O 多路复用

这是整套机制的地基。操作系统提供了 `epoll`（Linux）和 `kqueue`（macOS）这类系统调用，它们的能力可以用一句话概括：

> "帮我同时盯着这 10000 个网络连接，哪个有数据来了，你通知我。"

操作系统在内核层面监控所有连接，当某个连接有数据到达时，通过中断通知你的程序。所以一个线程能"同时"处理上万个连接——它并不是真的同时处理，而是让操作系统帮它盯着，有动静再来处理。

### 第二层：Netty 的 EventLoop

WebFlux 默认使用 Netty 作为底层服务器。Netty 把操作系统的 epoll 封装成了 EventLoop：

```
┌─────────────────────────────────────────────┐
│              EventLoop 线程                  │
│                                             │
│  while(true) {                              │
│      events = epoll.poll()  // 问OS：有事吗？ │
│      for (event in events) {               │
│          event.handler()   // 处理这个事件    │
│      }                                      │
│  }                                          │
└─────────────────────────────────────────────┘
```

本质上就是一个死循环：不停地问操作系统"有什么新事件吗"，有了就处理，没有就继续等。线程不会阻塞在业务等待上，它只阻塞在 `epoll.poll()` 这一行——而这种阻塞是"等操作系统通知"，CPU 被释放出去了，跟"线程阻塞在数据库等待"的性质完全不同。

### 第三层：Project Reactor 的回调链

这是 WebFlux 开发者直接打交道的那一层。`Mono` 和 `Flux` 的本质是**一条提前注册好的回调函数链**。

```kotlin
val result = webClient.get("/api/data")   // 第1步
    .map { parse(it) }                    // 第2步
    .filter { it.isValid() }              // 第3步
    .subscribe { send(response, it) }     // 第4步
```

当你调用 `.subscribe()` 的那一刻，实际上你组装了这样一个结构：

```
┌───────────────────────────────────────────────────────┐
│  回调链（全部存在 JVM 堆内存里）                         │
│                                                       │
│  [发起HTTP请求] → 完成时执行 [parse]                    │
│                    → 完成时执行 [filter]                │
│                       → 完成时执行 [发送响应]            │
└───────────────────────────────────────────────────────┘
```

数据还没来，但"数据来了之后做什么"已经定义好了。当 Netty 的 EventLoop 收到操作系统通知，它取出数据，在当前线程上**按顺序同步执行整条回调链**。

所以整个过程是：等待 I/O 时是异步的（不占线程），I/O 完成后回调链在一个线程上顺序执行（不存在并发问题）。

---

## 五、"事件不会丢失吗？"

如果你用过 Kafka 或 RabbitMQ，可能会本能地担心：事件驱动模型不会丢消息吗？

答案是：WebFlux 的"事件"和 MQ 的"消息"**是完全不同的东西**。

| 对比维度 | Kafka/MQ 消息 | WebFlux 事件 |
|:---|:---|:---|
| 存在哪里 | 网络传输 + 磁盘持久化 | JVM 进程内存中 |
| 跨越什么 | 机器、进程、网络 | 同一个进程内的函数调用 |
| 丢失风险来源 | 网络故障、磁盘故障、进程崩溃 | 几乎没有"丢失"的概念 |
| 本质是什么 | 需要持久化的消息 | 已注册好的回调函数 |

Kafka 消息丢失，是因为消息要跨网络、写磁盘，中间任何一环断了就没了。WebFlux 的"事件"根本不离开你的 JVM——它就是内存里一条已经注册好的回调链。只要进程活着，回调链就在那里。

唯一会"丢失"的情况是 JVM 进程崩溃。但这时候 Spring MVC 处理到一半的请求也一样会丢——这是所有内存系统的共同特点，跟同步还是异步无关。

---

## 六、代码层面：从回调地狱到优雅的链式调用

理解了底层原理后，来看代码。如果直接用原始回调写异步逻辑，你会得到著名的**回调地狱**：

```kotlin
// 原始回调风格 —— 噩梦
fetchUser(userId) { user ->
    fetchPermissions(user.id) { permissions ->
        fetchSpace(permissions.spaceId) { space ->
            fetchChecklists(space.id) { checklists ->
                if (checklists.isNotEmpty()) {
                    saveAuditLog(user, space) { log ->
                        sendNotification(user) { _ ->
                            respond(checklists)
                        }
                    }
                }
            }
        }
    }
}
```

每一步嵌套在上一步的回调里，错误处理要在每一层单独写，debug 是灾难。

Reactor 的设计目标就是消灭这种嵌套。同样的逻辑用 Reactor 写：

```kotlin
// Reactor 链式风格 —— 线性阅读
fetchUser(userId)
    .flatMap { user -> fetchPermissions(user.id) }
    .flatMap { permissions -> fetchSpace(permissions.spaceId) }
    .flatMap { space -> fetchChecklists(space.id) }
    .filter { checklists -> checklists.isNotEmpty() }
    .flatMap { checklists -> saveAuditLog(...).thenReturn(checklists) }
    .flatMap { checklists -> sendNotification(...).thenReturn(checklists) }
    .subscribe { checklists -> respond(checklists) }
```

没有嵌套，从上往下线性阅读。每个 `flatMap` 的意思就是："上一步的结果来了，用它做下一件异步的事。"

### 你需要掌握的核心操作符

其实常用的就这么几个：

- `mono.map { }` — 同步变换值，比如把 JSON 解析成对象
- `mono.flatMap { }` — 异步变换值，返回另一个 Mono（比如拿到用户 ID 后去查权限）
- `flux.filter { }` — 过滤
- `flux.collectList()` — 把 `Flux<T>` 收集成 `Mono<List<T>>`
- `Mono.zip(a, b)` — 并行执行两个 Mono，等两个都完成
- `mono.onErrorReturn` — 出错时给默认值
- `mono.onErrorResume` — 出错时切换到另一条链

并行调用的场景尤其优雅：

```kotlin
// 并行调用两个外部 API，等两个都完成再组装
Mono.zip(
    fetchFixtures(year, month),    // 并行发出
    fetchCalendarEvents(month)     // 并行发出，不用等上面完成
).map { (fixtures, events) ->
    CalendarPageResponse(fixtures, events)
}
```

在 MVC 中实现同样效果需要手动管理线程池和 Future，WebFlux 里天然支持。

---

## 七、Debug 难题：真实存在，但有解

WebFlux 的 debug 体验确实不如 MVC 友好，这一点不回避。

**MVC 出错时的栈追踪：**

```
java.lang.NullPointerException
    at ChecklistService.getTemplates(ChecklistService.kt:42)   ← 一眼看到
    at ChecklistController.getTemplates(ChecklistController.kt:21)
```

**WebFlux 出错时的栈追踪：**

```
java.lang.NullPointerException
    at reactor.core.publisher.MonoFlatMap$FlatMapMain.onNext(MonoFlatMap.java:150)
    at reactor.core.publisher.FluxMap$MapSubscriber.onNext(FluxMap.java:122)
    ... 20行 Reactor 内部代码 ...
    ← 你自己的代码在哪？不知道
```

Reactor 提供了两种解决方案：

**方案一：在关键节点添加 checkpoint**

```kotlin
fetchUser(userId)
    .checkpoint("after fetchUser")
    .flatMap { fetchPermissions(it.id) }
    .checkpoint("after fetchPermissions")
    .flatMap { fetchSpace(it.spaceId) }
```

出错时日志会标记是哪个 checkpoint 之后出的问题。

**方案二：全局开启调试模式**

```kotlin
// 应用启动时添加，开发环境使用
Hooks.onOperatorDebug()
```

栈追踪会包含你的代码位置，但有性能开销，仅建议在开发环境使用。

**方案三（推荐）：搭配 Kotlin 协程**

这是 Kotlin 项目的最佳实践——用 `suspend` 函数取代 Reactor 链式调用，代码看起来和同步一模一样，栈追踪也恢复正常：

```kotlin
// Kotlin 协程风格 —— 看起来和 MVC 几乎一样，实际是非阻塞的
@GetMapping
suspend fun getTemplates(@PathVariable spaceId: Long): List<ChecklistTemplateResponse> {
    return checklistService.getTemplates(spaceId)
}
```

关于 Kotlin 协程的具体用法和原理，我会在后续文章中详细展开。这里只需要知道：Spring WebFlux 完全支持协程，`Mono<T>` 和 `suspend fun(): T` 可以互转，两种风格可以混用。

---

## 八、"开一个线程不也能异步吗？"——一个关键的认知修正

学到这里，你可能会想：我不用 WebFlux，自己开个线程池来查数据库，查完了回调通知主线程，不也是异步吗？

方向没错，但有一个本质区别：**开新线程 ≠ 非阻塞 I/O**。

```
线程池 + 回调方案：

主线程              工作线程#42
  │                    │
  │── 把查询扔给线程池 ──▶│
  │                    │ ← 线程#42 在这里阻塞等待数据库
  │                    │ ← 活着，占内存，但什么都不做
  │                    │
  │◀── 回调通知结果 ────│
```

线程还是在等，只是换了一个线程来等。500 个并发查询，还是需要 500 个线程干等。你只是把"谁在等"从主线程换成了工作线程，**线程总数没有减少**。

```
WebFlux 真正做的（OS 级非阻塞 I/O）：

EventLoop线程         操作系统内核
  │                       │
  │── 发出查询，注册兴趣 ──▶│
  │                       │ ← 内核在等，不是任何线程在等
  │── 去处理其他请求        │
  │── 去处理其他请求        │
  │── 去处理其他请求        │
  │                       │ 数据来了
  │◀── 中断通知 ───────────│
  │ 继续处理这个请求
```

等待下沉到了**操作系统内核层面**，没有任何应用层线程在等。500 个并发查询，只需要几个 EventLoop 线程轮转处理。

一句话概括：WebFlux 的本质优势不是"异步回调"（线程池也能做），而是**把 I/O 等待彻底下沉到操作系统，让应用层线程永远不空等**。

---

## 九、什么时候该用 WebFlux，什么时候不该

WebFlux 并不是 Spring MVC 的"升级版"。它是一个不同的工具，解决不同的问题。

| 场景 | 等待时间 | 并发量 | 推荐方案 |
|:---|:---|:---|:---|
| 普通 CRUD | 中（10~50ms） | 一般 | MVC 完全够用 |
| 调用第三方 API | 高（100ms~数秒） | 低 | MVC 也够用 |
| 实时消息推送（SSE / WebSocket） | 极高（连接长时间保持） | 高 | WebFlux 优势明显 |
| 万级 QPS 高并发服务 | 中 | 极高 | WebFlux 优势明显 |
| 聚合多个下游 API | 高 | 中 | WebFlux 并行调用有优势 |
| 大文件流式传输 | 高 | 中 | WebFlux 背压机制有优势 |

### 迁移成本也要考虑

如果你当前的项目使用了 Spring Data JPA，迁移到 WebFlux 意味着需要将数据库层替换为 **R2DBC**（Reactive Relational Database Connectivity），因为 JPA 是阻塞的，在 WebFlux 中使用会阻塞事件循环线程，反而更慢。而 R2DBC 不支持 JPA 的 `@Entity`、`@ManyToMany` 这类关联映射，复杂查询需要手写。

此外，Spring Security 的配置也需要重写（`ReactiveSecurityContextHolder` 替代 `SecurityContextHolder`），Flyway 在 R2DBC 模式下的支持也有限。

### 低风险的入门方式

如果你想在现有 MVC 项目中学习响应式编程，最好的切入点是使用 `WebClient` 替换外部 HTTP 调用。`WebClient` 是 WebFlux 提供的非阻塞 HTTP 客户端，可以独立用在 MVC 项目里，不需要全面迁移：

```kotlin
val webClient = WebClient.create("https://api.example.com")

fun getDataReactive(): Mono<List<DataResponse>> {
    return webClient.get()
        .uri("/endpoint")
        .header("Authorization", "Bearer $token")
        .retrieve()
        .bodyToMono(JsonNode::class.java)
        .map { parseResponse(it) }
}
```

---

## 十、总结

如果用一段话概括这篇文章的核心：

Spring MVC 给每个请求分配一个专属线程，简单直观，但线程数量是天花板。Spring WebFlux 用极少的线程配合事件循环，让线程从不空等——代价是代码风格从"顺序执行"变成"定义流水线"。底层依赖操作系统的 I/O 多路复用、Netty 的 EventLoop 封装、以及 Project Reactor 的回调链抽象，三层配合让"等待"这件事彻底下沉到了操作系统内核。

选择 MVC 还是 WebFlux，不是"新旧"的问题，而是**你的场景是否存在大量 I/O 等待 + 高并发压力**的问题。大多数 CRUD 应用，MVC 完全够用。但当你需要处理万级并发、长连接推送、或多下游聚合时，WebFlux 提供的非阻塞模型会让你的服务器资源利用率提升一个数量级。

而如果你用的是 Kotlin，`WebFlux + Coroutines` 的组合可以让你兼得两个世界的好处：非阻塞的性能，加上同步代码的可读性。关于 Kotlin 协程如何与 WebFlux 深度结合，我们下篇文章再聊。

---

### 推荐学习路径

1. **Reactor 互动教程** — [projectreactor.io/learn](https://projectreactor.io/learn)，30 分钟跑完，强烈推荐作为第一站
2. **Reactor Reference Guide** — 官方文档的第 3、4 章讲核心概念
3. **Spring WebFlux 官方文档** — 写得比大多数书好，且与你使用的 Spring Boot 版本同步
4. **在现有项目中用 WebClient 替换一个外部 HTTP 调用** — 低风险的实战练习
5. ***Hands-On Reactive Programming in Spring 5*** — 目前最系统的一本书，从 Reactor 讲到 WebFlux