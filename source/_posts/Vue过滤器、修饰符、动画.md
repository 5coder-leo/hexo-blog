---
title: Vue过滤器、修饰符、动画
author: 5coder
abbrlink: 1929
date: 2021-05-20 06:27:43
summary:
tags: Vue
category: 大前端(杂识)
---

# Vue——过滤器、键盘修饰符、动画等

## 1.过滤器

> Vue.js 允许你自定义过滤器，可被用于一些常见的文本格式化。过滤器可以用在两个地方：**双花括号插值（Mustache）和 `v-bind` 表达式** (后者从 2.1.0+ 开始支持)。过滤器应该被添加在 JavaScript 表达式的尾部，由“管道”符号指示

```html
<!--在Mustache中使用过滤器-->
{{message | capitalize}}

<!--在v-bind中使用过滤器-->
<div v-bind:id="rawId | formatId"></div>
```

### 1.1私有过滤器

在组件的选项中定义本地的过滤器，使用filters

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  <p>{{msg | capitalize}}</p>
</div>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      msg: 'hello world'
    },
    methods: {},
    filters: {
      capitalize: function (value) {
        if (!value) return ''
        value = value.toString()
        return value.charAt(0).toUpperCase() + value.slice(1)
      }
    }
  })
</script>
</body>
</html>
```

### 1.2全局过滤器

在创建Vue实例之前定义全局过滤器

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  <p>{{msg | capitalize2}}</p>
</div>
<script src="../vue.js"></script>
<script>
  Vue.filter('capitalize2', function (value) {
    if (!value) return ''
    return value.toUpperCase()
  })
  let vm = new Vue({
    el: '#app',
    data: {
      msg: 'hello world'
    },
    methods: {},
  })
</script>
</body>
</html>
```

> **注意：当局部和全局有两个同名过滤器时，被控制实例优先使用私有过滤器，即局部过滤器优先于全局过滤器被调用！**

## 2.键盘修饰符及

> 在监听键盘事件时，我们经常需要检查详细的按键。Vue 允许为 `v-on` 在监听键盘事件时添加按键修饰符

```html
<!-- 只有在 `key` 是 `Enter` 时调用 `vm.submit()` -->
<input v-on:keyup.enter="submit">

<!--使用 keyCode attribute 也是允许的-->
<input v-on:keyup.13="submit">
```

为在必要的情况下支持旧浏览器，Vue提供了绝大多数常用的按键码的别名：

- .enter
- .tab
- .delete(捕获删除和退格键)
- .esc
- .space
- .up
- .down
- .left
- .right

> 通过config.ketCodes对象自定义按键修饰符别名

```html
Vue.config.keyCodes.f1 = 112
```

## 3.系统修饰键

可以通过一下修饰符来实现**<u>仅在按下相应按键时才出发鼠标或键盘事件的监听器</u>**

- .ctrl
- .alt
- .shift
- .meta

> **注意：在 Mac 系统键盘上，meta 对应 command 键 (⌘)。在 Windows 系统键盘 meta 对应 Windows 徽标键 (⊞)。在 Sun 操作系统键盘上，meta 对应实心宝石键 (◆)。在其他特定键盘上，尤其在 MIT 和 Lisp 机器的键盘、以及其后继产品，比如 Knight 键盘、space-cadet 键盘，meta 被标记为“META”。在 Symbolics 键盘上，meta 被标记为“META”或者“Meta”。**

```html
<!-- Alt + C -->
<input v-on:keyup.alt.67="clear">

<!-- Ctrl + Click -->
<div @click.ctrl="doSomething">Do Something</div>
```

> **注意：修饰键与常规按键不同，在和 keyup 时间一起使用时，时间触发时修饰键必须处于按下状态。换句话说，只有在按住Ctrl的情况下释放其他按键，才能触发keyUp.ctrl。而单单释放ctrl也不会出发时间。如果想要这样的行为，请为Ctrl换用keyCode:keyup.17。**

### 3.1 .exact修饰符

.exact修饰符允许控制由精确的系统修饰符组合触发的事件。

```html
<div id="app">
<!-- 即使Alt或Shift被同时按下时也会触发 -->
  <button @click.ctrl="onClick">即使Alt或Shift被同时按下时也会触发</button>
<!--  有且只有Ctrl被按下的时候才会触发-->
  <button @click.ctrl.exact="onCtrlClick">有且只有Ctrl被按下的时候才会触发</button>
<!--  没有任何系统修饰符被按下的是否才触发-->
  <button @click.exact="onClickWithout">没有任何系统修饰符被按下的是否才触发</button>
</div>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {},
    methods: {
      onClick(){
        alert('即使Alt或Shift被同时按下时也会触发')
      },
      onCtrlClick(){
        alert('有且只有Ctrl被按下的时候才会触发')
      },
      onClickWithout(){
        alert('没有任何系统修饰符被按下的是否才触发')
      },
    }
  })
</script>
```

### 3.2鼠标按钮修饰符

- .left
- .right
- .middle

这些修饰符会限制处理函数仅响应特定的鼠标按钮。

## 4.vue-resource实现get/post/jsonp请求

### 4.1 JSONP

jsonp实现原理

> - 由于浏览器安全限制，不允许ajax访问协议不同、域名不同、端口号不同的数据接口，浏览器认为这种访问不安全
> - 可以通过动态创建script标签的形式，把script标签的src属性指向数据接口的地址，因为script标签不存在跨域限制，这种数据获取方式称作JSONP（注意：根据JSONP实现原理，了解到JSONP只能实现GET请求）



具体实现过程

- ```
  先在客户端定义一个回调方法，预定义对数据的操作
  再把这个回调方法的名称，通过URL传参的形式，提交到服务器的数据接口
  服务器数据接口组织好要发给客户端的数据，再拿着客户端传递过来的回调方法名称，拼接出一个调用这个方法的字符串，发送给客户端去解析执行
  客户端拿到服务器返回的字符串之后，当做script脚本去解析之星，这就拿到了JSONP的数据了
  ```

Node.js手动实现JSONP请求案例（服务器案例）

```js
const http = require('http')
// 导入解析URL地址的核心模块
const urlModule = require('url')

const server = http.createServer();

// 监听服务器request请求事件，处理每个请求
server.on('request', (req, res) => {
  const url = req.url
  
  // 解析客户端请求的URL地址
  let info = urlModule.parse(url, true)
  
  // 如果请求的URL地址是/getjsonp，则表示要获取JSONP类型的数据
  if (info.pathname === '/getjsonp') {
    // 获取客户端指定的回调函数的名称
    let cbName = info.query.callback
    console.log(info)
    
    // 手动拼接要返回给客户端的数据
    let data = {
      name: 'zhangsan',
      age: '12',
      gender: 'man',
      hobby: ['eating', 'sleeping', 'play doudou']
    }
    
    // 拼接出一个方法的调用，把要发送给客户端的数据，序列化为字符串，作为参数传递给这个调用的方法
    let result = `${cbName}(${JSON.stringify(data)})`
    // 将拼接好的方法的调用，返回给客户端去解析执行
    res.end(result)
  } else {
    res.end('404')
  }
})

server.listen(3000, () => {
  console.log('server running at 3000')
})
```

原生JavaScript实现jsonp案例

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>
<div id="app"></div>
<script>
  function myJSONP(URL, callback, cbName) {
    // 给系统定义一个全局按量callbackName, 指向callback
    window[cbName] = callback

    // 创建script节点
    let scriptObj = document.createElement('script')
    // 和image不同，script的src不会发送http请求
    scriptObj.src = URL
    scriptObj.type = 'text/javascript'
    // script标签的请求是在上树的时候发出，请求的是一个函数的执行语句
    document.head.appendChild(scriptObj)
    // 为了不污染页面，迅速把script拿掉
    document.head.removeChild(scriptObj)
  }
  // 使用
  myJSONP('http://127.0.0.1:3000/getjsonp?callback=cbName', function (data) {
    console.log(data)
  }, 'cbName')

  console.log(window['cbName'])
</script>
</body>
</html>
```

### 4.2 vue-resource基本使用

vue-resource配置步骤

- 直接通过script标签引入，先引入vue.js，再引入vue-resource.js

- 发送get请求：

  ```js
  // 在vue实例上的method中添加方法
  let vm = new Vue({
    el: '#app',
    data: {},
    methods: {
      getInfo() {
        this.$http.get('http://127.0.0.1:8899/api/getlunbo')
          .then(res => {
          console.log(res.body) // 数据在response响应对象中的body中  
        })
      }
    }
  })
  ```

- 发送post请求：

  ```js
  let vm = new Vue({
    el: '#app',
    data: {},
    methods: {
      postInfo() {
        let url = 'http://127.0.0.1:8899/api/post'
        // post方法接收三个参数
        // 1.要请求的URL地址；
        // 2.要发送的数据对象；
        // 3.指定post提交的编码类型为application/x-www-form-urlencode
        this.$http.post(url, {name: 'zhangsan'}, {emulateJSON: true})
          .then(response => {
            console.log(response.body)
          })
      }
    }
  })
  ```

- 发送JSONP请求

  ```js
    let vm = new Vue({
      el: '#app',
      data: {},
      methods: {
        jsonpInfo() {
          let url = 'http://127.0.0.1:8899/api/jsonp'
          this.$http.jsonp(url)
          .then(res=> {
            console.log(res.body)
          })
        }
      }
    })
  ```

## 5.Vue动画

> vue在插入、更新或者移除DOM时，提供了多种不同方式的应用过渡效果，包括以下工具：
>
> - 在CSS过度和动画中自动应用class
> - 配合第三方CSS动画库，如Animate.css
> - 在过渡钩子函数中使用JavaScript直接操作DOM（Vue不推荐直接操作DOM）
> - 配合第三方JavaScript动画库，如Velocity.js

### 5.1 单元素/组件过度

Vue提供了transition的封装组件，在下列情况下可以给任何元素和组件添加进入/离开过渡

- 条件渲染（v-if）
- 条件展示（v-show）
- 动态组件
- 组件根节点

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>

  <style>
      .fade-enter-active, .fade-leave-active {
        transition: opacity 0.5s;
      }

      .fade-enter, .fade-leave-to {  /* .fade-leave-active below version 2.1.8 */
          opacity: 0;
      }
  </style>

</head>
<body>

<div id="app">
  <button @click="show=!show">show</button>

  <transition name="fade">  <!--name属性定义动画-->
    <p v-if="show">这是需要动画效果的元素</p>
  </transition>

</div>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      show: true
    },
    methods: {}
  })
</script>
</body>
</html>
```

当插入或删除包含在<font color='red'> transition</font>组件中的元素时，Vue会做以下处理：

- 自动嗅探目标元素是否应用了CSS过度或动画，如果是，在恰当的时机添加/删除css类名
- 如果过度组件提供了<font color='lightgreen'>JavaScript钩子函数</font>,这些钩子函数将在恰当的时机被调用
- 如果没有找到JavaScript钩子函数并且也没有检测到css过渡/动画，DOM操作（插入或删除）在下一帧中立即执行（注意：此指浏览器逐帧动画机制，和Vue的<font color='red'>nextTick</font>）不同

### 5.3 使用过渡类名

在进入/离开的过渡中，会有6个class切换。

1. <font color='red'>v-enter</font>：定义进入过渡的开始状态。在元素被插入之前生效，在元素被插入之后的下一帧移除。
2. <font color='red'>v-enter-active：</font>定义进入过渡生效时的状态。在整个进入过渡的阶段中应用，在元素被插入之前生效，在过渡/动画完成之后移除。这个类可以被用来定义进入过渡的过程时间，延迟和曲线函数。
3. <font color='red'>v-enter-to：</font>**2.1.8版本以上**定义进入过渡的结束状态。在元素被插入之后下一帧生效（与此同时<font color='red'>v-enter</font>被移除），在过渡/动画完成之后移除。
4. <font color='red'>v-leave：</font>定义离开过渡的开始状态。在离开过渡被触发时立刻生效，下一帧被移除。
5. <font color='red'>v-leave-active：</font>定义过渡生效时的状态。在整个离开过渡的阶段中应用，在离开过渡被触发时立刻生效，在过渡/动画完成之后移除。这个类可以被用来定义离开过渡的过渡时间，延迟和曲线函数。
6. <font color='red'>v-leave-to：</font>**2.1.8版本以上**定义离开过渡的结束状态。在离开过渡被触发之后的下一帧生效（与此同时<font color='red'>v-leave</font>被删除），在过渡/动画完成之后移除。

对于这些在过渡中切换的类名来说，如果你使用一个没有名字的 `<transition>`，则 `v-` 是这些类名的默认前缀。如果你使用了 `<transition name="my-transition">`，那么 `v-enter` 会替换为 `my-transition-enter`。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
  <style>
      .fade-enter-active,
      .fade-leave-active {
          transition: all 2s ease;
          position: absolute;
      }

      .fade-enter,
      .fade-leave-to {
          opacity: 0;
          transform: translateX(100px);
      }
  </style>
</head>
<body>

<div id="app">
  <input type="button" value="动起来" @click="myAnimate">
  <!-- 使用transition将需要过渡的元素包裹起来 -->
  <transition name="fade">  <!--transition使用name属性，则style样式中就会以定义的name作为前缀-->
    <div v-show="isShow">动画哦</div>
  </transition>
</div>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      isShow: false
    },
    methods: {
      myAnimate() {
        this.isShow = !this.isShow
      }
    }
  })
</script>
</body>
</html>
```

### 5.4 CSS动画

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
  <style>
      .bounce-enter-active {

          animation: bounce-in .5s;
      }

      .bounce-leave-active {
          animation: bounce-in .5s reverse;
      }

      @keyframes bounce-in {  /* 定义动画 */
          0% {
              transform: scale(0);
          }

          50% {
              transform: scale(1.5);
          }

          100% {
              transform: scale(1);
          }
      }

  </style>
</head>
<body>

<div id="app">
  <button @click="show = !show">Toggle Show</button>

  <transition name="bounce">
    <p v-if="show">这是一大段话这是一大段话这是一大段话这是一大段话这是一大段话这是一大段话这是一大段话这是一大段话这是一大段话这是一大段话</p>
  </transition>
</div>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      show: true
    },
    methods: {}
  })
</script>
</body>
</html>
```

### 5.5 自定义过渡的类名

通过以下attribute自定义过渡类名：

- enter-class
- enter-active-class
- enter-to-calss(2.1.8+)
- leave-class
- leave-active-class
- leave-to-calss(2.1.8+)

示例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
  <link href="https://cdn.jsdelivr.net/npm/animate.css@3.5.1" rel="stylesheet" type="text/css">
</head>
<body>

<div id="app">
  <button @click="show = !show">Toggle render</button>
  
  <!--自定义过渡的类名-->
  <transition
    name="custom-classes-transition"
    enter-active="animated tada"
    leave-active-class="animated bounceOutRight"
  >
    <p v-if="show">hello world</p>
  </transition>

</div>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      show: true
    },
    methods: {}
  })
</script>
</body>
</html>
```

### 5.6 显性的过度持续时间

> 很多情况下，Vue可以自动得出过渡效果的完成时机。默认情况下，Vue会等待其在过渡效果的根元素的第一个transitionend或animateend事件。然而也可以不这样设定，比如可以拥有一个精心编排的一系列过渡效果，其中一些嵌套的内部元素相比于过渡相国的根元素有延迟或更长的过渡效果。
>
> 这种情况下可以用<transition>组件上的duration prop定制一个显性的过度持续时间（单位为毫秒）

```html
<transition :duration="1000">...</transition>
```

也可以告知进入和移出的持续时间：

```html
<transition :duration="{ enter: 500, leave: 800}">...</transition>
```

### 5.7 JavaScript动画钩子函数

可以在transition的attribute中声明JavaScript钩子

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  <transition
    @before-enter="beforeEnter"
    @enter="enter"
    @after-enter="afterEnter"
    @enter-cancelled="enterCancelled"

    @before-leave="beforeLeave"
    @leave="leave"
    @after-leave="afterLeave"
    @leave-cancelled="leaveCancelled"
  >
    <!--  DOM元素  -->
  </transition>
</div>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {},
    methods: {
      // ----进入中-----
      beforeEnter(el) {
        // ...
      },
      // 当与CSS结合使用时，回调函数done是可选的
      enter(el, done) {
        // ...
        done()
      },
      afterEnter(el) {
        // ...
      },
      enterCancelled(el) {
        // ...
      }

      // ----离开时----
      beforeLeave(el) {
        // ...
      },
      // 当与 CSS 结合使用时
      // 回调函数 done 是可选的
      leave(el, done) {
        // ...
        done()
      },
      afterLeave(el) {
        // ...
      },
      // leaveCancelled 只用于 v-show 中
      leaveCancelled(el) {
        // ...
      }
    }
  })
</script>
</body>
</html>
```

这些钩子函数可以结合CSS <font color='red'>transitions/animations</font>使用，也可以单独使用。

当只用 JavaScript 过渡的时候，**在 `enter` 和 `leave` 中必须使用 `done` 进行回调**。否则，它们将被同步调用，过渡会立即完成。

推荐对于仅使用 JavaScript 过渡的元素添加 `v-bind:css="false"`，Vue 会跳过 CSS 的检测。这也可以避免过渡过程中 CSS 的影响。

案例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  <button @click="show = !show">Toggle</button>

  <transition @before-enter="beforeEnter" @enter="enter" @leave="leave" :css="false">
    <p v-if="show">Demo</p>
  </transition>
</div>
<script src="../vue.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/velocity/1.2.3/velocity.min.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      show: false
    },
    methods: {
      beforeEnter(el) {
        el.style.opacity = 0
        el.style.transformOrigin = 'left'
      },
      enter(el, done) {
        Velocity(el, {opacity: 1, fontSize: '1.4em'}, {duration: 300})
        Velocity(el, {fontSize: '1em'}, {complete: done})
      },
      leave(el, done) {
        Velocity(el, {translateX: '15px', rotateZ: '50deg'}, {duration: 600})
        Velocity(el, {rotateZ: '100deg'}, {loop: 2})
        Velocity(el, {
          rotateZ: '45deg',
          translateY: '30px',
          translateX: '30px',
          opacity: 0
        }, {complete: done})
      }
    },
  })
</script>
</body>
</html>
```

### 5.8  transition mode

`<transition>` 的默认行为 - 进入和离开同时发生。

同时生效的进入和离开的过渡不能满足所有要求，所以 Vue 提供了**过渡模式**

- `in-out`：新元素先进行过渡，完成之后当前元素过渡离开。
- `out-in`：当前元素先进行过渡，完成之后新元素过渡进入。

```html
<transition name="fade" mode="out-in">
  <!-- ... the buttons ... -->
</transition>
```

```html
<transition name="fade" mode="in-out">
  <!-- ... the buttons ... -->
</transition>
```

### 5.9 多个组件的过渡

多个组件的过渡简单很多 - 我们不需要使用 `key` attribute。相反，我们只需要使用[动态组件](https://cn.vuejs.org/v2/guide/components.html#动态组件)：

```html
<style>
	.component-fade-enter-active, .component-fade-leave-active {
    transition: opacity .3s ease;
  }
  .component-fade-enter, .component-fade-leave-to
  /* .component-fade-leave-active for below version 2.1.8 */ {
    opacity: 0;
  }
</style>

<transition name="component-fade" mode="out-in">
  <component v-bind:is="view"></component>
</transition>
<script>
	new Vue({
  el: '#transition-components-demo',
  data: {
    view: 'v-a'
  },
  components: {
    'v-a': {
      template: '<div>Component A</div>'
    },
    'v-b': {
      template: '<div>Component B</div>'
    }
  }
})
</script>
```

### 5.10 列表过渡

那么怎么同时渲染整个列表，比如使用 `v-for`？在这种场景中，使用 **`<transition-group>`** 组件。在我们深入例子之前，先了解关于这个组件的几个特点：

- 不同于 `<transition>`，它会以一个真实元素呈现：默认为一个 `<span>`。你也可以通过 `tag` attribute 更换为其他元素。
- [过渡模式](https://cn.vuejs.org/v2/guide/transitions.html#过渡模式)不可用，因为我们不再相互切换特有的元素。
- 内部元素**总是需要**提供唯一的 `key` attribute 值。
- CSS 过渡的类将会应用在内部的元素中，而不是这个组/容器本身。

列表的进入/离开过渡

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
  <style>
      /* transition-group中自定义了name属性，因此需要使用list为前缀 */
      .list-enter,
      .list-leave-to {
          opacity: 0;
          transform: translateY(10px);
      }

      .list-enter-active,
      .list-leave-active {
          transition: all 0.3s ease;
      }
  </style>
</head>
<body>

<div id="app">
  <input type="text" v-model="txt" @keyup.enter="add">


  <transition-group tag="ul" name="list">
    <li v-for="(item, i) in list" :key="i">{{ item }}</li>
  </transition-group>

</div>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      list: [1, 2, 3, 4],
      txt: ''
    },
    methods: {
      add() {
        this.list.push(this.txt)
        this.txt = ''
      }
    }
  })
</script>
</body>
</html>
```

### 5.11 列表的排序过渡

`<transition-group>` 组件还有一个特殊之处。不仅可以进入和离开动画，**还可以改变定位**。要使用这个新功能只需了解新增的 `v-move` 特性，**它会在元素的改变定位的过程中应用**。

`v-move` 和 `v-leave-active` 结合使用，能够让列表的过渡更加平缓柔和：

```css
.v-move{
  transition: all 0.8s ease;
}
.v-leave-active{
  position: absolute;
}
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
  <style>
    .flip-list-move {
        transition: transform 1s;
    }
  </style>
</head>
<body>

<div id="app">
  <button @click="shuffle">Shuffle</button>
  <transition-group name="flip-list" tag="ul">
    <li v-for="item in items" :key="item">
      {{ item }}
    </li>
  </transition-group>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.14.1/lodash.min.js"></script>
<script src="../vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    },
    methods: {
      shuffle() {
        this.items = _.shuffle(this.items)
      }
    }
  })
</script>
</body>
</html>
```

