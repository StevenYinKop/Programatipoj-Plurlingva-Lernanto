---
title: webpack6-打包图片
url: https://www.yuque.com/stevenyin/liv/to5i7f
---

<a name="2f313f9b"></a>

# 图片处理

<a name="88ef35a8"></a>

## webpack 打包图片

<a name="7b51f668"></a>

### 1. 在`js`中创建图片引入

如果我们使用下述的写法, 图片在打包后是不能正常显示的

```javascript
  const img = new Image();
  img.src = './boram.jpg';
  document.body.appendChild(img);
```

原因很简单, 这里的`image.src='./boram.jpg'`;被识别为一个字符串, 打完包后, 首先图片资源没有被处理, 其次在打包后的目录下并不存在名叫`boram.jpg`的图片, 这个时候就会出现如下的问题.

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/17/01.png#alt=Alt%20text)

我们如果想要正确的导入图片, 需要使用 require 语法, 让 webpack 知道这里存在模块的依赖关系(js 依赖于图片).我们来把代码修改为这样:

```javascript
  const img = new Image();
  img.src = require('./boram.jpg');
  document.body.appendChild(img);
```

当然也可以用 ES6 中的 import 语法:

```javascript
  import boram from './boram.jpg';
  // const boram = require('./boram.jpg');
  const img = new Image();
  img.src = boram;
  document.body.appendChild(img);
```

上面的写法都是支持的, 好, 现在再来`npx webpack`打包一下:

此时打包出错了:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/02.png#alt=Alt%20text)

结合之前`CSS`打包的时候报的错误, 这个也很好理解, 因为我们没有使用一个合适的`loader`去加载这个`webpack`不认识的模块(`.jpg`), 这里需要使用到的是[file-loader](https://github.com/webpack-contrib/file-loader):

先安装:

```sh
  npm install file-loader --save-dev 或者 yarn add file-loader
```

和之前使用的 loader 使用方法一样:

```javascript
  module: {
    rules: [{
      test: /\.(png|jpg|gif)$/, // 以png, jpg, gif结尾的文件, 会被file-loader处理
      use: 'file-loader',
    }]
  }
```

再来`npx webpack`试一下:

打开我们的页面:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/03.png#alt=Alt%20text)

图片正确加载了, 而且注意看这个图片名, 并不是我们之前定义的图片的名字, 而是哈希码.当然这个图片名是可以由我们自定义的, 具体方式在可以查阅[官方文档](https://github.com/webpack-contrib/file-loader)

<a name="381d6eca"></a>

### 2. 在`css`中引入`background: url(...);`

在 CSS 中, 我们可以直接使用之前提到过的 css-loader, 这个 loader 会帮助我们把 CSS 中引用的图片进行打包,

```css
  /** image.css */
  .webpack-background-test {
    width: 500px;
    height: 500px;
    background: url(./boram.jpg);
  }
```

```html
  <!-- index.html -->
  <div class="webpack-background-test"></div>
```

```javascript
  // index.js
  import './image.css';
```

打包运行:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/04.png#alt=Alt%20text)

结果可以正确显示, 并且图片也被正确地打包了.

<a name="a1f6c959"></a>

### 3. 在`html`中使用`<img />`

接下来我们尝试在`index.html`中使用`<img />`来引入文件, 如果我们还是直接这么写:

```html
  <!-- index.html -->
  <img src="boram.jpg" alt="boram" />
```

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/05.png#alt=Alt%20text))

这样图片依然是无法显示的, 因为`webpack`依然会把这个`src`当做是一个写死的字符串

我们想要处理这种情况的话, 有需要一个新的`loader`, `html-withimg-loader`

先安装`yarn add html-withimg-loader -D`,

然后再在 `webpack` 配置中添加一个新的 `rules`:

```javascript
  module: {
    rules: [
      {
        test: /\.html$/,
        use: 'html-withimg-loader'
      }]
  }
```

打包`npx webpack`运行:

图片可以正确加载了:

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/06.png#alt=Alt%20text))

<a name="dc5d9f54"></a>

## 使用 url-loader 将小图片转换成 base64

当我们页面有很多小图片的时候, 这个时候我们可能并不想通过开启多次 HTTP 请求去获取这些图片, 因为每一张图片都要请求一次服务器显得有些太过多余, 我们可以使用`url-loader`, 来对图片进行处理, 配置一个图片大小, 如果图片小于这个值, 就直接在代码中转换成 `base64` , 而不去引用:

安装`yarn add url-loader -D`,

配置:

```javascript
  module: {
    rules: [
      {
        test: /\.(png|jpg|gif)$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 30 * 1024, // 限制当图片小于30KB时, 将图片转换为base64而不去打包.
          }
        }
      }
  ]
}
```

这里需要注意的是, 我们设置了阈值之后, 当图片的大小大于 30KB 的时候, `url-loader`会默认使用`file-loader`来打包图片, 也就是说我们还需要安装`file-loader`才能够支撑它正常运行, 这里之前已经安装过了`file-loader`所以没有问题.

我们这里的测试图片有四张, 两张大于 30KB, 两张小于 30KB,

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/07.png#alt=Alt%20text)

我们先用 js 引入的方式来测试一下图片的打包情况:

```javascript
  const img1 = new Image();
  img1.src = require('./boram.jpg');
  document.body.appendChild(img1);

  const img2 = new Image();
  img2.src = require('./boram2.jpg');
  document.body.appendChild(img2);

  const img3 = new Image();
  img3.src = require('./boram3.jpg');
  document.body.appendChild(img3);

  const img4 = new Image();
  img4.src = require('./boram4.jpg');
  document.body.appendChild(img4);
```

执行`npx webpack`

结果可以正常显示并且可以看到中间两张小图片被转换成了 base64 而 1,4 两张图片则是通过网络请求访问:

其他两种方法也可以正常时候`url-loader`来转换,这里就不做演示了, 做法其实没啥太大差别.

<a name="b5c9fc2e"></a>

## 将不同类型的模块打包入不同目录下

我们现在打包出来的目录非常的简单粗暴, 所有的文件都生成在 build 目录下, 这样如果项目的模块多了, 比如有大量图片, CSS, JS 分模块打包的话, 会显得乱的一比.我们可以在打包时配置`outputPath`来对文件进行分类.

首先我们在 url-loader 这里加上一个`outputPath`看看效果:

```javascript
  {
    test: /\.(png|jpg|gif)$/,
    use: {
      loader: 'url-loader',
      options: {
        limit: 30 * 1024,
        outputPath: '/img/',
      }
    }
  },
```

`npx webpack`打包完成后我们可以看到我们的 build 下多了一个 img 目录, 我们的图片被打包到了 img 下,同时引用这些图片的代码前也相应加入了`'/img'`的路径

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/08.png#alt=Alt%20text)

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/09.png#alt=Alt%20text)

<a name="22bb6e28"></a>

## [publicPath](https://webpack.js.org/guides/public-path/)

publicPath 可以在引用资源的时候统一加上一个前缀.

比如说我们的项目为了加速加载, 可能会将打包后的一些文件比如 `CSS`, 图片资源等放在 `CDN` 服务器上, 这个时候我们在引入这些文件的时候就应该是类似于这样(仅举例, 随便找了一个 `CDN` 的地址而已):

`https://code.jquery.com/jquery-3.4.0.min.js`,

也就是说我们打包之后的文件, `jquery-3.4.0.min.js`. 我们在`index.html`中, 打包时应该加上这么一个前缀, 不然这个文件可能就引入失败了.此时我们可以在配置中加入`publicPath`选项:

```javascript
  module.exports = {
  ...其他配置
    output: {
      filename: 'bundle.js',
      path: path.resolve(__dirname, 'build'),
      publicPath: 'https://code.jquery.com',
    },
  ...其他配置
  }
```

然后我们打包之后得到结果, 引用的资源前面都会加上这么一个 `url` 前缀.

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/10.png#alt=Alt%20text)

当然啦, 打完包之后要把代码丢到这个路径下, 否则这个配置就没有卵用了, 因为你找不到这个资源了.

可是如果使用这种方式的话有一个问题, 它会把所有的静态资源引用前面全部加上这个前缀, 也许我们只希望把图片资源加上前缀呢?

我们可以把上面写的`publicPath`属性单独地添加在`url-loader`的`options`中, 而不是直接添加在全局的`output`中.

```javascript
  {
    test: /\.(png|jpg|gif)$/,
    use: {
      loader: 'url-loader',
      options: {
        limit: 30 * 1024, // 限制当图片小于30KB时, 将图片转换为base64而不去打包.
        outputPath: '/img/',
        publicPath: 'http://localhost:8080/static',
      }
    }
  },
```

![](%7B%7B@@IMAGE_URL@@%7D%7D/blog_img/2019/04/18/11.png#alt=Alt%20text)

这是一个很有用的属性, 并不是专门用来添加 `CDN` 的前缀的, 也可以添加相对路径, 如添加`/statics/`.
