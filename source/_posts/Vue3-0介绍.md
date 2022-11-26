---
title: Vue3.0介绍
author: 5coder
tags: Vue3.0
category: 大前端
abbrlink: 46153
date: 2022-11-26 14:37:31
password:
keywords:
top:
cover:
---

# Vue3.0介绍

## 1.Vue.js 3.0 源码组织方式

**Vue2.x与Vue3.0的区别**

- 源码组织方式的变化

  - Vue3.0的源码全部采用`TypeScript`重写
  - 使用`Monorepo`方式来组织项目结构，把独立的功能模块都提取到不同的包中。

  packages下都是独立发行的包，可以独立使用。

  ![](http://5coder.cn/img/1669446353_2937816ab692eff4a999afb81da6bb87.png)

- Composition API（组合API）

  Vue 3.0代码虽然重写，但是90%以上的API兼容2.x，并且增加了`Composition API`（组合API），是用来解决Vue 2.x在开发大型项目时遇到超大组件，使用`options API`不好拆分和重用的问题。

- 性能提升

  Vue 3.0使用`Proxy`重写了响应式代码，并对编译器做了优化，重写了虚拟DOM，从而让渲染和`update`的性能都有了大幅度的提升，另外服务端渲染`SSR`的性能也提升了2-3倍。

- Vite

  官方提供了一个开发工具Vite，使用Vite在开发和测试阶段，不用打包项目，可以直接去运行项目，提升了开发的效率。

## 2.不同的构建版本

![](http://5coder.cn/img/1669446481_3f62c8b051859578d171d607afe8a7a7.png)

![](http://5coder.cn/img/1669447158_bcac938cc75496637ae1b8d331ed6878.png)

## 3.Composition API 设计动机

- RFC (Request For Comments)

  https://github.com/vuejs/rfcs

- Composition API RFC

  https://composition-api.vuejs.org

**Composition API 的设计动机**

> Options API：使用包含组件描述选项的对象来创建组件的方式。例如选项：`data`、`methods`、`created`等等组成对象，来组成组件。

![](http://5coder.cn/img/1669447559_df26b93cee8276c78f71cb752548ff1e.png)

案例：可以看到要实现一个功能，需要在不同选项中添加。如果此时需要在添加一个功能，就需要在多个选项中添加代码。并且难以提取组件中重复的代码。

- Options API（Vue 2.x）

  - 包含一个描述组件选项（data、methods、props等）的对象
  - Options API开发复杂组件，同一个功能逻辑的代码被拆分到不同选项
  - Options API难以提取组件中可重用的逻辑，虽然有mixin，但容易命名冲突，数据来源不清晰。

- Composition API（Vue 3.0）

  - Vue 3.0新增的一组API
  - 一组基于函数的API
  - 可以更灵活的组织组件的逻辑

  Compisition API案例，可以看到将功能封装到一个函数内部，如果需要再增加一个功能，只需要再封装一个函数，然后在setup函数中调用函数。

  ![](http://5coder.cn/img/1669447675_885e5404d65c64d4905ea19004583dfb.png)

官方提供的案例图，Options API中可以看到相同色块代表同一个功能，分布在不同的位置，而Composition API则是一个功能一个块。

![](http://5coder.cn/img/1669447826_f11d29df367a618799c8b71681400bd4.png)

## 4.性能提升

- 响应式系统升级

  > 首先来看一下响应式系统升级。我们都知道Vue2的时候，数据响应式的原理使用的是`defineProperty`，在初始化的时候会遍历`data`中的所有成员。通过`defineProperty`，把对象的属性转换成`getter`和`setter`。如果`data`中的属性又是对象的话，需要递归处理每一个子对象的属性。**注意这些都是在初始化的时候进行的**。也就是说如果你没有使用这个属性的时候，你也把它进行了响应式的处理。
  >
  > 而Vue3中采用的是`ES6`以后新增的`proxy`对象。`proxy`对象的性能本身就比`defineProperty`要好。另外，代理对象可以拦截属性的**访问、复制、删除**等操作。不需要初始化的时候遍历所有的属性。另外，如果有多层属性嵌套的话，只有访问某个属性的时候，才会递归处理下一级的属性，使用`proxy`对象默认就可以监听到动态添加的属性。而Vue2里边想要动态添加一个显示的属性需要调用`this.$set`的方法来处理。而且Vue2中还监听不到属性的**删除**，对数组的**索引和length属性的修改**也监听不到。Vue3中**使用代理对象可以监听属性的删除以及数组的索引和length属性的修改操作**。所以Vue3中使用`proxy`对象提升了响应式系统的性能和功能。

  - Vue 2.x中响应式系统的核心是defineProperty
  - Vue 3.0中使用Proxy对象重写响应式系统
    - 可以监听动态新增的属性
    - 可以监听删除的属性
    - 可以监听数组的索引和length属性

- 编译优化

  > Vue3中通过优化编译的过程和重写虚拟`DOM`，让首次渲染和更新的性能有了大幅度的提升。我们知道Vue2的时候，模板首先需要编译成`render`函数，这个过程一般是在构建的过程中完成的。在编译的时候会编译**静态根节点**和**静态节点**。静态根节点要求节点中必须有一个静态子节点，当组件的状态发生变化后，会通知`watch`触发`watcher`和`update`。最终去执行虚拟`DOM`的`patch`操作遍历所有的虚拟节点，找到差异，然后更新到真实`DOM`上。
  > `Diff`的过程中会去比较整个虚拟`DOM`，先对比新旧的`div`以及它的属性，然后再对比它内部的子节点。Vue2中渲染的最小单位是组件。Vue2中`diff`的过程会跳过静态根节点，因为静态根节点的内容不会发生变化，也就是Vue2中通过**标记静态根节点优化了`diff`的过程**。但是在Vue2的时候，**静态节点还需要再进行`diff`，这个过程没有被优化**。
  >
  > Vue3中为了提高性能，在编译的时候会**标记和提升所有的静态节点**，然后`diff`的时候**只需要对比动态节点的内容**。另外在Vue3中新引入了一个`Fragments`，也就是片段的特性，模板中不需要再创建一个唯一的根节点模板，里边可以直接放文本内容或者很多同级的标签。
  >
  > 在Vs code中需要升级你的`Vetur`插件，否则模板中如果没有唯一的根据点VS Code依然会提示有错误。
  >
  > ![](http://5coder.cn/img/1669450114_d8c12a3d8b31eca828dc7e29ef21d1ed.png)
  >
  > 左边是我们刚刚看到的组件模板中的内容，右边是我们编译之后的render函数，但是这个编译的结果跟Vue2会有很大的区别，首先这里调用`_createBlock`给我们的根`div`创建了一个`block`，它是一个树的结构，然后通过`createVNode`的去创建了我们的子节点，那这里的`createVNode`的其实就是类似于我们之前的`h`函数。
  >
  > 那我们来删除这里面的**根节点**，来看一下它的变化。
  >
  > ![](C:/Users/5coder/AppData/Roaming/Typora/typora-user-images/image-20221126161031253.png)当我们删除根节点之后，这里会创建一个`fragment`，也就是我们之前说的片段。其实从这里还可以看到，它内部还是维护了一个树形的结构，那么最外层是`fragment`，里边是我们的这些`VNode`的。
  > Vue 2.x中通过标记静态根节点，优化diff的过程

  - Vue 3.0中标记和提升所有的静态根节点，diff的时候只需要对比动态节点内容
    - Fragments（升级vetur插件）
    - 静态提升
    - Patch flag
    - 缓存事件处理函数

- 源码体积的优化

  - Vue 3.0中移除了一些不常用的API（如inline-template、filter等）
  - Tree-shaking

## 5.Vite

**ES Module**

- 现代浏览器都支持ES Module（IE不支持）
- 通过下面的方式加载模块
- 支持模块的script默认延迟加载（相当于省略了defer属性）
  - 类似于script标签设置defer
  - 在文档解析完成后，触发DOMContentLoaded事件前执行（加载模块并执行，是在DOM创建之后，并且在DOMContentLoaded执行之前执行的）

浏览器使用ES Module案例

项目结构：![](http://5coder.cn/img/1669455142_42b18eb8f7ec9d0ee024fe9810e982e4.png)

`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <div id="app">Hello World</div>
  <script>
    window.addEventListener('DOMContentLoaded', () => {
      console.log('DOMContentLoaded')
    })

  </script>
  <script type="module" src="./modules/index.js"></script>
</body>
</html>
```

`modules/index.js`

```js
import { forEach } from './utils.js'

const app = document.querySelector('#app')
console.log(app.innerHTML)

const arr = [1, 2, 3]
forEach(arr, item => {
  console.log(item)
})
```

`modules/utils.js`

```js
export const forEach = (array, fn) => {
  let i
  for (i = 0; i < array.length; i++) {
    fn(array[i])
  }
}

export const some = (array, fn) => {
  let result = true
  for (const value of array) {
    result = result || fn(value)
    if (result) {
      break
    }
  }
  return result
}
```

打开index.html我们可以发现，设置了`type="module"`后，`script`默认延迟加。并且执行结果为：先加载模块，后执行`DomContentLoaded`事件。

![](http://5coder.cn/img/1669455300_f8f59d34a49ebf9bee9e19cf871aa90e.png)

**Vite与Vue-cli区别**

Vite的快就是使用浏览器支持的`ES module`的方式，避免开发环境下打包，从而提升开发速度。下面看一下`Vite`和`Vue Cli`的区别，最主要的区别是`Vite`在开发环境下不需要打包，因为在开发模式下，`Vite`使用浏览器原生支持的`ES module`加载模块，也就是通过`import`来导入模块，支持`ES module`的现代浏览器通过`script` `type="module"`的方式加载模块代码。

因为`Vite`不需要打包项目，因此`Vite`在开发模式下打开页面是秒开的，而`Vue Cli`在开发环境下会先打包整个项目，如果项目比较大，速度会特别慢。

- Vite在开发模式下不需要打包可以直接运行
- Vue-cli开发模式下必须对项目打包才可以运行
- Vite在生产环境下使用Rollup打包基于ES Module的方式打包
- Vue-cli使用webpack打包

**Vite特点**

Vite会开启一个测试的服务器，它会拦截浏览器发送的请求，浏览器会向服务器发送请求获取相应的模块，那为此会对浏览器不识别的模块进行处理。比如当`import`单文件组件的时候，也就是后缀名为`.vue`的文件时，会在服务器上对`.vue`文件进行编译，把编译的结果返回给浏览器。稍后我们会演示这个过程。使用这种方式让`Vite`有以下的优点：

- 快速冷启动

  因为不需要打包，所以可以快速冷启动。

- 按需编译

  代码是按需编译的，因此只有当代码在当前需要加载的时候才会编译。你不需要在开启开发服务器的时候等待整个项目被打包，那当项目比较大的时候，这个时候就会更明显。

- 模块热更新

  `Vite`支持模块热更新，并且模块热更新的性能与模块总数无关。无论你有多少模块，`HMR`的速度始终比较快。

另外，Vite在生产环境下使用`Rollup`打包，`Rollup`基于浏览器原生的`ES Module`进行打包，它不需要再使用`Babel`，再把`import`转换成`require`以及一些相应的辅助函数，因此打包的体积会比`webpack`打包的体积更小。现在浏览器都已经支持`ES Module`的方式加载模块。

**Vite创建项目**

Vite有两种创建项目的方式，一种是创建基于Vue3的项目，可以直接在终端输入`npm init vite-app <项目名称>`来创建项目，然后再切换到项目目录`cd <项目名称>`，输入`npm i`安装依赖。最后通过`npm run dev`在开发环境下运行项目。

![](http://5coder.cn/img/1669455499_9d00aba0a2cb87d6dc270ffd7c8716bc.png)

 还有一种方式是基于模板创建项目，Vite基于模板的方式可以让它支持其他的框架，在创建项目的时候，后面跟上要使用的框架，比如是`--template react`。

![](http://5coder.cn/img/1669455507_eef5c6d7039303af4cbfeaebb4f5d5f4.png)

这里我们演示第一种方式。

使用第一种方式创建后的项目目录结构如下：

![](http://5coder.cn/img/1669456909_5786e7a001edbdd0918a877efec511de.png)

`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="/favicon.ico" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vite App</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
```

`main.js`

```js
import { createApp } from 'vue'
import App from './App.vue'  // 将单文件组件当成模块来加载
import './index.css'

createApp(App).mount('#app')
```

`APP.vue`

```html
<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <HelloWorld msg="Hello Vue 3.0 + Vite" />
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>
```

使用`npm run dev`运行项目，可以开发服务器开启的速度很快，因为他没有打包的过程。

![](http://5coder.cn/img/1669457317_98b5fd39927d6f824f54732b47365ecf.png)

网页源代码：![](http://5coder.cn/img/1669457349_ee622af0c3f2ea55ffc8ab03cbbf5916.png)

打开开发人员工具，找到`NetWork`：

![](http://5coder.cn/img/1669457477_d633579d4f81e3ba92ad6f9e72bc10ef.png)

这里有很多请求，找一下`.vue`结尾的这块有一个app.vue。`Vite`开启的这个`web`服务器，它会劫持`.vue`的请求，它首先会把`.vue`文件解析成`JS`文件，并且把响应头中的`contentType`设置为`application/javascript`，目的是告诉浏览器**我现在给你发送的是一个javascript脚本**。

![](http://5coder.cn/img/1669457657_9495050c671074cb5a67c66fdfca608a.png)

那下面我们再来看`response`，这是服务器解析的js模块，这里又导入了`helloWorld.vue`这个单文件组件。

注意`import { render as __render } from "/src/App.vue?type=template"`。这里又通过import导入了App.vue模块，后面加了一个参数`:type="template"`。这里导入这个模块的`render`函数，注意，我们的`App.vue`是单文件组件，在编写的时候根本没有写`render`函数。现在之所以能导出这个`render`函数，是因为服务器对它做了特殊的处理，我们一会儿来解释。那这里只要加载模块就会向服务器发送请求，请求这个模块。

再来往下看，这里又请求了`HelloWorld.vu`e这个单文件组件，它的处理方式跟刚刚的`App.vue`是一样的。再往下看的话，这里又请求了`App.vue?type=template`。这次请求到服务器之后，服务器会把这个`App.vue`这个单文件组件通过`vue`中的模块`compile-sfc`给它编译成`render`函数。

![](http://5coder.cn/img/1669457922_d832af3667d76ad649966044137db6d9.png)

可以看到`response`中的内容，这里首先把静态节点提升，然后下面是render函数。这就是Vite的工作原理：它使用浏览器支持的`ES Module`的方式来加载模块。在开发环境下，它不会打包项目，把所有的模块的请求都交给服务器来处理，在服务器去处理浏览器不能识别的模块。如果是单文件组件，会调用`compile-sfc`编译单文件组件，并把编译的结果返回给浏览器。

