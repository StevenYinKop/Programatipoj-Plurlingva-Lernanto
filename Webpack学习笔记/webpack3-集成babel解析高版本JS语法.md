---
title: webpack3-集成babel解析高版本JS语法
url: https://www.yuque.com/stevenyin/liv/xynbnh
---

<a name="6bbec982"></a>

# Webpack(三)

`HTML`, `CSS`整完了, 下面轮到 `JS` 了, `JS` 的语法现在在飞速发展和变革, 从 `ES6` 到现在 `ES10`(today: 2019-4-9)的草案, 各种新的语法特性层出不穷, 但是浏览器厂商没有办法在短时间内完成如此多的新特性的更新, 所以[Babel](https://babeljs.io/)应运而生.从官网上偷来的介绍:

> Babel is a toolchain that is mainly used to convert ECMAScript 2015+ code into a backwards compatible version of JavaScript in current and older browsers or environments.

> 翻译: `Babel` 是一个工具链，主要用于将 `EcmaScript 2015+(ES6+)`代码转换为当前或者旧浏览器或者环境中向后兼容的 `JavaScript` 版本。

我们写一个测试的 `js` 代码:

```javascript
  const testFn = () => {
    console.log('this is es6');
  }
  testFn();
```

打包

```sh
  npx webpack
```

查看一下打包后的结果(我的是 `bundlie.js`), 在结果中有这么一句话

```javascript
  eval("const testFn = () => {\n\tconsole.log('this is es6');\n}\ntestFn();\n\n\n//# sourceURL=webpack:///./src/index.js?");
```

可以看到, 这里直接把箭头函数打包进去了, 这并不是我们想要的结果.

下面就在我们的 `Webpack` 配置里面添加 `babel` 的配置项, 让我们可以使用新语法撸项目, 并且可以在打包时转换为 `ES5`.

首先安装一下 `Babel` 的依赖:

```sh
  npm install babel-loader @babel/core @babel/preset-env --save-dev 或者 yarn add babel-loader @babel/core @babel/preset-env -D
```

然后在 `module.rules` 下增加一个对象:

```javascript
  {
    test: /\.js$/,
    use: {
      loader: 'babel-loader', // 这个loader用于把ES6+的新语法转化为ES5
      options: {
        presets: [
          '@babel/preset-env',
        ]
      }
    }
  }
```

添加完成后执行打包命令

```sh
  npx webpack
```

再查看打包后的文件: 可以发现其中的箭头函数被转换为了 `ES5` 中 `function` 的写法了:

```javascript
  eval("var testFn = function testFn() {\n  console.log('this is es6');\n};\n\ntestFn();\n\n//# sourceURL=webpack:///./src/index.js?");
```

我们再在刚刚测试的 `js` 文件中加入几行代码:

```javascript
  class A {
    a = 1;
  }
```

尝试打包, 发现居然报错了.报错的内容是这样的:

```sh
  ERROR in ./src/index.js
  Module build failed (from ./node_modules/babel-loader/lib/index.js):
  SyntaxError: E:\Programs\Web\full-stack-learning\_webpack\src\index.js: Support for the
  syntax 'classProperties' isn't currently enabled (11:5):

    9 | testFn();
    10 | class A {
  > 11 |   a = 1;
      |     ^
    12 | }

  Add @babel/plugin-proposal-class-properties (https://git.io/vb4SL) to the 'plugins' sect
  Babel config to enable transformation.
```

这里需要我们安装一个 `plugin` 叫做[@babel/plugin-proposal-class-properties](https://babeljs.io/docs/en/babel-plugin-proposal-class-properties)

安装一下这个插件

```sh
  yarn add @babel/plugin-proposal-class-properties -D
```

**这个插件并不是添加在 `Webpack` 的 `plugins` 中, 这个属于 `babel` 的插件而不是 `webpack` 的插件**

所以需要在刚刚写好的 `loader` 里面再做如下的配置:

```javascript
{
  test: /\.js$/,
  use: {
    loader: 'babel-loader', // 这个loader用于把ES6+的新语法转化为ES5
    options: {
      presets: ['@babel/preset-env'],
      plugins: [
        ['@babel/plugin-proposal-class-properties', { loose: true }]
      ]
    }
  }
},
```

解释一下这里的参数 `loose`, 在这个插件的官网上对它的解释是这样的:

**loose**: **boolean**, defaults to **false**.

When **`true`**, class properties are compiled to use an assignment expression instead of Object.defineProperty.

For an explanation of the consequences of using either, see [Definition vs. Assignment](http://2ality.com/2012/08/property-definition-assignment.html) (TL;DR in Part 5)

意思的话就是说,

这个属性如果为 `false`, 则会对这个对象里面的属性使用赋值表达式进行初始化,

而如果是 `true`, 则使用 `Object.defineProperty` 这个方法来初始化.

下面是官网提供的例子:

对于这段代码来说:

```javascript
  class Bork {
    static a = 'foo';
    static b;

    x = 'bar';
    y;
  }
```

当**loose: false**时, 上面的代码会被转换成:

```javascript
  var Bork = function Bork() {
    babelHelpers.classCallCheck(this, Bork);
    Object.defineProperty(this, "x", {
      configurable: true,
      enumerable: true,
      writable: true,
      value: 'bar'
    });
    Object.defineProperty(this, "y", {
      configurable: true,
      enumerable: true,
      writable: true,
      value: void 0
    });
  };

  Object.defineProperty(Bork, "a", {
    configurable: true,
    enumerable: true,
    writable: true,
    value: 'foo'
  });
  Object.defineProperty(Bork, "b", {
    configurable: true,
    enumerable: true,
    writable: true,
    value: void 0
  });
```

当**loose: true**时, 上面的代码会被转换成:

```javascript
  var Bork = function Bork() {
    babelHelpers.classCallCheck(this, Bork);
    this.x = 'bar';
    this.y = void 0;
  };

  Bork.a = 'foo';
  Bork.b = void 0;
```

我在刚刚的配置文件中添加了`{loose: true}`, 所以当我运行

```sh
  npx webpack
```

之后, 检查一下打包后的文件,发现里面有这么一句话:

```javascript
  eval("function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError(\"Cannot call a class as a function\"); } }\n\nvar testFn = function testFn() {\n  console.log('this is es6');\n};\n\ntestFn();\n\nvar A = function A() {\n  _classCallCheck(this, A);\n\n  this.a = 1;\n};\n\n//# sourceURL=webpack:///./src/index.js?");
```

其中有一个

```javascript
  var A = function A() {\n  _classCallCheck(this, A);\n\n  this.a = 1;\n};
```

说明我们的代码被转换成了直接赋值的形式.

除了 `class`, 我们还有一个常用的语法就是 `decorator` 装饰器, 比如在写 `react` 的时候会用`@connect` 去关联 `Redux`, 或者使用 `Vue` 的时候用 `vue-property-decorator` 进行 `TypeScript` 风格代码的编写, 当我们使用这些装饰器的时候, 也需要专门的 `babel` 插件去支持它们,先搞一个装饰器, 我们在刚刚的代码上加上一个装饰器, 这个装饰器的作用就是, **打印被修饰的类的信息**:

```javascript
  @connect
  class A {
    a = 1;
  }
  function connect(clz) {
    console.log(clz)
  }
```

打包

```sh
  npx webpack
```

果然报错了, 报错的信息

```sh
ERROR in ./src/index.js
Module build failed (from ./node_modules/babel-loader/lib/index.js):
SyntaxError: E:\Programs\Web\full-stack-learning\_webpack\src\index.js: Support for the
 syntax 'decorators-legacy' isn't currently enabled (10:1):

   8 | }
   9 | testFn();
> 10 | @connect
     | ^
  11 | class A {
  12 |   a = 1;
  13 | }
```

查阅一下 `Babel` 的官网, 上面写了需要使用[@babel/plugin-proposal-decorators](https://babeljs.io/docs/en/babel-plugin-proposal-decorators)这个插件来支持装饰器语法. 安装一下这个插件

```sh
  npm install --save-dev @babel/plugin-proposal-decorators 或者 yarn add @babel/plugin-proposal-decorators -D
```

使用插件的方法和之前一样, 它并不是 `Webpack` 的 `Plugins`, 它是 `Babel` 的 `Plugins`,要配置在 `babel` 的 `loader` 里面

```javascript
{
   test: /\.js$/,
   use: {
     loader: 'babel-loader', // 这个loader用于把ES6+的新语法转化为ES5
     options: {
       presets: ['@babel/preset-env'],
       plugins: [
         ['@babel/plugin-proposal-decorators', { legacy: true }],
         ['@babel/plugin-proposal-class-properties', { loose: true }]
       ]
     }
   }
},
```

注意到它的文档中有这么一段:

    NOTE: Compatibility with @babel/plugin-proposal-class-properties
    If you are including your plugins manually and using @babel/plugin-proposal-class-properties, make sure that @babel/plugin-proposal-decorators comes before @babel/plugin-proposal-class-properties.

    When using the legacy: true mode, @babel/plugin-proposal-class-properties must be used in loose mode to support the @babel/plugin-proposal-decorators.
    /* 如果你想同时使用@babel/plugin-proposal-class-properties(对class的支持)和@babel/plugin-proposal-decorators(对decorator的支持), 必须确保把@babel/plugin-proposal-decorators(对decorator的支持)写在@babel/plugin-proposal-class-properties(对class的支持)之前.
    当你设置legacy的时候@babel/plugin-proposal-class-properties(对class的支持)必须把loose设置为true
    */

下面说一下这个属性:

> **legacy**: **boolean**, defaults **false**.

> Use the legacy (stage 1) decorators syntax and behavior.

使用 `stage 1` 中的旧的装饰器语法.

完成了上述配置之后我们再来打包:

```sh
  npx webpack
```

看一下打包后的文件中, 可以看到有这么一段代码:

```javascript
  eval("var _class, _temp;\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError(\"Cannot call a class as a function\"); } }\n\nvar testFn = function testFn() {\n  console.log('this is es6');\n};\n\ntestFn();\n\nvar A = connect(_class = (_temp = function A() {\n  _classCallCheck(this, A);\n\n  this.a = 1;\n}, _temp)) || _class;\n\nfunction connect(clz) {\n  console.log(clz);\n}\n\n//# sourceURL=webpack:///./src/index.js?");
```

很明显其中的装饰器已经被正确的翻译成了函数的形式
