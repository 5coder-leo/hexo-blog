---
title: Promise对象使用回顾
tags: Promise
category: 大前端
abbrlink: 741
date: 2021-05-19 22:31:14
---

## Promise对象使用回顾

抽象表达：Promise 是JS 中进行异步编程的新的解决方案
具体表达：Promise 是一个构造函数，promise对象用来封装一个异步操作并可以获取其结果

### 1.promise诞生的意义是什么，为什么会有promise?

1. 指定回调函数的方式更加灵活
   **promise之前：必须在启动异步任务前指定**
   **promise：启动异步任务=> 返回promie 对象=> 给promise 对象绑定回调函**
   **数(甚至可以在异步任务结束后指定/多个)**
2. 支持链式调用, 可以解决回调地狱问题
   **什么是回调地狱? 回调函数嵌套调用, 外部回调函数异步执行的结果是嵌套的回调函数执行的条件**
   **回调地狱的缺点? 不便于阅读/ 不便于异常处理**
   **解决方案? promise 链式调用**
   **终极解决方案? async/await**

### 2.promise的Api有哪些?

1. Promise 构造函数: Promise (excutor) {}
2. Promise.prototype.then 方法: (onResolved, onRejected) => {}
3. Promise.prototype.catch 方法: (onRejected) => {}
4. Promise.resolve 方法: (value) => {}
5. Promise.reject 方法: (reason) => {}
6. Promise.all 方法: (promises) => {}
7. Promise.race 方法: (promises) => {}

### 3.Promise基本用法

```js
// Promise 基本示例

const promise = new Promise(function (resolve, reject) {
  // 这里用于“兑现”承诺

  // resolve(100) // 承诺达成

  reject(new Error('promise rejected')) // 承诺失败
})

promise.then(function (value) {
  // 即便没有异步操作，then 方法中传入的回调仍然会被放入队列，等待下一轮执行
  console.log('resolved', value)
}, function (error) {
  console.log('rejected', error)
})

console.log('end')

```

### 4.Promise使用案例

```js
// Promise 方式的 AJAX

function ajax (url) {
  // 返回一个promise对象
  return new Promise(function (resolve, reject) {
    var xhr = new XMLHttpRequest()
    xhr.open('GET', url)
    xhr.responseType = 'json'
    xhr.onload = function () {
      if (this.status === 200) {
        resolve(this.response)
      } else {
        reject(new Error(this.statusText))
      }
    }
    xhr.send()
  })
}

ajax('/api/foo.json').then(function (res) {
  console.log(res)  // ajax请求成功后调用
}, function (error) {
  console.log(error)  // ajax请求失败后调用
})

```

### 5.Promise常见误区

promise最常见的误区的就是嵌套使用：

```js
function ajax(url) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest()
        xhr.open('GET', url)
        xhr.responseType = 'json'
        xhr.onload = function () {
            if (this.status === 200) {
                resolve(this.response)
            } else {
                reject(new Error(this.statusText))
            }
        }
        xhr.send()
    })
}
```

```js
ajax('/api/urls.json').then(function (urls) {
    ajax(urls.users).then(function (users) {
        ajax(urls.users).then(function (users) {
            ajax(urls.users).then(function (users) {
                ajax(urls.users).then(function (users) {

                })
            })
        })
    })
})
```

嵌套使用就失去了Promise通过状态变化获取结果的优势，依然无法获取其中某个回调是否完成的结果。

### 6.Promise链式调用

```js
// Promise 链式调用

function ajax(url) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest()
        xhr.open('GET', url)
        xhr.responseType = 'json'
        xhr.onload = function () {
            if (this.status === 200) {
                resolve(this.response)
            } else {
                reject(new Error(this.statusText))
            }
        }
        xhr.send()
    })
}

// var promise = ajax('/api/users.json')

// var promise2 = promise.then(
//   function onFulfilled (value) {
//     console.log('onFulfilled', value)
//   },
//   function onRejected (error) {
//     console.log('onRejected', error)
//   }
// )

// console.log(promise2 === promise)

ajax('/api/users.json')
    .then(function (value) {
        console.log(1111)
        return ajax('/api/urls.json')
    }) // => Promise
    .then(function (value) {
        console.log(2222)
        console.log(value)
        return ajax('/api/urls.json')
    }) // => Promise
    .then(function (value) {
        console.log(3333)
        return ajax('/api/urls.json')
    }) // => Promise
    .then(function (value) {
        console.log(4444)
        return 'foo'
    }) // => Promise
    .then(function (value) {
        console.log(5555)
        console.log(value)
    })

```

### 7.Promise异常处理

```js
// Promise 异常处理

function ajax (url) {
  return new Promise(function (resolve, reject) {
    // foo()
    // throw new Error()
    var xhr = new XMLHttpRequest()
    xhr.open('GET', url)
    xhr.responseType = 'json'
    xhr.onload = function () {
      if (this.status === 200) {
        resolve(this.response)
      } else {
        reject(new Error(this.statusText))
      }
    }
    xhr.send()
  })
}

// ajax('/api/users11.json')
//   .then(function onFulfilled (value) {
//     console.log('onFulfilled', value)
//   }, function onRejected (error) {
//     console.log('onRejected', error)
//   })

// 使用 catch 注册失败回调是更常见的

// ajax('/api/users11.json')
//   .then(function onFulfilled (value) {
//     console.log('onFulfilled', value)
//   })
//   .catch(function onRejected (error) {
//     console.log('onRejected', error)
//   })

// then(onRejected) 实际上就相当于 then(undefined, onRejected)

// ajax('/api/users11.json')
//   .then(function onFulfilled (value) {
//     console.log('onFulfilled', value)
//   })
//   .then(undefined, function onRejected (error) {
//     console.log('onRejected', error)
//   })

// 同时注册的 onRejected 只是给当前 Promise 对象注册的失败回调
// 它只能捕获到当前 Promise 对象的异常

// ajax('/api/users.json')
//   .then(function onFulfilled (value) {
//     console.log('onFulfilled', value)
//     return ajax('/error-url')
//   }, function onRejected (error) {
//     console.log('onRejected', error)
//   })

// 因为 Promise 链条上的任何一个异常都会被一直向后传递，直至被捕获
// 分开注册的 onRejected 相当于给整个 Promise 链条注册失败回调

ajax('/api/users.json')
  .then(function onFulfilled (value) {
    console.log('onFulfilled', value)
    return ajax('/error-url')
  }) // => Promise {}
  // .catch(function onRejected (error) {
  //   console.log('onRejected', error)
  // })

// 全局捕获 Promise 异常，类似于 window.onerror
window.addEventListener('unhandledrejection', event => {
  const { reason, promise } = event

  console.log(reason, promise)
  // reason => Promise 失败原因，一般是一个错误对象
  // promise => 出现异常的 Promise 对象

  event.preventDefault()
}, false)

// Node.js 中使用以下方式
// process.on('unhandledRejection', (reason, promise) => {
//   console.log(reason, promise)
//   // reason => Promise 失败原因，一般是一个错误对象
//   // promise => 出现异常的 Promise 对象
// })

```

### 8.Promise静态方法

```js
// 常用 Promise 静态方法

function ajax (url) {
  return new Promise(function (resolve, reject) {
    // foo()
    // throw new Error()
    var xhr = new XMLHttpRequest()
    xhr.open('GET', url)
    xhr.responseType = 'json'
    xhr.onload = function () {
      if (this.status === 200) {
        resolve(this.response)
      } else {
        reject(new Error(this.statusText))
      }
    }
    xhr.send()
  })
}

// Promise.resolve('foo')
//   .then(function (value) {
//     console.log(value)
//   })

// new Promise(function (resolve, reject) {
//   resolve('foo')
// })

// 如果传入的是一个 Promise 对象，Promise.resolve 方法原样返回

// var promise = ajax('/api/users.json')
// var promise2 = Promise.resolve(promise)
// console.log(promise === promise2)

// 如果传入的是带有一个跟 Promise 一样的 then 方法的对象，
// Promise.resolve 会将这个对象作为 Promise 执行

// Promise.resolve({
//   then: function (onFulfilled, onRejected) {
//     onFulfilled('foo')
//   }
// })
// .then(function (value) {
//   console.log(value)
// })

// Promise.reject 传入任何值，都会作为这个 Promise 失败的理由

// Promise.reject(new Error('rejected'))
//   .catch(function (error) {
//     console.log(error)
//   })

Promise.reject('anything')
  .catch(function (error) {
    console.log(error)
  })

```

### 9.Promise并行执行

```js
// Promise 并行执行

function ajax (url) {
  return new Promise(function (resolve, reject) {
    // foo()
    // throw new Error()
    var xhr = new XMLHttpRequest()
    xhr.open('GET', url)
    xhr.responseType = 'json'
    xhr.onload = function () {
      if (this.status === 200) {
        resolve(this.response)
      } else {
        reject(new Error(this.statusText))
      }
    }
    xhr.send()
  })
}

// ajax('/api/users.json')
// ajax('/api/posts.json')

// var promise = Promise.all([
//   ajax('/api/users.json'),
//   ajax('/api/posts.json')
// ])

// promise.then(function (values) {
//   console.log(values)
// }).catch(function (error) {
//   console.log(error)
// })

// ajax('/api/urls.json')
//   .then(value => {
//     const urls = Object.values(value)
//     const tasks = urls.map(url => ajax(url))
//     return Promise.all(tasks)
//   })
//   .then(values => {
//     console.log(values)
//   })

// Promise.race 实现超时控制

const request = ajax('/api/posts.json')
const timeout = new Promise((resolve, reject) => {
  setTimeout(() => reject(new Error('timeout')), 500)
})

Promise.race([
  request,
  timeout
])
.then(value => {
  console.log(value)
})
.catch(error => {
  console.log(error)
})

```

### 10.Promise执行时序

```js
// 微任务

console.log('global start')

// setTimeout 的回调是 宏任务，进入回调队列排队
setTimeout(() => {
  console.log('setTimeout')
}, 0)

// Promise 的回调是 微任务，本轮调用末尾直接执行
Promise.resolve()
  .then(() => {
    console.log('promise')
  })
  .then(() => {
    console.log('promise 2')
  })
  .then(() => {
    console.log('promise 3')
  })

console.log('global end')

```

```js
// Promise vs. Callback

function ajax (url, callback) {
  const executor = (resolve, reject) => {
    var xhr = new XMLHttpRequest()
    xhr.open('GET', url)
    xhr.responseType = 'json'
    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve(xhr.response)
      } else {
        reject(new Error(xhr.statusText))
      }
    }
    xhr.send()
  }

  if (typeof callback === 'function') {
    // support callback
    executor(
      res => callback(null, res),
      err => callback(error)
    )
  }

  return new Promise(executor)
}

// ajax('/api/urls.json', (error, value) => {
//   if (error) {
//     return console.error(error)
//   }
//   console.log(value)
// })

// ajax('/api/urls.json')
//   .then(value => {
//     console.log(value)
//   })
//   .catch(error => {
//     console.error(error)
//   })

// Callback hell
ajax('/api/url1', (error, value) => {
  ajax('/api/url2', (error, value) => {
    ajax('/api/url3', (error, value) => {
      ajax('/api/url4', (error, value) => {

      })
    })
  })
})

// Promise chain
ajax('/api/url1')
  .then(value => {
    return ajax('ajax/url2')
  })
  .then(value => {
    return ajax('ajax/url3')
  })
  .then(value => {
    return ajax('ajax/url4')
  })
  .catch(error => {
    console.error(error)
  })

// sync mode code
try {
  const value1 = ajax('/api/url1')
  console.log(value1)
  const value2 = ajax('/api/url2')
  console.log(value2)
  const value3 = ajax('/api/url3')
  console.log(value3)
  const value4 = ajax('/api/url4')
  console.log(value4)
} catch (e) {
  console.error(e)
}

```

### 11.Generator异步方案

```js
// 生成器函数回顾

function * foo () {
  console.log('start')

  try {
    const res = yield 'foo'
    console.log(res)
  } catch (e) {
    console.log(e)
  }
}

const generator = foo()

const result = generator.next()
console.log(result)


// generator.next('bar')

generator.throw(new Error('Generator error'))

```

```js
// Generator 配合 Promise 的异步方案

function ajax (url) {
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest()
    xhr.open('GET', url)
    xhr.responseType = 'json'
    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve(xhr.response)
      } else {
        reject(new Error(xhr.statusText))
      }
    }
    xhr.send()
  })
}

function * main () {
  try {
    const users = yield ajax('/api/users.json')
    console.log(users)

    const posts = yield ajax('/api/posts.json')
    console.log(posts)

    const urls = yield ajax('/api/urls11.json')
    console.log(urls)
  } catch (e) {
    console.log(e)
  }
}

function co (generator) {
  const g = generator()

  function handleResult (result) {
    if (result.done) return // 生成器函数结束
    result.value.then(data => {
      handleResult(g.next(data))
    }, error => {
      g.throw(error)
    })
  }

  handleResult(g.next())
}

co(main)

// const result = g.next()

// result.value.then(data => {
//   const result2 = g.next(data)

//   if (result2.done) return

//   result2.value.then(data => {
//     const result3 = g.next(data)

//     if (result3.done) return

//     result3.value.then(data => {
//       g.next(data)
//     })
//   })
// })

```

### 12.Async方案

```js
// Async / Await 语法糖

function ajax (url) {
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest()
    xhr.open('GET', url)
    xhr.responseType = 'json'
    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve(xhr.response)
      } else {
        reject(new Error(xhr.statusText))
      }
    }
    xhr.send()
  })
}

function co (generator) {
  const g = generator()

  function handleResult (result) {
    if (result.done) return // 生成器函数结束
    result.value.then(data => {
      handleResult(g.next(data))
    }, error => {
      g.throw(error)
    })
  }

  handleResult(g.next())
}

async function main () {
  try {
    const users = await ajax('/api/users.json')
    console.log(users)

    const posts = await ajax('/api/posts.json')
    console.log(posts)

    const urls = await ajax('/api/urls.json')
    console.log(urls)
  } catch (e) {
    console.log(e)
  }
}

// co(main)
const promise = main()

promise.then(() => {
  console.log('all completed')
})

```

本篇主要从代码角度去了解primise，基本用法都写在注释内，若有疑问，欢迎留言