# Cookies
## Cookeis特性
### 前端数据存储
### 后端通过http头设置
### 请求时通过http头传给后端
### 前端也可以读写Cookies
### 遵循同源策略（CORS）

## Cookies属性
### 域名(Domain) - Cookie属于哪一个网站
### 有效期(Expires)
### 路径(Path) - Cookie可以作用于网站的哪一级
### http-only - Cookies只能被http协议所使用
### secure - Cookies是否只能在https协议中使用

## Cookies应用
### 存储个性化的设置
### 存储未登录时用户的唯一标识
### 存储已登录用户的凭证
### 存储其他的业务数据

## Cookies - 登录用户凭证
1. 前端提交用户名和密码
2. 后端验证用户名和密码
3. 后端通过http头设置用户凭证
4. 后续访问时后端先验证用户凭证

## Cookies和XSS的关系
1. XSS可能窃取Cookies中的数据
2. http-only的Cookie不会被Javascript代码

## Cookies和CSRF的关系
1. CSRF利用用户的Cookies
2. 第三方网站是无法读写Cookies的，它只能携带Cookies去发送请求。
3. 最好能阻止第三方使用Cookies

