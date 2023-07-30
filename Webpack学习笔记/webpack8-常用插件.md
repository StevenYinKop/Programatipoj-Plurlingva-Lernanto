---
title: webpack8-常用插件
url: https://www.yuque.com/stevenyin/liv/vewa39
---

<a name="3111e41a"></a>

# Webpack 中的常用插件

<a name="4d2c099b"></a>

## 这里主要介绍三个常用的插件

1. [cleanWebpackPlugin](https://github.com/johnagan/clean-webpack-plugin)
2. [copyWebpackplugin](https://www.webpackjs.com/plugins/copy-webpack-plugin/)
3. [bannerPlugin](https://www.webpackjs.com/plugins/banner-plugin/)(`webpack` 内置插件)

<a name="1924cdf0"></a>

### [cleanWebpackPlugin](https://github.com/johnagan/clean-webpack-plugin)

这个插件用来在 `build` 前清空 `output.path` 目录下的所有文件, 并且在每一次重新打包后删除掉那些没有引用的 `assets`

先安装一下插件`npm install --save-dev clean-webpack-plugin` 或者 `clean-webpack-plugin yarn add -D`安装完成后在配置文件中添加下面的配置信息:

```javascript
  let CleanWebpackPlugin = require('clean-webpack-plugin')
  module.exports = {
    plugins: [
      new CleanWebpackPlugin(), // 默认情况下这个插件会清除配置中output.path指定的目录.
    ],
  }
```

当然这里也可以传入参数:

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| dry | Simulate the removal of files | `boolean` | `false` |
| verbose | (Always enabled when dry is true) | `boolean` | `false` |
| cleanStaleWebpackAssets | Automatically remove all unused webpack assets on rebuild | `boolean` | `false` |
| protectWebpackAssets | Do not allow removal of current webpack assets | `boolean` | `true` |
| cleanOnceBeforeBuildPatterns | Removes files once prior to Webpack compilation. Not included in rebuilds (watch mode).Use !negative patterns to exclude files | `string[]` | `['**\/*']` |
| cleanAfterEveryBuildPatterns | Removes files after every build (including watch mode) that match this pattern. Used for files that are not created directly by Webpack. Use !negative patterns to exclude files | `string[]` | `disabled` |
| dangerouslyAllowCleanPatternsOutsideProject | Allow clean patterns outside of process.cwd(),requires dry option to be explicitly set | `boolean` | `false` |

<a name="116ebf49"></a>

### [copyWebpackplugin](https://www.webpackjs.com/plugins/copy-webpack-plugin/)

将单个文件或整个目录复制到生成目录.

安装插件:

```sh
    npm install --save-dev copy-webpack-plugin 或者 yarn add copy-webpack-plugin -D
```

使用方法和上面的插件类似, 在 `plugins` 数组中 new 一个新的插件

```javascript
  let CopyWebpackPlugin = require('copy-webpack-plugin')
  module.exports = {
    plugins: [
      new CopyWebpackPlugin([
        {
          from: './document', to: './'
        }
      ]),
    ],
  }
```

`CopyWebpackPlugin` 可以传入两个参数:

第一个参数用来描述拷贝的文件的来源, 目标位置, 文件类型等

第二个参数则是用来配置这个插件的一些属性, 如是否显示 `log`, 是否监听文件变化重新拷贝等.

<a name="d0984852"></a>

### [bannerPlugin](https://www.webpackjs.com/plugins/banner-plugin/)

这个插件就比较简单而且好理解了, 主要用来为打包后的每个文件生成一个 `banner`, 这是 `webpack` 内置的一个插件, 使用方式的话相对于上面两个插件更简单一些, 不需要安装额外的依赖

```javascript
  let webpack = require('webpack')
  module.exports = {
    plugins: [
      new webpack.BannerPlugin(banner) //new webpack.BannerPlugin(options) 或者使用这种, 填写详细的配置信息
    ],
  }
```

`options` 的可选配置有:

```typescript
  {
    banner: string, // 其值为字符串，将作为注释存在
    raw: boolean, // 如果值为 true，将直出，不会被作为注释
    entryOnly: boolean, // 如果值为 true，将只在入口 chunks 文件中添加
    test: string | RegExp | Array, // 匹配相应规则的文件, 对这些文件添加
    include: string | RegExp | Array, // 包含的文件
    exclude: string | RegExp | Array, // 剔除的文件
  }
```
