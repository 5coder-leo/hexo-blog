---
title: 模拟Vue.js响应式原理
author: 5coder
tags:
  - Vue
  - Vue响应式原理
category: 大前端
keywords: Vue响应式原理
abbrlink: 27165
date: 2021-05-26 05:26:42
password:
top: true
cover:
---

# 模拟 Vue.js 响应式原理

> 摘要：
>
> 接下来学习Vue响应式的原理，其中会模拟实现一个最简单的Vue。下面先来看一段代码，这段代码是Vue最基础的结构，我们要做的事情就是自己实现一个实现相同的效果。模拟的原因是我们都知道在面试的时候，Vue响应式原理是一个必问的问题，通过模拟显示Vue响应式的原理，可以更好的回答这些问题。另外在模拟显示原理的过程中，就是借鉴Vue的源码模拟一个最小版本的Vue，这个过程中可以学习别人优秀的经验，并且把它转化成自己的经验，在实际项目中遇到问题也可以通过原理层面来解决。
>
> ![](http://5coder.cn/img/gkYTl1K65hJvWoQ.png)
>
> 课程目标：
>
> - 模拟一个最小版本的Vue
> - 响应式原理在面试的常见问题
> - 学习别人优秀的经验，转换成自己的经验
> - 实际项目中出问题的原理层面的解决
>   - 给Vue实例新增一个成员是否是响应式的？
>   - 给属性重新赋值成对象，是否是响应式的？
> - 为学习Vue源码做铺垫

## 1.准备工作

- 数据驱动
- 响应式的核心原理
- 发布订阅模式和观察者模式

### 1.1数据驱动

> 数据响应式、双向绑定、数据驱动

- 数据响应式
  - 数据模型仅仅是普通的JavaScript对象，而当修改数据时，视图会进行更新，避免了繁琐的DOM操作，提高开发效率（jQuery的核心是进行DOM操作）
- 双向绑定
  - 数据改变，视图改变；视图改变，数据也随之改变
  - 可以用v-model在表单元素上创建双向数据绑定
- 数据驱动是Vue最独特的特性之一
  - 开发过程中仅需要关注数据本身，不需要关心数据是如何渲染到视图

### 1.2数据响应式的核心原理

#### 数据响应式核心原理-Vue2

- [Vue2.x数据响应式核心原理](https://cn.vuejs.org/v2/guide/reactivity.html)

  当你把一个普通的 JavaScript 对象传入 Vue 实例作为 `data` 选项，Vue 将遍历此对象所有的 property，并使用 [`Object.defineProperty`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty) 把这些 property 全部转为 [getter/setter](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Working_with_Objects#定义_getters_与_setters)。`Object.defineProperty` 是 ES5 中一个无法 shim 的特性，这也就是 Vue 不支持 IE8 以及更低版本浏览器的原因。

- [MDN-Object.defineProperty](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty)

- 浏览器兼容IE8以上（不兼容IE8）

1.defineProperty单个成员

```html
<div id="app">
  hello
</div>

<script>
  // 模拟Vue中的data选项
  let data = {
    msg: 'hello'
  }

  // 模拟Vue实例
  let vm = {}

  // 数据劫持： 当访问或者设置vm中的成员的时候，做一些干预操作
  Object.defineProperty(vm, 'msg', {
    // 可枚举（可遍历）
    enumerable: true,
    // 可配置（可以使用delete删除，可以通过defineProperty重新定义）
    configurable: true,

    // 当获取值的时候执行
    get() {
      console.log('get: ', data.msg)
      return data.msg
    },
    // 当设置值的时候执行
    set(newValue) {
      console.log('set: ', newValue)
      if (newValue === data.msg) {
        return
      }
      data.msg = newValue
      // 数据更改，更新DOM的值
      document.querySelector('#app').textContent = data.msg
    }
  })

  // 测试
  vm.msg = 'Hello World'
  console.log(vm.msg)
</script>
```

2.defineProperty多个成员

```html
<div id="app">
    hello
</div>

<script>
    // 模拟 Vue 中的 data 选项
    let data = {
        msg: 'hello',
        count: 10
    }

    // 模拟 Vue 的实例
    let vm = {}

    proxyData(data)

    function proxyData(data) {
        // 遍历data对象的所有属性
        Object.keys(data).forEach(key => {
            // 把data中的属性，转换成vm的setter/getter
            Object.defineProperty(vm, key, {
                enumerable: true,
                configurable: true,
                get() {
                    console.log('get: ', key, data[key])
                    return
                },
                set(newValue) {
                    console.log('set: ', key, newValue)
                    if (newValue === data[key]) {
                        return
                    }
                    data[key] = newValue
                    // 数据改变，更新DOM的值
                    document.querySelector('#app').textContent = data[key]
                }

            })
        })
    }

    // 测试
    vm.msg = 'Hello World'
    console.log(vm.msg)
</script>
```

**Vue2.x中响应式的核心原理是基于defineProperty实现的**

#### 数据响应式核心原理-Vue3

- [MDN - Proxy](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy)
- [MDN-Proxy-get](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy/Proxy/get)
- [MDN-Proxy-set](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy/Proxy/set)
- 直接监听对象，而非属性
- ES 6中新增，IE 不支持，性能由浏览器优化

```html
<div id="app">
    hello
</div>
<script>
    // 模拟Vue中的data选项
    let data = {
        msg: 'hello',
        count: 0
    }

    // 模拟 Vue 实例
    let vm = new Proxy(data, {
        // 执行代理行为的函数
        // 当访问 vm 的成员会执行。target参数：目标对象；key参数：被获取的属性名
        get(target, key) {
            console.log('get, key: ', key, target[key])
            return target[key]
        },
        // 当设置 vm 的成员会执行
        set(target, key, newValue) {
            console.log('set, key: ', key, newValue)
            if (target[key] === newValue) {
                return
            }
            target[key] = newValue
            document.querySelector('#app').textContent = target[key]
        }
    })
    // 测试
    vm.msg = 'Hello World'
    console.log(vm.msg)
</script>
```

**Vue3.0的响应式核心原理是基于Proxy实现的。**

### 1.3发布订阅模式和观察者模式

#### 发布订阅模式

> 案例：
>
> 场景：小学三年级二班
>
> 人物：班主任、学生家长
>
> 每次考试后，学生家长订阅学生开始成绩，班主任发布成绩，班级作为数据中心。这时候，家长为订阅者，班主任为发布者。
>
> 我们假定，存在一个"信号中心"，某个任务执行完成，就向信号中心"发布"（publish）一个信号，其他任务可以向信号中心"订阅"（subscribe）这个信号，从而知道什么时候自己可以开始执行。这就叫做**"发布/订阅模式"（publish-subscribe pattern）**

[Vue中的自定义事件](https://cn.vuejs.org/v2/guide/migration.html#dispatch-%E5%92%8C-broadcast-%E6%9B%BF%E6%8D%A2)

```js
// Vue 自定义事件
let vm = new Vue()
// vm内部存在一个属性，该属性记录每次注册事件的数据，键为时间类型，值为每个时间类型记录的处理函数，多个处理函数为Array形式，
// { 'click': [fn1, fn2], 'change': [fn] }

// 注册事件(订阅消息)
vm.$on('dataChange', () => {
  console.log('dataChange')
})

vm.$on('dataChange', () => {
  console.log('dataChange1')
})
// 触发事件(发布消息)
vm.$emit('dataChange')
```

Vue兄弟组件通信过程

```js
// eventBus.js
// 事件中心
let eventHub = new Vue()

// ComponentA.vue
// 发布者
addTodo: function () {
    // 发布消息(事件)
    eventHub.$emit('add-todo', {text: this.newTodoText})
    this.newTodoText = ''
}

// ComponentB.vue
created: function () {
    // 订阅消息(事件)
    eventHub.$on('add-todo', this.addTodo)
}
```

模拟Vue自定义事件的实现

```js
// 事件触发器
class EventEmitter {
  constructor () {
    // { 'click': [fn1, fn2], 'change': [fn] }
    // 用来存储发布事件的数据，数据类型如上所示
    this.subs = Object.create(null)
  }

  // 注册事件
  $on (eventType, handler) {
    this.subs[eventType] = this.subs[eventType] || []  // 判断当前的事件类型中是否存在事件对应的处理函数Array
    this.subs[eventType].push(handler)
  }

  // 触发事件
  $emit (eventType) {
    if (this.subs[eventType]) {  // 判断事件类型中是否存在事件对应的处理函数Array
      this.subs[eventType].forEach(handler => {
        handler()
      })
    }
  }
}

// 测试
let em = new EventEmitter()
em.$on('click', () => {
  console.log('click1')
})
em.$on('click', () => {
  console.log('click2')
})

em.$emit('click')
```

![](http://5coder.cn/img/Hv9K5PRl6NQO2mI.png)

#### 观察者模式

- 观察者(订阅者)--Watcher
  - update()：当事件发生时，具体要做的事情
- 目标(发布者)--Dep
  - subs数组：存储所有的观察者
  - addSubs()：添加观察者
  - notify()：当事件发生，调用所有观察者的update()方法
- 没有事件中心

代码实现：

```js
// 发布者
class Dep {
  // 存储所有观察者
  constructor() {
    this.subs = []
  }
  // 添加所有的观察者
  addSub(sub) {
    if (sub && sub.update) {
      this.subs.push(sub)
    }
  }
  // 通知所有观察者
  notify() {
    this.subs.forEach(sub => {
      sub.update()
    })
  }
}
// 观察者(订阅者)
class Watcher{
  update() {
    console.log('观察者update被调用');
  }
}

// 测试
let dep = new Dep()
let watcher = new Watcher()

dep.addSub(watcher)
dep.notify()
```

![](http://5coder.cn/img/3hWS41TbeR6Oz5x.png)

#### 总结

- 观察者模式是由具体目标调度，比如当事件触发，Dep就会调用观察者的方法，所以观察者模式的订阅者与发布者之前是存在依赖的。例如Vue中的生命周期函数update方法。
- 发布/订阅模式由统一调度中心调用，因此发布者和订阅者不需要知道对方的存在。例如Vue中的兄弟组件通信。

> 现实案例：
>
> 观察者模式：发布者-老师，观察者-家长，事件-学生成绩不合格。老师技能是每当某个学生成绩不合格，老师会通知家长，家长执行update方法（打孩子，家长必须存在一个update方法），前提是家长需要和老师提前沟通，老师将需要的家长添加到通知列表。
>
> 发布/订阅模式：发布者-老师，订阅者-家长，事件中心-班级。每当考试完毕，老师会推送每个学生成绩至对应家长，有兴趣的家长自己调用老师的发布技能，获取学生成绩。

![](http://5coder.cn/img/UqTQB6cAK2GC3Ro.png)

## 2.响应式原理模拟

### 2.1.整体分析

Vue基本结构

![](http://5coder.cn/img/WEDe4Jft6cV89zZ.png)

打开浏览器，打印Vue实例vm。

![](http://5coder.cn/img/SwtJ2sjnTY3dNz4.png)

最小版本的Vue中要模拟vm中的$data、$el、$options，还要把data中的成员注入到Vue实例中。

最小版本Vue由下面的类型组成。

![](http://5coder.cn/img/3KCXRfpqz7H1OTv.png)

- Vue
  - 把data中的成员注入到Vue实例，并且把data中的成员转成getter/setter，Vue内部会调用Observer和Compiler
- Observer
  - 能够对数据对象的所有属性进行监听，如有变动可拿到最新值并通知Dep(发布者)
- Compiler
  - 解析每个元素中的指令/插值表达式，并替换成相应的数据
- Dep
  - 添加观察者(watcher)，当数据变化通知所有观察者
- Watcher
  - 数据变化更新视图

### 2.2.Vue

首先实现第一个部分-Vue。

- 功能

  - 负责接收初始化的参数(选项)
  - 负责把data中的属性注入到Vue实例，转换成getter/setter
  - 负责调用observer监听data中所有属性的变化
  - 负责调用compiler解析指令/插值表达式

- 结构

  ![](http://5coder.cn/img/NYb5DAh92ZdHQWq.png)

- 实现代码

  miniVue结构

  ![](http://5coder.cn/img/hjcJ1WilUo5Ran6.png)

  `index.html`

  ```html
  <!DOCTYPE html>
  <html lang="cn">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta http-equiv="X-UA-Compatible" content="ie=edge">
      <title>Mini Vue</title>
  </head>
  <body>
  <div id="app">
      <h1>差值表达式</h1>
      <h3>{{ msg }}</h3>
      <h3>{{ count }}</h3>
      <h1>v-text</h1>
      <div v-text="msg"></div>
      <h1>v-model</h1>
      <input type="text" v-model="msg">
      <input type="text" v-model="count">
  </div>
  <script src="./js/dep.js"></script>
  <script src="./js/watcher.js"></script>
  <script src="./js/compiler.js"></script>
  <script src="./js/observer.js"></script>
  <script src="./js/vue.js"></script>
  <script>
      let vm = new Vue({
          el: '#app',
          data: {
              msg: 'Hello Vue',
              count: 100,
              person: {name: 'zs'}
          }
      })
  </script>
  </body>
  </html>
  ```
  
  `vue.js`
  
  ```js
  class Vue {
    constructor(options) {
      // 1.通过属性保存选项
      this.$options = options || {}
      this.$data = options.data || {}
      this.$el = typeof options.el === 'string' ? document.querySelector(options.el) : options.el
      // 2.把data中的成员转换成setter和getter,注入到vue实例中
      this._proxyData(this.$data)
      // 下面两件事需要依赖observer和compiler，后面再实现
      // 3.调用observer对象，监听数据的变化
      // 4.调用compiler对象，解析指令和插值表达式
    }
  
    _proxyData(data) {    // 让vue代理data中的属性
      // 遍历data中的所有属性
      Object.keys(data).forEach(key => {
        // 把data的属性注入到vue实例中
        Object.defineProperty(this, key, {
          enumerable: true,
          configurable: true,
          get() {
            return data[key]
          },
          set(newValue) {
            if (newValue === data[key]) {
              return
            }
            data[key] = newValue
          }
        })
      })
    }
  }
  ```
  
  测试，打开index.html，打开控制台，打印vm实例，如下图，预期的$el、$data、$options都已经注入到vue实例中了。
  
  ![](http://5coder.cn/img/wdUEylYAkFm4jiD.png)
  
  

### 2.3.Observer

接下来实现第二部分，Observer

功能：

- 负责把data选项中的属性转换成响应式数据
- data中的某个属性也是对象，把该属性转换成响应式数据
- 数据变化发送通知

结构

![](http://5coder.cn/img/7yM3LboGNw9SnWp.png)

`walk`方法的作用是遍历`data`中的所有属性，所以它的参数是data对象。defineReactive（定义响应式数据），通过调用`Object.definePropoty()`把属性转换成getter和setter，`walk`方法在循环过程会调用`defineReactive()`方法。

代码实现：

Observer.js

```js
class Observer {
  constructor(data) {
    this.walk(data)
  }

  walk(data) {
    // 核心作用是遍历data对象中的所有属性
    // 1.判断data是否是对象
    if (!data || typeof data !== 'object') {
      return
    }
    // 2.遍历data对象所有属性
    Object.keys(data).forEach(key => {
      // 此处使用箭头函数，箭头函数不会改变this的执行，所以此处this依然指的是Observer对象
      this.defineReactive(data, key, data[key])
    })
  }

  defineReactive(obj, key, val) {
    // 参数obj对象,其实就是data对象；key是obj的属性；val是obj对象对应key的值
    Object.defineProperty(obj, key, {
      enumerable: true,
      configurable: true,
      get() {
        return val
      },
      set(newValue) {
        if (newValue === val) {
          return
        }
        val = newValue
        // TODO 最后实现，发送通知
      }
    })
  }
}
```

测试：

因为在Vue.js中第三步中需要创建Observer对象，所以添加以下代码：

![](http://5coder.cn/img/MUfGaRr5QluWYnC.png)

因为在index.html中引入的vue.js需要依赖observer.js，所以先引入observer.js，打开浏览器，打开控制台，打印vm对象。Observer对象核心的功能是把data中的属性转换成getter和setter，如下图实现：

```html
<script src="./js/observer.js"></script>
<script src="./js/vue.js"></script>
```

![](http://5coder.cn/img/EBcl4FXakydrMue.png)

#### Observer-defineReactive 1

接下来解释一下为什么defineReactive需要传递第三个参数val，为了演示问题，需要触发get方法。所以在index.html中访问msg属性，`console.log(vm.msg)`，当访问`vm.msg`时，首先会触发vue.js中的_proxyData中get方法，而vue.js中的get方法又调用了`data[key]`，当访问`data[key]`时，又会触发observer.js中`defineReactive`中的get方法。

![](http://5coder.cn/img/PgsKkopbcXZBNm6.png)

> 上图中的vue.js第29行键入错误，改为`data[key] = newValue`。

打开浏览器，控制台正常打印出来了`'Hello Vue'`。当将observer中的get方法中返回的`val`改变为`obj[key]`。时，查看浏览器控制台出现报错——**堆栈溢出**。

![](http://5coder.cn/img/VSnf2aMutcoQlh3.png)

此时在observer.js中的19行出现错误，内容是`return obj[key]`，此处的obj就是data对象，当访问data[key]时就会触发此处的get方法。这就形成**死递归**，这就是传递`val`参数而不是直接使用`obj[key]`的原因。

此处还有一个细节，当`defineReactive`方法调用完成之后，val参数是一个局部变量，所以他的值应该被释放掉，但是在index.html中依然可以打印出来，原因就此处形成了闭包，提升了`val`的作用域。defineReactive第一个参数obj其实就是$data对象，$data中引用了get方法，而get方法又对val有引用，也就是外部对get方法有引用，而get方法又用到了val，所以此处发生了闭包，所以val的值并没有被释放掉。

![](http://5coder.cn/img/G591WQvneaxoZyI.png)

#### Observer-defineReactive 2

defineReactive中的两个问题，

1. **如果data中的某个属性是对象，需要把对象内部的属性转换成响应式数据**

   - 处理前

     ![](http://5coder.cn/img/U2oFrSq8wCsH1lO.png)

     在浏览器控制台打印vm实例，发现person对象的name属性并没有getter和setter方法，也就是并未被转换成响应式，只对**person对象**进行响应式处理，并未对**person内部属性**做任何处理。

   - 处理后

     ![](http://5coder.cn/img/G7NRC4B3ngskWZ5.png)

     浏览器测试，发现person对象的name属性也具有getter和setter，第一个问题解决。

     ![](http://5coder.cn/img/wlLZJDkihvgH3te.png)

2. **当data的当前属性重新赋值成一个新对象的时候，该对象的内部属性需要转换成响应式数据**

   - 处理前

     将data中的msg属性的值由字符串改为对象`vm.msg = { test: 'Hello' }`，观察更改后的对象的属性test属性并没有getter和setter方法，同样$data中的msg对象的属性test也没有getter和setter。

     ![](http://5coder.cn/img/pcgEkSm7WLQNOwJ.png)

   - 处理后

     ![](http://5coder.cn/img/qbjvRndk9asSt4Y.png)

     浏览器测试，发现新修改的msg的值中的test属性也具有getter和setter，为响应式的。

     ![](http://5coder.cn/img/YtFyesvKrgHLGPA.png)

### 2.4.Compiler

功能

> 与Vue内部不同，做了简化，并没有使用虚拟DOM，只是做了DOM操作。

- 负责编译模板，解析指令/插值表达式
- 负责页面的首次渲染
- 当数据变化后重新渲染视图

结构

![](http://5coder.cn/img/S6dLN3w7rbEehjc.png)

基本结构实现：

```js
class Compiler {
  constructor(vm) {
    this.el = vm.$el
    this.vm = vm
  }

  // 编译模板，处理文本节点和元素节点
  compile(el) {
  }

  // 编译元素节点，处理指令
  compileElement(node) {

  }

  // 编译文本节点，处理插值表达式
  compileText(node) {

  }

  // 判断元素属性的名字是否为指令
  isDirective(attrName) {
    return attrName.startsWith('v-')
  }

  // 判断传入的节点是否为文本节点
  isTextNode(node) {
    return node.nodeType === 3
  }

  // 判断传入的节点是否为元素节点
  isElementNode(node) {
    return node.nodeType === 1
  }
}
```

> node.nodeType用法，请参考[MDN（Node.nodeType）](https://developer.mozilla.org/zh-CN/docs/Web/API/Node/nodeType)

#### Compiler-compile

接下来实现compile方法

```js
// 编译模板，处理文本节点和元素节点
compile(el) {
  let childNodes = el.childNodes
  Array.from(childNodes).forEach(node => {
    if (this.isTextNode(node)) {
      // 处理文本节点
      this.compileText(node)
    } else if (this.isElementNode(node)) {
      // 处理元素节点
      this.compileElement(node)
    }

    // 以上处理只是el中的第一层子节点，当node节点中还有其他节点时,
    // 判断node节点，是否有子节点，如果有子节点，要递归调用compile
    if (node.childNodes && node.childNodes.length !== 0) {
      this.compile(node)
    }
  })
}
```

#### Compiler-compileText

首先在compileText中打印出node节点的内容

![](http://5coder.cn/img/1DkHvEN4wjUtByc.png)

打开浏览器，打印结果如下图：

![](http://5coder.cn/img/KQyOBhqp14eArdk.png)

接下来开始写compileText的内容。

```js
// 编译文本节点，处理插值表达式
compileText(node) {
  // console.dir(node)
  // 使用正则表达式匹配花括号中的内容
  let reg = /\{\{(.+?)\}\}/
  // 获取文本节点的内容
  let value = node.textContent
  if (reg.test(value)) {
    // 获取正则表达式匹配的第一个分组内容(.+?)，即花括号中的内容并去除左右空格
    let key = RegExp.$1.trim()
    // 将正则表达式中匹配到的插值表达式替换成该属性对应的值,重新赋值给文本节点
    node.textContent = value.replace(reg, this.vm[key])
  }
}
```

打开浏览器测试，发现index.html中的插值表达式已经被替换成正确的值了

![](http://5coder.cn/img/JQ9g4wIbsvy6NGC.png)

#### Compiler-compileElement

最后实现compileElement，他的作用是编译元素节点，处理指令，此处只模拟`v-text`与`v-model`。

首先遍历dom元素所有属性，找到v-开头的属性名，也就是指令，以及v-开头的属性名对应的值，也就是指令关联的数据，最终需要把这个指令对应的数据展示到指令指定的位置。

观察属性节点，name为指令名称，value为指令的值，也就是对应的vm实例中的属性名。

![](http://5coder.cn/img/gKnAQBHwrRoELZD.png)

代码实现

```js
// 编译元素节点，处理指令
compileElement(node) {
  // console.log(node.attributes)
  // 遍历所有的属性节点
  Array.from(node.attributes).forEach(attr => {
    let attrName = attr.name  // v-text或v-model
    if (this.isDirective(attrName)) {
      // v-text去除v-
      attrName = attrName.substr(2)
      let key = attr.value  // 对应的msg或count
      this.update(node, key, attrName)
    }
  })
  // 判断是否是指令
}

update(node, key, attrName) {
  let updateFn = this[attrName + 'Updater']
  updateFn && updateFn(node, this.vm[key])
}

// 处理v-text指令
textUpdater(node, value) {
  // 替换元素的显示内容
  node.textContent = value
}

// 处理v-model指令
modelUpdater(node, value) {
  // 替换表单元素的值
  node.value = value
}
```

![](http://5coder.cn/img/LkSXbnzEtPy3cvT.png)

打开浏览器测试，发现v-指令中的内容全部被替换成为真实的值。

![](http://5coder.cn/img/rypSQYKwDICv7BH.png)

#### Compiler复习

完整代码

```js
class Compiler {
  constructor(vm) {
    this.el = vm.$el
    this.vm = vm
    this.compile(this.el)  // 调用new Compiler()创建对象时，可以立即编译模板
  }

  // 编译模板，处理文本节点和元素节点
  compile(el) {
    let childNodes = el.childNodes
    Array.from(childNodes).forEach(node => {
      if (this.isTextNode(node)) {
        // 处理文本节点
        this.compileText(node)
      } else if (this.isElementNode(node)) {
        // 处理元素节点
        this.compileElement(node)
      }

      // 以上处理只是el中的第一层子节点，当node节点中还有其他节点时,
      // 判断node节点，是否有子节点，如果有子节点，要递归调用compile
      if (node.childNodes && node.childNodes.length !== 0) {
        this.compile(node)
      }
    })
  }

  // 编译元素节点，处理指令
  compileElement(node) {
    // console.log(node.attributes)
    // 遍历所有的属性节点
    Array.from(node.attributes).forEach(attr => {
      let attrName = attr.name  // v-text或v-model
      if (this.isDirective(attrName)) {
        // v-text去除v-,只保留后面的值
        attrName = attrName.substr(2)
        let key = attr.value  // 对应的msg或count
        this.update(node, key, attrName)
      }
    })
    // 判断是否是指令
  }

  update(node, key, attrName) {
    // 参数node：dom元素；key：data中的属性名；attrName：指令去掉v-后面的内容
    let updateFn = this[attrName + 'Updater']  // 获取指令对应的方法
    updateFn && updateFn(node, this.vm[key])
  }

// 处理v-text指令
  textUpdater(node, value) {
    // 替换元素的显示内容
    node.textContent = value
  }

// 处理v-model指令
  modelUpdater(node, value) {
    // 替换表单元素的值
    node.value = value
  }


  // 编译文本节点，处理插值表达式
  compileText(node) {
    // console.dir(node)
    // 使用正则表达式匹配花括号中的内容{{ msg }}
    let reg = /\{\{(.+?)\}\}/
    // 获取文本节点的内容
    let value = node.textContent
    if (reg.test(value)) {
      // 获取正则表达式匹配的第一个分组内容(.+?)，即花括号中的内容并去除左右空格
      let key = RegExp.$1.trim()
      // 将正则表达式中匹配到的插值表达式替换成该属性对应的值,重新赋值给文本节点
      node.textContent = value.replace(reg, this.vm[key])
    }
  }

  // 判断元素属性的名字是否为指令
  isDirective(attrName) {
    return attrName.startsWith('v-')
  }

  // 判断传入的节点是否为文本节点
  isTextNode(node) {
    return node.nodeType === 3
  }

  // 判断传入的节点是否为元素节点
  isElementNode(node) {
    return node.nodeType === 1
  }
}
```

### 2.5.Dep

![](http://5coder.cn/img/WAQm6v9sdrKCn3l.png)

功能：

- 收集依赖，添加观察者（watcher）
- 通知所有观察者

结构：

![](http://5coder.cn/img/qiOb7STVP9EzapF.png)

代码实现：

dep.js

```js
class Dep {
  constructor() {
    // 存储所有的观察者watcher
    // Stores all observers
    this.subs = []
  }

  // 添加观察者
  // Add observer
  addSubs(sub) {
    // 判断是否为空以及是否是观察者（观察者拥有update方法）
    // Determine if the sub is empty and if it's an observer(the observer has the update method)
    if (sub && sub.update) {
      this.subs.push(sub)
    }
  }

  // 发送通知,遍历subs数组中的所有观察者，调用每个观察者的update方法去更新视图
  // Send notification，Iterate through all the observers in the subs array and call the update method on each
  // observer to update the view
  notify() {
    this.subs.forEach(sub => {
      sub.update()
    })
  }
}
```

Dep类的作用是收集依赖和发送通知，需要为每一个响应式数据创建一个Dep对象，在使用响应式数据的时收集依赖，也就是创建观察者对象，当数据变化的时候，通知所有观察者，调用观察者的`update`的方法更新视图，所以需要在observer中来创建Dep对象。

![](http://5coder.cn/img/8qLOb1R9GohAIvg.png)

`observer`类中的`get`方法中，当访问属性的值的时去收集依赖，在收集依赖的时候首先要判断`Dep`这个类有没有设置静态属性`target`，也就是观察者对象，但是在定义`Dep`这个类的时候并没有给这个类设置它的属性，它的这个属性是在`watcher`对象中来添加的，在写`watcher`的时候再回过来看。首先判断`Dep`这个类有没有`target`这个静态属性，如果有的话再进入`Dep`对象的`addSub()`方法去添加观察者。

### 2.6.Watcher

watcher

![](http://5coder.cn/img/eQP8Acin3tmpr5D.png)

在`data`中的属性的`getter`方法中，通过`Dep`对象收集依赖，在`data`属性的`setter`方法中，通过`Dep`对象触发依赖。所以`data`中的每一个属性都需要创建一个`Dep`对象，在收集依赖时，把依赖该数据的所有`watcher`(观察者对象)添加到`Dep`对象中的`subs`数组中。在`setter`方法中去触发依赖，也就是发送通知，调用`Dep`对象的`notify`方法去通知所有关联的`watcher`对象，watcher对象负责更新对应的视图。

总结`watcher`对象的功能：

- 当数据变化触发依赖，dep通知所有的Watcher实例更新视图
- 自身实例化的时候往dep对象中添加自己

结构

![](http://5coder.cn/img/ZmEdC5uB14vhyig.png)

```js
class Watcher {
  constructor(vm, key, cb) {
    // vue实例
    this.vm = vm
    // data中的属性名称
    this.key = key
    // 回调函数，负责更新视图
    this.cb = cb

    // 把当前的watcher对象记录到Dep类的静态属性target中
    Dep.target = this
    // 在访问vm[key]时触发了get方法，在get方法中调用addSub()方法
    // 在observer中的get方法中以及调用了addSub方法：Dep.target && dep.addSub(Dep.target)
    this.oldValue = vm[key]
    // 置空，防止重复添加
    Dep.target = null
  }

  // 当数据发生变化时更新视图
  update() {
    let newValue = this.vm[this.key]
    if (this.oldValue === newValue) {
      return
    }
    this.cb(newValue)
  }
}
```

#### 创建watcher对象 1

compiler.js中的compileText方法，在处理插值表达式时创建watcher对象

![](http://5coder.cn/img/txg8LHGMnqXJZaA.png)

index.html中引入

![](http://5coder.cn/img/JnZrkD3VUTNA8y2.png)

打开浏览器控制台，改变插值表达式绑定的值msg

```shell
vm.msg = 'xxx'
```

![](http://5coder.cn/img/rXgSAIemNzB53Ed.png)

#### 创建watcher对象2

这里处理textUpdater——v-text指令和modelUpdater——v-model指令，在指令中新增如下代码：

```js
// 处理v-text指令
textUpdater(node, value) {
  // 替换元素的显示内容
  node.textContent = value
  new Watcher(this.vm, key, (newValue) => {
    node.textContent = newValue
  })
}

// 处理v-model指令
modelUpdater(node, value) {
  // 替换表单元素的值
  node.value = value
  new Watcher(this.vm, key, (newValue) => {
    node.value = newValue
  })
}
```

其中，`new Watcher()`中的第一个参数：`this.vm`，在调用`textUpdater()`和`modelUpdater()`方法时是直接通过`updateFn()`进行调用的，因此此处的`this`指向的是有问题的，并不是期望的`Compiler`对象(`this`的指向是由谁调用来决定的，如果调用`updateFn`时是使用`this.updateFn()`调用，则this指向`Compiler`对象)。所以在调用updateFn方法时，使用call方法改变this的指向：`updateFn && updateFn.call(this, node, this.vm[key])`，其中的第一个参数代表`update`方法指向的this`，`而`update`方法的调用是通过this.update()调用的，因此此处this指向Compiler对象。

第二个参数：key，由于在textUpdater和modelUpdater中并没有传递key值，所以需要在调用updateFn时将key传递下去，因此为`updateFn && updateFn.call(this, node, this.vm[key], key)`

所以修改后的完整代码是compiler.js：

```js
class Compiler {
  constructor(vm) {
    this.el = vm.$el
    this.vm = vm
    this.compile(this.el)
  }

  // 编译模板，处理文本节点和元素节点
  compile(el) {
    let childNodes = el.childNodes
    Array.from(childNodes).forEach(node => {
      if (this.isTextNode(node)) {
        // 处理文本节点
        this.compileText(node)
      } else if (this.isElementNode(node)) {
        // 处理元素节点
        this.compileElement(node)
      }

      // 以上处理只是el中的第一层子节点，当node节点中还有其他节点时,
      // 判断node节点，是否有子节点，如果有子节点，要递归调用compile
      if (node.childNodes && node.childNodes.length !== 0) {
        this.compile(node)
      }
    })
  }

  // 编译元素节点，处理指令
  compileElement(node) {
    // console.log(node.attributes)
    // 遍历所有的属性节点
    Array.from(node.attributes).forEach(attr => {
      let attrName = attr.name  // v-text或v-model
      if (this.isDirective(attrName)) {
        // v-text去除v-
        attrName = attrName.substr(2)
        let key = attr.value  // 对应的msg或count
        this.update(node, key, attrName)
      }
    })
    // 判断是否是指令
  }

  update(node, key, attrName) {
    let updateFn = this[attrName + 'Updater']
    // 使用call方法改变this的指向，进而在textUpdater和modelUpdater中可以通过this.vm获取到vue实例
    updateFn && updateFn.call(this, node, this.vm[key], key)
  }

  // 处理v-text指令
  textUpdater(node, value, key) {
    // 替换元素的显示内容
    node.textContent = value
    // 为每一个指令/插值表达式创建 watcher 对象，监视数据的变化
    new Watcher(this.vm, key, (newValue) => {
      node.textContent = newValue
    })
  }

  // 处理v-model指令
  modelUpdater(node, value, key) {
    // 替换表单元素的值
    node.value = value
    // 为每一个指令/插值表达式创建 watcher 对象，监视数据的变化
    new Watcher(this.vm, key, (newValue) => {
      node.value = newValue
    })
  }


  // 编译文本节点，处理插值表达式
  compileText(node) {
    // console.dir(node)
    // 使用正则表达式匹配花括号中的内容
    let reg = /\{\{(.+?)\}\}/
    // 获取文本节点的内容
    let value = node.textContent
    if (reg.test(value)) {
      // 获取正则表达式匹配的第一个分组内容(.+?)，即花括号中的内容并去除左右空格
      let key = RegExp.$1.trim()
      // 将正则表达式中匹配到的插值表达式替换成该属性对应的值,重新赋值给文本节点
      node.textContent = value.replace(reg, this.vm[key])

      // 创建watcher对象，当数据改变更新视图
      new Watcher(this.vm, key, (newValue) => {
        node.textContent = newValue
      })
    }
  }

  // 判断元素属性的名字是否为指令
  isDirective(attrName) {
    return attrName.startsWith('v-')
  }

  // 判断传入的节点是否为文本节点
  isTextNode(node) {
    return node.nodeType === 3
  }

  // 判断传入的节点是否为元素节点
  isElementNode(node) {
    return node.nodeType === 1
  }
}
```

### 2.7.视图变化更新数据

上述步骤实现了数据变化更新视图，但是并没有完成双向绑定，即v-model中的input改变后，视图并没有更新，代码实现如下compiler.js：

```js
// 处理v-model指令
modelUpdater(node, value, key) {
  // 替换表单元素的值
  node.value = value
  new Watcher(this.vm, key, (newValue) => {
    node.value = newValue
  })
  // 双向绑定
  node.addEventListener('input', () => {
    this.vm[key] = node.value
  })
}
```

测试，当输入框的值改变时，插值表达式和v-text对应的视图也会发生变化。

![](http://5coder.cn/img/doKJPLU1G7HqtXe.png)

### 2.8.调试

> 视频是录制拉勾教育-大前端高薪训练营Part3，如有侵权，请联系删除。此处放置视频，是因为DEBUG过程用文字不好描述，视频更加清晰明了。

- 调试页面首次渲染的过程

  <iframe src="http://5coder.cn/static/video/22.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height=500 width=700 autoplay="false"> </iframe>

- 调试数据改变更新视图的过程

  <iframe src="http://5coder.cn/static/video/23.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height=500 width=700  autoplay="false"> </iframe>

### 2.9.总结

问题

- 给属性重新赋值成对象，是否是响应式的？

  重新给属性赋值成对象，该属性依然是响应式的。在observer.js中，当重新赋值时，触发defineReactive方法中的set方法，首先记录newValue也就是新对象的值，然后调用that.walk方法，重新遍历newValue的所有属性，并重新调用defineReactive方法。

  ![](http://5coder.cn/img/bRYNsQcxuE6XA8M.png)

- 给Vue实例新增一个成员是否是响应式的？（[官方文档](https://cn.vuejs.org/v2/guide/reactivity.html#%E6%A3%80%E6%B5%8B%E5%8F%98%E5%8C%96%E7%9A%84%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9)）

  ![](http://5coder.cn/img/HyEFBuSLljkAsIM.png)

  data中的属性是在new Vue中，通过new Observer()转换成响应式数据，而手动给vm添加一个test属性，并没有经过observer处理，仅仅是在vm上添加了一个普通的js属性，所以不是响应式的。

  ![](http://5coder.cn/img/2naKVrAsozIleDJ.png)





整体流程

![](http://5coder.cn/img/C1BAcQ4KMIHDRTw.png)

- Vue
  - 记录传入的选项，设置`$data/$el`
  - 把`data`的成员注入到Vue实例
  - 负责调用`Observer`实现数据响应式处理（数据劫持），内部有get和set方法
  - 负责调用`Compiler`编译指令和插值表达式
- Observer
  - 数据劫持
    - 负责把data中的成员转换成`getter/setter`
    - 负责把多层属性转换成`getter/setter`
    - 如果给属性赋值为新对象，把新对象的成员设置为`getter/setter`
  - 添加`Dep`和`Watcher`的依赖关系
  - 数据变化发送通知
- Compiler
  - 负责编译模板，解析指令/插值表达式
  - 负责页面的首次渲染过程
  - 当数据变化后重新渲染
- Dep
  - 收集依赖，添加订阅者（`watcher`）
  - 通知所有订阅者
- Watcher
  - 自身实例化的时候往`dep`对象中添加自己
  - 当数据变化`dep`通知所有的`Watcher`实例更新视图

## TODO：有空的时候会将所有文件做一张脑图，用来复习！