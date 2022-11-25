---
title: 搭建自己的SSR
author: 5coder
tags: Vue SSR
category: 大前端
abbrlink: 27646
date: 2022-11-25 23:22:27
password:
keywords:
top:
cover:
---

## Vue SSR介绍

### 是什么

- 官方文档：https://ssr.vuejs.org/ 
- Vue SSR（Vue.js Server-Side Rendering） 是 Vue.js 官方提供的一个服务端渲染（同构应用）解 决方案 
- 使用它可以构建同构应用 
- 还是基于原有的 Vue.js 技术栈

> 官方文档的解释：Vue.js 是构建客户端应用程序的框架。默认情况下，可以在浏览器中输出 Vue 组件，进行生成 DOM 和操作 DOM。然而，也可以将同一个组件渲染为服务器端的 HTML 字符 串，将它们直接发送到浏览器，最后将这些静态标记"激活"为客户端上完全可交互的应用程序。 服务器渲染的 Vue.js 应用程序也可以被认为是"同构"或"通用"，因为应用程序的大部分代码都可 以在服务器和客户端上运行。

### 使用场景

在对你的应用程序使用服务器端渲染 (SSR) 之前，你应该问的第一个问题是，是否真的需要它。

技术层面：

- 更快的首屏渲染速度
- 更好的 SEO

业务层面：

- 不适合管理系统
- 适合门户资讯类网站，例如企业官网、知乎、简书等
- 适合移动网站

### 如何实现Vue SSR

（1）基于 Vue SSR 官方文档提供的解决方案 

官方方案具有更直接的控制应用程序的结构，更深入底层，更加灵活，同时在使用官方方案的过程中， 也会对Vue SSR有更加深入的了解。

该方式需要你熟悉 Vue.js 本身，并且具有 Node.js 和 webpack 的相当不错的应用经验。

（2）Nuxt.js 开发框架

NUXT提供了平滑的开箱即用的体验，它建立在同等的Vue技术栈之上，但抽象出很多模板，并提供了 一些额外的功能，例如静态站点生成。通过 Nuxt.js 可以快速的使用 Vue SSR 构建同构应用。

## 1.渲染一个Vue实例

接下来我们以 Vue SSR 的官方文档为参考，来学习一下它的基本用法。

> 目标： 
>
> - 了解如何使用 VueSSR 将一个 Vue 实例渲染为 HTML 字符串

首先我们来学习一下服务端渲染中最基础的工作：模板渲染。 说白了就是如何在服务端使用 Vue 的方式解析替换字符串。 在它的官方文档中其实已经给出了示例代码，下面我们来把这个案例的实现过程以及其中含义演示一 下。

```bash
mkdir my-vue-ssr
cd my-vue-ssr
npm init -y
npm install vue vue-server-renderer nodemon
```

`my-vue-ssr/server.js ：`

```js
const Vue = require('vue')

const renderer = require('vue-server-renderer').createRenderer()

const app = new Vue({
  template: `
  <div id="app">
    <h1>{{ message }}</h1>
  </div>
  `,
  data: {
    message: '5coder前端开发'
  }
})

renderer.renderToString(app, (err, html) => {
  if (err) throw err
  console.log(html)
})
```

命令行运行：`nodemon server.js`后，可以看到模板已经被渲染为字符串。

![](http://5coder.cn/img/1668992402_250439c795ade624f34d472f92efdc31.png)

## 2.结合到Web服务中

使用express框架来实现web服务器，`yarn add express`。

server.js

```js
/**
 *@date:2022/11/21
 *@Description:server
 */

const Vue = require('vue')
const express = require('express')

const renderer = require('vue-server-renderer').createRenderer()

const server = express()

server.get('/', (req, res) => {
  const app = new Vue({
    template: `
    <div id="app">
      <h1>{{ message }}</h1>
    </div>
  `,
    data: {
      message: '5coder前端开发'
    }
  })

  renderer.renderToString(app, (err, html) => {
    if (err) {
      return res.status(500).end('Internal Server Error')
    }
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    res.end(`
    <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>Title</title>
      </head>
      <body>
         ${html}
      </body>
      </html>
    `)
  })

})

server.listen(3000, () => {
  console.log('Server Running at port 3000...')
})
```

![](http://5coder.cn/img/1668992955_b3b4b7dc77070ae56d89a77f587685c1.png)

## 3.使用HTML模板

对于页面的模板，还有一种做法，就是将其放到单独的文件中。新建`index.template.html`文件，并设置特殊注释`vue-ssr-outlet`。在render中添加template参数。

`index.template.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>
<!--本段注释，使用render渲染页面，会将下面注释当做模板来使用，具体渲染内容会替换下面注释-->
<!--vue-ssr-outlet-->
</body>
</html>

```

`server.js`

```js
/**
 *@date:2022/11/21
 *@Description:server
 */

const Vue = require('vue')
const express = require('express')
const fs = require('fs')

// 传递读取到的index.template.html模板文件流
const renderer = require('vue-server-renderer').createRenderer({
  template: fs.readFileSync('./index.template.html', 'utf-8'),
})  

const server = express()

server.get('/', (req, res) => {
  const app = new Vue({
    template: `
    <div id="app">
      <h1>{{ message }}</h1>
    </div>
  `,
    data: {
      message: '5coder前端开发'
    }
  })

  renderer.renderToString(app, (err, html) => {
    if (err) {
      return res.status(500).end('Internal Server Error')
    }
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    // 直接返回html，返回的html会替代index.template.html中的注释内容
    res.end(html)
  })

})

server.listen(3000, () => {
  console.log('Server Running at port 3000...')
})
```

![](http://5coder.cn/img/1669012778_99c24a2fa21e5898c1fdc1fd16328e27.png)

## 4.在模板中使用外部数据

页面模板也可以使用外部数据。在renderToString方法中，传递第二个可选参数`{title: '5coder'}`。在页面模板中使用时，使用模板语法`{{ title }}`进行使用。需要注意如果需要渲染一段HTML字符串，需要使用`{{{ html_str }}}`三个括号。

`server.js`

```js
/**
 *@date:2022/11/21
 *@Description:server
 */

const Vue = require('vue')
const express = require('express')
const fs = require('fs')

const renderer = require('vue-server-renderer').createRenderer({
  template: fs.readFileSync('./index.template.html', 'utf-8'),
})

const server = express()

server.get('/', (req, res) => {
  const app = new Vue({
    template: `
    <div id="app">
      <h1>{{ message }}</h1>
    </div>
  `,
    data: {
      message: '5coder前端开发'
    }
  })

  renderer.renderToString(app, {
    title: '5coder',
    content: `
      <h1 style="color: orangered">我是5coder，一个前端开发</h1>
    `
  },(err, html) => {
    if (err) {
      return res.status(500).end('Internal Server Error')
    }
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    res.end(html)
  })

})

server.listen(3000, () => {
  console.log('Server Running at port 3000...')
})
```

`index.template.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
</head>
<body>
<!--本段注释，使用render渲染页面，会将下面注释当做模板来使用，具体渲染内容会替换下面注释-->
<!--vue-ssr-outlet-->
{{{ content }}}
</body>
</html>
```

![](http://5coder.cn/img/1669013297_17203c3a674b2c8270966a9cd1b99fda.png)

## 5.构建配置-基本思路

服务端渲染只是把`vue`实例处理成纯静态的`HTML`字符串，发送给客户端，对于vue实例来说，这种需要客户护短动态交互的功能，其并没有提供。

![](http://5coder.cn/img/1669013742_46f1cd652ca0a30e59bc7426ba346cc6.png)

![](http://5coder.cn/img/1669013785_ee65521cee395282396bd9e6df1ca2cf.png)

到目前为止，我们还没有讨论过如何将相同的 Vue 应用程序提供给客户端。为了做到这一点，我们需要使用 webpack 来打包我们的 Vue 应用程序。事实上，我们可能需要在服务器上使用 webpack 打包 Vue 应用程序，因为：

- 通常 Vue 应用程序是由 webpack 和 `vue-loader` 构建，并且许多 webpack 特定功能不能直接在 Node.js 中运行（例如通过 `file-loader` 导入文件，通过 `css-loader` 导入 CSS）。
- 尽管 Node.js 最新版本能够完全支持 ES2015 特性，我们还是需要转译客户端代码以适应老版浏览器。这也会涉及到构建步骤。

所以基本看法是，对于客户端应用程序和服务器应用程序，我们都要使用 webpack 打包 - 服务器需要「服务器 bundle」然后用于服务器端渲染(SSR)，而「客户端 bundle」会发送给浏览器，用于混合静态标记。

![](http://5coder.cn/img/1669013898_c8665e2f705d48b4ddcfbe8b21677b70.png)

我们将在后面的章节讨论规划结构的细节 - 现在，先假设我们已经将构建过程的规划都弄清楚了，我们可以在启用 webpack 的情况下编写我们的 Vue 应用程序代码。

## 6.构建配置-源码结构

我们需要使用 webpack 来打包我们的 Vue 应用程序。事实上，我们可能需要在服务器上使用 webpack 打包 Vue 应用程序，因为：

- 通常 Vue 应用程序是由 webpack 和 vue-loader 构建，并且许多 webpack 特定功能不能直接在 Node.js 中运行（例如通过 file-loader 导入文件，通过 css-loader 导入 CSS）。
- 尽管 Node.js 最新版本能够完全支持 ES2015 特性，我们还是需要转译客户端代码以适应老版浏览 器。这也会涉及到构建步骤。

所以基本看法是，对于客户端应用程序和服务器应用程序，我们都要使用 webpack 打包 - 服务器需要 「服务器 bundle」然后用于服务器端渲染(SSR)，而「客户端 bundle」会发送给浏览器，用于混合静 态标记。 

现在我们正在使用 webpack 来处理服务器和客户端的应用程序，大部分源码可以使用通用方式编写， 可以使用 webpack 支持的所有功能。同时，在编写通用代码时，有一些事项要牢记在心。 一个基本项目可能像是这样：

![](http://5coder.cn/img/1669017535_0f617123cc41b18e71e6fad5727486ed.png)

```sh
src
├── components
│ ├── Foo.vue
│ ├── Bar.vue
│ └── Baz.vue
├── App.vue
├── app.js # 通用 entry(universal entry)
├── entry-client.js # 仅运行于浏览器
└── entry-server.js # 仅运行于服务器
```

`App.vue`

```vue
<!-- 客户端渲染的入口节点 -->
<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <h2>客户端动态交互</h2>
    <div>
      <input v-model="message">
    </div>
    <div>
      <button @click="onClick">点击测试</button>
    </div>
  </div>
</template>
<script>
export default {
  name: 'App',
  data() {
    return {
      message: '拉钩教育'
    }
  },
  methods: {
    onClick(){
      console.log('Hello World')
    }
  }
}
</script>
<style>
</style>

```

`app.js`

`app.js` 是我们应用程序的「通用 entry」。在纯客户端应用程序中，我们将在此文件中创建根 Vue 实例，并直接挂载到 DOM。但是，对于服务器端渲染(SSR)，责任转移到纯客户端 entry 文件。`app.js` 简单地使用 export 导出一个 `createApp` 函数：

```js
import Vue from 'vue'
import App from './App.vue'

// 导出一个工厂函数，用于创建新的
// 应用程序、router 和 store 实例
export function createApp () {
  const app = new Vue({
    // 根实例简单的渲染应用程序组件。
    render: h => h(App)
  })
  return { app }
}
```

`entry-client.js`:

客户端 entry 只需创建应用程序，并且将其挂载到 DOM 中：

```js
import { createApp } from './app'

// 客户端特定引导逻辑……

const { app } = createApp()

// 这里假定 App.vue 模板中根元素具有 `id="app"`
app.$mount('#app')
```

`entry-server.js`:

服务器 entry 使用 default export 导出函数，并在每次渲染中重复调用此函数。此时，除了创建和返回应用程序实例之外，它不会做太多事情 - 但是稍后我们将在此执行服务器端路由匹配 (server-side route matching) 和数据预取逻辑 (data pre-fetching logic)。

```js
import { createApp } from './app'

export default context => {
  const { app } = createApp()
  
  // 服务端的路由处理、数据预取
  
  return app
}

```

截止目前，以上代码还不能运行，原因是需要进行webpack打包后才可以正常使用。

## 7.构建配置-安装依赖

安装依赖

### （1）安装生产依赖

```shell
npm i vue vue-server-renderer express cross-env
```

| 包                  | 说明                                  |
| ------------------- | ------------------------------------- |
| vue                 | Vue.js 核心库                         |
| vue-server-renderer | Vue 服务端渲染工具                    |
| express             | 基于 Node 的 Web 服务框架             |
| cross-env           | 通过 `npm scripts` 设置跨平台环境变量 |

### （2）安装开发依赖

```shell
npm i -D webpack webpack-cli webpack-merge webpack-node-externals @babel/core
@babel/plugin-transform-runtime @babel/preset-env babel-loader css-loader urlloader file-loader rimraf vue-loader vue-template-compiler friendly-errorswebpack-plugin
```

| 包                                                           | 说明                                 |
| ------------------------------------------------------------ | ------------------------------------ |
| webpack                                                      | webpack核心包                        |
| webpack-cli                                                  | webpack的命令行工具                  |
| webpack-merge                                                | webpack配置信息合并工具              |
| webpack-node-externals                                       | 排除webpack中的Node模块              |
| rimraf                                                       | 基于Node封装的一个跨平台`rm -rf`工具 |
| friendly-errors-webpack-plugin                               | 友好的 webpack 错误提示              |
| @babel/core <br />@babel/plugin-transform-runtime <br />@babel/preset-env <br />babel-loader | Babel 相关工具                       |
| vue-loader <br />vue-template-compiler                       | 处理 .vue 资源                       |
| file-loader                                                  | 处理字体资源                         |
| css-loader                                                   | 处理 CSS 资源                        |
| url-loader                                                   | 处理图片资源                         |

## 8.构建配置-webpack配置文件

配置文件及打包命令 

### （1）初始化 webpack 打包配置文件

```sh
build
├── webpack.base.config.js # 公共配置
├── webpack.client.config.js # 客户端打包配置文件
└── webpack.server.config.js # 服务端打包配置文件
```

> 相关webpack配置可以查看文章[Webpack 4](http://doc.5coder.cn/doc/60/) 和[Webpack 5](http://doc.5coder.cn/doc/61/)

`webpack.base.config.js`

```js
/**
 * 公共配置
 */
const VueLoaderPlugin = require('vue-loader/lib/plugin')  // 处理.vue资源的插件
const path = require('path')
const FriendlyErrorsWebpackPlugin = require('friendly-errors-webpack-plugin')  // 友好的webpack日志输出
const resolve = file => path.resolve(__dirname, file)

const isProd = process.env.NODE_ENV === 'production'  // 环境变量中的env

module.exports = {
  mode: isProd ? 'production' : 'development',
  output: {
    path: resolve('../dist/'),  // 输出目录
    publicPath: '/dist/',  // 设定打包结果文件的请求路径前缀
    filename: '[name].[chunkhash].js'
  },
  resolve: {
    alias: {
      // 路径别名，@ 指向 src
      '@': resolve('../src/')
    },
    // 可以省略的扩展名
    // 当省略扩展名的时候，按照从前往后的顺序依次解析
    extensions: ['.js', '.vue', '.json']
  },
  devtool: isProd ? 'source-map' : 'cheap-module-eval-source-map',
  module: {
    rules: [
      // 处理图片资源
      {
        test: /\.(png|jpg|gif)$/i,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 8192,
            },
          },
        ],
      },

      // 处理字体资源
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: [
          'file-loader',
        ],
      },

      // 处理 .vue 资源
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },

      // 处理 CSS 资源
      // 它会应用到普通的 `.css` 文件
      // 以及 `.vue` 文件中的 `<style>` 块
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ]
      },

      // CSS 预处理器，参考：https://vue-loader.vuejs.org/zh/guide/pre-processors.html
      // 例如处理 Less 资源
      // {
      //   test: /\.less$/,
      //   use: [
      //     'vue-style-loader',
      //     'css-loader',
      //     'less-loader'
      //   ]
      // },
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
    new FriendlyErrorsWebpackPlugin()
  ]
}
```

`webpack.client.config.js`

```js
/**
 * 客户端打包配置
 */
const { merge } = require('webpack-merge')
const baseConfig = require('./webpack.base.config.js')
const VueSSRClientPlugin = require('vue-server-renderer/client-plugin')

module.exports = merge(baseConfig, {
  entry: {
    app: './src/entry-client.js'  // 相对于执行打包所处的目录
  },

  module: {
    rules: [
      // ES6 转 ES5，只需要在客户端做处理，因为服务端的nodeJS本身是支持ES6的
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            cacheDirectory: true,
            plugins: ['@babel/plugin-transform-runtime']
          }
        }
      },
    ]
  },

  // 重要信息：这将 webpack 运行时分离到一个引导 chunk 中，
  // 以便可以在之后正确注入异步 chunk。
  optimization: {
    splitChunks: {
      name: "manifest",
      minChunks: Infinity
    }
  },

  plugins: [
    // 此插件在输出目录中生成 `vue-ssr-client-manifest.json`。
    new VueSSRClientPlugin()
  ]
})

```

`webpack.server.config.js`

```js
/**
 * 服务端打包配置
 */
const { merge } = require('webpack-merge')
const nodeExternals = require('webpack-node-externals')
const baseConfig = require('./webpack.base.config.js')
const VueSSRServerPlugin = require('vue-server-renderer/server-plugin')

module.exports = merge(baseConfig, {
  // 将 entry 指向应用程序的 server entry 文件
  entry: './src/entry-server.js',

  // 这允许 webpack 以 Node 适用方式处理模块加载
  // 并且还会在编译 Vue 组件时，
  // 告知 `vue-loader` 输送面向服务器代码(server-oriented code)。
  target: 'node',

  output: {
    filename: 'server-bundle.js',
    // 此处告知 server bundle 使用 Node 风格导出模块(Node-style exports)
    libraryTarget: 'commonjs2'
  },

  // 不打包 node_modules 第三方包，而是保留 require 方式直接加载
  externals: [nodeExternals({
    // 白名单中的资源依然正常打包
    allowlist: [/\.css$/]
  })],

  plugins: [
    // 这是将服务器的整个输出构建为单个 JSON 文件的插件。
    // 默认文件名为 `vue-ssr-server-bundle.json`
    new VueSSRServerPlugin()
  ]
})

```

## 9.构建配置-配置构建命令

在package.json中配置scripts命令

```json
  "scripts": {
    "build:client": "cross-env NODE_ENV=production webpack --config build/webpack.client.config.js",
    "build:server": "cross-env NODE_ENV=production webpack --config build/webpack.server.config.js",
    "build": "rimraf dist && npm run build:client && npm run build:server",
  },
```

运行测试：

```shell
yarn build:client
```

![](http://5coder.cn/img/1669018794_13ae3ebdc82e21f192d6523fda387684.png)

```shell
yarn build:server
```

![](http://5coder.cn/img/1669018944_98d7dc354f78f493070c0438ad081c28.png)

```shell
yarn build
```

![](http://5coder.cn/img/1669019010_53d4cfe2b19a669d244fe6410d4b3b5e.png)

## 10.构建配置-启动应用

> # Bundle Renderer 指引
>
> ## 使用基本 SSR 的问题
>
> 到目前为止，我们假设打包的服务器端代码，将由服务器通过 `require` 直接使用：
>
> ```js
> const createApp = require('/path/to/built-server-bundle.js')
> ```
>
> 这是理所应当的，然而在每次编辑过应用程序源代码之后，都必须停止并重启服务。这在开发过程中会影响开发效率。此外，Node.js 本身不支持 source map。
>
> ## 传入 BundleRenderer
>
> `vue-server-renderer` 提供一个名为 `createBundleRenderer` 的 API，用于处理此问题，通过使用 webpack 的自定义插件，server bundle 将生成为可传递到 bundle renderer 的特殊 JSON 文件。所创建的 bundle renderer，用法和普通 renderer 相同，但是 bundle renderer 提供以下优点：
>
> - 内置的 source map 支持（在 webpack 配置中使用 `devtool: 'source-map'`）
> - 在开发环境甚至部署过程中热重载（通过读取更新后的 bundle，然后重新创建 renderer 实例）
> - 关键 CSS(critical CSS) 注入（在使用 `*.vue` 文件时）：自动内联在渲染过程中用到的组件所需的CSS。更多细节请查看 [CSS](https://v2.ssr.vuejs.org/zh/guide/css.html) 章节。
> - 使用 [clientManifest](https://v2.ssr.vuejs.org/zh/api/#clientmanifest) 进行资源注入：自动推断出最佳的预加载(preload)和预取(prefetch)指令，以及初始渲染所需的代码分割 chunk。
>
> ------
>
> 在下一章节中，我们将讨论如何配置 webpack，以生成 bundle renderer 所需的构建工件 (build artifact)，但现在假设我们已经有了这些需要的构建工件，以下就是创建和使用 bundle renderer 的方法：
>
> ```js
> const { createBundleRenderer } = require('vue-server-renderer')
> 
> const renderer = createBundleRenderer(serverBundle, {
>   runInNewContext: false, // 推荐
>   template, // （可选）页面模板
>   clientManifest // （可选）客户端构建 manifest
> })
> 
> // 在服务器处理函数中……
> server.get('*', (req, res) => {
>   const context = { url: req.url }
>   // 这里无需传入一个应用程序，因为在执行 bundle 时已经自动创建过。
>   // 现在我们的服务器与应用程序已经解耦！
>   renderer.renderToString(context, (err, html) => {
>     // 处理异常……
>     res.end(html)
>   })
> })
> ```
>
> bundle renderer 在调用 `renderToString` 时，它将自动执行「由 bundle 创建的应用程序实例」所导出的函数（传入`上下文`作为参数），然后渲染它。
>
> 注意，推荐将 `runInNewContext` 选项设置为 `false` 或 `'once'`。更多细节请查看 [API 参考](https://v2.ssr.vuejs.org/zh/api/#runinnewcontext)。

`server.js`

```js
const Vue = require('vue')
const express = require('express')
const fs = require('fs')

const serverBundle = require('./dist/vue-ssr-server-bundle.json')
const template = fs.readFileSync('./index.template.html', 'utf-8')
const clientManifest = require('./dist/vue-ssr-client-manifest.json')

const render = require('vue-server-renderer').createBundleRenderer(serverBundle, {
  template,
  clientManifest
})

const server = express()
server.get('/', (req, res) => {
  render.renderToString({
    title: '拉钩教育',
    meta: `
    <meta name="description" content="拉钩教育">
    `
  }, (err, html) => {
    if (err) {
      return res.status(500).end("Internal Server Error!")
    }
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    res.end(html)
  })
})

server.listen(3000, () => {
  console.log('Server running at port 3000...')
})

```

此时运行`nodemon server.js`，发现404报错，原因是找不到客户端的bundle文件。因此需要设置`server.use('/dist', express.static('./dist'))`

![](http://5coder.cn/img/1669020214_2b074eb19ed236730a46f3c848cc2a6c.png)

```js
const Vue = require('vue')
const express = require('express')
const fs = require('fs')

const serverBundle = require('./dist/vue-ssr-server-bundle.json')
const template = fs.readFileSync('./index.template.html', 'utf-8')
const clientManifest = require('./dist/vue-ssr-client-manifest.json')

const render = require('vue-server-renderer').createBundleRenderer(serverBundle, {
  template,
  clientManifest
})

const server = express()

server.use('/dist', express.static('./dist'))

server.get('/', (req, res) => {
  render.renderToString({
    title: '拉钩教育',
    meta: `
    <meta name="description" content="拉钩教育">
    `
  }, (err, html) => {
    if (err) {
      return res.status(500).end("Internal Server Error!")
    }
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    res.end(html)
  })
})

server.listen(3000, () => {
  console.log('Server running at port 3000...')
})

```

此时发现，在输入框输入后，上面的标签内容也随之变化。

![](http://5coder.cn/img/1669020398_b7a57dc76a221190a24e5509ba0a911e.png)

## 11.构建配置-解析渲染流程

### （1）服务端渲染

- renderer.renderToString 渲染了什么？ 
- renderer 是如何拿到 entry-server 模块的？ 
  - createBundleRenderer 中的 serverBundle 
- server Bundle 是 Vue SSR 构建的一个特殊的 JSON 文件 
  - entry：入口 
  - files：所有构建结果资源列表 
  - maps：源代码 source map 信息 
- server-bundle.js 就是通过 server.entry.js 构建出来的结果文件 
- 最终把渲染结果注入到模板中

![](http://5coder.cn/img/1669020884_94451f13a45931cb9ebe57fda4d4bd61.png)

### （2）客户端渲染

- vue-ssr-client-manifest.json 
  - publicPath：访问静态资源的根相对路径，与 webpack 配置中的 publicPath 一致 
  - all：打包后的所有静态资源文件路径 
  - initial：页面初始化时需要加载的文件，会在页面加载时配置到 preload 中 
  - async：页面跳转时需要加载的文件，会在页面加载时配置到 prefetch 中 
  - modules：项目的各个模块包含的文件的序号，对应 all 中文件的顺序；moduleIdentifier和 和all数组中文件的映射关系（modules对象是我们查找文件引用的重要数据）

![](http://5coder.cn/img/1669021679_2ca927a36f905d36affd5eeb24e451bf.png)

`app.fb08227f866ec45d060e.js`是如何工作的，参考下面官方文档。

> **客户端激活 (client-side hydration)**
>
> 所谓客户端激活，指的是 Vue 在浏览器端接管由服务端发送的静态 HTML，使其变为由 Vue 管理的动态 DOM 的过程。
>
> 在 `entry-client.js` 中，我们用下面这行挂载(mount)应用程序：
>
> ```js
> // 这里假定 App.vue template 根元素的 `id="app"`
> app.$mount('#app')
> ```
>
> **由于服务器已经渲染好了 HTML，我们显然无需将其丢弃再重新创建所有的 DOM 元素。相反，我们需要"激活"这些静态的 HTML，然后使他们成为动态的（能够响应后续的数据变化）。**
>
> 如果你检查服务器渲染的输出结果，你会注意到应用程序的根元素上添加了一个特殊的属性：
>
> ```html
> <div id="app" data-server-rendered="true">
> ```
>
> `data-server-rendered` 特殊属性，让客户端 Vue 知道这部分 HTML 是由 Vue 在服务端渲染的，并且应该以激活模式进行挂载。注意，这里并没有添加 `id="app"`，而是添加 `data-server-rendered` 属性：你需要自行添加 ID 或其他能够选取到应用程序根元素的选择器，否则应用程序将无法正常激活。
>
> 注意，在没有 `data-server-rendered` 属性的元素上，还可以向 `$mount` 函数的 `hydrating` 参数位置传入 `true`，来强制使用激活模式(hydration)：
>
> ```js
> // 强制使用应用程序的激活模式
> app.$mount('#app', true)
> ```
>
> 在开发模式下，Vue 将推断客户端生成的虚拟 DOM 树 (virtual DOM tree)，是否与从服务器渲染的 DOM 结构 (DOM structure) 匹配。如果无法匹配，它将退出混合模式，丢弃现有的 DOM 并从头开始渲染。**在生产模式下，此检测会被跳过，以避免性能损耗。**
>
> ### 一些需要注意的坑
>
> 使用「SSR + 客户端混合」时，需要了解的一件事是，浏览器可能会更改的一些特殊的 HTML 结构。例如，当你在 Vue 模板中写入：
>
> ```html
> <table>
> <tr><td>hi</td></tr>
> </table>
> ```
>
> 浏览器会在 `<table>` 内部自动注入 `<tbody>`，然而，由于 Vue 生成的虚拟 DOM (virtual DOM) 不包含 `<tbody>`，所以会导致无法匹配。为能够正确匹配，请确保在模板中写入有效的 HTML。

## 12.构建配置开发模式-基本思路

我们现在已经实现同构应用的基本功能了，但是这对于一个完整的应用来说还远远不够，例如如何处理 同构应用中的路由、如何在服务端渲染中进行数据预取等功能。这些功能我们都会去对它进行实现，但 是在实现它们之前我们要先来解决一个关于打包的问题：

- 每次写完代码，都要重新打包构建 
- 重新启动 Web 服务 
- 很麻烦...

所以下面我们来实现项目中的开发模式构建，也就是我们希望能够实现：

- 写完代码，自动构建 
- 自动重启 Web 服务 
- 自动刷新页面内容 
- ...

**基本思路**
生产模式

- npm run build 构建
- node server.js 启动应用

开发模式

- 监视代码变动自动构建，热更新等功能
- node server.js 启动应用

所以我们设计了这样的启动脚本：

```json
"scripts": {
  "build:client": "cross-env NODE_ENV=production webpack --config build/webpack.client.config.js",
  "build:server": "cross-env NODE_ENV=production webpack --config build/webpack.server.config.js",
  "build": "rimraf dist && npm run build:client && npm run build:server",
  "start": "cross-env NODE_ENV=production node server.js",
  "dev": "node server.js"
},
```

服务端配置：

```js
const express = require('express')
const fs = require('fs')
const { createBundleRenderer } = require('vue-server-renderer')
const setupDevServer = require('./build/setup-dev-server')

const server = express()

// express.static 处理的是物理磁盘中的资源文件
server.use('/dist', express.static('./dist'))

const isProd = process.env.NODE_ENV === 'production'

let renderer
let onReady
if (isProd) {
  // 如果是生产模式，直接读取serverBundle、模板文件template、clientManifest，并进行渲染
  const serverBundle = require('./dist/vue-ssr-server-bundle.json')
  const template = fs.readFileSync('./index.template.html', 'utf-8')
  const clientManifest = require('./dist/vue-ssr-client-manifest.json')
  renderer = createBundleRenderer(serverBundle, {
    template,
    clientManifest
  })
} else {
  // 开发模式 -> 监视打包构建 -> 重新生成 Renderer 渲染器
  onReady = setupDevServer(server, (serverBundle, template, clientManifest) => {
    renderer = createBundleRenderer(serverBundle, {
      template,
      clientManifest
    })
  })
}

const render = async (req, res) => {
  try {
    const html = await renderer.renderToString({
      title: '拉勾教育',
      meta: `
        <meta name="description" content="拉勾教育">
      `
    })
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    res.end(html)
  } catch (err) {
    res.status(500).end('Internal Server Error.')
  }
}

// 服务端路由设置为 *，意味着所有的路由都会进入这里
server.get('*', isProd
  ? render
  : async (req, res) => {
    // 等待有了 Renderer 渲染器以后，调用 render 进行渲染
    await onReady
    render(req, res)
  }
)

server.listen(3000, () => {
  console.log('server running at port 3000.')
})

```

## 13.构建配置开发模式-提取处理模块

![](http://5coder.cn/img/1669039605_5cfb25f83c89a364add22ac947859110.png)

## 14.构建配置开发模式-update更新函数

`build/setup-dev-server.js`

```js
const fs = require('fs')
const path = require('path')
const chokidar = require('chokidar')
const webpack = require('webpack')
const devMiddleware = require('webpack-dev-middleware')
const hotMiddleware = require('webpack-hot-middleware')

const resolve = file => path.resolve(__dirname, file)

module.exports = (server, callback) => {
  let ready
  const onReady = new Promise(r => ready = r)

  // 监视构建 -> 更新 Renderer

  let template
  let serverBundle
  let clientManifest

  const update = () => {
    if (template && serverBundle && clientManifest) {
      ready()
      callback(serverBundle, template, clientManifest)
    }
  }

  // 监视构建 template -> 调用 update -> 更新 Renderer 渲染器


  // 监视构建 serverBundle -> 调用 update -> 更新 Renderer 渲染器


  // 监视构建 clientManifest -> 调用 update -> 更新 Renderer 渲染器


  return onReady
}

```

## 15.构建配置开发模式-处理模板文件

关于 Node 中的监视的问题：

- fs.watch
- fs.watchFile
- 第三方包：[chokidar](https://github.com/paulmillr/chokidar)

`build/setup-dev-server.js`

```js
  // 监视构建 template -> 调用 update -> 更新 Renderer 渲染器
  const templatePath = path.resolve(__dirname, '../index.template.html')
  template = fs.readFileSync(templatePath, 'utf-8')
  update()
  // fs.watch、fs.watchFile
  chokidar.watch(templatePath).on('change', () => {
    template = fs.readFileSync(templatePath, 'utf-8')
    update()
  })
```

## 16.构建配置开发模式-服务端监视打包

`build/setup-dev-server.js`

```js
	const resolve = file => path.resolve(__dirname, file)

	...
	// 监视构建 serverBundle -> 调用 update -> 更新 Renderer 渲染器
  const serverConfig = require('./webpack.server.config')
  const serverCompiler = webpack(serverConfig)
  serverCompiler.watch({}, (err, stats) => {
    if (err) throw err
    if (stats.hasErrors()) return
    serverBundle = JSON.parse(
    	fs.readFileSync(resolve('../dist/vue-ssr-server-bundle.json'), 'utf-8')
    )
  })
```

## 17.构建配置开发模式-把数据写入内存中

webpack 默认会把构建结果存储到磁盘中，对于生产模式构建来说是没有问题的；但是我们在开发模式中会频繁的修改代码触发构建，也就意味着要频繁的操作磁盘数据，而磁盘数据操作相对于来说是比较慢的，所以我们有一种更好的方式，就是把数据存储到内存中，这样可以极大的提高构建的速度。[memfs](https://github.com/streamich/memfs) 是一个兼容 Node 中 fs 模块 API 的内存文件系统，通过它我们可以轻松的实现把 webpack 构建结果输出到内存中进行管理。

[webpack-dev-middleware](https://github.com/streamich/memfs) 作用是，以监听模式启动 webpack，将编译结果输出到内存中，然后将内存文件输出到 Express 服务中。

安装依赖：

```shell
npm i -D webpack-dev-middleware
```

`build/setup-dev-server.js`

```js
const devMiddleware = require('webpack-dev-middleware')
	...
	// 监视构建 serverBundle -> 调用 update -> 更新 Renderer 渲染器
  const serverConfig = require('./webpack.server.config')
  const serverCompiler = webpack(serverConfig)
  const serverDevMiddleware = devMiddleware(serverCompiler, {
    logLevel: 'silent' // 关闭日志输出，由 FriendlyErrorsWebpackPlugin 处理
  })
  serverCompiler.hooks.done.tap('server', () => {
    serverBundle = JSON.parse(
      serverDevMiddleware.fileSystem.readFileSync(resolve('../dist/vue-ssr-server-bundle.json'), 'utf-8')
    )
    update()
  })
  ...
```

## 18.构建配置开发模式-客户端构建

`build/setup-dev-server.js`

```js
// 监视构建clientManifest -> 调用update -> 更新Renderer渲染器
const clientConfig = require('./webnpack.client.config')
const clientCompiler = webpack(clientConfig)
const clientDevMiddleware = devMiddleware(clientCompiler, {
  publicPath: clientConfig.output.publicPath,
  logLevel: 'silent'  // 关闭日志输出，由FriendlyErrorsWebpackPlugin处理
})
clientCompiler.hooks.done.tap('client', ()) => {
  clientManifest = JSON.parse(
  	clientDevMiddleware.fileSystem.readFileSync(resolve('../dist/vue-ssr-client-manifest.json'))
  )
  update()
}

// !!!重要，将clientDevMiddleware挂在到Express服务中，提供对其内部内存中数据的访问
```

至此，已经可以使用`yarn dev`进行打包构建，构建过程中可以发现物理磁盘并没生成文件。打开浏览器访问`localhost:3000`,可以看到页面已经正常渲染，并且在输入框中输入内容后，页面也随之变化。

![](http://5coder.cn/img/1669040661_7c8076ad0e0fa0318d441d9c3fd67c27.png)

## 19.构建配置开发模式-热更新

热更新功能需要使用到 [webpack-hot-middleware](https://github.com/webpack-contrib/webpack-hot-middleware) 工具包。

安装依赖：

```shell
npm install --save-dev webpack-hot-middleware
```

工作原理：

- 中间件将自身安装为 webpack 插件，并侦听编译器事件。
- 每个连接的客户端都有一个 Server Sent Events 连接，服务器将在编译器事件上向连接的客户端发布通知。
  - [MDN - 使用服务器发送事件](https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events/Using_server-sent_events)
  - [Server-Sent Events 教程](http://www.ruanyifeng.com/blog/2017/05/server-sent_events.html)
- 当客户端收到消息时，它将检查本地代码是否为最新。如果不是最新版本，它将触发 webpack 热模块重新加载。

`build/setup-dev-server.js`

```js
const hotMiddleware = require('webpack-hot-middleware')
...  
	// 监视构建 clientManifest -> 调用 update -> 更新 Renderer 渲染器
  const clientConfig = require('./webpack.client.config')
  // 热更新插件
  clientConfig.plugins.push(new webpack.HotModuleReplacementPlugin())
  clientConfig.entry.app = [
    'webpack-hot-middleware/client?quiet=true&reload=true', // 和服务端交互，处理热更新一个客户端脚本
    clientConfig.entry.app
  ]
  clientConfig.output.filename = '[name].js' // 热更新模式下确保一致的 hash

  const clientCompiler = webpack(clientConfig)
  const clientDevMiddleware = devMiddleware(clientCompiler, {
    publicPath: clientConfig.output.publicPath,
    logLevel: 'silent' // 关闭日志输出，由 FriendlyErrorsWebpackPlugin 处理
  })
  clientCompiler.hooks.done.tap('client', () => {
    clientManifest = JSON.parse(
      clientDevMiddleware.fileSystem.readFileSync(resolve('../dist/vue-ssr-client-manifest.json'), 'utf-8')
    )
    update()
  })

	// 热更新插件
  server.use(hotMiddleware(clientCompiler, {
    log: false // 关闭它本身的日志输出
  }))

  // 重要！！！将 clientDevMiddleware 挂载到 Express 服务中，提供对其内部内存中数据的访问
  server.use(clientDevMiddleware)
```

![](http://5coder.cn/img/1669041912_8e423e1437268e7ed1d755413e28a1df.png)

综上，完整代码如下：

![](http://5coder.cn/img/1669042325_9874016bb4bd2551af0b2a61435e8bea.png)

`build/setup-dev-server.js`

```js
const fs = require('fs')
const path = require('path')
const chokidar = require('chokidar')
const webpack = require('webpack')
const devMiddleware = require('webpack-dev-middleware')
const hotMiddleware = require('webpack-hot-middleware')

const resolve = file => path.resolve(__dirname, file)

module.exports = (server, callback) => {
  let ready
  const onReady = new Promise(r => ready = r)

  // 监视构建 -> 更新 Renderer

  let template
  let serverBundle
  let clientManifest

  const update = () => {
    if (template && serverBundle && clientManifest) {
      ready()
      callback(serverBundle, template, clientManifest)
    }
  }

  // 监视构建 template -> 调用 update -> 更新 Renderer 渲染器
  const templatePath = path.resolve(__dirname, '../index.template.html')
  template = fs.readFileSync(templatePath, 'utf-8')
  update()
  // fs.watch、fs.watchFile
  chokidar.watch(templatePath).on('change', () => {
    template = fs.readFileSync(templatePath, 'utf-8')
    update()
  })

  // 监视构建 serverBundle -> 调用 update -> 更新 Renderer 渲染器
  const serverConfig = require('./webpack.server.config')
  const serverCompiler = webpack(serverConfig)
  const serverDevMiddleware = devMiddleware(serverCompiler, {
    logLevel: 'silent' // 关闭日志输出，由 FriendlyErrorsWebpackPlugin 处理
  })
  serverCompiler.hooks.done.tap('server', () => {
    serverBundle = JSON.parse(
      serverDevMiddleware.fileSystem.readFileSync(resolve('../dist/vue-ssr-server-bundle.json'), 'utf-8')
    )
    update()
  })

  // 监视构建 clientManifest -> 调用 update -> 更新 Renderer 渲染器
  const clientConfig = require('./webpack.client.config')
  // 热更新插件
  clientConfig.plugins.push(new webpack.HotModuleReplacementPlugin())
  clientConfig.entry.app = [
    'webpack-hot-middleware/client?quiet=true&reload=true', // 和服务端交互，处理热更新一个客户端脚本
    clientConfig.entry.app
  ]


  clientConfig.output.filename = '[name].js' // 热更新模式下确保一致的 hash
  const clientCompiler = webpack(clientConfig)
  const clientDevMiddleware = devMiddleware(clientCompiler, {
    publicPath: clientConfig.output.publicPath,
    logLevel: 'silent' // 关闭日志输出，由 FriendlyErrorsWebpackPlugin 处理
  })
  clientCompiler.hooks.done.tap('client', () => {
    clientManifest = JSON.parse(
      clientDevMiddleware.fileSystem.readFileSync(resolve('../dist/vue-ssr-client-manifest.json'), 'utf-8')
    )
    update()
  })
  server.use(hotMiddleware(clientCompiler, {
    log: false // 关闭它本身的日志输出
  }))

  // 重要！！！将 clientDevMiddleware 挂载到 Express 服务中，提供对其内部内存中数据的访问
  server.use(clientDevMiddleware)

  return onReady
}

```

`build/webpack.base.config.js`

```js
/**
 * 公共配置
 */
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const path = require('path')
const FriendlyErrorsWebpackPlugin = require('friendly-errors-webpack-plugin')
const resolve = file => path.resolve(__dirname, file)

const isProd = process.env.NODE_ENV === 'production'

module.exports = {
  mode: isProd ? 'production' : 'development',
  output: {
    path: resolve('../dist/'),
    publicPath: '/dist/',
    filename: '[name].[chunkhash].js'
  },
  resolve: {
    alias: {
      // 路径别名，@ 指向 src
      '@': resolve('../src/')
    },
    // 可以省略的扩展名
    // 当省略扩展名的时候，按照从前往后的顺序依次解析
    extensions: ['.js', '.vue', '.json']
  },
  devtool: isProd ? 'source-map' : 'cheap-module-eval-source-map',
  module: {
    rules: [
      // 处理图片资源
      {
        test: /\.(png|jpg|gif)$/i,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 8192,
            },
          },
        ],
      },

      // 处理字体资源
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: [
          'file-loader',
        ],
      },

      // 处理 .vue 资源
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },

      // 处理 CSS 资源
      // 它会应用到普通的 `.css` 文件
      // 以及 `.vue` 文件中的 `<style>` 块
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ]
      },
      
      // CSS 预处理器，参考：https://vue-loader.vuejs.org/zh/guide/pre-processors.html
      // 例如处理 Less 资源
      // {
      //   test: /\.less$/,
      //   use: [
      //     'vue-style-loader',
      //     'css-loader',
      //     'less-loader'
      //   ]
      // },
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
    new FriendlyErrorsWebpackPlugin()
  ]
}

```

`build/webpack.client.config.js`

```js
/**
 * 客户端打包配置
 */
const { merge } = require('webpack-merge')
const baseConfig = require('./webpack.base.config.js')
const VueSSRClientPlugin = require('vue-server-renderer/client-plugin')

module.exports = merge(baseConfig, {
  entry: {
    app: './src/entry-client.js'
  },

  module: {
    rules: [
      // ES6 转 ES5
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            cacheDirectory: true,
            plugins: ['@babel/plugin-transform-runtime']
          }
        }
      },
    ]
  },

  // 重要信息：这将 webpack 运行时分离到一个引导 chunk 中，
  // 以便可以在之后正确注入异步 chunk。
  optimization: {
    splitChunks: {
      name: "manifest",
      minChunks: Infinity
    }
  },

  plugins: [
    // 此插件在输出目录中生成 `vue-ssr-client-manifest.json`。
    new VueSSRClientPlugin()
  ]
})

```

`build/webpack.server.config.js`

```js
/**
 * 服务端打包配置
 */
const { merge } = require('webpack-merge')
const nodeExternals = require('webpack-node-externals')
const baseConfig = require('./webpack.base.config.js')
const VueSSRServerPlugin = require('vue-server-renderer/server-plugin')

module.exports = merge(baseConfig, {
  // 将 entry 指向应用程序的 server entry 文件
  entry: './src/entry-server.js',

  // 这允许 webpack 以 Node 适用方式处理模块加载
  // 并且还会在编译 Vue 组件时，
  // 告知 `vue-loader` 输送面向服务器代码(server-oriented code)。
  target: 'node',

  output: {
    filename: 'server-bundle.js',
    // 此处告知 server bundle 使用 Node 风格导出模块(Node-style exports)
    libraryTarget: 'commonjs2'
  },

  // 不打包 node_modules 第三方包，而是保留 require 方式直接加载
  externals: [nodeExternals({
    // 白名单中的资源依然正常打包
    allowlist: [/\.css$/]
  })],

  plugins: [
    // 这是将服务器的整个输出构建为单个 JSON 文件的插件。
    // 默认文件名为 `vue-ssr-server-bundle.json`
    new VueSSRServerPlugin()
  ]
})

```

`server.js`

```js
const express = require('express')
const fs = require('fs')
const { createBundleRenderer } = require('vue-server-renderer')
const setupDevServer = require('./build/setup-dev-server')

const server = express()

server.use('/dist', express.static('./dist'))

const isProd = process.env.NODE_ENV === 'production'

let renderer
let onReady
if (isProd) {
  const serverBundle = require('./dist/vue-ssr-server-bundle.json')
  const template = fs.readFileSync('./index.template.html', 'utf-8')
  const clientManifest = require('./dist/vue-ssr-client-manifest.json')
  renderer = createBundleRenderer(serverBundle, {
    template,
    clientManifest
  })
} else {
  // 开发模式 -> 监视打包构建 -> 重新生成 Renderer 渲染器
  onReady = setupDevServer(server, (serverBundle, template, clientManifest) => {
    renderer = createBundleRenderer(serverBundle, {
      template,
      clientManifest
    })
  })
}

const render = async (req, res) => {
  try {
    const html = await renderer.renderToString({
      title: '拉勾教育',
      meta: `
        <meta name="description" content="拉勾教育">
      `
    })
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    res.end(html)
  } catch (err) {
    res.status(500).end('Internal Server Error.')
  }
}

// 服务端路由设置为 *，意味着所有的路由都会进入这里
server.get('*', isProd
  ? render
  : async (req, res) => {
    // 等待有了 Renderer 渲染器以后，调用 render 进行渲染
    await onReady
    render(req, res)
  }
)

server.listen(3000, () => {
  console.log('server running at port 3000.')
})

```

[完整代码包下载](http://doc.5coder.cn/media/attachment/2022/11/my-vue-ssr.rar)

## 20.编写通用应用注意事项

我们现在终于把实现 Vue SSR 同构应用的基础环境搭建起来了，虽然还有很多不足之处，但是也能满足我们当前的基本使用了。

所以接下来我们就要把内容的核心转移到 Vue SSR 本身上了，那首先我们来了解一下编写通用应用的注意事项，通过了解这些注意事项对于如何正确的使用 Vue SSR 是非常有帮助的。

在这些注意事项中，有些其实已经在前面的学习过程中了解过了，而有些还没有接触过，所以在这里通过官方文档做一个简单的总结。

> **编写通用代码**
>
> 在进一步介绍之前，让我们花点时间来讨论编写"通用"代码时的约束条件 - 即运行在服务器和客户端的代码。由于用例和平台 API 的差异，当运行在不同环境中时，我们的代码将不会完全相同。所以这里我们将会阐述你需要理解的关键事项。
>
> ### 服务器上的数据响应
>
> 在纯客户端应用程序 (client-only app) 中，每个用户会在他们各自的浏览器中使用新的应用程序实例。对于服务器端渲染，我们也希望如此：每个请求应该都是全新的、独立的应用程序实例，以便不会有交叉请求造成的状态污染 (cross-request state pollution)。
>
> 因为实际的渲染过程需要确定性，所以我们也将在服务器上“预取”数据 ("pre-fetching" data) - 这意味着在我们开始渲染时，我们的应用程序就已经解析完成其状态。也就是说，将数据进行响应式的过程在服务器上是多余的，所以默认情况下禁用。禁用响应式数据，还可以避免将「数据」转换为「响应式对象」的性能开销。
>
> ### 组件生命周期钩子函数
>
> 由于没有动态更新，所有的生命周期钩子函数中，只有 `beforeCreate` 和 `created` 会在服务器端渲染(SSR) 过程中被调用。这就是说任何其他生命周期钩子函数中的代码（例如 `beforeMount` 或`mounted` ），只会在客户端执行。
>
> 此外还需要注意的是，你应该避免在 `beforeCreate` 和 `created` 生命周期时产生全局副作用的代码，例如在其中使用 `setInterval` 设置 `timer`。在纯客户端 (`client-side only`) 的代码中，我们可以设置一个 `timer`，然后在 `beforeDestroy` 或 `destroyed` 生命周期时将其销毁。但是，由于在 `SSR` 期间并不会调用销毁钩子函数，所以 `timer` 将永远保留下来。为了避免这种情况，请将副作用代码移动到`beforeMount` 或 `mounted` 生命周期中。
>
> ### 访问特定平台(Platform-Specific) API
>
> 通用代码不可接受特定平台的 API，因此如果你的代码中，直接使用了像 `window` 或 `document` ，这种仅浏览器可用的全局变量，则会在 Node.js 中执行时抛出错误，反之也是如此。
>
> 对于共享于服务器和客户端，但用于不同平台 API 的任务(task)，建议将平台特定实现包含在通用 API中，或者使用为你执行此操作的 library。例如，[axios](https://github.com/axios/axios) 是一个 HTTP 客户端，可以向服务器和客户端都暴露相同的 API。
>
> 对于仅浏览器可用的 API，通常方式是，在「纯客户端 (client-only)」的生命周期钩子函数中惰性访问(lazily access) 它们。
>
> 请注意，考虑到如果第三方 library 不是以上面的通用用法编写，则将其集成到服务器渲染的应用程序中，可能会很棘手。你可能要通过模拟 (mock) 一些全局变量来使其正常运行，但这只是 hack 的做法，并且可能会干扰到其他 library 的环境检测代码。
>
> ### 区分运行环境
>
> > 参考：https://webpack.js.org/plugins/define-plugin/[](https://webpack.js.org/plugins/define-plugin/)
>
> ```js
> new webpack.DefinePlugin({
>   'process.client': true,
>   'process.server': false
> });
> ```
>
> ### 自定义指令
>
> 大多数自定义指令直接操作 DOM，因此会在服务器端渲染 (SSR) 过程中导致错误。有两种方法可以解决这个问题：
>
> 1. 推荐使用组件作为抽象机制，并运行在「虚拟 DOM 层级(Virtual-DOM level)」（例如，使用渲染函数(render function)）。
> 2. 如果你有一个自定义指令，但是不是很容易替换为组件，则可以在创建服务器 renderer 时，使用`directives` 选项所提供"服务器端版本(server-side version)"。

## 21.路由处理-配置VueRouter

代码目录：

![](http://5coder.cn/img/1669210108_88e075c706fef1539d5c40ab3b7eca3e.png)

**使用 `vue-router` 的路由**

你可能已经注意到，我们的服务器代码使用了一个 `*` 处理程序，它接受任意 URL。这允许我们将访问的 URL 传递到我们的 Vue 应用程序中，然后对客户端和服务器复用相同的路由配置！

为此，建议使用官方提供的 `vue-router`。我们首先创建一个文件，在其中创建 router。注意，类似于 `createApp`，我们也需要给每个请求一个新的 router 实例，所以文件导出一个 `createRouter` 函数：

```js
import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '@/pages/Home'  // 同步的方式导入组件

Vue.use(VueRouter)

export const createRouter = () => {
  const router = new VueRouter({
    mode: 'history',  // 兼容前后端路由
    routes: [
      {
        path: '/',
        name: 'home',
        component: () => import('@/pages/Home')  // 使用路由懒加载
      },
      {
        path: '/about',
        name: 'about',
        component: () => import('@/pages/About')  // 使用路由懒加载
      },
      {
        path: '*',
        name: 'error404',
        component: () => import('@/pages/404')  // 使用路由懒加载
      },
    ]

  })

  return router
}
```

## 22.路由处理-将路由注册到根实例

更新`app.js`

```js
import Vue from 'vue'
import App from './App.vue'
import {createRouter} from "./router";

// 导出一个工厂函数，用于创建新的
// 应用程序、router 和 store 实例
export function createApp() {
  // 创建 router 实例
  const router = createRouter()
  const app = new Vue({
    router,  // 把路由挂在到Vue根实例中
    // 根实例简单的渲染应用程序组件。
    render: h => h(App)
  })
  return {app, router}
}

```

## 23.路由处理-适配服务端入口

现在我们需要在 `entry-server.js` 中实现服务器端路由逻辑 (server-side routing logic)：

```js
// entry-server.js
import { createApp } from './app'

export default context => {
  // 因为有可能会是异步路由钩子函数或组件，所以我们将返回一个 Promise，
  // 以便服务器能够等待所有的内容在渲染前，就已经准备就绪。
  return new Promise((resolve, reject) => {
    const {app, router} = createApp()

    // 设置服务器端 router 的位置
    router.push(context.url)

    // 等到 router 将可能的异步组件和钩子函数解析完
    router.onReady(() => {
      const matchedComponents = router.getMatchedComponents()
      // 匹配不到的路由，执行 reject 函数，并返回 404
      if (!matchedComponents.length) {
        return reject({code: 404})
      }

      // Promise 应该 resolve 应用程序实例，以便它可以渲染
      resolve(app)
    }, reject)
  })
}
```

以上代码可以改造成：

```js
// entry-server.js
import { createApp } from './app'

export default async context => {
  // 因为有可能会是异步路由钩子函数或组件，所以我们将返回一个 Promise，
  // 以便服务器能够等待所有的内容在渲染前，就已经准备就绪。
  const {app, router} = createApp()

  // 设置服务器端 router 的位置
  router.push(context.url)

  // 等到 router 将可能的异步组件和钩子函数解析完
  await new Promise(router.onReady.bind(router))
  return app
}
```

## 24.路由处理-服务端server适配

假设服务器 bundle 已经完成构建（请再次忽略现在的构建设置），服务器用法看起来如下：

`server.js`

```js
const express = require('express')
const fs = require('fs')
const { createBundleRenderer } = require('vue-server-renderer')
const setupDevServer = require('./build/setup-dev-server')

const server = express()

server.use('/dist', express.static('./dist'))

const isProd = process.env.NODE_ENV === 'production'

let renderer
let onReady
if (isProd) {
  const serverBundle = require('./dist/vue-ssr-server-bundle.json')
  const template = fs.readFileSync('./index.template.html', 'utf-8')
  const clientManifest = require('./dist/vue-ssr-client-manifest.json')
  renderer = createBundleRenderer(serverBundle, {
    template,
    clientManifest
  })
} else {
  // 开发模式 -> 监视打包构建 -> 重新生成 Renderer 渲染器
  onReady = setupDevServer(server, (serverBundle, template, clientManifest) => {
    renderer = createBundleRenderer(serverBundle, {
      template,
      clientManifest
    })
  })
}

const render = async (req, res) => {
  try {
    const html = await renderer.renderToString({
      title: '拉勾教育',
      meta: `
        <meta name="description" content="拉勾教育">
      `,
      url: req.url
    })
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    res.end(html)
  } catch (err) {
    res.status(500).end('Internal Server Error.')
  }
}

// 服务端路由设置为 *，意味着所有的路由都会进入这里
server.get('*', isProd
  ? render
  : async (req, res) => {
    // 等待有了 Renderer 渲染器以后，调用 render 进行渲染
    await onReady
    render(req, res)
  }
)

server.listen(3000, () => {
  console.log('server running at port 3000.')
})

```

## 25.路由处理-适配客户端入口

需要注意的是，你仍然需要在挂载 app 之前调用 `router.onReady`，因为路由器必须要提前解析路由配置中的异步组件，才能正确地调用组件中可能存在的路由钩子。这一步我们已经在我们的服务器入口 (server entry) 中实现过了，现在我们只需要更新客户端入口 (client entry)：

`entry-client.js`

```js
/**
 *@date:2022/11/21
 *@Description:entry-client
 */
import { createApp } from './app'

// 客户端特定引导逻辑……

const { app, router } = createApp()

// 这里假定 App.vue 模板中根元素具有 `id="app"`
router.onReady(() => {
  app.$mount('#app')
})
```

## 26.路由处理-处理完成

最后要在 App.vue 根组件中来设置路由的出口，因为没有路由出口的话，匹配到的路由组件就不知道要渲染到哪里。

`App.vue`

```vue
<!-- 客户端渲染的入口节点 -->
<template>
  <div id="app">
    <ul>
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/about">About</router-link>
      </li>
    </ul>

    <!--    路由出口-->
    <router-view/>
  </div>
</template>
<script>
export default {
  name: 'App',
  data() {
    return {
      message: '拉钩教育'
    }
  },
  methods: {
    onClick() {
      console.log('Hello World')
    }
  }
}
</script>
<style>
</style>

```

配置好出口以后，启动应用：`yarn dev`

![](http://5coder.cn/img/1669212879_0affdca96402d7d9d725d7bc3e90bb80.png)

启动成功，访问页面。

测试路由导航，可以看到正常工作，那说明我们同构应用中的路由产生作用了。

现在我们的应用就非常的厉害了，当你首次访问页面的时候，它是通过服务端渲染出来的，服务端渲染拥有了更快的渲染速度以及更好的 SEO，当服务端渲染的内容来到客户端以后被客户端 `Vue` 结合 `VueRouter` 激活，摇身一变成为了一个客户端 `SPA` 应用，之后的页面导航也不需要重新刷新整个页面。这样我们的网站就既拥有了更好的渲染速度，也拥有了更好的用户体验。

除此之外，我们在路由中配置的异步组件（也叫路由懒加载）也是非常有意义，它们会被分割为独立的`chunk`（也就是单独的文件），只有在需要的时候才会进行加载。这样就能够避免在初始渲染的时候客户端加载的脚本过大导致激活速度变慢的问题。关于它也可以来验证一下，通过 `npm run build` 打包构建，我们发现它们确实被分割成了独立的 `chunk`。然后再来看一下在运行期间这些 chunk 文件是如何加载的。

![](http://5coder.cn/img/1669213220_12cc1b0ef89337da0847aed8f6ac9e89.png)

![](http://5coder.cn/img/1669213060_f8a6234b1235e7602963540d51af964c.png)

你会发现除了 `app` 主资源外，其它的资源也被下载下来了，你是不是要想说：不是应该在需要的时候才加载吗？为什么一上来就加载了。

原因是在页面的头部中的带有 `preload` 和 `prefetch` 的 link 标签。

![](http://5coder.cn/img/1669213082_828a1830948d8dc31cedc6c7a1fc37cb.png)

我们期望客户端 JavaScript 脚本尽快加载尽早的接管服务端渲染的内容，让其拥有动态交互能力，但是如果你把 script 标签放到这里的话，浏览器会去下载它，然后执行里面的代码，这个过程会阻塞页面的渲染。

所以看到真正的 script 标签是在页面的底部的。而这里只是告诉浏览器可以去预加载这个资源。但是不要执行里面的代码，也不要影响网页的正常渲染。直到遇到真正的 script 标签加载该资源的时候才会去执行里面的代码，这个时候可能已经预加载好了，直接使用就可以了，如果没有加载好，也不会造成重复加载，所以不用担心这个问题。

而 prefetch 资源是加载下一个页面可能用到的资源，浏览器会在空闲的时候对其进行加载，所以它并不一定会把资源加载出来，preload 一定会预加载。所以你可以看到当我们去访问 about 页面的时候，它的资源是通过 prefetch 预取过来的，提高了客户端页面导航的响应速度。

![image-20221123222111125](http://5coder.cn/img/1669213271_3f71bd506ae3874b14df99f82acf69e4.png)

好了，关于同构应用中路由的处理，以及代码分割功能就介绍到这里。

## 27.管理页面Head内容

无论是服务端渲染还是客户端渲染，它们都使用的同一个页面模板。

页面中的 body 是动态渲染出来的，但是页面的 head 是写死的，也就说我们希望不同的页面可以拥有自己的 head 内容，例如页面的 title、meta 等内容，所以下面我们来了解一下如何让不同的页面来定制自己的 head 头部内容。

官方文档这里专门描述了关于页面 Head 的处理，相对于来讲更原生一些，使用比较麻烦，有兴趣的同学可以了解一下。
我这里主要给大家介绍一个第三方解决方案：[vue-meta](https://github.com/nuxt/vue-meta)。

Vue Meta 是一个支持 SSR 的第三方 Vue.js 插件，可让你轻松的实现不同页面的 head 内容管理。使用它的方式非常简单，而只需在页面组件中使用 `metaInfo` 属性配置页面的 head 内容即可。

```vue
<template>
	...
</template>
<script>
export default {
  metaInfo: {
    title: 'My Example App',
    titleTemplate: '%s - Yay!',
    htmlAttrs: {
      lang: 'en',
      amp: true
    }
  }
}
</script>
```

页面渲染出来的结果：

```vue
<html lang="en" amp>
<head>
	<title>My Example App - Yay!</title>
	...
</head>
```

安装：`npm i vue-meta`

在通用入口`app.js`中通过插件的方式将 vue-meta 注册到 Vue 中。

```js
import Vue from 'vue'
import App from './App.vue'
import VueMeta from "vue-meta";
import {createRouter} from "./router";

Vue.use(VueMeta)

Vue.mixin({
  metaInfo: {
    titleTemplate: '%s - 拉勾教育'
  }
})

// 导出一个工厂函数，用于创建新的
// 应用程序、router 和 store 实例
export function createApp() {
  // 创建 router 实例
  const router = createRouter()
  const app = new Vue({
    router,  // 把路由挂在到Vue根实例中
    // 根实例简单的渲染应用程序组件。
    render: h => h(App)
  })
  return {app, router}
}

```

然后在服务端渲染入口`ertry-server.js`模块中适配 vue-meta：

```js
// entry-server.js
import { createApp } from './app'

export default async context => {
  // 因为有可能会是异步路由钩子函数或组件，所以我们将返回一个 Promise，
  // 以便服务器能够等待所有的内容在渲染前，就已经准备就绪。
  const { app, router } = createApp()

  const meta = app.$meta()

  // 设置服务器端 router 的位置
  router.push(context.url)

  context.meta = meta

  // 等到 router 将可能的异步组件和钩子函数解析完
  await new Promise(router.onReady.bind(router))
  return app
}
```

最后在模板页面`index.template.html`中注入 meta 信息：

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {{{ meta.inject().title.text() }}}
  {{{ meta.inject().meta.text() }}}
</head>

<body>
  <!--vue-ssr-outlet-->
</body>

</html>

```

下面就是直接在组件中使用即可：

![](http://5coder.cn/img/1669215262_10dc013a348313822ecd8e5987c5f43d.png)

![](http://5coder.cn/img/1669215303_650b1de7c5433c1abe1192b39d5fae48.png)

当然，还可以定制更多的内容，在[官网](https://vue-meta.nuxtjs.org/api/)中看到还可以定制title、titleTemplate、htmlAttrs、headAttrs等。

![image-20221123225720060](http://5coder.cn/img/1669215440_0e87d25e40576c31d7e593c467370838.png)

## 28.数据预取和状态管理-思路分析

[数据预取和状态官方文档](https://v2.ssr.vuejs.org/zh/guide/data.html#%E6%95%B0%E6%8D%AE%E9%A2%84%E5%8F%96%E5%AD%98%E5%82%A8%E5%AE%B9%E5%99%A8-data-store)

接下来我们来了解一下服务端渲染中的数据预取和状态管理。

官方文档中的描述比较枯燥，无法在很短的时间内搞清楚它到底要做什么，所以我们这里通过一个实际的业务需求来引入这个话题。

我们的需求就是：

- 已知有一个数据接口，接口返回一个文章列表数据
- 我们想要通过服务端渲染的方式来把异步接口数据渲染到页面中

这个需求看起来是不是很简单呢？无非就是在页面发请求拿数据，然后在模板中遍历出来，如果是纯客

户端渲染的话确实就是这样的，但是想要通过服务端渲染的方式来处理的话就比较麻烦了。

无论如何，我们都要来尝试一下：

![](http://5coder.cn/img/1669215693_469ffc5ad9285655d33ffdb0743d2ec0.png)

也就是说我们要在服务端获取异步接口数据，交给 Vue 组件去渲染。

我们首先想到的肯定是在组件的生命周期钩子中请求获取数据渲染页面，那我们可以顺着这个思路来试一下。

在组件中添加生命周期钩子，beforeCreate 和 created，服务端渲染仅支持这两个钩子函数的调用。然后下一个问题是如何在服务端发送请求？依然使用 axios，axios 既可以运行在客户端也可以运行在服务端，因为它对不同的环境做了适配处理，在客户端是基于浏览器的XMLHttpRequest 请求对象，在服务端是基于 Node.js 中的 http 模块实现，无论是底层是什么，上层的使用方式都是一样的。

首先创建Post.vue组件

```vue
<template>
  <div>
    <h1>Post List</h1>
    <ul>
      <li v-for="post in posts" :key="post.id">{{ post.title }}</li>
    </ul>
  </div>
</template>

<script>

export default {
  name: 'PostList',
  metaInfo: {
    title: 'Posts'
  },
  data () {
    return {
      posts: []
    }
  },

  // 服务端渲染
  //     只支持 beforeCreate 和 created
  //     不会等待 beforeCreate 和 created 中的异步操作
  //     不支持响应式数据
  // 所有这种做法在服务端渲染中是不会工作的！！！
  async created () {
    console.log('Posts Created Start')
    const { data } = await axios({
      method: 'GET',
      url: 'https://cnodejs.org/api/v1/topics'
    })
    this.posts = data.data
    console.log('Posts Created End')
  }
}
</script>

<style>

</style>

```

我们尝试在`created`生命周期函数中获取数据，运行服务后，我们发现页面确实出现了文章列表页面，但这真的是`Post`中的`created`生命周期函数中请求的吗？可以打开浏览器查看，在初始请求`post/`的时候，打开预览页面，发现文章列表页面并没有被渲染出来，而是在客户端中再次请求后才渲染出来的。所以是服务端的请求没有生效吗，可以打开控制台，发现我们打印的日志也打印出来了。因此得出结论，服务端的`created`和`beforeCreated`生命周期函数并不会响应数据。

![](http://5coder.cn/img/1669216738_8f7a646fa257494cc73934114ed37527.png)

在`network`中可以发现，还有一个`topics`的请求，我们打开后可以发现，文章数据是客户端自己请求出来的。

![](http://5coder.cn/img/1669216793_b8ccc55db65220ed60507e8af71d2e00.png)

这时候查看服务员控制台，我们发现日志打印也成功的输出了。所以印证了以上的现象：服务端的`created`和`beforeCreated`生命周期函数并不会响应数据。

## 29.数据预取和状态管理-数据预取

> 在服务器端渲染(SSR)期间，我们本质上是在渲染我们应用程序的"快照"，所以如果应用程序依赖于一些异步数据，**那么在开始渲染过程之前，需要先预取和解析好这些数据**。
>
> 另一个需要关注的问题是在客户端，在挂载 (mount) 到客户端应用程序之前，需要获取到与服务器端应用程序完全相同的数据 - 否则，客户端应用程序会因为使用与服务器端应用程序不同的状态，然后导致混合失败。
>
> 为了解决这个问题，获取的数据需要位于视图组件之外，即放置在专门的数据预取存储容器(data store)或"状态容器(state container)"中。首先，在服务器端，我们可以在渲染之前预取数据，并将数据填充到 store 中。此外，我们将在 HTML 中序列化(serialize)和内联预置(inline)状态。这样，在挂载(mount)到客户端应用程序之前，可以直接从 store 获取到内联预置(inline)状态。

接下来我们就按照官方文档给出的参考来把服务端渲染中的数据预取以及状态管理来处理一下。

通过官方文档我们可以看到，它的核心思路就是把在服务端渲染期间获取的数据存储到 Vuex 容器中，然后把容器中的数据同步到客户端，这样就保持了前后端渲染的数据状态同步，避免了客户端重新渲染的问题。

所以接下来要做的第一件事儿就是把 Vuex 容器创建出来。

### （1）通过 Vuex 创建容器实例，并挂载到 Vue 根实例

安装 Vuex：`npm i vuex`

创建 Vuex 容器：

```js
import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

export const createStore = () => {
  return new Vuex.Store({
    state: () => ({
      posts: []
    }),

    mutations: {
      setPosts(state, data) {
        seate.posts = data
      }
    },

    actions: {
      // 在服务端渲染器件，务必让action返回Promise
      async getPosts({ commit }) {
        const { data } = await axios.get('https://cnodejs.org/api/v1/topics')
        commit('setPosts', data.data)
      }
    }
  })
}
```

在通用应用入口`app.js`中将 `Vuex` 容器挂载到 `Vue` 根实例：

```js
import Vue from 'vue'
import App from './App.vue'
import VueMeta from "vue-meta";
import { createRouter } from "./router";
import { createStore } from "./store";

Vue.use(VueMeta)

Vue.mixin({
  metaInfo: {
    titleTemplate: '%s - 拉勾教育'
  }
})

// 导出一个工厂函数，用于创建新的
// 应用程序、router 和 store 实例
export function createApp() {
  // 创建 router 实例
  const router = createRouter()
  const store = createStore()
  const app = new Vue({
    router,  // 把路由挂在到Vue根实例中
    store,  // 把容器挂在到Vue示例中
    // 根实例简单的渲染应用程序组件。
    render: h => h(App)
  })
  return { app, router, store }
}

```

### （2）在组件中使用 serverPrefetch 触发容器中的 action

```vue
<template>
  <div>
    <h1>Post List</h1>
    <ul>
      <li v-for="post in posts" :key="post.id">{{ post.title }}</li>
    </ul>
  </div>
</template>

<script>
// import axios from 'axios'
import { mapState, mapActions } from 'vuex'


export default {
  name: 'PostList',
  metaInfo: {
    title: 'Posts'
  },
  data() {
    return {
      // posts: []
    }
  },
  computed: {
    ...mapState(['posts'])
  },
  // Vue ssr特殊为服务端渲染提供的一个生命周期钩子函数
  serverPrefetch() {
    // 发起action 返回Promise
    // this.$store.dispatch('getPosts')
    return this.getPosts()
  },
  methods: {
    ...mapActions(['getPosts'])
  }
  // 服务端渲染
  //     只支持 beforeCreate 和 created
  //     不会等待 beforeCreate 和 created 中的异步操作
  //     不支持响应式数据
  // 所有这种做法在服务端渲染中是不会工作的！！！
  // async created() {
  //   console.log('Posts Created Start')
  //   const { data } = await axios({
  //     method: 'GET',
  //     url: 'https://cnodejs.org/api/v1/topics'
  //   })
  //   this.posts = data.data
  //   console.log('Posts Created End')
  // }
}
</script>

<style>

</style>

```

## 30.数据预取和状态管理-将预取数据同步到客户端

在服务端渲染应用入口中将容器状态序列化到页面中

接下来我们要做的就是把在服务端渲染期间所获取填充到容器中的数据同步到客户端容器中，从而避免两个端状态不一致导致客户端重新渲染的问题。

- 将容器中的 state 转为 JSON 格式字符串
- 生成代码： `window.__INITIAL__STATE = 容器状态` 语句插入模板页面中
- 【客户端通过 `window.__INITIAL__STATE` 获取该数据】

entry-server.js

```js
// entry-server.js
import { createApp } from './app'

export default async context => {
  // 因为有可能会是异步路由钩子函数或组件，所以我们将返回一个 Promise，
    // 以便服务器能够等待所有的内容在渲染前，
    // 就已经准备就绪。
  const { app, router, store } = createApp()

  const meta = app.$meta()

  // 设置服务器端 router 的位置
  router.push(context.url)

  context.meta = meta

  // 等到 router 将可能的异步组件和钩子函数解析完
  await new Promise(router.onReady.bind(router))

  context.rendered = () => {
    // Renderer 会把 context.state 数据对象内联到页面模板中
    // 最终发送给客户端的页面中会包含一段脚本：window.__INITIAL_STATE__ = context.state
    // 客户端就要把页面中的 window.__INITIAL_STATE__ 拿出来填充到客户端 store 容器中
    context.state = store.state
  }

  return app
}
```

![](http://5coder.cn/img/1669218378_f4583f1a6b89c07dfd1580a1cadb0449.png)

最后，在客户端渲染入口中把服务端传递过来的状态数据填充到客户端 Vuex 容器中：

entry-client.js

```js
/**
 * 客户端入口
 */
import { createApp } from './app'

// 客户端特定引导逻辑……

const { app, router, store } = createApp()

if (window.__INITIAL_STATE__) {
  store.replaceState(window.__INITIAL_STATE__)
}

router.onReady(() => {
  app.$mount('#app')
})

```

![](http://5coder.cn/img/1669218489_bede17d8b790e30bd848c52e9f981cfb.png)

客户端更新问题：

```js
...
  mounted () {
    if (!this.posts.length) {
      this.$store.dispatch('getPosts')
    }
  },
  beforeRouteLeave (to, from, next) {
    this.$store.commit('setPosts', [])
    next()
  }
...
```

## 31.服务端渲染优化

这里主要针对是服务端层面的优化。尽管 Vue 的 SSR 速度相当快，但由于创建组件实例和虚拟 DOM 节点的成本，它无法与纯基于字符串的模板的性能相匹配。在 SSR 性能至关重要的情况下，明智地利用缓存策略可以极大地缩短响应时间并减少服务器负载。

缓存能够更快的将内容发送给客户端，提升 web 应用程序的性能，同时减少服务器的负载。

### 页面缓存

如[官方文档](https://vuejs.org/guide/scaling-up/ssr.html#page-level-caching)中介绍的那样，对特定的页面合理的应用 [micro-caching](https://www.nginx.com/blog/benefits-of-microcaching-nginx/) 能够大大改善服务器处理并发的能力(吞吐率 RPS )。但并非所有页面都适合应用 micro-caching 缓存策略，我们可以将资源分为三类：

- 静态资源：如 `js` 、`css` 、`images` 等。
- 用户特定的动态资源：不同的用户访问相同的资源会得到不同的内容。
- 用户无关的动态资源：任何用户访问该资源都会得到相同的内容，但该内容可能在任意时间发生变化，如博客文章。

只有“用户无关的动态资源”适合应用 micro-caching 缓存策略。

- https://github.com/isaacs/node-lru-cache

安装依赖：npm i lru-cache

server.js

```js
const express = require('express')
const fs = require('fs')
const { createBundleRenderer } = require('vue-server-renderer')
const setupDevServer = require('./build/setup-dev-server')
const LRU = require('lru-cache')
const cache = new LRU({
  max: 100,
  maxAge: 10000 // Important: entries expires after 1 second.
})
const isCacheable = req => {
  console.log(req.url)
  if (req.url === '/posts') {
    return true
  }
}
const server = express()
server.use('/dist', express.static('./dist'))
const isProd = process.env.NODE_ENV === 'production'

let renderer
let onReady
if (isProd) {
  const serverBundle = require('./dist/vue-ssr-server-bundle.json')
  const template = fs.readFileSync('./index.template.html', 'utf-8')
  const clientManifest = require('./dist/vue-ssr-client-manifest.json')
  renderer = createBundleRenderer(serverBundle, {
    template,
    clientManifest
  })
} else {
  // 开发模式 -> 监视打包构建 -> 重新生成 Renderer 渲染器
  onReady = setupDevServer(server, (serverBundle, template, clientManifest) => {
    renderer = createBundleRenderer(serverBundle, {
      template,
      clientManifest
    })
  })
}
const render = async (req, res) => {
  try {
    const cacheable = isCacheable(req)
    if (cacheable) {
      const html = cache.get(req.url)
      if (html) {
        return res.end(html)
      }
    }
    const html = await renderer.renderToString({
      title: '拉勾教育',
      meta: `
<meta name="description" content="拉勾教育">
`,
      url: req.url
    })
    res.setHeader('Content-Type', 'text/html; charset=utf8')
    res.end(html)
    if (cacheable) {
      cache.set(req.url, html)
    }
  } catch (err) {
    res.status(500).end('Internal Server Error.')
  }
}
// 服务端路由设置为 *，意味着所有的路由都会进入这里
server.get('*', isProd
  ? render
  : async (req, res) => {
    // 等待有了 Renderer 渲染器以后，调用 render 进行渲染
    await onReady
    render(req, res)
  }
)
server.listen(3000, () => {
  console.log('server running at port 3000.')
})
```

### Gzip 压缩

注意事项：

- 默认的过滤器功能使用 compressible 模块来确定 res.getHeader（'Content-Type'）是否可压缩。

### 组件级别缓存
