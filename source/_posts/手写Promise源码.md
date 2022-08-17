---
title: 手写Promise源码
author: 5coder
tags: 
  - Promise 
  - Review
category: 大前端
abbrlink: 33976
date: 2021-05-19 22:32:14
password:
keywords:
top:
cover:
---

```js
/*
@Author: 5coder
@Data: 2022-08-16 
@Descriptions: 07.手写Promise源码
@Product: WebStorm
*/

/*
  1. Promise就是一个类，在执行这个类的时候，需要传递一个执行器进去，执行器就会立即执行executor
    执行器executor会有两个参数resolve和reject方法
  2. Promise中有三种状态，分别为：成功-fulfilled， 失败-rejected， 等待-pending
  3.状态只能有pending转换为另外两种
    pending -> fulfilled
    pending -> rejected
  4.resolve和reject函数是用来更改状态的
    resolve：fulfilled
    reject： rejected
  5.then方法内部做的事情就是判断状态，如果状态是成功，就调用成功的回调函数（successCallback），如果状态是失败，就调用失败回调函数（failCallback）
  6.then成功回调有一个参数（value），表示成功之后的值；then失败回调有一个参数，表示失败之后的值（reason）
*/

const PENDING = 'pending'  // 等待
const FULFILLED = 'fulfilled'  // 成功
const REJECTED = 'rejected'  // 失败

class MyPromise {
  // 需要传入执行器，并且立即执行
  constructor(executor) {
    try {
      executor(this.resolve, this.reject)
    } catch (e) {
      this.reject(e)
    }
  }

  status = PENDING  // promise状态默认为等待
  value = undefined  // 成功之后的值
  reason = undefined  // 失败之后的原因
  successCallback = []  // 成功回调
  failCallback = []  // 失败回调

  resolve = value => {
    // 如果状态不是等待，组织程序向下执行
    // 将状态更改为成功
    if (this.status !== PENDING) return
    this.status = FULFILLED
    // 保存成功之后的值
    this.value = value
    // 成功回调是否存在，如果存在就调用--异步情况
    // this.successCallback && this.successCallback(this.value)
    while (this.successCallback.length) this.successCallback.shift()()
  }

  reject = reason => {
    // 如果状态不是等待，组织程序向下执行
    if (this.status !== PENDING) return
    // 将状态更改为失败
    this.status = REJECTED
    // 保存失败之后的值
    this.reason = reason
    // 失败回调是否存在，如果存在就调用--异步情况
    // this.failCallback && this.failCallback(reason)
    while (this.failCallback.length) this.failCallback.shift()()
  }

  then(successCallback, failCallback) {
    successCallback = successCallback ? successCallback : value => value
    failCallback = failCallback ? failCallback : reason => {
      throw reason
    }
    let promise2 = new MyPromise((resolve, reject) => {
      if (this.status === FULFILLED) {
        // 使用setTimeOut是因为在这里不能直接获取到promise2，需要等待同步代码执行完成之后，promise2被赋值后，在异步代码中进行获取
        setTimeout(() => {
          try {
            // 成功回调
            let x = successCallback(this.value)
            // 判断x的值是普通纸还是promise对象
            // 如果是普通值，直接调用resolve
            // 如果是promise对象，查看promise对象返回的结果，再根据promise对象返回的结果，决定调用resolve还是reject
            resolvePromise(promise2, x, resolve, reject)
          } catch (e) {
            reject(e)
          }
        }, 0)
      } else if (this.status === REJECTED) {
        // 失败回调
        setTimeout(() => {
          try {
            // 失败回调
            let x = failCallback(this.reason)
            // 判断x的值是普通纸还是promise对象
            // 如果是普通值，直接调用resolve
            // 如果是promise对象，查看promise对象返回的结果，再根据promise对象返回的结果，决定调用resolve还是reject
            resolvePromise(promise2, x, resolve, reject)
          } catch (e) {
            reject(e)
          }
        }, 0)
      } else {
        // 如果是等待状态，状态为pending，--异步情况
        // 将成功回调和失败回调存储下来
        this.successCallback.push(() => {
          setTimeout(() => {
            try {
              // 成功回调
              let x = successCallback(this.value)
              // 判断x的值是普通纸还是promise对象
              // 如果是普通值，直接调用resolve
              // 如果是promise对象，查看promise对象返回的结果，再根据promise对象返回的结果，决定调用resolve还是reject
              resolvePromise(promise2, x, resolve, reject)
            } catch (e) {
              reject(e)
            }
          }, 0)
        })
        this.failCallback.push(() => {
          setTimeout(() => {
            try {
              // 失败回调
              let x = failCallback(this.reason)
              // 判断x的值是普通纸还是promise对象
              // 如果是普通值，直接调用resolve
              // 如果是promise对象，查看promise对象返回的结果，再根据promise对象返回的结果，决定调用resolve还是reject
              resolvePromise(promise2, x, resolve, reject)
            } catch (e) {
              reject(e)
            }
          }, 0)
        })
      }
    })
    return promise2
  }

  finally(callback) {
    return this.then(value => {
      return MyPromise.resolve(callback()).then(() => value)
    }, reason => {
      return MyPromise.resolve(callback()).then(() => {
        throw reason
      })
    })
  }

  catch(failCallback) {
    return this.then(undefined, failCallback)
  }

  static all(array) {
    let result = []
    let index = 0
    return new MyPromise((resolve, reject) => {
      function addData(key, value) {
        result[key] = value
        index++
        if (index === array.length) {
          resolve(result)
        }
      }

      for (let i = 0; i < array.length; i++) {
        let current = array[i]
        // 判断是普通值还是promise对象
        if (current instanceof MyPromise) {
          // promise对象
          current.then(value => {
            addData(i, value)
          }, reason => reject(reason))
        } else {
          // 普通值
          addData(i, array[i])
        }
      }
    })
  }

  static resolve(value) {
    // 如果是promise对象，直接返回
    if (value instanceof MyPromise) return value
    return new MyPromise(resolve => resolve(value))
  }


}

function resolvePromise(promise2, x, resolve, reject) {
  if (promise2 === x) {
    return reject(new TypeError("Chaining cycle detected for promise #<Promise>"))
  }
  if (x instanceof MyPromise) {
    // promise对象
    // x.then(value => resolve(value), reason => reject(reason))
    x.then(resolve, reject)
  } else {
    // 普通值
    resolve(x)
  }
}

module.exports = MyPromise
```

