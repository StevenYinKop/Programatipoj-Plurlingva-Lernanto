---
title: webpack1-简单配置,devServer,hash bundle
url: https://www.yuque.com/stevenyin/liv/gx4g5r
---

<a name="a67129c2"></a>

# Webpack(一)

<a name="5332daa3"></a>

## Webpack 是什么

本质上，`webpack` 是一个现代 `JavaScript` 应用程序的静态模块打包器(`module bundler`)。当 `webpack` 处理应用程序时，它会递归地构建一个依赖关系图(`dependency graph`)，其中包含应用程序需要的每个模块，然后将所有这些模块打包成一个或多个 `bundle。`(From [here](https://www.webpackjs.com/concepts/))

说白了, 它可以进行: 代码转换, 文件优化, 代码分割, 模块合并, 自动刷新, 代码校验, 自动发布

\##Webpack 安装

安装本地的 `webpack`

```sh
  npm install webpack webpack-cli -D 或者 yarn add webpack webpack-cli -D
```

`-D` 代表当前是开发依赖, 上线以后不需要使用

<a name="ee10aaa4"></a>

## Webpack 可以零配置

- `webpack` 是一个打包工具, 把所有资源按照文件入口进行打包
- 默认支持 Js 的模块, 所以如果不加任何配置, 想要打包 `css` 以及其他的资源的话会报错.
- 在零配置的情况下, 我们直接在项目的根目录执行

```sh
  npx webpack
```

`npx` 是 `npm5.2` 的新命令, 具体作用可以参考阮一峰老师的博客: <http://www.ruanyifeng.com/blog/2019/02/npx.html>

执行上面的命令等价于执行这个 `cmd` 命令: `node_modules/bin/webpack.cmd`

```bat
  @IFEXIST "%~dp0\node.exe" (
    "%~dp0\node.exe"  "%~dp0\..\webpack\bin\webpack.js" %*
  ) ELSE (
  @SETLOCAL
  @SET PATHEXT=%PATHEXT:;.JS;=;%
  node  "%~dp0\..\webpack\bin\webpack.js" %*
  )
```

<a name="2549d8ef"></a>

## Webpack 手动配置

- 默认配置文件的名字: **webpack.config.js**
- `webpack` 是 `node` 编写的, 所以我们要使用 `node` 的语法

```javascript
  let path =require('path')
  module.exports = {
    mode: 'development',  // 可选值: 'production '| 'development',
    entry: './src/index.js' // 入口文件
    output: {
      filename: 'bundle.js', // 打包后的文件名
      path: path.resolve(__dirname, 'dist'), // 路径必须是一个绝对路径, 所以需要node的path模块的帮助, 使用path.resolve方法解析路径
    }
  }
```

每当我们写好代码, 想要打包的时候, 只需要在 `webpack.config.js` 中配置好相应的配置项, 然后执行 `webpack` 命令就好了, 比如上面的代码就会去寻找`./src/index.js` 文件作为入口文件, 然后和这个文件相关的所有依赖都会被打包到`./dist/bundle.js` 这个文件中. 这个文件可以直接在 `HTML` 中使用 `script` 标签引用执行.

如果我们想要更改文件名的话, 比如改成 `webpack.config.cincommon.js`, 这样默认 `webpack` 是不会读取的, 需要在执行 `webpack` 命令的时候添加一个参数:

```sh
 webpack --config webpack.config.cincommon.js
```

`webpack` 就会去寻找这个文件当做配置文件. 当然我们也可以把这条命令配置到 `package.json` 的 `script` 属性下:

```javascript
  // package.json
  "script" : {
    "build": "webpack -- --config webpack.config.cincommon.js"
  }
```

注意这里的写法, 比上面多了"`--`", 因为在 `package.json` 的配置中, 如果需要传递参数, 则需要写在`--`的后面, 这样的话 `node` 在执行的时候会认为后面的是需要传递给 `webpack` 的参数.

<a name="62522b38"></a>

## webpack 内置了开发服务

安装开发依赖:

```sh
npm install webpack-dev-server -D 或者 yarn add webpack-dev-server -D
```

`webpack-dev-server` 是一个开发时服务器, 内置了 `express`, 执行时不会对代码进行打包, 而是直接起一个 `node` 服务器, 把代码跑上去. 也就是把文件写到内存中(内存中打包)

默认配置的 `webpack-dev-server` 会跑在 `8080` 端口下, 而且基于项目的根目录`/`

自定义 `webpack-dev-server`, `webpack` 的配置里面加入一个属性:

```javascript
module.exports = {
  ...
  devServer: {
    port: 3000, // 指定端口号
    progress: true, // 显示进度条
    contentBase: './build', // localhost:3000对应着项目中的build目录
    compress: true,
  }
  ...
}
```

上面代码的作用, 可以启动一个 `express` 服务器, 以`/build` 目录作为服务器的根目录(`/`)

但是有一个问题, 当前使用的 `index.html` 文件实际上并不是一开始就存在于 `build` 目录下的, 因为我们只对 `js` 进行了打包, `html` 文件并不会直接带进去, 这个时候就用到一个 `webpack` 的插件: `html-webpack-plugin`, 先安装一下这个插件

```sh
  npm install html-webpack-plugin -D 或者 yarn add html-webpack-plugin -D
```

然后在 `webpack.config.js` 中引入这个插件

```javascript
  let HtmlWebpackPlugin = require('html-webpack-plugin')
  module.exports = {
  ...
    plugins: [
      new HtmlWebpackPlugin({
        template: './src/index.html', // 源文件路径
        filename: 'index.html', // 拷贝文件到指定build目录, 文件名为index.html
        minify: { // 压缩html
          removeAttributeQuotes: true, //删除html中的引号
          collapseWhitespace: true, // 删除换行
        },
        hash: true, //为js文件添加hash戳,
      })
    ]
  ...
}
```

除了使用插件中的 `hash: true` 来添加 `hash` 值以外, 还可以在上面配置 `output` 的时候, 直接指定生成的文件带有 `hash` 值:

```javascript
  module.exports = {
    ...
    output: {
      filename: 'bundle.[hash].js', // 表示生成的文件名中带有hash值
      // 或者这样写↓
      filename: 'bundle.[hash:8].js', // 表示生成的文件名中带有hash值, 并且只有8位
    },
    ...
  }
```

这样的话再 `build` 的时候生成的 `bundle` 文件就会带有一个 `hash` 值在文件名中, 避免了出现缓存的情况.
