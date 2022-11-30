---
title: Vite实现原理
author: 5coder
tags: Vite
category: 大前端
abbrlink: 35306
date: 2022-11-30 16:14:55
password:
keywords:
top:
cover:
---

# Vite实现原理

## 1.Vite

接下来再来回顾一下Vite，之前已经演示过Vite的基本使用，这里的重点是来了解Vite的核心实现原理。先来回顾一下Vite的概念，**Vite是一个面向现代浏览器的一个更轻、更快的web应用开发工具，它基于`ECMAScript`标准的原生模块系统`ES Module`来实现的。**

它的出现是为了解决外`webpack`在开发阶段使用`webpack-dev-server`冷启动时间过长，另外`webpack-HMR`热更新反应速度慢的问题。使用Vite创建的项目就是一个普通的Vue3的应用，没有太多特殊的地方，相比基于Vue cli创建的项目也少了很多的配置文件和依赖。

Vite创建的项目开发依赖非常的简单，只有`vite`和@`vue/compiler-sfc`。Vite就是接下来要模拟实现的命令航工具，`vue/compiler-sfc`就是用来编译项目中的`.vue`结尾的单文件组件，vue2中使用的是`vue/template-compiler`。这里需要注意的是，Vite目前只支持Vue3.0的版本，在创建项目的时候通过指定使用不同的模板，也可以支持其他的框架。

Vite项目中提供了两个子命令，`vite serve`和`vite build`。`vite serve`开启一个用于开发的web服务器，在启动服务器的时候不需要编译所有的代码文件，启动速度非常的快。

![](http://5coder.cn/img/1669797562_6fdf1c95663663a09de25d918c517f25.png)

在运行`vite serve`的时候，不需要打包，直接开启一个web服务器，当浏览器请求服务器，比如请求一个单文件组件，这个时候在服务器端编译单文件组件，然后把编译的结果返回给浏览器。注意，这里的编译是在**服务器端**，另外模块的处理是在请求到服务器端处理的。

![](http://5coder.cn/img/1669797660_d22a81bdc26a08631ae31f7066bbd82a.png)

再来回顾一下`vue-cli`创建的应用，它在启动开发的web服务器的时候使用的是`vue-cli-service-serve`，当运行`vue-cli-service-serve`的时候，它内部会使用`webpack`首先去打包所有的模块。如果模块比较多的话，打包速度会非常的慢，把打包的结果存储到内存中，然后才会开启开发的外部服务器浏览器，请求外部服务器把内存中打包的结果直接返回给浏览器。

`webpack`这类工具，它的做法是将所有的模块提前编译打包进`bundle`里。换句话说，不管模块是否被执行，是否使用到，都要被编译和打包到`bundle`里。随着项目越来越大，打包后的帮也越来越大，打包的速度自然也就越来越慢。

Vite利用现代浏览器原生支持的`ES Module`模块化的特性，省略了对模块的打包，对于需要编译的文件，比如单文件、组件、样式模块等为采用的另一种模式，**即时编译**。也就是说只有具体去请求某个文件的时候，才会在服务端编译这个文件。所以这种即时编译的好处主要体现在按需编译速度会更快。

Vite默认也支持HMR模块热更新，相对于`webpack`中的`HMR`，性能更好，因为Vite只需要立即编译当前所修改的文件即可，所以响应速度非常快。而`webpack`修改某个文件过后会自动以这个文件为入口重新`build`一次，所有涉及到的依赖也会被重新加载一次，所以反应速度稍微会慢一些。

- Vite HMR
  - 立即编译当前所修改的文件
- Webpack HMR
  - 会自动以这个文件为入口重写build一次，所有的涉及到的依赖也都会被加载一遍

Vite在生产模式下打包需要使用`vite build`的命令，这个命令内部采用的是`rollup`进行打包，最终还是会把文件都提前编译并打包到一起。对于代码切割的需求，vite它内部采用的是原生的动态导入的特性实现的，所以**打包结果还是只能够支持现代浏览器**，不过动态导入特性是有相应的`Polyfill`的。

那随着Vite的出现，引发了另外一个值得思考的问题，究竟有没有必要去打包应用呢？之前使用`webpack`进行打包，会把所有的模块打包到一个`bundle.js`中，主要有两个原因，第一是浏览器环境并不支持模块化，第二是零散的模块文件会产生大量的`http`请求。

先来看第一个问题，浏览器环境并不支持模块化。随着现在浏览器对`ES Module`标准支持的逐渐完善，第一个问题已经慢慢不存在了，现阶段绝大多数浏览器都是支持`ES Module`特性的。

再来看第二个问题，之前打包还有一个目的，就是当JS文件比较多的时候，每个JS文件都要发送一次请求，每个请求都要创建一个连接，那为了减少请求服务器的次数，所以打包成一个文件。这个问题HTTP已经帮我们解决，它可以复用链接。

下面看一下浏览器对`ES Module`的支持情况。

![](http://5coder.cn/img/1669800466_96b54ab7be9945dae0ca0e7ccce45438.png)

Vite创建的项目几乎不需要额外的配置，默认就支持`TypeScript`以及`CSS`的预编译器，但是需要单独安装对应的编译器以及支持JSX和`Web Assembly`。其他的future你可以打开官网来查看。

> Vite带来的优势主要体现在提升开发者在开发过程中的体验。外部开发服务器不需要等待，可以立即启动。另外模块热更新几乎是实时的，所需的文件是按需编译，避免编译用不到的文件，还有开箱即用，避免各种`loader`以及`plugin`的配置。
>

## 2.Vite 实现原理-静态Web服务器

接下来通过实现一个自己的Vite工具来深入了解Vite的工作原理。先来回顾一下Vite的核心功能。Vite的核心功能包括开启一个静态的web服务器，并且能够编译单文件组件，而且提供`HMR`的功能。

当启动Vite的时候，首先会将当前项目目录作为静态文件服务器的根目录。静态文件服务器会拦截部分请求，例如当请求单文件组件的时候，会实施编译以及处理其他浏览器不能识别的模块。通过`webSocket`实现`HMR`，这个功能会跳过。下面首先来实现一个能够开启静态web服务器的命令行工具。Vite内部使用的是`koa`来开启静态web服务器。

项目目录：

![](http://5coder.cn/img/1669801692_b5b2525988a5f23cd9c8a57d469f2829.png)

`index.js`

```js
#!/usr/bin/env node
const Koa = require('koa')
const send = require("koa-send")

const app = new Koa()

// 1.静态文件服务器
app.use(async (ctx, next) => {
  await send(ctx, ctx.path, { root: process.cwd(), index: 'index.html' })
  await next()
})

app.listen(3000)
console.log('Server 3000')
```

要基于`koa`来开发一个静态的we部服务器，所以`index.js`这里先来导入所需要的两个模块，`koa`和`koa-send`。然后再来创建一个`koa`的实例，接下来使用`koa`开发静态web服务器，默认返回根目录中的`index.html`。

先来创建一个中间键，它负责去处理静态文件，默认加载当前目录下，也就是运行该命令行工具目录中的`index.html`。

接下来直接调用`send`，把`index.html`面返回给浏览器，当然返回的是当前目录，也就是运行该命令行工具的这个目录下的`index.html`。直接调用`send`的函数，第一个参数是`ctx`上下文，第二个参数是`ctx.path`当前请求的路径。第三个参数要去配置根目录，当前web服务器的根目录是`root: process.cwd()`，接着要设置默认的页面index，默认的页面就是`index.html`。返回静态页面就写完了，因为是中间键，所以还要调用一下`next`。

接下来需要去监听端口`3000`。

到这里静态服务器就暂时写完了来测试一下，测试之前我们先来`npm link`一下，它会把当前这个项目链接到`npm`这个安装目录里边来，下面打开一个基于Vue3开发的项目，然后在终端里边只需要输入`my-vite-cli`，也就是开发的这个命令行工具。

![](http://5coder.cn/img/1669801422_9e9b557af1f9c90c08e1749371e19ad6.png)

因为还没处理完，页面上什么都没看到。打开`console`控制台，这里有个错误，它告诉我们解析vue模块的时候失败了。我们使用`import`导入模块的时候，这里要求使用相对路径。

![](http://5coder.cn/img/1669802248_700608cfca48d7d107ba93f1d08c490a.png)

再切换到`network`，刷新一下来看`main.js`，这次请求这里导入了`vue`，但导入`vue`的时候，它后边的路径没有`/、./、../`，所以浏览器不识别，我们希望他去`node_modules`文件夹去加载`vue`，这是打包工具的默认行为，但是浏览器不支持。想要解决这个问题的话，来看一下`Vite`中是如何处理的。

![](http://5coder.cn/img/1669801378_22b64993e507b6dee6fd84f74a442337.png)

当浏览器从Vite开启的外部服务器加载`main.js`的时候，首先会去处理加载第三方模块的路径，所以在服务器端要手动来处理这个路径的问题。当请求一个模块的时候，比如当前请求的`main.js`这个模块，要把该模块中加载第三方模块的`import`中的路径做一个处理，让它加载一个不存在的路径，这里的`/@modules/vue.js`。

再来看一下这次请求的`headers`，在响应头中可以找到`contentType`，它的值是`application/javascript`，它的作用是告诉浏览器返还的文件是一个`JavaScript`文件。所以一会可以在web服务器输出之前先判断一下当前返回的文件是否是`js`文件，如果是的话，再来处理里边的第三方模块的路径，然后再去请求`/@modules/vue.js`的时候，这个路径在服务器上是根本不存在的，没有`@modules`文件夹，需要在服务器上要去处理这个请求，去`node_modules`去加载的`vue`模块。

好，这是我们的思路，那到这里我们加载`index.html`的静态服务器其实就搞定了，稍后再来处理加载第三方模块的问题。

## 3.Vite 实现原理-修改第三方模块的路径

接下来处理请求第三方模块的问题，需要来创建两个中间键，一个中间键是把加载第三方模块的`import`中的路径改变，改成加载`/@modules/模块的名称`。另一个中间件，当请求过来之后，判断请求路径中是否有`/@modules/模块的名称`，如果有的话，取`node_modules`目录中加载对应的模块。下面实现第一个中间键，**修改第三方模块的路径**。

```js
#!/usr/bin/env node
const Koa = require('koa')
const send = require("koa-send")

const app = new Koa()

const streamToString = stream => new Promise((resolve, reject) => {
  const chunks = []
  stream.on('data', chunk => chunks.push(chunk))
  stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')))
  stream.on('error', reject)
})

// 1.静态文件服务器
app.use(async (ctx, next) => {
  await send(ctx, ctx.path, { root: process.cwd(), index: 'index.html' })
  await next()
})

// 2.修改第三方模块的路径
app.use(async (ctx, next) => {
  if (ctx.type === 'application/javascript') {
    const contents = await streamToString(ctx.body)
    // import vue from 'vue
    // import App from './App.vue
    // 这里需要将【from '】替换成【from '@modules】
    ctx.body = contents.replace(/(from\s+['"])(?!\.\/)/g, '$1/@modules/')
  }
})

app.listen(3000)
console.log('Server 3000')
```

第一个中间件中加载了静态文件，当把静态文件返回给浏览器之前，要判断一下当前返回的文件是否是`javascript`模块，如果是的话，来修改第三方模块的路径，修改成`/@modules/模块的名称`。

在把文件返回给浏览器之前，需要判断一下当前返回给浏览器的文件是否是`javascript`，在这里只需要判断响应头中的contentType是否为`application/javascript`，如果是，那需要找到这个文件中的内容，然后处理`import`中的路径。

`ctx.body`就是要返回给浏览器的`js`文件。注意`ctx.body`是一个流，要修改字符串中的路径，所以需要把**流转换成字符串**。这件事情其他位置还有用，所以在最上面来定一个函数`streamToString`，这个函数的作用是把流转换成字符串。

```js
const streamToString = stream => new Promise((resolve, reject) => {
  const chunks = []
  stream.on('data', chunk => chunks.push(chunk))
  stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')))
  stream.on('error', reject)
})
```

因为读取流是一个异步的过程，所以这里要返回一个`promise`对象。在这个函数里，首先要定一个`chunks`数组，它存储一会读取到的`buffer`，然后来注册`stream`的`data`事件，去监听读取到的`buffer`，把读取到的`buffer`存储到`chunks`数组中。当数据读取完毕之后，把获取到的结果传递给`resolve`。这里先要把数组中的`buffer`合并，然后再转换成字符串。把以上流程注册到`end`事件中。最后如果出错的话，调用`reject`，再注册出错的事件`error`，这个时候直接执行reject。

```js
// 2.修改第三方模块的路径
app.use(async (ctx, next) => {
  if (ctx.type === 'application/javascript') {
    const contents = await streamToString(ctx.body)
    // import vue from 'vue'
    // import App from './App.vue
    // 这里需要将【from '】替换成【from '@modules】
    ctx.body = contents.replace(/(from\s+['"])(?!\.\/)/g, '$1/@modules/')
  }
})
```

现在可以把`ctx.body`转换成字符串，来接收一下它的返回结果`const contents = await streamToString(ctx.body)`。接下来把`contents`中加载第三方模块的路径修改一下，然后把结果重新赋值给`ctx.body`输出。这里需要通过**正则表达式**把第三方模块匹配出来，然后替换成`/@modules/模块的名称`。

下面打开浏览器来测试一下，打开浏览器之前我们还需要重启一下服务器，因为这里代码修改了。

先来看一下`main.js`请求，找到`response`来看这次请求的结果，注意这里的`vue`的路径已经被修改了，修改成了`/@modules/vue`，这个路径是不存在的。下一个请求是`/@modules/vue`这个文件，而现在返回的是`404`，这个路径根本是不存在的，所以获取不到文件。所以在静态的web服务器中，当请求过来之后，还要首先去判断一下当前请求的路径中是否以`/@modules/`开头，如果是的话就去`node_module`找对应的模块，下面实现这个功能。

![](http://5coder.cn/img/1669811866_4a24cedb94cfb25805bd9b1571e5d315.png)

## 4.Vite 实现原理-加载第三方模块

上一小节中创建了一个中间件，负责把加载的第三方模块的路径修改成`/@modules/`的形式。现在再来创建一个中间键，当请求过来以后，判断请求的路径是否以`/@modules/`开头，如果是的话，去`node_modules`目录中加载对应的模块。

接下来在处理静态文件**之前**再来创建一个中间键。注意这里是在处理静态文件之前。这里要做的事情是当请求的路径是以`/@modules/`开头的话，把请求的路径修改成`node_modules`中对应的文件路径，然后继续交给处理静态文件的中间件去处理，所以这个中间界应该写在第一个位置。

```js
#!/usr/bin/env node
const path = require('path')
const Koa = require('koa')
const send = require("koa-send")

const app = new Koa()

const streamToString = stream => new Promise((resolve, reject) => {
  const chunks = []
  stream.on('data', chunk => chunks.push(chunk))
  stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')))
  stream.on('error', reject)
})

// 3. 加载第三方模块
app.use(async (ctx, next) => {
  // ctx.path --> /@modules/vue
  if (ctx.path.startsWith('/@modules/')) {
    const moduleName = ctx.path.substr(10)
    const pkgPath = path.join(process.cwd(), 'node_modules', moduleName, 'package.json')
    const pkg = require(pkgPath)
    ctx.path = path.join('/node_modules', moduleName, pkg.module)
  }
  await next()
})

// 1.静态文件服务器
app.use(async (ctx, next) => {
  await send(ctx, ctx.path, { root: process.cwd(), index: 'index.html' })
  await next()
})

// 2.修改第三方模块的路径
app.use(async (ctx, next) => {
  if (ctx.type === 'application/javascript') {
    const contents = await streamToString(ctx.body)
    // import vue from 'vue
    // import App from './App.vue
    // 这里需要将【from '】替换成【from '@modules】
    ctx.body = contents.replace(/(from\s+['"])(?!\.\/)/g, '$1/@modules/')
  }
})

app.listen(3000)
console.log('Server 3000')
```

在这个函数里首先要获取当前的路径，使用的是`ctx.path`，当前希望处理的路径是这个样子的`ctx.path --> /@modules/vue`。所以先来判断一下`ctx.path`属性是否是以`/@modules/`开头的，如果是的话，那再从这个路径中截取模块的名字`vue`。注意这里的`/@modules/`总共是10个字符，以直接来截取。

拿到模块的名称之后，要获取这个模块的入口文件，这里要获取的是`ES Module`模块的入口文件。需要先找到这个模块的`package.json`，然后再获取`package.json`的`module`字段的值，也就是`ES Module`模块的入口，需要先来拼接模块的`package.json`文件的路径。这里用到`node`中的`path`模块，可以调用`path.join()`来拼接路径。

先定一个常量来接收拼接好的路径，现在要拼接的是`package.json`的路径。当前项目的路径是`process.cwd()`，然后是`node_modules`文件夹，在`node_modules`文件夹里边来找模块`moduleName`，然后再去找这个模块下面的`package.json`。有了这个路径之后，再使用`require`来加载`package.json`。最后重新给`cpx.path`赋值，因为之前请求的这个路径是不存在的，需要重新给它设置一个存在的路径，让它去加载这个文件。

到这里加载第三方模块就写完了，然后重启一下服务器，再打开浏览器来测试一下，看看是否OK。

![](http://5coder.cn/img/1669814888_136d2577d494314bdbbb12efe828b5b6.png)

但是这还有一个问题，加载的`vue`是`bundle`的`vue`版本，也就是需要打包的vue，但这个vue里边它又去加载了vue源码中的`runtime-dom`模块，还去加载了vue中的`shared`的模块，但是看一下请求这个位置，它根本就没有请求到这两个模块，是不是加载这两个模块出了问题呢？好，我们来看一下在`console`里面有两个错误。

这两个错误告诉我们加载模块失败。第一个是`App.vue`，第二个是`index.css`，也就是当前去加载`App.vue`和`index.css`这l两个个模块时，浏览器不能识别，所以在服务器上还要去处理浏览器不能够识别的模块。

## 5.Vite 实现原理-编译单文件组件

刚刚演示过浏览器无法处理在`main.js`中使用`import`加载的单文件组件模块和样式模块，浏览器只能够处理`js`模块，所以通过`import`加载的其他模块都需要在服务器端处理。当请求单文件组件的时候，需要在服务器上把单文件组件编译成`js`模块，然后返回给浏览器。下面先打开浏览器来观察一下`Vite`中是如何去处理单文件组件的，然后再来自己实现。这里只演示单文件组件的处理过程，其他通过`import`导入的模块你可以参考我们的实现思路自己来写。

![](http://5coder.cn/img/1669816945_09b10701e4c6b263aa718735f19501ef.png)

当第一次请求这个文件的时候，服务器会把单文件组件编译成一个对象。这里先加载`HelloWorld`这个组件，然后创建了一个组件的选项对象。注意这里没有模板，因为模板最终要被编译成`render`函数，然后挂载到选项对象上。那下面又去加载了`App.vue?type=template`。

![](http://5coder.cn/img/1669817160_649e6ee5bb99549a6dc433f17cd55ab6.png)

这次请求是告诉服务器，你去帮我编一下这个单文件组件的模板，然后返回一个`render`函数，注意现在下载的就是它的`render`函数，然后把`render`函数挂载到刚刚创建的组件选项对象上来。从这里可以看到，**当请求单文件组件的时候，服务器会来编译单文件组件，并把相应的结果返回给浏览器。**

`App.vue?type=template`这次请求是告诉服务器，你帮我把单文件组件编译成`render`函数，可以找到这个`render`函数这块，通过`export`把这个`render`函数导出了。在`app.vue`里边，去加载这个组件返回的这个`render`函数，并且把它挂载到`script`对象的`render`方法上来。

这是`vite`中是如何去处理单文件组件的，它会发送两次请求，第一次请求是把单文件组件编译成一个对象，第二次请求是编译单文件组件的模板返回一个`render`函数，并且把这个`render`函数挂载到刚刚创建的那个对象的`render`方法上。

下面实现一下第一次请求的过程：把单文件组件编译成一个对象

这次请求需要把单文件组件编译成一个组件的选项对象，这里需要写一个中间件来处理单文件组件。现在需要确定这个中间件书写的位置。当请求到单文件组件并把单文件组件读取完成之后。接下来需要对单文件组件进行编译，并且把编译的结果返回给浏览器，这里的核心是把单文件组件读取完成之后再处理，所以是在处理完静态文件之后，并且单文件组件也有可能会加载第三方模块，所以是在处理第三方模块之前，1和3中间。

```js
#!/usr/bin/env node
const path = require('path')

const Koa = require('koa')
const send = require("koa-send")
const compilerSFC = require('@vue/compiler-sfc')
const { Readable } = require("stream");

const app = new Koa()

const streamToString = stream => new Promise((resolve, reject) => {
  const chunks = []
  stream.on('data', chunk => chunks.push(chunk))
  stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')))
  stream.on('error', reject)
})

const stringToStream = text => {
  const stream = new Readable()
  stream.push(text)
  stream.push(null)
  return stream
}

// 3. 加载第三方模块
app.use(async (ctx, next) => {
  // ctx.path --> /@modules/vue
  if (ctx.path.startsWith('/@modules/')) {
    const moduleName = ctx.path.substr(10)
    const pkgPath = path.join(process.cwd(), 'node_modules', moduleName, 'package.json')
    const pkg = require(pkgPath)
    ctx.path = path.join('/node_modules', moduleName, pkg.module)
  }
  await next()
})

// 1.静态文件服务器
app.use(async (ctx, next) => {
  await send(ctx, ctx.path, { root: process.cwd(), index: 'index.html' })
  await next()
})

// 4.处理单文件组件
app.use(async (ctx, next) => {
  if (ctx.path.endsWith('.vue')) {
    // 把ctx.body转换成字符串
    const contents = await streamToString(ctx.body)
    const { descriptor } = compilerSFC.parse(contents)
    let code
    if (!ctx.query.type) {
      code = descriptor.script.content
      // console.log(code)

      code = code.replace(/export\s+default\s+/g, 'const __script = ')

      code += `
        import { render as __render } from "${ctx.path}?type=template"
        __script.render = __render
        export default __script
      `
    }
    ctx.type = 'application/javascript'
    ctx.body = stringToStream(code)
  }

  await next()
})


// 2.修改第三方模块的路径
app.use(async (ctx, next) => {
  if (ctx.type === 'application/javascript') {
    const contents = await streamToString(ctx.body)
    // import vue from 'vue
    // import App from './App.vue
    // 这里需要将【from '】替换成【from '@modules】
    ctx.body = contents.replace(/(from\s+['"])(?![\.\/])/g, '$1/@modules/')
  }
})

app.listen(3000)
console.log('Server 3000')
```

当请求的文件是单文件组件的时候，需要对单文件组件进行编译，编译的工作比较复杂，因为Vue3里的每一个模块都可以拿出来单独使用，而Vue3中又提供了编译单文件组件的模块`@vue/compiler-sfc`，所以可以直接使用这个模块来对单文件组件进行编译。

接下来要分两次来处理单文件组件，首先要去判断当前请求的是否是单文件组件，也就是请求的路径的后缀是否是以`.vue`结尾`ctx.path.endsWith('.vue')`。如果是以`.vue`结尾的话，需要把`ctx.body`转换成字符串，因为`ctx.body`中现在就是单文件组件中的内容，而在编译单文件组件的时候是需要单文件组件的内容的。`const contents = await streamToString(ctx.body)`。

这个单文件组件的内容就获取到了。下面要调用`compilerSFC.parse()`方法编译单文件组件，`const { descriptor } = compilerSFC.parse(contents)`

然后在下面再来定一个`code`变量，这是最终要返回给浏览器的代码。之前看过`vite`中的处理过程，单文件组件的请求有两次，第一次是不带`type`参数，第二次是带着`type=template`参数。

先来处理不带参数的情况，也就是第一次的请求。第一次请求的时候需要返回这个单文件组件编译之后的选项对象。先来判断一下当前的查询字符串中是否有`type`，如果当前`query`中没有`type`属性的时候，说明是第一次请求，先去接收到当前单文件组件编译之后的`js`代码。`code = descriptor.script.content`，可以打印一下

```js
import HelloWorld from './components/HelloWorld.vue'
                                                    
export default {                                    
  name: 'App',
  components: {                                     
    HelloWorld                                      
  }
}                                                   


export default {     
  name: 'HelloWorld',
  props: {           
    msg: String      
  },
  data() {           
    return {         
      count: 0       
    }                
  }                  
}
```

下面来改造一下这里的`code`，刚刚看过`code`的形式了，下面需要先把`code`中的`export default`方替换成`const __script =` ，`code = code.replace(/export\s+default\s+/g, 'const __script = ')`

```js
import {render as __render} from "/src/App.vue?type=template"
__script.render = __render
__script.__hmrId = "/src/App.vue"
typeof __VUE_HMR_RUNTIME__ !== 'undefined' && __VUE_HMR_RUNTIME__.createRecord(__script.__hmrId, __script)
__script.__file = "F:\\Web\\lagou\\03-05-Vue.js3.0\\code\\02-vite-demo\\src\\App.vue"
export default __script
```

然后后面还要去拼接上一段代码，

```js
code += `
        import { render as __render } from "${ctx.path}?type=template"
        __script.render = __render
        export default __script
      `
```

接下来设置响应头中的`contentType`，把它设置为`application/javascript`，需要告诉浏览器，现在发给你的是`javascript`模块，让浏览器去执行`javascript`模块。

最后还要把`code`输出给浏览器，`code`是字符串，需要把`code`转换成只读流设置给`ctx.body`，因为下一个中间键中要去处理的这个`body`是流的形式。

所以下面我们要来写一个辅助的函数，把字符串转换成流。

```js
const { Readable } = require("stream");

const stringToStream = text => {
  const stream = new Readable()
  stream.push(text)
  stream.push(null)
  return stream
}
```

给`ctx.body`去赋值，`ctx.body = stringToStream(code)`。重启测试

![](http://5coder.cn/img/1669819029_783e5a00785ac79d329837a566150e6c.png)

刷新一下浏览器，先找到`app.vue`，请求的这个路径已经OK了，第二次请求`App.vue?type=template`此时还没有返回的内容是因为还没有处理第二次请求。

## 6.Vite 实现原理-编译单文件组件

我们已经把单文件组件的第一次请求处理完毕，第一次请求会把单文件组件定义成组件的选项对象，然后返回给浏览器，但是这个选项对象中没有模板或者`render`函数，接下来再来处理单文件组件的第二次请求，第二次请求`url`中会带着参数`type=template`。第二次请求中，要把单文件组件的模板编译成`render`函数。

```
ctx.query.type === 'template'
```

`ctx.query.type === 'template'`的时候是对单文件组件的第二次请求。在这里要去编译模板，`compilerSFC`对象下有一个专门编译模板的方法`compileTemplate`，它需要接受一个对象形式的参数，设置要编译的模板的内容。

```js
const templateRender = compilerSFC.compileTemplate({ source: descriptor.template.content })
```

组件模板中的内容可以通过`descriptor.template.content`获取，返回的对象中有`code`属性，`code`就是的`render`函数。

![](http://5coder.cn/img/1669819353_bd1ac54a4ee87f30f6f5fc0276685e84.png)

但是`console`中有一个报错，它指向`shared`文件。

![](http://5coder.cn/img/1669819369_ad1b0b50d06ce781d679c1bf5d8dbe3f.png)

![](http://5coder.cn/img/1669819385_23749ee79a7fb993fb95314cab6dff89.png)

注意这个位置出错，它访问不到`process`。当前的代码是在浏览器环境下执行的，而`process`是`node`的环境中的对象，而现在是在浏览器环境中执行的，浏览器环境中没有`process`对象，所以报错，因此需要在返回的`js`模块中处理这部分。

```js
ctx.body = contents
      .replace(/(from\s+['"])(?![\.\/])/g, '$1/@modules/')
      .replace(/process\.env\.NODE_ENV/g, '"development"')
```

在返回`js`模块之前，要把`js`模块中的所有`process.env.NODE_ENV`都替换成`development`，表示当前是开发环境。

打开浏览器来测试一下。

刷新浏览器，终于可以看到这个结果了。这块没有样式是因为我们之前把样式模块以及图片都给它注释起来了。点击这个按钮组件也可以正常工作。

到这里，模拟`vite`的实现就写完了。这里的核心是在开发阶段不需要本地打包，根据需要请求服务器编译单文件组件。当然这里还没有去处理样式和图片模块，可以根据实现单文件组件的思路来尝试实现处理样式模块和图片模块，可以观察Vite返回的结果，自己来模拟。















![](http://5coder.cn/img/1669819499_c2db34f8d35a40c9a133d42585c60837.png)
