# CSRF
## Cross Site Reuqest Forgery(跨站请求伪造)
利用Cookie保存了用户的身份

用户打开了一个第三方网页，可视的内容是人畜无害的。但是我回到原来的网页时，在原网站上以我的名义做了一系列我所不知情的操作。(`one click attack`)

### POST请求需要构造form表单进行。
一旦用户的浏览器被弹窗，攻击者就可能利用这样一个隐藏的`iframe`以当前用户的名义进行一系列的操作。

`form`的`target`如果是一个`iframe`的`name`的话，表单会在`iframe`页面中进行提交和跳转。但是`iframe`的`display`是`none`，所以这个过程对用户是不可见的。
```html
<body>
<script>
    document.write(`
    <form name="commentForm" target="iframe_name" method="post" action="http://bankserver/post/transferMoney">
        <input name="postId" type="hidden" value="stevenyin" />
        <textarea name="amount">10000</textarea>
    </form>
    `);
    var iframe = doc  ument.createElement('iframe');
    iframe.name = 'iframe_name';
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    setTimeout(function() {
        document.querySelector('[name=commentForm]').submit();
    }, 1000);
</script>
</body>
```
### Get请求相对更容易一些，只需要构造请求的URL和params
```html
<body>
<a href="http://bankserver/transfer?clientId=111&amount=10000&description=stupidDesign">
    Click me to get money!
</a>
</body>
```
只要用户点击了这个链接，就会通过GET请求向服务器发送get请求。

### 不需要点击也可以攻击
```html
<body>
<img src="http://bankserver/transfer?clientId=111&amount=10000&description=stupidDesign" />
</body>
```
这样的话用户甚至不需要点击任何的事情，只要访问页面，就会遭到攻击。

### 配合XSS攻击，向页面中插入链接 
```html
<body>
<img src="http://bankserver/addComment?comment=<a href='https://some.phishing.websites/click_and_delete_all_your_data_!'>Click me!</a>" />
</body>
```
一旦执行成功，用户会在源网站发布一条评论，所有点击评论中链接的其他用户，都会被里面设计的一些恶意代码波及到。

## CSRF攻击的危害
- 利用用户的登录态
- 用户并不知情
- 完成业务请求

- 盗取用户资金
- 冒充用户发帖背锅
- 损坏网站名誉


## CSRF攻击的防御方式
### CSRF攻击的原理
1. `user`在A网站进行登录
2. A网站认证了`user`的身份，并且使用`Cookie`保存了用户态
3. B网站通过构造链接、隐藏表单等方式，携带A网站的`Cookie`，冒充`user`对A网站进行访问。以达到目的。

### 从CSRF攻击中的几个关键点入手
1. B网站向A网站发送请求
2. 带A网站的`Cookie`
3. 这个请求不会走A网站的前端
4. `http headers`的`referer`中包含B网站的信息

### 防御方式
1. 设置`Cookie`的`sameSite`属性为`strict`，意思是从第三方网站发送到A网站的请求不会将`cookie`一并携带至服务器。
   - 弊端：1. 浏览器的支持不够完善。2. 如果服务器支持匿名用户的一些操作，B网站仍然可以向A网站发送钓鱼链接并且成功绕过验证。
2. 在A网站的前端加入一些验证信息
   1. 前后端进行改造以增加验证码的功能。
      - 弊端：会影响一些用户体验。
   2. 前端加入token，生成一个随机字符串，让攻击者发起请求时，没有办法获得到这个token，每一次提交时用这个token来进行验证。
      - 后端生成token，返回给前端
      - 前端将token存在cookie和另一个可以获得的地方（如input-hidden或meta等）。
      - 表单提交时，后端校验cookie中的token和表单提交的token进行校验。
3. 验证referer是不是来自自己的前端网站，禁止来自第三方网站的请求。
