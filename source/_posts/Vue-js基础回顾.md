---
title: Vue.js基础回顾
author: 5coder
abbrlink: 41703
date: 2021-05-23 09:29:59
tags: Vue
category: 大前端
password:
keywords: Vue
top:
cover:
---

# 一、Vue基础结构

Vue代码的基础结构：

1. 这是最基础的Vue代码，在创建Vue实例时，传入`el`和`data`选项，Vue内部会把`data`中的数据传入到`el`指向的模板中，并把模板渲染到浏览器。

![image-20210523093150780](http://5coder.cn/img/98EjT6puZt5nlBF.png)

2. 本段代码执行的效果与上面相同，这里使用了render选项和**$mount**方法。使用**Vue-cli**脚手架创建的代码解构与下面的代码相同，**render**方法接受一个参数，参数为**h**函数，**h**函数在后面的笔记中会有详细的讲解，这里简单介绍一下，h函数的作用是创建虚拟dom，**render**方法把h函数创建的虚拟dom返回。​**$mount**的作用是把虚拟dom转换成真实dom渲染到浏览器。

![image-20210523093852667](http://5coder.cn/img/TnFxfGS3zP5iYOV.png)

# 二、Vue的生命周期

下面给出vue生命周期图示，每个生命周期函数作用都会讲到。

每个 Vue 实例在被创建时都要经过一系列的初始化过程——例如，需要设置数据监听、编译模板、将实例挂载到 DOM 并在数据变化时更新 DOM 等。同时在这个过程中也会运行一些叫做**生命周期钩子**的函数，这给了用户在不同阶段添加自己的代码的机会。

![20210323232204766.png](http://5coder.cn/img/9mk8PLyboMi6uwV.png)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>

</head>
<body>
<div id="app">
  <input type="button" value="数据更新" @click="msg='No'">
  <h3 id="h3">{{msg}}</h3>
</div>

<script src="vue.js"></script>
<script>
  let vm = new Vue({
    el: '#app',
    data: {
      msg: 'ok'
    },
    methods: {
      show() {
        console.log('show方法被调用')
      }
    },
    beforeCreate() {
      // console.log(this.msg)  // undefined
      // this.show()  // this.show is not a function
    },
    created() {
      // console.log(this.msg)  // ok
      // this.show()  // show方法被调用
    },
    beforeMount() {
      // console.log(document.getElementById('h3').innerHTML)  // {{msg}}
    },
    mounted() {
      // console.log(document.getElementById('h3').innerHTML)  // ok
    },
    beforeUpdate() {
      // console.log(document.getElementById('h3').innerHTML)  // ok
      // console.log('data中的数据' + this.msg)  // No
    },
    updated() {
      // console.log('界面上的内容' + document.getElementById('h3').innerHTML)  // ok
      // console.log('data中的数据' + this.msg)  // ok
    },

  })
</script>
</body>
</html>
```

# 三、Vue语法和概念

详细信息查看链接（Vue官方文档）

1. 插值表达式

   - 文本

     数据绑定最常见的形式就是使用“Mustache”语法 (双大括号) 的文本插值：

     ```html
     <span>Message: {{ msg }}</span>
     ```

     Mustache 标签将会被替代为对应数据对象上 `msg` property 的值。无论何时，绑定的数据对象上 `msg` property 发生了改变，插值处的内容都会更新。

     通过使用 [v-once 指令](https://cn.vuejs.org/v2/api/#v-once)，你也能执行一次性地插值，当数据改变时，插值处的内容不会更新。但请留心这会影响到该节点上的其它数据绑定：

     ```html
     <span v-once>这个将不会改变: {{ msg }}</span>
     ```

2. 指令（指令详细文档，请移步[这里]()，官方文档在[这里](https://cn.vuejs.org/v2/guide/syntax.html#%E6%8C%87%E4%BB%A4)）

3. [计算属性和侦听器](https://cn.vuejs.org/v2/guide/computed.html)

4. [Class和Style绑定](https://cn.vuejs.org/v2/guide/class-and-style.html)

5. [条件渲染](https://cn.vuejs.org/v2/guide/conditional.html)/[列表渲染](https://cn.vuejs.org/v2/guide/list.html)

6. [表单输入绑定](https://cn.vuejs.org/v2/guide/forms.html)

7. [组件](https://cn.vuejs.org/v2/guide/components.html)

8. [插槽](https://cn.vuejs.org/v2/guide/components-slots.html)

9. [插件](https://cn.vuejs.org/v2/guide/plugins.html)

10. [混入mixin](https://cn.vuejs.org/v2/guide/mixins.html)

11. [深入响应式原理](https://cn.vuejs.org/v2/guide/reactivity.html)

12. [不同构建版本的Vue](https://cn.vuejs.org/v2/guide/migration.html)