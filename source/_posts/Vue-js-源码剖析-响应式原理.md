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
cover:
---

# Vue源码解析-响应式原理

## 课程目标

- Vue.js的静态成员和实例成员初始化过程
  - `vue.use()`、`vue.set()`、vue.extened()等这些全局成员的创建过程
  - vm.$el、`vm.$data`、vm.$on、`vm.$mount`等这些实例成员的创建过程
- 首次渲染的过程
  - 创建完vue实例，并把数据传递给vue之后，vue内部是如何把数据渲染到页面的，后续在分析源码过程中都是基于这个过程的
- **数据响应式原理（核心）**
  - 

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

    ![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210621215220709.png)

##### 调试

- examples的实例中引入的是vue.min.js，将其改为vue.js

- 打开Chrome的调试工具中的source

  ![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210621215534350.png)

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

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210621232639624.png)

将vue版本改为`vue.runtime.js`，发现浏览器报错，提示更改为render函数或者用compiler-included build。

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210621232855357.png)

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

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210621233125601.png)

#### 使用vue-cli创建项目时查看vue构件版本

在使用`vue create projectName`创建的项目中，查看`vue`的构建版本。由于Vue对`webpack.config.js`进行了深度封装，所以在目录中无法看到其配置文件，但是Vue提供了命令行来查看配置文件。

```bash
vue inspect  # 直接输出到控制台
vue inspect > output.js  # 将执行vue inspect命令后的结果输出到output.js文件中
```

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210622055014013.png)

> output.js不是一个有效的`webpack`配置文件，不能拿来直接使用。

可以看到在`resolve`中的`alias`中，vue-cli使用了`vue.runtime.esm.js`（运行时版本，模块化为ES Module）作为构建版本，`vue$`中的`$`符号为精确匹配，在使用时直接使用`import Vue from vue`。

> runtime+compiler与runtime对比（ast：抽象语法树），由下面过程可见runtime-only性能更高。
>
> - **runtime+compiler**
>   - `template -> ast -> render -> vdom ->UI`
> - **runtime-only**
>   - `render -> vdom -> UI`
>
> ![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210622060735123.png)
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

## Vue的初始化

## 首次渲染过程

## 数据响应式原理

## 实例方法/数据

## 异步更新队列-nextTick

