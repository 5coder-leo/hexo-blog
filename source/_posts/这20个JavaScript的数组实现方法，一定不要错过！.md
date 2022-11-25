---
title: 这20个JavaScript的数组实现方法，一定不要错过！
author: 5coder
tags: JavaScript
category: JavaScript
abbrlink: 62254
date: 2022-11-25 23:29:14
password:
keywords:
top:
cover:
---

# **写在前面**

我想，大家一定对JavaScript中的数组很熟悉了，我们每天都会用到它的各种方法，比如push、pop、forEach、map……等等。

但是仅仅使用它就足够了吗？如果你想成为出色的程序员，你一定不想停在熟悉使用阶段这里，你肯定想进一步挑战自己，走向更高的水平。

因此，今天我为大家准备了20个JavaScript的数组实现方法，如果你还不知道怎么实现它们的话，请一定不要错过今天的内容。

## **1.forEach**

forEach 是我们工作中非常常用的数组方法，实现起来也比较简单，这是我们需要完成的第一个功能。

代码如下：

```js
Array.prototype.forEach2 = function (callback, thisCtx) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }

  const length = this.length
  let i = 0

  while (i < length) {
    // Deleted, the newly added element index i is not in the array, so it will not be accessed
    if (this.hasOwnProperty(i)) {
      callback.call(thisCtx, this[ i ], i, this)
    }

    i++
  }
}
```

测试一下：

```js
let demoArr = [ 1, 2, 3, 4, , 5 ]

demoArr.forEach2((it, i) => {
  if (i === 1) {
    // 5 will not be printed out
    demoArr.push(5)
  } else if (i === 2) {
    // 4 will not be printed out, but "4-4" will be printed out
    demoArr.splice(3, 1, '4-4')
  }

  console.log(it)
})

/*
 1
 2
 3
 4-4
 5
*/
```

哇，恭喜！我们已经实现了 forEach 的功能。

## **2.map**

你一般用map做什么？大多数时候是将一个数组转换为另一个数组。

代码如下：

```js
Array.prototype.map2 = function (callback, thisCtx) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }

  const length = this.length
  let i = 0
  // The return value of the map method is a new array
  let newArray = []

  while (i < length) {
    // Deleted and uninitialized values will not be accessed
    if (this.hasOwnProperty(i)) {
      newArray.push(callback.call(thisCtx, this[ i ], i, this))
    }

    i++
  }
  // Return new array
  return newArray
}
```

测试一下：

```js
let arr = [ 0, 1, 2, 3, 4,, 5 ]

let arr2 = arr.map2(function (it, i, array) {
  console.log(it, i, array, this)
  return it * it
}, { name: 'fatfish' })

console.log(arr2) // [0, 1, 4, 9, 16, 25]
```

朋友们，你们觉得不难吗？是不是很简单？我们接着看后面的内容。

## **3.every**

every() 方法测试数组中的所有元素是否通过提供的函数实现的测试，它返回一个布尔值。

每种方法都有你以前可能没有注意到的三点，它们是什么？

- 在空数组上调用 every 方法将返回 true。
- 回调方法只会被已经赋值的索引调用。
- 如果值被删除，回调将不会被调用。

```js
let emptyArr = []
// Calling every method on an empty array returns true
console.log(emptyArr.every((it) => it > 0)) // true
// The `callback` method will only be called by an index that has already been assigned a value.
let arr = [ 0, 1, 2, 3, 4,, 5, -1 ]
// The `callback` method will not be called when an array value is deleted or an index that has never been assigned a value.
delete arr[7]

console.log(arr.every((it) => it >= 0)) // true
```

代码如下：

```js
Array.prototype.every2 = function (callback, thisCtx) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }

  const length = this.length
  let i = 0
  // If the length of the array is 0, the while loop will not be entered
  while (i < length) {
    // False will be returned as long as a value does not conform to the judgment of callback
    if (this.hasOwnProperty(i) && !callback.call(thisCtx, this[ i ], i, this)) {
      return false
    }

    i++
  }

  return true
}
```

测试一下：

```js
let emptyArr = []
// Calling every method on an empty array returns true
console.log(emptyArr.every2((it) => it > 0)) // true
// The `callback` method will only be called by an index that has already been assigned a value.
let arr = [ 0, 1, 2, 3, 4,, 5, -1 ]
// The `callback` method will not be called when an array value is deleted or an index that has never been assigned a value.
delete arr[7]

console.log(arr.every2((it) => it >= 0)) // true
```

## **4.some**

some() 方法测试数组中的至少一个元素是否通过了提供的函数实现的测试。

代码如下：

```js
Array.prototype.some2 = function (callback, thisCtx) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }

  const length = this.length
  let i = 0

  while (i < length) {
    // Returns true if any element meets the callback condition
    if (this.hasOwnProperty(i) && callback.call(thisCtx, this[ i ], i, this)) {
      return true
    }

    i++
  }

  return false
}
```

测试一下：

```js
let emptyArr = []
// An empty array will return false
console.log(emptyArr.some2((it) => it > 0)) // false

let arr = [ 0, 1, 2, 3, 4,, 5, -1 ]

delete arr[7]

console.log(arr.some2((it) => it < 0)) // false
console.log(arr.some2((it) => it > 0)) // true
```

## **5.filter**

filter() 方法创建一个新数组，其中，包含所有通过所提供函数实现的测试的元素。

```js
Array.prototype.filter2 = function (callback, thisCtx) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }

  const length = this.length
  // The return value will be a new array
  let newArray = []
  let i = 0

  while (i < length) {
    if (this.hasOwnProperty(i) && callback.call(thisCtx, this[ i ], i, this)) {
      newArray.push(this[ i ])
    }
    i++
  }

  return newArray
}
```

测试一下：

```js
// The position with index 5 will not be traversed because it has no initialization value
let arr = [ 0, 1, 2, -3, 4,, 5 ]
// we try to remove the last element
delete arr[6]
// filter out values greater than 0
let filterArr = arr.filter2((it) => it > 0)

console.log(filterArr) // [ 1, 2, 4 ]
```

## **6.reduce**

这个函数稍微复杂一些，让我们用一个例子来看看它是如何使用的。

```js
const sum = [1, 2, 3, 4].reduce((prev, cur) => {
  return prev + cur;
})

console.log(sum) // 10

// initialization
prev = initialValue = 1, cur = 2

// step 1
prev = (1 + 2) =  3, cur = 3

// step 2
prev = (3 + 3) =  6, cur = 4

// step 3
prev = (6 + 4) =  10, cur = undefined (quit)
```

代码如下：

```js
Array.prototype.reduce2 = function (callback, initValue) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }

  let pre = initValue
  let i = 0
  const length = this.length
  // When the initial value is not passed, use the first value of the array as the initial value  
  if (typeof pre === 'undefined') {
    pre = this[0]
    i = 1
  }

  while (i < length) {
    if (this.hasOwnProperty(i)) {
      pre = callback(pre, this[ i ], i, this)
    }
    i++
  }

  return pre
}
```

测试一下：

```js
const sum = [1, 2, 3, 4].reduce2((prev, cur) => {
  return prev + cur;
})
console.log(sum) // 10
```

## **7.reduceRight**

reduceRight() 方法对累加器和数组的每个值（从右到左）应用一个函数，以将其减少为单个值。

它与 reduce 非常相似，只是 reduceRight 从右到左遍历。

```js
const sum = [1, 2, 3, 4].reduce((prev, cur) => {
  console.log(prev, cur)
  return prev + cur;
})
// 1 2
// 3 3
// 6 4

console.log(sum) // 10
const sum2 = [1, 2, 3, 4].reduceRight((prev, cur) => {
  console.log(cur)
  return prev + cur;
})
// 4 3
// 7 2
// 9 1
console.log(sum2) // 10
```

代码如下：

```js
Array.prototype.reduceRight2 = function (callback, initValue) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }
  let pre = initValue
  const length = this.length
  // Start with the last element
  let i = length - 1
  // If no initial value is passed, the last element is taken as the initial value
  if (typeof pre === 'undefined') {
    pre = this[i]
    i--
  }
  while (i >= 0) {
    if (this.hasOwnProperty(i)) {
      pre = callback(pre, this[ i ], i, this)
    }
    i--
  }
  return pre
}
```

测试一下：

```js
const sum = [1, 2, 3, 4].reduceRight2((prev, cur) => {
  console.log(cur)
  return prev + cur;
})
// 4 3
// 7 2
// 9 1
console.log(sum) // 10
```

## **8.find**

find() 方法返回提供的数组中满足提供的测试功能的第一个元素，如果没有值满足测试函数，则返回 undefined。

代码如下：

```js
Array.prototype.find2 = function (callback, thisCtx) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }
  const length = this.length
  let i = 0
  while (i < length) {
    const value = this[ i ]
    // As long as there is an element that matches the logic of the callback function, the element value is returned
    if (callback.call(thisCtx, value, i, this)) {
      return value
    }
    i++
  }
  // otherwise return undefined  
  return undefined
}
```

测试一下

```js
let arr = [ 0, 1, 2, 3, 4,, 5 ]
let ele = arr.find2(function (it, i, array) {
  console.log(it, i, array, this)
  return it > 3
}, { name: 'fatfish' })
console.log(ele) // 4
```

## **9.findIndex**

findIndex() 方法返回数组中满足提供的测试函数的第一个元素的索引。否则，它返回 -1，表示没有元素通过测试。

```js
let arr = [ 0, 1, 2, 3, 4,, 5 ]
let index = arr.findIndex((it, i, array) => {
  return it > 2
})
console.log(index) // 3
```

代码如下：

```js
Array.prototype.findIndex2 = function (callback, thisCtx) {
  if (typeof callback !== 'function') {
    throw `${callback} is not a function`
  }
  const length = this.length
  let i = 0
  while (i < length) {
    // Return index i that conforms to callback logic
    if (callback.call(thisCtx, this[ i ], i, this)) {
      return i
    }
    i++
  }
  return -1
}
```

测试一下：

```js
let arr = [ 0, 1, 2, 3, 4,, 5 ]
let index = arr.findIndex2(function (it, i, array) {
  console.log(it, i, array, this)
  return it > 2
}, { name: 'fatfish' })
console.log(index) // 3
```

## **10.indexOf**

indexOf() 方法返回可以在数组中找到给定元素的第一个索引，如果不存在，则返回 -1。

```js
arr.indexOf(searchElement[, fromIndex])
```

笔记：

- 如果开始搜索的索引值大于等于数组的长度，则表示不会在数组中进行搜索，返回-1。
- 如果fromIndex为负数，则按照-1表示从最后一个元素开始查找，-2表示从倒数第二个元素开始查找的规则进行查找，以此类推。
- 如果 fromIndex 为负数，则仍然从前向后搜索数组。

```js
const array = [2, 5, 9]
console.log(array.indexOf(2))      // 0
console.log(array.indexOf(7))      // -1
console.log(array.indexOf(9, 2))   // 2
console.log(array.indexOf(2, -1))  // -1
console.log(array.indexOf(2, -3))  // 0
console.log(array.indexOf(2, -4))  // 0
```

代码如下：

```js
Array.prototype.indexOf2 = function (targetEle, fromIndex) {
  const length = this.length
  fromIndex = +fromIndex || 0
  // If the array is empty or the search starts from a place greater than or equal to the length of the array, it will directly return -1
  if (length === 0 || fromIndex >= length) {
    return -1
  }
  /*
    1. Search elements from fromIndex
    2. Use it directly when fromindex is greater than 0
    3. If it is less than 0, first subtract the absolute value of fromIndex from the length. If it is still less than 0, take 0 directly
  */
  let i = Math.max(fromIndex >= 0 ? fromIndex : length - Math.abs(fromIndex), 0)
  while (i < length) {
    // element in the array and equal to targetEle
    if (this.hasOwnProperty(i) && targetEle === this[ i ]) {
      return i
    }
    i++
  }
  return -1
}
```

测试一下：

```js
const array = [2, 5, 9]
console.log(array.indexOf2(2))      // 0
console.log(array.indexOf2(7))      // -1
console.log(array.indexOf2(9, 2))   // 2
console.log(array.indexOf2(2, -1))  // -1
console.log(array.indexOf2(2, -3))  // 0
console.log(array.indexOf2(2, -4))  // 0
```

## **11.lastIndexOf**

lastIndexOf() 方法返回可以在数组中找到给定元素的最后一个索引，如果不存在，则返回 -1，从 fromIndex 开始向后搜索数组。

它与 indexOf 非常相似，只是 lastIndexOf 从右到左遍历。

```js
let array = [2, 5, 9, 2]
console.log(array.lastIndexOf(2)) // 3
console.log(array.lastIndexOf(7)) // -1
console.log(array.lastIndexOf(2, 3)) // 3
console.log(array.lastIndexOf(2, 2)) // 0
console.log(array.lastIndexOf(2, -2)) // 0
console.log(array.lastIndexOf(2, -1)) // 3
```

代码如下：

```js
Array.prototype.lastIndexOf2 = function (targetEle, fromIndex) {
  const length = this.length
  fromIndex = typeof fromIndex === 'undefined' ? length - 1 : fromIndex
  // // Empty array, when fromIndex is negative and the absolute value is greater than the length of the array, the method returns -1, that is, the array will not be searched.
  if (length === 0 || fromIndex < 0 && Math.abs(fromIndex) >= length) {
    return -1
  }
  let i
  if (fromIndex >= 0) {
    // If `fromIndex` is greater than or equal to the length of the array, the entire array is searched.
    i = Math.min(fromIndex, length - 1)
  } else {
    i = length - Math.abs(fromIndex)
  }
  while (i >= 0) {
    // Returns the index when it is equal to targetEle
    if (i in this && targetEle === this[ i ]) {
      return i
    }
    i--
  }
  // Returns -1 when the current value is not found
  return -1
}
```

测试一下：

```js
let array = [2, 5, 9, 2]
console.log(array.lastIndexOf2(2)) // 3
console.log(array.lastIndexOf2(7)) // -1
console.log(array.lastIndexOf2(2, 3)) // 3
console.log(array.lastIndexOf2(2, 2)) // 0
console.log(array.lastIndexOf2(2, -2)) // 0
console.log(array.lastIndexOf2(2, -1)) // 3
```

## **12.includes**

includes() 方法确定数组是否在其条目中包含某个值，根据需要返回 true 或 false。

```js
arr.includes(valueToFind[, fromIndex])
```

笔记：

- include 方法将从 fromIndex 索引开始搜索 valueToFind。
- 如果 fromIndex 为负数，则开始搜索 array.length + fromIndex 的索引。
- 如果数组中存在 NaN，则 [..., NaN] Includes (NaN) 为真。

```js
console.log([1, 2, 3].includes(2))     // true
console.log([1, 2, 3].includes(4))     // false
console.log([1, 2, 3].includes(3, 3))  // false
console.log([1, 2, 3].includes(3, -1)) // true
console.log([1, 2, NaN].includes(NaN)) // true
```

代码如下：

```js
Array.prototype.includes2 = function (targetEle, fromIndex) {
  const length = this.length
  fromIndex = +fromIndex || 0
  if (length === 0 || fromIndex >= length) {
    return false
  }
  // Search for elements from the position of fromIndex
  let i = Math.max(fromIndex >= 0 ? fromIndex : length - Math.abs(fromIndex), 0)
  while (i < length) {
    const value = this[ i ]
    // Please note NaN
    if (targetEle === value || typeof targetEle === 'number' && typeof value === 'number' && isNaN(targetEle) && isNaN(value)) {
      return true
    }
    i++
  }
  return false
}
```

测试一下：

```js
console.log([1, 2, 3].includes2(2))     // true
console.log([1, 2, 3].includes2(4))     // false
console.log([1, 2, 3].includes2(3, 3))  // false
console.log([1, 2, 3].includes2(3, -1)) // true
console.log([1, 2, NaN].includes2(NaN)) // true
```

## **13.push**

push() 方法将一个或多个元素添加到数组的末尾，并返回数组的新长度。

```js
const animals = ['pigs', 'goats', 'sheep']
animals.push('cows')
console.log(animals, animals.length) 
// ["pigs", "goats", "sheep", "cows"], 4
animals.push('chickens', 'cats', 'dogs')
console.log(animals, animals.length) 
// ["pigs", "goats", "sheep", "cows", "chickens", "cats", "dogs"], 7
```

代码如下：

```js
Array.prototype.push2 = function (...pushEles) {
  const pushEleLength = pushEles.length
  const length = this.length
  let i = 0

  while (i < pushEleLength) {
    this[ length + i ] = pushEles[ i ]
    i++
  }
  return this.length
}
```

测试一下：

```js
const animals = ['pigs', 'goats', 'sheep']
animals.push2('cows')
console.log(animals, animals.length) 
// ["pigs", "goats", "sheep", "cows"], 4
animals.push2('chickens', 'cats', 'dogs')
console.log(animals, animals.length) 
// ["pigs", "goats", "sheep", "cows", "chickens", "cats", "dogs"], 7
```

## **14.pop**

pop() 方法从数组中删除最后一个元素并返回该元素，此方法更改数组的长度。

```js
let arr = [ 1, 2 ]
let arr2 = []
console.log(arr.pop(), arr) // 2 [1]
console.log(arr2.pop(), arr2) // undefined []
```

代码如下：

```js
Array.prototype.pop2 = function () {
  const length = this.length
  // If it is an empty array, return undefined
  if (length === 0) {
    return undefined
  }
  const delEle = this[ length - 1 ]
  this.length = length - 1
  return delEle
}
```

测试一下：

```js
let arr = [ 1, 2 ]
let arr2 = []
console.log(arr.pop2(), arr) // 2 [1]
console.log(arr2.pop2(), arr2) // undefined []
```

## **15.unshift**

unshift() 方法将一个或多个元素添加到数组的开头并返回数组的新长度。

笔记：

- 如果传入多个参数调用 unshift 一次，与传入一个参数调用 unshift 多次（例如循环调用）会得到不同的结果。

```js
let arr = [4,5,6]
// Insert multiple elements at once
arr.unshift(1,2,3)
console.log(arr) // [1, 2, 3, 4, 5, 6]
let arr2 = [4,5,6]
// Insert multiple times
arr2.unshift(1)
arr2.unshift(2)
arr2.unshift(3)
console.log(arr2); // [3, 2, 1, 4, 5, 6]
```

代码如下：

```js
Array.prototype.unshift2 = function (...unshiftEles) {
  // With "...", Insert the element to be added in front of the array
  let newArray = [ ...unshiftEles, ...this ]
  let length = newArray.length

  let i = 0
  if (unshiftEles.length === 0) {
    return length
  }
  // Recopy to array
  while (i < length) {
    this[ i ] = newArray[ i ]
    i++
  }

  return this.length
}
```

测试一下：

```js
let arr = [4,5,6]
// Insert multiple elements at once
arr.unshift2(1,2,3)
console.log(arr) // [1, 2, 3, 4, 5, 6]
let arr2 = [4,5,6]
// Insert multiple times
arr2.unshift2(1)
arr2.unshift2(2)
arr2.unshift2(3)
console.log(arr2); // [3, 2, 1, 4, 5, 6]
```

## **16.shift**

shift() 方法从数组中删除第一个元素并返回该删除的元素，此方法更改数组的长度。

```js
let arr = [ 1, 2 ]
console.log(arr.shift(), arr) // 1 [2]
console.log(arr.shift(), arr) // 2 []
```

代码如下：

```js
Array.prototype.shift2 = function () {
  const length = this.length
  const delValue = this[ 0 ]
  let i = 1
  while (i < length) {
    // Starting from the first element, the following elements move forward one bit
    this[ i - 1 ] = this[ i ]
    i++
  }
  // Set the length of the array
  this.length = length - 1
  // Return deleted value
  return delValue
}
```

测试一下：

```js
let arr = [ 1, 2 ]
console.log(arr.shift2(), arr) // 1 [2]
console.log(arr.shift2(), arr) // 2 []
```

## **17.reverse**

reverse() 方法将数组反转到位，第一个数组元素成为最后一个，最后一个数组元素成为第一个。

```js
const arr = [1, 2, 3]
console.log(arr) // [1, 2, 3]
arr.reverse()
console.log(arr) // [3, 2, 1]
```

代码如下：

```js
Array.prototype.reverse2 = function () {
  let i = 0
  let j = this.length - 1
  while (i < j) {
    [ this[ i ], this[ j ] ] = [ this[ j ], this[ i ] ]
    i++
    j--
  }
  return this
}
```

测试一下：

```js
const arr = [1, 2, 3]
console.log(arr) // [1, 2, 3]
arr.reverse2()
console.log(arr) // [3, 2, 1]
```

## **18.fill**

fill() 方法将数组中的所有元素更改为静态值，从开始索引（默认 0）到结束索引（默认 array.length），它返回修改后的数组。

```js
const array1 = [1, 2, 3, 4];
console.log(array1.fill(0, 2, 4)) // [1, 2, 0, 0]

console.log(array1.fill(5, 1)) // [1, 5, 5, 5]
console.log(array1.fill(6)) // [6, 6, 6, 6]
```

代码如下：

```js
Array.prototype.fill2 = function (value, start, end) {
  const length = this.length
  start = start >> 0
  // The default value of end is length
  end = typeof end === 'undefined' ? length : end >> 0
  // The minimum value of start is 0 and the maximum value is length
  start = start >= 0 ? Math.min(start, length) : Math.max(start + length, 0)
  // The minimum value of end is 0 and the maximum value is length
  end = end >= 0 ? Math.min(end, length) : Math.max(end + length, 0)
  // The element that fills the specified range is value
  while (start < end) {
    this[ start ] = value
    start++
  }
  return this
}
```

测试一下：

```js
const array1 = [1, 2, 3, 4];
console.log(array1.fill2(0, 2, 4)) // [1, 2, 0, 0]

console.log(array1.fill2(5, 1)) // [1, 5, 5, 5]
console.log(array1.fill2(6)) // [6, 6, 6, 6]
```

## **19.concat**

concat() 方法用于合并两个或多个数组，此方法不会更改现有数组，而是返回一个新数组。

```js
let num1 = [[1]]
let num2 = [2, [3]]
let num3=[5,[6]]
let nums = num1.concat(num2) // [[1], 2, [3]]
let nums2 = num1.concat(4, num3) // [[1], 4, 5,[6]]
```

代码如下：

```js
Array.prototype.concat2 = function (...concatEles) {
  const length = concatEles.length
  // The array itself needs to be expanded one layer
  let newArray = [ ...this ]
  let i = 0
  while (i < length) {
    const value = concatEles[ i ]
    Array.isArray(value) ? newArray.push(...value) : newArray.push(value)
    i++
  }
  return newArray
}
```

测试一下：

```js
let num1 = [[1]]
let num2 = [2, [3]]
let num3=[5,[6]]
let nums = num1.concat2(num2) // [[1], 2, [3]]
let nums2 = num1.concat2(4, num3) // [[1], 4, 5,[6]]
```

## **20.join**

join() 方法通过连接数组（或类似数组的对象）中的所有元素创建并返回一个新字符串，用逗号或指定的分隔符字符串分隔，如果数组只有一个项目，则将返回该项目而不使用分隔符。

```js
const elements = ['Fire', 'Air', 'Water']
const elements2 = ['Fire']
console.log(elements.join()) // Fire,Air,Water
console.log(elements.join('')) // FireAirWater
console.log(elements.join('-')) //  Fire-Air-Water
console.log(elements2.join('-')) // Fire
```

代码如下：

```js
Array.prototype.join2 = function (format = ',') {
  const length = this.length
  // Save the last element because it does not participate in the connection of format
  let lastEle = this[ length - 1 ]
  let string = ''
  if (length === 0) {
    return string
  }
  for (i = 0; i < length - 1; i++) {
    string += this[ i ] + format
  }
  return string + lastEle
}
```

测试一下：

```js
const elements = ['Fire', 'Air', 'Water']
const elements2 = ['Fire']
console.log(elements.join2()) // Fire,Air,Water
console.log(elements.join2('')) // FireAirWater
console.log(elements.join2('-')) //  Fire-Air-Water
console.log(elements2.join2('-')) // Fire
```

以上这20个JavaScript的数组实现方法，你学会了吗？有疑问可以在评论去留言分享。
