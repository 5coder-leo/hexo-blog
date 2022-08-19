---
title: Nuxt.js基础
author: 5coder
tags: Nuxt.js
category: 大前端
abbrlink: 25880
date: 2021-07-22 21:43:29
keywords:
top:
cover:
---

## Nuxt.js基础

## Nuxt.js介绍

### Nuxt.js是什么？

- [官网](https://zh.nuxtjs.org/)
- [GitHub仓库](https://github.com/nuxt/nuxt.js)

> 官网介绍
>
> `Nuxt.js` 是一个基于 `Vue.js` 的服务端渲染应用框架，它可以帮我们轻松的实现同构应用。
>
> 通过对客户端/服务端基础架构的抽象组织，`Nuxt.js` 主要关注的是应用的 **UI渲染**。
>
> 我们的目标是创建一个灵活的应用框架，你可以基于它初始化新项目的基础结构代码，或者在已有Node.js 项目中使用 Nuxt.js。
>
> `Nuxt.js` 预设了利用 `Vue.js` 开发**服务端渲染**的应用所需要的各种配置。
>
> 除此之外，我们还提供了一种命令叫： `nuxt generate` ，为基于 `Vue.js` 的应用提供生成对应的静态站点的功能。
>
> 我们相信这个命令所提供的功能，是向开发集成各种微服务（**Microservices**）的 Web 应用迈开的新一步。
>
> 作为框架，`Nuxt.js` 为 **客户端/服务端** 这种典型的应用架构模式提供了许多有用的特性，例如**异步数据加载、中间件支持、布局支持**等非常实用的功能。

### Nuxt.js框架是如何运作的？

![](http://5coder.cn/img/image-20210722221056696.png)

Nuxt.js集成了以下组件/框架，用于开发完整而强大的Web应用：

- Vue.js
- Vue Router
- Vuex（当配置了**Vuex状态树配置项**时才会引入）
- Vue Server Renderer（排除使用`mode:'spa'`）
- Vue-Meta

压缩并gzip后，总代吗大小为：**57kb**（如果使用了Vuex特性的话为**60kb**）

另外，Nuxt.js使用[Webpack](https://github.com/webpack/webpack)和[vue-router](https://github.com/vuejs/vue-loader)、[babel-loader](https://github.com/babel/babel-loader)来处理代码的自动构建工作（如打包、代码分层、压缩等）

### Nuxt.js特性

- 基于Vue.js
  - Vue、Vue Router、Vuex、Vue SSR
- 自动代码分层
- 服务端渲染
- 强大的路由功能，支持异步数据
- 静态文件服务
- ES2015+语法支持
- 打包和压缩js和css
- HTML头部标签管理
- 本地开发支持热加载
- 集成ESLint
- 支持各种样式预处理器：SASS、LESS、Stylus
- 支持HTTP/2推送

### Nuxt.js渲染方式

#### 服务器端渲染站点和静态站点

> 服务器端呈现的站点在用户每次请求页面时都呈现在服务器上，因此服务器需要能够在每次请求时为页面提供服务。
>
> 静态站点与服务器端呈现的应用程序非常相似，主要区别在于静态站点是在构建时呈现的，因此不需要服务器。 从一个页面导航到另一个页面是在客户端。  
>
> `nuxt.config.js`
>
> ```js
> export default {
> 	ssr: true // default value
> }
> ```

#### 仅客户端渲染

> 只有客户端呈现，就没有服务器端呈现。 客户端呈现是指使用JavaScript在浏览器中呈现内容。 我们没有从HTML中获取所有内容，而是获得一个带有JavaScript文件的基本HTML文档，然后使用浏览器呈现站点的其余部分。 对于客户端渲染设置ssr为`false`。  
>
> `nuxt.config.js`
>
> ```js
> export default {
> 	ssr: false
> }
> ```

### Nuxt.js的使用方式

- 初始项目
- 已有的Node.js服务端项目
  - 直接把Nuxt当做一个**中间件**集成到**Node Web Server**中
- 现有的Vue.js项目
  - <u>非常熟系Nuxt.js</u>
  - <u>至少百分之十的代码改动</u>

## 创建项目

### 使用create-nuxt-app创建项目

```bash
yarn create nuxt-app <project-name>
cd <project-name>
yarn dev
```

### 从零开始创建项目

#### （1）准备

```bash
# 创建示例项目
mkdir nuxt-app-demo

# 进入示例项目目录中
cd nuxt-app-demo

# 初始化package.json文件
yarn init -y

# 安装nuxt
yarn add nuxt
```

在`package.json`文件的`scripts`中新增：

```json
"scripts": {
  "dev": "nuxt"
}
```

上面的配置使得我们可以通过运行`yarn dev`来运行`Nuxt`

#### （2）创建页面并启动项目

创建`pages`目录

```
mkdir pages
```

创建第一个页面pages/index.vue：

```html
<template>
	<h1>Hello world!</h1>
</template>
```

然后启动项目：

```bash
yarn dev
```

现在应用运行在http://localhost:3000上。

> 注意：Nuxt.js会监听`pages`目录中的文件更改，因此在添加新页面时无需重新启动应用程序。

## Nuxt路由

Nuxt.js 依据 `pages` 目录结构自动生成 vue-router 模块的路由配置。

### 基础路由

假设pages的目录结构如下：

![](http://5coder.cn/img/image-20210722223136076.png)

那么Nuxt.js自动生成的路由配置如下：

```json
router: {
  routes: [
    {
      name: 'index',
      path: '/',
      component: 'pages/index.vue'
    },
    {
      name: 'user',
      path: '/user',
      component: 'pages/user/index.vue'
    },
    {
      name: 'user-one',
      path: '/user/one',
      component: 'pages/user/one.vue'
    }
  ]
}
```

自动生成的`.nuxt/router.js`

![](http://5coder.cn/img/image-20210722230731656.png)

### [路由导航](https://router.vuejs.org/zh/guide/)

- a 标签
  - 它会刷新整个页面，不要使用
- `<nuxt-link>` 组件
- 编程式导航

```html
<template>
  <div>
    <h1>About Nuxt.js</h1>
    <!--    整个页面刷新，走服务端渲染-->
    <h2>a链接</h2>
    <a href="/">首页</a>
    <hr>

    <!-- router-link导航链接组件 -->
    <h2>router-link</h2>
    <router-link to="/">首页</router-link>
    <hr>

    <!--    编程式导航-->
    <h2>编程式导航</h2>
    <button @click="onClick">首页</button>
  </div>
</template>

<script>
export default {
  name: "about",
  methods: {
    onClick() {
      this.$router.push('/')
    }
  }
}
</script>
```

### 动态路由

- [Vue Router动态路由匹配](https://router.vuejs.org/zh/guide/essentials/dynamic-matching.html)

  - 我们经常需要把某种模式匹配到的所有路由，全都映射到同个组件。例如，我们有一个 `User` 组件，对于所有 ID 各不相同的用户，都要使用这个组件来渲染。那么，我们可以在 `vue-router` 的路由路径中使用“动态路径参数”(dynamic segment) 来达到这个效果：

  ```js
  const User = {
    template: '<div>User</div>'
  }
  
  const router = new VueRouter({
    routes: [
      // 动态路径参数 以冒号开头
      { path: '/user/:id', component: User }
    ]
  })
  ```

  现在呢，像 `/user/foo` 和 `/user/bar` 都将映射到相同的路由。

  一个“路径参数”使用冒号 `:` 标记。当匹配到一个路由时，参数值会被设置到 `this.$route.params`，可以在每个组件内使用。于是，我们可以更新 `User` 的模板，输出当前用户的 ID：

  ```js
  const User = {
    template: '<div>User {{ $route.params.id }}</div>'
  }
  ```

- [Nuxt.js动态路由](https://www.nuxtjs.cn/guides/features/file-system-routing#dynamic-routes)

  - 有时不可能知道路由的名称，比如当我们调用一个api来获取用户列表或博客文章时。 我们称之为动态路由。 要创建动态路由，需要在.vue文件名之前或目录名称之前添加下划线。 您可以任意命名文件或目录，但必须使用下划线作为前缀。

  目录结构：

  ```txt
  pages/
  --| _slug/
  -----| comments.vue
  -----| index.vue
  --| users/
  -----| _id.vue
  --| index.vue
  ```

  Nuxt.js生成对应的路由配置表

  ```json
  router: {
    routes: [
      {
        name: 'index',
        path: '/',
        component: 'pages/index.vue'
      },
      {
        name: 'users-id',
        path: '/users/:id?',
        component: 'pages/users/_id.vue'
      },
      {
        name: 'slug',
        path: '/:slug',
        component: 'pages/_slug/index.vue'
      },
      {
        name: 'slug-comments',
        path: '/:slug/comments',
        component: 'pages/_slug/comments.vue'
      }
    ]
  }
  ```

  > 如您所见，名为 users-id 的路由的路径为 :id?这使它成为可选的，如果你想使它成为必需的，请在 users/_id 目录中创建一个 index.vue 文件。

> 从Nuxt >= v2.13开始，已经安装了一个爬虫程序，它将抓取你的链接标签并基于这些链接生成动态路由。 但是，如果您有没有链接到的页面，比如秘密页面，那么您将需要手动生成这些动态路由。  

拿到当前匹配的路由对象的参数

> You can access the current route parameters within your local page or component by referencing `this.$route.params.{parameterName}`. For example, if you had a dynamic users page (`users\_id.vue`) and wanted to access the `id` parameter to load the user or process information, you could access the variable like this: `this.$route.params.id`.

![](http://5coder.cn/img/image-20210723061713653.png)

![](http://5coder.cn/img/image-20210723061749059.png)

### 嵌套路由

- [Vue Router嵌套路由](https://router.vuejs.org/zh/guide/essentials/nested-routes.html)

  实际生活中的应用界面，通常由多层嵌套的组件组合而成。同样地，URL 中各段动态路径也按某种结构对应嵌套的各层组件，例如：

  ```txt
  /user/foo/profile                     /user/foo/posts
  +------------------+                  +-----------------+
  | User             |                  | User            |
  | +--------------+ |                  | +-------------+ |
  | | Profile      | |  +------------>  | | Posts       | |
  | |              | |                  | |             | |
  | +--------------+ |                  | +-------------+ |
  +------------------+                  +-----------------+
  ```

  借助 `vue-router`，使用嵌套路由配置，就可以很简单地表达这种关系。

  接着上节创建的 app：

  ```html
  <div id="app">
    <router-view></router-view>
  </div>
  ```

  ```js
  const User = {
    template: '<div>User {{ $route.params.id }}</div>'
  }
  
  const router = new VueRouter({
    routes: [{ path: '/user/:id', component: User }]
  })
  ```

  这里的 `<router-view>` 是最顶层的出口，渲染最高级路由匹配到的组件。同样地，一个被渲染组件同样可以包含自己的嵌套 `<router-view>`。例如，在 `User` 组件的模板添加一个 `<router-view>`：

  ```js
  const User = {
    template: `
      <div class="user">
        <h2>User {{ $route.params.id }}</h2>
        <router-view></router-view>
      </div>
    `
  }
  ```

  要在嵌套的出口中渲染组件，需要在 `VueRouter` 的参数中使用 `children` 配置：

  ```js
  const router = new VueRouter({
    routes: [
      {
        path: '/user/:id',
        component: User,
        children: [
          {
            // 当 /user/:id/profile 匹配成功，
            // UserProfile 会被渲染在 User 的 <router-view> 中
            path: 'profile',
            component: UserProfile
          },
          {
            // 当 /user/:id/posts 匹配成功
            // UserPosts 会被渲染在 User 的 <router-view> 中
            path: 'posts',
            component: UserPosts
          }
        ]
      }
    ]
  })
  ```

  **要注意，以 `/` 开头的嵌套路径会被当作根路径。 这让你充分的使用嵌套组件而无须设置嵌套的路径。**

  你会发现，`children` 配置就是像 `routes` 配置一样的路由配置数组，所以呢，你可以嵌套多层路由。

  此时，基于上面的配置，当你访问 `/user/foo` 时，`User` 的出口是不会渲染任何东西，这是因为没有匹配到合适的子路由。如果你想要渲染点什么，可以提供一个 空的 子路由：

  ```js
  const router = new VueRouter({
    routes: [
      {
        path: '/user/:id',
        component: User,
        children: [
          // 当 /user/:id 匹配成功，
          // UserHome 会被渲染在 User 的 <router-view> 中
          { path: '', component: UserHome }
  
          // ...其他子路由
        ]
      }
    ]
  })
  ```

- [Nuxt.js嵌套路由](https://www.nuxtjs.cn/guides/features/file-system-routing#nested-routes)

你可以通过 vue-router 的子路由创建 Nuxt.js 应用的嵌套路由。
创建内嵌子路由，你需要添加一个 Vue 文件，同时添加一个与**该文件同名的目录**用来存放子视图组件。

> Warning: 别忘了在父组件( .vue 文件) 内增加 <nuxt-child/> 用于显示子视图内容。

假设文件结构如：

```txt
pages/
--| users/
-----| _id.vue
-----| index.vue
--| users.vue
```

Nuxt.js 自动生成的路由配置如下：

```json
router: {
  routes: [
    {
      path: '/users',
      component: 'pages/users.vue',
      children: [
        {
          path: '',
          component: 'pages/users/index.vue',
          name: 'users'
        },
        {
          path: ':id',
          component: 'pages/users/_id.vue',
          name: 'users-id'
        }
      ]
    }
  ]
}
```

![](http://5coder.cn/img/image-20210723063147108.png)

![](http://5coder.cn/img/image-20210723063221316.png)

![](http://5coder.cn/img/image-20210723063237799.png)

