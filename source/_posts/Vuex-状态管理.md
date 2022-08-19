---
title: Vuex 状态管理
author: 5coder
tags: Vuex
category: 大前端
keywords: Vuex
abbrlink: 31096
date: 2021-07-19 21:22:53
top:
cover:


---

# Vuex状态管理

## 课程目标

- 组件通信方式回顾
- Vuex核心概念和基本使用
- 购物车案例
- 模拟实现Vuex

## 组件内的状态管理流程

Vue最核心的两个功能：数据驱动和组件化

组件化开发给我们带来了：

- 更快的开发效率
- 更好的可维护性

每个组件都有自己的状态、视图和行为等组成部分

```js
new Vue({
// state
  data () {
    return {
      count: 0
    }
  },
// view
  template: `
<div>{{ count }}</div>
`,
// actions
  methods: {
    increment () {
      this.count++
    }
  }
})
```

状态管理包含一下几部分：

- **state**，驱动应用的数据源
- **view**，以声明方式将state映射到视图
- **actions**，响应在view上的用户输入导致的状态变化

![](http://5coder.cn/img/image-20210719213045881.png)

## 组件间通信方式回顾

大多数场景下的组件都并不是独立存在的，而是相互协作共同构成了一个复杂的业务功能。在 Vue 中为不同的组件关系提供了不同的通信规则。

![](http://5coder.cn/img/image-20210719213508962.png)

### [父传子：Props Down](https://cn.vuejs.org/v2/guide/components.html#%E9%80%9A%E8%BF%87-Prop-%E5%90%91%E5%AD%90%E7%BB%84%E4%BB%B6%E4%BC%A0%E9%80%92%E6%95%B0%E6%8D%AE)

- 子组件中通过props接受数据
- 父组件中给子组件通过相应属性传值

> **Props**
>
> [Prop 的大小写 (camelCase vs kebab-case)](https://cn.vuejs.org/v2/guide/components-props.html#Prop-的大小写-camelCase-vs-kebab-case)
>
> HTML 中的 attribute 名是大小写不敏感的，所以浏览器会把所有大写字符解释为小写字符。这意味着当你使用 DOM 中的模板时，camelCase (驼峰命名法) 的 prop 名需要使用其等价的 kebab-case (短横线分隔命名) 命名：
>
> ```js
> Vue.component('blog-post', {
> // 在 JavaScript 中是 camelCase 的
> props: ['postTitle'],
> template: '<h3>{{ postTitle }}</h3>'
> })
> ```
>
> ```html
> <!-- 在 HTML 中是 kebab-case 的 -->
> <blog-post post-title="hello!"></blog-post>
> ```
>
> 重申一次，如果你使用字符串模板，那么这个限制就不存在了。
>
> [Prop 类型](https://cn.vuejs.org/v2/guide/components-props.html#Prop-类型)
>
> 到这里，我们只看到了以字符串数组形式列出的 prop：
>
> ```js
> props: ['title', 'likes', 'isPublished', 'commentIds', 'author']
> ```
>
> 但是，通常你希望每个 prop 都有指定的值类型。这时，你可以以对象形式列出 prop，这些 property 的名称和值分别是 prop 各自的名称和类型：
>
> ```js
> props: {
>   title: String,
>   likes: Number,
>   isPublished: Boolean,
>   commentIds: Array,
>   author: Object,
>   callback: Function,
>   contactsPromise: Promise // or any other constructor
> }
> ```
>
> 这不仅为你的组件提供了文档，还会在它们遇到错误的类型时从浏览器的 JavaScript 控制台提示用户。你会在这个页面接下来的部分看到[类型检查和其它 prop 验证](https://cn.vuejs.org/v2/guide/components-props.html#Prop-验证)。



![](http://5coder.cn/img/image-20210719213708568.png)

![](http://5coder.cn/img/image-20210719213815350.png)

### [子传父：Event Up](https://cn.vuejs.org/v2/guide/components.html#%E7%9B%91%E5%90%AC%E5%AD%90%E7%BB%84%E4%BB%B6%E4%BA%8B%E4%BB%B6)

![](http://5coder.cn/img/image-20210720054418797.png)

![](http://5coder.cn/img/image-20210720054522110.png)

### [非父子组件：Event Bus](https://cn.vuejs.org/v2/guide/migration.html#dispatch-%E5%92%8C-broadcast-%E6%9B%BF%E6%8D%A2)

我们可以使用一个非常简单的Event Bus来解决这个问题：

eventbus.js

```js
export default new Vue()
```

然后在需要通信的两端：

使用`$on`订阅：

```js
// 没有参数
bus.$on('自定义事件名称', () => {
  // 执行操作
})

// 有参数
bus.$on('自定义事件名称', data => {
  // 执行操作
})
```

使用`$emit`发布：

```js
// 没有自定义传参
bus.$emit('自定义事件名称')

// 有自定义传参
bus.$emit('自定义事件名称', 参数数据)
```

### [父直接访问子组件：通过ref获取子组件](https://cn.vuejs.org/v2/guide/components-edge-cases.html#%E8%AE%BF%E9%97%AE%E5%AD%90%E7%BB%84%E4%BB%B6%E5%AE%9E%E4%BE%8B%E6%88%96%E5%AD%90%E5%85%83%E7%B4%A0)

`ref`有两个作用：

- 如果把它作用到**普通HTML标签上，则获取的是DOM**
- 如果把它作用到**组件标签上，则获取到的是组件实例**

创建`base-input`

```html
<template>
  <div><h1>ref Child</h1>    <input ref="input" type="text" v-model="value"></div>
</template>
<script>export default {
  data() {
    return {value: ''}
  }, methods: {
    focus() {
      this.$refs.input.focus()
    }
  }
}</script>
```

在使用子组件的时候，添加`ref`属性：

```html
<base-input ref='usernameInput'></base-input>
```

然后在父组件等渲染完毕后使用`$refs`访问：

```js
mounted() {
  this.$refs.usernameInput.focus()
}
```

> `$refs`只会在组件渲染完成之后生效，并且它们不是响应式的。这仅作为一个用于直接操作子组件的“逃生舱”——你应该避免在模板或计算属性中访问`$refs`

## 简易的状态管理方案

如果多个组件之间要共享状态（数据），使用上面的方式虽然可以实现，但是比较麻烦，而且多个组件之间互相传值很难跟踪数据的变化，如果出现问题很难定位问题。

当遇到多个组件需要共享状态的时候，典型的场景：购物车。我们如果使用上述的方案都不合适，会遇到以下问题：

- 多个视图依赖同一状态
- 来自不同视图的行为需要变更同一状态

对于问题一，传参的方法对于多层嵌套的组件将会非常繁琐，并且对于兄弟组件间的状态传递无能为力。

对于问题二，我们经常会采用父子组件直接引用或者通过事件来变更和同步状态的多份拷贝。以上的这些模式非常脆弱，通常会导致无法维护的代码。

因此，我们为什么不把组件的共享状态抽取出来，以一个全局单例模式管理呢？在这种模式下，我们的组件树构成了一个巨大的“视图”，不管在树的哪个位置，任何组件都能获取状态或者触发行为！

通过定义和隔离状态管理中的各种概念并通过强制规则维持视图和状态间的独立性，我们的代码将会变得更结构化且易维护。

我们可以把多个组件的状态，或者整个程序的状态放到一个集中的位置存储，并且可以检测到数据的更改。你可能已经想到了 `Vuex`。

这里我们先以一种简单的方式来实现

- 首先创建一个共享的仓库 `store` 对象

```js
export default {
  debug: true,
  state: {
    user: {
      name: 'xiaomao',
      age: 18,
      sex: '男'
    }
  },
  setUserNameAction (name) {
    if (this.debug) {
      console.log('setUserNameAction triggered：', name)
    }
    this.state.user.name = name
  }
}
```

- 把共享的仓库 `store` 对象，存储到需要共享状态的组件的 `data` 中

```html
<template>
  <div>
    <h1>componentA</h1>
    user name: {{ sharedState.user.name }}
    <button @click="change">Change Info</button>
  </div>
</template>

<script>
import store from './store'
export default {
  methods: {
    change () {
      store.setUserNameAction('componentA')
    }
  },
  data () {
    return {
      privateState: {},
      sharedState: store.state
    }
  }
}
</script>
```

接着我们继续延伸约定，组件不允许直接变更属于 `store` 对象的 `state`，而应执行 `action` 来分发(`dispatch`) 事件通知 `store` 去改变，这样最终的样子跟 `Vuex` 的结构就类似了。这样约定的好处是，我们能够记录所有 `store` 中发生的 `state` 变更，同时实现能做到记录变更、保存状态快照、历史回滚/时光旅行的先进的调试工具。

## Vuex回顾

### [什么是Vuex](https://vuex.vuejs.org/zh/)

> [Vuex](https://vuex.vuejs.org/zh/) 是一个专为 Vue.js 应用程序开发的**状态管理模式**。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。Vuex 也集成到 Vue 的官方调试工具 [devtools extension](https://github.com/vuejs/devtools)，提供了诸如零配置的 `time-travel` 调试、状态快照导入导出等高级调试功能。

- Vuex 是专门为 Vue.js 设计的状态管理库
- 它采用集中式的方式存储需要共享的数据
- 从使用角度，它就是一个 JavaScript 库
- 它的作用是进行状态管理，解决复杂组件通信，数据共享

### 什么情况下使用Vuex

> 官方文档：
>
> Vuex 可以帮助我们管理共享状态，并附带了更多的概念和框架。这需要对短期和长期效益进行权衡。
>
> 如果您不打算开发大型单页应用，使用 Vuex 可能是繁琐冗余的。确实是如此——如果您的应用够简单，您最好不要使用 Vuex。一个简单的 [store](https://cn.vuejs.org/v2/guide/state-management.html#%E7%AE%80%E5%8D%95%E7%8A%B6%E6%80%81%E7%AE%A1%E7%90%86%E8%B5%B7%E6%AD%A5%E4%BD%BF%E7%94%A8) 模式就足够您所需了。但是，如果您需要构建一个中大型单页应用，您很可能会考虑如何更好地在组件外部管理状态，Vuex 将会成为自然而然的选择。引用 Redux 的作者 Dan Abramov 的话说就是：Flux 架构就像眼镜：您自会知道什么时候需要它。

当你的应用中具有以下需求场景的时候：

- 多个视图依赖于同一状态
- 来自不同视图的行为需要变更同一状态

建议符合这种场景的业务使用 Vuex 来进行数据管理，例如非常典型的场景：购物车。

**注意：Vuex 不要滥用，不符合以上需求的业务不要使用，反而会让你的应用变得更麻烦。**

### 核心概念回顾

![](http://5coder.cn/img/vuex.png)

- `Store`:仓库，`store`是使用`Vuex`应用程序的核心，每一个应用仅有一个`store`。`store`是一个容器，包含应用中的大部分状态，当然我们不能直接改变`store`中的应用状态，我们需要通过提交`mutation`的方式改变状态。
- `State`：就是状态，保存在store中。因为`store`是唯一的，所以`state`状态也是惟一的，称为单一状态树。但是所有的状态都保存在`state`中的话，会让程序难以维护，可以通过后续的模块解决该问题。
  - 注意：这里的`state`状态是响应式的
- `Getter`：`getter`就像是`Vuex`中的计算属性，方便从一个属性派生出其他的值，它内部可以对计算的结果进行缓存，只有当内部依赖的`state`状态发生改变时才会重新计算。
- `Mutation`：`state`状态的变化必须要通过提交`mutation`来完成
- `Action`：`action`和`mutation`类似，不同的是`action`可以进行异步的操作，内部改变状态的时候都需要提交`mutation`
- `Module`：由于使用单一状态树，应用的所有状态会集中到一个比较大的对象上来，当应用变得十分复杂时，，`store`对象就有可能编的相当臃肿。为了解决以上问题，`Vuex`允许我们将`store`分隔成模块，每个模块拥有自己的`state`、`mutation`、`action`、`getter`甚至是嵌套的子模块

#### 示例演示

使用`vue create vuex-demo`创建包含router和vuex的空项目

#### 基本结构

`src/store/index.js`

```js
import Vue from 'vue'
// 1.导入Vuex
import Vuex from 'vuex'

// 2.注册Vuex
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
```

`src/main.js`

```js
import Vue from 'vue'
import store from './store'

Vue.config.productionTip = false

new Vue({
  store,  // 3.注入$store到Vue实例
  render: h => h(App)
}).$mount('#app')
```

#### [State](https://vuex.vuejs.org/zh/guide/state.html#state)

`Vuex`使用单一状态树，用一个对象就包含了全部的应用层级状态。

使用`mapState`简化`State`在视图中的使用，[mapState](https://vuex.vuejs.org/zh/guide/state.html#mapstate-%E8%BE%85%E5%8A%A9%E5%87%BD%E6%95%B0)返回计算属性

`mapState`有两种使用方式：

- **接收数组参数**

  ```js
  // 该方式是Vuex提供的，所以使用前需要先导入
  import { mapState } from 'vuex'
  // mapState返回名称为count和msg的计算属性
  // 在模板中直接使用count和msg
  computed: {
    ...mspState(['count', 'msg'])
  }
  ```

  使用数组参数

  ```html
  <h1>Vuex - Demo</h1>
  <!--    count: {{ $store.state.count }}<br>-->
  <!--    msg: {{ $store.state.msg }}-->
  
  count: {{ count }}<br>
  msg: {{ msg }}
  ```

- **接受对象参数**

  如果当前视图中已经有了`count`和`msg`，如果使用上述方式的话会有命名冲突，解决的方式：

  ```js
  import {mapState} from 'vuex'
  
  export default {
    computed: {
      // count: state => state.count
      // ...mapState(['count', 'msg'])
      ...mapState({num: 'count', message: 'msg'})    // 当store中存在count和msg时，使用对象参数重命名count和msg
    }
  }
  ```
  
  使用对象参数
  
  ```html
  <h1>Vuex - Demo</h1>
  count: {{ num }}<br>
  msg: {{ message }}
  ```

#### [Getter](https://vuex.vuejs.org/zh/guide/getters.html#getter)

`Getter`就是`store`中的计算属性，使用[mapGetter](https://vuex.vuejs.org/zh/guide/getters.html#mapgetters-%E8%BE%85%E5%8A%A9%E5%87%BD%E6%95%B0)简化视图中的使用

`App.vue`

```js
import {mapGetters, mapState} from 'vuex'

export default {
  computed: {
    // count: state => state.count
    // ...mapState(['count', 'msg'])
    ...mapState({num: 'count', message: 'msg'}),
    ...mapGetters(['reverseMsg'])
  }
}
```

使用

```html
<h2>Getter</h2>
<!--    reverseMsg: {{ $store.getters.reverseMsg }}-->
reverseMsg: {{ reverseMsg }}
```

`src/store/index.js`

```js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        count: 1,
        msg: 'Hello Vuex'
    },
    getters: {
        reverseMsg(state) {
            return state.msg.split('').reverse().join('')
        }
    },
    mutations: {
    },
    actions: {
    },
    modules: {}
})
```

#### [Mutation](https://vuex.vuejs.org/zh/guide/mutations.html#mutation)

更改`Vuex`的`store`中的状态的唯一方法是提交`mutation`。`Vuex`中的`mutation`非常类似于事件：每个`mutation`都有一个**字符串的事件类型（type）**和**一个回调函数（handler）**。这个回调函数就是我们实际进行状态更改的地方，并且它会接受`state`作为第一个参数。

使用`Mutation`改变状态的好处是：集中的一个位置对状态修改，不管在什么地方修改，都可以追踪到状态的修改。可以实现高级的**time-travel**调试功能

`App.vue`

```js
import {mapGetters, mapMutations, mapState} from 'vuex'

export default {
  computed: {
    // count: state => state.count
    // ...mapState(['count', 'msg'])
    ...mapState({num: 'count', message: 'msg'}),
    ...mapGetters(['reverseMsg']),
  },
  methods: {
    ...mapMutations(['increate'])
  }
}
```

使用

```html
<h2>Mutation</h2>
<!--    <button @click="$store.commit('increate', 2)">Mutation</button>-->
<button @click="increate(3)">Mutation</button>
```

`src/store/index.js`

```js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        count: 1,
        msg: 'Hello Vuex'
    },
    getters: {
        reverseMsg(state) {
            return state.msg.split('').reverse().join('')
        }
    },
    mutations: {
        increate(state, payload) {
            state.count += payload
        }
    },
    actions: {},
    modules: {}
})

```

![vuex](http://5coder.cn/img/vuex.gif)

#### [Action](https://vuex.vuejs.org/zh/guide/actions.html#action)

`Action`类似于`mutation`，不同在于：

- `Action`提交的是`mutation`，而不是直接变更状态
- `Action`可以包含任意异步操作

`App.vue`

```js
import {mapActions, mapGetters, mapMutations, mapState} from 'vuex'

export default {
  computed: {
    // count: state => state.count
    // ...mapState(['count', 'msg'])
    ...mapState({num: 'count', message: 'msg'}),
    ...mapGetters(['reverseMsg']),
  },
  methods: {
    ...mapMutations(['increate']),
    ...mapActions(['increateAsync'])
  }
}
```

使用

```html
<h2>Action</h2>
<!--    <button @click="$store.dispatch('increateAsync', 5)">Action</button>-->
<button @click="increateAsync(5,1)">Action</button>
```

`src/store/index.js`

```js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        count: 1,
        msg: 'Hello Vuex'
    },
    getters: {
        reverseMsg(state) {
            return state.msg.split('').reverse().join('')
        }
    },
    mutations: {
        increate(state, payload) {
            state.count += payload
        }
    },
    actions: {
        increateAsync(context, payload) {
            console.log(payload)
            setTimeout(() => {
                context.commit('increate', payload)
            }, 2000)
        }
    },
    modules: {}
})

```

#### Module

由于使用单一状态树，应用的所有状态会集中到一个比较大的对象。当应用变得非常复杂时，store 对象就有可能变得相当臃肿。

为了解决以上问题，Vuex 允许我们将 store 分割成模块（module）。每个模块拥有自己的 state、mutation、action、getter、甚至是嵌套子模块。在案例中体会 Module 的使用。

目录结构：

![](http://5coder.cn/img/image-20210720231254540.png)

![](http://5coder.cn/img/image-20210720231711492.png)

#### 严格模式

之前在介绍核心概念时说过，所有的状态变更必须通过提交`mutation`，但是这仅仅是一个**约定**。如果你想的话，可以在组建中随时获取`$store.state.msg`，对它进行修改。从语法层面来说，这是没有问题的，但是这样操作破坏了`Vuex`的约定。如果在组件中直接修改`state`，那在`dev-tools`中无法追踪状态的变更。开启严格模式之后，如果在组件中直接修改`state`状态，会抛出错误。演示如下：

`store/index.js`中添加`strict: true`

![](http://5coder.cn/img/image-20210721055156446.png)

在`App.vue`中添加如下代码，点击按钮直接修改`store`中`state.msg`的值

![image-20210721055240615](http://5coder.cn/img/image-20210721055240615.png)

打开浏览器进行测试，发现$store.state.msg的值确实被修改了，但是console中会抛出异常。

![](http://5coder.cn/img/image-20210721055417299.png)

需要注意的是：不要再生产模式下开启严格模式，严格模式会深度检查状态树，来检查不合规的状态改变，会影响性能。可以再开发环境中启用严格模式，在生产模式下关闭严格模式。调整后的代码：

- 当`npm run serve`时，`process.env.NODE_ENV`为`development`开发环境；
- 当`npm run build`时，`process.env.NODE_ENV`是`production`。这样就可以根据环境来动态的设置严格模式。

![](http://5coder.cn/img/image-20210721055707152.png)

## 购物车案例

接下来我们通过一个购物车案例来演示 Vuex 在项目中的使用方式，首先把购物车的项目模板下载下来。

[模板地址](https://github.com/goddlts/vuex-cart-demo-template.git)

案例演示

![cart](http://5coder.cn/img/cart.gif)

server.js，在访问数据时，必须先使用`node server.js`启动server接口

```js
const express = require('express')
const cors = require('cors')
const app = express()

app.use(cors())

const hostname = '127.0.0.1'
const port = 3000

const _products = [
  { id: 1, title: 'iPad Pro', price: 500.01 },
  { id: 2, title: 'H&M T-Shirt White', price: 10.99 },
  { id: 3, title: 'Charli XCX - Sucker CD', price: 19.99 }
]

app.use(express.json())

app.get('/products', (req, res) => {
  res.status(200).json(_products)
})

app.post('/checkout', (req, res) => {
  res.status(200).json({
    success: Math.random() > 0.5
  })
})

app.listen(port, hostname, () => {
  console.log(`Server is running at http://${hostname}:${port}/`)
})

```



### 功能列表

- 商品列表组件
- 商品列表中弹出框组件（购物车弹出框）
- 购物车列表组件

### 商品列表

#### 商品列表功能

- Vuex中创建两个模块，分别用来记录商品列表和购物车的状态，`stroe`的结构：

  ```txt
  store
  	--modules
  		cart.js
  		products.js
  	index.js
  ```

- `products`模块，`store/modules/products.js`

```js
import axios from 'axios'
const state = {
  products: []
}
const getters = {}
const mutations = {}
const actions = {
  async getProducts ({ commit }) {
    const { data } = await axios({
      method: 'GET',
      url: 'http://127.0.0.1:3000/products'
    })
    commit('setProducts', data)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}

```

- `store/index.js`中注册`products.js`模块

```js
import Vue from 'vue'
import Vuex from 'vuex'
import products from './modules/products'
import cart from './modules/cart'

Vue.use(Vuex)

const myPlugin = store => {
  store.subscribe((mutation, state) => {
    if (mutation.type.startsWith('cart/')) {
      window.localStorage.setItem('cart-products', JSON.stringify(state.cart.cartProducts))
    }
  })
}

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    products,
    cart
  },
  plugins: [myPlugin]
})

```

- `views/products.vue`中实现商品列表的功能

```html
<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item><a href="#/">首页</a></el-breadcrumb-item>
      <el-breadcrumb-item><a href="#/">商品列表</a></el-breadcrumb-item>
    </el-breadcrumb>
    <el-table
      :data="products"
      style="width: 100%">
      <el-table-column
        prop="title"
        label="商品">
      </el-table-column>
      <el-table-column
        prop="price"
        label="价格">
      </el-table-column>
      <el-table-column
        prop="address"
        label="操作">
        <!-- <template slot-scope="scope"> -->
        <template v-slot="scope">
          <el-button @click="addToCart(scope.row)">加入购物车</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'
export default {
  name: 'ProductList',
  computed: {
    ...mapState('products', ['products'])
  },
  methods: {
    ...mapActions('products', ['getProducts']),
  },
  created () {
    this.getProducts()
  }
}
</script>

<style></style>

```

#### 添加购物车

- `cart` 模块实现添加购物车功能，`store/modules/cart.js`

```js
const mutations = {
  addToCart (state, product) {
    // 1. cartProducts 中没有该商品，把该商品添加到数组，并增加 count，isChecked，totalPrice
    // 2. cartProducts 有该商品，让商品的数量加1，选中，计算小计
    const prod = state.cartProducts.find(item => item.id === product.id)
    if (prod) {
      prod.count++
      prod.isChecked = true
      prod.totalPrice = prod.count * prod.price
    } else {
      state.cartProducts.push({
        ...product,
        count: 1,
        isChecked: true,
        totalPrice: product.price
      })
    }
  }
}

```

- `store/index.js` 中注册 `cart` 模块

```js
import Vue from 'vue'
import Vuex from 'vuex'
import products from './modules/products'
import cart from './modules/cart'

Vue.use(Vuex)

const myPlugin = store => {
  store.subscribe((mutation, state) => {
    if (mutation.type.startsWith('cart/')) {
      window.localStorage.setItem('cart-products', JSON.stringify(state.cart.cartProducts))
    }
  })
}

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    products,
    cart
  },
  plugins: [myPlugin]
})

```

- `view/products.vue` 中实现添加购物车功能

```js
  methods: {
    ...mapMutations('cart', ['addToCart'])
  },
```

- 测试，通过 vue-devtools 观察数据的变化

### 商品列表-弹出购物车窗口

#### 购物车列表

- `components/pop-cart.vue`中展示购物车列表

```html
<template>
  <el-popover
    width="350"
    trigger="hover"
  >
    <el-table :data="cartProducts" size="mini">
      <el-table-column property="title" width="130" label="商品"></el-table-column>
      <el-table-column property="price" label="价格"></el-table-column>
      <el-table-column property="count" width="50" label="数量"></el-table-column>
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button @click="deleteFromCart(scope.row.id)" size="mini">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div>
      <p>共 {{ totalCount }} 件商品 共计¥{{ totalPrice }}</p>
      <el-button size="mini" type="danger" @click="$router.push({ name: 'cart' })">去购物车</el-button>
    </div>
    <el-badge :value="totalCount" class="item" slot="reference">
      <el-button type="primary">我的购物车</el-button>
    </el-badge>
  </el-popover>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex'
export default {
  name: 'PopCart',
  computed: {
    ...mapState('cart', ['cartProducts']),
    ...mapGetters('cart', ['totalCount', 'totalPrice'])
  },
  methods: {
    ...mapMutations('cart', ['deleteFromCart'])
  }
}
</script>

<style>

</style>

```

#### 删除

- `cart` 模块实现从购物车删除的功能，`store/modules/cart.js`

```js
deleteFromCart (state, prodId) {
  const index = state.cartProducts.findIndex(item => item.id === prodId)
  index !== -1 && state.cartProducts.splice(index, 1)
}
```

- `components/pop-cart.vue` 中实现删除功能

```html
<el-table-column label="操作">
  <template v-slot="scope">
    <el-button @click="deleteFromCart(scope.row.id)" size="mini">删除</el-button>
  </template>
</el-table-column>
```

```js
methods: {
  ...mapMutations('cart', ['deleteFromCart'])
}
```

#### 小计

- `cart` 模块实现统计总数和总价，`store/modules/cart.js`

```js
const getters = {
  totalCount (state) {
    return state.cartProducts.reduce((count, prod) => {
      return count + prod.count
    }, 0)
  },
  totalPrice (state) {
    return state.cartProducts.reduce((count, prod) => {
      return count + prod.totalPrice
    }, 0).toFixed(2)
  }
}
```

- `components/pop-cart.vue` 中显示徽章和小计

```html
<div>
  <p>共 {{ totalCount }} 件商品 共计¥{{ totalPrice }}</p>
  <el-button size="mini" type="danger" @click="$router.push({ name: 'cart' })">去购物车</el-button>
</div>
<el-badge :value="totalCount" class="item" slot="reference">
  <el-button type="primary">我的购物车</el-button>
</el-badge>
```

```js
computed: {
  ...mapState('cart', ['cartProducts']),
  ...mapGetters('cart', ['totalCount', 'totalPrice'])
},
```

### 购物车

#### 购物车列表

```html
<template>
  <el-popover
    width="350"
    trigger="hover"
  >
    <el-table :data="cartProducts" size="mini">
      <el-table-column property="title" width="130" label="商品"></el-table-column>
      <el-table-column property="price" label="价格"></el-table-column>
      <el-table-column property="count" width="50" label="数量"></el-table-column>
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button @click="deleteFromCart(scope.row.id)" size="mini">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div>
      <p>共 {{ totalCount }} 件商品 共计¥{{ totalPrice }}</p>
      <el-button size="mini" type="danger" @click="$router.push({ name: 'cart' })">去购物车</el-button>
    </div>
    <el-badge :value="totalCount" class="item" slot="reference">
      <el-button type="primary">我的购物车</el-button>
    </el-badge>
  </el-popover>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex'
export default {
  name: 'PopCart',
  computed: {
    ...mapState('cart', ['cartProducts']),
    ...mapGetters('cart', ['totalCount', 'totalPrice'])
  },
  methods: {
    ...mapMutations('cart', ['deleteFromCart'])
  }
}
</script>

<style>

</style>

```

#### 全选功能

- `cart` 模块实现更新商品的选中状态，`store/modules/cart.js`

```js
const mutations = {
  addToCart(state, product) {
    // 1. cartProducts 中没有该商品，把该商品添加到数组，并增加 count，isChecked，totalPrice
    // 2. cartProducts 有该商品，让商品的数量加1，选中，计算小计
    const prod = state.cartProducts.find(item => item.id === product.id)
    if (prod) {
      prod.count++
      prod.isChecked = true
      prod.totalPrice = prod.count * prod.price
    } else {
      state.cartProducts.push({
        ...product,
        count: 1,
        isChecked: true,
        totalPrice: product.price
      })
    }
  },
  deleteFromCart(state, prodId) {
    const index = state.cartProducts.findIndex(item => item.id === prodId)
    index !== -1 && state.cartProducts.splice(index, 1)
  },
updateAllProductChecked(state, checked) {
  state.cartProducts.forEach(prod => {
    prod.isChecked = checked
  })
},
updateProductChecked(state, {
  checked,
  prodId
}) {
  const prod = state.cartProducts.find(prod => prod.id === prodId)
  prod && (prod.isChecked = checked)
},
  updateProduct(state, {
    prodId,
    count
  }) {
    const prod = state.cartProducts.find(prod => prod.id === prodId)
    if (prod) {
      prod.count = count
      prod.totalPrice = count * prod.price
    }
  }
}

```

- `views/cart.vue`，实现全选功能
  - [使用事件抛出一个值](https://cn.vuejs.org/v2/guide/components.html#%E4%BD%BF%E7%94%A8%E4%BA%8B%E4%BB%B6%E6%8A%9B%E5%87%BA%E4%B8%80%E4%B8%AA%E5%80%BC)

```html
<el-table-column
  width="55">
  <template v-slot:header>
    <el-checkbox v-model="checkedAll" size="mini">
    </el-checkbox>
  </template>
  <!--
    @change="updateProductChecked"  默认参数：更新后的值
    @change="updateProductChecked(productId, $event)"  123, 原来那个默认参数
      当你传递了自定义参数的时候，还想得到原来那个默认参数，就手动传递一个 $event
   -->
  <template v-slot="scope">
    <el-checkbox
      size="mini"
      :value="scope.row.isChecked"
      @change="updateProductChecked({
        prodId: scope.row.id,
        checked: $event
      })"
    >
    </el-checkbox>
  </template>
</el-table-column>
```

```js
export default {
  name: 'Cart',
  computed: {
    ...mapState('cart', ['cartProducts']),
    ...mapGetters('cart', ['checkedCount', 'checkedPrice']),
    checkedAll: {
      get () {
        return this.cartProducts.every(prod => prod.isChecked)
      },
      set (value) {
        this.updateAllProductChecked(value)
      }
    }
  },
  methods: {
    ...mapMutations('cart', [
      'updateAllProductChecked',
      'updateProductChecked',
      'updateProduct'
    ])
  }
}
```

#### 数组文本框

- `cart` 模块实现更新商品数量，`store/modules/cart.js`

```js
updateProduct(state, {
    prodId,
    count
  }) {
    const prod = state.cartProducts.find(prod => prod.id === prodId)
    if (prod) {
      prod.count = count
      prod.totalPrice = count * prod.price
    }
  }
```

- `views/cart.vue`，实现数字文本框功能

```html
<el-input-number :value="scope.row.count" @change="updateProduct({
            prodId: scope.row.id,
            count: $event
          })" size="mini">
</el-input-number>
```

```js
methods: {
  ...mapMutations('cart', [
    'updateAllProductChecked',
    'updateProductChecked',
    'updateProduct'
  ])
}
```

#### 删除

#### 小计

- `cart` 模块实现统计选中商品价格和数量，`store/modules/cart.js`

```js
checkedCount(state) {
  return state.cartProducts.reduce((sum, prod) => {
    if (prod.isChecked) {
      sum += prod.count
    }
    return sum
  }, 0)
},
checkedPrice(state) {
  return state.cartProducts.reduce((sum, prod) => {
    if (prod.isChecked) {
      sum += prod.totalPrice
    }
    return sum
  }, 0)
}
```

- `views/cart.vue`，实现小计

```html
<div>
  <p>已选 <span>{{ checkedCount }}</span> 件商品，总价：<span>{{ checkedPrice }}</span></p>
  <el-button type="danger">结算</el-button>
</div>
```

```js
computed: {
  ...mapState('cart', ['cartProducts']),
  ...mapGetters('cart', ['checkedCount', 'checkedPrice']),
  checkedAll: {
    get() {
      return this.cartProducts.every(prod => prod.isChecked)
    },
    set(value) {
      this.updateAllProductChecked(value)
    }
  }
}
```

### 本地存储

#### Vuex插件

- `Vuex`的插件就是一个函数
- 这个函数接受一个`store`的参数
- 这个函数内可以注册一个函数，让它可以在`mutaions`之后再执行
- 就像在`axios`中的过滤器，在所有请求之后统一完成一件事

![](http://5coder.cn/img/image-20210721221103084.png)

- `mutation`的结构
  - 如果想在`cart`模块中的`mutation`之行结束之后再来调用调用，`product`模块中不需要，可以使用`mutation`

![](http://5coder.cn/img/image-20210721221642267.png)

- 注册插件

![image-20210721221144978](http://5coder.cn/img/image-20210721221144978.png)

- 最终实现

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  import products from './modules/products'
  import cart from './modules/cart'
  
  Vue.use(Vuex)
  
  const myPlugin = store => {
    // 当store初始化后调用
    // subscribe的作用是用来订阅store中的mutation，会在每个mutation完成之后调用
    // 参数：mutation、state
    // 如果想在cart模块中的mutation之行结束之后再来调用调用，product模块中不需要，可以使用mutation
    store.subscribe((mutation, state) => {
      // 每次调用mutation之后调用
      // mutation的格式为 { type, payload }
      if (mutation.type.startsWith('cart/')) {
        //记录到localStorage
        window.localStorage.setItem('cart-products', JSON.stringify(state.cart.cartProducts))
      }
    })
  }
  
  
  export default new Vuex.Store({
    state: {},
    mutations: {},
    actions: {},
    modules: {
      cart,
      products
    },
    plugins: [myPlugin]
  })
  ```

## Vuex模拟实现

回顾基础示例，自己模拟实现一个`Vuex`实现同样的功能

```js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    count: 0,
    msg: 'Hello World'
  },
  getters: {
    reverseMsg(state) {
      return state.msg.split('').reverse().join('')
    }
  },
  mutations: {
    increate(state, payload) {
      state.count += payload.num
    }
  },
  actions: {
    increate(context, payload) {
      setTimeout(() => {
        context.commit('increate', {num: 5})
      }, 2000)
    }
  }
})
```

### 实现思路

- 实现`install`方法
  - `Vuex`是`Vue`的一个插件，所以和模拟`VueRouter`类似，县实现`Vue`插件约定的`install`方法
- 实现`Store`类
  - 实现构造函数，接受`options`对象参数
  - `state`的响应式处理
  - `getter`的实现
  - `commit`、`dispatch`方法

### install方法

```js
let _Vue = null
function install (Vue) {
  _Vue = Vue
  _Vue.mixin({
    beforeCreate () {
      if (this.$options.store) {
        Vue.prototype.$store = this.$options.store
      }
    }
  })
}
```

### Store类

```js
let _Vue = null

class Store {
  constructor(options) {
    const {
      state = {},
      getters = {},
      mutations = {},
      actions = {}
    } = options

    this.state = _Vue.observable(state)
    // 此处不直接 this.getters = getters，是因为下面的代码中要方法 getters 中的 key
    // 如果这么写的话，会导致 this.getters 和 getters 指向同一个对象
    // 当访问 getters 的 key 的时候，实际上就是访问 this.getters 的 key 会触发 key 属性的getter
    // 会产生死递归
    this.getters = Object.create(null)
    Object.keys(getters).forEach(key => {
      Object.defineProperty(this.getters, key, {
        get: () => getters[key](state)
      })
    })
    this._mutations = mutations
    this._actions = actions
  }

  commit(type, payload) {
    this._mutations[type](this.state, payload)
  }

  dispatch(type, payload) {
    this._actions[type](this, payload)
  }

}

// install方法可以接受两个参数，一个是Vue构造函数，另外一个是额外的选项，这里只需要Vue构造函数
function install(Vue) {
  _Vue = Vue
  _Vue.mixin({
    beforeCreate() {
      // 首先判断当前Vue实例的$options中是否有store，如果是组件实例的话没有store选项，就不需要做这件事
      if (this.$options.store) {
        // 这里注册插件的时候会混入beforeCreate，当创建根实例的时候就会把$store注入到Vue实例上
        _Vue.prototype.$store = this.$options.store
      }
    }
  })
}

export default {
  Store,
  install
}
```

### 使用自己实现的Vuex

`src/store/index.js` 中修改导入 `Vuex` 的路径，测试

```js
import Vuex from '../myvuex'
// 注册插件
Vue.use(Vuex)
```

