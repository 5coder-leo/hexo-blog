---
title: Vue3.0响应式系统原理
author: 5coder
tags: Vue3.0响应式系统原理
category: 大前端
abbrlink: 28180
date: 2022-11-27 20:48:01
password:
keywords:
top:
cover:
---

# Vue3.0响应式系统原理

## 1.响应式系统原理-介绍

接下来通过模拟Vue3的响应式系统来深入了解它内部的工作原理。先来回顾一下Vue3重写了响应式系统，和Vue2相比，Vue3的响应式系统底层采用`proxy`对象实现，在初始化的时候不需要遍历所有的属性，把属性通过`defineProperty`转换成`getter`和`setter`。另外如果有多层属性嵌套的话，只有访问某个属性的时候才会递归处理下一级的属性，所以Vue3中响应式系统的性能要比Vue2好。

Vue3的响应式系统默认可以监听动态添加的属性，还可以监听属性的删除操作以及数组的索引和`length`属性的修改操作。另外Vue3的响应式系统还可以作为一个模块单独使用。

- Proxy 对象实现属性监听
- 多层属性嵌套，在访问属性过程中处理下━级属性默认监听动态添加的属性
- 默认监听属性的删除操作
- 默认监听数组索引和length 属性
- 可以作为单独的模块使用

接下来自己实现Vue3中显样式系统的核心函数，分别去实现之前使用过的`reactive`/`ref`/`toRefs`/`computed`的函数。`watch`和`watchEffect`是Vue3的`runtime.core`中实现的。
`watch`函数的内部其实使用了一个叫做`effect`的底层函数，我们会模拟实现`effect`函数以及Vue3中收集依赖和触发更新的函数`track`和`trigger`。

- `reactive`/`ref`/`toRefs`/`computed`
- `effect`
- `track`
- `trigger`

## 2.响应式系统原理-Proxy对象回顾

在模拟实现Vue3的响应式原理之前，先来回顾一下`Proxy`对象。重点来看两个小问题：

- `set` 和 `deleteProperty` 中需要返回布尔类型的值，在严格模式下，如果返回 false 的话会出现 `Type Error` 的异常
- `Proxy` 和 `Reflect` 中使用的 `receiver`

[Refelct MDN文档](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Reflect)

`proxy.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <script>
    'use strict'
    // 问题1： set 和 deleteProperty 中需要返回布尔类型的值
    //        在严格模式下，如果返回 false 的话会出现 Type Error 的异常
    const target = {
      foo: 'xxx',
      bar: 'yyy'
    }
    // Reflect.getPrototypeOf()
    // Object.getPrototypeOf()
    const proxy = new Proxy(target, {
      get (target, key, receiver) {
        // return target[key]
        return Reflect.get(target, key, receiver)
      },
      set (target, key, value, receiver) {
        // target[key] = value
        return Reflect.set(target, key, value, receiver)
      },
      deleteProperty (target, key) {
        // delete target[key]
        return Reflect.deleteProperty(target, key)
      }
    })

    proxy.foo = 'zzz'
    // delete proxy.foo
    console.log(proxy.foo)
  </script>
</body>
</html>
```

先来看一下`proxy`对象的使用，这里先定义了一个对象`target`，然后通过`proxy`代理`target`对象。在创建`proxy`对象的时候，传入了第二个参数，它是一个对象，可以叫做处理器或者监听器。那这里的`get`、 `set` 、`deleteProperty`可以分别监听对属性的**访问**、**赋值**以及**删除**操作。`get`和`set`这两个方法，它最后有个参数叫做`receiver`，在这里代表的是当前的`proxy`对象或者继承自`proxy`的对象。

在获取或设置值的时候使用的`Reflect`，分别调用了`Reflect.get`和`Reflect.set`这两个方法。Reflect是反射的意思，是ES6中新增的成员。Java和C#上里也有反射，是在代码运行期间用来获取或设置对象中的成员。这里是借鉴Java或C#下中的反射，因为Javascript的特殊性，代码在运行期间可以随意的去给对象增加成员或者获取对象中成员的信息，所以在ES6之前，Javascript中并没有反射。

过去Javascript很随意的把一些方法挂载到`Object`中，比如`Object.getPrototypeOf()`这个方法，`Reflect`中也有对应的方法`Reflect.getPrototypeOf()`，方法的作用是一样的，只是表达语义的问题。如果在`Reflect`中有对应的`Object`中的方法，那建议使用`Reflect`中的方法，所以上面都是使用`Reflect`来操作对象中的成员。Vue3的源码中也使用的是`Reflect`。

首先来说第一个问题，`set`和`deleteProperty`这两个方法中都需要返回一个布尔类型，在严格模式下如果返回`false`会报`type`的错误。

![](http://5coder.cn/img/1669556601_6725dff84cfcc03187f33545790414c8.png)

`set`方法中，如果我们给只读属性赋值，那这个时候会设置失败，返回`false`。当前代码中的`set`和`deleteProperty`都没有写`return`，默认返回的是`undefined`，转换成布尔类型的话是`false`。所以在最后去给属性赋值或者删除属性的时候都会报类型错误。注意有一个前提是在**严格模式**下，非严格模式下是不会报错的。

找到代理对象中的`set`方法，在`set`方法中可以直接返回`return Reflect.set(target, key, value, receiver)`，这个方法设置成功之后会返回`true`，设置失败之后会返回`false`，那下面`deleteProperty`也是一样的，`return Reflect.deleteProperty(target, key)`，然后再来打开浏览器。刷新一下浏览器，这时候设置成功之后不会报错。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <script>
    'use strict'
    // 问题2：Proxy 和 Reflect 中使用的 receiver

    // Proxy 中 receiver：Proxy 或者继承 Proxy 的对象
    // Reflect 中 receiver：如果 target 对象中设置了 getter，getter 中的 this 指向 receiver

    const obj = {
      get foo() {
        console.log(this)
        return this.bar
      }
    }

    const proxy = new Proxy(obj, {
      get (target, key, receiver) {
        if (key === 'bar') {
          return 'value - bar'
        }
        return Reflect.get(target, key, receiver)
      }
    })
    console.log(proxy.foo)
  </script>
</body>
</html>
```

第二个问题和`receiver`相关，来看一下`receiver`，在`proxy`的`handler`对象的`get`和`set`中会接收一个`receiver`，它是当前创建的`proxy`对象或者继承自当前`proxy`的子对象。`Reflect`中调用`set`和`get`的时候也传入了一个`receiver`对象。

解释一下`receiver`对象，如果`target`对象中设置了`getter`，那么`getter`中的`this`指向的就是这个`receiver`。那么通过代码来解释一下，我们这里有一个对象，它有一个`foo`的属性，只有`get`。在`get`中打印了`this`，并且返回了`this.bar`半，当前对象中并没有定义`bar`属性。

再来看这个代理对象，这里监听了`get`，也就是下边在访问`proxy.foo`的时候，首先会去执行`obj`这个对象中的`foo`，它对应`get`，然后打印`this`，再来访问`this.bar`，当`Reflect.get`没有设置`receiver`的时候，此处的`this`就是obj对象。

![](http://5coder.cn/img/1669557185_cc85cf18d9a045d61ff07eca0deea037.png)

```js
const obj = {
  get foo() {
    console.log(this)
    return this.bar
  }
}

const proxy = new Proxy(obj, {
  get (target, key, receiver) {
    if (key === 'bar') {
      return 'value - bar'
    }
    return Reflect.get(target, key)
  }
})
console.log(proxy.foo)
```

来给`Reflect.get`添加`receiver`。此处的`receiver`是`proxy`对象中的`get`方法中的`receiver`，它是当前的`proxy`对象。访问`target`对象中的`get`的时候，会让这里的`this`指向`receiver`对象，也就是代理对象。那此处的`this`就是代理对象，当访问`this.bar`的时候，会执行代理对象的`get`方法。

![](http://5coder.cn/img/1669557337_289eeeab27be40c2ff5acb83a5633a60.png)

## 3.响应式系统原理-reactive

reactive

- 接受一个参数，判断这个参数是否是对象
- 创建拦截器对象`handler`，设置`get`/`set`/`deleteProperty`
- 返回`Proxy`

接下来我们来实现响应式原理中的第一个函数。目录结构如下：![](http://5coder.cn/img/1669560269_b3abe9153f8d05b69c89ae3999b5170f.png)



在`index.js`中编写，`reactive`函数接收一个参数`target`，它里面首先要判断`target`参数是否是对象，如果不是的话，直接返回，因为`reactive`只能把**对象**转换成响应式对象，这是和`ref`不同的地方。

然后来创建proxy中的拦截器对象，也就是`handle`的对象，它里面包含`get`、`set`和`deleteProperty`这些拦截的方法，最后创建并返回proxy对象，要传入拦截器对象。

在`index.js`中，首先来创建`reactive`这个函数的形式，模块中导出一个`reactive`函数，它接受一个`target`的参数，首先要判断这个`target`是否是对象，如果不是对象的话直接返回，否则的话把`target`转换成代理对象。

```js
export function reactive(target) {
    return new Proxy(target, handler)
}
```

要判断一个变量是否是对象，这件事情其他地方还要使用，所以在模块的最上面先来定一个辅助的函数`isObject`，用来判断一个变量是否是对象。

```js
const isObject = val => val !== null && typeof val === 'object'

export function reactive(target) {
    return new Proxy(target, handler)
}
```

接下来再来定义一个`handle`的对象，这是`proxy`构造函数的第二个参数，叫做**处理器**或者**拦截器对象**。`handle`的对象中包含`get`、`set`和`deleteProperty`。先把这个对象的**形式**写出来，一会再分别去实现它里边的方法。

```js
const isObject = val => val !== null && typeof val === 'object'

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
    },
    set(target, key, value, receiver) {
    },
    deleteProperty(target, key) {
    }
  }
  return new Proxy(target, handler)
}
```

下面分别来实现`handler`中的这三个方法。先来实现`get`方法，在`get`方法里首先要去收集依赖，至于如何收集依赖，**下一小节再来实现**。返回`target`中`key`的值，这里直接通过`Reflect.get`来获取。直接`return Reflect.get(target, key, receiver)`，这里还有一个问题，如果当前这个`key`属性对应的值也是对象，那么还需要把它再转换成响应式对象，这是之前说过的，如果对象中有嵌套属性的话，会在`get`中递归收集下一级属性的依赖。

这里先接受`Reflect`的返回值`const result = Reflect.get(target, key, receiver)`，接下来需要先去判断一下`result`是否是对象，如果是对象需要再调用`reactive`来处理，这件事情待会`ref`函数内部也要使用，所以再来封装一个辅助的函数`covert`。

```js
// 判断是否为对象
const isObject = val => val !== null && typeof val === 'object'
// 判断target是否为对象，如果是对象，则继续调用reactive函数将其转为响应式对象，如果不是对象，直接返回target
const convert = target => isObject(target) ? reactive(target) : target

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
      console.log('get', key)
      const result = Reflect.get(target, key, receiver)
      return convert(result)
    },
    set(target, key, value, receiver) {
      
    },
    deleteProperty(target, key) {
      
    }
  }
  return new Proxy(target, handler)
}
```

下面再来写`set`方法，在`set`方法里边，首先要去获取。`key`属性的值，需要定一个变量`oldValue`来获取，调用`Reflect.get`来获取它的值。获取这个`oldValue`的目的是等会要去判断一下当前传入的`newValue`跟`oldValue`是否相等，如果相等的话，不需要做任何的处理，如果它们的值不同的话，这个时候要调用`Reflect.set`方法重新去修改这个属性的值，并且还要去触发更新。但是之前说过，`set`方法中需要返回一个布尔类型的值，标示赋值是否成功。

```js
// 判断是否为对象
const isObject = val => val !== null && typeof val === 'object'
// 判断target是否为对象，如果是对象，则继续调用reactive函数将其转为响应式对象，如果不是对象，直接返回target
const convert = target => isObject(target) ? reactive(target) : target
const hasOwnProperty = Object.prototype.hasOwnProperty
const hasOwn = (target, key) => hasOwnProperty.call(target, key)

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
      console.log('get', key)
      const result = Reflect.get(target, key, receiver)
      return convert(result)
    },
    set(target, key, value, receiver) {
      // 获取
      const oldValue = Reflect.get(target, key, receiver)
      let result = true  // set方法需要返回布尔值类型的数据，这里默认为true
      if (oldValue !== value) {
        result = Reflect.set(target, key, value, receiver)  // 复制成功会返回true，失败会返回false
        // 触发更新
        console.log('set', key, value)
      }
      return result
    },
    deleteProperty(target, key) {
      
    }
  }
  return new Proxy(target, handler)
}
```

最后再来写`deleteProperty`这个方法，在`deleteProperty`中，首先要判断当前`target`中是否有需要删除的`key`属性，如果`target`中有`key`属性，并且把`key`成功删除之后，再来触发更新。

最后要返回删除是否成功，现在模块的最上面再来写一个辅助的函数`hasOwn`，以及抽离出`hasOwnProperty`，它的作用是用来判断某个对象本身是否具有指定的属性。

这里首先要调用`hasOwn`来判断一下，并且来接收一下它的返回结果。然后再来调用`Reflect.deleteProperty(target, key)`来删除`target`中的`key`属性，并且它会返回一个布尔类型。如果当前`target`中有`key`属性，并且删除成功，这个时候要去触发更新。

```js
// 判断是否为对象
const isObject = val => val !== null && typeof val === 'object'
// 判断target是否为对象，如果是对象，则继续调用reactive函数将其转为响应式对象，如果不是对象，直接返回target
const convert = target => isObject(target) ? reactive(target) : target
const hasOwnProperty = Object.prototype.hasOwnProperty
const hasOwn = (target, key) => hasOwnProperty.call(target, key)

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
      console.log('get', key)
      const result = Reflect.get(target, key, receiver)
      return convert(result)
    },
    set(target, key, value, receiver) {
      // 获取
      const oldValue = Reflect.get(target, key, receiver)
      let result = true
      if (oldValue !== value) {
        result = Reflect.set(target, key, value, receiver)
        // 触发更新
        console.log('set', key, value)
      }
      return result
    },
    deleteProperty(target, key) {
      const hadKey = hasOwn(target, key)
      const result = Reflect.deleteProperty(target, key)
      if (hadKey && result) {
        // 触发更新
        console.log('delete', key)
      }
      return result
    }
  }
  return new Proxy(target, handler)
}
```

下面在网页中来测试.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>
<script type="module">
  import {reactive} from './my-reactivity/index.js'
  const obj = reactive({
    name: 'zs',
    age: 18
  })

  obj.name = 'lisi'
  obj.age = 20
  delete obj.name
  console.log(obj)
</script>
</body>
</html>
```

![](http://5coder.cn/img/1669564092_7fccedf4cd529a79c391abba99d58a22.png)

可以看到分别触发了`get`、`set`、`deleteProperty`，这里`reactive`方法就模拟完了。

## 4.响应式系统原理-收集依赖

接下来来实现响应式系统中收集依赖的过程。先来演示一下Vue3中的`reactivity`模块，也就是响应式系统的模块，通过演示响应式系统模块的使用来总结实现依赖收集的思路。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
<script type="module">
  import { reactive, effect } from './node_modules/vue/dist/vue.esm-browser.js'

  const product = reactive({
    name: 'iPhone',
    price: 5000,
    count: 3
  })

  let total = 0
  effect(() => {
    total = product.price * product.count
  })

  console.log(total)

  product.price = 4000
  console.log(total)

  product.count = 1
  console.log(total)

</script>
</body>
</html>
```

这里已经安装好了`reactivity`模块，并且实现了一个简单的案例，来看一下代码。首先导入了`reactivity`模块中的`reactive`和`effect`这两个函数，`reactive`的作用是用来创建显式数据的，下面来看`effect`函数的作用。

首先，创建了一个响应式的对象`product`，它是用来描述商品的，商品的名称是iPhone，商品的单价是5000，库存是三个。
接下来又定义了一个变量`total`，这是`product`总价。定了`effect`这个函数，它接受一个函数作为参数。`effect`的用法和`watchEffect`的用法一样，`watchEffect`内部就是调用`effect`来实现的。

`effect`中的函数首先会执行一次，当这个函数中引用响应式数据的时候，比如这里使用了`product.price`还有`product.count`，如果响应式数据发生变化，它会再次执行。当利用`effect`之后，会计算出商品的总价格，打印`total`，那此时的总价格应该是15000，接下来改变了商品的单价，`product.price = 4000`。当响应式数据变化之后，`effect`中的函数会再次执行，最后又把count的值改成了1。当显式数据变化之后，`effect`中的函数会再次执行。

![](http://5coder.cn/img/1669596834_8c47333dc37db2020f82ab38ece52592.png)

在首次加载的时候，首先会执行`effect`中的函数，在`effect`函数内部首先会调用**参数箭头函数**，在这个箭头函数中又访问了`product`，`product`是`reactive`返回的响应式对象，也就是代理对象。当我们访问`product.price`的时候，会执行`price`属性的`get`方法，在`get`方法中要**收集依赖**，**收集依赖的过程其实就是存储这个属性和回调函数**，而属性又跟对象相关，所以在代理对象的`get`方法中，首先会存储`target`目标对象，然后是`target`对象的属性，这里是`price`。然后再把对应的箭头函数存储起来，这里是有对应关系的，目标对象、对应的属性、对应的这个箭头函数。在触发更新的时候，再根据对象的属性找到这个函数。

`price`的依赖收集完毕之后会继续访问`product.count`，它会执行`count`属性对应的`get`方法，在`get`方法中需要存储目标对象以及对应的`count`属性及当前这个箭头函数。

接下来给`product price`重新赋值的时候，会执行`price`属性对应的`set`方法。在`set`方法中需要触发更新，那触发更新其实就是找到依赖收集过程中存储的对象的`price`属性对应的`effect`函数，找到这个函数之后会立即执行。

这是依赖收集和触发更新的一个简单的过程，通过一张图解释一下。

![](http://5coder.cn/img/1669596104_a0ab90f21d6aa5a39ca580b8ee6ba43f.png)

在依赖收集的过程中，会创建三个集合，分别是`targetMap`还有`depsMap`还有`dep`。其中`targetMap`的作用是用来**记录目标对象和一个字典**，也就是中间的这个`depsMap`。`targetMap`使用的类型是`weakMap`弱引用的map，这里的`key`其实就是`target`对象，因为是弱引用，当目标对象失去引用之后，可以销毁。`targetMap`的值是`depsMap`，`depsMap`是一个字典，类型是`map`，字典中的`key`是**目标对象中的属性名称**，值是一个`set`集合，`set`集合中存储的元素不会重复，它里面存储的是`effect`函数，因为可以多次调用`effect`，在`effect`中访问同一个属性，这时候该属性会收集多次依赖对应多个`effect`函数。

所以通过这种结构，可以存储目标对象，目标对象的属性以及属性对应的effect函数，一个属性可能对应多个函数，那将来触发更新的时候，可以在这个结构中根据目标对象的属性找到`effect`函数，然后执行。

一会要实现的收集依赖的`track`函数，它内部首先要根据当前的`targetMap`这个对象来找到`depsMap`，如果没有找到的话，要给当前对象创建一个`depsMap`并添加到`targetMap`中。如果找到了，再去根据当前使用的属性来`depsMap`中找到对应的`dep`，`dep`里存储的是`effect`函数，如果没有找到的话，为当前属性创建对应的`dep`，并且存储到`depsMap`中。
如果找到当前属性对应的`dep`集合，那就把当前的`effect`函数存储到`dep`集合中，这就是整个收集依赖的思路。

## 5.响应式系统原理-effect-track

下面来实现收集依赖的功能，分别来实现`effect`和`track`两个函数。

`effect`函数接收一个函数作为参数`callback`，在`effect`函数中首先要执行1次`callback`，在`callback`中会访问现实对象的属性，在这个过程中去收集依赖，在收集依赖的过程中，要把callback存储起来。所以要想办法让之后的`track`函数能够访问到这里的`callback`，在这个函数的上面先来定一个变量`activeEffect`来记录`callback`。然后在函数中先把`callback`存储到`activeEffect`中。当依赖收集完毕之后，还需要将`activeEffect`设置为`null`，因为收集依赖的时候如果有嵌套属性的话，是一个递归的过程。

```js
let activeEffect = null

export function effect(callback) {
  //  effect中首先要执行一次callback，访问响应时对象属性，去收集依赖
  activeEffect = callback
  callback()
  activeEffect = null
}
```

下面实现`track`函数，`track`函数接收两个参数，一个是目标对象`target`，还有一个是要跟踪的属性`key`。`track`内部要把`target`存储到一个`targetMap`中。`track`是收集依赖，`trigger`是触发更新。`trigger`函数要去`targetMap`中找到属性对应的`effect`函数，然后来执行。

在`track`内部首先要判断`activeEffect`的值为`null`的话，直接返回，说明当前没有要收集的依赖，否则要去`targetMap`中，根据当前的`target`来找`depsMap`，因为我们当前的`target`就是`targetMap`中的键。还要判断一下是否找到了`depsMap`，因为`target`它可能没有收集的依赖。如果没有找到的话，要为当前的`target`创建一个对应的`depsMap`去存储键和对应的`dep`对象->也就是要执行的`effect`函数，然后再把它添加到`targetMap`中。

接下来根据属性查找对应的`dep`对象，`let dep = depsMap.get(key)`，然后再来判断一下`dep`是否存在，`dep`法是一个集合，这个集合用来去存储属性对应的那些`effect`函数，如果没有找到的话，跟之前一样，也要创建一个新的`dep`集合，并且把它添加到`depsMap`中。

接下来就可以把`effect`函数添加到`dep`集合中，`dep.add(activeEffect)`。还要在代理对象的`get`中来调用一下这个函数。

```js
// 判断是否为对象
const isObject = val => val !== null && typeof val === 'object'
// 判断target是否为对象，如果是对象，则继续调用reactive函数将其转为响应式对象，如果不是对象，直接返回target
const convert = target => isObject(target) ? reactive(target) : target
const hasOwnProperty = Object.prototype.hasOwnProperty
const hasOwn = (target, key) => hasOwnProperty.call(target, key)

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
      console.log('get', key)
      track(target, key)
      const result = Reflect.get(target, key, receiver)
      return convert(result)
    },
    set(target, key, value, receiver) {
      // 获取
      const oldValue = Reflect.get(target, key, receiver)
      let result = true
      if (oldValue !== value) {
        result = Reflect.set(target, key, value, receiver)
        // 触发更新
        console.log('set', key, value)
      }
      return result
    },
    deleteProperty(target, key) {
      const hadKey = hasOwn(target, key)
      const result = Reflect.deleteProperty(target, key)
      if (hadKey && result) {
        // 触发更新
        console.log('delete', key)
      }
      return result
    }
  }

  return new Proxy(target, handler)

}


let activeEffect = null

export function effect(callback) {
  //  effect中首先要执行一次callback，访问响应时对象属性，去收集依赖
  activeEffect = callback
  callback()
  activeEffect = null
}

let targetMap = new WeakMap()

export function track(target, key) {
  if (!activeEffect) return
  let depsMap = targetMap.get(target)
  if (!depsMap) {
    targetMap.set(target, (depsMap = new Map()))
  }
  let dep = depsMap.get(key)
  if (!dep) {
    depsMap.set(key, (dep = new Set()))
  }
  dep.add(activeEffect)
}
```

好，那到这里整个依赖收集的过程就完成了，这个过程可以通过之前看到那张图来回顾。

## 6.响应式系统原理-trigger

```js
// 判断是否为对象
const isObject = val => val !== null && typeof val === 'object'
// 判断target是否为对象，如果是对象，则继续调用reactive函数将其转为响应式对象，如果不是对象，直接返回target
const convert = target => isObject(target) ? reactive(target) : target
const hasOwnProperty = Object.prototype.hasOwnProperty
const hasOwn = (target, key) => hasOwnProperty.call(target, key)

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
      track(target, key)
      const result = Reflect.get(target, key, receiver)
      return convert(result)
    },
    set(target, key, value, receiver) {
      // 获取
      const oldValue = Reflect.get(target, key, receiver)
      let result = true
      if (oldValue !== value) {
        result = Reflect.set(target, key, value, receiver)
        // 触发更新
        trigger(target, key)
      }
      return result
    },
    deleteProperty(target, key) {
      const hadKey = hasOwn(target, key)
      const result = Reflect.deleteProperty(target, key)
      if (hadKey && result) {
        // 触发更新
        trigger(target, key)
      }
      return result
    }
  }

  return new Proxy(target, handler)

}


let activeEffect = null

export function effect(callback) {
  //  effect中首先要执行一次callback，访问响应时对象属性，去收集依赖
  activeEffect = callback
  callback()
  activeEffect = null
}

let targetMap = new WeakMap()

export function track(target, key) {
  if (!activeEffect) return
  let depsMap = targetMap.get(target)
  if (!depsMap) {
    targetMap.set(target, (depsMap = new Map()))
  }
  let dep = depsMap.get(key)
  if (!dep) {
    depsMap.set(key, (dep = new Set()))
  }
  dep.add(activeEffect)
}


// 触发更新
export function trigger(target, key) {
  // 根据target，在targetMap中找打key
  const depsMap = targetMap.get(target)
  if (!depsMap) return
  const dep = depsMap.get(key)
  if (dep) {
    dep.forEach(effect => {
      effect()
    })
  }
}
```

依赖收集完毕之后，再来实现触发更新，对应要实现的函数是`trigger`，这个过程跟`track`的过程正好相反。

`trigger`函数也有两个参数，分别是`target`和`key`，要根据`target`去`targetMap`中来找到`depsMap`。判断是否找到了`depsMap`，如果没有找到直接`return`。

如果找到了`depsMap`，再根据`key`来找对应的`dep`集合，`dep`集合里边存储的是这个`key`所对应的`effect`t函数。再来判断一下`dep`集合是否有值，如果`dep`有值的话，需要去遍历`dep`集合，然后执行里面的每一个`effect`函数。

到这里trigger函数就写完了。下面要找到`reactive`函数，要找到代理对象的`set`方法和`deleteProperty`方法，然后在这两个方法中来调用`trigger`触发更新。随后进行测试。

![](http://5coder.cn/img/1669603346_f1002ea3c08a485e9e36918cdf494e45.png)

![](http://5coder.cn/img/1669603355_31121f7d02f4de4124a7941c25d565ce.png)

可以看到正常执行`get`、`set`、`deleteProperty`。

## 7.响应式系统原理-ref

之前已经实现了`reactive`函数，它可以创建响应式的对象，下面再来实现一个创建响应式对象的函数`ref`，这个函数之前使用过了，它接收一个参数，可以是原始值，也可以是对象，如果传入的是对象，并且这个对象是`ref`创建的对象，那直接返回。如果是普通对象的话，它内部会调用`reactive`来创建响应式对象，否则的话创建一个只有`value`属性的响应式对象，然后把它返回。

在`ref`函数里边，首先要判断`raw`是否是使用`ref`创建的对象，`ref`创建的对象有什么特点呢？我们还不知道，所以我们一会儿来写，我们先来写上注释，要判断要是否是`ref`创建的对象，如果是的话，直接返回。

接下来来判断`raw`是否是对象，如果是对象，就要`reactive`创建响应式式对象，否则的话返回原始值。这件事情直接写过一个函数`convert`，这里直接调用就可以了，还要把这个调用的结果存储到一个变量`value`中。

接下来不管`value`当前是什么值，都要去创建一个`ref`的对象，这个对象是一个只有`value`属性的对象，并且这个`value`属性具有`get`、`set`标识，标识是否是`ref`创建的对象。

下面来实现这个对象，这个对象里边首先要创建一个标识的属性`__v_isRef`，它的值是`true`。接下来再来创建`value`的属性，value属性只有对应的`get`和`set`。

如果给`value`重新赋制成一个对象，它依然是响应式的，因为当`raw`是对象的时候，convert里边会利用`reactive`把它转换成响应式对象，这是跟`reactive`的一个区别。接下来开始测试。

```js
// 判断是否为对象
const isObject = val => val !== null && typeof val === 'object'
// 判断target是否为对象，如果是对象，则继续调用reactive函数将其转为响应式对象，如果不是对象，直接返回target
const convert = target => isObject(target) ? reactive(target) : target
const hasOwnProperty = Object.prototype.hasOwnProperty
const hasOwn = (target, key) => hasOwnProperty.call(target, key)

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
      track(target, key)
      const result = Reflect.get(target, key, receiver)
      return convert(result)
    },
    set(target, key, value, receiver) {
      // 获取
      const oldValue = Reflect.get(target, key, receiver)
      let result = true
      if (oldValue !== value) {
        result = Reflect.set(target, key, value, receiver)
        // 触发更新
        trigger(target, key)
      }
      return result
    },
    deleteProperty(target, key) {
      const hadKey = hasOwn(target, key)
      const result = Reflect.deleteProperty(target, key)
      if (hadKey && result) {
        // 触发更新
        trigger(target, key)
      }
      return result
    }
  }

  return new Proxy(target, handler)

}


let activeEffect = null

export function effect(callback) {
  //  effect中首先要执行一次callback，访问响应时对象属性，去收集依赖
  activeEffect = callback
  callback()
  activeEffect = null
}

let targetMap = new WeakMap()

export function track(target, key) {
  if (!activeEffect) return
  let depsMap = targetMap.get(target)
  if (!depsMap) {
    targetMap.set(target, (depsMap = new Map()))
  }
  let dep = depsMap.get(key)
  if (!dep) {
    depsMap.set(key, (dep = new Set()))
  }
  dep.add(activeEffect)
}

// 触发更新
export function trigger(target, key) {
  // 根据target，在targetMap中找打key
  const depsMap = targetMap.get(target)
  if (!depsMap) return
  const dep = depsMap.get(key)
  if (dep) {
    dep.forEach(effect => {
      effect()
    })
  }
}

export function ref(raw) {
  // 判断raw是否是ref创建的对象，如果是，直接返回
  if (isObject(raw) && raw.__v_isRef) return

  let value = convert(raw)
  const r = {
    __v_isRef: true,
    get value() {
      track(r, 'value')
      return value
    },
    set value(newValue) {
      if (newValue !== value) {
        raw = newValue
        value = convert(raw)
        trigger(r, 'value')
      }
    }
  }

  return r
}
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <script type="module">
    import { reactive, effect, ref } from './my-reactivity/index.js'

    const price = ref(5000)
    const count = ref(3)
   
    let total = 0 
    effect(() => {
      total = price.value * count.value
    })
    console.log(total)

    price.value = 4000
    console.log(total)

    count.value = 1
    console.log(total)

  </script>
</body>
</html>
```

![](http://5coder.cn/img/1669606787_fad5269398d66eec2ff175c2e210b5e3.png)

可以看到正常运行。

最后再来总结一下`ref`和`reactive`这两个函数的区别。

`ref`可以把基本类型的数据转换成响应式对象，当获取数据时要使用`value`属性，模板中使用的时候可以省略。`reactive`不能把基本数据类型的数据转换成响应式对象。`ref`返回的对象重新给`value`属性赋值成对象以后也是响应式的，那刚刚我们代码里边是通过convert来处理的，我们在todo list案例删除已完成代办项的时候使用过。

`reactive`创建的响应式对象重新赋值以后会丢失响应式，因为重新赋值的对象不再是`dep`对象。`reactive`返回的对象中的属性不可以解构，如果想要解构的话，需要使用`toRefs`来处理返回的这个对象。

如果一个对象中的成员非常多的时候，使用`ref`并不方便，因为总要带着value属性。如果一个函数内部只有一个响应式数据，这个时候可以使用`ref`会比较方便，因为可以直接解构返回，之前案例里使用的都是ref。

![](http://5coder.cn/img/1669604177_f6a806c268dfd9181ff4225588932505.png)

![](http://5coder.cn/img/1669604228_168a0b11a5a17215dc2a844cbd8132af.png)

## 8.响应式系统原理-toRefs

接下来再来实现`toRefs`函数，首先要知道这个函数的作用，`toRefs`函数接受一个`reactive`返回的响应式对象，也就是一个`proxy`对象。

如果传入的参数不是reactive创建的显项式对象直接返回，然后再把传入对象的所有属性转换成一个类似于`ref`返回的对象，把转换后的属性挂载到一个新的对象上返回。

先来定一个`toRefs`的函数，它接收一个参数`proxy`，在这个函数里边，做的第一件事情是判断这个函数的参数是否是一个`reactive`创建的对象，如果不是的话，发送警告，因为上面实现的`reactive`中创建的对象没有做标识的属性，所以这步跳过。

接下来定义一个`ret`，要给`ret`去赋值，要判断一下传过来这个参数，如果是数组的，那么创建一个长度是`length`数组，否则的话返回一个空对象。`const ret = proxy instanceof Array ? new Array(proxy.length) : {}`

处理完成之后，接下来来遍历`key`这个对象的所有属性，如果是数组的话，遍历它的所有索引，把每一个属性都转换成类似于`ref`返回的对象。在变历的过程中，要把每一个属性都转换成一个`ref`返回的对象。

这个转换的过程再来封装成一个函数`toProxyRef`。在这个函数里边，直接来创建一个对象，最终要返回这个对象。遍历的时候这里边要去调用`toRefs`去把所有属性转换一下，并且把转换好的属性存储到`ret[key]`对象里面来。

```js
// 判断是否为对象
const isObject = val => val !== null && typeof val === 'object'
// 判断target是否为对象，如果是对象，则继续调用reactive函数将其转为响应式对象，如果不是对象，直接返回target
const convert = target => isObject(target) ? reactive(target) : target
const hasOwnProperty = Object.prototype.hasOwnProperty
const hasOwn = (target, key) => hasOwnProperty.call(target, key)

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
      track(target, key)
      const result = Reflect.get(target, key, receiver)
      return convert(result)
    },
    set(target, key, value, receiver) {
      // 获取
      const oldValue = Reflect.get(target, key, receiver)
      let result = true
      if (oldValue !== value) {
        result = Reflect.set(target, key, value, receiver)
        // 触发更新
        trigger(target, key)
      }
      return result
    },
    deleteProperty(target, key) {
      const hadKey = hasOwn(target, key)
      const result = Reflect.deleteProperty(target, key)
      if (hadKey && result) {
        // 触发更新
        trigger(target, key)
      }
      return result
    }
  }

  return new Proxy(target, handler)

}


let activeEffect = null

export function effect(callback) {
  //  effect中首先要执行一次callback，访问响应时对象属性，去收集依赖
  activeEffect = callback
  callback()
  activeEffect = null
}

let targetMap = new WeakMap()

export function track(target, key) {
  if (!activeEffect) return
  let depsMap = targetMap.get(target)
  if (!depsMap) {
    targetMap.set(target, (depsMap = new Map()))
  }
  let dep = depsMap.get(key)
  if (!dep) {
    depsMap.set(key, (dep = new Set()))
  }
  dep.add(activeEffect)
}

// 触发更新
export function trigger(target, key) {
  // 根据target，在targetMap中找打key
  const depsMap = targetMap.get(target)
  if (!depsMap) return
  const dep = depsMap.get(key)
  if (dep) {
    dep.forEach(effect => {
      effect()
    })
  }
}

export function ref(raw) {
  // 判断raw是否是ref创建的对象，如果是，直接返回
  if (isObject(raw) && raw.__v_isRef) return

  let value = convert(raw)
  const r = {
    __v_isRef: true,
    get value() {
      track(r, 'value')
      return value
    },
    set value(newValue) {
      if (newValue !== value) {
        raw = newValue
        value = convert(raw)
        trigger(r, 'value')
      }
    }
  }

  return r
}

export function toRefs(proxy) {
  const ret = proxy instanceof Array ? new Array(proxy.length) : {}
  for (const key in proxy) {
    ret[key] = toProxyRef(proxy, key)
  }
  return ret
}


function toProxyRef(proxy, key) {
  return {
    __v_isRef: true,
    get value() {
      return proxy[key]
    },
    set value(newValue) {
      proxy[key] = newValue
    }
  }
}
```

最后来测试一下。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <script type="module">
    import { reactive, effect, toRefs } from './my-reactivity/index.js'

    function useProduct () {
      const product = reactive({
        name: 'iPhone',
        price: 5000,
        count: 3
      })
      
      return toRefs(product)
    }

    const { price, count } = useProduct()


    let total = 0 
    effect(() => {
      total = price.value * count.value
    })
    console.log(total)

    price.value = 4000
    console.log(total)

    count.value = 1
    console.log(total)

  </script>
</body>
</html>
```

![](http://5coder.cn/img/1669608230_064277dbea6c220469990f17a8eab3a8.png)

可以看到正常返回显示。

## 9.响应式系统原理-computed

最后再来简单模拟一下`computed`的函数的内部实现，`computed`的需要接受一个有返回值的函数作为参数，这个函数的返回值就是计算属性的值，并且要监听这个函数内部使用的响应式数据的变化，最后把这个函数执行的结果返回。

```js
export function computed(getter) {
  const result = ref()
  effect(() => (result.value = getter))
  return result
}
```

在`effect`中执行`get`的时候，访问响应式数据的属性会去收集依赖，当数据变化后会重新执行`effect`函数，把`get`的结果再存储到`result`中。打开页面进行测试。

```js
// 判断是否为对象
const isObject = val => val !== null && typeof val === 'object'
// 判断target是否为对象，如果是对象，则继续调用reactive函数将其转为响应式对象，如果不是对象，直接返回target
const convert = target => isObject(target) ? reactive(target) : target
const hasOwnProperty = Object.prototype.hasOwnProperty
const hasOwn = (target, key) => hasOwnProperty.call(target, key)

export function reactive(target) {
  if (!isObject(target)) return target

  const handler = {
    get(target, key, receiver) {
      // 收集依赖
      track(target, key)
      const result = Reflect.get(target, key, receiver)
      return convert(result)
    },
    set(target, key, value, receiver) {
      // 获取
      const oldValue = Reflect.get(target, key, receiver)
      let result = true
      if (oldValue !== value) {
        result = Reflect.set(target, key, value, receiver)
        // 触发更新
        trigger(target, key)
      }
      return result
    },
    deleteProperty(target, key) {
      const hadKey = hasOwn(target, key)
      const result = Reflect.deleteProperty(target, key)
      if (hadKey && result) {
        // 触发更新
        trigger(target, key)
      }
      return result
    }
  }

  return new Proxy(target, handler)

}


let activeEffect = null

export function effect(callback) {
  //  effect中首先要执行一次callback，访问响应时对象属性，去收集依赖
  activeEffect = callback
  callback()
  activeEffect = null
}

let targetMap = new WeakMap()

export function track(target, key) {
  if (!activeEffect) return
  let depsMap = targetMap.get(target)
  if (!depsMap) {
    targetMap.set(target, (depsMap = new Map()))
  }
  let dep = depsMap.get(key)
  if (!dep) {
    depsMap.set(key, (dep = new Set()))
  }
  dep.add(activeEffect)
}

// 触发更新
export function trigger(target, key) {
  // 根据target，在targetMap中找打key
  const depsMap = targetMap.get(target)
  if (!depsMap) return
  const dep = depsMap.get(key)
  if (dep) {
    dep.forEach(effect => {
      effect()
    })
  }
}

export function ref(raw) {
  // 判断raw是否是ref创建的对象，如果是，直接返回
  if (isObject(raw) && raw.__v_isRef) return

  let value = convert(raw)
  const r = {
    __v_isRef: true,
    get value() {
      track(r, 'value')
      return value
    },
    set value(newValue) {
      if (newValue !== value) {
        raw = newValue
        value = convert(raw)
        trigger(r, 'value')
      }
    }
  }

  return r
}

export function toRefs(proxy) {
  const ret = proxy instanceof Array ? new Array(proxy.length) : {}
  for (const key in proxy) {
    ret[key] = toProxyRef(proxy, key)
  }
  return ret
}


function toProxyRef(proxy, key) {
  return {
    __v_isRef: true,
    get value() {
      return proxy[key]
    },
    set value(newValue) {
      proxy[key] = newValue
    }
  }
}

export function computed (getter) {
  const result = ref()

  effect(() => (result.value = getter()))

  return result
}
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
<script type="module">
  import { reactive, effect, computed } from './my-reactivity/index.js'

  const product = reactive({
    name: 'iPhone',
    price: 5000,
    count: 3
  })

  let total = computed(() => {
    return product.price * product.count
  })


  console.log(total.value)

  product.price = 4000
  console.log(total.value)

  product.count = 1
  console.log(total.value)

</script>
</body>
</html>
```

到这里模拟了响应式系统中的`reactive`、`ref`、`toRefs`、`computed`的函数的内部实现，还实现了依赖收集和触发更新的`track` 、`trigger`以及`effect`函数，但这三个函数比较底层，一般情况下不会直接去调用好。

