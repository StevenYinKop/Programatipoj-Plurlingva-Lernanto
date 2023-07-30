---
title: webpack2-CSS相关插件
url: https://www.yuque.com/stevenyin/liv/otx44i
---

<a name="9453dee7"></a>

# Webpack(二)

`Wepack` 在不做任何额外配置的情况下只支持打包 `js` 模块,

先随便写一个 `index.css`:

```css
  body {
    background: red;
  }
```

然后把这个 `CSS` 在我们的 `js` 中引用:

```javascript
  require("./index.css")
```

这个时候我们使用 `webpack` 打包

```sh
npx webpack
```

打包会出现错误:

```sh
ERROR in ./src/a.css 1:5
Module parse failed: Unexpected token (1:5)
You may need an appropriate loader to handle this file type.
> body {
|   background: red;
| }
 @ ./src/index.js 2:0-18
```

很明显这里要求我们要找一个正确的 `loader` 去处理这个文件类型(`.css`)

我们这里使用两个 `loader`:

- [css-loader](https://www.npmjs.com/package/css-loader): **用来处理 `CSS` 中的`@import` 语法**
- [style-loader](https://www.npmjs.com/package/style-loader): **用来把 `CSS` 插入到 `head` 标签中**

  之所以分成两个 `loader` 也是希望每一个 `loader` 的功能尽可能的单一.

  在 `webpack` 的配置文件中追加如下配置:

```javascript
  module.exports = {
    ...
    module: {
      rules: [
        {test: /\.css$/, use: [ 'style-loader', 'css-loader' ]}, // 匹配以.css结尾的文件
      ]
    }
    ...
  }
```

`use` 的参数可以为:

- 字符串: 表示只写一个 `loader` 比如:

```javascript
  {test: /\.css$/, use: 'css-loader'}
```

- 数组: 可以写多个 `loader`, `loader` 的执行顺序是从右向左, 从下向上, 比如:

```javascript
  {test: /\.css$/, use: ['style-loader', 'css-loader']}
```

**这样会先执行 `css-loader`, 再去执行 `style-loader`**

- 对象: 对象其实是数组的增强版, 它在加载 `loader` 的基础上, 还可以添加一些额外的 `loader` 参数, 比如 `style-loader` 的 `options: {insertAt: 'top'}`等参数.下面再具体展开,

```javascript
  rules: [
    {
      test: /\.css$/,
      use: [
        {
          loader: 'style-loader',
          options: {
            insertAt: 'top', // 将CSS插入在head标签的上面, 这样的话我们自己写一些样式可以覆盖掉这些打包后的样式.
          }
        },
        'css-loader'
      ]
    }
  ]
```

当然别忘了安装一下这两个 `loader`:

```sh
  npm install css-loader style-loader --save-dev 或者 yarn add css-loader style-loader -D
```

然后再执行

```sh
npx webpack
```

这样的话就不会再报错了, 而且 `CSS` 文件也可以正确的加载.

<a name="f9de3bf4"></a>

## 使用 `CSS` 预处理器

同样, 如果使用了 `CSS` 预处理器, 也需要添加 `loader`,

`less` -> [less-loader](https://www.npmjs.com/package/less-loader)

`sass` -> [sass-loader](https://www.npmjs.com/package/sass-loader)

`stylus` -> [stylus-loader](https://www.npmjs.com/package/stylus-loader)

比如我们在项目中添加一个 `sass` 的预处理器, 首先要先安装 `sass` 和 `sass-loader` 的依赖

```sh
  npm install node-sass sass-loader --save-dev 或者 yarn add node-sass sass-loader -D
```

安装完成后在配置文件的 `module.rules` 下继续添加:

```javascript
  rules: [
    ...
    {
      test: /\.scss$/,
      use: [
        {
          loader: 'style-loader',
          options: {
            insertAt: 'top', // 将CSS插入在head标签的上面, 这样的话我们自己写一些样式可以覆盖掉这些打包后的样式.
          }
        },
        'css-loader',
        'sass-loader',
      ]
    }
  ],
```

<a name="MiniCssExtractPlugin"></a>

## MiniCssExtractPlugin

按照上面的配置, 打包出来的 `css` 全部会堆积到 `template` 的 `head` 中. 如果我们想要把 `CSS` 单独抽离成 `css` 文件, 并且以 `link` 的形式引用的话, 这样需要用到另一个插件(`plugin`): [**mini-css-extract-plugin**](https://www.npmjs.com/package/mini-css-extract-plugin)

先安装:

```sh
  yarn add mini-css-extract-plugin -D
```

在配置文件中引入这个插件:

```javascript
  var MiniCssExtractPlugin = require('mini-css-extract-plugin')
```

然后在 `plugins` 下添加这个插件(插件并没有先后执行的顺序, 可以随意放):

```javascript
  plugins: [
    ...,
    new MiniCssExtractPlugin({
      filename: 'main.css'
    })
  ]
```

配置好之后我们想想之前使用的 `style-loader`, 作用是把 `CSS` 插入到 `head` 标签中, 而这个插件是将 `CSS` 打包成一个`.css` 文件, 然后通过 `link` 的形式引入进来, 这两个功能实际上是冲突的, 所以我们如果要使用 `style-loader`, 则不要使用 `mini-css-extract-plugin`, 现在使用 `mini-css-extract-plugin` 的话, 我们要把之前配置的 `module` 里面的 `style-loader` 用 `mini-css-extract-plugin` 的 `loader` 替换掉:

```javascript
  rules: [
    {
      test: /\.css$/,
      use: [
        MiniCssExtractPlugin.loader,
        'css-loader'
      ]
    }
  ]
```

这样一来我们再进行 `build` 的时候就可以把 `css` 文件单独生成在 `main.css` 中, 并且 `link` 到 `template` 标签中了.

<a name="c0120e2c"></a>

## 浏览器前缀

以上的处理已经可以实现打包, 编译 `scss` 等, 但是当我们使用 `transform` 等属性时需要加上浏览器前缀, 比如:

```css
  div {
    transform:rotate(7deg);
    -ms-transform:rotate(7deg); /* IE 9 */
    -moz-transform:rotate(7deg); /* Firefox */
    -webkit-transform:rotate(7deg); /* Safari 和 Chrome */
    -o-transform:rotate(7deg);  /* Opera */
  }
```

而我们上述的打包, 并不能够添加这些前缀信息, 导致我们需要重复编写上面的代码, 所以我们可以使用[autoprefixer](https://www.npmjs.com/package/autoprefixer)来添加前缀, 当然使用这个包的前提是需要使用[postcss-loader](https://www.npmjs.com/package/postcss-loader)来加载.

安装:

```sh
  npm install autoprefixer postcss-loader --save-dev 或者 yarn add autoprefixer postcss-loader -D
```

然后在 `module.rules` 中, **之前写好的配置项中间**添加上 `postcss-loader`

```javascript
  rules: [
    {
      test: /\.css$/,
      use: [
        MiniCssExtractPlugin.loader,
        'css-loader',
        'postcss-loader',
      ]
    }
  ]
```

运行**npx webpack**进行打包, 结果并没有成功, `webpack` 报了一个错

```sh
  Error: No PostCSS Config found in: /usr/project/src
```

它在项目的根目录下没有找到相应的 `postcss` 的配置文件.我们在项目的根目录下新建一个 `postcss.config.js`,

在这个文件中我们写入:

```javascript
  module.exports = {
    plugins: [require('autoprefixer')],
  }
```

再次运行**npx webpack**, 打包成功.

<a name="2e57a29f"></a>

## 压缩 `CSS`

之前使用了**html-webpack-plugin**中的**minify**配置, 可以实现对 `html` 的压缩,

我们也可以使用另一个插件[**optimize-css-assets-webpack-plugin**](https://www.npmjs.com/package/optimize-css-assets-webpack-plugin)对 `CSS` 进行压缩

安装

```sh
  yarn add optimize-css-assets-webpack-plugin -D
```

在配置文件中引入这个插件并且使用它:

```javascript
  var OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')
  module.exports = {
    ...
    optimization: {
      minimizer: [ // 这里是个数组, 因为可能会有很多优化项
        new OptimizeCssAssetsWebpackPlugin()
      ],
    }
    ...
  }
```

配置完成后, 执行 `npx webpack` 的时候, 这个时候发现 `CSS` 文件已经成功压缩了, 但是问题来了, `JS` 文件之前是可以正常压缩的, 结果现在不灵了, 查看文档后发现, 如果我们使用了 `optimize-css-assets-webpack-plugin` 插件, 就一定要使用[uglifyjs-webpack-plugin](https://www.npmjs.com/package/uglifyjs-webpack-plugin)来对 `js` 进行压缩...一堆坑...

只能再安装 `uglifyjs-webpack-plugin` 了

```sh
  yarn add uglifyjs-webpack-plugin -D
```

在配置文件里面使用:

```javascript
  var OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')
  var UglifyjsWebpackPlugin = require('uglifyjs-webpack-plugin')
  module.exports = {
    ...
    optimization: {
      minimizer: [ // 这里是个数组, 因为可能会有很多优化项
        new UglifyjsWebpackPlugin({
          cache: true, // 启用缓存
          parallel: true, // 并行打包, 默认并发数: os.cups().length - 1
          sourceMap: true, // 使用sourceMap将错误位置映射到具体模块, 当我们把ES的高级语法编译为JS后, 再调试时它能够定位到我们源文件(高级语法的位置)
        }),
        new OptimizeCssAssetsWebpackPlugin()
      ],
    }
    ...
  }
```
