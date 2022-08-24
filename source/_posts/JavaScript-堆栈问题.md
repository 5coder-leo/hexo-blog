---
title: JavaScript-堆栈分析
author: 5coder
tags: 
  - JavaScript
  - 性能优化
category: 大前端
abbrlink: 36194
date: 2022-08-23 17:22:53
---

## JavaScript-堆栈分析

### 1.堆栈处理

堆栈准备

- JavaScript执行环境
- 执行环境栈（ECStack，execution context stack）
- 全局执行环境栈（EC(G)）
- 执行上下文
- VO(g)：Variable Object(Global)，全局变量对象
- GO:Global Object，全局对象类似于window

```js
var x = 100
var y = x
y = 200
console.log(x)

/*
1.基本数据类型是按照值进行操作
2.基本数据类型的值是存放在栈区的，复杂数据类型是存放在堆区的
3.无论栈内存还是后续引用数据类型会使用到的堆内存，都属于计算机内存
4.GO(全局对象)
*/
```

![堆栈处理](http://5coder.cn/img/1661234581_5e00a465c2d6a28f3c8669b5a70056fc.png)

### 2.引用类型堆栈处理

```js
var obj1 = {x : 100}
var obj2 = obj1
obj2['x'] = 200
console.log(obj1['x'])
// 如下图
```

![引用类型堆栈](http://5coder.cn/img/1661235391_ffc9609fac409a687893b24ef4c30549.png)

```js
var obj1 = {x : 100}
var obj2 = obj1
obj2 = {
    name: 'alishi'
}
console.log(obj1['x'])
// 如下图
```

![引用类型堆栈2](http://5coder.cn/img/1661242580_485c5e2b87f35ad431a0a9cbf1ec1932.png)

```js
var obj1 = {x: 100}
var obj2 = obj1
obj1.y = obj1 = {x: 200}
// 类似
// obj1.y = {x: 200}
// obj1 = {x: 200}
console.log(obj1)  // { x: 200 }
console.log(obj1.y)  // undefined
console.log(obj2)  // { x: 100, y: { x: 200 } }

// 如下图
```

![引用类型堆栈3](http://5coder.cn/img/1661243538_5c7becdef671a6df9df32643e6b4d711.png)

### 3.函数堆栈处理

```js
var arr = ['5coder', 'leo']

function foo(obj) {
  obj[0] = 'zoe'
  obj = ['拉钩教育']
  obj[1] = '大前端'
  console.log(obj)
}

foo(arr)
console.log(arr)
/**
 * 01 函数创建
 * -- 可以将函数名称看做是变量，存放在 VO 当中 ，同时它的值就是当前函数对应的内存地址
 * -- 函数本身也是一个对象，创建时会有一个内存地址，空间内存放的就是函数体代码（字符串形式的）
 * 02 函数执行
 * -- 函数执行时会形成一个全新私有上下文，它里面有一个AO 用于管理这个上下文当中的变量
 * -- 步骤：
 *  01 作用域链 <当前执行上下文， 上级作用域所在的执行上下文>
 *  02 确定 this
 *  03 初始化 arguments （对象）
 *  04 形参赋值：它就相当于是变量声明，然后将声明的变量放置于 AO
 *  05 变量提升
 *  06 代码执行
 */

// 如下图
```

![函数堆栈执行](http://5coder.cn/img/1661245987_0d4232baf1231cc6f55c4fcd8b9b01bf.png)

### 4.闭包堆栈处理

```js
var a = 1
function foo() {
  var b = 2
  return function (c) {
    console.log(c + b++)
  }
}

var f = foo()
f(5)
f(10)

/*
* 1.闭包：是一种机制
*   保护：当前上下文当中的变量与其他的上下文中变量互不干扰
*   保存：当前上下文中的数据（对地址）被当前上下文以外的上下文忠的变量引用，这个数据就保存下来
* 2.闭包：
*   函数调用想成了一个全新的私有上下文，在函数调用之后当前上下文不被释放就是闭包（临时不被释放）
*
* */
// 如下图
```



![04-闭包与堆栈执行](http://5coder.cn/img/1661246438_d9698b81f9e56f58defa6f26c9f7569e.png)

### 5.闭包与垃圾回收

```js
let a = 10
function foo(a) {
  return function (b) {
    console.log(b + (++a))
    
  }
}

let fn = foo(10)
fn(5)
foo(6)(7)
fn(20)
console.log(a)
// 如下图
```



![05-闭包与GC](http://5coder.cn/img/1661246446_efad8315a80a738cc9a9b099dff2eaf2.png)

### 6.循环添加事件

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>循环添加事件</title>
</head>
<body>
<button>按钮1</button>
<button>按钮2</button>
<button>按钮3</button>
<script>
  var aButtons = document.querySelectorAll('button')
  console.log(aButtons)
  /*
  * 基础
  for (var i = 0; i < aButtons.length; i++) {
    aButtons[i].onclick = function () {
      console.log(`当前的索引值为${i}`)
    }
  }
   */

  /*  for (var i = 0; i < aButtons.length; i++) {
      (function (i) {
        aButtons[i].onclick = function () {
          console.log(`当前的索引值为${i}`)
        }
      })(i)
    }*/

  /*  for (var i = 0; i < aButtons.length; i++) {
      aButtons[i].onclick = (function (i) {
        return function () {
          console.log(`当前的索引值为${i}`)
        }
      })(i)
    }*/


  /*  for (let i = 0; i < aButtons.length; i++) {
      aButtons[i].onclick = function () {
        console.log(`当前的索引值为${i}`)
      }
    }*/

  for (var i = 0; i < aButtons.length; i++) {
    aButtons[i].myIndex = i
    aButtons[i].onclick = function () {
      console.log(`当前的索引值为${this.myIndex}`)
    }
  }

</script>
</body>
</html>

```

循环添加事件-底层执行分析

![循环添加事件](http://5coder.cn/img/1661246456_b113bf25d47870695d5a1d730966c7fd.png)

### 8.循环添加事件-事件委托方法实现

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
</head>
<body>
  <button index="1">按钮1</button>
  <button index="2">按钮2</button>
  <button index="3">按钮3</button>
</body>
<script>
  document.body.onclick = function (event) {
    var target = event.target,
      targetDom = target.tagName
    if (targetDom === 'BUTTON') {
      var index = target.getAttribute('index')
      console.log(`当前点击的是第${index}个按钮`)
    }
  }
</script>
</html>
<!--如下图-->
```

![事件委托](http://5coder.cn/img/1661307355_b8f4f25c38bc099ea4aea74e6f3a538c.png)

### 9.变量局部化

```js
// 变量局部化（全局、局部）
// 这样可以提高代码的执行效率（减少了数据访问时需要查找的路径）
// 数据的存储和读取
var i, str = ""

// function packageDom() {
//   for (var i = 0; i < 1000; i++) {
//     str += i
//   }
// }
// packageDom()


function packageDom() {
  let str = ''
  for (let i = 0; i < 1000; i++) {
    str += i
  }
}

packageDom()
// jsBench测试结果如下图
```

![jsBench测试结果](http://5coder.cn/img/1661321607_fde7f67fd0417f1288947a1d269e2cb4.png)

**减少访问层**

底层分析（**减少了数据访问时需要查找的路径-ec(page)到EC(G)**）：

![数据存取](http://5coder.cn/img/1661321648_181b4e8c1f47d498cc08b24520160a53.png)

### 10.缓存数据

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>减少数据读取次数</title></head>
<body>
<div id="skip" class="skip"></div>
<script>        
    var oBox = document.getElementById('skip')

    function hasEle(ele, cls) {
      console.log(ele.className)
      return ele.className === cls
    }
	
    // 空间上多一些占用
    function hasEle(ele, cls) {
      var className = ele.className
      console.log(className)
      return className === cls
    }

	console.log(hasEle(oBox, 'skip'))
</script>
</body>
</html>
```

![](http://5coder.cn/img/53YtRCWn2o1jsaT.png)

### 11.减少访问层数

```js
// 减少访问层级

function Person() {
  this.name = '5coder'
  this.age = 28
}

let p1 = new Person()
console.log(p1.age)


function Person() {
  this.name = '5coder'
  this.age = 28
  // 增加访问层数
  this.getAge = function () {
    return this.age
  }
}

let p1 = new Person()
console.log(p1.getAge())

```

![减少访问层数](http://5coder.cn/img/1661323050_f4fde3c4a6c357d42eb4f0143901daf9.png)

### 12.防抖与节流

> - 为什么需要防抖和节流：
>
> 在一些高频率事件触发的场景下我们不希望对应的事件处理函数多次执行场景:
>
> - 滚动事件
> - 输入的模糊匹配
> - 轮播图切换
> - 点击操作....
>
> 
>
> 浏览器默认情况下都会有自己的监听事件间隔（ 4~6ms)，如果检测到多次事件的监听执行，那么就会造成不必要的资源浪费。
>
> 前置的场景： 界面上有一个按钮，我们可以连续多次点击
>
> 防抖：对于这个高频的操作来说，我们只希望识别一次点击，可以人为是第一次或者是最后一次
> 节流：对于高频操作，我们可以自己来设置频率，让本来会执行很多次的事件触发，按着我们定义的频率减少触发的次数

- #### **防抖函数实现**

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>防抖函数实现</title>
</head>

<body>
  <button id="btn">点击</button>
  <script>
    var oBtn = document.getElementById('btn')
    // oBtn.onclick = function () {
    //   console.log('点击了')
    // }

    /** 
     * handle 最终需要执行的事件监听
     * wait 事件触发之后多久开始执行
     * immediate 控制执行第一次还是最后一次，false 执行最后一次
    */
    function myDebounce(handle, wait, immediate) {

      // 参数类型判断及默认值处理
      if (typeof handle !== 'function') throw new Error('handle must be an function')
      if (typeof wait === 'undefined') wait = 300
      if (typeof wait === 'boolean') {
        immediate = wait
        wait = 300
      }
      if (typeof immediate !== 'boolean') immediate = false

      // 所谓的防抖效果我们想要实现的就是有一个 ”人“ 可以管理 handle 的执行次数
      // 如果我们想要执行最后一次，那就意味着无论我们当前点击了多少次，前面的N-1次都无用
      let timer = null
      return function proxy(...args) {
        let self = this,
          init = immediate && !timer
        clearTimeout(timer)
        timer = setTimeout(() => {
          timer = null
          !immediate ? handle.call(self, ...args) : null
        }, wait)

        // 如果当前传递进来的是 true 就表示我们需要立即执行
        // 如果想要实现只在第一次执行，那么可以添加上 timer 为 null 做为判断
        // 因为只要 timer 为 Null 就意味着没有第二次....点击
        init ? handle.call(self, ...args) : null
      }

    }

    // 定义事件执行函数
    function btnClick(ev) {
      console.log('点击了1111', this, ev)
    }

    // 当我们执行了按钮点击之后就会执行...返回的 proxy
    oBtn.onclick = myDebounce(btnClick, 200, false)
    // oBtn.onclick = btnClick()  // this ev

  </script>
</body>

</html>
```



- #### **节流函数实现**

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>节流函数实现</title>
  <style>
    body {
      height: 5000px;
    }
  </style>
</head>

<body>
  <script>
    // 节流：我们这里的节流指的就是在自定义的一段时间内让事件进行触发

    function myThrottle(handle, wait) {
      if (typeof handle !== 'function') throw new Error('handle must be an function')
      if (typeof wait === 'undefined') wait = 400

      let previous = 0  // 定义变量记录上一次执行时的时间
      let timer = null  // 用它来管理定时器

      return function proxy(...args) {
        let now = new Date() // 定义变量记录当前次执行的时刻时间点
        let self = this
        let interval = wait - (now - previous)

        if (interval <= 0) {
          // 此时就说明是一个非高频次操作，可以执行 handle
          clearTimeout(timer)
          timer = null
          handle.call(self, ...args)
          previous = new Date()
        } else if (!timer) {
          // 当我们发现当前系统中有一个定时器了，就意味着我们不需要再开启定时器
          // 此时就说明这次的操作发生在了我们定义的频次时间范围内，那就不应该执行 handle
          // 这个时候我们就可以自定义一个定时器，让 handle 在 interval 之后去执行
          timer = setTimeout(() => {
            clearTimeout(timer) // 这个操作只是将系统中的定时器清除了，但是 timer 中的值还在
            timer = null
            handle.call(self, ...args)
            previous = new Date()
          }, interval)
        }
      }

    }

    // 定义滚动事件监听
    function scrollFn() {
      console.log('滚动了')
    }

    // window.onscroll = scrollFn
    window.onscroll = myThrottle(scrollFn, 600)
  </script>
</body>

</html>

```

