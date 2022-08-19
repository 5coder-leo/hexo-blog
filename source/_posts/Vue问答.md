---
title: 3-1作业
author: 5coder
tags:
  - Vue响应式
  - Diff
  - VueRouter
  - Snabbdom
category: 大前端(杂识)
abbrlink: 16452
date: 2021-06-18 05:36:40
password:
keywords:
top:
cover:
---

# 一、简单题

> **1、当我们点击按钮的时候动态给 data 增加的成员是否是响应式数据，如果不是的话，如何把新增成员设置成响应式数据，它的内部原理是什么。**

```js
let vm = new Vue({
 el: '#el'
 data: {
  o: 'object',
  dog: {}
 },
 method: {
  clickHandler () {
   // 该 name 属性是否是响应式的
   this.dog.name = 'Trump'
  }
 }
})
```

通过`this.dog.name = 'Trump'`并不是响应式数据，因为在Vue中当吧一个普通的JavaScript对象传入Vue实例作为`data`选项，Vue将便利所有对象的所有`property`，并使用`Object.defineProperty`把这些`property`全部转换为`getter/setter`。Vue无法检测`property`的**添加或移除**。由于Vue会在初始化实例时对`property`执行`getter/setter`转化，所以`property`必须在`data`对象上**存在**才能让Vue将它转换为响应式。

**对于对象**

对于已创建的实例，Vue不允许动态添加跟级别的响应式property。但是，可以使用

`Vue.set(object, propertyName, value)`方法向嵌套对象添加响应式property。例如：

```js
Vue.set(vm.someObject, 'b', 2)
```

还可以使用vm.$set实例方法，这也是Vue.set方法的别名：

```js
this.$set(this.someObject, 'b', 2)
```

当需要为已有对象赋值多个新property，比如使用Object.assign()或_.extend()。但是这样添加到对象的新property不会触发更新。这种情况下，应该使用原对象与要混合进去的对象的property一起创建一个新的对象。

```js
// 代替 Object.assgin(this.someObject, { a: 1, b: 2 })
this.someObject = Object.assgin({}, this.someObject, { a: 1, b: 2 })
```

**对于数组**

Vue不能检测一下数组的变动：

1. 当里利用索引直接设置一个数组项时，例如：`vm.items[indexOfItem] = newValue`
2. 当你修改数组的长度时，例如：`vm.items.length = newLength`

举个例子：

```js
var vm = new Vue({
  data: {
    items: ['a', 'b', 'c']
  }
})
vm.items[1] = 'x'  // 不是响应式的
vm.items.length = 2  // 不是响应式的
```

解决第一类问题（利用数组索引设置一个数组项`vm.items[indexOfItem] = newValue`）：

- ```js
  // Vue.set
  Vue.set(vm.items, indexOfItem, newValue)
  ```

- ```js
  // Array.property.splice
  vm.items.splice(indexOfItem, 1, newValue)
  ```

解决第二类问题（修改数组长度`vm.items.length = newLength`）

- ```js
  vm.items.splice(newLength)
  ```

*数组更新检查*

***变更方法***

- *push()：向尾部添加元素。改变原数组。*
- *pop()：从数组中删除最后一个元素，并返回该元素的值。并重置数组的长度。改变原数组。*
- *shift()：删除**第一个**元素并返回该元素的值，并重置数组的长度。改变原数组。*
- *unshift()：将一个或多个元素添加到数组的**开头**，并返回该数组的**新长度**。改变原数组。*
- *splice()：通过删除或替换现有元素或者原地添加新的元素来修改数组,并以数组形式返回被修改的内容。改变原数组。*
- *sort()：方法用[原地算法](https://en.wikipedia.org/wiki/In-place_algorithm)对数组的元素进行排序，并返回数组。默认排序顺序是在将元素转换为字符串，然后比较它们的UTF-16代码单元值序列时构建的。改变原数组。*
- *reverse()：将数组中元素的位置颠倒，并返回该数组。数组的第一个元素会变成最后一个，数组的最后一个元素变成第一个。改变原数组。*

***替换数组***

*变更方法，顾名思义，会变更调用了这些方法的原始数组。相比之下，也有非变更方法，例如 `filter()`、`concat()` 和 `slice()`。它们不会变更原始数组，而**总是返回一个新数组**。当使用非变更方法时，可以用新数组替换旧数组：*

```js
example1.items = example1.items.filter(function (item) {
  return item.message.match(/Foo/)
})
```

------

> **2.请简述Diff算法的执行过程**

在执行Diff算法的过程就是调用名为`patch`的函数，比较新旧节点。一边比较一边给真实DOM打补丁。`patch`函数接收两个参数：`oldVnode`和`vnode`，分别代表旧节点和新节点。`patch`函数内部会先执行`pre`钩子函数。

执行完成后，使用`isVnode`（函数内部查看`oldVnode`是否有`sel`属性）判断传入的`oldVnode`是否为DOM对象，如果不是vnode，则使用`emptyNodeAt`（函数内部找到`id/class/tagName`，调用`vnode()`函数将其转换为`vnode`对象：`{api.tagName(elm).toLowerCase() + id + c, {}, [], undefined, elm}`）将真实DOM转换为`vnode`对象。

`isVnode`

```typescript
function isVnode (vnode: any): vnode is VNode {
  return vnode.sel !== undefined
}
```

`emptyNodeAt`

```typescript
function emptyNodeAt (elm: Element) {
  const id = elm.id ? '#' + elm.id : ''
  const c = elm.className ? '.' + elm.className.split(' ').join('.') : ''
  return vnode(api.tagName(elm).toLowerCase() + id + c, {}, [], undefined, elm)
}
```

`vnode`

```typescript
export function vnode (sel: string | undefined,
  data: any | undefined,
  children: Array<VNode | string> | undefined,
  text: string | undefined,
  elm: Element | Text | undefined): VNode {
  const key = data === undefined ? undefined : data.key
  return { sel, data, children, text, elm, key }
}
```

接下来使用`sameVnode`（函数内部判断两个`oldVnode`和`vnode`的`key`和`sel`是否都相同，如果都想同则认为是同一个vnode对象）函数判断`oldVnode`和`vnode`是否为同一个`vnode`。

`sameVnode`

```typescript
function sameVnode (vnode1: VNode, vnode2: VNode): boolean {
  return vnode1.key === vnode2.key && vnode1.sel === vnode2.sel
}
```

- 如果为相同节点，则使用`patchVnode`（函数细节在下面讲）函数对比新旧节点差异，并更新到DOM上。

  `patchVnode`

  ```typescript
  function patchVnode (oldVnode: VNode, vnode: VNode, insertedVnodeQueue: VNodeQueue) {
    const hook = vnode.data?.hook
    hook?.prepatch?.(oldVnode, vnode)
    const elm = vnode.elm = oldVnode.elm!
    const oldCh = oldVnode.children as VNode[]
    const ch = vnode.children as VNode[]
    if (oldVnode === vnode) return
    if (vnode.data !== undefined) {
      for (let i = 0; i < cbs.update.length; ++i) cbs.update[i](oldVnode, vnode)
      vnode.data.hook?.update?.(oldVnode, vnode)
    }
    if (isUndef(vnode.text)) {
      if (isDef(oldCh) && isDef(ch)) {
        if (oldCh !== ch) updateChildren(elm, oldCh, ch, insertedVnodeQueue)
      } else if (isDef(ch)) {
        if (isDef(oldVnode.text)) api.setTextContent(elm, '')
        addVnodes(elm, null, ch, 0, ch.length - 1, insertedVnodeQueue)
      } else if (isDef(oldCh)) {
        removeVnodes(elm, oldCh, 0, oldCh.length - 1)
      } else if (isDef(oldVnode.text)) {
        api.setTextContent(elm, '')
      }
    } else if (oldVnode.text !== vnode.text) {
      if (isDef(oldCh)) {
        removeVnodes(elm, oldCh, 0, oldCh.length - 1)
      }
      api.setTextContent(elm, vnode.text!)
    }
    hook?.postpatch?.(oldVnode, vnode)
  }
  ```

  patchVnode函数内部，首先获取vnode中的`hook`钩子函数并执行`prepatch`，然后通过`oldVnode.elm!`获取`elm`属性，并赋值给`vnode.elm`与`elm`，通过`oldVnode.children as Vnode[]`获取老`vnode`子元素列表`oldCh`，通过`vnode.children as Vnode[]`获取新`Vnode`子元素列表`ch`。

  判断`vnode.data`如果不为`undefined`，遍历循环`cbs`并执行`update`钩子函数（`for (let i = 0; i < cbs.update.length; ++i) cbs.update[i](oldVnode, vnode)`）。

  判断`vnode.text`是否为`undefined`

  - 如果为`undefined`，再此判断`oldCh`和`ch`是否为`undefined`
    - 如果`oldCh`和`ch`存在，则判断如果`oldCh`不等于`ch`，执行`updateChildren`函数（下面详解）
    - 如果`oldCh`不存在，`ch`存在
      - 如果`oldVnode.text`存在，使用`api.setTextContent(elm, '')`，设置`elm`的`textContent`内容
      - 调用`addVnodes`添加节点
    - 如果`oldCh`存在，`ch`不存在
      - 调用`removeVnodes`删除老节点
    - 如果`oldVnode.text`存在，设置`elm`的`textContent`内容
  - 如果`vnode.text`不为`undefined`且`oldVnode.text !== vnode.text`
    - 如果`oldCh`存在，使用`removeVnode`删除`oldCh`节点
    - 给elm设置`vnode.text`值

- 如果不为相同节点，

  - 获取`oldVnode`的`elm`属性（`oldVnode.elm!`）并赋值给`elm`

  - 获取`oldVnode`的parent父元素（`api.parentNode(elm) as Node`）

  - 使用`createElm`（函数内部返回**vnode.elm**）函数将elm属性赋值给`vnode.elm`

    `createElm`

    ```typescript
    function createElm (vnode: VNode, insertedVnodeQueue: VNodeQueue): Node {
      // 执行用户设置的init钩子函数
      let i: any
      let data = vnode.data
      if (data !== undefined) {
        const init = data.hook?.init
        if (isDef(init)) {
          init(vnode)
          data = vnode.data
        }
      }
    ```

  - 接下来判断`parent`是否为空，如果不为空，调用`api.insertBefore(parent, vnode.elm!, api.nextSibling(elm))`将其插入到`parent`元素中的兄弟节点（一般为文本节点）之后，然后使用`removeVnodes`函数删除原来的`oldVnode`

    `removeVnode`

    ```typescript
    function removeVnodes (parentElm: Node,
      vnodes: VNode[],
      startIdx: number,
      endIdx: number): void {
      // 参数一：要删除节点的父节点
      // 参数二：要删除的节点
      // 参数三：开始索引
      // 参数四：结束索引
      for (; startIdx <= endIdx; ++startIdx) {
        //
        let listeners: number
        let rm: () => void
        const ch = vnodes[startIdx]
        if (ch != null) {
          if (isDef(ch.sel)) {
            // 内部触发了vnode的destroy钩子函数
            invokeDestroyHook(ch)
            // 防止重复删除DOM元素
            listeners = cbs.remove.length + 1
            // createRmCb高阶函数，内部返回真正删除dom元素的函数
            rm = createRmCb(ch.elm!, listeners)
            // remove钩子函数内部会真正调用rm（删除DOM元素）
            for (let i = 0; i < cbs.remove.length; ++i) cbs.remove[i](ch, rm)
            // 用户是否传入remove钩子函数
            const removeHook = ch?.data?.hook?.remove
            if (isDef(removeHook)) {
              removeHook(ch, rm)
            } else {
              rm()
            }
          } else { // Text node
            api.removeChild(parentElm, ch.elm!)
          }
        }
      }
    }
    ```

接下来遍历`insertVnodeQueue`（保存新插入节点的队列，为了触发钩子函数），执行`create`钩子函数。然后遍历`cbs`中的`post`，调用（`cbs.post[i]()`）post钩子函数。最后返回`vnode`对象。

```typescript
for (i = 0; i < insertedVnodeQueue.length; ++i) {
  insertedVnodeQueue[i].data!.hook!.insert!(insertedVnodeQueue[i])
}
for (i = 0; i < cbs.post.length; ++i) cbs.post[i]()
return vnode
```

# 二、编程题

> **1、模拟 VueRouter 的 hash 模式的实现，实现思路和 History 模式类似，把 URL 中的 # 后面的内容作为路由的地址，可以通过 hashchange 事件监听路由地址的变化。**

 实现思路（构建类图如下）：

- `+ options`
- `+data`
- `+routeMap`
- `+Constructor(Options): VueRouter`
- `_install(Vue): void`
- `+init(): void`
- `+initEvent(): void`
- `+createRouteMap(): void`
- `initComponents(Vue): void`

代码实现地址：https://gitee.com/coder5leo/fed-e-task-03-01/blob/master/codes/vue-router-hash/src/vuerouter/index.js

> **2、在模拟 Vue.js 响应式源码的基础上实现 v-html 指令，以及 v-on 指令。**

 代码实现地址：https://gitee.com/coder5leo/fed-e-task-03-01/tree/master/codes/minivue

> **3、参考 Snabbdom 提供的电影列表的示例，利用Snabbdom 实现类似的效果，如图：**
>
> ![](http://5coder.cn/img/Ciqc1F7zUZ-AWP5NAAN0Z_t_hDY449.png)

代码实现地址：https://gitee.com/coder5leo/fed-e-task-03-01/tree/master/codes/snabbdom-movie

