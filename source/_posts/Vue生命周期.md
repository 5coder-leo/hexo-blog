---
title: Vue生命周期
author: 5coder
abbrlink: 19670
date: 2021-05-20 06:27:56
summary:
tags: Vue
category: 大前端(杂识)
---

# Vue学习——生命周期

每个 Vue 实例在被创建时都要经过一系列的初始化过程——例如，需要设置数据监听、编译模板、将实例挂载到 DOM 并在数据变化时更新 DOM 等。同时在这个过程中也会运行一些叫做**生命周期钩子**的函数，这给了用户在不同阶段添加自己的代码的机会。

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/ufJwjZr6YklT4F7.png)


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

