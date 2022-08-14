---
title: 函数式编程-review
author: 5coder
category: Web Review
keywords: Review
abbrlink: 27799
date: 2022-08-14 17:30:06
tags: Review
password:
top:
cover:
---

# 一、函数式编程

- 函数式编程是一种编程范式，和面向对象编程是并列关系（编程范式：思想 + 实现的方式）

  - 面向对象编程：对现实世界中的事物的抽象，抽象出对象以及对象和对象之间的关系
  - 函数式编程：把现实世界的事物和事物之间的**联系**抽象到程序世界（对运算过程进行抽象）

  

  重点掌握：

  - 纯函数

    [https://zh.wikipedia.org/wiki/%E7%BA%AF%E5%87%BD%E6%95%B0](https://zh.wikipedia.org/wiki/纯函数)

    在程序设计中，若一个函数符合以下要求，则它可能被认为是**纯函数**：

    * 此函数在**相同的输入**值时，需**产生相同的输出**。函数的输出和输入值以外的其他隐藏信息或[状态](https://zh.wikipedia.org/w/index.php?title=程式狀態&action=edit&redlink=1)无关，也和由I/O设备产生的外部输出无关。

  * 该函数**不能有**语义上可观察的函数**副作用**，诸如“触发事件”，使输出设备输出，或更改输出值以外物件的内容等。(如果参数是引用传递，对参数的更改会影响函数以外的数据，因此不是纯函数)

  - 柯里化

  - 函数组合  lodash/fp   compose(fn, n1)  ---> flowRight

  ```js
  const fp = require('lodash/fp')
  
  const add = (a, b) => {
    return a + b
  }
  
  const f = fp.compose(fp.curry(add)(5), add)
  console.log(f(1, 2))
  ```

  - 函子暂时可以作为了解  `Array.of()`    `arr.map()`

- 柯里化概念意义和用法

  - 柯里化：把多个参数的函数转换可以具有任意个参数的函数，可以给函数组合提供细粒度的函数

  - 应用：

    - Vue.js 源码中使用柯里化的位置

      - src/platform/web/patch.js

      ```js
      // patch(obj, vdom1, vdom2)
      
      function createPatch (obj) {
        let ...
        return function patch (vdom1, vdom2) {
          ..
        }
      }
      
      const patch = createPatch(...)
      patch(vdom1, vdom2)
      ```

- 固定不常变化的参数

  

  ```js
  // 方法1
  function isType (type) {
    return function (obj) {
      return Object.prototype.toString.call(obj) === `[object ${type}]`
    }
  }
  
  const isObject = isType('Object')
  const isArray = isType('Array')
  
  
  // 方法2
  function isType (type, obj) {
    return Object.prototype.toString.call(obj) === `[object ${type}]`
  }
  
  let isTypeCurried = curry(isType)
  
  const isObject = isTypeCurried('Object')
  // isObject(obj)
  
  // 柯里化通用函数
  function curry (func) {
    return function curriedFn (...args) {
      // 判断实参和形参的个数
      if (args.length < func.length) {
        return function () {
          return curriedFn(...args.concat(Array.from(arguments)))
        }
      }
      // 实参和形参个数相同，调用 func，返回结果
      return func(...args)
    }
  }
  
  function getSum (a, b, c) {
  	return a + b + c
  }
  let curried = curry(getSum)
  curried(1, 2, 3)
  curried(1)(2)(3)
  curried(1, 2)(3)
  ```

  - 延迟执行(模拟 bind 方法)

  ```js
  function fn (a, b, c) {
  }
  const f = fn.bind(context, 1, 2)
  f(3)
  
  const f = fn.bind(context, 1)
  f(2, 3)
  
  const f = fn.bind(context)
  f(1,2,3)
  
  // rest 参数
  Function.prototype.mybind = function (context, ...args) {
    return (...rest) => this.call(context, ...args, ...rest)
  }
  
  function t (a, b, c) {
    return a + b + c
  }
  
  t.mybind()
  
  const sumFn = t.mybind(this, 1, 2)
  const sum = sumFn(3)
  console.log(sum)
  ```



- 函子在开发中的实际使用场景
  - 作用是控制副作用 (IO)、异常处理 (Either)、异步任务 (Task)

```js
class Functor {
  static of (value) {
    return new Functor(value)
  }
  
  constructor (value) {
    this._value = value
  }

  map (f) {
    return new Functor(f(this._value))
  }

  value (f) {
    return f(this._value)
  }
}

const toRMB = money => new Functor(money)
  .map(v => v.replace('$', ''))
  .map(parseFloat)
  .map(v => v * 7)
  .map(v => v.toFixed(2))
  .value(v => '¥' + v)

console.log(toRMB('$299.9'))
```

- folktale
  - https://folktale.origamitower.com/

```js
const MayBe = require('folktale/maybe')

const toRMB = m => MayBe.fromNullable(m)
  .map(v => v.replace('$', ''))
  .map(parseFloat)
  .map(v => v * 7)
  .map(v => v.toFixed(2))
  .map(v => '¥' + v)
	// .unsafeGet()
  .getOrElse('noting')

console.log(toRMB(null))
```

- 组合函数参数交换

  const split = *.curry((sep, str) =>* .split(str, sep))

  const join = *.curry((sep, array) =>* .join(array, sep)) 

  const map = *.curry((fn, array) =>* .map(array, fn))

  ```js
  const _ = require('lodash')
  
  // 非柯里化 数据优先 迭代置后
  // _.split(str, sep)
  // _.join(array, sep)
  // _.map(array, fn)
  
  // const f = _.flowRight(_.join(...), _.map(...), _.split)
  // console.log(f('NEVER SAY DIE', ' '))
  
  const split = _.curry((sep, str) => _.split(str, sep))
  const join = _.curry((sep, array) => _.join(array, sep))
  const map = _.curry((fn, array) => _.map(array, fn))
  const f = _.flowRight(join('-'), map(_.toLower), split(' '))
  console.log(f('NEVER SAY DIE'))
  ```

  ```js
  const fp = require('lodash/fp')
  
  // 自动柯里化 数据置后 迭代优先
  fp.split(sep)(str)
  fp.join(sep, array)
  fp.map(fn, array)
  
  const f = fp.compose(fp.join('-'), fp.map(fp.toLower), fp.split(' '))
  ```

  

- 柯里化实现原理

  ```js
  function curry (func) {
    return function curriedFn (...args) {
      // 判断实参和形参的个数
      if (args.length < func.length) {
        return function () {
          return curriedFn(...args.concat(Array.from(arguments)))
        }
      }
      // 实参和形参个数相同，调用 func，返回结果
      return func(...args)
    }
  }
  
  function getSum (a, b, c) {
    return a + b + c
  }
  let curried = curry(getSum)
  curried(1, 2, 3)
  curried(1)(2)(3)
  curried(1, 2)(3)
  ```



# 二、函数的执行上下文和闭包

## 1.函数的执行上下文

- 执行上下文（Execution Context）

  - 全局执行上下文
  - 函数级执行上下文
  - eval 执行上下文

- 函数执行的阶段可以分文两个：函数建立阶段、函数执行阶段

  - 函数建立阶段：当调用函数时，还没有执行函数内部的代码

    - 创建执行上下文对象

      ```js
      fn.ExecutionContext = {
        variableObject:  // 函数中的 arguments、参数、局部成员
        scopeChains:  // 当前函数所在的父级作用域中的活动对象
        this: {}			// 当前函数内部的 this 指向
      }
      ```

    function fn() {}

    - this 指向复习
      - fn() 直接调用，如果是非严格模式  this 指向 window，如果是严格模式this指向 undefined
      - obj.fn()  如果是函数调用，谁调用this指向谁
      - 构造函数中的 this ，指向的是当前创建的对象
      - 箭头函数中的this 指向父级作用域 中的this
      - 改变this的情况。。bind  call  apply

  - 函数执行阶段

    ```js
    // 把变量对象转换为活动对象
    fn.ExecutionContext = {
      activationObject:  // 函数中的 arguments、参数、局部成员
      scopeChains:  // 当前函数所在的父级作用域中的活动对象
      this: {}			// 当前函数内部的 this 指向
    }
    ```

- [[Scopes]] 作用域链，函数在创建时就会生成该属性，js 引擎才可以访问。这个属性中存储的是所有父级中的活动对象

```js
function fn (a, b) {
  function inner () {
    console.log(a, b)
  }
  console.dir(inner)
  // return inner
}
console.dir(fn)
const f = fn(1, 2)
```



## 2.[闭包](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Closures)

- https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Closures

- 发生闭包的两个必要条件

  1. 外部对一个函数 makeFn 内部有引用
  2. 在另一个作用域能够访问到 makeFn 作用域内部的局部成员

  > 使用闭包可以突破变量作用域的限制，原来只能从一个作用域访问外部作用域的成员
  >
  > 有了闭包之后，可以在外部作用域访问一个内部作用域的成员
  >
  > 可以缓存参数
  >
  > 根据不同参数生成不同功能的函数
  >
  > 

```js
function makeFn () {
  let name = 'MDN'
  return function inner () {
    console.log(name)
  }
}

let fn = makeFn()
fn()

fn = null

```

- 缓存参数

```js
function createPatch (obj) {
  return function patch (vdom1, vdom2) {
    ..
  }
}

const patch = createPatch(...)
              
                          
function makeAdder(x) {
  return function(y) {
    return x + y;
  };
}

var add5 = makeAdder(5);
var add10 = makeAdder(10);

console.log(add5(2));  // 7
console.log(add10(2)); // 12
```



