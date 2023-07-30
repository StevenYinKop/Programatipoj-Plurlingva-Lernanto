---
title: webpack5-集成JQuery
url: https://www.yuque.com/stevenyin/liv/olghny
---

<a name="dc066c01"></a>

# 引入第三方模块和全局变量(如 JQuery)

<a name="e3f9b848"></a>

## 安装 JQuery

```sh
yarn add jquery
```

在代码中引入 `jquery`

```javascript
import $ from 'jquery';
console.log($);
console.log(window.$);
```

`npx webpack`打包代码, 打开浏览器.`F12`

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/17/01.png#alt=Alt%20text)

从打印的结果来看, 我们可以看到, `console.log($)`可以正确打印出$的值, 是一个函数, 而`console.log(window.$)`则打印出了`undefined`;

我们引用的模块并不会挂在到 window 下, 也就是不能直接使用.

这个时候我们可以使用[expose-loader](https://webpack.docschina.org/loaders/expose-loader/)来将模块暴露到全局上.

<a name="0eeab1d8"></a>

## 使用 expose-loader

我们把上面引入的`import $ from 'jquery'`修改一下: `import $ from 'expose-loader?$!jquery'`.

这个语法看起来很奇怪, 实际上可以这样分解:

```javascript
expose-loader // 使用expose-loader
?$!
jquery // 将jquery以上面$的变量名暴露为全局变量
```

如果感觉`?$!`看着很奇怪不妨这样: `expose-loader?jquery!jquery`, 这代表着我们把`jquery`命名为`jquery`, 暴露在`window`中.

先测试这样一段代码:

```javascript
/** 这个import相当于是
 *	window.$= require('jquery');
 *	const $ = window.$
 */
import $ from 'expose-loader?$!jquery'
console.log($)
console.log(window.$)
```

我们安装`expose-loader`, 然后打包执行看一下效果

    yarn add expose-loader -D
    npx webpack

这一段代码的执行结果, 就会是这样:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/17/02.png#alt=Alt%20text)

也就是说很明显, `window` 下已经有一个全局的`$`, 我们可以直接使用了.

把代码改成下面这个样子重新`npx webpack`

```javascript
/** 这个import相当于是
 *	window.jquery = require('jquery');
 *	const $ = window.jquery
 */
import $ from 'expose-loader?jquery!jquery'
console.log($)
console.log(window.$)
console.log(window.jquery)
```

所以这里的显示结果也显而易见了:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/17/03.png#alt=Alt%20text)

这种写法可以很容易地将变量绑定在 `window` 上.但是写法总感觉有点恶心, 又是`?`又是`!`的.

所以我们还可以把这个 `loader` 写在 `webpack` 的配置中:

```javascript
  rules: [
  ...
    {
      test: require.resolve('jquery'), // require.resolve是node中的函数, 这个函数用来获得模块的绝对路径, 用来添加在全局中
      use: 'expose-loader?$', //这个后面可以加!jquery, 加的话会不生效, 用法可参见文档
    },
...
```

添加完成`loader`后, 我们把代码修改一下

```javascript
import $ from 'jquery'
console.log('$ = ', $)
console.log('window.$ = ', window.$)
console.log('window.jquery = ', window.jquery)
```

再`npx webpack`查看浏览器中的结果

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/17/04.png#alt=Alt%20text)

结果可以正确地读取`window`中的`$`. 但是这个时候, 我们要在代码的前面`import $ from 'jquery'`.

<a name="651561db"></a>

## 为每一个模块注入 `JQuery`

我们可以使用上面的`expose-loader`来将变量添加到`window`下, 另一种方式, 则是将 `jquery` 直接注入到每一个模块中, 我们要使用 `Webpack` 中内置的插件来完成这件事情:

```javascript
  let webpack = require('webpack');
  module.exports = {
    ... 其他的配置
    plugins: [
      ...其他的插件
      new webpack.ProvidePlugin({
        $: 'jquery', // 将jquery使用$进行注入
      }),
      ...其他的插件
    ],
    ... 其他的配置
  }
```

配置完成后我们编写一下测试代码:

```javascript
  console.log('$ = ', $)
```

我们可以看到下面的结果, 也就是我们的`$`注入是成功的.

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/17/05.png#alt=Alt%20text)
