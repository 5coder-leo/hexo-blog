title: Vue.js 源码剖析-虚拟DOM
author: 5coder
tags: Vue虚拟DOM
category: 大前端
keywords: Vue源码-虚拟DOM
abbrlink: 23019
date: 2021-07-09 05:27:00
top:
cover:
---
# Vue.js 源码剖析-虚拟DOM

------

# 响应式原理回顾

- Vue初始化过程
- Vue中静态成员和实例成员初始化的过程
- 首次渲染过程
- 响应式实现过程

# 虚拟DOM回顾

## 什么是虚拟DOM

虚拟DOM(Virtual DOM)是使用JavaScript对象来描述DOM，虚拟DOM的本质就是JavaScript对象，使用JavaScript对象来描述DOM的结构。应用的各种状态变化首先作用于虚拟DOM，最终映射到DOM。

Vue.js中的虚拟DOM借鉴了Snabbdom，并添加了一些Vue.js中的特性，例如：指令和组件机制。

Vue1.x中细粒度监测数据的变化，每个属性对应一个watcher，开销太大。Vue2.x中每个组件对应一个watcher，状态变化通知到组件，再引入虚拟DOM进行对比和渲染

## 为什么要使用虚拟DOM

- 使用虚拟DOM，可以避免用户直接操作真实DOM，开发过程关注业务代码的实现，不需要关注如何操作DOM，从而提高开发效率
- 作为一个中间层，可以跨平台，除Web平台外，还支持服务端渲染SSR、Weex框架（跨移动端平台）
- 关于性能方面，在首次渲染的时候肯定不如直接操作DOM，因为要维护一层额外的虚拟DOM对象，如果后续有频繁操作DOM的操作，这个时候可能会有性能的提升，虚拟DOM在更新真实DOM之前会通过Diff算法对比新旧两个虚拟DOM树的差异，组中把差异更新到真实DOM

# Vue.js中的虚拟DOM

- **演示`render`中的`h`函数**

  - `h()`函数就是`createElement()`

  ```js
  const vm = new Vue({
    el: '#app',
    render(h) {
      // h(tag, data, children)
      // render h('h1', this.msg)
      // render h('h1', {domProps: {innerHTML: this.msg}})
      // render h('h1', { attrs: { id: 'title' } }, this.msg)
      const vnode = h(
      	'h1',
        {
          attrs: { id: 'title' }
        },
        this.msg
      )
      console.log(vnode)
      return vnode
    },
    data: {
      msg: 'Hello Vue'
    }
  })
  ```

  ![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210709061932450.png)

- h函数（createElement[官方文档](https://cn.vuejs.org/v2/guide/render-function.html#createElement-%E5%8F%82%E6%95%B0)）

  - `vm.$createElement(tag, data, children, normalizeChildren)`
    - tag
      - 标签名称或者组件对象
    - data
      - 描述tag，可以设置DOM的属性或者标签的属性
    - children
      - tag中的文本内容或者子节点

- VNode

  - VNode的核心属性
    - tag（调用h函数时传入的tag）
    - data（调用h函数时传入的data）
    - children（调用h函数时传入的children）
    - text
    - elm（当VNode转换成真实DOM时，elm记录真实DOM）
    - key（作用是复用当前元素）

## 虚拟DOM创建过程

![整体过程分析](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/整体过程分析.png)

## createElement

### 功能

createElement()函数，用来创建虚拟节点(Vnode)，我们的render函数中的参数h，就是createElement()

```js
render(h) {
  // 此处的h就是vm.$createElement
  renturn h('h1', this.msg)
}
```

### 定义

在vm._render()中调用了，用户传递的或者编译生成的render函数，这个时候传递了createElement

- src/core/instance/render.js

  ```js
    // 对编译生成的 render 进行渲染的方法
    vm._c = (a, b, c, d) => createElement(vm, a, b, c, d, false)
    // normalization is always applied for the public version, used in
    // user-written render functions.
    // 对手写 render 函数进行渲染的方法
    vm.$createElement = (a, b, c, d) => createElement(vm, a, b, c, d, true)
  ```

  *vm._c和vm.createElement内部都调用了createElement，不同的是最后一个参数。vm._c在编译生成的render函数内部会调用，vm.$createElement在用户传入的render函数内部调用。当用户传入render函数的时候，要对用户传入的参数做处理。*

- src/core/vdom/create-element.js

  执行完createElement之后创建好了VNode，把创建好的VNode传递给vm._update()继续处理

  ```js
  // wrapper function for providing a more flexible interface
  // without getting yelled at by flow
  export function createElement (
    context: Component,
    tag: any,
    data: any,
    children: any,
    normalizationType: any,
    alwaysNormalize: boolean
  ): VNode | Array<VNode> {
    // 判断第三个参数
    // 如果data是数组或者原始值的话就是children，实现类似函数重载的机制
    if (Array.isArray(data) || isPrimitive(data)) {
      normalizationType = children
      children = data
      data = undefined
    }
    if (isTrue(alwaysNormalize)) {
      normalizationType = ALWAYS_NORMALIZE
    }
    return _createElement(context, tag, data, children, normalizationType)
  }
  ```

  

  ```js
  export function _createElement (
    context: Component,
    tag?: string | Class<Component> | Function | Object,
    data?: VNodeData,
    children?: any,
    normalizationType?: number
  ): VNode | Array<VNode> {
    if (isDef(data) && isDef((data: any).__ob__)) {
      process.env.NODE_ENV !== 'production' && warn(
    		// 由于MARKDOWN的编译问题，此处将`改为',优化显示，实际使用的是`
        'Avoid using observed data object as vnode data: ${JSON.stringify(data)}\n' +
        'Always create fresh vnode data objects in each render!',
        context
      )
      return createEmptyVNode()
    }
    // <component v-bind:is="currentTabComponent"></component>
    // object syntax in v-bind
    if (isDef(data) && isDef(data.is)) {
      tag = data.is
    }
    if (!tag) {
      // in case of component :is set to falsy value
      return createEmptyVNode()
    }
    // warn against non-primitive key
    if (process.env.NODE_ENV !== 'production' &&
      isDef(data) && isDef(data.key) && !isPrimitive(data.key)
    ) {
      if (!__WEEX__ || !('@binding' in data.key)) {
        warn(
          'Avoid using non-primitive value as key, ' +
          'use string/number value instead.',
          context
        )
      }
    }
    // support single function children as default scoped slot
    if (Array.isArray(children) &&
      typeof children[0] === 'function'
    ) {
      data = data || {}
      data.scopedSlots = { default: children[0] }
      children.length = 0
    }
  	// 去处理children
    if (normalizationType === ALWAYS_NORMALIZE) {
       // 当手写render函数的时候调用
       // 判断children的类型，如果是原始值的话转换成VNode的数组
       // 如果是数组的话，继续处理数组中的元素
       // 如果数组中的子元素又是数组(slot template)，递归处理
  		// 如果连续两个节点都是字符串会合并文本节点
      // 返回一维数组，处理用户手写的 render
      children = normalizeChildren(children)
    } else if (normalizationType === SIMPLE_NORMALIZE) {
      // 把二维数组，转换成一维数组
      // 如果children中有函数组件的话，函数组件会返回数组形式
      // 这时候children就是一个二维数组，只需要把二维数组转换为一维数组
      children = simpleNormalizeChildren(children)
    }
    let vnode, ns
    // 判断tag是字符串还是组件
    if (typeof tag === 'string') {
      let Ctor
      ns = (context.$vnode && context.$vnode.ns) || config.getTagNamespace(tag)
      // 是否是 html 的保留标签
      // 如果是浏览器的保留标签，创建对应的VNode
      if (config.isReservedTag(tag)) {
        // platform built-in elements
        if (process.env.NODE_ENV !== 'production' && isDef(data) && isDef(data.nativeOn)) {
          warn(
            `The .native modifier for v-on is only valid on components but it was used on <${tag}>.`,
            context
          )
        }
        vnode = new VNode(
          config.parsePlatformTagName(tag), data, children,
          undefined, undefined, context
        )
      // 判断是否是 自定义组件
      } else if ((!data || !data.pre) && 
        isDef(Ctor = resolveAsset(context.$options, 'components', tag))) {
        // 查找自定义组件构造函数的声明
        // 根据 Ctor 创建组件的 VNode
        // component
        vnode = createComponent(Ctor, data, context, children, tag)
      } else {
        // unknown or unlisted namespaced elements
        // check at runtime because it may get assigned a namespace when its
        // parent normalizes children
        vnode = new VNode(
          tag, data, children,
          undefined, undefined, context
        )
      }
    } else {
      // direct component options / constructor
      vnode = createComponent(tag, data, context, children)
    }
    if (Array.isArray(vnode)) {
      return vnode
    } else if (isDef(vnode)) {
      if (isDef(ns)) applyNS(vnode, ns)
      if (isDef(data)) registerDeepBindings(data)
      return vnode
    } else {
      return createEmptyVNode()
    }
  }
  ```

## update

### 功能

内部调用vm.__patch__()把虚拟DOM转换成真实DOM

### 定义

- src/core/instance/lifecycle.js

```js
Vue.prototype._update = function (vnode: VNode, hydrating?: boolean) {
  const vm: Component = this
  const prevEl = vm.$el
  const prevVnode = vm._vnode
  const restoreActiveInstance = setActiveInstance(vm)
  vm._vnode = vnode
  // Vue.prototype.__patch__ is injected in entry points
  // based on the rendering backend used.
  if (!prevVnode) {
    // initial render
    vm.$el = vm.__patch__(vm.$el, vnode, hydrating, false /* removeOnly */)
  } else {
    // updates
    vm.$el = vm.__patch__(prevVnode, vnode)
  }
  restoreActiveInstance()
  // update __vue__ reference
  if (prevEl) {
    prevEl.__vue__ = null
  }
  if (vm.$el) {
    vm.$el.__vue__ = vm
  }
  // if parent is an HOC, update its $el as well
  if (vm.$vnode && vm.$parent && vm.$vnode === vm.$parent._vnode) {
    vm.$parent.$el = vm.$el
  }
  // updated hook is called by the scheduler to ensure that children are
  // updated in a parent's updated hook.
}
```

## patch函数初始化

### 功能

对比两个VNode的差异，把差异更新到真实DOM。如果是首次渲染的话，会把真实DOM先转换成VNode

### Snabbdom中path函数的初始化

- src/snabbdom.ts

```typescript
export function init (modules: Array<Partial<Module>>, domApi?: DOMAPI) {
  return function patch (oldVnode: VNode | Element, vnode: VNode): Vnode {}
}
```

- ​	vnode

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

### Vue.js中path函数的初始化

- src/platform/web/runtime/index.js

```js
import { patch } from './patch'

Vue.prototype.__patch__ = inBrowser ? patch : noop
```

- src/platform/web/runtime/patch.js

```js
/* @flow */

import * as nodeOps from 'web/runtime/node-ops'
import { createPatchFunction } from 'core/vdom/patch'
import baseModules from 'core/vdom/modules/index'
import platformModules from 'web/runtime/modules/index'

// the directive module should be applied last, after all
// built-in modules have been applied.
const modules = platformModules.concat(baseModules)

export const patch: Function = createPatchFunction({ nodeOps, modules })
```

- src/core/vdom/patch.js

```js
export function createPatchFunction (backend) {
  let i, j
  const cbs = {}

  // modules 节点的属性/事件/样式的操作
  // nodeOps 节点操作
  const { modules, nodeOps } = backend

  for (i = 0; i < hooks.length; ++i) {
    // cbs['update'] = []
    cbs[hooks[i]] = []
    for (j = 0; j < modules.length; ++j) {
      if (isDef(modules[j][hooks[i]])) {
        // cbs['update'] = [updateAttrs, updateClass, update...]
        cbs[hooks[i]].push(modules[j][hooks[i]])
      }
    }
  }
  
  ......
  
    // 函数柯里化，让一个函数返回一个函数
  // createPatchFunction({ nodeOps, modules }) 传入平台相关的两个参数

  // core中的createPatchFunction (backend), const { modules, nodeOps } = backend
  // core中方法和平台无关，传入两个参数后，可以在上面的函数中使用这两个参数
  return function patch (oldVnode, vnode, hydrating, removeOnly) {
    ......
  }
}
```

## patch函数执行过程

```js
function patch (oldVnode, vnode, hydrating, removeOnly) {
  // 新的 VNode 不存在
  if (isUndef(vnode)) {
    // 老的 VNode 存在，执行 Destroy 钩子函数
    if (isDef(oldVnode)) invokeDestroyHook(oldVnode)
    return
  }

  let isInitialPatch = false
  const insertedVnodeQueue = []

  // 老的 VNode 不存在
  if (isUndef(oldVnode)) {
    // empty mount (likely as component), create new root element
    isInitialPatch = true
    // 创建新的 VNode
    createElm(vnode, insertedVnodeQueue)
  } else {
    // 新的和老的 VNode 都存在，更新
    const isRealElement = isDef(oldVnode.nodeType)
    // 判断参数1是否是真实 DOM，不是真实 DOM
    if (!isRealElement && sameVnode(oldVnode, vnode)) {
      // 更新操作，diff 算法
      // patch existing root node
      patchVnode(oldVnode, vnode, insertedVnodeQueue, null, null, removeOnly)
    } else {
      // 第一个参数是真实 DOM，创建 VNode
      // 初始化
      if (isRealElement) {
        // mounting to a real element
        // check if this is server-rendered content and if we can perform
        // a successful hydration.
        if (oldVnode.nodeType === 1 && oldVnode.hasAttribute(SSR_ATTR)) {
          oldVnode.removeAttribute(SSR_ATTR)
          hydrating = true
        }
        if (isTrue(hydrating)) {
          if (hydrate(oldVnode, vnode, insertedVnodeQueue)) {
            invokeInsertHook(vnode, insertedVnodeQueue, true)
            return oldVnode
          } else if (process.env.NODE_ENV !== 'production') {
            warn(
              'The client-side rendered virtual DOM tree is not matching ' +
              'server-rendered content. This is likely caused by incorrect ' +
              'HTML markup, for example nesting block-level elements inside ' +
              '<p>, or missing <tbody>. Bailing hydration and performing ' +
              'full client-side render.'
            )
          }
        }
        // either not server-rendered, or hydration failed.
        // create an empty node and replace it
        oldVnode = emptyNodeAt(oldVnode)
      }

      // replacing existing element
      const oldElm = oldVnode.elm
      const parentElm = nodeOps.parentNode(oldElm)

      // create new node
      // 创建 DOM 节点
      createElm(
        vnode,
        insertedVnodeQueue,
        // extremely rare edge case: do not insert if old element is in a
        // leaving transition. Only happens when combining transition +
        // keep-alive + HOCs. (#4590)
        oldElm._leaveCb ? null : parentElm,
        nodeOps.nextSibling(oldElm)
      )

      // update parent placeholder node element, recursively
      if (isDef(vnode.parent)) {
        let ancestor = vnode.parent
        const patchable = isPatchable(vnode)
        while (ancestor) {
          for (let i = 0; i < cbs.destroy.length; ++i) {
            cbs.destroy[i](ancestor)
          }
          ancestor.elm = vnode.elm
          if (patchable) {
            for (let i = 0; i < cbs.create.length; ++i) {
              cbs.create[i](emptyNode, ancestor)
            }
            // #6513
            // invoke insert hooks that may have been merged by create hooks.
            // e.g. for directives that uses the "inserted" hook.
            const insert = ancestor.data.hook.insert
            if (insert.merged) {
              // start at index 1 to avoid re-invoking component mounted hook
              for (let i = 1; i < insert.fns.length; i++) {
                insert.fns[i]()
              }
            }
          } else {
            registerRef(ancestor)
          }
          ancestor = ancestor.parent
        }
      }

      // destroy old node
      if (isDef(parentElm)) {
        removeVnodes([oldVnode], 0, 0)
      } else if (isDef(oldVnode.tag)) {
        invokeDestroyHook(oldVnode)
      }
    }
  }

  invokeInsertHook(vnode, insertedVnodeQueue, isInitialPatch)
  return vnode.elm
}
```

## createElm

把VNode转换成真实DOM，插入到DOM树上

```js
function createElm (
  vnode,
  insertedVnodeQueue,
  parentElm,
  refElm,
  nested,
  ownerArray,
  index
) {
  if (isDef(vnode.elm) && isDef(ownerArray)) {
    // This vnode was used in a previous render!
    // now it's used as a new node, overwriting its elm would cause
    // potential patch errors down the road when it's used as an insertion
    // reference node. Instead, we clone the node on-demand before creating
    // associated DOM element for it.
    vnode = ownerArray[index] = cloneVNode(vnode)
  }

  vnode.isRootInsert = !nested // for transition enter check
  if (createComponent(vnode, insertedVnodeQueue, parentElm, refElm)) {
    return
  }

  const data = vnode.data
  const children = vnode.children
  const tag = vnode.tag
  if (isDef(tag)) {
    if (process.env.NODE_ENV !== 'production') {
      if (data && data.pre) {
        creatingElmInVPre++
      }
      if (isUnknownElement(vnode, creatingElmInVPre)) {
        warn(
          'Unknown custom element: <' + tag + '> - did you ' +
          'register the component correctly? For recursive components, ' +
          'make sure to provide the "name" option.',
          vnode.context
        )
      }
    }

    vnode.elm = vnode.ns
      ? nodeOps.createElementNS(vnode.ns, tag)
      : nodeOps.createElement(tag, vnode)
    setScope(vnode)

    /* istanbul ignore if */
    if (__WEEX__) {
      // in Weex, the default insertion order is parent-first.
      // List items can be optimized to use children-first insertion
      // with append="tree".
      const appendAsTree = isDef(data) && isTrue(data.appendAsTree)
      if (!appendAsTree) {
        if (isDef(data)) {
          invokeCreateHooks(vnode, insertedVnodeQueue)
        }
        insert(parentElm, vnode.elm, refElm)
      }
      createChildren(vnode, children, insertedVnodeQueue)
      if (appendAsTree) {
        if (isDef(data)) {
          invokeCreateHooks(vnode, insertedVnodeQueue)
        }
        insert(parentElm, vnode.elm, refElm)
      }
    } else {
      createChildren(vnode, children, insertedVnodeQueue)
      if (isDef(data)) {
        invokeCreateHooks(vnode, insertedVnodeQueue)
      }
      insert(parentElm, vnode.elm, refElm)
    }

    if (process.env.NODE_ENV !== 'production' && data && data.pre) {
      creatingElmInVPre--
    }
  } else if (isTrue(vnode.isComment)) {
    vnode.elm = nodeOps.createComment(vnode.text)
    insert(parentElm, vnode.elm, refElm)
  } else {
    vnode.elm = nodeOps.createTextNode(vnode.text)
    insert(parentElm, vnode.elm, refElm)
  }
}
```

## patchVnode

# patchVnode(node, oldCh, start, end)

- 如果老节点和新节点相等，直接返回

- 如果新节点有elm属性，并且ownerArray存在

  > 克隆vnode

- 如果占位符相关：pass

- 如果新旧vnode都是静态的，只需要替换`componentInstance`

- 如果`vnode.data`存在并且`data.hook`存在并且`data.hook.prepatch`存在

  > 调用prepatch

- 获取新老节点的子节点：oldCh和ch

- 如果vnode.data存在并且vnode是isPatchable

  - 调用cbs中的钩子函数，操作节点的属性/样式/事件
  - 调用用户自定义钩子

- 如果新节点没有文本

  - 如果老节点的子节点和新节点的子节点存在

    - 如果老节点的子节点不等于新节点的子节点
      - 调用updateChildren

  - 如果新的有子节点，老的没有子节点

    - 判断环境是否为开发环境
      - 如果为开发环境，检查key值得重复情况
    - 如果老节点存在text
      - 先清空老节点DOM的文本内容，然后为当前DOM节点加入子节点
    - 调用addVnodes

  - 如果老节点有子节点，新节点没有子节点

    - 清空老节点中的文本内容

  - 新老节点都有文本节点

    - 修改文本

  - 如果data存在

    - 如果data.hook存在并且data.hook.postpatch存在，调用data.hook.postpatch()

```js
function patchVnode (
  oldVnode,
  vnode,
  insertedVnodeQueue,
  ownerArray,
  index,
  removeOnly
) {
  if (oldVnode === vnode) {
    return
  }

  if (isDef(vnode.elm) && isDef(ownerArray)) {
    // clone reused vnode
    vnode = ownerArray[index] = cloneVNode(vnode)
  }

  const elm = vnode.elm = oldVnode.elm

  if (isTrue(oldVnode.isAsyncPlaceholder)) {
    if (isDef(vnode.asyncFactory.resolved)) {
      hydrate(oldVnode.elm, vnode, insertedVnodeQueue)
    } else {
      vnode.isAsyncPlaceholder = true
    }
    return
  }

  // reuse element for static trees.
  // note we only do this if the vnode is cloned -
  // if the new node is not cloned it means the render functions have been
  // reset by the hot-reload-api and we need to do a proper re-render.
  // 如果新旧 VNode 都是静态的，那么只需要替换componentInstance
  if (isTrue(vnode.isStatic) &&
    isTrue(oldVnode.isStatic) &&
    vnode.key === oldVnode.key &&
    (isTrue(vnode.isCloned) || isTrue(vnode.isOnce))
  ) {
    vnode.componentInstance = oldVnode.componentInstance
    return
  }

  let i
  const data = vnode.data
  if (isDef(data) && isDef(i = data.hook) && isDef(i = i.prepatch)) {
    i(oldVnode, vnode)
  }

  const oldCh = oldVnode.children
  const ch = vnode.children
  if (isDef(data) && isPatchable(vnode)) {
    // 调用 cbs 中的钩子函数，操作节点的属性/样式/事件....
    for (i = 0; i < cbs.update.length; ++i) cbs.update[i](oldVnode, vnode)
    // 用户的自定义钩子
    if (isDef(i = data.hook) && isDef(i = i.update)) i(oldVnode, vnode)
  }

  // 新节点没有文本
  if (isUndef(vnode.text)) {
    // 老节点和老节点都有有子节点
    // 对子节点进行 diff 操作，调用 updateChildren
    if (isDef(oldCh) && isDef(ch)) {
      if (oldCh !== ch) updateChildren(elm, oldCh, ch, insertedVnodeQueue, removeOnly)
    } else if (isDef(ch)) {
      // 新的有子节点，老的没有子节点
      if (process.env.NODE_ENV !== 'production') {
        checkDuplicateKeys(ch)
      }
      // 先清空老节点 DOM 的文本内容，然后为当前 DOM 节点加入子节点
      if (isDef(oldVnode.text)) nodeOps.setTextContent(elm, '')
      addVnodes(elm, null, ch, 0, ch.length - 1, insertedVnodeQueue)
    } else if (isDef(oldCh)) {
      // 老节点有子节点，新的没有子节点
      // 删除老节点中的子节点
      removeVnodes(oldCh, 0, oldCh.length - 1)
    } else if (isDef(oldVnode.text)) {
      // 老节点有文本，新节点没有文本
      // 清空老节点的文本内容
      nodeOps.setTextContent(elm, '')
    }
  } else if (oldVnode.text !== vnode.text) {
    // 新老节点都有文本节点
    // 修改文本
    nodeOps.setTextContent(elm, vnode.text)
  }
  if (isDef(data)) {
    if (isDef(i = data.hook) && isDef(i = i.postpatch)) i(oldVnode, vnode)
  }
}
```

## updateChildren

updateChildren和Snabbdom中的updateChildren整体算法一致，这里不再展开了。我们再来看下它处理过程中key的作用，在patch函数中，调用patchVnode之前，会首先调用sameVnode()判断当前的辛劳VNode是否是相同节点，sameVnode()中首先判断key是否相同。

- 通过下面代码来体会key的作用

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>key</title>
  </head>
  <body>
    <div id="app">
      <button @click="handler">按钮</button>
      <ul>
        <li v-for="value in arr" :key="value">{{value}}</li>
      </ul>
    </div>
    <script src="../../dist/vue.js"></script>
    <script>
      const vm = new Vue({
        el: '#app',
        data: {
          arr: ['a', 'b', 'c', 'd']
        },
        methods: {
          handler () {
            this.arr.splice(1, 0, 'x')
            // this.arr = ['a', 'x', 'b', 'c', 'd']
          }
        }
      })
    </script>
  </body>
  </html>
  ```

- 当没有设置key的时候

  - 在updateChildren中比较子节点的时候，会做三次更新DOM操作和一次插入DOM的操作

- 当设置key的时候

  - 在updateChildren中比较子节点的时候，因为oldVnode的子节点的b,c,d和newVnode的x,b,c的key相同，所以只做比较，没有更新DOM的操作，当遍历完毕后，会再把x插入到DOM上，DOM操作只有一次插入操作。

## 总结

![整体过程分析](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/整体过程分析.png)