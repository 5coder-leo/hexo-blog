---
title: JavaScript-堆栈问题
author: 5coder
tags: JavaScript
category: 大前端
abbrlink: 36194
date: 2022-08-23 17:22:53
---

## JavaScript-堆栈问题

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



![04-闭包与堆栈执行](http://5coder.cn/img/1661246438_d9698b81f9e56f58defa6f26c9f7569e.png)

### 5.闭包与垃圾回收



![05-闭包与GC](http://5coder.cn/img/1661246446_efad8315a80a738cc9a9b099dff2eaf2.png)

### 6.循环添加事件

![06-循环添加事件](http://5coder.cn/img/1661246456_b113bf25d47870695d5a1d730966c7fd.png)



### 7.事件添加底层分析





### 8.事件委托

### 9.变量局部化

### 10.减少访问层

### 11.缓存数据

### 12.防抖与节流

#### **防抖函数实现**

#### **节流函数实现**
