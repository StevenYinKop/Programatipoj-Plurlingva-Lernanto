---
title: webpack7-集成SourceMap
url: https://www.yuque.com/stevenyin/liv/gogchg
---

<a name="26794a4e"></a>

# 打包多页应用与 SourceMap

<a name="e300b59b"></a>

## 单页面应用 vs 多页面应用

在 `SPA` 应用流行的今天, 多页面应用似乎在纯前端开发中渐渐淡出视线, 但是多页应用依然有它的优势.

我在网上找到了一篇[博客](https://juejin.im/post/5a0ea4ec6fb9a0450407725c)(<https://juejin.im/post/5a0ea4ec6fb9a0450407725c>)

|  |  | 单页面应用(`SPA`) | 多页面应用(`MPA`) |
| --- | --- | --- | --- |
| 组成 | 一个外壳页面和多个页面片段组成 | 多个完整页面构成 |  |
| 资源共用(`css`,`js`) | 共用，只需在外壳部分加载 | 不共用，每个页面都需要加载 |  |
| 刷新方式 | 页面局部刷新或更改 | 整页刷新 |  |
| url 模式 | a.com/#/pageone a.com/#/pagetwo | a.com/pageone.html a.com/pagetwo.html |  |
| 用户体验 | 页面片段间的切换快，用户体验良好 | 页面切换加载缓慢，流畅度不够，用户体验比较差 |  |
| 转场动画 | 容易实现 | 无法实现 |  |
| 数据传递 | 容易 | 依赖 `url` 传参、或者 `cookie` `、localStorage` 等 |  |
| 搜索引擎优化(`SEO`) | 需要单独方案、实现较为困难、不利于 `SEO` 检索 可利用服务器端渲染(`SSR`)优化 | 实现方法简易 |  |
| 试用范围 | 高要求的体验度、追求界面流畅的应用 | 适用于追求高度支持搜索引擎的应用 |  |
| 开发成本 | 较高，常需借助专业的框架 | 较低 ，但页面重复代码多 |  |
| 维护成本 | 相对容易 | 相对复杂 |  |

<a name="ff362b7c"></a>

## 使用 webpack 打包多页面应用

我们新建一个新的项目, 来配置多页面应用的打包:

使用`npm init`来新建项目, 这个过程比较简单.新建完成后得到一个 `package.json` 文件. 安装一下 `webpack` 相关依赖:

`npm install webpack webpack-cli --save-dev`或者`yarn add webpack webpack-cli -D`

然后编写`webpack.config.js`

```javascript
  let path = require('path')
  module.exports = {
    entry: {
      // 一个叫做home的入口文件, 文件位置在'./src/index.js',
      home: './src/index.js',
      // 另一个叫做another的入口文件, 文件位置在'./src/another.js',
      another: './src/another.js',
    },
    output: {
      // 代表entry里面的属性名, 也就是说打包出来的文件会变成俩,
      // 一个是home.js, 一个是another.js
      // 如果把这里的文件名写死成一个文件, 类似于之前的那种bundle.js的话,
      // 程序会报错, 因为从两个入口不能直接合并成同一个文件
      filename: '[name].js',
      // 打包到项目的dist路径下
      path: path.resolve(__dirname, 'dist')
    },
  }
```

我们需要新建这样的文件目录:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556106365141.png#alt=Alt%20text)

编写完成后我们打包`npx webpack`看看效果:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556106447145.png#alt=Alt%20text)

两个文件进行打包了, 现在我们打包了还不够, 像之前讲的那样需要把它们引入到对应的 html 中, 我们安装一下[HtmlWebpackPlugin](https://webpack.js.org/plugins/html-webpack-plugin/)插件.

`npm install --save-dev html-webpack-plugin`或者 `yarn add html-webpack-plugin -D`

在`webpack.config.js`中添加插件:

```javascript
  let path = require('path')
  let HtmlWebpackPlugin = require('html-webpack-plugin')
  module.exports = {
    entry: {
      // 一个叫做home的入口文件, 文件位置在'./src/index.js',
      home: './src/index.js',
      // 另一个叫做another的入口文件, 文件位置在'./src/another.js',
      another: './src/another.js',
    },
    output: {
      // 代表entry里面的属性名, 也就是说打包出来的文件会变成俩,
      // 一个是home.js, 一个是another.js
      // 如果把这里的文件名写死成一个文件, 类似于之前的那种bundle.js的话,
      // 程序会报错, 因为从两个入口不能直接合并成同一个文件
      filename: '[name].js',
      // 打包到项目的dist路径下
      path: path.resolve(__dirname, 'dist')
    },
    plugins: [
      // 先new一个HtmlWebpackPlugin, 它会将index.html拷贝到dist中并且命名为home.html
      new HtmlWebpackPlugin({
        template: './index.html',
        filename: 'home.html',
        // 关键代码: chunks会去寻找名为home.js的文件, 把它以<script>的形式引入到home.html中.
        // 如果不加入这句话的话, 那么打包出来的home.js和another.js都会被引入到home.html中, 也都会被引入到下面的another.html中
        chunks: ['home'],
      }),
      // 再new一个HtmlWebpackPlugin, 它会将index.html拷贝到dist中并且命名为another.html
      new HtmlWebpackPlugin({
        template: './index.html',
        filename: 'another.html',
        // 加入another.html中想要既引入home.js, 又引入another.js的话, 我们可以这样写
        // chunks: ['home', 'another'], 当然我们这里的需求并不是这样, 所以不做演示了
        chunks: ['another'],
      }),
    ],
  }
```

编写完成后打包`npx webpack`,看一下打包结果, 生成了两个 `html` 文件和两个 `js` 文件, 并且两个 `html` 文件分别引入了各自的 `js`.

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556107583186.png#alt=Alt%20text)

<a name="83cdb293"></a>

## [Devtool---SourceMap](https://webpack.js.org/configuration/devtool/)

在我们把代码打包后, 经过各种压缩, 去空格, `babel` 编译, 基本上原来 写的代码已经面目全非了, 要么在生产环境下被压缩成了一行, 要么一堆文件被打包到一起并且变量名也变掉了, 这个时候如果想要对代码进行调试, 只能感到深深的绝望.

`Devtool` 这个选项的作用就是:

> This option controls if and how source maps are generated.

> 这个选项用于控制是否要生成 SourceMap 和以怎样的方式生成 SourceMap.

> Choose a style of source mapping to enhance the debugging process. These values can affect build and rebuild speed dramatically.

> 我们可以使用一种 SourceMap 来提高我们 debug 的快感, 每一种 SourceMap 都有不同的作用.
>
> 下面是来自官网的各种 source-map 的比较

| devtool | build | rebuild | production | quality | comments |
| --- | --- | --- | --- | --- | --- |
| (none) | +++ | +++ | yes | bundled code | 不使用 devtool 时, 打包会出来的文件是一整个代码块, 不会根据模块分离成很多个部分. (我的理解就是像刚刚开始写代码时的那种写一个函数几百行) |
| eval | +++ | +++ | no | generated code | 相对于上面那种, 虽然代码可能写在同一个文件, 但是不同的模块会相互分离, 然后通过类似于 require 等方式引用 |
| cheap-eval-source-map | + | ++ | no | transformed code (lines only) | 代码也会根据模块进行拆分, 我们可以查看被 loader 翻译后, 被 webpack 打包前的代码, 只会标出错误的行数, 不会定位到具体的变量 |
| cheap-module-eval-source-map | o | ++ | no | original source (lines only) | 可以看到原始代码(自己写的代码), 只会标出错误的行数, 不会定位到具体的变量 |
| eval-source-map | -- | + | no | original source | 可以看到原始代码(自己写的代码) |
| cheap-source-map | + | o | yes | transformed code (lines only) | 代码也会根据模块进行拆分, 我们可以查看被 loader 翻译后, 被 webpack 打包前的代码, 只会标出错误的行数, 不会定位到具体的变量 |
| cheap-module-source-map | o | - | yes | original source (lines only) | 可以看到原始代码(自己写的代码), 只会标出错误的行数, 不会定位到具体的变量 |
| inline-cheap-source-map | + | o | no | transformed code (lines only) | 代码也会根据模块进行拆分, 我们可以查看被 loader 翻译后, 被 webpack 打包前的代码, 只会标出错误的行数, 不会定位到具体的变量 |
| inline-cheap-module-source-map | o | - | no | original source (lines only) | 可以看到原始代码(自己写的代码), 只会标出错误的行数, 不会定位到具体的变量 |
| source-map | -- | -- | yes | original source | 可以看到原始代码(自己写的代码) |
| inline-source-map | -- | -- | no | original source | 可以看到原始代码(自己写的代码) |
| hidden-source-map | -- | -- | yes | original source | 可以看到原始代码(自己写的代码) |
| nosources-source-map | -- | -- | yes | without source content | 这种方式不会包含源代码, 浏览器会从服务器请求源码, 所以我们需要设置[output.devtoolModuleFilenameTemplate](https://webpack.js.org/configuration/output/#outputdevtoolmodulefilenametemplate)来匹配到源代码的路径. |

> +++ super fast, ++ fast, + pretty fast, o medium, - pretty slow, -- slow

<a name="1a63ac23"></a>

### 示例

我们在之前写的`index.js`中加入一段 ES6 语法:

```javascript
  class Log{
    constructor() {
      console.lo("error"); //这里让代码报错,
    }
  }
const log = new Log();
```

当然别忘了加入`babel`相关的依赖(这里的配置内容请参考前面的一遍博客. 这里不做说明了), 我们使用 `webpack-dev-server` 来进行调试, `yarn add webpack-dev-server -D`.

现在运行 devServer: `npx webpack-dev-server`, 访问`http://localhost:8080/home.html`.

然后打开 F12 开发者工具, 我们可以发现代码报错了, 但是如果我们这个时候想要点进去查看报错的代码行数, 发现代码只有一行(当`webpack`中的`mode`没有配置或者配置为`'production'`时会出现下面的情况)

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556111711136.png#alt=Alt%20text)

而且点进去之后发现是压缩过的代码, 如果代码很复杂, 这显然没有办法调试了

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556111723230.png#alt=Alt%20text)

当然如果是`mode: 'development'`的话, 点进去之后代码并不是一行, 但是也不是我们想要的源码. 大概是下面这种情况:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556111904053.png#alt=Alt%20text)

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556111896665.png#alt=Alt%20text)

现在我们就可以通过`sourcemap`来映射编译后的代码和源代码, 这样可以方便我们的调试.我们再`webpack.config.js`中来增加一个选项:

```javascript
  module.exports = {
    mode: 'development',
    entry: {
      // 一个叫做home的入口文件, 文件位置在'./src/index.js',
      home: './src/index.js',
      // 另一个叫做another的入口文件, 文件位置在'./src/another.js',
      another: './src/another.js',
    },
    // 1) 源码映射, 会单独生成一个sourcemap文件, 出错了会标识出当前报错的列和行.
    devtool: 'source-map', // 增加映射文件 可以帮助我们调试源代码
    output: ....
    ....
  }
```

其实只添加了一行:`devtool: 'source-map'`, 现在打包看看效果`npx webpack`, 我们会发现, 打包后`dist`目录下, 多了一个叫做`home.js.map`的文件, 这个文件非常大, `home.js`大概`4.02KB`, 而这个`home.js.map`却有`3.8KB`的大小.

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556112247681.png#alt=Alt%20text)

现在我们再打开网页

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556113350580.png#alt=Alt%20text)

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1556113358788.png#alt=Alt%20text)

<a name="watch"></a>

## watch

接下来介绍一个自动打包的指令, 当我们每次修改完配置, 如果不想每次都重新执行`npm run build`命令的话, 就可以使用`watch`属性来自动打包.

```javascript
  module.exports = {
  ...省略其他配置
    watch: true,
    watchOptions: {
      poll: 1000, // 每隔1000ms轮询, 查看是否有被修改的文件需要重新打包
      aggregateTimeout: 1000, // 防抖
      ignored: /node_modules/, // 不需要监控node_modules, 监听这么多文件会非常消耗性能, 没必要
    },
  ...省略其他配置
  }
```

配置完成后我们执行`npx webpack`, 这个时候我们发现打包完成后, 终端的命令并没有结束, 而是挂起了

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1557150132853.png#alt=Alt%20text)

现在我们再去修改之前的代码(随便改点东西, 主要是为了看 `watch` 是否生效, 改了啥不重要), 修改完成后观察终端中

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/24/1557150307325.png#alt=Alt%20text)

我们发现代码自动打包了, 配置生效.
