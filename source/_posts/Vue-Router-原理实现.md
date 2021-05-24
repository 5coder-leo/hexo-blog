---

title: Vue-Router 原理实现
author: 5coder
abbrlink: 60218
date: 2021-05-23 10:20:13
tags: Vue-Router
category: 大前端
password:
keywords: 
- Vue-Router
- Vue-Router原理
top:
cover:
---

# Vue-Router 原理实现

> 摘要：
>
> **首先来复习一下Vue-Router的基本使用，模拟实现之前，通过它的基本使用方式来进行分析如何实现。然后再来回顾一下，Hash模式和History模式的区别，演示一下History模式如何去使用，History模式要结合服务器一起来使用。最后再来模拟实现自己的Vue-Router，通过自己来实现一个Vue-Router，通过模拟实现Vue-Router来了解Vue-Router内部的实现原理。**
>
> [==官方文档==](https://router.vuejs.org/zh/)

## 1.Vue-Router基本回顾-使用步骤

1. ### 使用`Vue.use(VueRouter)`注册路由插件

   `src/router/index.js`

   ```js
   import Vue from 'vue'
   import VueRouter from 'vue-router'
   import Index from '../views/Index.vue'
   // 1. 注册路由插件(Vue.use接收参数，如果参数是函数，则直接调用函数注册插件，如果是对象则使用对象的install方法注册组件)
   Vue.use(VueRouter)
   ```

2. ### 创建`router`对象

   `src/router/index.js`

   ```js
   // 路由规则
   const routes = [
     {
       path: '/',
       name: 'Index',
       component: Index
     },
     {
       path: '/blog',
       name: 'Blog',
       // route level code-splitting
       // this generates a separate chunk (about.[hash].js) for this route
       // which is lazy-loaded when the route is visited.
       component: () => import(/* webpackChunkName: "blog" */ '../views/Blog.vue')
     },
     {
       path: '/photo',
       name: 'Photo',
       // route level code-splitting
       // this generates a separate chunk (about.[hash].js) for this route
       // which is lazy-loaded when the route is visited.
       component: () => import(/* webpackChunkName: "photo" */ '../views/Photo.vue')
     }
   ]
   // 2. 创建 router 对象
   const router = new VueRouter({
     routes
   })
   
   export default router
   ```

3. ### 注册`router`对象

   `src/main.js`

   ```js
   import Vue from 'vue'
   import App from './App.vue'
   import router from './router'
   
   Vue.config.productionTip = false
   
   const vm = new Vue({
     // 3. 注册 router 对象
     router,
     render: h => h(App)
   }).$mount('#app')
   console.log(vm)
   ```

4. ### 创建路由组件的占位：`<router-view/>`

   `src/App.vue`

   ```vue
   <template>
     <div id="app">
       <div>
         <img src="@/assets/logo.png" alt="">
       </div>
       <div id="nav">
         <!-- 5. 创建链接 -->
         <router-link to="/">Index</router-link> |
         <router-link to="/blog">Blog</router-link> |
         <router-link to="/photo">Photo</router-link>
       </div>
       <!-- 4. 创建路由组建的占位 -->
       <router-view/>
     </div>
   </template>
   ```

5. ### 创建链接

   ```html
   <router-link to="/">Index</router-link> |
   <router-link to="/blog">Blog</router-link> |
   <router-link to="/photo">Photo</router-link>
   ```

创建Vue实例时，传入Vue-Router的作用：

1. 未传入router对象

   main.js中注释router：

   ```js
   import Vue from 'vue'
   import App from './App.vue'
   // import router from './router'
   
   Vue.config.productionTip = false
   
   const vm = new Vue({
     // 3. 注册 router 对象
     // router,
     render: h => h(App)
   }).$mount('#app')
   console.log(vm)
   ```

   打开浏览器，打印vm实例，发现vm实例中并无router相关的属性。

   ![](https://i.loli.net/2021/05/23/g2W65s8Xtaw9fFr.png)

2. 传入router对象

   将router对象解开注释，在浏览器控制台打印vm实例。

   ```js
   import Vue from 'vue'
   import App from './App.vue'
   import router from './router'
   
   Vue.config.productionTip = false
   
   const vm = new Vue({
     // 3. 注册 router 对象
     router,
     render: h => h(App)
   }).$mount('#app')
   console.log(vm)
   ```

   ![](https://i.loli.net/2021/05/23/Tz2uN3rWpYIJUZw.png)

   发现vm实例中多出了属性$route和$router属性。

   - $route

     route是一个跳转的路由对象，每一个路由都会有一个route对象，是一个局部的对象，可以获取对应的name,path,params,query等

     ![](https://i.loli.net/2021/05/23/mDbk2HtwN6ngsSc.png)

     - $route.path 
       字符串，等于当前路由对象的路径，会被解析为绝对路径，如 `"/home/news"` 。
     - $route.params 
       对象，包含路由中的动态片段和全匹配片段的键值对
     - $route.query 
       对象，包含路由中查询参数的键值对。例如，对于 `/home/news/detail/01?favorite=yes` ，会得到`$route.query.favorite == 'yes'` 。
     - $route.router 
       路由规则所属的路由器（以及其所属的组件）。
     - $route.matched 
       数组，包含当前匹配的路径中所包含的所有片段所对应的配置参数对象。
     - $route.name 
       当前路径的名字，如果没有使用具名路径，则名字为空。

     > **注意：query和params的区别**
     >
     > params传递参数需要在路由文件中进行配置，例如  path: "/detail/:id/:name",  component: Detail,最终url生成的路径是detail/10/apple , 传参的方式是： this.$router.push({ path: "/detail/"+id });
     >
     > query可以直接传递参数，且最终的url格式是 detail？id=10，传参的方式是：this.$router.push({ path: "/detail"，query：{id：this.id}});
     >
     > query和params获取参数传递参数都是通过当前路由 this.$route

   - $router

     $router是VueRouter的一个对象，通过Vue.use(VueRouter)和VueRouter构造函数得到一个router的实例对象，这个对象中是一个全局的对象，他包含了所有的路由包含了许多关键的对象和属性。

     ![](https://i.loli.net/2021/05/23/tHy76qjJxMCNLeV.png)

     举例：history对象

     ```js
     $router.push({path:'home'});  // 本质是向history栈中添加一个路由，在我们看来是 切换路由，但本质是在添加一个history记录
     ```

     方法：

     ```js
     $router.replace({path:'home'});  // 替换路由，没有历史记录
     ```

## 2.动态路由

代码示例：

![](https://i.loli.net/2021/05/23/MRqg8TNYynwb74h.png)

首先配置首页路径，其路径为固定"/"。详情页的路径为"/detail/:id"，不同商品对应不同的id，==:id==为占位符，告诉component要展示的商品，这就是动态路由。detail路由规则中，component组件采用路由懒加载的方式加载路由，用户访问详情页时才加载该组件。

组件中如何获取动态路由规则中的动态id？

- 方式1：通过当前路由规则=={{ $route.params.id }}==，获取数据
- 方式2：路由规则中开启props传参

![](https://i.loli.net/2021/05/23/RfosrUwIHl6BcjT.png)

## 3.嵌套路由

当多个组件中有相同的路由，可以把相同的内容提取到公共的组件中。如下图所示，加入首页、详情页有相同的头和尾，这时可以提取新的组件layout，把头和尾放到layout组件中，中间部分动态变化的使用router-view占位。访问首页时，将index组件和layout组件合并输出。

![](https://i.loli.net/2021/05/23/bjdzc3Pn2vfoxCM.png)

由于首页和详情页面有相同的头和尾，所以将相同的头和尾提取到components中的layout.vue组件中。

![](https://i.loli.net/2021/05/23/L9TMSi1aumeFjYt.png)

Index.vue、Detail.vue、Login.vue

```vue
<!-- -------------------------------Index.vue------------------------------- -->
<template>
  <div>
    这里是首页 <br>
    <router-link to="login">登录</router-link> |

    <router-link to="detail/5">详情</router-link>
  </div>
</template>

<script>
export default {
  name: 'Index'
}
</script>

<style>

</style>

<!-- -------------------------------Detail.vue------------------------------- -->
<template>
  <div>
    <!-- 方式1： 通过当前路由规则，获取数据 -->
    通过当前路由规则获取：{{ $route.params.id }}

    <br>
    <!-- 方式2：路由规则中开启 props 传参 -->
    通过开启 props 获取：{{ id }}
  </div>
</template>

<script>
export default {
  name: 'Detail',
  props: ['id']
}
</script>

<style>

</style>


<!-- -------------------------------Login.vue------------------------------- -->
<template>
  <div>
    这是登录页面
    <br>
    <router-link to="/">首页</router-link>
  </div>
</template>

<script>
export default {
  name: 'Login'
}
</script>

<style scoped>
</style>

```

路由规则**router/index.js**

路由规则中，首先配置的登录页面，当访问登陆页面时，直接加载Login组件。因为首页和详情页有相同的头和尾，而头和尾都提取到layout组件中，所以这里使用了**嵌套路由**，嵌套路由中会将外部的path与children中的path进行合并，分别加载Layout组件和Index组件，把他们合并到一起。

当嵌套路由中的path为根路径时，Index组件中的path可以写为空字符串。children中的path可以写为相对路径，也可以写为绝对路径，空字符串为相对路径。当访问根时，先加载Layout，再去加载Index，合并到一起进行渲染。

访问详情页时，外面的路径为根路径，Detail中配置的路径为相对路径，路径拼接后："/detail/:id"，合并Layout和Detail后渲染出来。

![](https://i.loli.net/2021/05/23/rFhfvWHYicSLPDR.png)

浏览器访问效果：

![](https://i.loli.net/2021/05/23/y86emD4zdM1UoIk.png)

![](https://i.loli.net/2021/05/23/myjW7eVwtZoIR4u.png)

![](https://i.loli.net/2021/05/23/pU19vKumQa5Hhln.png)

## 4.编程式导航

编程式导航[**官方文档**](https://router.vuejs.org/zh/guide/essentials/navigation.html)

之前在页面跳转时使用`router-link`形成超链接，但是在登陆页面时需要点击按钮跳转到首页，这时就需要使用编程式导航，调`用$router.push()`方法。

- Login.vue中，按钮button绑定方法push方法，内部使用`this.$router.push('/')`方法跳转到首页。使用push方法时参数接受有两种方式：
  - 第一种方式是字符串-跳转的路由地址
  - 第二种方式是对象，对象为{ name: 'Home' }，其中name来源于router/index.js中路由规则中的name属性，如图：

  ![](https://i.loli.net/2021/05/23/1kCXnyGANKsHPgt.png)

- Index.vue中，两个按钮分别绑定replace和getDetail方法。replace方法与push方法类似，都可以跳转到指定的路径，它们的参数形式也是一样的，但是replace方法不会记录历史，它会将当前的地址直接替换为'/login'地址。

  push方法传递路由参数，首先需要指定跳转的路由名称`name: 'Detail'`，接着使用params指定路由参数。

- Detail.vue中使用go方法：跳转到历史中的某一次路径，它可以使负数，也就是后退，当参数为-1时与`$router.back()`方法效果相同。

![](https://i.loli.net/2021/05/23/ReDFIjCUOL2bn3z.png)

## 5.Hash 模式和 History 模式的区别

`vue-router`默认hash模式——使用URL的hash来模拟一个完整的URL，于是当URL改变时，页面不会重新加载。

如果不想要很丑的hash，可以使用路由的history模式，这种模式充分利用`history.pushState` API来完成URl跳转而无需重新加载页面。

```js
const router = new VueRouter({
  mode: 'history',
  routes: [...]
})
```

当时用history模式时，URL就像正常的url，例如：

`http://blog.5coder.cn/user/id`，也好看！

不过这种模式要玩好，还需要后台配置支持。因为我们的应用是个单页客户端应用，如果后台没有正确的配置，当用户在浏览器直接访问 `http://oursite.com/user/id` 就会返回 404，这就不好看了。

所以呢，你要在服务端增加一个覆盖所有情况的候选资源：如果 URL 匹配不到任何静态资源，则应该返回同一个 `index.html` 页面，这个页面就是你 app 依赖的页面。

![](https://i.loli.net/2021/05/23/qtNlXpJ9RYM2EVr.png)

![](https://i.loli.net/2021/05/23/tKYyfsveLOjhpWa.png)

## 6.History 模式

History模式的使用

- History需要服务器的支持
- 单页应用中，服务端不存在`http://www.testurl.com/login`这样的地址会返回找不到该页面
  - vue-cli自带的web服务器已经配置好了对history模式的支持，所以无法演示，后面会在node和nginx服务器中进行演示
- 在服务端应该出了静态资源外都返回单页应用的index.html

![](https://i.loli.net/2021/05/23/zUIkK7wQBPMEfXq.png)

![](https://i.loli.net/2021/05/23/BzTIUiLqoE8nVQf.png)

## 7.History 模式 - Node.js

接下来通过node开发的web服务器演示vue-router的history模式。项目目录结构如下：

![](https://i.loli.net/2021/05/23/fg1S8CBbacz9djL.png)

express开发的Web服务器：

```js
const path = require('path')
// 导入处理 history 模式的模块
const history = require('connect-history-api-fallback')
// 导入 express
const express = require('express')  // express是基于node的一个web开发框架

const app = express()
// 注册处理 history 模式的中间件
app.use(history())
// 处理静态资源的中间件，网站根目录 ../web
app.use(express.static(path.join(__dirname, '../web')))

// 开启服务器，端口是 3000
app.listen(3000, () => {
  console.log('服务器开启，端口：3000')
})
```

使用`node app.js`启动web服务器，在浏览器中访问`localhost:3000`地址，当app.js中注释掉app.use(history())时，切换至About页面，F5刷新浏览器后，此时浏览器要向服务器发送请求，请求当前地址**'/adbot'**，而在node的服务器中并没有处理这个地址，所以这个时候node服务器输出一个默认的404页面。

当启用history插件时，再次刷新about页面，服务器会判断当前请求的页面服务器上没有，它会把单页应用默认的首页index.html返回给浏览器，浏览器接收到这个页面之后，会再去判断路由地址，发现是about，于是会加载about组件对应的内容，并且把它渲染浏览器上来，这是history执行的一个过程。

## 8.History 模式 - nginx

nginx服务器配置

- 从官网下载nginx的压缩包
- 把压缩包解压到指定目录
- 打开命令行，切换至刚才解压的目录
- 命令行启动nginx
  - start nginx 启动nginx
  - nginx -s reload 重启nginx（修改nginx配置文件后需要重启nginx服务器）
  - nginx -s stop 停止nginx

安装好的nginx目录如下图：

![](https://i.loli.net/2021/05/23/YKlEoP5nA19qufX.png)

![](https://i.loli.net/2021/05/23/C1msbSd8tMkJvVI.png)

命令行中启动nginx `start nginx.ext`，启动后在浏览器中访问localhost，如果现实下图则证明启动成功。

![](https://i.loli.net/2021/05/23/R7ibO1FAXe4chnU.png)

将打包好的dist目录内容拷贝到nginx/html目录中，再次刷新浏览器localhost路径可以看到刚才写的index.html，并且about、video都是可以正常进行跳转的。

![](https://i.loli.net/2021/05/23/znI5TCDBEf4Fyks.png)

当浏览器地址为localhost/about或者localhost/video时，刷新浏览器会出现404，如下图，因为nginx并未处理vue-router的history模式，当刷新时，服务器中不存在请求路径中对应的文件，所以服务器会返回404页面。

![](https://i.loli.net/2021/05/23/Bg1tbz3smwUScDK.png)

nginx解决vue-router的history模式，需要修改nginx/conf/nginx.conf的文件内容，如下：

![](https://i.loli.net/2021/05/23/jrvlKg8cza564SW.png)

修改nginx.conf后，需要重启nginx——`nginx -s reload`，再次刷新浏览器，发现nginx并未返回404页面，其工作的原理是：

nginx服务器会判断当前请求的页面服务器上不存在，它会把单页应用默认的首页index.html返回给浏览器，浏览器接收到这个页面之后，会再去判断路由地址，发现是about，于是会加载about组件对应的内容，并且把它渲染浏览器上来，这是history执行的一个过程。

## 9.VueRouter 实现原理

vue-router有两种模式，一种是hash模式，另外一种是history模式，此处使用history模式来模拟，hash模式可以自己实现，差别很小。

在模拟实现vue-router时会用到vue的一些基本概念，例如：

- 插件
- 混入mixin
- Vue.observable()
- 插槽
- render函数
- 运行时和完整版的Vue

### Hash模式

URL中 `#` 后面的内容作为路径地址，可以直接通过`location.url()`来切换URL地址，如果只改变路径中 `#` 后面的内容，浏览器不会向服务器请求对应的地址，但是会将该地址记录至访问历史中。

当hash改变后，需要监听hash的变化并做相应的处理，只需要监听`hashchange`事件。当hash改变后，会触发`hashchange`事件，在该事件记录当前的路由地址并找到该路径对应的组件然后重新渲染。

### History模式

history模式的路径就是一个普通的url，调用`history.pushState()`方法来改变地址栏，`pushState`方法仅仅改变当前地址栏并保存到浏览器的访问历史中，并不会真正的跳转到指定路径去向服务器请求。

通过监听`popstate`事件，可以监听到浏览器历史操作的变化。在`popstate`事件的处理函数中，可以记录改变后的地址。需要注意的是，当调用`pushState`或`replaceState`时并不会触发该事件。当点击浏览器的前进和后退按钮的时候，或者调用`history.back()`或`history.forword()`方法时，该事件才会被触发。当地址改变之后，根据当前路由地址找到对应组件重新渲染。

## 10.VueRouter 模拟实现-分析

```js
// router/index.js
// 注册插件 Vue.use()接受两种参数：
// 1.函数：Vue.use()内部直接调用函数
// 2.对象: Vue.use()内部调用对象的install方法
Vue.use(VueRouter)
// 创建路由对象，后续模拟时需要创建静态的install方法
const router = new VueRouter({
    routes: [
        {name: 'home', path: '/', component: homeComponent}
    ]
})


// main.js
// 创建Vue实例，注册router对象
new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
```

![](https://i.loli.net/2021/05/24/V9dtQF68YLa5rzX.png)

## 11.VueRouter-install

```js
let _Vue = null
export default class VueRouter{
    // 静态方法install，Vue.use()调用install方法时会传入两个参数：
    // 一个是Vue构造函数
    // 另一个个是可选的选项对象
    static install(Vue) {
        // 1. 判断当前插件是否被安装
        if (VueRouter.install.installed) {
            return
        }
        VueRouter.install.installed = true
        // 2. 把Vue的构造函数记录在全局
        // 把vue的构造函数记录到全局变量中，因为当前的install方法是一个静态方法，在这个静态方法中，接收的一个
        // 参数Vue的构造函数，将来在Vue中的一些实例方法中要使用这个Vue的构造函数。
        // 比如创建router-link和router-view这两个组件时调用vue.component()来创建，所以需要把Vue的构造函数给他记录到全局变量中
        _Vue = Vue
        // 3. 把创建Vue实例时传入的router对象注入到Vue实例
        // 把创建vue实例时传入的router对象，注入到所有的Vue实例上，之前所使用的this.$router就是在这个时候注入到Vue实例上的，
        // 所有的组件也都是vue的实例
        // _Vue.prototype.$router = this.$options.router  // 此时通过VueRouter.install()来调用，此时this指向VueRouter这个类，而不是Vue实例
        _Vue.mixin({
            beforeCreate() {
                // 此时能获取到Vue实例，this的指向为Vue实例
                if (this.$options.router) {  // 判断的作用是防止所有的组件都执行beforeCreate函数去注如
                    _Vue.prototype.$router = this.$options.router  // 从传入的选项中获取router属性
                }
            }
        })
    }
}
```

## 12.VueRouter-构造函数

构造函数需要接收一个参数options对象，其返回值是VueRouter对象。构造函数中需要初始化三个属性，分别是options、routeMap、data属性。data是一个响应式的对象，因为data中要存储当前的路由地址，当路由变化的时候要自动加载组件，所以data需要设置成响应式的对象。

```js
let _Vue = null
export default class VueRouter {
    // 静态方法install，Vue.use()调用install方法时会传入两个参数：...
    static install(Vue) {...}

    constructor(options) {
        this.options = options  // 记录构造函数中传入的选项options
        // 作用是将options中传入的路由规则-routes解析出来，存储到routeMap对象中，routeMap对象是键值对的形式，
        // 键为路由地址，值为路由组件，在router-view组件中会根据当前的路由地址来routeMap里边找到对应的组件，把它渲染到浏览器中。
        this.routeMap = {}
        
        // data是响应式的对象,其中有属性current，用来记录当前的路由地址。默认情况下当前的路由地址是'/',就是根目录。
        // Vue提供了一个方法vue.observable,该方法的作用是用来创建响应式对象。使用observable方法创建的响应式的对象可以直接用在渲染函数或者计算属性。
        this.data = _Vue.observable({
            current: '/'
        })
    }
}
```

## 13.VueRouter-createRouteMap



## 14.VueRouter-router-link



## 15.VueRouter-完整版的 Vue



## 16.VueRouter-render

## 17.VueRouter-router-view

## 18.VueRouter-initEvent