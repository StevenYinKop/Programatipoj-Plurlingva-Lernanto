
## XSS攻击注入点
- HTML 节点内容
```html
<div>
#{content}
</div>
```
- HTML属性
```html
<img src="#{image}">
<!-- const image="1\" onerror=\"alert(1)"; -->

<img src="1" onerror="alert(1)"/>
```
- JavaScript代码
```javascript
<script>
	var data = "#{content}";
	// const content = "hello\";alert(1);";
	var data = "hello";alert(1);"
</script>
```

- 富文本
1. 富文本会保留HTML
2. HTML就会存在XSS攻击的风险



## 如何防御XSS攻击
- 浏览器自带防御，可以通过`set("X-XSS-Protection", 0);`关闭防御。
1. 它能够拦截参数中出现HTML内容或者属性的XSS攻击，但是无法检测到JavaScript的代码和富文本中出现的情况。
2. 并不是所有浏览器都支持这样的防御机制，不能完全依赖这种方式来解决XSS攻击;
- 进行HTML转义：如`<`转义为：`&lt;`, `>`转义为：`&gt;`，这样程序就不会把这些符号当作是有效的HTML标签 
- 解决HTML属性的XSS攻击，转义双引号`"`, 单引号`'`等，防止其属性内容被拆分。
- 对JavaScript的code进行JSON.stringify(), 用于转义所有非法字符。以JavaScript中XSS攻击带来的问题。
- 对富文本中可能出现的所有标签进行白名单化管理，在富文本的数据存储前，对所有标签进行过滤。
1. 
```javascript
const whitelist = {
	"img": ["src"],
	"font": ["color", "size"],
	"a": ["href"]
};

$("*").each((index, elem) => {
	if (!whitelist[elem.name]) {
		$(elem).remove();
		return;
	}
	
	for (var attr in elem.attribs) {
		if (whitelist[elem.name].indexOf(attr) === -1) {
			$(elem).attr(attr, null);
		}
	}
});
```
2. 白名单定义的不好可能会对业务产生影响。
- 使用一些开源的xss js脚本

## CSP(Content Security Policy) - 用于指定哪些内容可以执行
- 是一个http的header
- child-src connect-src default-src
- font-src frame-src img-src
- manifest-src media-src object-src
- script-src style-src worker-src

- <host-source> <scheme-source> 'self'
- 'unsafe-inline' 'unsafe-eval' 'none'
- 'nonce-<base64-value>' '<hash-source>`
- 'strict-dynamic'

Content-Security-Policy: default-src 'self' http://google.com; connect-src 'none'

