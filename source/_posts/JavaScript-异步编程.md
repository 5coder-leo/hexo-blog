---
title: JavaScript 异步编程
tags: JavaScript
category: 大前端
abbrlink: 6342
date: 2021-05-19 22:31:03
cover: false
---

## JavaScript异步编程

### 一、同步模式

> 同步模式指的就是我们代码中的任务依次执行，程序执行的顺序与代码的编写顺序一致。
>
> 以下代码为同步模式的代码，具体分析其执行顺序

```js
console.log('Global begin')

function bar() {
    console.log('Bar task')
}

function foo() {
    console.log('Foo task')
    bar()
}

foo()
console.log('Global end')

// Global begin
// Foo task
// Bar task
// Global end
```

![无法查看时复制链接到浏览器观看：http://5coder.cn/img/202208152208328.gif](http://5coder.cn/img/202208152208328.gif)

分析：

> 1. 首先分析代码结构，本段代码为同步模式，js在读取到代码时，先将一个（anonymous）匿名函数放到调用栈。
>
> 2. 在读取到第一行console.log('Global begin')时，将其压到调用栈，随后去执行，当控制台打印出结果后，将其弹出调用栈，继续下一行代码；
>
> 3. 在读取到bar函数及foo函数时，由于其并未执行，因此调用栈内无执行任务；
> 4. 在读取到foo()函数调用时，首先将foo()压入调用栈，遇console.log('Foo task')代码，将其压入调用栈，执行完毕后弹出调用栈。随后将bar()压入调用栈，程序去bar()函数内部解析，将console.log('Bar task')压入调用栈。foo()函数执行完毕后，依次将bar()、foo()函数弹出调用栈；
> 5. 最后将console.log('Global end')压入调用栈并执行，随后将其弹出，代码运行完成，将(anonymous)弹出调用栈，程序完全结束。

### 二、异步模式

在浏览器端，耗时很长的操作都应该异步执行，避免浏览器失去响应，最好的例子就是Ajax操作。在服务器端，"异步模式"甚至是唯一的模式，因为执行环境是单线程的，如果允许同步执行所有http请求，服务器性能会急剧下降，很快就会失去响应。

异步调用并不会阻止代码的顺序执行，而是在将来的某一个时刻触发设置好的逻辑，所以我们

1. 并不知道逻辑什么时候会被调用
2. 只能定义当触发的时候逻辑是什么
3. 只能等待，同时可以去处理其他的逻辑

```js
console.log('global begin')
setTimeout(function timer1() {
    console.log('timer1 invoke')
}, 1800)
setTimeout(function timer2() {
    console.log('timer2 invoke')
    setTimeout(function inner() {
        console.log('inner invoke')
    }, 1000)
}, 1000)
console.log('global end')

// global begin
// global end
// timer2 invoke
// timer1 invoke
// inner invoke
```

复制地址到浏览器地址栏查看动图演示：

![无法查看时复制链接到浏览器观看：http://5coder.cn/img/202208152208762.gif](http://5coder.cn/img/202208152208762.gif)

分析：

> 首先分析代码结构，本段代码为异步模式，js在读取到代码时，先将一个（`anonymous`）匿名函数放到调用栈。
>
> 将第一行`console.log('global begin')`压入调用栈并执行后弹出，此时控制台打印`global begin`；
>
> 程序到`setTimeout`时，首先将`setTimeout(timer1)`压入调用栈，在web API线程放入timer1计时器，倒计时1.8s，随后将`setTimeout(timer1)`弹出调用栈；
>
> 同上步，将`setTimeout(timer2)`压入调用栈，web API线程放入`timer2`计时器，倒计时1s，随后将`setTimeout(timer2)`弹出调用栈；
>
> 随后将`console.log('global end')`压入调用栈并执行后弹出调用栈，代码执行完毕，将`anonymous`弹出调用栈；
>
> web API将`timer1`与`timer2`依次放入事件队列，此时`timer2`优先倒计时完毕，进入调用栈，然后执行内部代码。将`console.log('timer2 invoke')`压入调用栈并执行后弹出。
>
> 随后遇`setTimeout(inner)`,将其压入调用栈并在Web API加入`inner`计时器，倒计时1s。`setTimeout(inner)`弹出调用栈。
>
> 此时随倒计时，`timer1`倒计时完毕，程序进入`timer1`内部，将`console.log('timer1 invoke')`压入调用栈并执行后弹出。
>
> 随后`inner()`计时器进入任务队列，在倒计时结束后，压入调用栈并执行后弹出。至此，程序执行完毕。

### 三、回调函数

回调函数指的是需要在将来不确定的某一时刻异步调用的函数。通常，在这种回调函数中，我们经常需要频繁地访问外部数据。

```js
function foo(callback) {
    setTimeout(function () {
        callback()
    }, 3000)
}

foo(function () {
    console.log('这就是一个回到函数')
    console.log('调用者定义这个函数，执行者执行这个函数')
    console.log('起始就是调用者告诉执行者：异步任务结束后应该做什么')
})
```

### 四、Promise概述

由于上述回调函数可以存在嵌套关系，因此容易导致**回调地狱**问题，即产生如下代码：

```js
$.get('url1', function (data1) {
    $.get('url2', function (data2) {
        $.get('url3', function (data3) {
            $.get('url4', function (data4) {
                $.get('url5', function (data5) {
                    $.get('url6', function (data6) {
                        $.get('url7', function (data7) {
                            // 略微夸张，但实际存在
                        })
                    })
                })
            })
        })
    })
})
```

因此提出`Promise`承诺，即在回调函数中，承诺在异步完成后下一步干什么。

`Promise`存在三种状态，及承诺开始`pending`，承诺兑现`fulfilled`以及承诺失败`rejected`。并且，承诺的状态一旦确定就不可在被改变，即当状态为`fulfilled`时，此`promise`的状态就不可再变为`rejected`，反之同样。

[传送：Promise基本使用](http://5coder.cn/2021/0519741.html)

`fulfilled`与`rejected`存在`onFulfilled`和`onRejected`状态。

- 什么是`promise`?
- `promise`诞生的意义是什么，为什么会有`promise`?
- `promise`的Api有哪些?
- 如何使用这些Api呢？（mdn有详细的用法，详细的不能太详细）
- 终极解决方案`async`/`await`的使用！
- 手写一个promise吧！