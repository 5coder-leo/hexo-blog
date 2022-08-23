---
title: Vue.js 源码剖析-响应式原理
author: 5coder
tags: Vue响应式
category: 大前端
keywords: 响应式原理
abbrlink: 42659
date: 2021-06-21 21:30:13
password:
top:
cover: true
coverImg: http://5coder.cn/img/1661217798_0c9580b8c88e7fa7391117d7669cfe83.jpg
img: http://5coder.cn/img/1661217798_0c9580b8c88e7fa7391117d7669cfe83.jpg
---

# Vue源码解析-响应式原理

## 课程目标

- Vue.js的静态成员和实例成员初始化过程
  - `vue.use()`、`vue.set()`、vue.extened()等这些全局成员的创建过程
  - vm.$el、`vm.$data`、vm.$on、`vm.$mount`等这些实例成员的创建过程
- 首次渲染的过程
  - 创建完vue实例，并把数据传递给vue之后，vue内部是如何把数据渲染到页面的，后续在分析源码过程中都是基于这个过程的
- **数据响应式原理（核心）**

## 准备工作

#### Vue源码的获取

- 项目地址：https://github.com/vuejs/vue
- Fork一份到自己仓库，克隆到本地，可以自己写注释提交到github
- 为什么分析Vue2.6
  - 到目前为止Vue3.0的正式版本还没有发布
  - 新版本发布后，现有项目不会升级到3.0，2.x患有很长一段过渡期
  - 3.0项目地址：https://github.com/vuejs/vue-next

#### 源码目录结构

```txt
vue
    ├─dist  打包之后的结果，包含不同版本
    ├─examples  示例
    ├─flow  
    ├─packages
    ├─scripts
    ├─src
        ├─compiler  编译相关（把模板转换成render函数，render函数会创建虚拟DOM）
        ├─core  Vue 核心库
        	├─components  定义vue自带的keep-alive组件
        	├─global-api  定义vue中的静态方法，包含vue.component()、vue.filter()、vue.extend()等
        	├─instance  创建vue示例的位置，定义vue的构造函数以及vue的初始化、生命周期的响应函数
        	├─observer  响应式机制实现的位置
        	├─utils  公共成员
        	├─vdom  虚拟DOM，vue中的虚拟DOM重写了snabbdom，增加了组件的形式
        ├─platforms 平台相关代码
        	├─web  web平台下相关代码
                ├─compiler
                ├─runtime
                ├─server
                ├─util
                ├─entry-compiler.js  打包入口文件
                ├─entry-runtime.js  打包入口文件
                ├─entry-runtime-with-compiler.js  打包入口文件
                ├─entry-server-basic-renderer.js  打包入口文件
                ├─entry-server-renderer.js  打包入口文件
        	├─weex  week平台下相关代码（week是vue基于移动端下开发的框架）
        ├─server SSR，服务端渲染
        ├─sfc .vue 文件编译为 js 对象（Single File Component单文件组件）
        └─shared 公共的代码
```

#### 了解Flow

- 官网：https://flow.org/
- JavaScript的静态类型检查器
- Flow的静态类型检车错误是通过静态类型推断实现的
  - 文件开头通过`// @flow` 或者`/* @flow */`声明

#### 调试设置

##### 打包

- 打包工具Rollup

  - vue.js源码的打包工具使用的是Rollup，比webpack清凉
  - Webpack把所有的文件当做模块，Rollup只处理js文件，更适合在Vue.js这样的库中使用
  - Rollup打包不会生成冗余的代码

- 安装依赖

  ```shell
  yarn
  ```

- 设置sourcemap

  - package.json文件中的script的dev脚本中添加参数`--sourcemap`

    ```json
    "dev": "rollup -w -c scripts/config.js --sourcemap --environment TARGET:webfull-dev"
    ```

- 执行dev

  - 执行打包前先删除dist目录，rollup会自动生成dist目录

  - yarn dev执行打包，用的是rollup，-w参数是坚挺稳健的变化，文件变化自动重新打包

  - 结果

    ![](http://5coder.cn/img/image-20210621215220709.png)

##### 调试

- examples的实例中引入的是vue.min.js，将其改为vue.js

- 打开Chrome的调试工具中的source

  ![](http://5coder.cn/img/image-20210621215534350.png)

<iframe src="http://5coder.cn/static/video/20210621_215739.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height=500 width=700 autoplay="false"> </iframe>

#### Vue的不同构件版本

- 运行`yarn build`重新打包所有文件

- 官方文档 - [对不同构建版本的解释](https://cn.vuejs.org/v2/guide/installation.html#%E5%AF%B9%E4%B8%8D%E5%90%8C%E6%9E%84%E5%BB%BA%E7%89%88%E6%9C%AC%E7%9A%84%E8%A7%A3%E9%87%8A)

- dist\README.md

  |                              | UMD                | CommonJS          | ES Module      |
  | ---------------------------- | ------------------ | ----------------- | -------------- |
  | **Full**                     | vue.js             | vue.common.js     | vue.esm.js     |
  | **Runtime-only**             | vue.runtime.js     | vue.common.min.js | vue.esm.min.js |
  | **Full(Production)**         | vue.min.js         |                   |                |
  | **Runtime-only(Production)** | vue.runtime.min.js |                   |                |

##### 术语

- **完整版**：同时包含**编译器**和**运行时**的版本
- **编译器**：用来将模板字符串编译成为JavaScript渲染函数的代码，体积大、效率低
- **运行时**：用来创建Vue实例、渲染并处理虚拟DOM等的代码，体积小、效率高。基本上就是除去编译器的代码
- **[UMD](https://github.com/umdjs/umd)**：UMD版本**通用的模块版本**，支持多种模块方式。vue.js默认文件就是运行时+编译器的UMD版本
- [**CommonJS**](http://wiki.commonjs.org/wiki/Modules/1.1)(cjs)：CommonJS版本用来配合老的打包工具比如[Browserify](https://browserify.org/)或[webpack 1](https://webpack.github.io/)
- [**ES Module**](https://exploringjs.com/es6/ch_modules.html)：从2.6开始Vue会提供两个ES Module(ESM)构建稳健，为现代打包工具提供的版本
  - ESM格式被设计为可以被静态分析，所以打包工具可以利用这一点来进行“Tree-Shaking”并将用不到的代码排除最终的包
  - [ES6模块与CommonJS模块的差异](https://es6.ruanyifeng.com/#docs/module-loader#ES6-%E6%A8%A1%E5%9D%97%E4%B8%8E-CommonJS-%E6%A8%A1%E5%9D%97%E7%9A%84%E5%B7%AE%E5%BC%82)

##### Runtime + Compiler VS Runtime-only

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>

</head>
<body>
<div id="app">
  Hello World
</div>

<script src="../../dist/vue.js"></script>
<script>
  // Compiler
  // 需要编译器，把template转换成render函数
  const vm = new Vue({
    el: '#app',
    template: '<h1>{{ msg }}</h1>',
    data: {
      msg: "Hello Vue"
    }
  })
</script>
</body>
</html>
```

![](http://5coder.cn/img/image-20210621232639624.png)

将vue版本改为`vue.runtime.js`，发现浏览器报错，提示更改为render函数或者用compiler-included build。

![](http://5coder.cn/img/image-20210621232855357.png)

更改template如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>

</head>
<body>
<div id="app">
  Hello World
</div>

<script src="../../dist/vue.runtime.js"></script>
<script>
  // Compiler
  // 需要编译器，把template转换成render函数
  const vm = new Vue({
    el: '#app',
    // template: '<h1>{{ msg }}</h1>',
    render(h) {
      return h('h1', this.msg)
    },
    data: {
      msg: "Hello Vue"
    }
  })
</script>
</body>
</html>

```

![](http://5coder.cn/img/image-20210621233125601.png)

#### 使用vue-cli创建项目时查看vue构件版本

在使用`vue create projectName`创建的项目中，查看`vue`的构建版本。由于Vue对`webpack.config.js`进行了深度封装，所以在目录中无法看到其配置文件，但是Vue提供了命令行来查看配置文件。

```bash
vue inspect  # 直接输出到控制台
vue inspect > output.js  # 将执行vue inspect命令后的结果输出到output.js文件中
```

![](http://5coder.cn/img/image-20210622055014013.png)

> output.js不是一个有效的`webpack`配置文件，不能拿来直接使用。

可以看到在`resolve`中的`alias`中，vue-cli使用了`vue.runtime.esm.js`（运行时版本，模块化为ES Module）作为构建版本，`vue$`中的`$`符号为精确匹配，在使用时直接使用`import Vue from vue`。

> runtime+compiler与runtime对比（ast：抽象语法树），由下面过程可见runtime-only性能更高。
>
> - **runtime+compiler**
>   - `template -> ast -> render -> vdom ->UI`
> - **runtime-only**
>   - `render -> vdom -> UI`
>
> ![](http://5coder.cn/img/image-20210622060735123.png)
>
> 以上内容来自[**coderwhy**哔哩哔哩动画第96节视频](https://www.bilibili.com/video/BV15741177Eh?p=96)

## 寻找入口文件

- 查看dist/vue.js的构建过程

### 执行构建

```bash
yarn dev
# "dev": "rollup -w -c scripts/config.js --sourcemap --environment TARGET:web-full-dev"
# --environment TARGET:web-full-dev 设置环境变量TARGET
```

- `script/config.js`的执行过程

  - 作用：生成`rollup`构建的配置文件
  - 使用环境变量`TARGET=web-full-dev`

  ```js
  // 判断环境变量中是否有TARGET
  // 如果有的话，使用genConfig()生成rullup配置文件
  if (process.env.TARGET) {
      module.exports = genConfig(process.env.TARGET)
  } else {
      // 否则获取全部配置
      exports.getBuild = getConfig
      exports.getAllBuilds = () => Objet.keys(builds).map(genconfig)
  }
  ```

- `genConfig(name)`

  - 根据环境变量TARGET获取配置信息
  - builds[name]获取生成配置的信息

  ```js
  // Runtime+compiler development build (Browser)
  'web-full-dev': {
      entry: resolve('web/entry-runtime-with-compiler.js'),
      dest: resolve('dist/vue.js'),
      format: 'umd',
      env: 'development',
      alias: { he: './entity-decoder'},
      banner
  },
  ```

- `resolve()`

  - 获取入口和出口文件的绝对路径

  ```js
  const aliases = require('./alias')
  const resolve = p => {
      // 根据路径中的前半部分去alias中找别名
      const base = p.split('/')[0]
      if (aliases[base]) {
          return path.resolve(aliases[base], p.splice(base.length + 1))
      } else {
          return path.resolve(__dirname, '../', p)
      }
  }
  ```

### 结果

- 把`src/platforms/web/entry-runtime-with-compiler.js`构建成`dist/vue.js`，如果设置`--sourcemap`，则会生成`vue.js.map`文件
- `src/platform`文件夹下是Vue可以构建成不同平台下使用的库，目前有`weex`和`web`，还有服务端渲染`SSR`的库

## 从入口开始

- src/platform/web/entry-runtime-with-compiler.js

#### 通过查看源码解决下面问题

- 观察以下代码，通过阅读源码，回答在页面上输出的结果

```js
const vm = new Vue({    el: '#app',    template: '<h3>Hello Template</h3>',    render(h) {        return h('h4', 'Hello Render')    }})
```

- 阅读源码记录

  - el不能是body或者html标签
  - 如果没有render，把template转换成render函数
  - 如果有render方法，直接调用mount挂载DOM

  ```js
  // 1. el 不能是 body 或者 htmlif (el === document.body || el === document.documentElement) {  process.env.NODE_ENV !== 'production' && warn(    `Do not mount Vue to <html> or <body> - mount to normal elementsinstead.`  )  return this}const options = this.$optionsif (!options.render) {// 2. 把 template/el 转换成 render 函数……}// 3. 调用 mount 方法，挂载 DOMreturn mount.call(this, el, hydrating)
  ```

  - 调试代码
    - 调试的方法

  ```js
  const vm = new Vue({    el: '#app',    template: '<h3>Hello template</h3>',    render (h) {    	return h('h4', 'Hello render')    }})
  ```

  ![](http://5coder.cn/img/image-20210622223137140.png)

#### Vue的构造函数在哪里

> Vue的构造函数在哪？
>
> Vue实例的成员/Vue的静态成员从哪里来的？

- `src/platform/web/entry-runtime-with-compiler.js`中引用了'`./runtime/index`'

- `src/platform/web/runtime/index.js`

  - 设置Vue.config
  - 设置平台相关的指令和组件
    - 指令v-model、v-show
    - 组件transition、transition-group
  - 设置平台相关的`__patch__`方法（打补丁方法，对比新旧的VNode）
  - 设置`$mount`方法，挂载DOM

  ```js
  / install platform runtime directives & components// 注册跟平台相关指令和组件extend(Vue.options.directives, platformDirectives)  // 注册指令v-model、v-showextend(Vue.options.components, platformComponents)  // 注册组件v-transition、v-TransitionGroup// install platform patch function// 如果为浏览器环境则返回patch，否则返回noop空函数Vue.prototype.__patch__ = inBrowser ? patch : noop// public mount methodVue.prototype.$mount = function (  el?: string | Element,  hydrating?: boolean): Component {  el = el && inBrowser ? query(el) : undefined  return mountComponent(this, el, hydrating)  // 渲染DOM}
  ```

  - `src/platform/web/runtime/index.js`中引用了'`core/index`'
  - `src/core/index.js`
    - 定义了Vue的静态方法
    - `initGlobalAPI(Vue)`
  - `src/core/index.js`中引用了'`./instance/index`'
  - `src/core/instance/index.js`
    - 定义了Vue的构造函数

  ```js
  / 此处不用class的原因是因为方便后续给Vue实例混入实例成员function Vue (options) {  if (process.env.NODE_ENV !== 'production' &&    !(this instanceof Vue)  ) {    warn('Vue is a constructor and should be called with the `new` keyword')  }  // 调用_init()方法  this._init(options)}// 注册vm的_init()方法，初始化vminitMixin(Vue)// 注册vm的$data/$props/$set/$delete/$watchstateMixin(Vue)// 初始化事件相关方法// $on/$once/$off/$emiteventsMixin(Vue)// 初始化生命周期相关的混入方法// _update/$forceUpdate/$destroylifecycleMixin(Vue)// 混入render// $nextTick/_renderrenderMixin(Vue)
  ```

#### 四个导出Vue的模块

- `src/platform/web/entry-runtime-with-compiler.js`(核心作用：增加了编译的功能)
  - web平台相关的入口
  - 重写了平台相关的`$mount()`方法
  - 除了使用`$mount`方法可以将模板字符串转换成`render()`函数，还定义了`Vue.compile()`方法可以将模板字符串转换成`render()`函数
  - 注册了`Vue.compile()`方法，传递了一个HTML字符串返回`render`函数
- `src/platform/web/runtime/index.js`
  - web平台相关
  - 注册和平台相关的全局指令：`v-model`、`v-show`
  - 注册和平台相关的全局组件：`v-transition`、`v-transition-group`
  - 全局方法：
    - `__patch__`：把虚拟DOM转换成真实DOM
    - `$mount`：挂载方法，把DOM渲染到界面上
- `src/core/index.js`
  - 与平台无关
  - 设置了Vue的静态方法，`initGlobalAPI(Vue)`
- src/core/instance/index.js
  - 与平台无关
  - 定义了Vue构造函数，调用了`this._init(options)`方法
  - 给Vue中混入了常用的实例成员

![Snipaste_2021-06-23_06-11-34](http://5coder.cn/img/Snipaste_2021-06-23_06-11-34.png)

## Vue的初始化

### src/core/global-api/index.js

- 初始化Vue的静态方法

```js
/* @flow */

import config from '../config'
import { initUse } from './use'
import { initMixin } from './mixin'
import { initExtend } from './extend'
import { initAssetRegisters } from './assets'
import { set, del } from '../observer/index'
import { ASSET_TYPES } from 'shared/constants'
import builtInComponents from '../components/index'
import { observe } from 'core/observer/index'

import {
  warn,
  extend,
  nextTick,
  mergeOptions,
  defineReactive
} from '../util/index'

export function initGlobalAPI (Vue: GlobalAPI) {
  // config
  const configDef = {}
  configDef.get = () => config
  if (process.env.NODE_ENV !== 'production') {
    configDef.set = () => {
      warn(
        'Do not replace the Vue.config object, set individual fields instead.'
      )
    }
  }
  // 初始化Vue.config对象
  Object.defineProperty(Vue, 'config', configDef)

  // exposed util methods.
  // NOTE: these are not considered part of the public API - avoid relying on
  // them unless you are aware of the risk.
  // 这些工具方法不视作全局API的一部分，除非你已经意识到某些风险，否则不要去依赖他们
  Vue.util = {
    warn,
    extend,
    mergeOptions,
    defineReactive
  }
  // 静态方法 set/delete/nextTick
  Vue.set = set
  Vue.delete = del
  Vue.nextTick = nextTick

  // 2.6 explicit observable API
  // 让一个对象可响应
  Vue.observable = <T>(obj: T): T => {
    observe(obj)
    return obj
  }
 // 初始化vue.options对象，并给其扩展
  Vue.options = Object.create(null)
  ASSET_TYPES.forEach(type => {
    Vue.options[type + 's'] = Object.create(null)
  })

  // this is used to identify the "base" constructor to extend all plain-object
  // components with in Weex's multi-instance scenarios.
  Vue.options._base = Vue
  // 设置 keep-alive组件
  extend(Vue.options.components, builtInComponents)

  // 注册Vue.use()用来注册插件
  initUse(Vue)
  // 注册Vue.mixin()实现混入
  initMixin(Vue)
  // 注册Vue.extend()基于传入的options返回一个组件的构造函数
  initExtend(Vue)
  // 注册Vue.directive()、Vue.component()、Vue.filter()
  initAssetRegisters(Vue)
}
```

- src/core/global-api/use.js

```js
/* @flow */import { toArray } from '../util/index'export function initUse (Vue: GlobalAPI) {  Vue.use = function (plugin: Function | Object) {    const installedPlugins = (this._installedPlugins || (this._installedPlugins = []))    if (installedPlugins.indexOf(plugin) > -1) {      return this    }    // additional parameters    // 把数组中的第一个元素(plugin)去除，后面的是install方法或plugin的参数的参数    const args = toArray(arguments, 1)    args.unshift(this)    // 把this(Vue)插入第一个元素的位置    if (typeof plugin.install === 'function') {      plugin.install.apply(plugin, args)    } else if (typeof plugin === 'function') {      plugin.apply(null, args)    }    installedPlugins.push(plugin)    return this  }}
```

- src/core/global-api/mixin.js

```js
/* @flow */import { mergeOptions } from '../util/index'export function initMixin (Vue: GlobalAPI) {  Vue.mixin = function (mixin: Object) {    this.options = mergeOptions(this.options, mixin)    return this  }}
```

- src/core/global-api/extend.js

```js
/* @flow */

import { ASSET_TYPES } from 'shared/constants'
import { defineComputed, proxy } from '../instance/state'
import { extend, mergeOptions, validateComponentName } from '../util/index'

export function initExtend (Vue: GlobalAPI) {
  /**
   * Each instance constructor, including Vue, has a unique
   * cid. This enables us to create wrapped "child
   * constructors" for prototypal inheritance and cache them.
   */
  Vue.cid = 0
  let cid = 1

  /**
   * Class inheritance
   */
  Vue.extend = function (extendOptions: Object): Function {
    extendOptions = extendOptions || {}
    // Vue的构造函数
    const Super = this
    const SuperId = Super.cid
    // 从缓存中加载组件的构造函数
    const cachedCtors = extendOptions._Ctor || (extendOptions._Ctor = {})
    if (cachedCtors[SuperId]) {
      return cachedCtors[SuperId]
    }

    const name = extendOptions.name || Super.options.name
    if (process.env.NODE_ENV !== 'production' && name) {
      // 如果是开发环境验证组件的名称
      validateComponentName(name)
    }

    // 组件对应的构造函数
    const Sub = function VueComponent (options) {
      // 调用——init()初始化
      this._init(options)
    }
    // 原型继承自Vue
    Sub.prototype = Object.create(Super.prototype)
    Sub.prototype.constructor = Sub
    Sub.cid = cid++
    // 合并options
    Sub.options = mergeOptions(
      Super.options,
      extendOptions
    )
    Sub['super'] = Super

    // For props and computed properties, we define the proxy getters on
    // the Vue instances at extension time, on the extended prototype. This
    // avoids Object.defineProperty calls for each instance created.
    if (Sub.options.props) {
      initProps(Sub)
    }
    if (Sub.options.computed) {
      initComputed(Sub)
    }

    // allow further extension/mixin/plugin usage
    Sub.extend = Super.extend
    Sub.mixin = Super.mixin
    Sub.use = Super.use

    // create asset registers, so extended classes
    // can have their private assets too.
    ASSET_TYPES.forEach(function (type) {
      Sub[type] = Super[type]
    })
    // enable recursive self-lookup
    if (name) {
      Sub.options.components[name] = Sub
    }

    // keep a reference to the super options at extension time.
    // later at instantiation we can check if Super's options have
    // been updated.
    Sub.superOptions = Super.options
    Sub.extendOptions = extendOptions
    Sub.sealedOptions = extend({}, Sub.options)

    // cache constructor
    cachedCtors[SuperId] = Sub
    return Sub
  }
}
```

- src/core/global-api/extend.js

```js
/* @flow */

import { ASSET_TYPES } from 'shared/constants'
import { isPlainObject, validateComponentName } from '../util/index'

export function initAssetRegisters (Vue: GlobalAPI) {
  /**
   * Create asset registration methods.
   */
  // 遍历ASSET_TYPE数组，为Vue定义响应方法
  // ASSET_TYPE包括了directive、component、filter
  ASSET_TYPES.forEach(type => {
    Vue[type] = function (
      id: string,
      definition: Function | Object
    ): Function | Object | void {
      if (!definition) {
        return this.options[type + 's'][id]
      } else {
        /* istanbul ignore if */
        if (process.env.NODE_ENV !== 'production' && type === 'component') {
          validateComponentName(id)
        }
        // Vue.component('comp', { template: '' })
        if (type === 'component' && isPlainObject(definition)) {
          definition.name = definition.name || id
          // 把组件配置转换为组件的构造函数
          definition = this.options._base.extend(definition)
        }
        if (type === 'directive' && typeof definition === 'function') {
          definition = { bind: definition, update: definition }
        }
        // 全局注册，存储资源并赋值
        // this.options['components']['comp'] = definition
        this.options[type + 's'][id] = definition
        return definition
      }
    }
  })
}

```

![](http://5coder.cn/img/image-20210628055348086.png)

### src/core/instance/index.js

- 定义Vue的构造函数
- 初始化Vue的实例成员

```js
import { initMixin } from './init'
import { stateMixin } from './state'
import { renderMixin } from './render'
import { eventsMixin } from './events'
import { lifecycleMixin } from './lifecycle'
import { warn } from '../util/index'

// Vue构造函数，此处不用class的原因是因为方便后续给Vue实例混入实例成员
function Vue (options) {
  if (process.env.NODE_ENV !== 'production' &&
    !(this instanceof Vue)
  ) {
    warn('Vue is a constructor and should be called with the `new` keyword')
  }
  // 调用_init()方法
  this._init(options)
}
// 注册vm的_init()方法，初始化vm
initMixin(Vue)
// 注册vm的$data/$props/$set/$delete/$watch
stateMixin(Vue)
// 初始化事件相关方法
// $on/$once/$off/$emit
eventsMixin(Vue)
// 初始化生命周期相关的混入方法
// _update/$forceUpdate/$destroy
lifecycleMixin(Vue)
// 混入render
// $nextTick/_render
renderMixin(Vue)

export default Vue
```

- initMixin(Vue)----（src/core/instance/init.js）

  - 初始化`_init()`方法

    ```js
    /* @flow */
    
    import config from '../config'
    import { initProxy } from './proxy'
    import { initState } from './state'
    import { initRender } from './render'
    import { initEvents } from './events'
    import { mark, measure } from '../util/perf'
    import { initLifecycle, callHook } from './lifecycle'
    import { initProvide, initInjections } from './inject'
    import { extend, mergeOptions, formatComponentName } from '../util/index'
    
    let uid = 0
    
    export function initMixin (Vue: Class<Component>) {
      // 给vue的原型挂载init方法
      // 合并options / 初始化操作
      Vue.prototype._init = function (options?: Object) {
        const vm: Component = this
        // a uid
        vm._uid = uid++
    
        let startTag, endTag
        /* istanbul ignore if */
        if (process.env.NODE_ENV !== 'production' && config.performance && mark) {
          startTag = `vue-perf-start:${vm._uid}`
          endTag = `vue-perf-end:${vm._uid}`
          mark(startTag)
        }
    
        // a flag to avoid this being observed
        // 如果是Vue实例则不需要被observe
        vm._isVue = true
        // merge options
        // 合并options
        if (options && options._isComponent) {
          // optimize internal component instantiation
          // since dynamic options merging is pretty slow, and none of the
          // internal component options needs special treatment.
          initInternalComponent(vm, options)
        } else {
          vm.$options = mergeOptions(
            resolveConstructorOptions(vm.constructor),
            options || {},
            vm
          )
        }
        /* istanbul ignore else */
        if (process.env.NODE_ENV !== 'production') {
          initProxy(vm)
        } else {
          vm._renderProxy = vm
        }
        // expose real self
        vm._self = vm
        // Vm
        // vm的生命周期相关变量初始化
        // $children/$parent/$root/$refs
        initLifecycle(vm)
        
        // vm的事件监听初始化，父组件绑定在当前组件的事件
        initEvents(vm)
        
        // vm的编译render初始化
        // $slots/$scopedSlots_c/$createElement/$attrs/$listeners
        initRender(vm)
        
        // beforeCreate生命钩子的回调
        callHook(vm, 'beforeCreate')
        
        // 把inject的成员注入到vm上
        initInjections(vm) // resolve injections before data/props
        
        // 初始化vm的_props/methods/_data/computed/watch
        initState(vm)
        
        // 初始化provide
        initProvide(vm) // resolve provide after data/props
        
        // create生命钩子的回调
        callHook(vm, 'created')
    
        /* istanbul ignore if */
        if (process.env.NODE_ENV !== 'production' && config.performance && mark) {
          vm._name = formatComponentName(vm, false)
          mark(endTag)
          measure(`vue ${vm._name} init`, startTag, endTag)
        }
    
        if (vm.$options.el) {
          vm.$mount(vm.$options.el)
        }
      }
    }
    
    export function initInternalComponent (vm: Component, options: InternalComponentOptions) {
      const opts = vm.$options = Object.create(vm.constructor.options)
      // doing this because it's faster than dynamic enumeration.
      const parentVnode = options._parentVnode
      opts.parent = options.parent
      opts._parentVnode = parentVnode
    
      const vnodeComponentOptions = parentVnode.componentOptions
      opts.propsData = vnodeComponentOptions.propsData
      opts._parentListeners = vnodeComponentOptions.listeners
      opts._renderChildren = vnodeComponentOptions.children
      opts._componentTag = vnodeComponentOptions.tag
    
      if (options.render) {
        opts.render = options.render
        opts.staticRenderFns = options.staticRenderFns
      }
    }
    
    export function resolveConstructorOptions (Ctor: Class<Component>) {
      let options = Ctor.options
      if (Ctor.super) {
        const superOptions = resolveConstructorOptions(Ctor.super)
        const cachedSuperOptions = Ctor.superOptions
        if (superOptions !== cachedSuperOptions) {
          // super option changed,
          // need to resolve new options.
          Ctor.superOptions = superOptions
          // check if there are any late-modified/attached options (#4976)
          const modifiedOptions = resolveModifiedOptions(Ctor)
          // update base extend options
          if (modifiedOptions) {
            extend(Ctor.extendOptions, modifiedOptions)
          }
          options = Ctor.options = mergeOptions(superOptions, Ctor.extendOptions)
          if (options.name) {
            options.components[options.name] = Ctor
          }
        }
      }
      return options
    }
    
    function resolveModifiedOptions (Ctor: Class<Component>): ?Object {
      let modified
      const latest = Ctor.options
      const sealed = Ctor.sealedOptions
      for (const key in latest) {
        if (latest[key] !== sealed[key]) {
          if (!modified) modified = {}
          modified[key] = latest[key]
        }
      }
      return modified
    }
    
    ```

- stateMixin(Vue)

  ![](http://5coder.cn/img/image-20210628060200588.png)

- eventsMixin(Vue)

  ![](http://5coder.cn/img/image-20210628060108441.png)

- lifecycleMixin(Vue)

![](http://5coder.cn/img/image-20210628060417525.png)

- renderMixin(Vue)

![](http://5coder.cn/img/image-20210628060433991.png)

## 首次渲染过程

- Vue初始化完毕，开始真正的执行
- 调用new Vue()之前，已经初始化完毕
- 通过调试代码，记录首次渲染过程

![首次渲染过程](http://5coder.cn/img/首次渲染过程.png)

## 数据响应式原理

参考之前的文章：[模拟Vue.js响应式原理](http://blog.5coder.cn/2021/052627165.html)，文章中自己模拟了响应式原理，实现了简易版的响应式机制，其中的思想与方法与Vue.js源码吻合，可对照查看。

### 通过查看源码解决下面问题

- `vm.msg = { count: 0 }`，重新给属性赋值，是否是响应式的？
- `vm.arr[0] = 4`，给数组元素赋值，视图是否会更新？
- `vm.arr.length = 0`， 修改数组的length，视图是否会更新？
- `vm.arr.push(4)`，视图是否会更新？

### 响应式处理的入口

整个响应式处理的过程是比较复杂的，下面我们先从

- `src/core/instance/init.js`

  - `initState(vm)`vm状态的初始化
  - 初始化了`_data、_props、methods`等

- `src/core/instance/state.js`

  ```js
  // 数据的初始化
  if (opts.data) {
      initData(vm)
  } else {
      observe(vm._data = {}, true /* asRootData */)
  }
  ```

- `initData(vm)` vm数据的初始化

  ```js
  function initData (vm: Component) {
    let data = vm.$options.data
    // 初始化_data,组件中data是函数，调用函数返回结果
    // 否则直接返回data
    data = vm._data = typeof data === 'function'
      ? getData(data, vm)
      : data || {}
    if (!isPlainObject(data)) {
      data = {}
      process.env.NODE_ENV !== 'production' && warn(
        'data functions should return an object:\n' +
        'https://vuejs.org/v2/guide/components.html#data-Must-Be-a-Function',
        vm
      )
    }
    // proxy data on instance
    // 获取data中的所有属性
    const keys = Object.keys(data)
    // 获取props / methods
    const props = vm.$options.props
    const methods = vm.$options.methods
    let i = keys.length
    // 判断data上的成员是否和props/methods重名
    while (i--) {
      const key = keys[i]
      if (process.env.NODE_ENV !== 'production') {
        if (methods && hasOwn(methods, key)) {
          warn(
            `Method "${key}" has already been defined as a data property.`,
            vm
          )
        }
      }
      if (props && hasOwn(props, key)) {
        process.env.NODE_ENV !== 'production' && warn(
          `The data property "${key}" is already declared as a prop. ` +
          `Use prop default value instead.`,
          vm
        )
      } else if (!isReserved(key)) {
        proxy(vm, `_data`, key)
      }
    }
    // observe data
    // 响应式处理
    observe(data, true /* asRootData */)
  }
  ```

- `src/core/observer/index.js`

  - `observe(value, asRootData)`

  - 负责为每一个Object类型的value创建一个`observer`实例

    ```js
    export function observe (value: any, asRootData: ?boolean): Observer | void {  // 判断 value 是否是对象  if (!isObject(value) || value instanceof VNode) {    return  }  let ob: Observer | void  // 如果 value 有 __ob__(observer对象) 属性 结束  if (hasOwn(value, '__ob__') && value.__ob__ instanceof Observer) {    ob = value.__ob__  } else if (    shouldObserve &&    !isServerRendering() &&    (Array.isArray(value) || isPlainObject(value)) &&    Object.isExtensible(value) &&    !value._isVue  ) {    // 创建一个 Observer 对象    ob = new Observer(value)  }  if (asRootData && ob) {    ob.vmCount++  }  return ob}
    ```

### Observer

- `src/core/observer/index.js`

  - 对对象做响应化处理

  - 对数组做响应化处理

    ```js
    export class Observer {  // 观测对象  value: any;  // 依赖对象  dep: Dep;  // 实例计数器  vmCount: number; // number of vms that have this object as root $data  constructor (value: any) {    this.value = value    this.dep = new Dep()    // 初始化实例的 vmCount 为0    this.vmCount = 0    // 将实例挂载到观察对象的 __ob__ 属性    def(value, '__ob__', this)    // 数组的响应式处理    if (Array.isArray(value)) {      if (hasProto) {        protoAugment(value, arrayMethods)      } else {        copyAugment(value, arrayMethods, arrayKeys)      }      // 为数组中的每一个对象创建一个 observer 实例      this.observeArray(value)    } else {      // 遍历对象中的每一个属性，转换成 setter/getter      this.walk(value)    }  }  /**   * Walk through all properties and convert them into   * getter/setters. This method should only be called when   * value type is Object.   */  walk (obj: Object) {    // 获取观察对象的每一个属性    const keys = Object.keys(obj)    // 遍历每一个属性，设置为响应式数据    for (let i = 0; i < keys.length; i++) {      defineReactive(obj, keys[i])    }  }  /**   * Observe a list of Array items.   */  observeArray (items: Array<any>) {    for (let i = 0, l = items.length; i < l; i++) {      observe(items[i])    }  }}
    ```

  - `wakl(obj)`

    - 遍历obj的所有属性，为每一个属性调用`defineReactive()`方法，设置`getter/setter`

### defineReactive()

- `src/core/observer/index.js`
- `defineReactive(obj, key, val, customSetter, shallow)`
  - 为一个对象定义一个响应式的属性，每一个属性对应一个`dep`对象
  - 如果该属性的值是对象，继续调用`observe`
  - 如果给属性赋新值，继续调用`observe`
  - 如果数据更新发送通知

#### 对象响应式处理

```js
/**
 * Define a reactive property on an Object.
 */
export function defineReactive (
  obj: Object,
  key: string,
  val: any,
  customSetter?: ?Function,
  shallow?: boolean
) {
  // 1.为每一个属性，创建依赖对象实例
  const dep = new Dep()
  // 获取obj的属性描述符
  const property = Object.getOwnPropertyDescriptor(obj, key)
  if (property && property.configurable === false) {
    return
  }
  // 提供预定义的存取器函数
  // cater for pre-defined getter/setters
  const getter = property && property.get
  const setter = property && property.set
  if ((!getter || setter) && arguments.length === 2) {
    val = obj[key]
  }
  // 2.判断是否递归观察子对象，并将子对象属性都转换成getter/setter，返回子观察对象
  let childOb = !shallow && observe(val)
  Object.defineProperty(obj, key, {
    enumerable: true,
    configurable: true,
    get: function reactiveGetter () {
      // 如果预定义的getter存在，则value等于getter调用的返回值
      // 否则直接赋予属性值
      const value = getter ? getter.call(obj) : val
      // 如果存在当前依赖目标，即watcher对象，则建立依赖
      if (Dep.target) {
        // dep()添加相互的依赖
        // 一个组件对应一个watcher对象
        // 一个watcher会对应多个dep（要观察的属性很多）
        // 我们可以手动创建多个watcher监听一个属性的变化，一个dep可以对应多个watcher
        dep.depend()
        // 如果子观察对象目标存在，建立子对象的依赖关系
        if (childOb) {
          childOb.dep.depend()
          // 如果属性是数组，则特殊处理收集数组对象依赖
          if (Array.isArray(value)) {
            dependArray(value)
          }
        }
      }
      // 返回属性值
      return value
    },
    set: function reactiveSetter (newVal) {
      // 如果预定义的getter存在则value等于getter调用的返回值
      // 否则直接赋予属性值
      const value = getter ? getter.call(obj) : val
      /* eslint-disable no-self-compare */
      // 如果新值等于旧值或者新旧值为NaN则不执行
      if (newVal === value || (newVal !== newVal && value !== value)) {
        return
      }
      /* eslint-enable no-self-compare */
      if (process.env.NODE_ENV !== 'production' && customSetter) {
        customSetter()
      }
      // 如果没有setter直接返回
      // #7981: for accessor properties without setter
      if (getter && !setter) return
      // 如果预定义setter存在则调用，否则直接更新新值
      if (setter) {
        setter.call(obj, newVal)
      } else {
        val = newVal
      }
      // 3.如果新值是对象，观察子对象并返回子对象的observer对象
      childOb = !shallow && observe(newVal)
      // 4.派发更新（发布更改通知）
      dep.notify()
    }
  })
}
```

#### 数组的响应式处理

- Observer的构造函数中

  ```js
  // 数组的响应式处理
  if (Array.isArray(value)) {
    if (hasProto) {
      protoAugment(value, arrayMethods)
    } else {
      copyAugment(value, arrayMethods, arrayKeys)
    }
    // 为数组中的每一个对象创建一个 observer 实例
    this.observeArray(value)
  } else {
    // 遍历对象中的每一个属性，转换成 setter/getter
    this.walk(value)
  }
  
  
  // helpers
  
  /**
   * Augment a target Object or Array by intercepting
   * the prototype chain using __proto__
   */
  function protoAugment (target, src: Object) {
    /* eslint-disable no-proto */
    target.__proto__ = src
    /* eslint-enable no-proto */
  }
  
  /**
   * Augment a target Object or Array by defining
   * hidden properties.
   */
  /* istanbul ignore next */
  function copyAugment (target: Object, src: Object, keys: Array<string>) {
    for (let i = 0, l = keys.length; i < l; i++) {
      const key = keys[i]
      def(target, key, src[key])
    }
  }
  ```

- 处理数组修改数据的方法

  - `src/core/observer/array.js`

    ```js
    /*
     * not type checking this file because flow doesn't play well with
     * dynamically accessing methods on Array prototype
     */
    
    import { def } from '../util/index'
    
    const arrayProto = Array.prototype
    // 使用数组的原型创建一个新的对象(克隆数组的原型)
    export const arrayMethods = Object.create(arrayProto)
    // 修改数组元素的方法
    const methodsToPatch = [
      'push',
      'pop',
      'shift',
      'unshift',
      'splice',
      'sort',
      'reverse'
    ]
    
    /**
     * Intercept mutating methods and emit events
     */
    methodsToPatch.forEach(function (method) {
      // cache original method
      // 保存数组原方法
      const original = arrayProto[method]
      // 调用Object.defineProperty() 重新定义修改数组的方法
      def(arrayMethods, method, function mutator (...args) {
        // 执行数组的原始方法
        const result = original.apply(this, args)
        // 获取数组对象的ob对象
        const ob = this.__ob__
        let inserted
        switch (method) {
          case 'push':
          case 'unshift':
            inserted = args
            break
          case 'splice':
            inserted = args.slice(2)
            break
        }
        // 对插入的新元素，重新遍历数组元素设置为响应式数据
        if (inserted) ob.observeArray(inserted)
        // notify change
        // 调用了修改数组的方法，调用数组的ob对象发送通知
        ob.dep.notify()
        return result
      })
    })
    
    ```

  - `def`方法

    ```js
    /**
     * Define a property.
     */
    export function def (obj: Object, key: string, val: any, enumerable?: boolean) {
      Object.defineProperty(obj, key, {
        value: val,
        enumerable: !!enumerable,
        writable: true,
        configurable: true
      })
    }
    ```

### Dep类

- src/core/observer/dep.js
- 依赖对象
- 记录watcher对象
- depend() ---- watcher记录对应的dep
- 发布通知

1. 在`defineReactive()`中的`getter`中创建`dep`对象，并判断`Dep.target`是否有值（一会再来看看有什么时候有值得），调用`dep.depend()`
2. `dep.depend()`内部调用`Dep.target.addDep(this)`，也就是`watcher`的`addDep()`方法，它内部最后调用`dep.addSub(this)`，把`watcher`对象，添加到`dep.subs.push(watcher)`中，也就是把订阅者添加到`dep`的`subs`数组中，当数据变化的时候调用`watcher`对象的`update()`方法
3. 什么时候设置的`Dep.target`？通过简单的案例调试观察。调用`mountComponent()`方法的时候，创建了渲染`watcher`对象，执行`watcher`中的`get()`方法
4. `get()`方法内部调用`pushTarget(this)`，把当前`Dep.target = watcher`，同时把当前`watcher`入栈，因为有父子组件嵌套的时候，先把父组件对应的`watcher`入栈，再去处理子组件的`watcher`，子组件的处理完毕后，再把父组件对应的`watcher`出栈，继续操作
5. `Dep.target`用来存放目前正在使用的`watcher`。全局唯一，并且一次也只能有一个`watcher`被使用

```js
/* @flow */

import type Watcher from './watcher'
import { remove } from '../util/index'
import config from '../config'

let uid = 0
// dep 是个可观察对象，可以有多个指令订阅它
/**
 * A dep is an observable that can have multiple
 * directives subscribing to it.
 */
export default class Dep {
  // 静态属性，watcher 对象
  static target: ?Watcher;
  // dep 实例 Id
  id: number;
  // dep 实例对应的 watcher 对象/订阅者数组
  subs: Array<Watcher>;

  constructor () {
    this.id = uid++
    this.subs = []
  }

  // 添加新的订阅者 watcher 对象
  addSub (sub: Watcher) {
    this.subs.push(sub)
  }

  // 移除订阅者
  removeSub (sub: Watcher) {
    remove(this.subs, sub)
  }

  // 将观察对象和 watcher 建立依赖
  depend () {
    if (Dep.target) {
      // 如果 target 存在，把 dep 对象添加到 watcher 的依赖中
      Dep.target.addDep(this)
    }
  }

  // 发布通知
  notify () {
    // stabilize the subscriber list first
    const subs = this.subs.slice()
    if (process.env.NODE_ENV !== 'production' && !config.async) {
      // subs aren't sorted in scheduler if not running async
      // we need to sort them now to make sure they fire in correct
      // order
      subs.sort((a, b) => a.id - b.id)
    }
    // 调用每个订阅者的update方法实现更新
    for (let i = 0, l = subs.length; i < l; i++) {
      subs[i].update()
    }
  }
}
// Dep.target 用来存放目前正在使用的watcher
// 全局唯一，并且一次也只能有一个watcher被使用
// The current target watcher being evaluated.
// This is globally unique because only one watcher
// can be evaluated at a time.
Dep.target = null
const targetStack = []
// 入栈并将当前 watcher 赋值给 Dep.target
// 父子组件嵌套的时候先把父组件对应的 watcher 入栈，
// 再去处理子组件的 watcher，子组件的处理完毕后，再把父组件对应的 watcher 出栈，继续操作
export function pushTarget (target: ?Watcher) {
  targetStack.push(target)
  Dep.target = target
}

export function popTarget () {
  // 出栈操作
  targetStack.pop()
  Dep.target = targetStack[targetStack.length - 1]
}

```

### Watcher类

- Watcher分为三种，`Comouted Watcher`、用户`Watcher`（侦听器）、**渲染`Watcher`**

- 渲染`Watcher`的创建时机

  - `src/core/instance/lifecycle.js`

    ```js
    export function mountComponent (
      vm: Component,
      el: ?Element,
      hydrating?: boolean
    ): Component {
      vm.$el = el
      if (!vm.$options.render) {
        vm.$options.render = createEmptyVNode
        if (process.env.NODE_ENV !== 'production') {
          /* istanbul ignore if */
          if ((vm.$options.template && vm.$options.template.charAt(0) !== '#') ||
            vm.$options.el || el) {
            warn(
              'You are using the runtime-only build of Vue where the template ' +
              'compiler is not available. Either pre-compile the templates into ' +
              'render functions, or use the compiler-included build.',
              vm
            )
          } else {
            warn(
              'Failed to mount component: template or render function not defined.',
              vm
            )
          }
        }
      }
      callHook(vm, 'beforeMount')
    
      let updateComponent
      /* istanbul ignore if */
      if (process.env.NODE_ENV !== 'production' && config.performance && mark) {
        updateComponent = () => {
          const name = vm._name
          const id = vm._uid
          const startTag = `vue-perf-start:${id}`
          const endTag = `vue-perf-end:${id}`
    
          mark(startTag)
          const vnode = vm._render()
          mark(endTag)
          measure(`vue ${name} render`, startTag, endTag)
    
          mark(startTag)
          vm._update(vnode, hydrating)
          mark(endTag)
          measure(`vue ${name} patch`, startTag, endTag)
        }
      } else {
        updateComponent = () => {
          vm._update(vm._render(), hydrating)
        }
      }
    	// 创建渲染Watcher，exOrFn为updateComponent
      // we set this to vm._watcher inside the watcher's constructor
      // since the watcher's initial patch may call $forceUpdate (e.g. inside child
      // component's mounted hook), which relies on vm._watcher being already defined
      new Watcher(vm, updateComponent, noop, {
        before () {
          if (vm._isMounted && !vm._isDestroyed) {
            callHook(vm, 'beforeUpdate')
          }
        }
      }, true /* isRenderWatcher */)
      hydrating = false
    
      // manually mounted instance, call mounted on self
      // mounted is called for render-created child components in its inserted hook
      if (vm.$vnode == null) {
        vm._isMounted = true
        callHook(vm, 'mounted')
      }
      return vm
    }
    ```

- 渲染`watcher`创建的位置：lifecycle.js的`mountComponent`函数中

- `Watcher`的构造函数初始化，处理`exOrFn`（渲染`watcher`和侦听器处理不同，渲染`watcher`为`updateComponent`，对比新旧`vdom`并渲染到页面上）

- 调用`this.get()`，他里面调用`pushTarget()`，然后`this.getter.call(vm,vm)`（对于渲染`watcher`调用`updateComponent`），如果是用户`watcher`会回去属性的值（触发`get`操作）

- 当数据更新时，`dep`中调用`notify()`方法，`notify()`中调用`watcher`的`update()`方法

- `update()`中调用`queueWatcher()`

- `queueWatcher()`是一个核心方法，去除重复操作，调用`flushSchedulerQueue()`刷新队列并执行`watcher`

- `flushSchedulerQueue()`中对`watcher`排序，遍历所有`watcher`，如果有`before`，触发生命周期的钩子函数`beforeUpdate`，执行`wacher.run()`，它内部调用`this.get()`，然后调用`this.cb()`（渲染`wacher`的`cb`是`noop`，侦听器的`function`）

  1. 组件更新的顺序是从父组件到子组件（因为先创建父组件，后创建子组件）
  2. 组件的用户`watcher`在渲染watcher之前运行（因为用户`watcher`（initState）是在渲染`watcher`（mountComponent）之前创建的）
  3. 如果一个组件在父组件执行之前被销毁，那他应该被跳过

- 整个流程结束

### 调试响应式数据执行过程

- 数组响应式处理的核心过程和数组收集依赖的过程

- 当数组的数据改变的时候watcher的执行过程

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>observe</title>
  </head>
  <body>
    <div id="app">
      {{ arr }}
    </div>
  
    <script src="../../dist/vue.js"></script>
    <script>
      const vm = new Vue({
        el: '#app',
        data: {
          arr: [2, 3, 5]
        }
      })
  
      // vm.arr.push(8)
      // vm.arr[0] = 100
      // vm.arr.length = 0
      
    </script>
  </body>
  </html>
  ```

### 回答以下问题

- 检测变化的注意事项

  ```js
  methods: {
    handler() {
      this.obj.count = 555
      this.arr[0] = 1
      this.arr.length = 0
      this.arr.push(4)
    }
  }
  ```

- 转换成响应式数据

  ```js
  methods: {
    handler() {
      this.$set(this.obj, 'count', 555)
      this.$set(this.arr, 0, 1)
      this.arr.splice(0)
    }
  }
  ```

### 数据响应式原理总结

![](http://5coder.cn/img/响应式处理过程.png)

### 动态添加一个响应式属性

> 当我们给一个响应式对象，动态增加一个对象，这个属性是否为响应式？

示例代码

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>set</title>
</head>
<body>
  <div id="app">
    {{ obj.title }}
    <hr>
    {{ obj.name }}
    <hr>
    {{ arr }}
  </div>

  <script src="../../dist/vue.js"></script>
  <script>
    const vm = new Vue({
      el: '#app',
      data: {
        obj: {
          title: 'Hello Vue'
        },
        arr: [1, 2, 3]
      }
    })
  </script>
</body>
</html>
```

![](http://5coder.cn/img/image-20210706052116706.png)

打开浏览器开发者模式，分别键入如下内容：

- `vm.obj.name = 'abc'`

  ![](http://5coder.cn/img/image-20210706052150370.png)

  **可以发现，动态给`obj`增加`name`属性，视图并未更新，说明此时`name`属性不是响应式的**

- `vm.$set(vm.obj, 'name', 'zhangsan')`

  ![](http://5coder.cn/img/image-20210706052431324.png)

  可以使用`vm.$set(vm.obj, 'name', 'zhangsan')`来给响应式对象动态添加响应式属性(或者使用Vue.set())。

  使用vm.$set()方法改变数组的第一个元素的值：`vm.$set(vm.arr, 0, 100)`。vm.$set()[官方文档](https://cn.vuejs.org/v2/api/#vm-set)

  ![](http://5coder.cn/img/image-20210706053012528.png)

  ![](http://5coder.cn/img/image-20210706053024997.png)

  不能给Vue实例或者Vue实例的跟数组对象动态的添加响应式属性。

  ![](http://5coder.cn/img/image-20210706053237085.png)

## 实例方法/数据

### vm.$set

#### 定义位置

- `Vue.set()`

  - global-api/index.js

  ```js
  // 静态方法 set/delete/nextTick
  Vue.set = set
  Vue.delete = del
  Vue.nextTick = nextTick
  ```

- `vm.$set()`

  - instance/index.js

  ```js
  // 注册vm的$data/$props/$set/$delete/$watch
  // instance/state.js
  stateMixin(Vue)
  
  // instance/state.js
  Vue.prototype.$set = set
  Vue.prototype.$delete = del
  ```

#### 源码

- `set()`方法

  - observer/index.js

  ```js
  /**
   * Set a property on an object. Adds the new property and
   * triggers change notification if the property doesn't
   * already exist.
   */
  export function set (target: Array<any> | Object, key: any, val: any): any {
    if (process.env.NODE_ENV !== 'production' &&
      (isUndef(target) || isPrimitive(target))
    ) {
      warn(`Cannot set reactive property on undefined, null, or primitive value: ${(target: any)}`)
    }
    // 判断target是否是数组，key值是否是合法的索引
    if (Array.isArray(target) && isValidArrayIndex(key)) {
      target.length = Math.max(target.length, key)
      // 通过splice对key位置的元素进行替换
      // splice在array.js进行了响应化的处理，此处的splice已经不是原生的splice方法
      target.splice(key, 1, val)
      return val
    }
    // 如果key在对象中已经存在，直接赋值
    if (key in target && !(key in Object.prototype)) {
      target[key] = val
      return val
    }
    // 获取target中的observer对象
    const ob = (target: any).__ob__
    // 如果target是Vue实例或者$data直接返回，如果是$data的话其observe对象中的vmCount为1，否则为0
    if (target._isVue || (ob && ob.vmCount)) {
      process.env.NODE_ENV !== 'production' && warn(
        'Avoid adding reactive properties to a Vue instance or its root $data ' +
        'at runtime - declare it upfront in the data option.'
      )
      return val
    }
    // 如果ob不存在，target不是响应式对象，此时直接赋值即可
    if (!ob) {
      target[key] = val
      return val
    }
    // 把key设置为响应式属性
    defineReactive(ob.value, key, val)
    // 发送通知
    ob.dep.notify()
    return val
  }
  ```

#### 调试

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>set</title>
</head>
<body>
  <div id="app">
    {{ obj.title }}
    <hr>
    {{ obj.name }}
    <hr>
    {{ arr }}
  </div>

  <script src="../../dist/vue.js"></script>
  <script>
    const vm = new Vue({
      el: '#app',
      data: {
        obj: {
          title: 'Hello Vue'
        },
        arr: [1, 2, 3]
      }
    })
  </script>
</body>
</html>
```

> 回顾`defineReactive`中的`childOb`，给每一个响应式对象设置一个**ob**
>
> 调用`$set`的时候，会获取`ob`对象，并通过`ob.dep.notify()`发送通知

### vm.$delete

- 功能

  删除对象的属性。如果对象是响应式的，确保删除能触发更新视图。这个方法主要用于避开Vue不能检测到属性被删除的限制，但是你应该很少会使用它。

  > 注意：目标不能是一个Vue实例或者Vue实例的跟数据对象

- 示例

  ```js
  vm.$delete(vm.obj, 'title')
  ```

#### 定义位置

- `Vue.delete()`

  - global-api/index.js

  ```js
  // 静态方法 set/delete/nextTick
  Vue.set = set
  Vue.delete = del
  Vue.nextTick = nextTick
  ```

- `vm.$delete()`

  - instance/index.js

  ```js
  // 注册 vm 的 $data/$props/$set/$delete/$watch
  stateMixin(Vue)
  
  // instance/state.js
  Vue.prototype.$set = set
  Vue.prototype.$delete = del
  ```

#### 源码

- src/core/observer/index.js

  ```js
  /**
   * Delete a property and trigger change if necessary.
   */
  export function del (target: Array<any> | Object, key: any) {
    if (process.env.NODE_ENV !== 'production' &&
      (isUndef(target) || isPrimitive(target))
    ) {
      warn(`Cannot delete reactive property on undefined, null, or primitive value: ${(target: any)}`)
    }
    // 判断是否是数组，以及key是否合法
    if (Array.isArray(target) && isValidArrayIndex(key)) {
      // 如果是数组通过splice删除
      // splice做过响应式处理
      target.splice(key, 1)
      return
    }
    // 获取target的ob对象
    const ob = (target: any).__ob__
    // target如果是Vue实例或者$data对象，直接返回
    if (target._isVue || (ob && ob.vmCount)) {
      process.env.NODE_ENV !== 'production' && warn(
        'Avoid deleting properties on a Vue instance or its root $data ' +
        '- just set it to null.'
      )
      return
    }
    // 如果target对象没有key属性直接返回，判断依据是：key是否直接属于target属性，而不是继承来的
    // 如果是继承来的或者没有这个属性，直接返回
    if (!hasOwn(target, key)) {
      return
    }
    // 删除属性
    delete target[key]
    if (!ob) {
      return
    }
    // 通过ob发送通知
    ob.dep.notify()
  }
  ```

### vm.$watch

`vm.$watch(expOrFn, callback, [options])`，[官方文档](https://cn.vuejs.org/v2/api/#vm-watch)

- 功能

  观察Vue实例变化的一个表达式或计算属性函数。回调函数得到的参数为新值和旧值。表达式只接受监督的键路径。对于更负责的表达式，用一个函数取代

- 参数

  - expOrFn：要监视的$data中的属性，可以是表达式或函数
  - callback：数据变化后执行的函数
    - 函数：回调函数
    - 对象：具有handler属性(字符串或者函数)，如果该属性为字符串则methods中相应的定义
  - options：可选的选项
    - deep：布尔类型，深度监听
    - immediate：布尔类型，是否立即执行一次回调函数

- 示例1

  ```js
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>watcher</title>
  </head>
  <body>
    <div id="app">
      {{ user.fullName }}
    </div>
  
    <script src="../../dist/vue.js"></script>
    <script>
      const vm = new Vue({
        el: '#app',
        data: {
          user: {
            firstName: '诸葛',
            lastName: '亮',
            fullName: ''
          }
        }
      })
  
      vm.$watch('user',
        function (newValue, oldValue) {
          this.user.fullName = newValue.firstName + ' ' + newValue.lastName
        }
      )
    </script>
  </body>
  </html>
  ```

  打开浏览器，发现并没有立即显示`诸葛亮`，此时需要添加第三个参数options，内容为：`{immediate: true}`，其意味着立即执行。再次刷新页面，发现页面显示了诸葛亮。

  当我们需要监听vm.$data.user.firstName时，发现后续可能还要监听vm.$data.user.lastName，所以此时写多个watch是非常不方便的，此时在options中添加：deep: true，即为深度监听。不但监听user对象的变化，而且监听其内部属性的变化。此时修改firstName，发现视图也会更新。

- 示例2

  ```js
  const vm = new Vue({
    el: '#app',
    data: {
      a: '1',
      b: '2',
      msg: 'Hello Vue',
      user: {
        firstName: '诸葛',
        lastName: '亮'
      }
    }
  })
  
  // expOrFn是表达式
  vm.$watch('msg', function (newVal, oldVal) {
    congole.log(newVal)
  })
  vm.$watch('user.firstName', function (newVal, oldVal) {
    congole.log(newVal)
  })
  
  // expOrFn是函数
  vm.$watch(function () {
    return this.a + this.b
  }, function (newVal, oldVal) {
    console.log(newVal)
  })
  
  // deep是true，此时比较消耗性能
  vm.$watch('user', function (newVal, oldVal) {
    console.log(newVal)
  }, {
    deep: true
  })
  
  // immediate是true
  vm.$watch('msg', function (newVal, oldVal) {
    console.log(newVal)
  }, {immediate: true})
  ```

#### 三种类型的Watcher对象

- 没有静态方法，因为$watch方法中要使用vue的实例
- Watcher分三种：计算属性Watcher、用户Watcher(侦听器)、渲染Watcher
- 创建顺序：计算属性Watcher、用户Watcher(侦听器)、渲染Watcher
- vm.$watch()
  - src/core/instance/state.js

#### 源码

```js
Vue.prototype.$watch = function (
  expOrFn: string | Function,
  cb: any,
  options?: Object
): Function {
  // 获取 Vue 实例 this
  const vm: Component = this
  if (isPlainObject(cb)) {
    // 判断如果 cb 是对象执行 createWatcher
    return createWatcher(vm, expOrFn, cb, options)
  }
  options = options || {}
  // 标记为用户 watcher
  options.user = true
  // 创建用户 watcher 对象
  const watcher = new Watcher(vm, expOrFn, cb, options)
  // 判断 immediate 如果为 true
  if (options.immediate) {
    // 立即执行一次 cb 回调，并且把当前值传入
    try {
      cb.call(vm, watcher.value)
    } catch (error) {
      handleError(error, vm, `callback for immediate watcher "${watcher.expression}"`)
    }
  }
  // 返回取消监听的方法
  return function unwatchFn () {
    watcher.teardown()
  }
}
```

#### 调试

- 查看watcher的创建顺序

- 测试代码

  - ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>watcher</title>
    </head>
    <body>
      <div id="app">
        {{ reversedMessage }}
        <hr>
        {{ user.fullName }}
      </div>
    
      <script src="../../dist/vue.js"></script>
      <script>
        const vm = new Vue({
          el: '#app',
          data: {
            message: 'Hello Vue',
            user: {
              firstName: '诸葛',
              lastName: '亮',
              fullName: ''
            }
          },
          computed: {
            reversedMessage: function () {
              return this.message.split('').reverse().join('')
            }
          },
          watch: {
            // 'user.firstName': function (newValue, oldValue) {
            //   this.user.fullName = this.user.firstName + ' ' + this.user.lastName
            // },
            // 'user.lastName': function (newValue, oldValue) {
            //   this.user.fullName = this.user.firstName + ' ' + this.user.lastName
            // },
            'user': {
              handler: function (newValue, oldValue) {
                this.user.fullName = this.user.firstName + ' ' + this.user.lastName
              },
              deep: true,
              immediate: true
            }
          }
        })
      </script>
    </body>
    </html>
    ```

    将断点打在src/core/observer/watcher.js中的watcher构造函数中

  - 计算属性watcher

    ![](http://5coder.cn/img/image-20210707055015275.png)

  - 用户watcher（侦听器）

    ![](http://5coder.cn/img/image-20210707055122029.png)

    ![](http://5coder.cn/img/image-20210707055217763.png)

  - 渲染watcher

    ![](http://5coder.cn/img/image-20210707055333356.png)

    ![](http://5coder.cn/img/image-20210707055459252.png)
    - 查看渲染`watcher`的执行过程
      - 当数据更新，`defineReactive`的`set`方法中调用`dep.notify()`
      - 调用`watcher`的`update()`
      - 调用`ququeWatcher()`，把`watcher`存入队列，如果已经存在，不重复添加
      - 循环调用`flushSchedulerQueue()`
        - 通过nextTick()，在消息循环结束之前时候调用`flushShedulerQueue()`
      - 调用`watcher.run()`
        - 调用`watcher.get()`获取最新值
        - 如果是渲染`wacher`结束
        - 如果 用户`watcher`，调用`this.cb()`

## 异步更新队列-nextTick()

- Vue更新DOM是异步执行的，批量的
  - 在下次DOM更新循环结束之后执行延迟回调。在修改数据之后立即使用这个办法，获取更新后的DOM
- `vm.$nextTick(function() { /* 操作DOM */ }` / `Vue.$nextTick(function () {})`

### vm.$nextTick()代码演示

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>nextTick</title>
</head>
<body>
  <div id="app">
    <p id="p" ref="p1">{{ msg }}</p>
    {{ name }}<br>
    {{ title }}<br>
  </div>
  <script src="../../dist/vue.js"></script>
  <script>
    const vm = new Vue({
      el: '#app',
      data: {
        msg: 'Hello nextTick',
        name: 'Vue.js',
        title: 'Title'
      },
      mounted() {
        this.msg = 'Hello World'
        this.name = 'Hello snabbdom'
        this.title = 'Vue.js'
  
        Vue.nextTick(() => {
          console.log(this.$refs.p1.textContent)
        })
      }
    })

    
  </script>
</body>
</html>
```

### vm.$nextTick()代码演示

### 定义位置

- src/core/instance/render.js

```js
Vue.prototype.$nextTick = function (fn: Function) {
  return nextTick(fn. this)
}
```

### 源码

- 手动调用`vm.$nextTick()`
- 在`Watcher`的`queueWatcher`中执行`nextTick()`
- src/core/util/next-tick.js

- $nextTick()实例方法

  ![](http://5coder.cn/img/image-20210707063325418.png)

- $nextTick()静态方法

  ![](http://5coder.cn/img/image-20210707063356290.png)

```js
export function nextTick (cb?: Function, ctx?: Object) {
  let _resolve
  // 把 cb 加上异常处理存入 callbacks 数组中
  callbacks.push(() => {
    if (cb) {
      try {
        // 调用 cb()
        cb.call(ctx)
      } catch (e) {
        handleError(e, ctx, 'nextTick')
      }
    } else if (_resolve) {
      _resolve(ctx)
    }
  })
  if (!pending) {
    pending = true
    // 调用
    timerFunc()
  }
  // $flow-disable-line
  if (!cb && typeof Promise !== 'undefined') {
    // 返回 promise 对象
    return new Promise(resolve => {
      _resolve = resolve
    })
  }
}
```

- timerFunc()

```js
/* @flow */
/* globals MutationObserver */

import { noop } from 'shared/util'
import { handleError } from './error'
import { isIE, isIOS, isNative } from './env'

export let isUsingMicroTask = false

const callbacks = []
let pending = false

function flushCallbacks () {
  pending = false
  const copies = callbacks.slice(0)
  callbacks.length = 0
  for (let i = 0; i < copies.length; i++) {
    copies[i]()
  }
}

// Here we have async deferring wrappers using microtasks.
// In 2.5 we used (macro) tasks (in combination with microtasks).
// However, it has subtle problems when state is changed right before repaint
// (e.g. #6813, out-in transitions).
// Also, using (macro) tasks in event handler would cause some weird behaviors
// that cannot be circumvented (e.g. #7109, #7153, #7546, #7834, #8109).
// So we now use microtasks everywhere, again.
// A major drawback of this tradeoff is that there are some scenarios
// where microtasks have too high a priority and fire in between supposedly
// sequential events (e.g. #4521, #6690, which have workarounds)
// or even between bubbling of the same event (#6566).
let timerFunc

// The nextTick behavior leverages the microtask queue, which can be accessed
// via either native Promise.then or MutationObserver.
// MutationObserver has wider support, however it is seriously bugged in
// UIWebView in iOS >= 9.3.3 when triggered in touch event handlers. It
// completely stops working after triggering a few times... so, if native
// Promise is available, we will use it:
/* istanbul ignore next, $flow-disable-line */
if (typeof Promise !== 'undefined' && isNative(Promise)) {
  const p = Promise.resolve()
  timerFunc = () => {
    p.then(flushCallbacks)
    // In problematic UIWebViews, Promise.then doesn't completely break, but
    // it can get stuck in a weird state where callbacks are pushed into the
    // microtask queue but the queue isn't being flushed, until the browser
    // needs to do some other work, e.g. handle a timer. Therefore we can
    // "force" the microtask queue to be flushed by adding an empty timer.
    if (isIOS) setTimeout(noop)
  }
  isUsingMicroTask = true
} else if (!isIE && typeof MutationObserver !== 'undefined' && (
  isNative(MutationObserver) ||
  // PhantomJS and iOS 7.x
  MutationObserver.toString() === '[object MutationObserverConstructor]'
)) {
  // Use MutationObserver where native Promise is not available,
  // e.g. PhantomJS, iOS7, Android 4.4
  // (#6466 MutationObserver is unreliable in IE11)
  let counter = 1
  const observer = new MutationObserver(flushCallbacks)
  const textNode = document.createTextNode(String(counter))
  observer.observe(textNode, {
    characterData: true
  })
  timerFunc = () => {
    counter = (counter + 1) % 2
    textNode.data = String(counter)
  }
  isUsingMicroTask = true
} else if (typeof setImmediate !== 'undefined' && isNative(setImmediate)) {
  // Fallback to setImmediate.
  // Technically it leverages the (macro) task queue,
  // but it is still a better choice than setTimeout.
  timerFunc = () => {
    setImmediate(flushCallbacks)
  }
} else {
  // Fallback to setTimeout.
  timerFunc = () => {
    setTimeout(flushCallbacks, 0)
  }
}

export function nextTick (cb?: Function, ctx?: Object) {
  let _resolve
  // 把 cb 加上异常处理存入 callbacks 数组中
  callbacks.push(() => {
    if (cb) {
      try {
        // 调用 cb()
        cb.call(ctx)
      } catch (e) {
        handleError(e, ctx, 'nextTick')
      }
    } else if (_resolve) {
      _resolve(ctx)
    }
  })
  if (!pending) {
    pending = true
    // 调用
    timerFunc()
  }
  // $flow-disable-line
  if (!cb && typeof Promise !== 'undefined') {
    // 返回 promise 对象
    return new Promise(resolve => {
      _resolve = resolve
    })
  }
}
```

