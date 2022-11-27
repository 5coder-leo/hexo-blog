---
title: Composition API
author: 5coder
tags: Vue3.0
category: 大前端
abbrlink: 51960
date: 2022-11-26 19:37:13
password:
keywords:
top:
cover:
---

# Composition API

## 1.Composition API

接下来我们来介绍一下Vue3中新增的`Composition API`如何使用。注意`Composition API`仅仅是Vue3中新增的`API`，我们依然可以使用`Options API`。先来实现一下之前演示的获取鼠标位置的案例。做这个案例之前，需要先介绍一下`createApp`这个函数，这里不借助任何的构建工具，直接使用浏览器中原生的`ES Module`的方式来加载Vue模块。注意，这里我们会使用`vue.esm.browser.js`完整版的Vue。

首先，安装Vue3.0，创建`createApp.html`文件。

`createApp.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  x: {{ position.x }} <br>
  y: {{ position.y }} <br>

</div>
<script type="module">
  import { createApp } from './node_modules/vue/dist/vue.esm-browser.js'
  /*
  * createApp的作用是创建一个vue对象，它可以接受一个选项作为参数，也就是一个组件的选项，
  * 跟Vue2中给Vue构造函数传入的选项一样，它可以传入data、methods、create、computer等选项。
  *
  * */
  const app = createApp({
    data() {
      return {
        position: {
          x: 0,
          y: 0,
        }
      }
    }
  })

  console.log(app)
  app.mount('#app')

</script>
</body>
</html>
```

打开浏览器，可以看到打印出来的`app`对象。

![](http://5coder.cn/img/1669465331_c0664b226f5e122791cb93c0e789199e.png)

这里可以看到`X`和`Y`都可以正常响应式，然后打开开发人员工具来看一下刚刚打印的`vue`对象，把这个对象展开，这里的成员要比Vue2中的`vue`对象的成员要少很多，而且这些成员都没有使用`$`开头，说明未来我们基本不用给这个对象上新增成员。这里面可以看到`component` 、`directive`、 `mixin`还有`use`。它和以前的使用方式都是一样的，`mount`和过去的`$mount`的作用类似，还有一个`unmount`，它类似于过去的`$destroyed`。

`Composition API`还是在选项的这个位置来书写，不过要用到一个新的选项，叫做`setup`，`setup`函数是`Composition API`的入口。

> **setup执行的时机**
>
> **它是在`prop`被解析完毕，但是在组件实例被创建之前执行的**，所以在`setup`内部无法通过`this`获取到组件的实例，因为组件实例还未被创建，所以在`setup`中也无法访问到组件中的`data`、`computed`、`methods`， `setup`的内部的`this`此时指向的是`undefined`。

VUe3中提供了一个新的API，让我们来创建响应式对象，这个函数是`reactive`，在使用`reactive`之前，先要导入这个函数，在`import`的后边我们直接来导入`reactive`。导入完成之后，在`setup`中就可以使用`reactive`函数来创建响应式对象，

> `reactive`函数的作用是把一个对象转换成响应式对象，并且该对象的嵌套属性也都会转换成响应式对象，它返回的是一个`proxy`对象。

`createApp.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  x: {{ position.x }} <br>
  y: {{ position.y }} <br>

</div>
<script type="module">
  import { createApp, reactive } from './node_modules/vue/dist/vue.esm-browser.js'
  /*
  * createApp的作用是创建一个vue对象，它可以接受一个选项作为参数，也就是一个组件的选项，
  * 跟Vue2中给Vue构造函数传入的选项一样，它可以传入data、methods、create、computer等选项。
  *
  * */
  const app = createApp({
    setup() {
      // 第一个参数 props，props的作用是用来接收外部传入的参数，并且prop是一个响应式的对象，它不能被解构.
      // 第二个参数 context，它具有三个成员，分别是attrs、emit、slots
      // setUp需要返回一个对象，可以使用在template、methods compute以及生命周期的钩的函数中
      const position = reactive({
        x: 0,
        y: 0,
      })
      return {
        position
      }
    },
    mounted() {
      this.position.x = 100
    }
  })
  console.log(app)
  app.mount('#app')
</script>
</body>
</html>
```

![](http://5coder.cn/img/1669466208_33a2a2c09958052df8f9e31d9a598773.png)

## 2.生命周期钩子函数

接下来再来演示如何在`setup`中使用生命周期的钩子函数。先来回顾一下上面的案例，这里的响应式数据已经搞定了，下面需要注册鼠标移动的事件，当鼠标移动的时候响应式当前鼠标的位置。当这个组件被卸载的时候，这个鼠标移动的事件要被移除，注册`mousemove`事件可以在`mounted`来实现，但是别忘了最终的目标是要让获取鼠标位置的整个逻辑，封装到一个函数中，这样任何组件都可以重用。这个时候使用`mounted`的选项就不合适了。其实我们在`setup`中也可以使用生命周期的钩子函数。

在`setup`函数中可以使用组件生命周期中的钩子函数，但是需要在生命周期钩子函数前面加上`on`，然后首字母大写，比如选项中的`mounted`，在`setup`中对应的这个函数是`onMounted`。

另外，`setup`是在组件初始化之前执行的，是在`beforeCreate`和`created`之间执行的，所以在`beforeCreate`和`created`中的代码都可以放在`setup`函数中，这里的`beforeCreate`和`created`不需要在`setup`中有对应的实现。

下面的这些选项中的勾子函数的写法对应在`setup`中的实线，分别是在前面加上`on`，然后首字母大写。

注意这里的`unmounted`，它类似于之前的`destroyed`。还有下面的`renderTracked`、`renderTriggered`的这两个钩子函数非常相似，都是在`render`函数被重新调用的时候触发的。那它们不同的是`renderTracked`是在首次调用`render`的时候也会触发。`renderTriggered`在首次定用的时候不会触发。

![](http://5coder.cn/img/1669466538_85d98d1c6625e5779098d2e5b391a66a.png)

`createApp.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  x: {{ position.x }} <br>
  y: {{ position.y }} <br>

</div>
<script type="module">
  import { createApp, reactive, onMounted, onUnmounted } from './node_modules/vue/dist/vue.esm-browser.js'
  /*
  * createApp的作用是创建一个vue对象，它可以接受一个选项作为参数，也就是一个组件的选项，
  * 跟Vue2中给Vue构造函数传入的选项一样，它可以传入data、methods、create、computer等选项。
  *
  * */

  function useMousePosition() {
    // 第一个参数 props，props的作用是用来接收外部传入的参数，并且prop是一个响应式的对象，它不能被解构.
    // 第二个参数 context，它具有三个成员，分别是attrs、emit、slots
    // setUp需要返回一个对象，可以使用在template、methods compute以及生命周期的钩的函数中
    const position = reactive({
      x: 0,
      y: 0,
    })

    const update = e => {
      position.x = e.pageX
      position.y = e.pageY
    }

    // 注册事件
    onMounted(() => {
      window.addEventListener('mousemove', update)
    })
    // 移除事件
    onUnmounted(() => {
      window.removeEventListener('mousemove', update)
    })

    return position
  }

  const app = createApp({
    setup() {
      const position = useMousePosition()
      return {
        position
      }
    },
  })

  console.log(app)
  app.mount('#app')

</script>
</body>
</html>
```



## 3.reactive-toRefs-ref

接下来再来介绍`Composition API`中的三个函数，`reactive`、`toRefs`还有`ref`，这三个函数都是创建响应式数据的。

先从一个问题看起，先来看一下刚刚案例中使用的`reactive`函数的一个小问题。当我们不希望在模板中使用`position.x`和`position.y`，而是只是用`x`和`y`。可以在`setup`函数中解构`useMousePosition`的返回值。`const { x, y } = useMousePosition`，

并且直接在`setup`中返回`x`和`y`。

`createApp.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  x: {{ x }} <br>
  y: {{ y }} <br>

</div>
<script type="module">
  import { createApp, reactive, onMounted, onUnmounted } from './node_modules/vue/dist/vue.esm-browser.js'
  /*
  * createApp的作用是创建一个vue对象，它可以接受一个选项作为参数，也就是一个组件的选项，
  * 跟Vue2中给Vue构造函数传入的选项一样，它可以传入data、methods、create、computer等选项。
  *
  * */

  function useMousePosition() {
    // 第一个参数 props，props的作用是用来接收外部传入的参数，并且prop是一个响应式的对象，它不能被解构.
    // 第二个参数 context，它具有三个成员，分别是attrs、emit、slots
    // setUp需要返回一个对象，可以使用在template、methods compute以及生命周期的钩的函数中
    const position = reactive({
      x: 0,
      y: 0,
    })

    const update = e => {
      position.x = e.pageX
      position.y = e.pageY
    }

    // 注册事件
    onMounted(() => {
      window.addEventListener('mousemove', update)
    })
    // 移除事件
    onUnmounted(() => {
      window.removeEventListener('mousemove', update)
    })

    return position
  }

  const app = createApp({
    setup() {
      const { x, y } = useMousePosition()
      return {
        x,
        y
      }
    },
  })

  console.log(app)
  app.mount('#app')

</script>
</body>
</html>
```

此时，打开浏览器，发现鼠标移动，页面上的`x`和`y`并没有随着变化。这是为什么呢？

这里来解释一下，这里的`position`是响应式对象，因为我们在`useMousePosition`中去借用了`reactive`函数将传入的`position`对象包装成了`proxy`对象。将来访问`position`的`x`和`y`的时候，会调用代理对象`proxy`中的`getter`拦截收集依赖，当`x`和`y`变化之后，会调用代理对象`proxy`中的`setter`进行拦截触发更新。

当把代理对象解构的时候，当把`position`代理对象解构的时候，就相当于定义了`x`和`y`两个变量来接收`position.x`和`position.y`，而**基本类型的赋值就是把值在内存中复制一份，所以这里的`x`和`y`就是两个基本类型的变量，跟代理对象无关。**当重新给`x`和`y`赋值的时候，也不会调用代理对象的`setter`，无法触发更新的操作，所以不能对当前的响应式对象进行解构。

### 3.1 toRefs

如果我们就想像刚刚那么做呢？这里来介绍一个新的API，叫做`toRefs`，先演示它如何使用。

导入`toRefs`，在`useMousePosition`返回`position`时，使用`toRefs`包裹`position`。

`createApp.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  x: {{ x }} <br>
  y: {{ y }} <br>

</div>
<script type="module">
  import { createApp, reactive, onMounted, onUnmounted, toRefs } from './node_modules/vue/dist/vue.esm-browser.js'
  /*
  * createApp的作用是创建一个vue对象，它可以接受一个选项作为参数，也就是一个组件的选项，
  * 跟Vue2中给Vue构造函数传入的选项一样，它可以传入data、methods、create、computer等选项。
  *
  * */

  function useMousePosition() {
    // 第一个参数 props，props的作用是用来接收外部传入的参数，并且prop是一个响应式的对象，它不能被解构.
    // 第二个参数 context，它具有三个成员，分别是attrs、emit、slots
    // setUp需要返回一个对象，可以使用在template、methods compute以及生命周期的钩的函数中
    const position = reactive({
      x: 0,
      y: 0,
    })

    const update = e => {
      position.x = e.pageX
      position.y = e.pageY
    }

    // 注册事件
    onMounted(() => {
      window.addEventListener('mousemove', update)
    })
    // 移除事件
    onUnmounted(() => {
      window.removeEventListener('mousemove', update)
    })

    return toRefs(position)  // 可以把响应式对象中的所有属性，都转为响应式对象
  }

  const app = createApp({
    setup() {
      const { x, y } = useMousePosition()
      return {
        x,
        y
      }
    },
  })

  console.log(app)
  app.mount('#app')

</script>
</body>
</html>
```

现在来解释原因，toRefs要求我们传入的这个参数必须是一个代理对象`proxy`，当前的`position`就是我们`reactive`返回的一个代理对象，如果的`position`不是代理对象的话，它会报警告，提示需要传递代理对象。

**接下来它内部会创建一个新的对象，然后遍历传入的这个代理对象的所有属性，把所有属性的值都转换成响应式对象**。注意`toRefs`里边是把`position`这个对象的**所有属性的值都转换成响应式对象**，**然后再挂载到新创建的对象上，最后把这个新创建的对象返回。**

它内部会为代理对象的每一个属性创建一个具有`value`属性的对象，该对象是响应式的`value`属性，具有`getter`和`setter`，这一点和下面要讲的`ref`函数类似。`getter`里面返回代理对象中对应属性的值，`setter`中给代理对象的属性赋值，所以返回的每一个属性都是响应式的。

`toRefs`这个函数的作用就是把对象的每一个属性都转换成响应式数据，所以可以解构`toRefs`返回的对象，解构的每一个属性也都是响应式。下边在解构的时候，解构的是`toRefs`这个函数返回的新的对象，这个对象的所有属性都是响应式对象，并且这个属性是一个对象，它有一个`value`属性，在模板中使用的时候可以把这个value省略，但是我们在代码中去写的时候，这个`value`是不可以去省略的，我们稍后的时候会去演示。

### 3.2 ref

接下来再来介绍一个响应式的API，叫做`ref`，这是一个函数，它的作用是把普通数据转换成响应式数据。和`reactive`不同的是，`reactive`是把一个对象转换成响应式数据。`ref`可以把基本类型的数据包装成响应式对象。

ref.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
<div id="app">
  <button @click="increase">按钮</button>
  <span>{{ count }}</span>
</div>
<script type="module">
  import { createApp, ref } from './node_modules/vue/dist/vue.esm-browser.js'

  function useCount () {
    const count = ref(0)
    return {
      count,
      increase: () => {
        count.value++
      }
    }
  }

  createApp({
    setup () {
      return {
        ...useCount()
      }
    }
  }).mount('#app')
</script>
</body>
</html>
```

下面来解释一下`ref`内部做了什么？首先基本数据类型，它存储的是值，所以它不可能是响应式数据，我们知道响应式数据要通过该收集依赖通过`setter`触发更新。
`ref`的参数它如果是对象，内部会调用`reactive`返回一个代理对象，也就是如果调用`ref`的时候，参数传递的是对象的话，它内部其实就是调用reactive。
`ref`的参数如果是基本类型的值，比如我们传入的是`0`，它内部会创建一个只有`value`属性的对象，该对象的`value`属性具有getter和`setter`，在`getter`中收集依赖在`setter`中触发更新。

## 4.computed

接下来我们再来介绍几个API。首先来看计算属性，计算属性的作用是简化模板中的代码，可以缓存计算的结果，当数据变化后才会重新计算。

我们依然可以向`Vue2.x`的时候，在创建组件的时候传入`computed`的选项来创建计算属性。在`Vue3`中，也可以在`setup`中通过`computed`的函数来创建计算属性。`computed`的函数有两种用法，第一种是传入一个获取值的函数，函数内部依赖响应式的数据，当依代的数据发生变化后，会重新执行该函数获取数据。computed的函数返回一个不可变的响应式对象，类似于使用ref创建的对象只有一个value属性。

获取计算属性的值要通过`value`属性来获取，模板中使用计算属性可以省略`value`， `computed`的第二种用法是传入一个对象，这个对象具有`getter`和`setter`，返回一个不可变的响应式对象。例如下面这段代码，当获取值的时候会触发这个对象的`getter`，当设置值的时候会触发这个对象的`setter`。

![](http://5coder.cn/img/1669474552_a1fb07f90ef993fff8637a7673ccf3f9.png)

> 这里已经创建好了一个页面，并且做了一些准备工作。我们这里放了一个按钮，当点击按钮的时候，会利用push方法创建一个待办事项，下面去显示未完成的代办事项个数。

`computed.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <button @click="push">按钮</button>
    未完成：{{ activeCount }}
  </div>
  <script type="module">
    import { createApp, reactive, computed } from './node_modules/vue/dist/vue.esm-browser.js'
    const data = [
      { text: '看书', completed: false },
      { text: '敲代码', completed: false },
      { text: '约会', completed: true }
    ]

    createApp({
      setup () {
        const todos = reactive(data)

        const activeCount = computed(() => {
          return todos.filter(item => !item.completed).length
        })

        return {
          activeCount,
          push: () => {
            todos.push({
              text: '开会',
              completed: false
            })
          }
        }
      }
    }).mount('#app')
  </script>
</body>
</html>
```

点击页面中的按钮后，可以发现未完成的数量+1。当往`todos`中添加一项的时候，`todos`变化了，计算属性中传入的函数会重新执行，重新获取未完成的待办事项的个数。

`computed`可以创建一个响应式的数据，这个显示的数据依赖于其他响应式的数据，当依赖类的数据发生变化后，会重新计算属性传入的这个函数。

## 5.watch

接下来我们再来看侦听器。和`computed`类似，在`setup`函数中可以使用`watch`来创建一个侦听器，它的使用方式和之前使用`this.$watch`或者选项中的`watch`作用是一样的，监听响应式数据的变化，然后执行一个相应的回调函数，可以获取到监听数据的新值和旧值。



- Watch的三个参数
  - 要监听的数据
  - 监听到数据变化后执行的函数，这个函数有两个参数分别是新值和旧值
  - 选项对象，deep和immediate
- Watch的返回值
  - 取消监听的函数

下面来介绍一下要写的这个案例。这个案例来自`vue`的官网，这是一个选择困难症必备的应用，可以在这个文本框中输入一个只需要回答是和否的问题，然后会发送一个请求，请求这个接口，它会随机返回一个`yes or no`。这个接口除了返回`yes no`之外，还会随机返回一个好玩的图片，如果你需要的话，可以把图片也展示出来。

`watch.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <p>
      请问一个 yes/no 的问题:
      <input v-model="question">
    </p>
    <p>{{ answer }}</p>
  </div>

  <script type="module">
    // https://www.yesno.wtf/api
    import { createApp, ref, watch } from './node_modules/vue/dist/vue.esm-browser.js'

    createApp({
      setup () {
        const question = ref('')
        const answer = ref('')

        watch(question, async (newValue, oldValue) => {
          const response = await fetch('https://www.yesno.wtf/api')
          const data = await response.json()
          answer.value = data.answer
        })

        return {
          question,
          answer
        }
      }
    }).mount('#app')
  </script>
</body>
</html>
```

模板中用到了`question`和`answer`，所以需要在`setup`中定义并且返回`question`和`answer` ，`question`和`answer`都是响应式的，因为他们都是自符串，所以这里可以使用`ref`来创建响应式的对象。定义`question`和`answer` ，`question`就等于通过`ref`来创建我们这个响应式对象，`question`里边其实存储的就是一个字符串，接下来再创建一个`answer`。`ref`返回的对象是不可变的，可以改变这个对象的value属性。

当用户在文本框中输入问题以后，也就是`question`的值发生变化之后，这个时候要发送请求，获取答案给`answer`赋值，所以这里我们要监听`question`的变化，我们要用到watch。`watch`函数的第一个参数是`ref`或者`reactive`返回的对象，要监听`question`，**注意第一个参数，这个位置跟以前不一样，我们在Vue2使用`this.$watch`的时候，第一个参数是字符串。**然后是回调函数，这个回调函数可以接收新值和旧值。第三个参数我们暂时不需要。

当值变化之后，我们要去请求这个接口，那这里我们直接用`fetch`来发送请求。

`fetch`返回的是一个`promise`对象，所以这块可以用`async`、`await`来简化调用。当拿到`response`之后，要解析出来里边的答案，给`answer`去赋值，给`answer`赋值的时候，注意要给`answer`的`value`属性来赋值，注意`response.json()`它返回的也是一个`promise`对象。在`setup`的最后，还要把`question`和`answer`返回。

打开浏览器来测试一下。

![](http://5coder.cn/img/1669475876_654c7a03305d7dfede1bc55e2570dd4e.png)

`watch`使用起来和过去的`this.$watch`是一样的，**不一样的是第一个参数不是字符串，而是`ref`或者返回的对象。**

## 6.watchEffect

在Vue3中还提供了一个新的函数`watchEffect`，它其实就是`watch`函数的简化版本。内部实现是和`watch`调用的同一个函数`doWatch`，不同的是，`watchEffect`没有第二个回调函数的参数。`watchEffect`接受一个函数作为参数，它会监听这个函数内部使用的响应式数据的变化，它会立即执行一次这个函数，当数据变化之后会重新运行该函数。它也返回一个取消监听的函数。

- 是watch函数的简化版本，也用来监视数据的变化
- 接受一个函数作为参数，监听函数内响应式数据的变化

`watchEffect.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <button @click="increase">increase</button>
    <button @click="stop">stop</button>
    <br>
    {{ count }}
  </div>

  <script type="module">
    import { createApp, ref, watchEffect } from './node_modules/vue/dist/vue.esm-browser.js'

    createApp({
      setup () {
        const count = ref(0)
        const stop = watchEffect(() => {
          console.log(count.value)
        })

        return {
          count,
          stop,
          increase: () => {
            count.value++
          }
        }
      }
    }).mount('#app')
  </script>
</body>
</html>
```

`watchEffect`中的函数初始的时候首先会执行一次，当count的值发生变化的时候，这个函数会再次被调用，另外`watchEffect`会返回一个函数，取消对数据的监视。点击stop后，再次点击`increase`，发现模板中的数据在增加，而控制台并没有再进行输出。

后续的案例中我们会使用`watchEffect`监听数据的变化，当数据变化后，把变化的数据存储到`localStory`中，那这个时候使用`watchEffect`会非常的方便。

![](http://5coder.cn/img/1669476246_2bf923bba68c50a62b8c649348b7eab2.png)

## 7.todolist-功能演示

接下来我们来做一个案例`todoList`，`todoList`是代办事项清单，平时工作或者学习的时候也应该有一个自己的代办事项清单，它是一个非常经典的案例，学习一个新的技术后，可以通过这个案例快速来巩固所学的知识。

todoList需要实现以下功能：

- 添加待办事项
- 删除待办事项
- 编辑待办事项
- 切换待办事项
- 存储待办事项

## 8.todolist-项目结构

之前的案例都是直接在网页上引用`vue`模块，接下来在做todoList案例的时候，使用vue的脚手架来创建项目。首先我们升级`vue-cli`到4.5以上的版本，新版本在创建项目的时候可以选择使用view3.0，`vue-cli`使用的方式和之前是一样的，先使用vue create创建项目，创建项目的时候选择vue3.0。

全局安装/升级@vue/cli：`npm install -g @vue/cli`

vue create my-todolist

```bash
vue create my-todolist
```

使用Vue3![](http://5coder.cn/img/1669529708_69a7ab8d72f07b9f12ec09760cdac025.png)

已经创建好了项目，并把组件和样式文件都提前设置好了。那下面我们来看一下页面的结构，然后一个功能一个功能来实现。

![](http://5coder.cn/img/1669530237_ea487411430452585531023b5fad7ee6.png)

`App.vue`

```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
      >
    </header>
    <section class="main">
      <input id="toggle-all" class="toggle-all" type="checkbox">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li>
          <div class="view">
            <input class="toggle" type="checkbox">
            <label>测试数据</label>
            <button class="destroy"></button>
          </div>
          <input type="text" class="edit">
        </li>
        <li>
          <div class="view">
            <input class="toggle" type="checkbox">
            <label>测试数据</label>
            <button class="destroy"></button>
          </div>
          <input type="text" class="edit">
        </li>
      </ul>
    </section>
    <footer class="footer">
      <span class="todo-count">
        <strong>1</strong>item left
      </span>
      <ul class="filters">
        <li><a href="#/all">All</a></li>
        <li><a href="#/active">Active</a></li>
        <li><a href="#/completed">Completed</a></li>
      </ul>
      <button class="clear-completed" v-show="count > remainingCount">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'

export default {
  name: 'App',
  setup () {

  },

}
</script>

<style>
</style>

```

运行`yarn serve`查看效果

![](http://5coder.cn/img/1669530272_7e23510991ca1e1d7c460178c111fb0e.png)

## 9.todolist-添加待办事项

```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
          v-model="input"
          @keyup.enter="addTodo"
      >
    </header>
    <section class="main">
      <input id="toggle-all" class="toggle-all" type="checkbox">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li
            v-for="todo in todos"
            :key="todo.text"
        >
          <div class="view">
            <input class="toggle" type="checkbox">
            <label>{{ todo.text }}</label>
            <button class="destroy"></button>
          </div>
          <input type="text" class="edit">
        </li>
      </ul>
    </section>
    <footer class="footer">
      <span class="todo-count">
        <strong>1</strong>item left
      </span>
      <ul class="filters">
        <li><a href="#/all">All</a></li>
        <li><a href="#/active">Active</a></li>
        <li><a href="#/completed">Completed</a></li>
      </ul>
      <button class="clear-completed">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'
import { ref } from 'vue'

// 1.添加待办事项

const useAdd = todos => {
  const input = ref('') // 创建响应式数据
  const addTodo = () => {
    const text = input.value && input.value.trim()  // 获取输入框的值，并去除前后空格
    if (text.length === 0) return
    // 添加到todos数组中，用于模板渲染
    todos.value.unshift({
      text,
      completed: false
    })
    // 回车后，清空输入框
    input.value = ''
  }
  // 返回响应式数据和方法
  return {
    input,
    addTodo
  }
}

export default {
  name: 'App',
  setup() {
    // 初始化todos
    const todos = ref([])
    return {
      ...useAdd(todos),
      todos
    }
  }
}
</script>

<style>
</style>
```

查看效果

![](http://5coder.cn/img/1669531049_496c3bc768c73c976bb69abffc04561f.png)

到这我们的第一个任务添加待办事项就完成了。

## 10.todolist-删除待办事项

```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
          v-model="input"
          @keyup.enter="addTodo"
      >
    </header>
    <section class="main">
      <input id="toggle-all" class="toggle-all" type="checkbox">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li
            v-for="todo in todos"
            :key="todo.text"
        >
          <div class="view">
            <input class="toggle" type="checkbox">
            <label>{{ todo.text }}</label>
            <button class="destroy" @click="remove(todo)"></button>
          </div>
          <input type="text" class="edit">
        </li>
      </ul>
    </section>
    <footer class="footer">
      <span class="todo-count">
        <strong>1</strong>item left
      </span>
      <ul class="filters">
        <li><a href="#/all">All</a></li>
        <li><a href="#/active">Active</a></li>
        <li><a href="#/completed">Completed</a></li>
      </ul>
      <button class="clear-completed">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'
import { ref } from 'vue'

// 1.添加待办事项
const useAdd = todos => {
  const input = ref('')
  const addTodo = () => {
    const text = input.value && input.value.trim()
    if (text.length === 0) return
    todos.value.unshift({
      text,
      completed: false
    })
    input.value = ''
  }
  return {
    input,
    addTodo
  }
}

// 2.删除待办事项
const useRemove = todos => {
  const remove = todo => {
    const index = todos.value.indexOf(todo)  // 找到todo在todos中的索引
    todos.value.splice(index, 1)  // 删除改元素
  }
  return {
    remove
  }
}

export default {
  name: 'App',
  setup() {
    const todos = ref([])
    return {
      todos,
      ...useAdd(todos),
      ...useRemove(todos)
    }
  },

}
</script>

<style>
</style>

```

## 11.todolist-编辑待办事项

- 双击待办项,展示编辑文本框
- 按回车或者编辑文本框失去焦点,修改数据
- 按esc取消编辑
- 把编辑文本框清空按回车，删除这一项·显示编辑文本框的时候获取焦点

App.vue

```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
          v-model="input"
          @keyup.enter="addTodo"
      >
    </header>
    <section class="main">
      <input id="toggle-all" class="toggle-all" type="checkbox">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li
            v-for="todo in todos"
            :key="todo"
            :class="{ editing: todo === editingTodo }"
        >
          <div class="view">
            <input class="toggle" type="checkbox">
            <label @dblclick="editTodo(todo)">{{ todo.text }}</label>
            <button class="destroy" @click="remove(todo)"></button>
          </div>
          <input
              type="text"
              class="edit"
              v-model="todo.text"
              @keyup.enter="doneEdit(todo)"
              @blur="doneEdit(todo)"
              @keyup.esc="cancelEdit(todo)"
          >
        </li>
      </ul>
    </section>
    <footer class="footer">
      <span class="todo-count">
        <strong>1</strong>item left
      </span>
      <ul class="filters">
        <li><a href="#/all">All</a></li>
        <li><a href="#/active">Active</a></li>
        <li><a href="#/completed">Completed</a></li>
      </ul>
      <button class="clear-completed">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'
import { ref } from 'vue'

// 1.添加待办事项
const useAdd = todos => {
  const input = ref('')
  const addTodo = () => {
    const text = input.value && input.value.trim()
    if (text.length === 0) return
    todos.value.unshift({
      text,
      completed: false
    })
    input.value = ''
  }
  return {
    input,
    addTodo
  }
}

// 2.删除待办事项
const useRemove = todos => {
  const remove = todo => {
    const index = todos.value.indexOf(todo)  // 找到todo在todos中的索引
    todos.value.splice(index, 1)
  }
  return {
    remove
  }
}

// 3.编辑待办项
const useEdit = (remove) => {
  let beforeEditingText = ''  // 保存编辑前的文本框的值
  const editingTodo = ref(null)  // 记录当前是否是编辑状态

  // 编辑todo
  const editTodo = (todo) => {
    beforeEditingText = todo.text
    editingTodo.value = todo
  }

  // 完成编辑todo
  const doneEdit = (todo) => {
    if (!editingTodo.value) return
    todo.text = todo.text.trim()
    todo.text || remove(todo)
    editingTodo.value = null
  }

  // 取消编辑todo
  const cancelEdit = todo => {
    editingTodo.value = null
    todo.text = beforeEditingText
  }

  return {
    editingTodo,
    editTodo,
    doneEdit,
    cancelEdit
  }

}

export default {
  name: 'App',
  setup() {
    const todos = ref([])
    const { remove } = useRemove(todos)

    return {
      todos,
      remove,
      ...useAdd(todos),
      ...useEdit(remove)
    }
  },

}
</script>

<style>
</style>

```

此时还没有处理“自动获得焦点”

## 12.todolist-编辑待办事项-编辑文本框获取焦点

下面来实现在编辑代办事项的时候让编辑文本框块获得焦点。这里需要用到自定义指令，Vue3中自定义指令的使用方式和Vue2中稍有不同。先来介绍一下Vue2和Vue3中自定义指令的差别。主要是自定义指令的钩子函数被重命名，**Vue3把钩子函数的名称和组件中钩子函数的名称保持一致，这样很容易理解，但是自定义指令的钩子函数和组件钩子函数的执行方式是不一样的**。

Vue3中的钩子函数的名称，它有三组，分别是`mount`、`update`还有`unmounted`，分别是在自定义指令修饰的元素被挂载到DOM树、更新、卸载的时候执行。这是自定义指令的第一种用法，在创建自定义指令的时候还可以传函数，这种用法比较简洁，更常用一些。第二个参数是函数的时候，Vue3和Vue2的用法是一样的。

指定名称后面的这个函数在Vue3的时候是在`mounted`和`update`的时候去执行，跟Vue2的执行实际其实是一样的。Vue2里这个函数是在`bind`和`update`的时候执行，那这个函数的`el`参数是我们指令所绑定的那个元素，`binding`这个参数可以获取到指定对应的值，通过`binding.value`来获取。

![](http://5coder.cn/img/1669545122_848f767bedabc54228ee212732aaf877.png)

![](http://5coder.cn/img/1669545189_e3b1caa702f75c94f405acd54bc039e5.png)

```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
          v-model="input"
          @keyup.enter="addTodo"
      >
    </header>
    <section class="main">
      <input id="toggle-all" class="toggle-all" type="checkbox">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li
            v-for="todo in todos"
            :key="todo"
            :class="{ editing: todo === editingTodo }"
        >
          <div class="view">
            <input class="toggle" type="checkbox">
            <label @dblclick="editTodo(todo)">{{ todo.text }}</label>
            <button class="destroy" @click="remove(todo)"></button>
          </div>
          <input
              type="text"
              class="edit"
              v-editing-focus="todo === editingTodo"
              v-model="todo.text"
              @keyup.enter="doneEdit(todo)"
              @blur="doneEdit(todo)"
              @keyup.esc="cancelEdit(todo)"
          >
        </li>
      </ul>
    </section>
    <footer class="footer">
      <span class="todo-count">
        <strong>1</strong>item left
      </span>
      <ul class="filters">
        <li><a href="#/all">All</a></li>
        <li><a href="#/active">Active</a></li>
        <li><a href="#/completed">Completed</a></li>
      </ul>
      <button class="clear-completed">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'
import { ref } from 'vue'

// 1.添加待办事项
const useAdd = todos => {
  const input = ref('')
  const addTodo = () => {
    const text = input.value && input.value.trim()
    if (text.length === 0) return
    todos.value.unshift({
      text,
      completed: false
    })
    input.value = ''
  }
  return {
    input,
    addTodo
  }
}

// 2.删除待办事项
const useRemove = todos => {
  const remove = todo => {
    const index = todos.value.indexOf(todo)  // 找到todo在todos中的索引
    todos.value.splice(index, 1)
  }
  return {
    remove
  }
}

// 3.编辑待办项
const useEdit = (remove) => {
  let beforeEditingText = ''  // 保存编辑前的文本框的值
  const editingTodo = ref(null)  // 记录当前是否是编辑状态

  // 编辑todo
  const editTodo = (todo) => {
    beforeEditingText = todo.text
    editingTodo.value = todo
  }

  // 完成编辑todo
  const doneEdit = (todo) => {
    if (!editingTodo.value) return
    todo.text = todo.text.trim()
    todo.text || remove(todo)
    editingTodo.value = null
  }

  // 取消编辑todo
  const cancelEdit = todo => {
    editingTodo.value = null
    todo.text = beforeEditingText
  }

  return {
    editingTodo,
    editTodo,
    doneEdit,
    cancelEdit
  }

}

export default {
  name: 'App',
  setup() {
    const todos = ref([])
    const { remove } = useRemove(todos)

    return {
      todos,
      remove,
      ...useAdd(todos),
      ...useEdit(remove)
    }
  },
  directives: {
    editingFocus: (el, binding) => {
      binding.value && el.focus()
    }
  }

}
</script>

<style>
</style>
```

![image-20221127183636520](http://5coder.cn/img/1669545396_0dc67982467553590e47314ebf739f72.png)

## 13.todolist-切换待办事项-演示效果

![](http://5coder.cn/img/1669546229_b65788a679ea40468d56530c55d36289.png)

- 点击checkbox，改变所有待办项状态
- All/Active/Completed
- 其它
  - 显示未完成待办项个数
  - 移除所有完成的项目
  - 如果没有待办项，隐藏 main和 footer

## 14.todolist-切换待办事项-改变待办事项完成状态

接下来开始来做切换待办事项状态的第一个子任务，点击`checkbox`，改变所有待办事项的完成状态。

```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
          v-model="input"
          @keyup.enter="addTodo"
      >
    </header>
    <section class="main">
      <input id="toggle-all" class="toggle-all" type="checkbox" v-model="allDone">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li
            v-for="todo in todos"
            :key="todo"
            :class="{ editing: todo === editingTodo, completed: todo.completed }"
        >
          <div class="view">
            <input class="toggle" type="checkbox" v-model="todo.completed">
            <label @dblclick="editTodo(todo)">{{ todo.text }}</label>
            <button class="destroy" @click="remove(todo)"></button>
          </div>
          <input
              type="text"
              class="edit"
              v-editing-focus="todo === editingTodo"
              v-model="todo.text"
              @keyup.enter="doneEdit(todo)"
              @blur="doneEdit(todo)"
              @keyup.esc="cancelEdit(todo)"
          >
        </li>
      </ul>
    </section>
    <footer class="footer">
      <span class="todo-count">
        <strong>1</strong>item left
      </span>
      <ul class="filters">
        <li><a href="#/all">All</a></li>
        <li><a href="#/active">Active</a></li>
        <li><a href="#/completed">Completed</a></li>
      </ul>
      <button class="clear-completed">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'
import { computed, ref } from 'vue'

// 1.添加待办事项
const useAdd = todos => {
  const input = ref('')
  const addTodo = () => {
    const text = input.value && input.value.trim()
    if (text.length === 0) return
    todos.value.unshift({
      text,
      completed: false
    })
    input.value = ''
  }
  return {
    input,
    addTodo
  }
}

// 2.删除待办事项
const useRemove = todos => {
  const remove = todo => {
    const index = todos.value.indexOf(todo)  // 找到todo在todos中的索引
    todos.value.splice(index, 1)
  }
  return {
    remove
  }
}

// 3.编辑待办项
const useEdit = (remove) => {
  let beforeEditingText = ''  // 保存编辑前的文本框的值
  const editingTodo = ref(null)  // 记录当前是否是编辑状态

  // 编辑todo
  const editTodo = (todo) => {
    beforeEditingText = todo.text
    editingTodo.value = todo
  }

  // 完成编辑todo
  const doneEdit = (todo) => {
    if (!editingTodo.value) return
    todo.text = todo.text.trim()
    todo.text || remove(todo)
    editingTodo.value = null
  }

  // 取消编辑todo
  const cancelEdit = todo => {
    editingTodo.value = null
    todo.text = beforeEditingText
  }

  return {
    editingTodo,
    editTodo,
    doneEdit,
    cancelEdit
  }

}

// 4.切换待办项完成状态
const useFilter = (todos) => {
  const allDone = computed({
    get() {
      return !todos.value.filter(todo => !todo.completed).length
    },
    set(value) {
      todos.value.forEach(todo => {
        todo.completed = value
      })
    }
  })

  return {
    allDone
  }
}

export default {
  name: 'App',
  setup() {
    const todos = ref([])
    const { remove } = useRemove(todos)

    return {
      todos,
      remove,
      ...useAdd(todos),
      ...useEdit(remove),
      ...useFilter(todos)
    }
  },
  directives: {
    editingFocus: (el, binding) => {
      binding.value && el.focus()
    }
  }

}
</script>

<style>
</style>
```

## 15.todolist-切换待办事项-切换状态

接下来再来实现切换待办事项状态的第二个子任务，点击`all`、`active`、`completed`个超链接的时候，查看不同状态的待办事项。

在模板中，先找到三个超链接的位置，超链接的`href`属性是三个锚点，这里不使用路由功能，自己来实现。首先要监视地址中`hash`的变化，当组件挂载完毕，要注册`hashChange`事件。当组件卸载的时候，要把`hashChange`事件移除。在`hashChange`事件中，要获取当前锚点的值，只需要这里的单词`all`、`active`、`completed`，所以可以把前面的`#`号杠去掉。然后再根据`hash`来判断当前要获取哪种状态的待办事项列表。

把过滤代办事项数据的函数定义到一个对象，然后根据`hash`的值去对象中获取对应的函数，当然函数的名称跟`hash`值是一样的，这是核心思路，这样写的话，就避免了写一堆if语句。

```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
          v-model="input"
          @keyup.enter="addTodo"
      >
    </header>
    <section class="main">
      <input id="toggle-all" class="toggle-all" type="checkbox" v-model="allDone">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li
            v-for="todo in filteredTodos"
            :key="todo"
            :class="{ editing: todo === editingTodo, completed: todo.completed }"
        >
          <div class="view">
            <input class="toggle" type="checkbox" v-model="todo.completed">
            <label @dblclick="editTodo(todo)">{{ todo.text }}</label>
            <button class="destroy" @click="remove(todo)"></button>
          </div>
          <input
              type="text"
              class="edit"
              v-editing-focus="todo === editingTodo"
              v-model="todo.text"
              @keyup.enter="doneEdit(todo)"
              @blur="doneEdit(todo)"
              @keyup.esc="cancelEdit(todo)"
          >
        </li>
      </ul>
    </section>
    <footer class="footer">
      <span class="todo-count">
        <strong>1</strong>item left
      </span>
      <ul class="filters">
        <li><a href="#/all">All</a></li>
        <li><a href="#/active">Active</a></li>
        <li><a href="#/completed">Completed</a></li>
      </ul>
      <button class="clear-completed">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'
import { computed, onMounted, onUnmounted, ref } from 'vue'

// 1.添加待办事项
const useAdd = todos => {
  const input = ref('')
  const addTodo = () => {
    const text = input.value && input.value.trim()
    if (text.length === 0) return
    todos.value.unshift({
      text,
      completed: false
    })
    input.value = ''
  }
  return {
    input,
    addTodo
  }
}

// 2.删除待办事项
const useRemove = todos => {
  const remove = todo => {
    const index = todos.value.indexOf(todo)  // 找到todo在todos中的索引
    todos.value.splice(index, 1)
  }
  return {
    remove
  }
}

// 3.编辑待办项
const useEdit = (remove) => {
  let beforeEditingText = ''  // 保存编辑前的文本框的值
  const editingTodo = ref(null)  // 记录当前是否是编辑状态

  // 编辑todo
  const editTodo = (todo) => {
    beforeEditingText = todo.text
    editingTodo.value = todo
  }

  // 完成编辑todo
  const doneEdit = (todo) => {
    if (!editingTodo.value) return
    todo.text = todo.text.trim()
    todo.text || remove(todo)
    editingTodo.value = null
  }

  // 取消编辑todo
  const cancelEdit = todo => {
    editingTodo.value = null
    todo.text = beforeEditingText
  }

  return {
    editingTodo,
    editTodo,
    doneEdit,
    cancelEdit
  }

}

// 4.切换待办项完成状态
const useFilter = (todos) => {
  const allDone = computed({
    get() {
      return !todos.value.filter(todo => !todo.completed).length
    },
    set(value) {
      todos.value.forEach(todo => {
        todo.completed = value
      })
    }
  })

  const filter = {
    all: list => list,
    active: list => list.filter(todo => !todo.completed),
    completed: list => list.filter(todo => todo.completed),
  }

  const type = ref('all')  // 保存type
  const filteredTodos = computed(() => filter[type.value](todos.value))  // 计算属性
  const onHashChange = () => {
    const hash = window.location.hash.replace('#/', '')
    console.log('hash',hash)
    if (filter[hash]) {
      console.log(11)
      type.value = hash
    } else {
      type.value = 'all'
      window.location.hash = ''
    }
  }

  onMounted(() => {
    window.addEventListener('hashchange', onHashChange)
    onHashChange()
  })

  onUnmounted(() => {
    window.removeEventListener('hashchange', onHashChange)
  })

  return {
    allDone,
    filteredTodos
  }
}

export default {
  name: 'App',
  setup() {
    const todos = ref([])
    const { remove } = useRemove(todos)

    return {
      todos,
      remove,
      ...useAdd(todos),
      ...useEdit(remove),
      ...useFilter(todos)
    }
  },
  directives: {
    editingFocus: (el, binding) => {
      binding.value && el.focus()
    }
  }

}
</script>

<style>
</style>
```

## 16.todolist-切换待办事项-其它

- 显示待办事项个数
- 删除已完成的待办事项

```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
          v-model="input"
          @keyup.enter="addTodo"
      >
    </header>
    <section class="main" v-show="count">
      <input id="toggle-all" class="toggle-all" type="checkbox" v-model="allDone">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li
            v-for="todo in filteredTodos"
            :key="todo"
            :class="{ editing: todo === editingTodo, completed: todo.completed }"
        >
          <div class="view">
            <input class="toggle" type="checkbox" v-model="todo.completed">
            <label @dblclick="editTodo(todo)">{{ todo.text }}</label>
            <button class="destroy" @click="remove(todo)"></button>
          </div>
          <input
              type="text"
              class="edit"
              v-editing-focus="todo === editingTodo"
              v-model="todo.text"
              @keyup.enter="doneEdit(todo)"
              @blur="doneEdit(todo)"
              @keyup.esc="cancelEdit(todo)"
          >
        </li>
      </ul>
    </section>
    <footer class="footer" v-show="count">
      <span class="todo-count">
        <strong>{{ remainingCount }}</strong> {{ remainingCount > 1 ? "items" : "item" }} left
      </span>
      <ul class="filters">
        <li><a href="#/all" :class="{active : type === 'all'}">All</a></li>
        <li><a href="#/active" :class="{active : type === 'active'}">Active</a></li>
        <li><a href="#/completed" :class="{active : type === 'completed'}">Completed</a></li>
      </ul>
      <button class="clear-completed" @click="removeCompleted" v-show="count > remainingCount">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'
import { computed, onMounted, onUnmounted, ref } from 'vue'

// 1.添加待办事项
const useAdd = todos => {
  const input = ref('')
  const addTodo = () => {
    const text = input.value && input.value.trim()
    if (text.length === 0) return
    todos.value.unshift({
      text,
      completed: false
    })
    input.value = ''
  }
  return {
    input,
    addTodo
  }
}

// 2.删除待办事项
const useRemove = todos => {
  const remove = todo => {
    const index = todos.value.indexOf(todo)  // 找到todo在todos中的索引
    todos.value.splice(index, 1)


  }
  // 删除已完成的待办事项
  const removeCompleted = () => {
    todos.value = todos.value.filter(todo => !todo.completed)
  }
  return {
    remove,
    removeCompleted
  }
}

// 3.编辑待办项
const useEdit = (remove) => {
  let beforeEditingText = ''  // 保存编辑前的文本框的值
  const editingTodo = ref(null)  // 记录当前是否是编辑状态

  // 编辑todo
  const editTodo = (todo) => {
    beforeEditingText = todo.text
    editingTodo.value = todo
  }

  // 完成编辑todo
  const doneEdit = (todo) => {
    if (!editingTodo.value) return
    todo.text = todo.text.trim()
    todo.text || remove(todo)
    editingTodo.value = null
  }

  // 取消编辑todo
  const cancelEdit = todo => {
    editingTodo.value = null
    todo.text = beforeEditingText
  }

  return {
    editingTodo,
    editTodo,
    doneEdit,
    cancelEdit
  }

}

// 4.切换待办项完成状态
const useFilter = (todos) => {
  const allDone = computed({
    get() {
      return !todos.value.filter(todo => !todo.completed).length
    },
    set(value) {
      todos.value.forEach(todo => {
        todo.completed = value
      })
    }
  })

  const filter = {
    all: list => list,
    active: list => list.filter(todo => !todo.completed),
    completed: list => list.filter(todo => todo.completed),
  }

  const type = ref('all')  // 保存type
  const filteredTodos = computed(() => filter[type.value](todos.value))  // 计算属性
  const remainingCount = computed(() => filter.active(todos.value).length)
  const count = computed(() => todos.value.length)
  const onHashChange = () => {
    const hash = window.location.hash.replace('#/', '')
    if (filter[hash]) {
      type.value = hash
    } else {
      type.value = 'all'
      window.location.hash = ''
    }
  }


  onMounted(() => {
    window.addEventListener('hashchange', onHashChange)
    onHashChange()
  })

  onUnmounted(() => {
    window.removeEventListener('hashchange', onHashChange)
  })

  return {
    allDone,
    filteredTodos,
    remainingCount,
    count,
    type
  }
}

export default {
  name: 'App',
  setup() {
    const todos = ref([])
    const { remove, removeCompleted } = useRemove(todos)

    return {
      todos,
      remove,
      removeCompleted,
      ...useAdd(todos),
      ...useEdit(remove),
      ...useFilter(todos)
    }
  },
  directives: {
    editingFocus: (el, binding) => {
      binding.value && el.focus()
    }
  }

}
</script>

<style>
</style>

```

## 17.todolist-存储待办事项

接下来我们来实现todo list案例的最后一个功能，把待办事项存储到`localStorage`中，防止刷新的时候丢失数据，当数据修改的时候要把数据存储到`localStorage`，下次加载的时候再从本地存储中把数据还原。

接下来要操作本地存储，可以把操作本地存储的代码分装到一个模块中，这是一个通用的模块，将来在其他组件中也可以使用。

`utils/useLocalStorage.js`

```js
function parse(str) {
  let value
  try {
    value = JSON.parse(str)
  } catch (e) {
    value = null
  }

  return value
}

function strginify(obj) {
  let value
  try {
    value = JSON.stringify(obj)
  } catch (e) {
    value = null
  }
  return value
}

export default function useLocalStorage() {
  function setItem(key, value) {
    value = strginify(value)
    window.localStorage.setItem(key, value)
  }

  function getItem(key) {
    let value = window.localStorage.getItem(key)
    if (value) {
      value = parse(value)
    }
    return value
  }

  return {
    setItem,
    getItem
  }

}
```

准备工作都做好了，下面来想一下这个功能如何实现。当`todos`中数据变化的时候，需要把变化后的数据存储到本地存储中，要调用`setItem`，当添加数据或者删除数据或者编辑数据的时候，都会引起todos的变化，所以要去修改`useAdd`、`useRemove`、`useEdit`，这样太麻烦了，有没有简单一点的办法呢？

这个时候可以想到`watchEffect`，它可以监视数据的变化，如果数据改变了，可以执行相应的操作。还有当页面首次加载的时候，要首先从本地存储中获取数据，如果没有数据的话，可以初始化成一个空数组。所有的这些操作可以再封装到一个函数中。

通过`composition API`实现这个案例，把不同的逻辑代码拆分到不同的`use`函数中，同一功能的代码只存在一个函数中，而且更方便组件之间重用代码，这是`composition API`比`options API`好的地方。


```html
<template>
  <section id="app" class="todoapp">
    <header class="header">
      <h1>todos</h1>
      <input
          class="new-todo"
          placeholder="What needs to be done?"
          autocomplete="off"
          autofocus
          v-model="input"
          @keyup.enter="addTodo"
      >
    </header>
    <section class="main" v-show="count">
      <input id="toggle-all" class="toggle-all" type="checkbox" v-model="allDone">
      <label for="toggle-all">Mark all as complete</label>
      <ul class="todo-list">
        <li
            v-for="todo in filteredTodos"
            :key="todo"
            :class="{ editing: todo === editingTodo, completed: todo.completed }"
        >
          <div class="view">
            <input class="toggle" type="checkbox" v-model="todo.completed">
            <label @dblclick="editTodo(todo)">{{ todo.text }}</label>
            <button class="destroy" @click="remove(todo)"></button>
          </div>
          <input
              type="text"
              class="edit"
              v-editing-focus="todo === editingTodo"
              v-model="todo.text"
              @keyup.enter="doneEdit(todo)"
              @blur="doneEdit(todo)"
              @keyup.esc="cancelEdit(todo)"
          >
        </li>
      </ul>
    </section>
    <footer class="footer" v-show="count">
      <span class="todo-count">
        <strong>{{ remainingCount }}</strong> {{ remainingCount > 1 ? "items" : "item" }} left
      </span>
      <ul class="filters">
        <li><a href="#/all" :class="{active : type === 'all'}">All</a></li>
        <li><a href="#/active" :class="{active : type === 'active'}">Active</a></li>
        <li><a href="#/completed" :class="{active : type === 'completed'}">Completed</a></li>
      </ul>
      <button class="clear-completed" @click="removeCompleted" v-show="count > remainingCount">
        Clear completed
      </button>
    </footer>
  </section>
  <footer class="info">
    <p>Double-click to edit a todo</p>
    <!-- Remove the below line ↓ -->
    <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
    <!-- Change this out with your name and url ↓ -->
    <p>Created by <a href="https://www.lagou.com">教瘦</a></p>
    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
  </footer>
</template>

<script>
import './assets/index.css'
import { computed, onMounted, onUnmounted, ref, watchEffect } from 'vue'
import useLocalStorage from "./utils/useLocalStorage";

const storage = useLocalStorage()

// 1.添加待办事项
const useAdd = todos => {
  const input = ref('')
  const addTodo = () => {
    const text = input.value && input.value.trim()
    if (text.length === 0) return
    todos.value.unshift({
      text,
      completed: false
    })
    input.value = ''
  }
  return {
    input,
    addTodo
  }
}

// 2.删除待办事项
const useRemove = todos => {
  const remove = todo => {
    const index = todos.value.indexOf(todo)  // 找到todo在todos中的索引
    todos.value.splice(index, 1)


  }
  // 删除已完成的待办事项
  const removeCompleted = () => {
    todos.value = todos.value.filter(todo => !todo.completed)
  }
  return {
    remove,
    removeCompleted
  }
}

// 3.编辑待办项
const useEdit = (remove) => {
  let beforeEditingText = ''  // 保存编辑前的文本框的值
  const editingTodo = ref(null)  // 记录当前是否是编辑状态

  // 编辑todo
  const editTodo = (todo) => {
    beforeEditingText = todo.text
    editingTodo.value = todo
  }

  // 完成编辑todo
  const doneEdit = (todo) => {
    if (!editingTodo.value) return
    todo.text = todo.text.trim()
    todo.text || remove(todo)
    editingTodo.value = null
  }

  // 取消编辑todo
  const cancelEdit = todo => {
    editingTodo.value = null
    todo.text = beforeEditingText
  }

  return {
    editingTodo,
    editTodo,
    doneEdit,
    cancelEdit
  }

}

// 4.切换待办项完成状态
const useFilter = (todos) => {
  const allDone = computed({
    get() {
      return !todos.value.filter(todo => !todo.completed).length
    },
    set(value) {
      todos.value.forEach(todo => {
        todo.completed = value
      })
    }
  })

  const filter = {
    all: list => list,
    active: list => list.filter(todo => !todo.completed),
    completed: list => list.filter(todo => todo.completed),
  }

  const type = ref('all')  // 保存type
  const filteredTodos = computed(() => filter[type.value](todos.value))  // 计算属性
  const remainingCount = computed(() => filter.active(todos.value).length)
  const count = computed(() => todos.value.length)
  const onHashChange = () => {
    const hash = window.location.hash.replace('#/', '')
    if (filter[hash]) {
      type.value = hash
    } else {
      type.value = 'all'
      window.location.hash = ''
    }
  }


  onMounted(() => {
    window.addEventListener('hashchange', onHashChange)
    onHashChange()
  })

  onUnmounted(() => {
    window.removeEventListener('hashchange', onHashChange)
  })

  return {
    allDone,
    filteredTodos,
    remainingCount,
    count,
    type
  }
}

// 5.存储待办事项
const useStorage = () => {
  const KEY = 'TODOKEYS'
  const todos = ref(storage.getItem(KEY) || [])
  watchEffect(() => {
    storage.setItem(KEY, todos.value)
  })
  return todos
}

export default {
  name: 'App',
  setup() {
    const todos = useStorage()
    const { remove, removeCompleted } = useRemove(todos)

    return {
      todos,
      remove,
      removeCompleted,
      ...useAdd(todos),
      ...useEdit(remove),
      ...useFilter(todos)
    }
  },
  directives: {
    editingFocus: (el, binding) => {
      binding.value && el.focus()
    }
  }

}

</script>

<style>
</style>

```

![](http://5coder.cn/img/1669552311_067e582d9befd91d60da975dcbb59d47.png)
