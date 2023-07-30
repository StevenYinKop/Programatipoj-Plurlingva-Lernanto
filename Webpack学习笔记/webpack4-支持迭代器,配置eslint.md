---
title: webpack4-支持迭代器,配置eslint
url: https://www.yuque.com/stevenyin/liv/yrnkgr
---

<a name="5746ba76"></a>

# Generator 语法和 js 语法检查

<a name="a4a7f8f6"></a>

## 使用 Generator 语法

当我们在代码中使用 `generator` 语法的时候, 如:

```javascript
  function* a() {
    yield 1;
  }
```

这段代码会被编译为

```javascript
  var _marked = [a].map(regeneratorRuntime.mark);
  function a() {
    return regeneratorRuntime.wrap(function a$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            _context.next = 2;
            return 1;

          case 2:
          case "end":
            return _context.stop();
        }
      }
    }, _marked[0], this);
  }
```

虽然代码被转换成了 `ES5` 的语法, 但是这个时候一个很诡异的事情发生了, 我们把这个编译后的 `bundle.js` 文件引用的时候, 浏览器会报错:

```sh
Uncaught ReferenceError: regeneratorRuntime is not defined
    at eval (index.js:5)
    at Object../src/index.js (bundle.js?a2f7efb37dc77f62ae95:96)
    at __webpack_require__ (bundle.js?a2f7efb37dc77f62ae95:20)
    at bundle.js?a2f7efb37dc77f62ae95:84
    at bundle.js?a2f7efb37dc77f62ae95:87
```

因为这个 `regeneratorRuntime` 实际上是 `babel` 的一个内置的 `API`, 并不是浏览器中的 `API`, 而在编译后, 虽然 `generator` 被转换为了 `regeneratorRuntime`, 但是并没有声明这个函数.

我们还需要额外的插件[babel-plugin-transform-runtime](https://babeljs.io/docs/en/babel-plugin-transform-runtime)来增加对 `regeneratorRuntime` 的支持.(对 `generator` 的拓展可以看[这里](https://juejin.im/post/5bd85cfbf265da0a9e535c10)).

首先使用这个插件:

```sh
  npm install --save-dev @babel/plugin-transform-runtime
```

在 `babel` 的文档中, 提到了我们在使用这个插件的时候, 需要再使用另一个插件叫做[@babel/runtime](https://babeljs.io/docs/en/babel-runtime)来在生产环境下注入一些脚本, 所以还需要使用`--save` 来安装这个插件

```sh
  npm install --save @babel/runtime
```

安装好了之后, 下面就比较做的事情就比较熟悉了, 把`@babel/plugin-transform-runtime` 这个插件放入 `babel` 的 `plugins` 中

```javascript
{
   test: /\.js$/,
   use: {
     loader: 'babel-loader', // 这个loader用于把ES6+的新语法转化为ES5
     options: {
       presets: ['@babel/preset-env'],
       plugins: [
         ['@babel/plugin-proposal-decorators', { legacy: true }], // 支持装饰器的插件
         ['@babel/plugin-proposal-class-properties', { loose: true }], // 支持class语法的插件
         ['@babel/plugin-transform-runtime'] // 支持generator的插件
       ]
     }
   }
 },
```

配置完毕之后, 我们再重新打包`npx webpack`, 并且把打包后的 `bundle` 丢到 `HTML` 中, 发现此时浏览器已经不报错了. 但是在执行 `npx webpack` 的时候我们发现, 在打包的过程中报了一些错误.

```sh
ERROR in   Error: C:/被隐藏的路径/node_modules/@babel/runtime/helpers/typeof.js?:33
  module.exports = _typeof;
                 ^
  TypeError: Cannot assign to read only property 'exports' of object '#<Object>'

  - typeof.js?:33 Module.eval
    [.]/[@babel]/runtime/helpers/typeof.js?:33:16

  - typeof.js?:34 eval
    [.]/[@babel]/runtime/helpers/typeof.js?:34:30

  - index.html:98 Module../node_modules/@babel/runtime/helpers/typeof.js
    C:/被隐藏的路径/src/index.html:98:1

  - index.html:21 __webpack_require__
    C:/被隐藏的路径/src/index.html:21:30

  - index.html:132 Module../node_modules/webpack/buildin/global.js
    C:/被隐藏的路径/src/index.html:132:1

  - index.html:21 __webpack_require__
    C:/被隐藏的路径/src/index.html:21:30

  - lodash.js?:17101 eval
    [.]/[lodash]/lodash.js?:17101:41

  - index.html:120 Object../node_modules/lodash/lodash.js
    C:/被隐藏的路径/src/index.html:120:1
```

因为 `webpack` 在打包的时候, 把当前项目中所有的 `js` 文件都进行扫描了, 我们要排除掉 `node_modules` 里面的文件,

需要在配置中添加**exclude**或者**include**属性:

```javascript
  rules: [
    {
      test: /\.js$/,
      use: {...},
      exclude: /node_modules/, // 这条rule只命中node_modules之外的文件.
      include: path.resolve(__dirname, 'src'), // 这条rule只命中项目目录下src目录内的文件.
    },
  ]
```

这两个属性可以搭配使用也可以只用其中某一个, 达到自己的需求即可.

这个时候在进行打包`npx webpack`就不会出现这些报错信息了, 因为 `webpack` 跳过了 `node_modules` 里面的文件. ##使用更高级的语法

如果我们使用更高级的语法比如:

```javascript
  console.log("examples".includes("a"));
```

这是 ES7 的语法.我们打包试一下.

这一段代码在 `bundle.js` 中并没有进行转换,而是原样输出了,

```javascript
  eval("省略省略....console.log(\"examples\".includes(\"a\"));....省略省略");
```

如果我们想要转换这样的语法, 则需要另一个插件: [@babel/polyfill](https://babeljs.io/docs/en/babel-polyfill):

官网上对这个插件的介绍比较详细, 因为这个插件确实比较重要一些

Babel includes a [polyfill](https://en.wikipedia.org/wiki/Polyfill_\(programming\)) that includes a custom [regenerator runtime](https://github.com/facebook/regenerator/blob/master/packages/regenerator-runtime/runtime.js) and [core-js](https://github.com/zloirock/core-js).

This will emulate a full ES2015+ environment (no < Stage 4 proposals) and is intended to be used in an application rather than a library/tool. (this polyfill is automatically loaded when using babel-node).

This means you can use new built-ins like `Promise` or `WeakMap`, static methods like `Array.from` or `Object.assign`, instance methods like `Array.prototype.includes`, and `generator functions` (provided you use the [regenerator](https://babeljs.io/docs/en/babel-plugin-transform-regenerator) plugin). The polyfill adds to the global scope as well as native prototypes like String in order to do this.

首先安装一下

```sh
npm install --save @babel/polyfill
```

> 因为这个插件会在源代码之前运行, 所以我们需要使用`--save`, 而不是`--save-dev`

安装完成之后我们要在代码的最开头引入这个插件

```javascript
  require('@babel/polyfill');
  ....
  console.log("examples".includes("a")); // 使用新的语法
  ....
```

打包`npx webpack`, 我们打开编译之后的 `bundle.js` 发现这个文件变得很大, 仔细阅读打包后的代码发现, `@babel/polyfill` 的功能是在原型链上自己新增了新的语法, 比如这个 `string` 下的 `includes` 实例方法, 在源代码中可以看到这么一段代码

```javascript
eval("// 21.1.3.7
  String.prototype.includes(searchString, position = 0)\n
  \n
    var $export = __webpack_require__(/*! ./_export */ \"./node_modules/core-js/modules/_export.js\");\n
    var context = __webpack_require__(/*! ./_string-context */ \"./node_modules/core-js/modules/_string-context.js\");\n
    var INCLUDES = 'includes';\n
  \n
    $export($export.P + $export.F * __webpack_require__(/*! ./_fails-is-regexp */ \"./node_modules/core-js/modules/_fails-is-regexp.js\")(INCLUDES), 'String', {\n
    includes: function includes(searchString /* , position = 0 */) {\n
      return !!~context(this, searchString, INCLUDES)\n
        .indexOf(searchString, arguments.length > 1 ? arguments[1] : undefined);\n
    }\n
  });\n
  \n
  \n
  //# sourceURL=webpack:///./node_modules/core-js/modules/es6.string.includes.js?");
```

这样的话就可以使用新的语法进行 `coding` 了.

<a name="1cf481e0"></a>

## 代码检查

`JavaScript` 是一个动态的弱类型语言, 有的错误在开发时不一定能够及时发现, 要一遍一遍地调试, 浪费了大量的时间. 或者说一个团队中, 不同的人有不同的编码风格, 这样会导致团队没有一个统一的编码规范, 维护起来, 就是, 相似的功能, 但是各位各显神通, 用各种方法实现.

所以我们可以使用[ESLint](https://eslint.org/)这样的工具来对我们的代码进行规范性检查.

这玩意儿怎么用?

首先安装 `loader` 和 `eslint`:

```sh
  yarn add eslint eslint-loader -D 或者 npm install eslint eslint-loader --save-dev
```

然后添加 `module.rules`:

```javascript
  rules: [{
    test: /.js/, // 匹配所有的js文件
    use: {
      loader: 'eslint-loader', // 对匹配到的js文件执行eslint-loader.
    },
  }, {
    其他的module.rules
  }]
```

`loader` 默认是从右向左执行, 由下到上执行.所以我们应该先去校验 `js`, 然后再去使用 `babel` 进行转换. 所以如果我们的 `loader` 这样写:

```javascript
  rules: [{
        test: /.js/,
        use: {loader: 'eslint-loader'},
      },{
      test: /.js/,
      use: {loader: 'babel-loader'},
    }
  ]
```

上面的代码省略了其他的选项, 只保留了一个 `loader` 的名字, 如果是这样的书写顺序, `babel-loader`会先执行, 而`eslint-loader`会后执行, 所以我们可以把上面的两个 `rules` 调换一下位置, 把`eslint-loader`放在下面, `babel-loader`放在上面, 还有一种方式是在 `loader` 中添加一个 `options.enforce`:

```javascript
  rules: [{
    test: /.js/, // 匹配所有的js文件
    use: {
      loader: 'eslint-loader', // 对匹配到的js文件执行eslint-loader.
      options: {
        enforce: 'pre', // previous
      }
    },
  }, {
    其他的module.rules
  }]
```

这个参数就是强行让`eslint-loader`在最前面执行.

现在`eslint-loader`配置好了, 但是我们需要校验代码, 需要有一个校验的规则, 比如说, 我的字符串是用单引号还是双引号? 每一行代码的结尾需不需要添加分号?

这些配置我们可以在[这里 eslint demo](https://eslint.org/demo/)找到一个在线配置 `configuration` 的页面, 这里可以选择你需要自定义的一些配置项, 选择需要的配置项之后, 页面的最下方有一个`Download .eslintrc.json file with this configuration` , 下载完毕, 得到一个`eslintrc.json`文件, 改个文件名:`.eslintrc.json`, 把这个文件丢到项目的根目录下, 完工.

我在代码中添加这样一句话:

```javascript
  const testEsLint = "Hello ESLint"; // 仅仅是声明了这句话, 没有进行使用
```

我们配置好了之后执行一下打包试试效果`npx webpack`, 这个时候就可以看到类似下面的效果:

```sh
ERROR in ./src/index.js
Module Error (from ../node_modules/_eslint-loader@2.1.0@eslint-loader/index.js):
C:/被隐藏的路径/src\index.js
  15:5   error  'testEsLint' is assigned a value but never used  no-unused-vars
  17:1   error  'require' is not defined                         no-undef
  20:3   error  Unexpected console statement                     no-console
  20:3   error  'console' is not defined                         no-undef
  25:5   error  'A' is assigned a value but never used           no-unused-vars
  33:12  error  Unexpected constant condition                    no-constant-condition
  47:1   error  Unexpected console statement                     no-console
  47:1   error  'console' is not defined                         no-undef
  50:3   error  Unexpected console statement                     no-console
  50:3   error  'console' is not defined                         no-undef
```

我们可以上面的提示对自己的代码进行修改. 当然有的校验确实有点恶心, 让我们写代码的时候很烦躁, 可以根据后面的提示, 比如`no-console`, 在`.eslintrc.json`中把相应规则删除掉.
