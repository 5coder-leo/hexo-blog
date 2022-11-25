---
title: Webpack 4
author: 5coder
tags: Webpack4
category: 大前端
abbrlink: 38302
date: 2022-11-25 23:24:47
password:
keywords:
top:
cover:
---

[【附件】Webpack4-demo.rar](/media/attachment/2022/11/Webpack4-demo.rar)

## Webpack4

### 1. 模块打包工具的由来及概要

模块化确实很好的解决了在复杂应用开发过程当中的代码组织问题，但是随着引入模块化，Web应用又会产生一些新的问题：

> - 第一个，ESM模块系统，**它本身就存在环境兼容问题**，尽管现如今主流浏览器的最新版本都已经支持这样一个特性，但是目前还没有办法做到统一所有用户浏览器的使用情况，所以还需要去解决兼容问题；
>
> - 第二个，通过模块化的方式划分出来的模块文件会比较多，而前端应用又是运行在浏览器当中的，因此每一个在应用当中所需要的文件，都需要从服务器当中请求回来，这些零散的模块文件必将会导致**浏览器频繁发出请求**，从而影响应用的工作效率；
>
> - 第三个，在前端应用开发过程当中，不仅仅只有JavaScript的代码需要模块化，随着应用的日益复杂，**HTML、CSS等资源文件**同样也会面临相同的问题。而且从宏观角度来看的话，这些文件也都可以看作为前端应用当中的一个模块，只不过这些模块的种类和用途跟JavaScript是不同的。

对于整个过程而言模块化肯定是有必要的，不过需要在原有的基础之上去引入更好的方案或者工具去解决上面这样几个问题或者是需求，让开发者在应用的开发阶段，可以继续享受模块化带来的优势，又不必担心模块化对生产环境所产生的一些影响。我们就先对这个所谓的更好的方案或者工具去提出一些设想，我们希望它们能够满足我们的这些设想：

> - 第一点，需要这样一个工具能够编译代码，**开发阶段编写的包含新特性的代码，直接去转换为能够兼容绝大多数环境的代码。**这样一来面临的环境问题也就不存在了；
>
>   ![image-20201218223016824](https://img-blog.csdnimg.cn/img_convert/fcea89fb03339b26f8bc1030070789a4.png)
>
> - 第二点，**能够将散落的模块文件再次打包到一起，解决了浏览器当中频繁对模块文件发出请求的问题。**至于模块化文件划分，只是在开发阶段需要它，因为它能够更好的代码，但是对于运行环境实际上是没有必要的。所以说可以选择在开发阶段通过模块化的方式去编写，生产阶段还是把它们打包到同一个文件当中。
>
>   ![image-20201218223045071](https://img-blog.csdnimg.cn/img_convert/607c74852bd73829ee740314c3cb23ab.png)
>
> - 第三点，需要去支持不同种类的前端资源类型，可以把前端开发过程当中所涉及到的样式，图片，字体等等所有资源文件都当作模块去使用。对于整个前端应用来讲，就有了一个**统一的模块化方案**。之前介绍的那些模块化方案，实际上只是针对现有JavaScript的模块化方案。现在强调，对于整个前端应用来讲，它的一个模块化的方案。这些资源，有了模块化方案后就可以通过代码去控制，那它就可以与业务代码统一去维护。这样对于整个来讲的话会更加合理一些。
>
>   ![image-20201218223107825](https://img-blog.csdnimg.cn/img_convert/cfbef08b888d5b8e76b5b2f65bdfa1f2.png)

针对前两个需求，完全可以借助于之前所了解过的一些构建系统，去配合一些编译工具就可以实现。但是，对于最后一个需求，很难通过这种方式去解决了，所以说就有了接下来所介绍的一个主题，也就是**前端模块打包工具**。

------

前端领域目前有一些工具，就很好的解决了以上这几个问题，其中最为主流的就是Webpack、Parcel、Rollup。以Webpack为例，它的一些核心特性，就很好的满足了上面的那些需求。

![image-20201218224701906](https://img-blog.csdnimg.cn/img_convert/89fdb90c55581bf2fcd1205bffde353d.png)

- 首先Webpack作为一个模块打包工具（Module Bundler），**它本身就可以解决模块化JavaScript代码打包的问题**。通过Webpack就可以将零散的模块代码打包到同一个JS文件当中。**对于代码中那些有环境兼容问题的代码，可以在打包的过程当中，通过模块加载器（Loader）对其进行编译转换。**

- 其次，**Webpack还具备代码拆分（Code splitting）的能力，能够将应用当中所有的代码，都按照需要去打包。**这样就不会产生把所有的代码全部打包到一起，产生的这个文件会比较大的这样一个问题。可以把应用加载过程当中初次运行的时候所必须的那些模块打包到一起，那对于其它的那些模块再单独存放。等到应用工作过程当中实际需要的某个模块，再去加载这个模块，从而实现**增量加载或者叫渐进式加载**，这样就不用担心**文件太碎**或者是**文件太大**这两个极端的问题。

- 最后对于前端模块类型的问题，**Webpack支持在JavaScript当中以模块化的方式去载入任意类型的资源文件。**例如在Webpack中就可以通过JavaScript去直接import一个css的文件，最终会通过style标签的形式去工作。其它类型的文件，也可以有类似的这种方式去实现。

总之来说，所有的打包工具它们都是以模块化为目标，**这里所说的模块化是对整个前端项目的模块化**，也就是比之前所说的JavaScript模块化要更为宏观一些。它可以让我们在开发阶段更好的去享受模块化所带来的优势，同时，又不必担心模块化对生产环境所产生的一些影响，那这就是模块化工具的一个作用。

### 2. Webpack快速上手、配置文件

- ##### Webpack快速上手

  Webpack作为目前最主流的前端模块打包器，提供了一整套的前端项目模块化方案，而不仅仅是局限于只对JavaScript的模块化。通过提供的前端模块化方案，我们就可以很轻松的对前端项目开发过程当中，涉及到的所有的资源进行模块化。因为Webpack的想法比较先进，而且它的文档也比较晦涩难懂，所以说在最开始的时候，它显得对开发者不是十分友好。但是随着它版本的迭代，官方的文档也在不断的更新。目前Webpack已经非常受欢迎了，基本上可以说是覆盖了绝大多数现代化的外部应用项目开发过程。

  ![image-20201218233427397](https://img-blog.csdnimg.cn/img_convert/16681ba911e1a4c0376f395109ce93a8.png)

  使用***yarn init***初始化项目目录，安装webpack以及webpack-cli，使用yarn webpack，webpack会自动从src中的index.js开始打包（寻找import）

  ```shell
  yarn init --yes
  yarn add webpack webpack-cli --dev
  yarn webpack
  ```

  运行yarn webpack后，webpack自动将index.js、heading.js打包在dist目录下的main.js中，将index.html中的资源引用变为dist/main.js，并将script中的type="module"取消。再次使用serve .命令运行，发现项目依然可以运行。

  ![image-20201218233230191](https://img-blog.csdnimg.cn/img_convert/3021b99cfd342d1a61ff6c445cb81d42.png)

  如果每次都需要yarn去运行webpack命令，会比较麻烦。可以在**package.json中添加scripts字段，并将其设置为“build”:"webpack"**,这样就可以直接运行

  ***yarn build***命令。

  ![image-20201218233642594](https://img-blog.csdnimg.cn/img_convert/8141ddb30e625b2154cc277bcbccc949.png)

- ##### Webpack配置文件

  Webpack4.0以后支持零配置文件打包。也就是说不需要配置文件，直接按照约定的内容区打包，它的约定是默认入口文件为src下的index.js，默认输出为dist下的main.js。我们如果需要按照自定约定去打包，Webpack也支持配置文件打包。

  在项目根目录下添加webpack.config.js文件，该文件在node环境下运行，其内容如下：

  ```js
  const path = require('path')
  
  module.exports = {
      entry: './src/main.js',  // 打包文件的默认入口，不能省略./
      output: {
          filename: 'bundle.js',  // 输出打包文件的文件名称
          path: path.join(__dirname, 'output')  // 必须为绝对路径，所以需要path模块配合
      }
  }
  ```

![image-20201220190419559](https://img-blog.csdnimg.cn/img_convert/963a979c3fea03634165fa7684c08fe5.png)

### 3. Webpack工作模式、打包结果运行原理

Webpack新增了一个工作模式的用法，这种用法大大简化了Webpack配置的复杂程度，可以把它理解成针对于不同环境的基础预设的配置。我们使用yarn webpack打包项目，命令行会出现一个配置警告，大致意思是我们没有设置一个mode的属性，可能会使用默认的production模式去工作，在这个模式下，webpack内部会自动启动一些优化插件，比如自动压缩代码。这对实际生产环境非常友好，但是对于开发环境中，我们无法阅读这些打包结果。

Webpack工作模式：

- production（默认）
- development（开发模式）
- none

可以通过cli参数去指定打包的模式，具体用法就是给webpack传递一个参数：--mode，参数有三种取值，默认就是production，production模式它会自动启动优化，去优化打包结果。第二种参数是development，开发模式会自动优化打包的速度，它会添加一些开发过程中需要的辅助到代码中（后面介绍调试的会详细介绍）。第三种参数是none模式，none模式下，webpack运行最原始状态的打包，不会做任何额外的处理。

```shell
yarn webpack --mode production  # production为默认的工作模式，可以不用去显式指定
yarn webpack --mode development
yarn webpack --mode none
```

目前工作模式只有这三种，具体的三种模式的差异可以从官网（https://webpack.js.org/configuration/mode）中找到。当然除了cli参数指定模式，还可以通过配置文件方式指定工作模式。

在webpack.config.js中添加node字段，并指定模式。这样就可以通过yarn webpack直接以配置的方式去打包。

webpack.config.js

```js
const path = require('path')

module.exports = {
  // 这个属性有三种取值，分别是 production、development 和 none。
  // 1. 生产模式下，Webpack 会自动优化打包结果；
  // 2. 开发模式下，Webpack 会自动优化打包速度，添加一些调试过程中的辅助；
  // 3. None 模式下，Webpack 就是运行最原始的打包，不做任何额外处理；
  mode: 'development',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist')
  }
}
```

------

我们解读一下webpack打包过后的结果，为了可以更好的理解打包过后的代码，这里先将webpack的工作模式是为none，这样是以最原始的状态去打包代码。

ps:此处使用的版本：

```
"webpack": "4.40.2",
"webpack-cli": "3.3.9"
```

webpack.config.js

```js
const path = require('path')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist')
  }
}
```

```shell
yarn webpack
```

生成的bundle.js文件

```js
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _heading_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1);


const heading = Object(_heading_js__WEBPACK_IMPORTED_MODULE_0__["default"])()

document.body.append(heading)


/***/ }),
/* 1 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (() => {
  const element = document.createElement('h2')

  element.textContent = 'Hello world'
  element.addEventListener('click', () => {
    alert('Hello webpack')
  })

  return element
});


/***/ })
/******/ ]);
```

整个函数是一个立即执行函数，参数为modules。函数调用时传入一个数组，数组中的每个元素是参数列表相同的函数。这里的函数对应的就是源代码中的模块，也就是说每一个模块最终都会被包裹到这样一个函数当中，从而去实现模块的私有作用域。

进入webpack工作入口函数，这个函数内部并不复杂，而且注释也非常清晰。最开始先定义了一个对象，用于存放或者叫缓存加载过的模块。紧接着，定义了一个__webpack_require函数，该函数专门用来加载模块。再往后就是在require函数上面挂载了一些其它的数据和一些工具函数。入口函数执行到最后，调用了require函数，参数传入0，来加载模块。这个地方的模块ID，实际上就是上面的模块数当中的元素下标，也就是说这里才开始去加载在源代码当中所谓的入口模块。

### 4. Webpack资源模块加载

正如一开始提到，webpack并不只是JavaScript的模块化打包工具。它应该是整个前端项目或前端工程的模块打包工具，也就是说可以通过webpack引入任意类型的静态资源文件。接下来通过webpack引入css文件。

首先在项目目录中添加一个**main.css**文件，内容如下：

```css
body {
  margin: 0 auto;
  padding: 0 20px;
  max-width: 800px;
  background: #186fb1;
}
```

然后回到**webpack.config.js**下，将入口文件的路径指向新创建的css文件。随后配置loader组件，test值为正则表达式/.css$/，use配置一个数组，分别为style-loader以及style-loader

```js
const path = require('path')

module.exports = {
  mode: 'none',
  entry: './src/main.css',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist')
  },
  module: {
    // rules数组针对于其它资源模块的加载规则，每个规则对象的都需要设置两个属性。
    rules: [
      {
        test: /.css$/,  // test用来去匹配在打包过程当中所遇到的文件路径
        // use用来去指定我们匹配到的文件，需要去使用的loader
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  }
}
```

命令行启动，yarn webpack，通过serve . 运行，在浏览器中访问就可以看到我们的css生效了。

**ps**:use中，如果配置了多个loader，其执行顺序是从数组最后一个元素往前执行。所以这里一定要把css-loader放到最后，因为我们必须要先通过css-loader把css代码转换为模块才可以正常打包。

style-loader工作代码在bundle.js中，部分代码如下：

![image-20201220213553744](https://img-blog.csdnimg.cn/img_convert/f78c11744afcfdb8ab25fd48aa08da6f.png)

> **loader是webpack实现整个前端模块化的核心，通过不同的loader就可以实现加载任何类型的资源。**

### 5. Webpack导入资源模块

通过上面的探索，webpack确实可以把css文件作为打包的入口文件。不过webpack的打包入口文件一般是JavaScript。因为打包入口文件从某种程度来说，算是应用的运行入口。前端应用当中的业务是由JavaScript去驱动的。上面只是尝试一下，正确的做法还是将JavaScript文件作为打包的入口文件。

webpack.config.js

```js
const path = require('path')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  }
}
```

![image-20201220220116596](https://img-blog.csdnimg.cn/img_convert/edda4f0a15355ba7ac2043e1d04848c2.png)

分别新建main.css以及heading.css文件，代码如图所示。分别在heading.js和main.js中通过import引入css文件。因为heading.css使用了类选择器，所以需要在黄色框中为element添加类名。

构建完成后，命令行运行yarn webpack，随后运行serve .命令，在浏览器打开，发现css文件生效。

> 传统的做法当中是将样式和行为分离开，单独去维护，单独去引入。而webpack中建议我们在JavaScript中引入css。原因是webpack不仅仅建议我们在JavaScript中引入css，而是建议我们编写代码过程中，去引入任何当前模块所需要的资源文件。**因为真正需要资源的不是应用，而是此刻正在编写的代码，它想要工作，就必须加载对应的资源。**
>
> 通过JavaScript代码去引入资源文件，或者叫建立我们JavaScript和资源文件之间的依赖关系。它有一个很明显的优势，JavaScript代码本身是负责完成整个应用的业务功能，那放大来看，它就是驱动了我们整个前端应用，而在实现业务功能的过程当中，可能需要用到样式、图片等等一系列的资源文件，如果建立了这种依赖关系，**一来逻辑上比较合理，因为我们的JavaScript确实需要这些资源文件的配合，才能去实现对应的功能，二来保证上线时资源文件不会缺失，而且每一个上线的文件都是必要的**。

### 6. Webpack文件资源加载器 

目前webpack社区提供了非常多的资源加载器，基本上能想到的所有合理的需求都会有对应的loader，接下来尝试一个非常有代表性的资源加载器。

大多数的加载器都类似于css-loader，都是将资源模块转换为js代码的实现方式去工作。但是，还有一些经常用到的资源文件，例如项目当中的图片或者字体，这些文件是没有办法通过js的方式去表示的，对于这一类的资源文件，需要用到文件资源加载器，也就是file-loader。

项目src目录中添加一张图片icon.png，在main.js中通过import的方式导入图片，并且创建图片标签，将其src设置为导入的接收值。

初始目录：

![image-20201220223044764](https://img-blog.csdnimg.cn/img_convert/e230ab5e25186ae765abad9526605e90.png)

main.js

```js
import createHeading from './heading.js'
import './main.css'
import icon from './icon.png'

const heading = createHeading()

document.body.append(heading)

const img = new Image()
img.src = icon

document.body.append(img)
```

随后在webpack.config.js中设置一个新的规则，当遇到.png结尾的文件时，使用file-loader加载器。

```js
const path = require('path')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
    publicPath: 'dist/'  // 网站的根目录
  },
  module: {
    rules: [
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: 'file-loader'
      }
    ]
  }
}

```

安装file-loader，命令行使用yarn webpack打包资源。serve .运行，通过浏览器可以观察到，img资源被加载成功。

打包后的目录：

![FtikhS9xqPB5I8a](http://5coder.cn/img/1667310668_3d19845d61a642be8d151c4ab4808bb9.png)

![image-20201220222145967](https://img-blog.csdnimg.cn/img_convert/58f2deba5b4e187aed89a4da0e881d99.png)

**总结文件加载器的工作过程，webpack打包过程中遇到图片文件，根据webpack.config.js中的配置规则对应到file-loader加载器。file-loader首先将导入的（图片）文件复制到输出目录dist，然后将文件拷贝到输出目录的路径作为这个模块的返回值，对于这个应用来说，这个资源就被发布了。同时，也可以通过模块的导出成员拿到这个资源的访问路径。**

### 7. Webpack URL 加载器 

除了file-loader这种通过拷贝物理文件的形式去处理文件资源以外，还有一种通过data-url去表示文件，这种方式也非常常见。Data URL是一种非常特殊的协议，它可以直接用来表示一个文件。传统URL一般要求服务器上有一个对应的文件，然后通过请求这个地址，得到服务器上对应的文件。

![image-20201221220611864](https://img-blog.csdnimg.cn/img_convert/ad3ae06a2b71b554b5898550f36e5c80.png)

Data URL是一种当前URL就可以直接去表示这种文件内容的方式，也就是说这种Data URL中的文本就已经包含了文件的内容。在使用这种URl时，我们就不会再发送任何的HTTP请求。例如下面的URL：

```js
data:text/html;charset=UTF-8,<h1>html content!</h1>
```

浏览器就能根据url解析出来这是一个HTML类型的文件内容，它的编码是UTF-8，内容是h1标签。复制该url到浏览器地址栏，可以看到浏览器将它正常渲染出来了。

![](http://5coder.cn/img/1667310699_0c230db44f57a06765338d08562ed61f.png)

但是如果是图片或者字体这一类的，这些无法通过文本表示的二进制文件。我们可以将这些文件内容编译为base64编码，以base64编码也就是字符串表示文件的内容。

webpack中有一种加载器专门处理这种文件：url-loader，安装该加载器并在webpack.config.js中配置如下：

```js
const path = require('path')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
    publicPath: 'dist/'
  },
  module: {
    rules: [
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: 'url-loader'
      }
    ]
  }
}

```

在遇到png文件时，通过url-loader编译后打包。运行yarn webpack，查看bundle.js文件，发现它将该图片转为base64编码，并导出。

![image-20201221224134389](https://img-blog.csdnimg.cn/img_convert/e058dcfe03d0d63b6cf4e8054e4d9f8b.png)

通过serve .启动服务器，发现该图片被正常显示在页面上。通过F12开发者工具打开发现该图片的src为上面base64的编码字符串。并且复制该url到地址栏，浏览器也可以正常渲染出该图片。

![image-20201221224338690](https://img-blog.csdnimg.cn/img_convert/5a7c8498e1d1ad955703a12e0a4f687d.png)

![image-20201221224421859](https://img-blog.csdnimg.cn/img_convert/7a8b21a3466a3282d4a5ca8f0d7dc7c7.png)

这种方式其实非常适合项目当中体积比较小的资源，因为体积过大的话，就会造成打包结果非常大，从而影响运行速度。最佳的实践方式，应该是对于项目当中的小文件，通过url-loader的去转换为URL代码，从而减少应用发送信息。对于较大的文件，应该传统的方式，单个文件方式去存放，从而提高我们应用的加载速度，它支持通过配置选项的方式来去实现刚刚所说的这种最佳实践方式。回到配置文件当中，具体做法就是将url-loader的这样一个字符串，这种简化的配置方式修改为一个对象，那对象当中的loader的属性，还是这个字符串url-loader，为它添加一些其它配置选项。option选项中可以配置其它参数。具体参数如下：

```js
{
    test: /.png$/,
    loader: 'url-loader',
    options: {
    	limit: 10 * 1024 // 10 KB
    	}
    }
}
```

- 小文件使用Data URL，减少请求次数
- 大文件单独提取存放，提高加载速度

### 8. Webpack 常用加载器分类

webpack中的资源加载器有点像是生活中工厂里的生产车间，‌‌它是用来去处理和加工打包过程当中所遇到的资源文件，‌‌设计当中还有很多其它的加载器，‌。

目前个人分为三类：

- 编译转换类型加载器

  它会把加载到的资源模块转换为JavaScript的代码，‌‌例如之前所用的css-loader，‌它就是将css代码转换为bundle当中的一个JavaScript的模块，‌‌从而去实现通过JavaScript去运行css

  ![image-20201221225405476](https://img-blog.csdnimg.cn/img_convert/bac5385dcfdeb7aab5a262a037273789.png)

- 文件操作类型加载器

  文件操作类型加载器都会把加载到的资源模块‌‌拷贝输出的目录，同时将文件的访问路径向外导出。例如之前用到的file-loader，它就是一个非常典型的文件操作类型加载器
  ![image-20201221225431523](https://img-blog.csdnimg.cn/img_convert/097e851dc0d57666c5661ba5a1e6e019.png)

- 代码检查类

  针对于代码质量检查的加载器，‌‌就是对所加的资源文件，一般是代码，‌‌去进行校验的一种加载器。‌‌这种加载器，它的目的是为了统一代码的风格，从而去提高代码质量，‌‌这种类型加载器一般不会去修改生产环境的代码。
  ![image-20201221225458458](https://img-blog.csdnimg.cn/img_convert/c2ff8b28d29161559bef903d7c2d1f3d.png)

### 9. Webpack 与ES2015

由于webpack默认就能处理代码当中的import和export，‌‌所以很自然都会有人认为webpack会自动编译的ES6代码。实则不然，‌‌那是webpack的仅仅是对模块去完成打包工作，‌‌所以说它才会对代码当中的import和export做一些相应的转换，‌‌它并不能去转换我们代码当中其它的es6特性。

如果需要将ES6的代码打包并编译为ES5的代码，需要一些其它的编译形加载器。这里安装一些额外的插件。

```shell
yarn add babel-loader @babel/core @babel/preset-env --dev
```

安装完成后，编写webpack.config.js配置文件，针对js代码指定babel-loader

```js
const path = require('path')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
    publicPath: 'dist/'
  },
  module: {
    rules: [
      {
        test: /.js$/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10 * 1024 // 10 KB
          }
        }
      }
    ]
  }
}

```

再次重新打包，代码中的ES2015中的新特性都被转换。

![image-20201221233429158](https://img-blog.csdnimg.cn/img_convert/7301aac913e0c3ae9e81967255cb1108.png)

总结：

- webpack只是打包工具，它不会处理一些ES6或者更高版本的新特性
- 如果需要处理新特性，可以通过为js代码单独配置加载器来实现

### 10. Webpack 加载资源的方式

除了代码中的import能够触发模块的加载，webpack还提供几种方式，具体如下：

- 遵循ESM标准的import声明

- 遵循commonJS标准的require函数

  如果通过commonJS标准的require函数载入一个ESM的话，需要require一个函数的default属性去获取

  ```js
  const heading = require('./heading.js').default
  ```

- 遵循AMD标准的define函数和require函数

webpack遵循多种模块化标准，不过除非必要，建议不要在一个项目中混用多种标准，这样会造成项目可维护性差。每个项目使用一种标准就行。

除了JavaScript代码中的这三种方式之外，还有一些独立的加载器，它在工作时也会去处理所加载到的资源当中的一些导入的模块，例如：

- css-loader加载的css文件，import指令以及部分属性当中的URL函数，也会去触发相应的资源模块加载

  样式代码中的@import指令和url函数

- html-loader加载html文件中的一些src属性也会触发

![image-20201222221225832](https://img-blog.csdnimg.cn/img_convert/4ee7e390f009c1bf2d23f12a72b58e71.png)

webpack.config.js

```js
const path = require('path')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
    publicPath: 'dist/'
  },
  module: {
    rules: [
      {
        test: /.js$/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10 * 1024 // 10 KB
          }
        }
      },
      {
        test: /.html$/,
        use: {
          loader: 'html-loader',
          options: {
            attrs: ['img:src', 'a:href']  // HTML中针对不同的属性采用不同的加载器
          }
        }
      }
    ]
  }
}

```

main.js入口文件

```js
import './main.css'

import footerHtml from './footer.html'

document.write(footerHtml)
```

总结webpack资源加载方式：

- 遵循ESM标准的import声明
- 遵循CommonJS标准的require函数
- 遵循AMD标准的define函数和require函数
- 样式代码中的@import指令和url函数
- HTML代码中的img标签的src属性以及a标签的href属性

### 11. Webpack 核心工作原理

其实webpack官网首屏的内容就已经很清楚的描述了它的工作原理。

![image-20201222223225625](https://img-blog.csdnimg.cn/img_convert/176dea8025479a1b72c7f8d8dc78f7f3.png)

这里以一个普通的前端项目为例，在项目中一般会散落着各种各样的代码及资源文件，webpack会根据webpack.config.js配置，找到其中一个文件作为打包入口，一般情况下入口文件是一个JavaScript文件。

![image-20201222224238793](https://img-blog.csdnimg.cn/img_convert/5879df32fd2922c5dcce3a0cddadb3e4.png)

**然后**，它会顺着入口文件中的代码，根据代码中出现的import或者require之类的语句，解析推断出来这个文件所依赖的资源，其次就形成了整个项目中所有用到文件之间的一个依赖关系的一个依赖树，有了这个依赖树之后，webpack会遍历或者叫递归这个依赖树，然后找到每个节点所对应的资源文件。

其次根据配置文件中rules属性去找到这个模块所对应的加载器，然后交给对应的loader加载器去加载这个模块。最后会将加载到的结果放到bundle.js也就是打包结果中，从而实现整个项目的打包。

![image-20201222224339634](https://img-blog.csdnimg.cn/img_convert/065b31ca7a88ec0e3edcb86987d23cb9.png)

整个过程中loader的机制气到了一个很重要的作用，因为如果没有loader的话，webpack就没办法实现各种资源文件的加载，那对于webpack来说，它也只能算是一个用来打包或者合并js模块代码的一个工具了。

### 12. webpack 开发一个Loader

loader作为webpack的核心机制，内部的工作原理非常简单，接下来一起开一发一个自己的loader。需求是一个markdown文件的加载器，希望有了一个加载器之后，可以直接在代码中直接导入这个markdown文件。

![image-20201222231837438](https://img-blog.csdnimg.cn/img_convert/fc02f685bb8e2eaa2a73a5ba110581d7.png)

webpack内部的一个工作原理其实非常简单，就是一个从输入到输出之间的一个转换，‌除此之外，还了解了loader，它实际上是一种管道的概念，可以将此次的这个loader的结果交给下一个loader去处理，‌‌然后通过多个loader去完成一个功能。‌例如之前所使用的css-loader和style-loader的之间的一个配合，包括后面还会使用到的sass或者less这种loader，它们也需要去‌‌配合刚刚所说的这两种loader，‌这个就是工作管道一个特性‌。

### 13. Webpack 插件机制介绍

插件机制是webpack当中另外一个核心特性‌‌，它目的是为了增强webpack项目自动化方面的能力‌‌，loader就是负责实现各种各样的资源模块的加载‌‌，从而实现整体项目打包‌‌，plugin则是用来去解决项目中除了资源以外，其它的一些自动化工作‌，例如：

- plugin可以帮我们去实现自动在打包之前去清除dist目录‌‌，也就是上一次打包的结果‌‌；
- 又或是它可以用来去帮我们拷贝那些不需要参与打包的资源文件到输出目录‌‌；
- 又或是它可以用来去帮我们压缩我们打包结果输出的代码‌‌。

总之‌‌，有了plugin的webpack，几乎无所不能的实现了前端工程化当中绝大多数经常用到的部分‌‌，这也正是很多初学者会有webpack就是前端工程化的这种理解的原因‌‌。

### 14. Webpack 自动清除输出目录插件

了解了插件的基本作用过后，接下来先来体验几个最常见的插件，‌‌通过这个过程去了解如何使用插件。

‌‌第一个就是用来**自动清除输出目录的插件(‌‌clean-webpack-plugin)**，通过之前的演示你可能已经发现，‌‌webpack每次打包的结果都是覆盖到dist目录，‌‌而在打包之前，dist中就可能已经存在一些之前的遗留文件，‌再次打包，它只能覆盖掉那些同名的文件，‌‌对于其它那些已经移除的资源文件就会一直积累在里面，非常不合理。那更为合理的做法就是在每次打包之前，‌‌自动去清理dist目录，‌‌这样就只会存在那些需要的文件，clean-webpack-plugin‌‌就很好的实现了这样一个需求。

‌‌那它是一个第三方的插件，先来通过yarn去安装，‌‌安装过后能回到webpack.config.js的配置文件当中，然后去导入这个‌‌那这个插件模块。‌‌然后，使用插件我们需要去为配置对象添加一个plugins属性，‌‌这个属性就是专门用来去配置插件的地方，‌‌它是一个数组，‌‌添加一个插件就是在这个数组当中去添加一个元素。

绝大多数插件模块导出的都是一个类型，‌这里的clean-webpack-plugin也不例外，‌‌所以使用它就是通过这个类型去创建一个实例，然后将这个实例放到这个数组当中。完成之后再次尝试yarn webpack进行打包，‌‌此时，之前的那些打包结果就不会存在了，‌‌dist目录中都是本次打包的结果，‌‌非常干净。

```js
const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
    publicPath: 'dist/'
  },
  module: {
    rules: [
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10 * 1024 // 10 KB
          }
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),  // 通过这个类型去创建一个实例
  ]
}

```

### 15. Webpack 自动生成HTML插件

- 生成基本HTML文件

  除了清理dist的目录以外，‌‌还有一个非常常见的需求就是自动去生成使用打包结果的HTML，在这之前HTML‌‌都是通过硬编码的方式单独去存放在项目根目录下的。‌‌

  但这种方式有两个问题，‌‌第一就是在项目发布时，需要同时去发布的HTML文件和所有的打包结果，这样的话会比较麻烦。‌‌而且上线过后，还需要去确保HTML的代码路径引用都是正确的。‌‌第二个问题是，如果说输出的目录或者是输出的文件名，也就是‌‌打包结果的配置发生了变化，‌‌HTML代码中script标签所引用的路径就需要手动的去修改。‌‌

  这是硬编码的方式存在的两个问题，‌‌要解决这两个问题，最好的办法就是通过webpack‌‌自动去生成HTML文件，‌‌也就是让HTML也去参与到webpack构建过程‌‌中，‌‌构建过程中，webpack知道它生成了多少个bundle，‌‌它会自动将这些打包的bundle添加到的页面当中。‌这样的话，‌‌一来HTML它也输出到了dist目录，上线的时候就只需要把dist目录发布出去就可以了，‌‌二来，HTML当中对于bundle的引用，它是动态的注入进来的，它不需要手动的去硬编码。‌‌所以说它可以确保路径的引用是正常的。

  ‌‌具体的实现方式，需要去借助一个叫html-webpack-plugin的一个插件去实现。这个插件同样也是一个第三方的模块，同样需要去单独安装这个模块。

  ```shell
  yarn add html-webpack-plugin --dev
  ```

  ‌‌之后回到配置文件当中，载入这个模块。‌‌但这里不同于clean-webpack-plugin，‌‌html-webpack-plugin默认导出的就是一个插件的类型，我们不需要去解构它内部的成员。‌‌有了这个类型过后，回到配置对象的plugins属性当中，去添加一个这个类型的实例对象。‌‌这样就完成了这个插件的一个配置。

  ‌‌那最后我们回到命令行终端，‌‌再次运行打包命令，‌‌index.html出现在了dist目录当中，对于bundle的引用的路径也是正常了。这样就不再去需要根目录下的index.html文件了，之后HTML文件都是通过webpack自动生成出来的‌。

  ```js
  const path = require('path')
  const { CleanWebpackPlugin } = require('clean-webpack-plugin')
  const HtmlWebpackPlugin = require('html-webpack-plugin')
  
  module.exports = {
    mode: 'none',
    entry: './src/main.js',
    output: {
      filename: 'bundle.js',
      path: path.join(__dirname, 'dist'),
    },
    module: {
      rules: [
        {
          test: /.css$/,
          use: [
            'style-loader',
            'css-loader'
          ]
        },
        {
          test: /.png$/,
          use: {
            loader: 'url-loader',
            options: {
              limit: 10 * 1024 // 10 KB
            }
          }
        }
      ]
    },
    plugins: [
      new CleanWebpackPlugin(),
      // 用于生成 index.html
      new HtmlWebpackPlugin(),
      })
    ]
  }
  
  ```

- 生成HTML基本标签以及使用模板生成HTML

  有了html-webpack-plugin之后，就可以动态生成应用所需要的的HTML文件，但是这里仍然存在一些需要改进的地方。

  首先是HTML中的标题必须要修改，其次是很多时候需要自定义页面当中的一些元数据标签和一些基本的DOM结构。对于简单的自定义，可以使用修改webpack.config.js文件中的html-webpack-plugin属性，如下：

  ```js
  plugins: [
      new CleanWebpackPlugin(),
      // 用于生成 index.html
      new HtmlWebpackPlugin({
          title: 'Webpack Plugin Sample',  // 生成html文件的标题
          meta: {
              viewport: 'width=device-width'  // 生成一些自定义的dom元素
          },
      }),
  ]
  ```

  如果需要对HTML文件进行大量的自定义的话，需要在源代码中添加一个用于生成HTML文件的模板文件，让html-webpack-plugin根据模板生成页面。在src目录中添加index.html文件，根据需要在模板中添加一些响应的元素。模板中希望动态输出一些内容，采用lodash模板语法的方式：

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Webpack</title>
  </head>
  <body>
    <div class="container">
      <!--loadsh模板语法,访问插件中的options属性中的title值-->
      <h1><%= htmlWebpackPlugin.options.title %></h1>
    </div>
  </body>
  </html>
  
  ```

  htmlWebpackPlugin.options实际是html-webpack-plugin内部提供的一个变量，也可以通过另外一个属性去添加一些自定义变量。然后通过template属性去指定模板文件。再次使用yarn webpack指令去打包项目，发现dist中的index.html出现了自定义的内容。

  ```js
  plugins: [
    new CleanWebpackPlugin(),
    // 用于生成 index.html
    new HtmlWebpackPlugin({
      title: 'Webpack Plugin Sample',
      meta: {
        viewport: 'width=device-width'
      },
      template: './src/index.html'  // 用于指向模板文件的路径
    }),
  ]
  ```

- 输出多个页面文件

  除了自定义输出文件的内容，同时输出多个页面文件也是一个非常常见的需求。其实配置非常简单，配置文件中添加一个新的HtmlWebpackPlugin对象，配置如下：

  ```js
    plugins: [
      new CleanWebpackPlugin(),
      // 用于生成 index.html
      new HtmlWebpackPlugin({
        title: 'Webpack Plugin Sample',
        meta: {
          viewport: 'width=device-width'
        },
        template: './src/index.html'
      }),
      // 用于生成 about.html
      new HtmlWebpackPlugin({
        filename: 'about.html',  // 用于指定生成的文件名称，默认值是index.html
        title: 'About html'
      })
    ]
  ```

  

### 16. Webpack 插件使用总结

在项目中，一般还有一些不需要参与构建的静态文件，‌‌它们最终也需要发布到线上，‌‌例如我们网站的favicon.icon，‌‌一般会把这一类的文件统一放在项目的public目录当中，‌‌希望webpack在打包时，可以一并将它们复制到输出目录。

‌‌对于这种需求，可以借助于copy_webpack_plugin，‌‌先安装一下这个插件‌‌，然后再去导入这个插件的类型，‌‌最后同样在这个plugin属性当中去添加一个这个类型的实例，‌‌这类型的构造函数它要求传入一个数组，‌‌用于去指定需要去拷贝的文件路径，它可以是一个通配符，也可以是一个目录或者是文件的相对路径，‌‌这里使用plugin，‌‌它表示在打包时会将所有的文件全部拷贝到输出目录，‌‌再次运行webpack指令，‌‌打包完成过后，public目录下所有的文件就会同时拷贝到输出目录。

```js
const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
    // publicPath: 'dist/'
  },
  module: {
    rules: [
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10 * 1024 // 10 KB
          }
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    // 用于生成 index.html
    new HtmlWebpackPlugin({
      title: 'Webpack Plugin Sample',
      meta: {
        viewport: 'width=device-width'
      },
      template: './src/index.html'
    }),
    // 用于生成 about.html
    new HtmlWebpackPlugin({
      filename: 'about.html'
    }),
    new CopyWebpackPlugin([
      'public'
    ])
  ]
}
```

### 17. Webpack 开发一个插件

通过前面的了解，我们知道相比于loader，plugin的能力范围相对更广一些。loader只是在加载模块的环节去工作，‌而plugin‌范围几乎触及到工作的每一个环节。那么plugin的工作机制到底是怎么实现的？其实原理很简单，webpack的插件机制其实就是在软件开发中最常见的**钩子机制**。

钩子机制也很容易理解，有点类似于web中的事件。在webpack工作过程中有很多环节，为了便于插件的扩展，webpack几乎给每一个环节都埋下了一个钩子。这样的话，在开发插件的过程中，就可以通过钩子在不同节点上挂载不同的任务，这样可以轻松的扩展webpack能力。

![image-20201225204515446](https://img-blog.csdnimg.cn/img_convert/b214729faab49e936736b2a3b128deff.png)

接下来自定义一个插件，了解具体如何往钩子上挂在任务。webpack要求插件必须是一个函数或者是一个包含apply方法的对象。一般会把插件定义为一个类型，然后在类型汇总定义一个方法，使用的时候就是通过这个类型构建一个实例。

插件需求：

- 清除webpack打包生成中的bundle.js中的每行首位的注释字符

  ![image-20201225204923683](https://img-blog.csdnimg.cn/img_convert/506d31733528ee2fb859b353b8759fee.png)

webpack.config.js

```js
const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

class MyPlugin {
  apply (compiler) {
    console.log('MyPlugin 启动')
    // 通过compiler的hooks方法访问emit，并通过tap方法注册一个钩子函数。参数一：插件名称；参数二：挂载到钩子上的函数
    compiler.hooks.emit.tap('MyPlugin', compilation => {
      // compilation => 可以理解为此次打包的上下文
      // compilation.assets打包过程中所有的资源信息
      for (const name in compilation.assets) {
        // console.log(name)  // 每个打包成功后的文件名
        // console.log(compilation.assets[name].source())  // 通过键值访问对应文件名的资源
        if (name.endsWith('.js')) {
          // 获取后缀为.js的文件资源
          const contents = compilation.assets[name].source()
          // 使用全局正则替换注释
          const withoutComments = contents.replace(/\/\*\*+\*\//g, '')
          // 将替换后的结果覆盖到原文件中
          compilation.assets[name] = {
            source: () => withoutComments,  // 暴露最新的内容
            size: () => withoutComments.length  // 暴露最新内容的长度
          }
        }
      }
    })
  }
}

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
    // publicPath: 'dist/'
  },
  module: {
    rules: [
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10 * 1024 // 10 KB
          }
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    // 用于生成 index.html
    new HtmlWebpackPlugin({
      title: 'Webpack Plugin Sample',
      meta: {
        viewport: 'width=device-width'
      },
      template: './src/index.html'
    }),
    // 用于生成 about.html
    new HtmlWebpackPlugin({
      filename: 'about.html'
    }),
    new CopyWebpackPlugin([
      // 'public/**'
      'public'
    ]),
    new MyPlugin()
  ]
}

```

随后运行yarn webpack重新打包，发现每行前面的注释已经被去除掉了。

### 18. Webpack 开发体验的问题

在此之前，我们已经了解了一些webpack的相关概念和一些基本的用法，‌‌但是如果以目前的状态去应对日常的开发工作还远远不够。‌‌那是因为编写源代码再通过webpack打包，然后，运行应用最后刷新浏览器这种周而复始的方式，过于原始。如果说在实际的开发中还按照这种方式去使用，那必然会大大降低我们的开发效率，‌‌应该如何去提高我们的开发效率？‌‌

在这里对理想的开发环境做一个设想，‌‌首先希望这样一个环境，它‌‌必须使用HTTP服务区运行而不是以文件的形式去预览。‌‌这样的话我们一来，‌‌更加接近生产环境的状态，‌‌二来可能会需要去使用ajax之类的一些API‌‌，这些API使用文件的形式‌‌去访问是不被支持的。其次‌‌我们希望这样一个环境当中，我们去修改源代码过后，webpack就可以自动帮我们完成构建，然后浏览器可以即时显示最新的结果，‌‌这样的话就可以大大减少在开发过程中额外的重复操作，‌‌最后，还需要这样一个环境，它能够去提供Source Map支持，这样的话，我们运行过程当中一旦出现错误，就可以根据错误的堆栈信息，快速定位到源代码当中对应的位置，‌‌便于调试应用，‌。那对于以上这些需求，‌‌webpack都已经有相对应的功能去实现，‌‌接下来让重点了解具体如何增强使用webpack的开发体验。

### 19. Webpack 自动编译及自动刷新浏览器

**自动编译**

- 目每次修改完源代码都是‌‌通过命令行手动重复运行webpack命令，从而得到最新的打包结果。‌‌那这种办法，‌‌我们也可以使用webpack cli提供的watch的工作模式。如果之前了解过其它的构建工具，那应该对这种模式并不陌生。

  在这种模式下，项目下的源文件会被监视，一旦这些文件发生变化，它就会‌‌自动重新去运用打包任务。具体的用法也非常简单，就是在启动webpack命令时添加    **--watch**命令参数，‌‌‌‌这样的话，webpack就会以监视模式去运行。在打包完成过后，cli不会立即退出，‌‌而是会等待文件的变化，然后再次工作，‌‌一直到手动结束这个cli。

  这种模式下，‌‌我们就只需要专注编码，‌‌不必再去手动完成这些重复的工作了。这里，可以再开启一个新的命令行终端，‌‌同时以http的形式去运行应用，‌‌然后，我们打开浏览器去预览，‌‌尝试修改源代码，‌‌以观察模式工作的webpack就会自动重新打包，‌刷新页面，查看最新的页面结果。‌

**自动刷新浏览器**

- 使用browser-sync去监听目录，并自动刷新浏览器

  ```shell
  browser-sync dist --files "**/*"
  ```



### 20. Webpack Dev Server

Webpack Dev Server是webpack官方推出的一个开发工具，根据名字，就应该知道它提供了一个开发服务器，并且，它将自动编译和自动刷新浏览器等一系列对开发非常友好的功能全部集成在了一起。这个工具可以直接解决我们之前的问题。

因为这是一个高度集成的工具，所以它使用起来也非常的简单。

- 打开命令行，以开发依赖安装

  ```
  yarn add webpack-dev-server --dev
  ```

它提供了一个webpack-dev-server的cli程序，那我们同样可以直接通过yarn去运行这个cli，或者，可以把它定义到npm script中。运行这个命令                        **yarn webpack-dev-server**，它内部会自动去使用webpack去打包应用，并且会启动一个HTTP server去运行打包结果。在运行过后，它还会去监听我们的代码变化，一旦语言文件发生变化，它就会自动立即重新打包，这一点，与watch模式是一样的。不过这里也需要注意webpack-dev-serverr为了提高工作效率，**它并没有将打包结果写入到磁盘当中**，它是将打包结果，暂时存放在内存当中，而内部的HTTP server从内存当中把这些文件读出来，然后发送给浏览器。这样一来的话它就会减少很多不必要的磁盘读写操作，从而大大提高我们的构建效率。

这里，我们还可以为这个命令传入一个**--open**的参数，它可以用于去自动唤起浏览器，去打开我们的运行地址，打开浏览器过后（如果说你有两块屏幕的话），你就可以把浏览器放到另外一块屏幕当中，然后，我们去体验这种一边编码，一边即时预览的开发环境了。

```shell
yarn webpack-dev-server --open
```

### 21. Webpack Dev Server静态资源访问

web-dev-server默认会将构建结果输出的文件，全部作为开发服务器的资源文件，也就是说，只要是通过webpack的打包能够输出的文件，都可以正常被访问到。但是如果说还有一些静态资源也需要作为开发服务器的资源被访问的，那就需要额外的去告诉webpack-dev-server。

它具体的方法就是在我们**webpack.config.js**的配置文件当中去添加一个对应的配置，在配置对象当中去添加一个**devServer**的属性，这个属性是专门用来为webpack制定相关的配置选项，可以通过这个配置对象的**contentBase**属性来去制定额外的静态资源路径，这个属性可以是一个字符串或者是一个数组，也就是说可以配置一个或者是多个路径，这里将这个路径设置为项目根目录当中的public目录。

```js
  devServer: {
    contentBase: './public',
  },
```

那可能有人会有疑问，因为之前（[**1.16 Webpack 插件使用总结**]()），已经通过插件将这个目录输出了，那按照刚刚的说法，我们所有输出的文件都可以直接被server，也就是直接可以在浏览器端访问到。那按道理来讲的话，这里这些文件就不需要再作为开发服务器的额外的资源路径了。事实情况确实如此，如果说你能这么想的话，那也就证明你确实理解了这样一个点，但是，我们在实际去使用webpack的时候，我们一般都会把copyWebpackPlugin这样的插件留在上线前的那一次打包中使用，那在平时的开发过程当中，我们一般不会去使用它，这是因为在开发过程中我们会频繁、重复执行打包任务，那假设我们需要拷贝的文件比较多或者是比较大，如果说我们每次都去执行这个插件的话，我们打包过程当中的开销就会比较大，速度自然也就会降低了。由于这是额外的话题，所以说具体的操作方式，就是具体怎么样去让我们在开发阶段，不去使用copyWebpackPlugin，然后在上线前那一刻我们再去使用这种插件，那这种操作方式我们在后续再来介绍。

那这里先注释掉**copyWebpackPlugin**，这样确保在打包过程当中不会再去输出public目录当中的静态资源文件，然后回到命令，再次执行**webpack-dev-server**，启动过后，此次**public**目录当中并没有被拷贝到输出目录，如果说webpack只去加载那些打包生成的文件，那public目录文件应该是访问不到的，但是通过刚才的**contentBase**已经将它指定为了额外的资源路径，所以说应该可以访问到。打开浏览器，去访问页面文件以及bundle.js，都是来源于打包结果当中，然后再去尝试访问一下favicon.ico，这个文件就是来源于contentBase当中所配置的public目录了，除此之外，例如这个other.html文件，它也是这个目录当中所指定的文件。以上，就是contentBase，它可以用来去为webpack额外去指定一个静态资源目录的操作方式。

```js
const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist')
  },
  devServer: {
    contentBase: './public',
  },
  module: {
    rules: [
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10 * 1024 // 10 KB
          }
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    // 用于生成 index.html
    new HtmlWebpackPlugin({
      title: 'Webpack Tutorials',
      meta: {
        viewport: 'width=device-width'
      },
      template: './src/index.html'
    }),
    // // 开发阶段最好不要使用这个插件
    // new CopyWebpackPlugin(['public'])
  ]
}

```

### 22. Webpack Dev Server 代理API

由于开发服务器的缘故，这里会将应用运行在**localhost:8080**，而最终上线过后，应用一般又和API会部署到同源地址下面。这样就会有一个非常常见的问题，那就是在实际生产环境当中，可以直接去访问API，但是回到开发环境当中就会产生跨域请求问题。

可能有人会说可以使用**跨域资源共享的方式**去解决这个问题，事实确实如此。如果请求的这个API支持CORS，这个问题就不成立了，但是，并不是每种情况下，服务端的API都一定要支持CORS的。如果说前后端同源部署，也就是我们的域名、协议、端口是一致，这种情况下根本没有必要去开启CORS，所以以上这个问题还是经常会出现，那解决这个问题最好的办法就是在开发服务器当中去配置**代理（proxy）**服务，也就是把接口服务代理到本地的这个开发服务地址。webpack-dev-server它支持直接通过配置的方式去添加代理服务。

![image-20210104225050518](https://img-blog.csdnimg.cn/img_convert/228f1a0798522ba345959f4091e5fecc.png)

![image-20210104225107315](https://img-blog.csdnimg.cn/img_convert/04e34f2d5a0fcf0deeb6782046c9946f.png)

具体的用法如下，目标就是将github的API代理到本地的开发服务器当中，先在浏览器当中尝试去访问一下其中的一个接口https://api.github.com/users

![image-20210104225350650](https://img-blog.csdnimg.cn/img_convert/6a645326ce94268c8b5496c8b15d938e.png)

Github的接口的**Endpoint（可以理解为接口端点/入口）**，它一般都是在根目录下，例如这里所使用的这个users这个Endpoint，知道了接口的地址过后，回到配置文件当中，在devServer当中去添加一个proxy属性，这个属性专门用来去添加代理服务配置的。这个属性是一个对象，其中每一个属性的就是一个代理规则的配置，那属性的名称，就是**需要被代理的请求路径前缀，也就是请求以哪个地址开始**，它就会走代理请求。但一般为了容易辨别，都会将其设置为"/api"，也就是请求开发服务器当中的"/api"开头的这种地址，都会让它代理到接口当中。

它的值是为这个前缀所匹配到的这个代理规则配置，将代理目标设置为"https://api.github.com"，也就是说当请求以斜线开头，代理目标就是https://api.github.com。此时如果去请求"http://localhost:8080/api/users"，就相当于请求了"https://api.github.com/api/users"。意思是请求的路径是什么，它最终代理的这个地址、路径是会完全一致的。

而实际需要请求的这个接口地址，实际上是在"https://api.github.com/users"，也就是跟路径下面的"users"，所以说对于代理路径当中的"/api"，需要通过重写的方式把它去掉，可以在这儿再去添加一个**pathRewrite**属性，来去实现代理路径的重写。重写规则就是把路径当中以"/api"开头的这个开头的这段字符串给它替换为空。**pathRewrite属性**，它最终会以正则的方式来去替换请求的路径，所以在这儿，以**"^"**表示开头。

除此之外，还需要设置changeOrigin属性为true，这是因为默认代理服务器的会以实际在浏览器当中请求的主机名，在这里就是**localhost:8080**作为代理请求的主机名。也就是在浏览器端对这个代理过后的这个地址发起请求，这个请求背后，它肯定还需要去请求到github服务器，请求的过程当中会带一个主机名，这个主机名默认情况下使用的是用户在浏览器端发起请求的主机名，也就是**localhost:8080**。而一般情况下服务器需要根据主机名去判断这一台主机名，因为一个请求请到服务器过后，服务器一般会有多个网站，它会根据主机名去判断这个请求是属于哪个网站，然后把这个请求指派到对应的网站。**localhost:8080**对于github来说肯定是不认识，所以说这里需要去修改，**"changeOrigin=true"**的这种情况下就会以实际代理请求发生的过程当中的主机名去请求。请求github的地址，真正请求的应该是https://api.github.com，所以说主机名就会保持原有状态。这个时候，就不用再关心最终把它代理成什么样，只需要去正常的请求就可以了。

webpack.config.js

```js
const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  ...
  devServer: {
    contentBase: './public',
    proxy: {
      '/api': {
        // http://localhost:8080/api/users -> https://api.github.com/api/users
        target: 'https://api.github.com',
        // http://localhost:8080/api/users -> https://api.github.com/users
        pathRewrite: {
          '^/api': ''
        }, 
        // 不能使用 localhost:8080 作为请求 GitHub 的主机名
        changeOrigin: true
      }
    }
  },
  ...
}

```

![image-20210104232606884](https://img-blog.csdnimg.cn/img_convert/841009c4c57e569d0eaf802bde0efcce.png)



main.js中添加代理过后的地址：

```js
// 跨域请求，虽然 GitHub 支持 CORS，但是不是每个服务端都应该支持。
// fetch('https://api.github.com/users')
fetch('/api/users') // http://localhost:8080/api/users
  .then(res => res.json())
  .then(data => {
    data.forEach(item => {
      const li = document.createElement('li')
      li.textContent = item.login
      ul.append(li)
    })
  })
```

![image-20210104232804802](https://img-blog.csdnimg.cn/img_convert/a9a9dbc6de2632b95efa275fdcea6478.png)

### 23. Source Map介绍

通过构建编译之类的操作，可以将开发阶段的源代码转换为能够在生产环境当中运行的代码，这是一种进步。但是这种进步的同时，也就意味着在实际生产环境当中运行的代码，与开发阶段所编写的代码之间会有很大的差异，在这种情况下，如果需要去调试应用，又或是运行应用的过程当中出现了意料之外的错误，我们将无从下手，这是因为无论是调试还是报错，它都是基于转换过后的代码来进行的，**Source map**就是解决这一类问题最好的一个办法。

其名字就已经表述了它的作用，叫做**源代码地图**，它是用来映射转换过后的代码与原代码之间的一个关系。一段转换过后的代码，通过转换过程当中生成的这个Source map文件，就可以逆向得到源代码。

![image-20210105205023140](https://img-blog.csdnimg.cn/img_convert/9c34c2fa48f3be49771a9f6fd88bac77.png)

![image-20210105205044813](https://img-blog.csdnimg.cn/img_convert/a6eed25cc06d3c7cfd7a328c260edb72.png)

目前，很多第三方的库在去发布的文件当中，都会有一个**".map"**后缀的文件，例如这里，可以打开**jquery-3.4.1.min.map**文件看一下，这是一个json格式的文件，这个文件里面记录的就是转换过后的代码与转换之前代码之间的映射关系。

主要有这几个属性，简单来看一下：

- 首先是**version**，它指的是当前这个文件所使用的**source map**的标准的版本，

- 然后是**"sources"**属性，这个属性中记录的是转换之前源文件的名称，因为很有可能是多个文件合并转换为了一个文件，所以说这里这个属性是一个数组。

- 再然后是**"name"**属性，这个指的是源代码当中使用的一些成员名称，在压缩代码时，会将开发阶段所编写的那些有意义的变量名替换为一些简短的字符，从而去压缩整体代码的体积，这个属性中记录的是原始对应的那些名称。

- 最后是**"mappings"**的属性，这个属性其实是整个**source map**文件的核心属性，它是一个**Base64-VLQ**编码的一个字符串，该字符串记录的信息，就是转换过后代码当中的字符与转换之前所对应的映射关系。

有这样一个文件后，一般会在转换过后的代码当中，通过添加一行注释的方式来引入这个source map文件，不过这个特性**它只是用来帮助开发者更容易去调试和定位错误的**，所以说它**对生产环境其实没有什么太大的意义**，在最新版的jquery中，已经去除了引用source map的注释。这里想要去尝试的话，需要手动的添加回来。

![image-20210105220338185](https://img-blog.csdnimg.cn/img_convert/d89b2612a1751c14b9f572143d6e8fb2.png)

这里在jquery.min.js文件当中，最后一行去添加一个注释**"//# sourceMappingURL=jquery-3.4.1.min.map"**，这样在浏览器当中如果打开了开发人员工具的，开发人员工具加载到的这个js文件最后有这么一行注释，它就会自动去请求这个**source map**文件，然后根据这个文件的内容，逆向解析出来对应的源代码，以便于调试，同时因为有了映射的关系，当源代码当中出现了错误，也就很容易能定位到源代码当中对应的位置。

这里简单总结一下，source map的它解决的就是在前端方向引入了构建编译之类的概念过后，导致前端编写的源代码与运行的代码之间，不一样所产生的那些调试的问题。 

### 24. Webpack 配置 Source Map

webpack打包过程同样支持为打包结果生成对应的source map文件。用法上也非常简单，不过它提供了很多不同的模式，这就导致大部分的初学者可能会比较懵。将来一起去研究webpack中如何去配置使用source map以及它几种不同模式之间的一些差异。

回到**webpack.config.js**配置文件当中，这里需要使用的一个配置属性——**devtool**，这个属性是用来去配置开发过程中的辅助工具，也就是与source map相关的一些功能配置，这里可以直接将这个属性设置为source map，然后打开命令行终端，运行**yarn webpack**。打包完成过后，打开所生成的dist的目录，此时在这个目录当中就会生成bundle.js和它对应的map文件。而且打开bundle.js，找到这个文件的最后，这个文件的最后也通过注释的方式去引入了这个soft map文件。

![image-20210105221909190](https://img-blog.csdnimg.cn/img_convert/658ccbdde0f3bbc8f564ba498a22ad7e.png)

![image-20210105221940611](https://img-blog.csdnimg.cn/img_convert/76dd1e9918d6b5f7c62b0dc3fa34e5ce.png)

如果只是这么去使用，实际的效果就会差的比较远，为什么这么说，因为截止到目前，webpack对source map的风格支持很多种，也就是说它有很多实现方式，那每种方式所生成的source map的效果，以及生成source map的速度都是不一样的，很简单也很明显的一个道理就是效果最好的，一般它的生成速度也就会最慢，而速度最快的一般生成出来的这个source map文件也就没有什么效果，具体哪种方式才是最好或者说最适合的，后续还需要继续去探索。

### 25. Websocket eval 模式的 Source Map

webpack.config.js中的devtool，它除了可以使用source-map，还支持很多其它的模式，具体的可以参考文档当中有一个不同模式之间的一个对比表。

![](http://5coder.cn/img/1667310740_574150a1b5969406e7b1d049a2e986f3.png)

这张表中分别从初次构建速度、重新打包速度、是否适合在生产环境中使用以及所生成的方式、source map的质量这四个维度，去对比了这些不同方式之间的一些差异，表格当中对比可能不够明显，所以接下来配合表格中的介绍，通过具体的尝试来去体会这些不同模式之间的差异，从而找到适合自己的最佳实践。

首先来看一个叫做**eval**的模式，eval是js当中的一个函数，它可以用来去运行我们字符串当中的js代码，这里可以尝试一下，通过一位去执行一个"console.log(123)"，默认情况下这段代码会运行在一个临时的虚拟机当中，可以通过source URL来去声明这段代码所属的文件路径，这里再来尝试执行一下，在这段js代码字符串当中去添加一个注释内容，就是**"#sourceURL='./foo/bar.js'"**，回车执行，此时这段代码它所运行的这个环境就是"./foo/bar.js"，这也就意味着可以通过**sourceURL**来去改变我们通过eval执行的这段代码所属的这种环境的一个名称，其实它还是运行在这个虚拟环境当中，只不过它告诉了执行引擎我这段代码所属的这个文件路径，这只是一个标识而已。

![image-20210105225714952](https://img-blog.csdnimg.cn/img_convert/97b12b652b18092a912201420823340c.png)

了解了这样一个特点过后，回到配置文件中，这里将devtool属性设置为**"eval"**。也就是使用eval模式，然后回到命令行终端，再次运行打包，打包完成过后去运行一下这个应用，然后回到浏览器，刷新一下页面，此时根据控制台的提示，就能找到这个错误所出现的文件，但是当打开这个文件，看到的却是打包过后的模块代码，那这是为什么？因为在这种模式下，它会将每一个模块所转换过后的代码都放在eval函数当中去执行，并且在这个一位函数执行的字符串的最后通过sourceURL的方式去说明所对应的文件路径，这样的话浏览器再通过eval去执行这段代码的时候就知道这段代码所对应的源代码是哪一个文件，从而实现定位错误所出现的文件，但只能去定位文件，这种模式下它不会去生成source map文件，也就是说实际上，跟source map没有什么太大关系，所以说它的构建速度也就是最快的，但是它的效果也很简单，它只能定位源代码文件的名称，而不知道具体的行列信息。

### 26. Webpack devtool模式对比

为了可以更好的对比不同模式的source map之间的差异，这里使用一个新的项目来同时创建出不同模式下的打包结果，然后通过具体的实验来去横向对比它们之间的差异。

目录结构:

![image-20210105230753043](https://img-blog.csdnimg.cn/img_convert/3fadec29dc44da4fca828a9a4e14a857.png)

打开webpack.config.js的配置文件，在这个文件当中已经提前定好了一个数组，数组中的每一个成员就是配置取值的一种。

```js
const allModes = [
	'eval',
	'cheap-eval-source-map',
	'cheap-module-eval-source-map',
	'eval-source-map',
	'cheap-source-map',
	'cheap-module-source-map',
	'inline-cheap-source-map',
	'inline-cheap-module-source-map',
	'source-map',
	'inline-source-map',
	'hidden-source-map',
	'nosources-source-map'
]
```

循环遍历这个数组，编写webpack.config.js内容，具体内容如下：

```js
const HtmlWebpackPlugin = require('html-webpack-plugin')

const allModes = [
	'eval',
	'cheap-eval-source-map',
	'cheap-module-eval-source-map',
	'eval-source-map',
	'cheap-source-map',
	'cheap-module-source-map',
	'inline-cheap-source-map',
	'inline-cheap-module-source-map',
	'source-map',
	'inline-source-map',
	'hidden-source-map',
	'nosources-source-map'
]

module.exports = allModes.map(item => {
	return {
		devtool: item,
		mode: 'none',
		entry: './src/main.js',
		output: {
			filename: `js/${item}.js`
		},
		module: {
			rules: [
				{
					test: /\.js$/,
					use: {
						loader: 'babel-loader',
						options: {
							presets: ['@babel/preset-env']
						}
					}
				}
			]
		},
		plugins: [
			new HtmlWebpackPlugin({
				filename: `${item}.html`
			})
		]
	}
})
```

配置一个html- webpack-plugin，也就是为每一个打包任务去生成一个HTML文件，通过前面的了解，应该知道，html可以用来生成一个使用打包结果的html，待会儿，就是通过这些HTML在浏览器当中去尝试这些不同的打包结果。

这样的配置可以一次生成多个打包任务，对应js目录中生成以数组allModes中每个元素命名的js文件。命令行通过yarn webpack运行结果如下：

![image-20210105231214786](https://img-blog.csdnimg.cn/img_convert/a5ad8a64cd481092f9c98da5e8caaf4e.png)

命令行运行serve dist：

![image-20210105231749697](https://img-blog.csdnimg.cn/img_convert/f7670b12154c84e20458bed591ea59bd.png)

有了这些不同模式下的打包结果过后，接下来就可以一个一个仔细去对比了，这里先看几个比较典型的模式，然后找出它们之间的一些关系。

- **eval模式**

  它就是将模块代码放到eval函数当中去执行，并且通过sourceURL标注这个模块文件的路径，这种模式下它并没有生成对应的source map，它只能定位是哪一个文件出了错误；

- **eval-source-map**模式

  这个模式同样也是使用eval函数去执行模块代码，不过这里有所不同的是，它除了可以帮找到错误出现的文件，还可以定位到具体的行和列的信息，因为在这种模式下相比于eval，它生成了source map；

- **cheap-eval-source-map**模式

  这个模式的名字差不多就可以推断出来一些信息，它其实就是在上面的的**eval-source-map**基础之上加了一个cheap，用我们计算机行业经常说的一个词就是阉割版的source map，为什么这么说，因为它虽然也生成了source map，但是这种模式下的source map，它只能帮我们定位导航而没有列的信息，也就是少了一点效果，它的生成速度自然也就会快很多；

- **cheap-module-eval-source-map**模式

  根据这个名字慢慢的就发现webpack的这些模式的名字好像不是乱起的，它好像有某种规律，这里其实就是**cheap-eval-source-map**的这个模式基础之上多了一个module，在这种模式下的特点，可能乍一看不会那么明显，因为它也就只能定位导航，这里再来把刚刚**cheap-eval-source-map**的这个模式也找出来，然后，仔细做一个对比，通过仔细对比你会发现，**cheap-module-eval-source-map**定位源代码跟我们编写的源代码是一模一样的，而**cheap-eval-source-map**它显示的是经过ES6转换过后的结果，这样的话这两者之间的差异也就出来了，这也是为什么之前在配置的时候会给js文件单独配一个**loader**的原因，因为带有module的这种模式下，它解析出来的源代码是没有经过loader的加工，也就是真正手写的那些源代码，而不带module，它是加工过后的一个结果，如果说想要真正跟手写代码一样的源代码的话，就需要选择cheap module这种模式；

  ![image-20210105232046657](https://img-blog.csdnimg.cn/img_convert/1be43a5e8e051d5cba86c21d6b6c1bad.png)

了解了以上这些模式过后，基本上就可以算是通盘了解了所有的模式，因为其它的模式无外乎就是把这几个特点再次排列组合罢了。例如。**cheap-source-map**，它没有eval，也就意味着它没有用eval的方式去执行模块代码，没有module的话也就意味着它反过来的这个源代码，是处理过后的代码。

- **inline-source-map模式**

  它跟普通的其实效果上是一样的，只不过source map的这个模式下，它的这个source map文件是以物理文件的方式存在，它使用的是**data URL**的方式去将我们的source map嵌入到的代码当中，之前遇到的eval，它其实也是使用这种行内的这种方式把source map嵌入进来，那这种方式实际上我个人觉得是最不可能用到的，因为它把source map嵌入到源代码当中过后，这个时候就导致这个代码体积会变大很多。

- **hidden-source-map模式**

  这个模式下在开发工具当中是看不到效果的，但是回到开发工具当中，去找一下这个文件，会发现它确实生成了source map文件，这就跟jquery是一样的，在构建过程当中生成的文件，但是，它在代码当中并没有通过注册的方式去引入这个文件，所以说在开发工具当中看不到效果，这个模式实际上是在开发一些第三方包的时候会比较有用，我们需要去生成source map，但是不想在的这个代码当中直接去应用它们，一旦当使用这个包的开发者出现了问题，它可以再把这个source map手动引入回来或者通过其它的方式去使用source map。Source map还有很多其它的使用方式，通过http_header也可以去使用，这些就不在这儿扩展了。

- **nosource-source-map模式**

  这个模式下能看到错误出现的位置，但是点击这个错误信息，点进去过后是看不到源代码的，这个nosource指的就是没有源代码，但是它同样提供了行列信息，这样的话对于我们来讲，还是结合自己编写的源代码找到错误出现的位置，只是在开发工具当中看不到源代码，**这是为了在生产环境当中去保护源代码不会被暴露**。

以上，介绍了很多种的source map，也做了一些具体的对比，通过这些对比，大家要能总结出来这个source map里面这几个核心关键词，它们的一些特点，然后，对于其它几个模式没有介绍到的，就很容易能知道它们一些特点了。可能了解很多的这些模式过后，对大家来讲的，最痛苦的一件事情就是选择一个合适的source map模式，这个问题，下面接着来看。

### 27. Webpack 选择Source Map模式

虽然webpack可支持各种各样的source map模式，但是其实掌握它们的特点过后，发现一般在应用开发时，只会用到其中的几种，根本就没必要在选择上纠结。这里介绍一下个人在开发时的一些选择。

首先，在**开发模式**下会选择**cheap-module-eval-source-map**，原因有三点:

![image-20210106195430575](https://img-blog.csdnimg.cn/img_convert/7fc4c530f64c1ec55dfcece75e43c171.png)

- 第一是编写代码的风格一般会要求每一行代码不会超过80个字符，source map能够定位到行就够了，因为每一行里面最多也就80字符，很容易找到对应的位置；

- 第二是使用框架的情况会比较多，以react和vue来说，无论是使用jsx还是vue的单文件组件，loader转换过后的代码和转换之前都会有很大的差别，这里需要去调试转换之前的源代码，所以要选择有module的方式；

- 第三是虽然**cheap-module-eval-source-map**的初次启动就是打包启动速度会慢一些，但是大多数时间都是在使用webpack-dev-server，以监视模式去重新打包，而不是每次都启动打包，所以说这种模式下它重新打包速度比较快。

其次在**生产模式**下会选择**none**，原因很简单，因为source map会暴露源代码到生产环境，这样的话，但凡是有一点技术的人，都可以很容易去复原项目当中绝大多数的源代码。这一点，其实被很多开发者可能都忽略掉了，它们就光认为source map能够带来便利，但是带来这个便利的同时也会有一些隐患。其次，个人认为调试和报错找错误这些都应该是开发阶段的事情，应该在开发阶段就尽可能把所有的问题和隐患都找出来，而不是到了生产环境让全民去帮忙公测。所以这种情况就尽量避免不在生产环境区域使用source map，如果说对你的代码实在是没有信心的话，那我建议你选择nosource-map模式，这样当出现错误时，在控台当中就可以找到源代码对应的位置，但是不至于去向外暴露的源代码内容。

当然这个过程当中的选择实际上也没有绝对，去理解这些模式之间的差异的目的，就是为了可以在不同环境当中，快速去选择一个合适的模式，而不是去寻求一个通用的法则，在开发行业没有绝对的通用法则。

### 28. Webpack 自动刷新问题

在此之前已经简单了解了webpack dev serve的一些基本用法和特性，但它主要就是为使用webpack构建的项目，提供了一个比较友好的开发环境和一个可以用来调试的开发服务器。使用webpack就可以让开发过程更加专注于编码，因为它可以监视到代码的变化，然后自动进行打包，最后再通过自动刷新的方式同步到浏览器，以便于即时预览。但是当实际去使用这样一个特性去完成一些具体的开发任务时，会发现这里还是会有一些不舒服的地方，例如在编辑器的应用，想在编辑其中输入一些文字，然后手动调整css，希望试试更新输入的文字样式，但是这个时候编辑器当中的内容却没有了，这里不得不再来编辑器当中再去添加一些文本，那久而久之的话就会发现，自动刷新这样一个功能还是很鸡肋，它并没有想象的那么好用。这是因为每次修改完代码，webpack监视到文件的变化过后就会自动打包，然后自动刷新到浏览器，一旦页面整体刷新，那页面中之前的**任何操作状态**都会丢失，所以就会出现刚刚所看到的这样一个情况。但是，聪明的人一般都会有一些小办法，例如可以在代码当中先去写死一个文本到编辑器当中，这样即便页面刷新，也不会有丢失的这种情况出现。这些方法都需要去编写一些跟业务本身无关的一些代码，更好的办法自然是能够在页面不刷新的这种情况下，代码也可以及时的更新进去，针对这样的需求webpack同样也可以满足，接下来了解一下webpack当中如何去在页面不刷新的情况下，及时的去更新代码模块。

![image-20210106204519425](https://img-blog.csdnimg.cn/img_convert/e4d2ba0f41b3a87b83d63f636fd7ff77.png)

### 29. Webpack HMR 体验

HMR全称是**Hot Module Replacement**，叫做**模块热替换或者叫做模块热更新**。计算机行业经常听到一个叫做**热拔插**的名词，那指的就是可以在一个正在运行的机器上随时去插拔设备，而机器的运行状态是不会受插设备的影响，而且插上的设备可以立即开始工作，例如电脑上的USB端口就是可以热拔插的。

模块热替换当中的这个**热**，跟刚刚提到的热拔插实际上是一个道理，它们都是在运行过程中的**即时变化**，那**<u>webpack中的模块热替换指的就是可以在应用程序运行的过程中实时的去替换掉应用中的某个模块，而应用的运行状态不会因此而改变。</u>**

例如在应用程序的运行过程中，修改了某个模块，通过自动刷新就会导致整个应用整体的刷新，页面中的状态信息都会丢失掉，而如果这个地方使用的是热替换的话，就可以实现只将刚刚修改的这个模块实时的去替换到应用当中，不必去完全刷新应用。

### 30. Webpack 开启 HMR

对于热更新这种强大的功能而言，操作并不算特别复杂，了解一下具体如何去使用。HMR已经集成到webpack-dev-server中，所以就不需要再去单独安装什么模块，使用这个特性需要再去运行参数**--hot**开启这个特性。

目录结构：

![](http://5coder.cn/img/1667310768_a3c09648a233d6245318ae340a4549ec.png)

```shell
yarn webpack-dev-server --hot
```

也可以使用配置的方式去打开HMR热更新

webpack.config.js

```js
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  mode: 'development',
  entry: './src/main.js',
  output: {
    filename: 'js/bundle.js'
  },
  devtool: 'source-map',
  devServer: {
    hot: true
    // hotOnly: true // 只使用 HMR，不会 fallback 到 live reloading
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.(png|jpe?g|gif)$/,
        use: 'file-loader'
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Webpack Tutorial',
      template: './src/index.html'
    }),
    new webpack.HotModuleReplacementPlugin()  // 必须开启插件
  ]
}

```

修改editor.css文件，发现浏览器并没有刷新页面，而且修改的内容也自动更新到浏览器上了。

### 31. Webpack 处理JS模块热替换

但是js文件好像有问题，修改js文件后，浏览器依然进行刷新，这是因为webpack-dev-server不知道如何去重新构建js模块。这是需要手动进行配置。

进入webpack打包的主入口文件main.js，添加如下代码（只针对当前编辑器案例）

```js
import createEditor from './editor'
import background from './better.png'
import './global.css'

const editor = createEditor()
document.body.appendChild(editor)

const img = new Image()
img.src = background
document.body.appendChild(img)

if (module.hot) {  // 判断hot是否开启，防止js出现错误后页面刷新后错误信息不被保留
  let hotEditor = editor  // 预先保存editor用于下次热更新使用
  module.hot.accept('./editor.js', () => {
    const value = hotEditor.innerHTML  // 预先保存页面状态信息（这里为编辑器输入的文本信息）
    document.body.removeChild(hotEditor)  // 移除原先的editor
    hotEditor = createEditor()  // 使用createEditor创建新的editor
    hotEditor.innerHTML = value  // 在新的editor中写入上面保留的页面状态信息
    document.body.appendChild(hotEditor)  // 将新的editor更新到页面中
  })
}
```

### 32. Webpack 处理图片模块热替换

```js
import createEditor from './editor'
import background from './better.png'
import './global.css'

const editor = createEditor()
document.body.appendChild(editor)

const img = new Image()
img.src = background
document.body.appendChild(img)

// ============ 以下用于处理 HMR，与业务代码无关 ============

// console.log(createEditor)

if (module.hot) {
  let lastEditor = editor
  module.hot.accept('./editor', () => {
    // console.log('editor 模块更新了，需要这里手动处理热替换逻辑')
    // console.log(createEditor)

    const value = lastEditor.innerHTML
    document.body.removeChild(lastEditor)
    const newEditor = createEditor()
    newEditor.innerHTML = value
    document.body.appendChild(newEditor)
    lastEditor = newEditor
  })

  module.hot.accept('./better.png', () => {
    img.src = background  // 重新赋值图片src路径
  })
}

```

### 33. Webpack 生产环境优化

前面了解到的一些用法和特性都是为了可以在开发阶段，拥有更好的开发体验，而这些体验提升的同时，webpack打包结果也会随之变得越来越臃肿，这是因为在这个过程中webpack为了实现这些特性，它会自动往打包结果中添加一些额外的内容，例如之前所使用到的**source map和HMR**，它们都会往输出结果当中去添加额外的代码来去实现各自的功能，但是这些额外的代码对于生产环境来讲是容易的，因为生产环境跟开发环境有了很大的差异，**在生产环境中强调的是以更少量，更高效的代码去完成业务功能，也就是说会更注重运行效率**。而在**开放环境中，只注重开发效率**，那针对这个问题，webpack当中就推出了**mode**的用法，那它提供了不同模式下的一些预设配置，其中生产模式中就已经包括了很多在生产环境当中所需要的优化配置，同时webpack也建议我们为不同的工作环境去创建不同的配置，以便于让打包结果可以适用于不同的环境。接下来一起来去探索一下生产环境中有哪些值得优化的地方以及一些注意事项。

### 34.  Webpack 不同环境下的配置

尝试为不同的工作环境以创建不同的webpack配置。创建不同的环境配置的方式主要有两种：

- 第一种是在配置文件中添加相应的配置判断条件，根据环境的判断条件的不同导出不同的配置。

  webpack配置文件支持导出函数，函数中返回所需要的的配置对象，函数接受两个参数，第一个是env（cli传递的环境名参数），第二个是argv（运行cli过程中传递的所有参数）。可以借助这样一个特点来去实现不同的开发环境和生产环境分别返回不同的配置。

  ```js
  const webpack = require('webpack')
  const { CleanWebpackPlugin } = require('clean-webpack-plugin')
  const HtmlWebpackPlugin = require('html-webpack-plugin')
  const CopyWebpackPlugin = require('copy-webpack-plugin')
  
  module.exports = (env, argv) => {
    const config = {
      mode: 'development',
      entry: './src/main.js',
      output: {
        filename: 'js/bundle.js'
      },
      devtool: 'cheap-eval-module-source-map',
      devServer: {
        hot: true,
        contentBase: 'public'
      },
      module: {
        rules: [
          {
            test: /\.css$/,
            use: [
              'style-loader',
              'css-loader'
            ]
          },
          {
            test: /\.(png|jpe?g|gif)$/,
            use: {
              loader: 'file-loader',
              options: {
                outputPath: 'img',
                name: '[name].[ext]'
              }
            }
          }
        ]
      },
      plugins: [
        new HtmlWebpackPlugin({
          title: 'Webpack Tutorial',
          template: './src/index.html'
        }),
        new webpack.HotModuleReplacementPlugin()
      ]
    }
  
    if (env === 'production') {
      config.mode = 'production'
      config.devtool = false
      config.plugins = [
        ...config.plugins,  // ES6将几个数组组合起来，生产环境下需要clean-webpack-plugin和copy-webpack-plugin
        new CleanWebpackPlugin(),
        new CopyWebpackPlugin(['public'])
      ]
    }
    return config
  }
  
  ```

  命令行运行：yarn webpack，当没有传递env参数时，webpack会默认mode为开发阶段（development），对应的public下的文件不会被复制。

  命令行运行：yarn webpack --env production，传递env参数后，webpack以生产环境（production）进行打包，额外的插件会工作，public目录下的文件会被复制。

  这就是通过在导出函数中对环境进行判断，从而去实现为不同的环境倒出不同的配置，当然也可以直接在全局去判断环境变量，然后直接导出不同的配置，这样也是可以的。

- 第二种是为不同的环境单独添加一个配置文件，确保每一个环境下面都会有一个对应的配置文件。

  通过判断环境参数数据返回不同的配对象，这种方式只适用于中小型项目。因为一旦项目变得复杂，配置文件也会一起变得复杂起来，所以说对于大型的项目，还是建议大家使用不同环境去对应不同配置文件的方式来实现。一般在这种方式下面，项目当中至少会有三个webpack配置文件，其中两个（webpack.dev.js/webpack.prod.js）是用来适配不同的环境的，那另外一个是一个公共的配置(webpack.common.js)。因为开发环境和生产环境并不是所有的配置都完全不同，所以说需要一个公共的文件来去抽象两者之间相同的配置。

  项目目录：

  ![image-20210106222819337](https://img-blog.csdnimg.cn/img_convert/c190385f1777089a4fcff11e656b2b29.png)

  webpack.common.js

  ```js
  const HtmlWebpackPlugin = require('html-webpack-plugin')
  
  module.exports = {
    entry: './src/main.js',
    output: {
      filename: 'js/bundle.js'
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            'style-loader',
            'css-loader'
          ]
        },
        {
          test: /\.(png|jpe?g|gif)$/,
          use: {
            loader: 'file-loader',
            options: {
              outputPath: 'img',
              name: '[name].[ext]'
            }
          }
        }
      ]
    },
    plugins: [
      new HtmlWebpackPlugin({
        title: 'Webpack Tutorial',
        template: './src/index.html'
      })
    ]
  }
  
  ```

  webpack.dev.js

  ```js
  const webpack = require('webpack')
  const merge = require('webpack-merge')
  const common = require('./webpack.common')
  
  module.exports = merge(common, {
    mode: 'development',
    devtool: 'cheap-eval-module-source-map',
    devServer: {
      hot: true,
      contentBase: 'public'
    },
    plugins: [
      new webpack.HotModuleReplacementPlugin()
    ]
  })
  ```

  webpack.prod.js

  ```js
  const merge = require('webpack-merge')
  const { CleanWebpackPlugin } = require('clean-webpack-plugin')
  const CopyWebpackPlugin = require('copy-webpack-plugin')
  const common = require('./webpack.common')
  
  module.exports = merge(common, {
    mode: 'production',
    plugins: [
      new CleanWebpackPlugin(),
      new CopyWebpackPlugin(['public'])
    ]
  })
  ```

  webpack-merge提供了更加智能的配置合并，使用yarn add webpack-merge --dev安装到生产环境中。将common中的配置分别于dev和prod组合，生产新的配置。

  命令行运行

  ```shell
  yarn webpack --config webpack.prod.js  # --config用于指定配置文件
  # 或者 yarn webpack --config webpack.dev.js
  ```

  如果觉得使用命令行太过麻烦，也可以在package.json进行配置

  ```js
    "scripts": {
      "prod": "webpack --config webpack.prod.js",
      "dev": "webpack --config webpack.dev.js"
    },
  ```

  随后命令行运行

  ```shell
  yarn prod  # 或者yarn dev
  ```

### 35. Webpack DefinePlugin

webpack4中新增的production模式下，内部新增了很多通用的优化功能。对于使用者而言，这种开箱即用的体验是非常棒的，但是对于学习者而言这种开箱即用会导致学习者忽略很多需要了解的东西，以至于出现问题后无从下手。如果需要深入了解webpack的使用，建议可以单独研究一下每个配置背后的作用。这里先学习几个主要的优化配置，顺便去了解webpack是如何优化打包结果的。

- DefinePlugin

  为代码注入全局成员，production模式下DefinePlugin会被启用，并且往代码中注入了一个常量：process.ev.NODE_ENV。很多第三方模块都是通过这个成员去判断当前的运行环境，从而去决定是否执行例如打印日志的这些操作。下面单独使用这个插件。

  webpack.config.js

  ```js
  const webpack = require('webpack')  // DefinePlugin为webpack内置插件
  
  module.exports = {
    mode: 'none',
    entry: './src/main.js',
    output: {
      filename: 'bundle.js'
    },
    plugins: [
      new webpack.DefinePlugin({
        // 值要求的是一个代码片段，该对象中每一个键值都会被注入到代码中
        // API_BASE_URL: 'https://api.example.com'  // 错误写法 第一步写法
        // API_BASE_URL: '"https://api.example.com"'  // 正确写法
        API_BASE_URL: JSON.stringify('https://api.example.com')
      })
    ]
  }
  
  ```

  main.js

  ```js
  console.log(API_BASE_URL)
  ```

  bundle.js

  ```js
  // 错误写法
  /***/ (function(module, exports) {
  
  console.log(https://api.example.com)  // 按照第一步写法，报错，非JavaScript代码段
  
  
  /***/ })
  /******/ ]);
  
  //  正确写法
  /***/ (function(module, exports) {
  
  console.log("https://api.example.com")  // 按照第二部或第三部写法，正常
  
  
  /***/ })
  /******/ ]);
  ```

### 36. Webpack Tree Shaking

Tree-shaking字面意义是“摇树”，伴随着摇树，树上的枯叶就会掉落下来。这里的Tree-shaking【摇掉】的是代码中未引用的部分，这部分代码叫做未引用代码（dead code）。Webpack生产模式优化中就有这样一个有用的功能，它可以检测出代码中未引用的代码，然后移除掉它们。

compontents.js

```js
export const Button = () => {
  return document.createElement('button')

  console.log('dead-code')  // 未引用代码
}
// 未引用代码，index.js中没有导入
export const Link = () => {
  return document.createElement('a')
}  
// 未引用代码，index.js中没有导入
export const Heading = level => {
  return document.createElement('h' + level)
}
```

index.js

```js
import { Button } from './components'

document.body.appendChild(Button())
```

通过**yarn webpack --mode production**打包后发现，console.log('dead code')以及其它两个组件压根没有输出到bundle.js，这是因为Tree-shaking在生产模式下自动开启。

### 37. Webpack 使用Tree Shaking

需要注意的hiTree-shaking并不是webpack中的某一个配置选项，它是一组功能搭配使用过后的使用效果，这种功能会在生产模式下自动启用。但是由于目前官方文档中对Tree-shaking的介绍有点混乱，所以这里再来介绍一下它在其它模式下如何一步一步的手动的开启。顺便通过这个过程，了解Tree-shaking的工作过程以及它的优化功能。

之前在没有启用production工作模式时，生成的bundle.js部分代码如下，其中未引用到的Link及Heading都被输出到bundle.js中。

```js
document.body.appendChild(Object(_components__WEBPACK_IMPORTED_MODULE_0__["Button"])())

/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Button", function() { return Button; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Link", function() { return Link; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Heading", function() { return Heading; });
const Button = () => {
  return document.createElement('button')

  console.log('dead-code')
}

const Link = () => {
  return document.createElement('a')
}

const Heading = level => {
  return document.createElement('h' + level)
}


/***/ }
```

然后在webpack.config.js中添加如下配置**optimization**，该对象集中配置webpack优化功能。

```js
module.exports = {
  mode: 'none',
  entry: './src/index.js',
  output: {
    filename: 'bundle.js'
  },
  optimization: {  // 集中配置webpack优化功能
    // 模块只导出被使用的成员
    usedExports: true,
    // 尽可能合并每一个模块到一个函数中
    concatenateModules: true,
    // 压缩输出结果
    // minimize: true
  }
}
```

随后继续运行yarn webpack打包命令，输出bundle.js部分如下：

```js
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// CONCATENATED MODULE: ./src/components.js
const Button = () => {
  return document.createElement('button')

  console.log('dead-code')
}

const Link = () => {
  return document.createElement('a')
}

const Heading = level => {
  return document.createElement('h' + level)
}

// CONCATENATED MODULE: ./src/index.js


document.body.appendChild(Button())


/***/ }
```

通过对比代码发现，未开启优化时，bundle.js将三个组件全部导入，然后使用**document.body.appendChild(Object(_componentsWEBPACK_IMPORTED_MODULE_0["Button"])())**创建组件。而开启优化后（为方便观察，先关闭minimize），bundle.js直接使用**document.body.appendChild(Button())**创建组件。实际上打开minimize后，在压缩代码中完全找不到Link以及Heading组件。

如果把代码看做【大树】，可以理解为**usedExports**将枯叶标记起来，而minimize负责把【枯叶】摇下来。

其中**concatenateModules**负责尽可能合并每一个模块到一个函数中，未开启时一个模块为一个函数。这个作用又被称之为**Scope Hoisting**（作用域提升），它是webpack3中添加的特性，此时再配合minimize，这样代码体积又会减小很多。

### 38. Webpack Tree Shaking 于Babel

由于早期webpack发展非常快，变化比较多，所有找资料时得到的结果并不一定适用于当前所使用的版本，对于Tree-shaking的资料更是如此。**很多资料中表示如果使用babel-loader就会导致Tree-shaking失效**。这里说明一下，首先需要明确的是Tree-shaking的实现，前提是必须使用ES Module组织代码，也就是说，交给webpack打包的代码必须使用ESM的方式来去实现的模块化。原因是webpack在打包所有模块之前，先将模块根据不同的配置交给不同的loader去处理，最后再将所有loader处理过后的结果打包在一起。为了转换ECMAScript新特性，很多时候会选择babel-loader去处理JavaScript，babel-loader转换代码时**有可能**会将ES Module处理成CommonJS，取决于是否使用转换ES Module的插件。例如之前使用的**"@babel/preset-env"**，其中就有这样一个插件去将ESM转换为CommonJS。这样webpack打包时，拿到的代码就是以commonJS组织的代码，所以说Tree-shaking会失效。

- **实验一：开启bebel-loader，验证Tree-shaking是否会失效**

  webpack.config.js

  ```js
  module.exports = {
    mode: 'none',
    entry: './src/index.js',
    output: {
      filename: 'bundle.js'
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: [
                  "@babel/preset-env"  // 插件集合
              ]
            }
          }
        }
      ]
    },
    optimization: {
      // 模块只导出被使用的成员
      usedExports: true,
      // 尽可能合并每一个模块到一个函数中
      // concatenateModules: true,
      // 压缩输出结果
      // minimize: true
    }
  }
  
  ```

  ```shell
  yarn webpack
  ```

  bundle.js

  ```js
  /***/ (function(module, __webpack_exports__, __webpack_require__) {
  
  "use strict";
  /* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Button; });
  /* unused harmony export Link */
  /* unused harmony export Heading */
  var Button = function Button() {
    return document.createElement('button');
    console.log('dead-code');
  };
  var Link = function Link() {
    return document.createElement('a');
  };
  var Heading = function Heading(level) {
    return document.createElement('h' + level);
  };
  
  /***/ })
  ```

  **结论：当开启bebel-loader时，Tree-shaking正常工作，当使用minimize后，未引用的代码将被删除掉。与上面的描述不符。这是因为最新版本中babel-loader中自动关闭了ES Module转换插件。**

  探索源码：

  node_modules\babel-loader\lib\injectCaller.js部分代码

  ```js
  module.exports = function injectCaller(opts, target) {
    if (!supportsCallerOption()) return opts;
    return Object.assign({}, opts, {
      caller: Object.assign({
        name: "babel-loader",
        // Provide plugins with insight into webpack target.
        // https://github.com/babel/babel-loader/issues/787
        target,
        // Webpack >= 2 supports ESM and dynamic import.
        supportsStaticESM: true,  // 当前环境支持ES Module
        supportsDynamicImport: true,
        // Webpack 5 supports TLA behind a flag. We enable it by default
        // for Babel, and then webpack will throw an error if the experimental
        // flag isn't enabled.
        supportsTopLevelAwait: true
      }, opts.caller)
    });
  };
  ```

  node_modules\@babel\preset-env\lib\index.js部分代码

  ```js
    const modulesPluginNames = getModulesPluginNames({
      modules,
      transformations: _moduleTransformations.default,
      shouldTransformESM: modules !== "auto" || !(api.caller == null ? void 0 : api.caller(supportsStaticESM)),  //禁用ESM的转换
      shouldTransformDynamicImport: modules !== "auto" || !(api.caller == null ? void 0 : api.caller(supportsDynamicImport)),
      shouldTransformExportNamespaceFrom: !shouldSkipExportNamespaceFrom,
      shouldParseTopLevelAwait: !api.caller || api.caller(supportsTopLevelAwait)
    });
  ```

  **所以webpack最终打包时得到的依然是ES Module的代码，所以Tree-shaking还是工作的。**

- **实验二：配置babel-loader，强制开启ES Module转换，验证Tree-shaking是否会失效**

  webpack.config.js

  ```js
  module.exports = {
    mode: 'none',
    entry: './src/index.js',
    output: {
      filename: 'bundle.js'
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: [
                // 如果 Babel 加载模块时已经转换了 ESM，则会导致 Tree Shaking 失效
                ['@babel/preset-env', { modules: 'commonjs' }]  // 强制使用babel esm插件，将代码中的esm转换为CommonJs
                // ['@babel/preset-env', { modules: false }]
                // 也可以使用默认配置，也就是 auto，这样 babel-loader 会自动关闭 ESM 转换
                // ['@babel/preset-env', { modules: 'auto' }]  // 根据环境判断是否开启ES Module插件
              ]
            }
          }
        }
      ]
    },
    optimization: {
      // 模块只导出被使用的成员
      usedExports: true,
      // 尽可能合并每一个模块到一个函数中
      // concatenateModules: true,
      // 压缩输出结果
      // minimize: true
    }
  }
  
  ```

  bundle.js

  ```js
  exports.Heading = exports.Link = exports.Button = void 0;
  
  var Button = function Button() {
    return document.createElement('button');
    console.log('dead-code');
  };
  
  exports.Button = Button;
  
  var Link = function Link() {
    return document.createElement('a');
  };
  
  exports.Link = Link;
  
  var Heading = function Heading(level) {
    return document.createElement('h' + level);
  };
  
  exports.Heading = Heading;
  ```

  发现usedExport未生效，其导出所有成员，包含未引用的成员。开启压缩袋吗Tree-shaking也没办法工作。

  

**总结：**最新版本的bebel-loader并不会导致Tree-shaking失效，如果不确定，最简单的办法是将preset-env中的module改为false，确保preset-env不会开启ES Module转换插件，这样也确保了Tree-shaking工作的前提。另外，上述实验过程也值得琢磨，通过这样会的探索可以了解到很多知其所以然的内容。

```js
['@babel/preset-env', { modules: false }]
```

### 39. Webpack sideEffects及注意

webpack4中还新增了一个**sideEffects**的新特性，它允许通过配置的方式去标识代码是否有副作用，从而为**Tree-shaking**提供更大的压缩空间，副作用是指模块执行的时候，除了导出成员是否还做了一些其它的事情，这个特性一般只有在去开发一个NPM模块时才会用到，但是因为官网当中把**sideEffects**的介绍跟Tree-shaking混到了一起，所以很多人误认为它俩是因果关系，其实它俩真的没有那么大的关系。

这里把sideEffects弄明白，你就能理解为什么了。这里先设计一个能够让sideEffects发挥效果的一个场景:

目录结构：

![image-20210107200147215](https://img-blog.csdnimg.cn/img_convert/aa0b81d92c22b6a6f0d07298ebcbc856.png)



基于刚刚的这个案例基础之上，把components拆分出了多个组件文件（button.js/heading.js/link.js），然后在index.js当中集中导出，便于外界导入。这是一种非常常见的同类文件组织方式。回到入口文件当中去导入components中的组件。

index.js打包入口文件

```js
import { Button } from './components'

// 样式文件属于副作用模块
import './global.css'

// 副作用模块
import './extend'

console.log((8).pad(3))

document.body.appendChild(Button())

```

这样就会出现一个问题，因为在这载入的是components这个目录下的index.js，index.js入口文件中又载入了所有的组件模块，这就会导致只想导入button组件，但是所有的组件模块都会被加载执行。打开命令行终端，然后尝试运行打包，打包完成过后找到打包结果，你会发现所有组件的模块确实都被打包进了bundle.js。

![image-20210107221625383](https://img-blog.csdnimg.cn/img_convert/f38df61f471ae9fcb1123bc94064da13.png)

**sideEffects**特性就可以用来解决此类问题，打开webpack.config.js的配置文件，在optimization属性当中去开启sideEffects属性，注意这个特性在production模式下同样也会自动开启。开启这个特性过后，webpack在打包时就会先检查当前代码，当前项目所属的这个package.json中有没有sideEffects的标识，以此来判断这个模块是否有副作用。如果说这个模块没有副作用，那这些没有用到的模块就不再会打包。可以打开package.json，然后尝试去添加一个sideEffects字段，把它设置false，这样的话就标识当前这个package.json所影响的这个项目，它当中所有的代码都没有副作用，一旦这些没有用的模块它没有副作用了，它就会被移除掉。

![image-20210107222128059](https://img-blog.csdnimg.cn/img_convert/0eeafedda34e073a7ece299a2759b478.png)

![image-20210107222115850](https://img-blog.csdnimg.cn/img_convert/624777152855a823b1e7779a3bec18b7.png)

完了以后再打开命令行终端，然后再次运行打包，打包过后同样找到打包输出的bundle.js，此时那些没有用到的模块就不再会被打包进来了，那这就是的sideEffects作用。注意这里设置了两个地方，先在webpack.config.js的配置当中去开启的sideEffects，它是用来去开启这个功能，而在package.json们添加的sideEffects它是用来标识项目代码是没有副作用的。它俩不是一个意思，不要弄混了

**sideEffects注意事项：**

使用sideEffects这个功能的前提就是确定你的代码没有副作用，否则的话，在webpack打包时就会误删掉那些有副作用的代码，例如这里准备了一个extend.js一个文件，在这个当中并没有向外导出任何成员，它仅仅是在number这个对象的原型上挂载了一个方法，用来为数字去添加前面的倒零，这是一种非常常见的基于原型的扩展方法。

```js
// 为 Number 的原型添加一个扩展方法
Number.prototype.pad = function (size) {
  // 将数字转为字符串 => '8'
  let result = this + ''
  // 在数字前补指定个数的 0 => '008'
  while (result.length < size) {
    result = '0' + result
  }
  return result
}
```

回到index.js当中去导入这个extend.js，但因为这个模块确实没有导出任何成员，所以说这里也就不需要去提取任何成员，只不过在导入这个模块过后就可以使用。它为number所提供的扩展方法了，这里为number做扩展的这样一个操作，就属于extend.js这个模块的副作用，因为在导入的这个模块过后，number的原型上就会多一个方法，这就是副作用。

```js
import { Button } from './components'

// 样式文件属于副作用模块
import './global.css'

// 副作用模块
import './extend'

console.log((8).pad(3))

document.body.appendChild(Button())
```

此时如果说还表示项目当中所有的代码都没有副作用的话，再次回到命令行运行打包，打包过后，找到打包结果，这个时候就会发现刚刚的这个扩展的操作，它是不会被打包进来的，因为它是副作用代码，但是在的配置当中已经声明了没有副作用，所以它们就被移除掉了。除此之外，还有在代码当中载入的css模块，都属于副作用模块，同样会面临刚刚这样一种问题。

解决的办法就是在package.json当中，关掉副作用或者是标识一下当前这个项目当中哪些文件是有副作用的，这样的话webpack就不会去忽略这些有副作用的模块。打开package.json，把false改成一个数组，然后再去添加一下extend.js的路径，还有这个global.css的文件路径，这里也可以使用路径通配符的方式来去配置。

```js
{
  "name": "31-side-effects",
  "version": "0.1.0",
  "main": "index.js",
  "author": "leo ",
  "license": "MIT",
  "scripts": {
    "build": "webpack"
  },
  "devDependencies": {
    "css-loader": "^3.2.0",
    "style-loader": "^1.0.0",
    "webpack": "^4.41.2",
    "webpack-cli": "^3.3.9"
  },
  "sideEffects": [
    "./src/extend.js",
    "*.css"
  ]
}
```

完成以后再次打开命令行终端运行打包，此时在找bundle.js中发现，这个有副作用的两个模块也会被同时打包进来了。以上就是对webpack和内置的一些优化属性的一些介绍，总之，这些特性，它都是为了弥补webpack的早期在设计上的一些遗留问题，这一类的技术的发展确实越来越好。

### 40. Webpack 代码分割

通过webpack实现前端项目整体模块化的优势很明显，但是它同样存在一些弊端，那就是项目当中所有的代码最终都会被打包到一起，试想一下，如果说应用非常复杂，模块非常多的话，那打包结果就会特别的大，很多时候超过两三兆也是非常常见的事情。而事实情况是，大多数时候在应用开始工作时，并不是所有的模块都是必须要加载进来的，但是，这些模块又被全部打包到一起，需要任何一个模块，都必须得把整体加载下来过后才能使用。而应用一般又是运行在浏览器端，这就意味着会浪费掉很多的流量和带宽。

更为合理的方案就是把的打包结果按照一定的规则去分离到多个bundle.js当中，然后根据应用的运行需要，按需加载这些模块，这样的话就可以大大提高应用的响应速度以及它的运行效率。可能有人会想起来在一开始的时候说过webpack就是把项目中散落的那些模块合并到一起，从而去提高运行效率，那这里又在说它应该把它分离开，这两个说法是不是自相矛盾？其实这并不是矛盾，只是物极必反而已，**资源太大了也不行，太碎了更不行**，项目中划分的这种模块的颗粒度一般都会非常的细，很多时候一个模块只是提供了一个小小的工具函数，它并不能形成一个完整的功能单元，如果不把这些散落的模块合并到一起，就有可能再去运行一个小小的功能时，会加载非常多的模块。而目前所主流的这种HTTP1.1协议，它本身就有很多缺陷，例如并不能同时对同一个域名下发起很多次的并行请求，而且每一次请求都会有一定的延迟，另外每次请求除了传输具体的内容以外，还会有额外的header请求头和响应头，当大量的这种请求的情况下，这些请求头加在一起，也是很大的浪费。

综上所述，模块打包肯定是有必要的，不过像应用越来越大过后，要开始慢慢的学会变通。为了解决这样的问题，**webpack支持一种分包的功能，也可以把这种功能称之为代码分割，它通过把模块，按照所设计的一个规则打包到不同的bundle.js当中，从而去提高应用的响应速度，目前的webpack去实现分包的方式主要有两种：**

- 第一种就是根据业务去配置不同的打包入口，也就是会有同时多个打包入口同时打包，这时候就会输出多个打包结果；

- 第二种就是采用ES Module的动态导入的功能，去实现模块的按需加载，这个时候webpack会自动的把动态导入的这个模块单独输出的一个bundle.js当中。

### 41. Webpack 多入口打包

多入口打包一般适用于传统的“多页”应用程序。最常见的划分规则是一个页面对应一个打包入口，对于不同页面之间公共的部分再去提取到公共的结果中。

目录结构

![未命名截图.png](https://img-blog.csdnimg.cn/img_convert/32a65a4d0d0865cca9ec1a4e1c9beb41.png)

一般webpack.config.js配置文件中的entry属性只会一个文件路径（打包入口），如果需要配置多个打包入口，则需要将entry属性定义成为一个对象（注**意不是数组，如果是数组的话，那就是将多个文件打包到一起，对于整个应用来讲依然是一个入口**）。一旦配置为多入口，输出的文件名也需要修改**"[name].bundle.js**"，[name]最终会被替换成入口的名称，也就是index和album。

```js
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  mode: 'none',
  entry: {
    index: './src/index.js',  // 多入口
    album: './src/album.js'
  },
  output: {
    filename: '[name].bundle.js'  // [name]占位符，最终被替换为入口名称index和album
  },
  optimization: {
    splitChunks: {
      // 自动提取所有公共模块到单独 bundle
      chunks: 'all'
    }
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/index.html',
      filename: 'index.html',
    }),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/album.html',
      filename: 'album.html',
    })
  ]
}
```

命令行运行yarn webpack命令，打开dist目录发现已经有两个js文件。打开html文件，发现两个html文件都引入了两个js文件，但需求是各自引入各自的js/css文件，所以这里需要进一步处理，在html-webpack-plugin插件中增加chunks属性，其值为对应需要引入的js文件入口名称。

![image-20210108114050868.png](https://img-blog.csdnimg.cn/img_convert/96984279cf6c0fddf49f3cc88a6003e4.png)

```js
...  
plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/index.html',
      filename: 'index.html',
      chunks: ['index']
    }),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/album.html',
      filename: 'album.html',
      chunks: ['album']
    })
  ]
```

### 42. Webpack 提取公共模块

多入口打包本身非常容易理解，也非常容易使用，但是它也存在一个小小的问题，就是在不同的打包入口当中，它一定会有那么一些公共的部分，按照目前这种多入口的打包方式，不同的打包结果当中就会出现相同的模块，例如在我们这里index入口和album入口当中就共同使用了global.css和fetch.js这两个公共的模块，因为实例比较简单，所以说重复的影响不会有那么大，但是如果共同使用的是jQuery或者Vue这种体积比较大的模块，那影响的话就会特别的大，所以说需要把这些公共的模块去。提取到一个单独的bundle.js当中，webpack中实现公共模块提取的方式也非常简单，只需要在优化配置当中去开启一个叫splitChunks的一个功能就可以了，回到配置文件当中，配置如下：

```js
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  mode: 'none',
  entry: {
    index: './src/index.js',
    album: './src/album.js'
  },
  output: {
    filename: '[name].bundle.js'
  },
  optimization: {
    splitChunks: {
      // 自动提取所有公共模块到单独 bundle
      chunks: 'all'  // 表示会把所有的公共模块都提取到单独的bundle.js当中
    }
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/index.html',
      filename: 'index.html',
      chunks: ['index']
    }),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/album.html',
      filename: 'album.html',
      chunks: ['album']
    })
  ]
}
```

打开命令行运行yarn webpack后发现，公共模块的部分被打包进album~index.bundle.js中去了。

### 43. Webpack 动态导入

按需加载是开发浏览器应用当中一个非常常见的需求，一般常说的按需加载指的是加载数据，这里所说的按需加载指的是在应用运行过程中需要某个模块时才去加载这个模块，这种方式可以极大的节省**带宽和流量**。webpack支持使用动态导入的这种方式来去实现模块的按需加载，而且所有动态导入的模块都会被自动提取到单独的bundle.js当中，从而实现分包，相比于**多入口**的方式，动态导入更为灵活，因为通过代码的逻辑去控制，需不需要加载某个模块，或者是时候加的某个模块。而分包的目的中就有很重要的一点就是：让模块实现按需加载，从而去提高应用的响应速度。

具体来看如何使用，这里已经提前设计好了一个可以发挥按需加载作用的场景，在这个页面的主体区域，如果访问的是文章页的话，得到的就是一个文章列表，如果访问的是相册页，显示的就是相册列表。

项目目录：

![image-20210109231933249](https://img-blog.csdnimg.cn/img_convert/4755b55464648db87ad131732d46051c.png)

动态导入使用的就是ESM标准当中的动态导入，在需要动态导入组件的地方，通过这个函数导入指定的路径，这个方法返回的就是一个promise，promise的方法当中就可以拿到模块对象，由于网站是使用的默认导出，所以说这里需要去解构模块对象当中的default，然后把它放到post的这个变量当中，拿到这个成员过后，使用mainElement.appendChild(posts())创建页面元素，album组件也是如此。完成以后再次回到浏览器，此时页面仍然可以正常工作的。

```js
// import posts from './posts/posts'
// import album from './album/album'

const render = () => {
  const hash = window.location.hash || '#posts'
  console.log(hash)
  const mainElement = document.querySelector('.main')

  mainElement.innerHTML = ''

  if (hash === '#posts') {
    // mainElement.appendChild(posts())
    // 这个方法返回的就是一个promise，promise的方法当中就可以拿到模块对象，由于网站是使用的默认导出，所以说这里需要去解构模块对象当中的default，然后把它放到post的这个变量当中
    import('./posts/posts').then(({ default: posts }) => {
      mainElement.appendChild(posts())
    })
  } else if (hash === '#album') {
    // mainElement.appendChild(album())
    import('./album/album').then(({ default: album }) => {
      mainElement.appendChild(album())
    })
  }
}

render()

window.addEventListener('hashchange', render)
```

这时再回到开发工具当中，然后重新去运行打包，然后去看看此时打包的结果是什么样子的，打包结束，打开dist目录，此时dist目录下就会多出3个js文件，那这三个js文件，实际上就是由动态导入自动分包所产生的。这3个文件的分别是刚刚导入的两个模块index.js/album.js，以及这两个模块当中公共模块fetch.js。

![image-20210109232950282](https://img-blog.csdnimg.cn/img_convert/56ecd812f6f1324681f75e2bb35833d5.png)

动态导入整个过程无需配置任何一个地方，只需要按照ESM动态导入成员的方式去导入模块就可以，内部会自动处理分包和按需加载，如果说你使用的是单页应用开发框架，比如react或者Vue的话，在你项目当中的路由映射组件，就可以通过这种动态导入的方式实现**按需加载**。

### 44. Webpack 魔法注释

默认通过动态导入产生的bundle.js文件，它的名称只是一个序号，但这并没有什么不好的，因为在生产环境当中，大多数时候是根本不用关心资源文件的名称是什么，但是如果说还是需要给这些bundle.js命名的话，可以使用webpack所特有的**魔法注释**是来去实现。

```js
// import posts from './posts/posts'
// import album from './album/album'

const render = () => {
  const hash = window.location.hash || '#posts'
  console.log(hash)
  const mainElement = document.querySelector('.main')

  mainElement.innerHTML = ''

  if (hash === '#posts') {
    // mainElement.appendChild(posts())
    // /* webpackChunkName: 'components' */'魔法注释，特定格式
    import(/* webpackChunkName: 'posts' */'./posts/posts').then(({ default: posts }) => {
      mainElement.appendChild(posts())
    })
  } else if (hash === '#album') {
    // mainElement.appendChild(album())
    import(/* webpackChunkName: 'album' */'./album/album').then(({ default: album }) => {
      mainElement.appendChild(album())
    })
  }
}

render()

window.addEventListener('hashchange', render)
```

特定格式：**webpackChunkName:'components'**，这样就可以给分包所产生的帮的起上名字了，再次打开命令行终端运行webpack打包，此时生成的bundle.js文件它的name会使用刚刚注释当中所提供的名称了。

![image-20210109233747793](https://img-blog.csdnimg.cn/img_convert/ea7f7453fddc009a91d1c9a31aa796f9.png)

如果webpackChunkName是相同的，最终就会被打包到一起，例如这里可以把这两个webpackChunkName设置为components，然后再次运行打包，此时，这两个模块它都会被打包进components.bundle.js文件，借助于这样一个特点，就可以根据自己的实际情况，灵活组织动态加载的模块所输出的文件了。

![image-20210109234606676](https://img-blog.csdnimg.cn/img_convert/10dbccf6c871b4efcb1eec9689b04a4b.png)

### 45. Webpack MiniCssExtractPlugin

MiniCssExtractPlugin是一个可以**将css代码从打包结果当中提取出来**的插件，通过这个插件就可以实现css模块的按需加载。它的使用也非常简单，回到项目当中，先执行**yarn add mini-css-extract-plugin**，打开webpack的配置文件，首先需要先导入这个插件的模块，导入过后就可以将这个插件添加到配置对象的plugins数组当中。这样的话，它在工作时就会自动提取代码当中的css到一个单独的文件当中。除此以外，目前所使用的样式模块，它是先交给css-loader去解析，然后交给style-loader的去处理，它的作用就是将样式代码通过**style**标签的方式注入到页面当中，从而使样式可以工作。MiniCssExtractPlugin的话，样式就会单独存放到文件当中，也就不需要加style标签，而是直接通过link的方式去引入。所以这里就不再需要style-loader，取而代之使用的是MiniCssExtractPlugin所提供的一个**MiniCssExtractPlugin.loader**，来实现样式文件，通过link标签的方式去引入。

webpack.config.js

```js
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')
const TerserWebpackPlugin = require('terser-webpack-plugin')

module.exports = {
  mode: 'none',
  entry: {
    main: './src/index.js'
  },
  output: {
    filename: '[name].bundle.js'
  },
  optimization: {
    minimizer: [
      new TerserWebpackPlugin(),
      new OptimizeCssAssetsWebpackPlugin()
    ]
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          // 'style-loader', // 将样式通过 style 标签注入
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Dynamic import',
      template: './src/index.html',
      filename: 'index.html'
    }),
    new MiniCssExtractPlugin()
  ]
}
```

完成以后回到命令行终端，再次运行webpack打包过后，就可以在目录当中看到提取出来的文件了，不过这里需要注意一点，如果说样式文件体积不是很大的话，提取到单个文件当中，效果可能适得其反。个人的经验是：如果css超过了**150KB**左右，才需要考虑是否将它提取到单独文件当中，否则的话其实css嵌入到代码当中，它减少一次请求效果可能会更好。

### 46. Webpack OptimizeCssAssetsWebpackPlugin

使用了MiniCssExtractPlugin过后，样式文件就可以被提取到单独的css文件当中了，但是这里同样有一个小问题，回到命令行，尝试以生产模式去运行打包（**yarn webpack --mode production**），照之前的了解，在生产模式下webpack会自动去**压缩输出**的结果，这里打开输出的样式文件，发现样式文件根本没有任何的变化，这是因为webpack内置的压缩插件仅仅针对于js文件的压缩，对于其它的资源文件压缩都需要额外的插件来去支持。

webpack官方推荐了一个**OptimizeCssAssetsWebpackPlugin插件**，可以使用这个插件来去压缩样式文件。首先安装一下这个插件，**yarn add optimize-css-assets-webpack-plugin**，安装完成后回到配置文件当中，先导入这个插件，完成过后去把这个插件添加到配置对象的plugins当中，此时再次回到命令行终端，重新运行打包，这次打包完成过后，样式文件就可以以压缩文件的格式去输出了。

不过这里还有一个额外的小问题，可能大家在官方文档当中会发现，文档当中这个插件它并不是配置在plugins数组当中的，而是添加到了optimization属性当中的minimizer属性当中，这是为什么，其实也非常简单。如果说把这个插件配置到plugin数组当中，这个插件它在任何情况下都会正常工作，而配置到minimizer当中的话，那只会在minimizer特性开启时才会工作，所以说webpack的建议，像这种**压缩类**的插件，应该配置到minimizer数组当中，以便于可以通过这个选项去统一控制。这里尝试把这个插件移植到的optimization属性的数组当中，然后再次运行打包，此时如果说没有开启压缩这个功能的话，这个插件就不会工作，反之如果说以生产模式打包，minimizer的属性就会自动开启，这个压缩插件就会自动工作，样式文件也就会被压缩。但是这么配置也有一个小小的缺点，可以来看一眼输出的js文件，这时候发现原本可以自动压缩的js，这次却不能自动压缩了，这是因为设置了minimizer这个数组，webpack就认为如果配置了这个数组，就是要去自定义所使用的压缩器插件，内部的js压缩器就会被覆盖掉，所以这里需要手动再去把它添加回来，内置的js压缩插件叫做**terser-webpack-plugin**，回到命令行，然后来手动安装一下这个模块，安装完成过后这里再来把这个插件手动的去添加到这个数组当中，这样的话，如果再以生产模式运行打包，js文件、css文件都可以正常被压缩了，如果说以普通模式打包也就是不开启压缩（minimizer）的话，它也就不会以压缩的形式输出了。

```js
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')  // css压缩插件
const TerserWebpackPlugin = require('terser-webpack-plugin')  // webpack内置的js压缩插件

module.exports = {
  mode: 'none',
  entry: {
    main: './src/index.js'
  },
  output: {
    filename: '[name].bundle.js'
  },
  optimization: {
    minimizer: [
      new TerserWebpackPlugin(),
      new OptimizeCssAssetsWebpackPlugin()
    ]
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          // 'style-loader', // 将样式通过 style 标签注入
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Dynamic import',
      template: './src/index.html',
      filename: 'index.html'
    }),
    new MiniCssExtractPlugin()
  ]
}
```

### 47. Webpack 输出文件名 Hash

一般部署前端的资源文件时，都会启用服务器的静态资源缓存，这样的话对于用户的浏览器而言，就可以缓存住应用当中的静态资源，后续就不再需要请求服务器得到这些文件，整体应用的响应速度就有一个大幅度的提升。不过开启静态资源的客户端缓存，也会有一些小小的问题，如果说在缓存策略当中的缓存失效时间设置的过短的，效果就不是特别明显，如果说把过期时间设置的比较长，一旦在这个过程当中应用发生了更新，重新部署过后，又没有办法及时更新到客户端。

为了解决这个问题，建议在生产模式下需要给输出的文件名当中加哈希值，这样的话一旦的资源文件发生改变，文件名称也可以跟着一起去变化，对于客户端而言，全新的文件名就是全新的请求，也就没有缓存的问题，这样的话就可以把服务端的缓存策略当中的时间设置得非常长，也就不用担心文件更新过后的问题。

webpack中的filename属性和绝大多数插件中的filename的属性，都支持通过占位符的方式来去为文件名设置hash，不过它们支持三种hash，效果各不相同。

- hash

  ```js
  const { CleanWebpackPlugin } = require('clean-webpack-plugin')
  const HtmlWebpackPlugin = require('html-webpack-plugin')
  const MiniCssExtractPlugin = require('mini-css-extract-plugin')
  const OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')
  const TerserWebpackPlugin = require('terser-webpack-plugin')
  
  module.exports = {
    mode: 'none',
    entry: {
      main: './src/index.js'
    },
    output: {
      // 这个hash是整个项目级别的，也就是说一旦项目当中有任何一个地方发生改动，这一次打包过程当中的哈希值全部都会发生变化。
      filename: '[name]-[hash].bundle.js'  // 最普通的hash，项目级别
    },
    optimization: {
      minimizer: [
        new TerserWebpackPlugin(),
        new OptimizeCssAssetsWebpackPlugin()
      ]
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            // 'style-loader', // 将样式通过 style 标签注入
            MiniCssExtractPlugin.loader,
            'css-loader'
          ]
        }
      ]
    },
    plugins: [
      new CleanWebpackPlugin(),
      new HtmlWebpackPlugin({
        title: 'Dynamic import',
        template: './src/index.html',
        filename: 'index.html'
      }),
      new MiniCssExtractPlugin({
        filename: '[name]-[hash].bundle.css'
      })
    ]
  }
  
  ```

  ![image-20210110004938544](https://img-blog.csdnimg.cn/img_convert/ed08f90eef13f5676bda2e72e8f21d99.png)

- chunkhash

  ```js
  const { CleanWebpackPlugin } = require('clean-webpack-plugin')
  const HtmlWebpackPlugin = require('html-webpack-plugin')
  const MiniCssExtractPlugin = require('mini-css-extract-plugin')
  const OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')
  const TerserWebpackPlugin = require('terser-webpack-plugin')
  
  module.exports = {
    mode: 'none',
    entry: {
      main: './src/index.js'
    },
    output: {
      // 这个哈希chunk级别的，也就是在打包过程当中，只要是同一路的打包，chunkhash都是相同的，一个打包入口算一路
      filename: '[name]-[chunkhash].bundle.js'
    },
    optimization: {
      minimizer: [
        new TerserWebpackPlugin(),
        new OptimizeCssAssetsWebpackPlugin()
      ]
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            // 'style-loader', // 将样式通过 style 标签注入
            MiniCssExtractPlugin.loader,
            'css-loader'
          ]
        }
      ]
    },
    plugins: [
      new CleanWebpackPlugin(),
      new HtmlWebpackPlugin({
        title: 'Dynamic import',
        template: './src/index.html',
        filename: 'index.html'
      }),
      new MiniCssExtractPlugin({
        filename: '[name]-[chunkhash].bundle.css'
      })
    ]
  }
  
  ```

- contenthash

  ```js
  const { CleanWebpackPlugin } = require('clean-webpack-plugin')
  const HtmlWebpackPlugin = require('html-webpack-plugin')
  const MiniCssExtractPlugin = require('mini-css-extract-plugin')
  const OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')
  const TerserWebpackPlugin = require('terser-webpack-plugin')
  
  module.exports = {
    mode: 'none',
    entry: {
      main: './src/index.js'
    },
    output: {
      // 它实际上是文件级别的hash，是根据输出文件的内容生成的哈希值，也就是说只要是不同的文件，它就有不同的哈希值
      filename: '[name]-[contenthash].bundle.js'
    },
    optimization: {
      minimizer: [
        new TerserWebpackPlugin(),
        new OptimizeCssAssetsWebpackPlugin()
      ]
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            // 'style-loader', // 将样式通过 style 标签注入
            MiniCssExtractPlugin.loader,
            'css-loader'
          ]
        }
      ]
    },
    plugins: [
      new CleanWebpackPlugin(),
      new HtmlWebpackPlugin({
        title: 'Dynamic import',
        template: './src/index.html',
        filename: 'index.html'
      }),
      new MiniCssExtractPlugin({
        filename: '[name]-[contenthash].bundle.css'
      })
    ]
  }
  
  ```

相比于hash和chunkhash，contenthash它应该算是解决缓存问题最好的方式，因为它精确的定位到了文件级别的hash，只有当这个文件发生了变化，才有可能去更新文件名，这个实际上是最适合去解决缓存问题的。另外，如果觉得这个20位长度的hash太长的话，webpack还允许指定hash的长度，可以在占位符里面通过":8"来去指定hash的长度，个人觉得如果说是控制缓存的话，八位的contenthash应该是最好的选择了。

```js
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')
const TerserWebpackPlugin = require('terser-webpack-plugin')

module.exports = {
  mode: 'none',
  entry: {
    main: './src/index.js'
  },
  output: {
    filename: '[name]-[contenthash:8].bundle.js'  // 控制缓存最好的选择
  },
  optimization: {
    minimizer: [
      new TerserWebpackPlugin(),
      new OptimizeCssAssetsWebpackPlugin()
    ]
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          // 'style-loader', // 将样式通过 style 标签注入
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Dynamic import',
      template: './src/index.html',
      filename: 'index.html'
    }),
    new MiniCssExtractPlugin({
      filename: '[name]-[contenthash:8].bundle.css'  // 控制缓存最好的选择
    })
  ]
}

```

