---
title: Vue指令
author: 5coder
abbrlink: 44857
date: 2021-05-20 06:27:27
summary:
tags: Vue
category: 大前端(杂识)
---

# Vue学习-指令

## 1.v-if

> v-if可以完全根据表达式的值在DOM中生成或移除一个元素。true->生成元素；false->移除元素。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  <p v-if="flag">如果条件为真，我显示；条件为假我不显示</p>
  <p v-if="flag2">俺也一样</p>
</div>
<script src="vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      flag: true,
      flag2: false
    },
    methods: {}
  })
</script>
</body>
</html>
```

*切换多个元素时，把template元素当做包装元素，并在其上使用v-if，最终渲染的结果不会包含它*

```html
<template v-if="templateFlag">
  <h1>Title</h1>
  <p>Paragraph1</p>
  <p>Paragraph2</p>
</template>
```

![](https://img-blog.csdnimg.cn/20210323152850534.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjEyMjM1NQ==,size_16,color_FFFFFF,t_70)


## 2.v-show

> v-show指令是根据表达式的值来显示或隐藏，其原理是动态的在元素上添加style="display:none"。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<div id="app">
  <p v-show="flag">v-show是否显示？</p>
</div>
<script src="vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      flag:false
    },
    methods: {}
  })
</script>
</body>
</html>
```

*v-show不支持template语法*

> v-if与v-show
>
> 在切换v-if模块时Vue.js有一个局部编译/卸载的过程，因为v-if中的模板可能包括数据绑定或子组件。v-if时真实的条件渲染，因为他会确保条件在切换时合适的销毁与重建条件快内的事件监听器和子组件
>
> v-if时惰性的——若初始渲染条件为假，则什么也不做，在条件第一次变为真时才开始拒不变异（编译会被缓存起来）
>
> v-show简单得多——元素始终被编译保留，知识简单的基于CSS切换。
>
> *一般来时v-if有更高的切花小号，而v-show有更高的初始渲染消耗。因此*如果需要频繁的切换，则使用v-show较好；如果在运行时条件不大可能改变，则使用v-if较好。

## 3.v-else

> v-else必须跟着v-if或v-show，充当else功能。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  <p v-if="ok">我是对的</p>
  <p v-else="ok">我是错的</p>
</div>
<script src="vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      ok:false
    },
    methods: {}
  })
</script>
</body>
</html>
```

## 4.v-model

> v-model指令使用来在input、select、text、checkbox、radio等表单控件元素上创建**双向数据绑定**。根据空间类型v-model自动选取正确的方式更新元素。v-model不过是语法糖，在用户输入时间中更新数据，以及特别处理一些极端例子。

简易计算器计算器：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<div id="app">
  <input type="number" v-model="a">
  <select v-model="operator">
    <option value="+">+</option>
    <option value="-">-</option>
    <option value="*">*</option>
    <option value="/">/</option>
  </select>
  <input type="number" v-model="b">
  <input type="button" @click="calculator" value="=">
  <input type="text" v-model="result">
</div>
<script src="vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      a:0,
      operator:'+',
      b:0,
      result:0
    },
    methods: {
      calculator () {
        this.result = eval(this.a + this.operator + this.b)
      }
    }
  })
</script>
</body>
</html>
```

> v-model除了上面的用法，还可以添加多个参数：number、lazy、debounce（vue2.0后移除，移除原因：其实现的是控制状态更新频率而不是控制高耗任务你是）
>
> - number：将用户输入自动转换为Number类型（如果转换结果为NaN，则返回原值）
>
> - lazy：默认情况下，v-model在inout时间中同步输入框的值与数据，可以添加一个lazy特性，从而将数据改到在change时间中发生
>
>   ```html
>   <!DOCTYPE html>
>   <html lang="en">
>   <head>
>       <meta charset="UTF-8">
>       <title>Title</title>
>   </head>
>   <body>
>           
>   <div id="app">
>     <input type="text" v-model.lazy="msg">
>     {{msg}}
>   </div>
>   <script src="vue.js"></script>
>   <script>
>     let vm = new Vue({
>       el: '#app',
>       data: {
>         msg: '内容实在change事件后才改变的'
>       },
>       methods: {}
>     })
>   </script>
>   </body>
>   </html>
>   ```

## [5.v-for](https://cn.vuejs.org/v2/guide/list.html)

> v-for指令基础原始局重复渲染元素。
>
> v-for需要特殊的别名，形式为“item in items”(items是数据数组，item是别名)，也可以用 `of` 替代 `in` 作为分隔符，因为它更接近 JavaScript 迭代器的语法(**一般 js for in 是遍历 key, 而 for of 遍历 value**)
>
> ```html
> <div v-for="item of items"></div>
> ```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>

<div id="app">
  <p v-for="item in list">{{item}}</p>
  <ul>
    <li v-for="(item,i) in list">{{i}} + {{item}}</li>  <!--v-for 还支持一个可选的第二个参数，即当前项的索引。-->
  </ul>


</div>
<script src="vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      list: [1, 2, 3, 4, 5, 6]
    },
    method: {}
  })
</script>
</body>
</html>
```

> 当 Vue 正在更新使用 `v-for` 渲染的元素列表时，它默认使用“就地更新”的策略。如果数据项的顺序被改变，Vue 将不会移动 DOM 元素来匹配数据项的顺序，而是就地更新每个元素，并且确保它们在每个索引位置正确渲染。
>
> 这个默认的模式是高效的，但是**只适用于不依赖子组件状态或临时 DOM 状态 (例如：表单输入值) 的列表渲染输出**。
>
> 建议尽可能在使用 `v-for` 时提供 `key` attribute，除非遍历输出的 DOM 内容非常简单，或者是刻意依赖默认行为以获取性能上的提升。
>
> **不要使用对象或数组之类的非基本类型值作为 `v-for` 的 `key`。请用字符串或数值类型的值。**
>
> ```html
> <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body><div id="app"><div> <label for="">ID:   <input type="text" v-model="id"></label> <label for="">Name:   <input type="text" v-model="name"> </label> <label for="">添加：   <input type="button" value="添加" @click="add"> </label></div><p v-for="item in list" :key="item.id"> <label for=""> <input type="checkbox"> </label> {{item.id}}------{{item.name}}</p></div><script src="vue.js"></script><script>let vm = new Vue({ el: '#app', data: {   id:'',   name:'',   list:[     {'id':1,'name':'李斯'},     {'id':2,'name':'嬴政'},     {'id':3,'name':'赵高'},     {'id':4,'name':'韩非子'},     {'id':5,'name':'荀子'},   ],   obj: {     name: 'Leo',     age: 28,     sex: 'male'   } }, methods: {   add(){     this.list.unshift({id:this.id, name:this.name})   } }})</script></body></html>
> ```



### 数组更新检查

#### 变更方法

- push()：向尾部添加元素。改变原数组。
- pop()：从数组中删除最后一个元素，并返回该元素的值。并重置数组的长度。改变原数组。
- shift()：删除**第一个**元素并返回该元素的值，并重置数组的长度。改变原数组。
- unshift()：将一个或多个元素添加到数组的**开头**，并返回该数组的**新长度**。改变原数组。
- splice()：通过删除或替换现有元素或者原地添加新的元素来修改数组,并以数组形式返回被修改的内容。改变原数组。
- sort()：方法用[原地算法](https://en.wikipedia.org/wiki/In-place_algorithm)对数组的元素进行排序，并返回数组。默认排序顺序是在将元素转换为字符串，然后比较它们的UTF-16代码单元值序列时构建的。改变原数组。
- reverse()：将数组中元素的位置颠倒，并返回该数组。数组的第一个元素会变成最后一个，数组的最后一个元素变成第一个。改变原数组。

#### 替换数组

变更方法，顾名思义，会变更调用了这些方法的原始数组。相比之下，也有非变更方法，例如 `filter()`、`concat()` 和 `slice()`。它们不会变更原始数组，而**总是返回一个新数组**。当使用非变更方法时，可以用新数组替换旧数组：

```js
example1.items = example1.items.filter(function (item) {
  return item.message.match(/Foo/)
})
```

你可能认为这将导致 Vue 丢弃现有 DOM 并重新渲染整个列表。幸运的是，事实并非如此。Vue 为了使得 DOM 元素得到最大范围的重用而实现了一些智能的启发式方法，所以用一个含有相同元素的数组去替换原来的数组是非常高效的操作。

## 6.v-text

> v-text指令可以更新元素的textContent。在内部，{{Mustache}}差值也被编译为textNode的一个v-text指令。v-text会将DOM元素中的textContent完全替换。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<div id="app">
  <h1 v-text="msg">这段话会被v-text完全替换！！！</h1>
</div>
<script src="vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      msg:'用你自己的方式，去成为一个真正的神。'
    },
    methods: {}
  })
</script>
</body>
</html>
```

## 7.v-html

> v-html指令可以更新元素的innerHTML。内容按普通的HTML插入——数据绑定被忽略。
>
> **在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 [XSS 攻击](https://en.wikipedia.org/wiki/Cross-site_scripting)。只在可信内容上使用 `v-html`，永不用在用户提交的内容上。**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<div id="app">
  <h1 v-html="htmlStr"></h1>
</div>
<script src="vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      htmlStr:'<h1>用你自己的方式，去成为一个真正的神！</h1>'
    },
    methods: {}
  })
</script>
</body>
</html>
```

> 在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 [XSS 攻击](https://en.wikipedia.org/wiki/Cross-site_scripting)。只在可信内容上使用 `v-html`，**永不**用在用户提交的内容上。

## 8.v-bind

> v-bind指令用于响应更新HTML特性，讲一个或多个attribute或者一个组件prop动态绑定到表达式。

```html
 <p v-bind:title="myTitle">鼠标悬浮显示title</p>
 <p :title="myTitle">鼠标悬浮显示title</p>  <!--缩写-->
```

```html
<!-- 绑定一个 attribute -->
<img v-bind:src="imageSrc">

<!-- 动态 attribute 名 (2.6.0+) -->
<button v-bind:[key]="value"></button>

<!-- 缩写 -->
<img :src="imageSrc">

<!-- 动态 attribute 名缩写 (2.6.0+) -->
<button :[key]="value"></button>

<!-- 内联字符串拼接 -->
<img :src="'/path/to/images/' + fileName">

<!-- class 绑定 -->
<div :class="{ red: isRed }"></div>
<div :class="[classA, classB]"></div>
<div :class="[classA, { classB: isB, classC: isC }]">

<!-- style 绑定 -->
<div :style="{ fontSize: size + 'px' }"></div>
<div :style="[styleObjectA, styleObjectB]"></div>

<!-- 绑定一个全是 attribute 的对象 -->
<div v-bind="{ id: someProp, 'other-attr': otherProp }"></div>

<!-- 通过 prop 修饰符绑定 DOM attribute -->
<div v-bind:text-content.prop="text"></div>

<!-- prop 绑定。“prop”必须在 my-component 中声明。-->
<my-component :prop="someThing"></my-component>

<!-- 通过 $props 将父组件的 props 一起传给子组件 -->
<child-component v-bind="$props"></child-component>

<!-- XLink -->
<svg><a :xlink:special="foo"></a></svg>
```

## 9.v-on

> v-on指令用于绑定事件监听器。事件类型由参数指定；表达式可以是一个方法的名字或一个内敛语句；如果没有修饰符，也可以省略。

```html
<input type='button' v-on:click='doSomething'>
<input type='button' @click='doSomething'>  <!--缩写-->
```

> 绑定事件监听器。事件类型由参数指定。表达式可以是一个方法的名字或一个内联语句，如果没有修饰符也可以省略。
>
> 用在普通元素上时，只能监听[**原生 DOM 事件**](https://developer.mozilla.org/zh-CN/docs/Web/Events)。用在自定义元素组件上时，也可以监听子组件触发的**自定义事件**。
>
> 在监听原生 DOM 事件时，方法以事件为唯一的参数。如果使用内联语句，语句可以访问一个 `$event` property：`v-on:click="handle('ok', $event)"`。
>
> 从 `2.4.0` 开始，`v-on` 同样支持不带参数绑定一个事件/监听器键值对的对象。注意当使用对象语法时，是不支持任何修饰器的。

#### 事件修饰符

> - `.stop` - 调用 `event.stopPropagation()`。阻止冒泡。
> - `.prevent` - 调用 `event.preventDefault()`。阻止默认事件，例如a链接的跳转事件。
> - `.capture` - 添加事件侦听器时使用 capture 模式。
> - `.self` - 只当事件是从侦听器绑定的元素本身触发时才触发回调。
> - `.{keyCode | keyAlias}` - 只当事件是从特定键触发时才触发回调。
> - `.native` - 监听组件根元素的原生事件。
> - `.once` - 只触发一次回调。
> - `.left` - (2.2.0) 只当点击鼠标左键时触发。
> - `.right` - (2.2.0) 只当点击鼠标右键时触发。
> - `.middle` - (2.2.0) 只当点击鼠标中键时触发。
> - `.passive` - (2.3.0) 以 `{ passive: true }` 模式添加侦听器
>
> ```html
> <!-- 方法处理器 -->
> <button v-on:click="doThis"></button>
> 
> <!-- 动态事件 (2.6.0+) -->
> <button v-on:[event]="doThis"></button>
> 
> <!-- 内联语句 -->
> <button v-on:click="doThat('hello', $event)"></button>
> 
> <!-- 缩写 -->
> <button @click="doThis"></button>
> 
> <!-- 动态事件缩写 (2.6.0+) -->
> <button @[event]="doThis"></button>
> 
> <!-- 停止冒泡 -->
> <button @click.stop="doThis"></button>
> 
> <!-- 阻止默认行为 -->
> <button @click.prevent="doThis"></button>
> 
> <!-- 阻止默认行为，没有表达式 -->
> <form @submit.prevent></form>
> 
> <!--  串联修饰符 -->
> <button @click.stop.prevent="doThis"></button>
> 
> <!-- 键修饰符，键别名 -->
> <input @keyup.enter="onEnter">
> 
> <!-- 键修饰符，键代码 -->
> <input @keyup.13="onEnter">
> 
> <!-- 点击回调只会触发一次 -->
> <button v-on:click.once="doThis"></button>
> 
> <!-- 对象语法 (2.4.0+) -->
> <button v-on="{ mousedown: doThis, mouseup: doThat }"></button>
> ```

#### 键盘修饰符以及自定义键盘修饰符

##### 1.x中自定义键盘修饰符【了解即可】

```js
Vue.directive('on').keyCodes.f2 = 113;
```

##### [2.x中自定义键盘修饰符](https://cn.vuejs.org/v2/guide/events.html#键值修饰符)

1. 通过`Vue.config.keyCodes.名称 = 按键值`来自定义案件修饰符的别名：

```js
Vue.config.keyCodes.f2 = 113;
```

2. 使用自定义的按键修饰符：

```js
<input type="text" v-model="name" @keyup.f2="add">
```



## 10.v-cloak

> v-cloak这个指令保持在元素上直到关联实例结束编译。和 CSS 规则如 `[v-cloak] { display: none }` 一起用时，这个指令可以隐藏未编译的 Mustache 标签直到实例准备完毕。
>
> 放置页面出现Mustache标签

```html
[v-cloak] {
  display: none;
}
<div v-cloak>
  {{ message }}  <!--不会显示，直到编译结束。-->
</div>
Vue.directive('on').keyCodes.f2 = 113;
```

##### [2.x中自定义键盘修饰符](https://cn.vuejs.org/v2/guide/events.html#键值修饰符)

1. 通过`Vue.config.keyCodes.名称 = 按键值`来自定义案件修饰符的别名：

```js
Vue.config.keyCodes.f2 = 113;
```

2. 使用自定义的按键修饰符：

```js
<input type="text" v-model="name" @keyup.f2="add">
```

