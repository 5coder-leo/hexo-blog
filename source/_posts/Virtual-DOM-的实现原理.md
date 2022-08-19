---
title: Virtual DOM 的实现原理
author: 5coder
tags:
  - Vue
  - Vue响应式原理
category: 大前端
keywords:
  - Virtual DOM
  - Snabbdom
abbrlink: 17380
date: 2021-06-04 05:37:23
top: true
cover:
img: /medias/featureimages/18.jpg
---

# Virtual DOM的实现原理

## 一、Virtual DOM

### 1.课程目标

- 了解什么是虚拟DOM，以及虚拟DOM的作用

- Snabbdom的基本使用

  Vue内部的虚拟DOM改造了一个开源库Snabbdom

- **Snabbdom的源码解析**

### 2.什么是Virtual DOM

- Virtual DOM(虚拟DOM)，是由普通的JS对象来描述DOM对象

- 真实DOM成员

  ```js
  let element = document.querySelector('#app')
  let s = ''
  for (var key in element) {
    s += key + ','
  }
  console.log(s)
  ```

  ```js
  // 打印DIV的所有成员
  align,title,lang,translate,dir,hidden,accessKey,draggable,spellcheck,autocapitalize,contentEditable,isContentEditable,inputMode,offsetParent,offsetTop,offsetLeft,offsetWidth,offsetHeight,style,innerText,outerText,oncopy,oncut,onpaste,onabort,onblur,oncancel,oncanplay,oncanplaythrough,onchange,onclick,onclose,oncontextmenu,oncuechange,ondblclick,ondrag,ondragend,ondragenter,ondragleave,ondragover,ondragstart,ondrop,ondurationchange,onemptied,onended,onerror,onfocus,oninput,oninvalid,onkeydown,onkeypress,onkeyup,onload,onloadeddata,onloadedmetadata,onloadstart,onmousedown,onmouseenter,onmouseleave,onmousemove,onmouseout,onmouseover,onmouseup,onmousewheel,onpause,onplay,onplaying,onprogress,onratechange,onreset,onresize,onscroll,onseeked,onseeking,onselect,onstalled,onsubmit,onsuspend,ontimeupdate,ontoggle,onvolumechange,onwaiting,onwheel,onauxclick,ongotpointercapture,onlostpointercapture,onpointerdown,onpointermove,onpointerup,onpointercancel,onpointerover,onpointerout,onpointerenter,onpointerleave,onselectstart,onselectionchange,onanimationend,onanimationiteration,onanimationstart,ontransitionend,dataset,nonce,autofocus,tabIndex,click,focus,blur,enterKeyHint,onformdata,onpointerrawupdate,attachInternals,namespaceURI,prefix,localName,tagName,id,className,classList,slot,part,attributes,shadowRoot,assignedSlot,innerHTML,outerHTML,scrollTop,scrollLeft,scrollWidth,scrollHeight,clientTop,clientLeft,clientWidth,clientHeight,attributeStyleMap,onbeforecopy,onbeforecut,onbeforepaste,onsearch,elementTiming,previousElementSibling,nextElementSibling,children,firstElementChild,lastElementChild,childElementCount,onfullscreenchange,onfullscreenerror,onwebkitfullscreenchange,onwebkitfullscreenerror,setPointerCapture,releasePointerCapture,hasPointerCapture,hasAttributes,getAttributeNames,getAttribute,getAttributeNS,setAttribute,setAttributeNS,removeAttribute,removeAttributeNS,hasAttribute,hasAttributeNS,toggleAttribute,getAttributeNode,getAttributeNodeNS,setAttributeNode,setAttributeNodeNS,removeAttributeNode,closest,matches,webkitMatchesSelector,attachShadow,getElementsByTagName,getElementsByTagNameNS,getElementsByClassName,insertAdjacentElement,insertAdjacentText,insertAdjacentHTML,requestPointerLock,getClientRects,getBoundingClientRect,scrollIntoView,scroll,scrollTo,scrollBy,scrollIntoViewIfNeeded,animate,computedStyleMap,before,after,replaceWith,remove,prepend,append,querySelector,querySelectorAll,requestFullscreen,webkitRequestFullScreen,webkitRequestFullscreen,createShadowRoot,getDestinationInsertionPoints,ELEMENT_NODE,ATTRIBUTE_NODE,TEXT_NODE,CDATA_SECTION_NODE,ENTITY_REFERENCE_NODE,ENTITY_NODE,PROCESSING_INSTRUCTION_NODE,COMMENT_NODE,DOCUMENT_NODE,DOCUMENT_TYPE_NODE,DOCUMENT_FRAGMENT_NODE,NOTATION_NODE,DOCUMENT_POSITION_DISCONNECTED,DOCUMENT_POSITION_PRECEDING,DOCUMENT_POSITION_FOLLOWING,DOCUMENT_POSITION_CONTAINS,DOCUMENT_POSITION_CONTAINED_BY,DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC,nodeType,nodeName,baseURI,isConnected,ownerDocument,parentNode,parentElement,childNodes,firstChild,lastChild,previousSibling,nextSibling,nodeValue,textContent,hasChildNodes,getRootNode,normalize,cloneNode,isEqualNode,isSameNode,compareDocumentPosition,contains,lookupPrefix,lookupNamespaceURI,isDefaultNamespace,insertBefore,appendChild,replaceChild,removeChild,addEventListener,removeEventListener,dispatchEvent
  ```

  可以看到有很多成员，也就是创建一个dom对象的成本非常高。

- 使用Virtual DOM来描述真实DOM

  创建Virtual DOM的成员很少，创建一个Virtual DOM的开销要比真实的DOM小很多

  ```js
  // 普通的JavaScript对象
  {
    sel: "div",  // 选择器
    data: {},
    children: undefined,
    text: "Hello Virtual DOM",  // dom文本
    elm: undefined,
    key: undefined
  }
  ```

### 3.为什么使用Virtual DOM

- 手动操作DOM比较麻烦，还需要考虑浏览器兼容性问题，虽然jQuery等库简化DOM操作，但随着项目的复杂DOM操作负责提升

  jQuery开发的列表[demo](https://codesandbox.io/s/jq-demo-5i7qp?file=/index.html)，列表有三种功能：增加、排序、删除，三种功能增加渐变效果，在2s之内把透明度从0变为1。通过点击增加、排序、删除按钮，发现页面每次都需要闪烁，其内部是重新渲染所有列表，性能消耗较高

  ![](http://5coder.cn/img/izVHJKWlDroh2tT.gif)

- 为了简化DOM的负责操作，于是出现了各种的MVVM框架，MVVM矿建解决了视图和状态的同步问题

- 为了简化视图的操作，可以使用模板引擎，但是模板引擎没有解决跟踪状态变化的问题，于是Virtual DOM出现了

- Virtual DOM的好处是当状态改变时不需要立即更新DOM，只需要创建一个虚拟树来描述DOM，Virtual DOM内部将弄清楚如何有效(**diff算法**)的更新DOM

  Virtual DOM列表[案例演示](https://codesandbox.io/s/jq-demo-4hbyb?file=/index.html)，可以看到当点击增加时，只有列表第一条在变化，整个页面并没有闪烁。通过Virtual DOM可有效减少DOM操作，Virtual记录上一次状态。

  ![](http://5coder.cn/img/gDTbA1F7hZCS2oz.gif)

- 参考GitHub上[virtual-dom](https://github.com/Matt-Esch/virtual-dom)的描述

  - 虚拟DOM可以维护程序的状态，跟踪上一次的状态
  - 通过比较前后两次状态的差异来更新真实的DOM

### 4.虚拟DOM的作用

- 维护视图和状态的关系
- 负责视图情况下提升渲染性能
- 跨平台
  - 浏览器平台渲染DOM
  - 服务端渲染SSR(Nuxt.js/Next.js)
  - 原生应用(Weex/React Native)
  - 小程序(mpvue/uni-app)等

![](http://5coder.cn/img/5QhHaZcxpKoCDJl.png)

### 5.Virtual DOM库

- [Snabbdom](https://github.com/snabbdom/snabbdom)
  - Vue2.x内部使用的Virtual DOM就是改造的Snabbdom
  - 大约200SLOC（Single Line Of Code）
  - 通过模块可扩展
  - 源码使用TypeScript开发
  - 最快的Virtual DOM之一
- [virtual-dom](https://github.com/Matt-Esch/virtual-dom)

### 6.案例演示

- [jQuery-demo](https://codesandbox.io/s/jq-demo-5i7qp)
- [snabbdom-demo](https://codesandbox.io/s/snabbdom-demo-4hbyb)

## 二、Snabbdom基本使用

### 1.创建项目

- 为了使用简单，使用了 [parcel](https://parceljs.org/getting_started.html)

- 创建项目

  ```bash
  # windows环境，创建项目目录
  md snabbdom-demo
  # 进入项目目录
  cd snabbdom-demo
  # 创建package.json
  yarn init -y
  # 本地安装parcel
  yarn add parcel-bundler
  ```

- 配置package.json的scripts

  ```json
  "scripts": {
      "dev": "parcel index.html --open",
      "build": "parcel bundle index.html"
  }
  ```

- 创建项目目录结构

  ```txt
  │  index.html
  │  package.json
  └─src
       01-basicusage.js
  ```

### 2.导入Snabbdom

#### Snabbdom文档

- 看文档的意义

  - 学习任何一个库都要 先看文档
  - 通过文档了解库的作用
  - 看文档中提供的实例，自己快速实现一个demo
  - 通过文档查看API的使用

- 文档地址

  - https://github.com/snabbdom/snabbdom

  - 当前版本v2.1.0

    ```shell
    # --depth 表示克隆深度, 1 表示只克隆最新的版本. 因为如果项目迭代的版本很多, 克隆会很慢
    git clone -b v2.1.0 --depth=1 https://github.com/snabbdom/snabbdom.git
    ```

#### 安装Snabbdom

- 安装Snabbdom

  ```bash
  npm install snabbdom@2.1.0
  ```

- `Snabbdom`的两个核心函数是`init`和`h()`

  - `init()`是一个高阶函数，返回`patch()`函数
  - `h()`函数返回虚拟节点VNode，这个函数在Vue.js的时候见过

  ```js
  import { init } from 'snabbdom/init'
  import { h } from 'snabbdom/h'
  const patch = init([])  // init()函数接受一个参数为数组
  ```

  > 注意：此时运行的话，项目会报错，提示找不到`init/h`模块，因为模块路径并不是`snabbdom/init`，这个路径是在package.json中的`exports`字段设置的，而我们使用的打包工具不支持`exports`这个字段，webpack4也不支持，webpack5支持该字段。
  >
  > ![](http://5coder.cn/img/fvRIz9ZgeTPwF1c.png)
  >
  > 该字段在导入`snabbdom/init`的时候回补全路径成`snabbdom/build/package/init.js`

  ```json
  "exports": {
      "./init": "./build/package/init.js",
      "./h": "./build/package/h.js",
      "./helpers/attachto": "./build/package/helpers/attachto.js",
      "./hooks": "./build/package/hooks.js",
      "./htmldomapi": "./build/package/htmldomapi.js",
      "./is": "./build/package/is.js",
      "./jsx": "./build/package/jsx.js",
      "./modules/attributes": "./build/package/modules/attributes.js",
      "./modules/class": "./build/package/modules/class.js",
      "./modules/dataset": "./build/package/modules/dataset.js",
      "./modules/eventlisteners": "./build/package/modules/eventlisteners.js",
      "./modules/hero": "./build/package/modules/hero.js",
      "./modules/module": "./build/package/modules/module.js",
      "./modules/props": "./build/package/modules/props.js",
      "./modules/style": "./build/package/modules/style.js",
      "./thunk": "./build/package/thunk.js",
      "./tovnode": "./build/package/tovnode.js",
      "./vnode": "./build/package/vnode.js"
    }
  ```

- 如果使用不支持package.json的exports字段的打包工具，我们应该把模块路径写全

  - 查看安装的snabbdom的目录结构

    ```js
    import { h } from 'snabbdom/build/package/h'
    import { init } from 'snabbdom/build/package/init'
    import { classModule } from 'snabbdom/build/package/modules/class'
    ```

- 回顾Vue中的render函数

  ```js
  new Vue({
  	router,
  	store,
  	render: h => h(App)
  }).$mount('#app')
  ```

### 3.代码演示

案例一：使用`snabbdom`写一个`Hello World`，使用虚拟DOM在`div`中放置纯文本内容“Hello World”。

```js
import {init} from 'snabbdom/build/package/init'
import {h} from 'snabbdom/build/package/h'

// init内部返回patch函数，把虚拟DOM渲染成真实DOM并挂载到DOM树上
const patch = init([])

/*
* h函数创建虚拟DOM，这里创建的是VNode虚拟节点，VNode的作用是用来描述真实DOM
* h函数参数：
* 参数一：标签+选择器，字符串形式
* 参数二：如果是字符串时，代表标签中的文本内容
* 此处创建的vnode div将要替换掉index.html中用来占位的#app的div
* */
let vnode = h('div#container.cls', 'Hello World')
let app = document.querySelector('#app')

/*
* patch函数的作用是对比两个VNode，把两个VNode的差异更新到真实DOM上
* 参数一：旧的 VNode或旧的真实DOM，patch函数内部会将真实DOM转换为VNode
* 参数二：新的 Vnode
* 返回值：返回一个新的Vnode，返回的值回作为下次调用patch函数时的第一个参数，老的VNode
* */
let oldVnode = patch(app, vnode)

```

命令行运行`yarn dev`，查看结果

![](http://5coder.cn/img/Yj5s46tyR73bPZc.png)

再加一个小功能：假设页面上有一个按钮，当点击按钮时，把`id`是`container`的`div`改成Hello Snabbdom，并且更改类样式。

![](http://5coder.cn/img/lb7zgO1VPkB93mY.png)

结果演示：![](http://5coder.cn/img/KV4UkexDc5uRtis.png)

案例二：在`div`中创建两个子元素：`h`和`p`标签。

```js
import {init} from 'snabbdom/build/package/init'
import {h} from 'snabbdom/build/package/h'
const patch = init([])

let vnode = h('div#container', [
  h('h1', 'Hello Snabbdom'),
  h('p', 'Hello p')
])
let app = document.querySelector('#app')

let oldVNode = patch(app, vnode)
```

![](http://5coder.cn/img/luEnD57tcdWOeAs.png)

拓展1：

> 两秒中后更新h标签和p标签中的文本内容

```js
import {init} from 'snabbdom/build/package/init'
import {h} from 'snabbdom/build/package/h'
const patch = init([])

let vnode = h('div#container', [
  h('h1', 'Hello Snabbdom'),
  h('p', 'Hello p')
])
let app = document.querySelector('#app')
let oldVNode = patch(app, vnode)

// 两秒中后更新h标签和p标签中的文本内容
setTimeout(() => {
  vnode = h('div.cls', [
    h('h2', 'Hello World'),
    h('p', '这是段落')
  ])
  // 把老的视图更新到新的状态
  patch(oldVNode, vnode)
}, 2000)
```

![](http://5coder.cn/img/ZzFB7SoLud3VstD.gif)

拓展2：

> 两秒后清空div标签的内容

```js
import {init} from 'snabbdom/build/package/init'
import {h} from 'snabbdom/build/package/h'
const patch = init([])

let vnode = h('div#container', [
  h('h1', 'Hello Snabbdom'),
  h('p', 'Hello p')
])
let app = document.querySelector('#app')
let oldVNode = patch(app, vnode)

// 两秒后清空div标签的内容
setTimeout(() => {
  // h('!')是创建注释
  vnode = h('!')
  patch(oldVNode, vnode)
}, 2000)
```

![](http://5coder.cn/img/XWG9SNfIaOwcbgy.gif)

### 4.模块

Snabbdom 的核心库并不能处理DOM元素的属性/样式/事件等，如果需要处理的话，可以使用模块

#### 常用模块

- 官方提供了6个模块
  - `attributes`
    - 设置VNode对应的DOM元素的属性，内部使用DOM的标准方法`setAttribute()`
    - 内部会对DOM对象的布尔类型的属性做判断，例如：selected/checked等
  - `props`
    - 和`attributes`模块相似，设置DOM元素的属性，内部使用`element[attr] = value`
    - 内部不能处理布尔类型的属性
  - `dataset`
    - 设置HTML5中提供的`data-*`的自定义属性
  - `class`
    - 不是用来**设置**类样式的，而是用来**切换**类样式。如果要设置类样式，可以通过`h()`的第一个参数来设置`h('#div.red', vnode)`
    - 注意：给元素设置类样式是通过`sel`选择器
  - `eventListeners`
    - 注册和移除事件
  - `style`
    - 设置行内样式，使用该模块可以很容易设置动画
    - 内部注册了`transitionEnd`事件
    - `delayed/remove/destroy`

#### 模块使用

模块的使用步骤：

- 导入需要的模块
- `init()`函数中注册模块
- 使用`h()`函数创建VNode的时候，可以把第二个参数设置为对象，其他参数依次后移

#### 代码演示

```js
import {init} from 'snabbdom/build/package/init'
import { h } from 'snabbdom/build/package/h'

// 1.导入所需的模块
import { styleModule } from 'snabbdom/build/package/modules/style'
import { eventListenersModule } from 'snabbdom/build/package/modules/eventlisteners'
// 2.init函数中注册所需的模块
// init()的参数是数组，可以用来传入模块，处理属性、样式、事件等
let patch = init([
  // 注册模块
  styleModule,
  eventListenersModule
])
// 3.使用h()函数创建Vnode
let vnode = h('div.cls', [
  h('h1', {style: {backgroundColor: 'red'}}, '这里是h1标签'),
  h('p', {on: {click: eventHandler}}, '这里是p标签')
])

function eventHandler() {
  console.log('别点我，疼')
}
let app = document.querySelector('#app')
patch(app, vnode)
```

![](http://5coder.cn/img/L1sDmbwxZ7SnjqG.png)

## 三、Snabbdom源码解析

> 接下来学习Snabbdom源码，因为Vue中的虚拟DOM是通过改造Snabbdom实现的。所以看完Snabbdom源码之后，就掌握了Vue中虚拟DOM的实现原理。通过查看Snabbdom源码，可以掌握VNode到底是什么，`h()、init()、patch()`到底是如何工作的。

### 1.概述

#### 如何学习源码

- 先宏观了解
- 带着目标看源码
- 看源码的过程不求甚解
- 调试
- 参考资料

#### Snabbdom的核心

- 使用`h()`函数创建`JavaScript`对象(`VNode`)描述真实`DOM`
- `init()`设置模块，创建`patch()`
- `patch()`比较新旧两个VNode，如果patch函数的第一个参数是真实DOM，首先将真实DOM转换成虚拟DOM，再进行对比
- 把变化的内容更新到真实`DOM`树上

#### Snabbdom源码

- 源码地址：

  - https://github.com/snabbdom/snabbdom
  - 当前使用版本：v2.1.0

- 克隆代码

  - ```bash
    git clone -b v2.1.0 --depth=1 https://github.com/snabbdom/snabbdom.git
    ```

- src目录结构

  ```txt
  ├── package
  │   ├── helpers
  │   │   └── attachto.ts		定义了 vnode.ts 中 AttachData 的数据结构
  │   ├── modules
  │   │   ├── attributes.ts		
  │   │   ├── class.ts
  │   │   ├── dataset.ts
  │   │   ├── eventlisteners.ts
  │   │   ├── hero.ts				example 中使用到的自定义钩子
  │   │   ├── module.ts			定义了模块中用到的钩子函数
  │   │   ├── props.ts
  │   │   └── style.ts
  │   ├── h.ts							h() 函数，用来创建 VNode
  │   ├── hooks.ts					所有钩子函数的定义
  │   ├── htmldomapi.ts			对 DOM API 的包装
  │   ├── init.ts						加载 modules、DOMAPI，返回 patch 函数
  │   ├── is.ts							辅助模块，判断数组和原始值的函数
  │   ├── jsx-global.ts			jsx 的类型声明文件
  │   ├── jsx.ts						处理 jsx
  │   ├── thunk.ts					优化处理，对复杂视图不可变值得优化
  │   ├── tovnode.ts				DOM 转换成 VNode
  │   ├── ts-transform-js-extension.cjs
  │   ├── tsconfig.json			ts 的编译配置文件
  │   └── vnode.ts					虚拟节点定义
  ```

### 2.h函数

- `h()`函数介绍

  - 在使用Vue的时候见过`h()`函数

    ```js
    new Vue({
        router,
        store,
        render: h => h(App)
    }).$mount('#app')
    ```

  - `h()`函数最早见于[hyperscript](https://github.com/hyperhype/hyperscript)，使用`JavaScript`创建超文本

  - Snabbdom中的`h()`函数不是用来创建超文本，而是创建`VNode`

- [函数重载](https://www.zhihu.com/question/63751258)

  - 概念

    - 函数名相同，**参数个数**或**参数类型**不同的函数
    - `JavaScript`中没有重载的概念
    - `TypeScript`中有重载，不过重载的实现还是用过代码调整参数

  - 重载的示意

    ```js
    // 参数个数不同的函数重载
    function add(a: number, b: number) {
        console.log(a + b)
    }
    function add(a: number, b: number, c: number) {
        console.log(a + b + c)
    }
    add(1, 2)  // 调用第一个add函数
    add(1, 2, 3)  // 调用第二个add函数
    ```

    

    ```js
    // 参数类型不同的函数重载
    function add (a: number, b: number) {
      console.log(a + b)
    }
    function add (a: number, b: string) {
      console.log(a + b)
    }
    add(1, 2)  // 调用第一个add函数
    add(1, '2')  // 调用第二个add函数
    ```

  - 源码位置：src/package/h.ts

    ```typescript
    // h 函数的重载
    export function h (sel: string): VNode
    export function h (sel: string, data: VNodeData | null): VNode
    export function h (sel: string, children: VNodeChildren): VNode
    export function h (sel: string, data: VNodeData | null, children: VNodeChildren): VNode
    export function h (sel: any, b?: any, c?: any): VNode {
      var data: VNodeData = {}
      var children: any
      var text: any
      var i: number
      // 处理参数，实现重载的机制
      // 当c参数不为undefined时，正面函数参数个数为3
      if (c !== undefined) {
        // 处理三个参数的情况
        // sel、data、children/text
        if (b !== null) {
          data = b
        }
        // 如果 c 是数组
        if (is.array(c)) {
          children = c
        // 如果 c 是字符串或者数字，是给节点标签中用来显示的内容
        } else if (is.primitive(c)) {
          text = c
        // 如果 c 是VNode
        } else if (c && c.sel) {
          children = [c]
        }
      } else if (b !== undefined && b !== null) {
        // 处理两个参数的情况
        // 如果b是数组
        if (is.array(b)) {
          children = b
        } else if (is.primitive(b)) {
          // 如果 c 是字符串或者数字
          text = b
        } else if (b && b.sel) {
          // 如果 b 是 VNode
          children = [b]
        } else { data = b }
      }
      if (children !== undefined) {
        // 处理 children 中的原始值(string/number)
        for (i = 0; i < children.length; ++i) {
          // 如果 child 是 string/number，创建文本节点
          if (is.primitive(children[i])) children[i] = vnode(undefined, undefined, undefined, children[i], undefined)
        }
      }
      if (
        sel[0] === 's' && sel[1] === 'v' && sel[2] === 'g' &&
        (sel.length === 3 || sel[3] === '.' || sel[3] === '#')
      ) {
        // 如果是 svg，添加命名空间
        addNS(data, children, sel)
      }
      // 返回 VNode
      return vnode(sel, data, children, text, undefined)
    };
    ```

### 3.VNode

- 一个VNode就是一个虚拟节点，用来描述一个DOM元素，如果这个VNode有`children`就是Virtual DOM

- 源码位置：src/package/vnode.ts

  ```typescript
  export interface VNode {
    // 选择器
    sel: string | undefined;
    // 节点数据：属性/样式/事件等
    data: VNodeData | undefined;
    // 子节点，和 text 只能互斥
    children: Array<VNode | string> | undefined;
    // 记录 vnode 对应的真实 DOM
    elm: Node | undefined;
    // 节点中的内容，和 children 只能互斥
    text: string | undefined;
    // 优化用
    key: Key | undefined;
  }
  
  export interface VNodeData {
    props?: Props
    attrs?: Attrs
    class?: Classes
    style?: VNodeStyle
    dataset?: Dataset
    on?: On
    hero?: Hero
    attachData?: AttachData
    hook?: Hooks
    key?: Key
    ns?: string // for SVGs
    fn?: () => VNode // for thunks
    args?: any[] // for thunks
    [key: string]: any // for any other 3rd party module
  }
  
  export function vnode (sel: string | undefined,
                        data: any | undefined,
                        children: Array<VNode | string> | undefined,
                        text: string | undefined,
                        elm: Element | Text | undefined): VNode {
    const key = data === undefined ? undefined : data.key
    return { sel, data, children, text, elm, key }
  }
  ```

### 4.Snabbdom

#### patch 整体过程分析

- `patch(oldVnode, newVnode)`
- `patch`函数俗称打补丁，把新节点中变化的内容渲染到真实DOM，最后返回新节点作为下一次处理的旧节点
- 对比新旧VNode是否相同节点(节点的`key`和`sel`相同)
  - 如果不是相同节点，删除之前的内容重新渲染
  - 如果是相同节点，在判断新的`VNode`是否有`text`，如果有并且和`oldVnode`的`text`不同，直接更新文本内容
    - 如果新的`VNode`有`children`，判断子节点是否有变化，判断子节点的过程使用的就是`diff`算法
- `diff`过程只是进行同层级比较

![](http://5coder.cn/img/ykzGs5gIqB8DFa2.png)

#### init

- 功能：`init(modules, domAPI)`, 返回`patch()`函数（高阶函数）

- 为什么使用高阶函数？

  - 因为`patch()`函数在**外部会调用多次**，每次调用依赖一些参数，比如：modules、domAPI、cbs
  - 通过高阶函数让`init()`内部形成闭包，返回的`patch()`可以访问到`modules、domAPI、cbs`，而不需要重新创建

- `init()`在返回`fatch()`之前，首先收集了所有模块中的钩子函数存储到`cbs`对象中

- 源码位置：src/package/init.ts

  ```typescript
  // 定义了一些hooks钩子函数的名称，这些钩子函数在init时会被初始化，在特定的时机会被执行
  const hooks: Array<keyof Module> = ['create', 'update', 'remove', 'destroy', 'pre', 'post']
  
  // 参数一：modules，模块数组
  // 参数二：domAPI，用来把VNode对象转换成其他平台下的对应的元素，没有传递时默认设置成DOMAPI(浏览器环境下的dom对象，htmlDomApi)
  export function init (modules: Array<Partial<Module>>, domApi?: DOMAPI) {
    let i: number
    let j: number
    // callbacks回调函数，存储模块中的钩子函数
    const cbs: ModuleHooks = {
      create: [],
      update: [],
      remove: [],
      destroy: [],
      pre: [],
      post: []
    }
    // 初始化 api
    const api: DOMAPI = domApi !== undefined ? domApi : htmlDomApi
    // 把传入的所有模块的钩子方法，统一存储到 cbs 对象中
    // 最终构建的 cbs 对象的形式 cbs = [ create: [fn1, fn2], update: [], ... ]
  	for (i = 0; i < hooks.length; ++i) {
      // cbs['create'] = []
      cbs[hooks[i]] = []
        for (j = 0; j < modules.length; ++j) {
          // const hook = modules[0]['create']
          const hook = modules[j][hooks[i]]
          if (hook !== undefined) {
            (cbs[hooks[i]] as any[]).push(hook)
          }
        }
    }
      ……
    return function patch (oldVnode: VNode | Element, vnode: VNode): VNode {
      ……
    }
  }
  ```

#### patch

- 功能

  - 传入新旧 `VNode`，对比差异，把差异渲染到 `DOM`
  - 返回新的 `VNode`，作为下一次 `patch()` 的 `oldVnode`

- 执行过程

  - 首先执行**模块**中的**钩子函数pre**

    ```js
    for (i = 0; i < cbs.pre.length; ++i) cbs.pre[i]()
    ```

  - 如果 `oldVnode` 和`vnode` 相同（`key`和`sel`相同）

    sameVnode

    ```js
    function sameVnode (vnode1: VNode, vnode2: VNode): boolean {
      // key和sel都相同
      return vnode1.key === vnode2.key && vnode1.sel === vnode2.sel
    }
    ```

    - 调用`patchVnode()`，找节点的差异并更新`DOM`(后面详细讲解)

      ```js
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

  - 如果`oldVnode`是`DOM`元素

    - 把`DOM`元素转换成`oldVnode`

      ```js
      function emptyNodeAt (elm: Element) {
        const id = elm.id ? '#' + elm.id : ''
        const c = elm.className ? '.' + elm.className.split(' ').join('.') : ''
        return vnode(api.tagName(elm).toLowerCase() + id + c, {}, [], undefined, elm)
      }
      ```

    - 调用`createElm()`把`vnode`转换为真实`DOM`，记录到`vnode.elm`

    - 把刚创建的`DOM`元素插入到`parent`中

    - 移除老节点

    - 触发用户设置的`create`钩子函数

- 源码位置：src/package/init.ts

  ```typescript
  return function patch (oldVnode: VNode | Element, vnode: VNode): VNode {
    let i: number, elm: Node, parent: Node
    // 保存新插入节点的队列，为了触发钩子函数
    const insertedVnodeQueue: VNodeQueue = []
    // 执行模块的 pre 钩子函数
    for (i = 0; i < cbs.pre.length; ++i) cbs.pre[i]()
    // 如果 oldVnode 不是 VNode，创建 VNode 并设置 elm 
    if (!isVnode(oldVnode)) {
      // 通过 emptyNodeAt 把 DOM 元素转换成空的 VNode
      oldVnode = emptyNodeAt(oldVnode)
    }
    // 如果新旧节点是相同节点(key 和 sel 相同)
    if (sameVnode(oldVnode, vnode)) {
      // 找节点的差异并更新 DOM
      patchVnode(oldVnode, vnode, insertedVnodeQueue)
    } else {
      // 如果新旧节点不同，vnode 创建对应的 DOM
      // 获取当前的 DOM 元素,!是TypeScript语法标识这个属性一定有值
      elm = oldVnode.elm!
      parent = api.parentNode(elm) as Node
      // 触发 init/create 钩子函数,创建 DOM
      createElm(vnode, insertedVnodeQueue)
  
      if (parent !== null) {
        // 如果父节点不为空，把 vnode 对应的 DOM 插入到文档中
        api.insertBefore(parent, vnode.elm!, api.nextSibling(elm))
        // 移除老节点
        removeVnodes(parent, [oldVnode], 0, 0)
      }
    }
  	// 执行用户设置的 insert 钩子函数
    for (i = 0; i < insertedVnodeQueue.length; ++i) {
      insertedVnodeQueue[i].data!.hook!.insert!(insertedVnodeQueue[i])
    }
    // 执行模块的 post 钩子函数
    for (i = 0; i < cbs.post.length; ++i) cbs.post[i]()
    return vnode
  }
  ```

#### createElm

- 功能

  - `createEle(Vnode, insertedVnodeQueue)`, 返回创建的DOM元素
  - 创建`vnode`对应的`DOM`元素，把DOM元素存储在`vnode`的`elm`属性中，但是并没有挂载在DOM树上

- 执行过程

  > 主要分为三个过程：
  >
  > - 执行用户设置的`init`钩子函数
  > - 把VNode转换成真实DOM，并存储在vnode的elm属性上，此时并没有挂载到DOM树上
  > - 返回新创建的DOM

  - 首先触发用户设置的`init`钩子函数
  - 如果选择器是`!`，创建注释节点
  - 如果选择器为空，创建文本节点
  - 如果选择器不为空
    - 解析选择器，设置标签的`id`和`class`属性
    - 执行模块的`create`钩子函数
    - 如果`vnode`有`children`，创建子`vnode`对应的`DOM`，追加到`DOM`树
    - 如果`vnode`的`text`值是`string/number`，创建文本节点并追加到`DOM`树
    - 执行用户设置的`create`钩子函数
    - 如果有用户设置的`insert`钩子函数，把`vnode`添加到队列中

- 源码位置：src/package/init.ts

  ```typescript
    function createElm (vnode: VNode, insertedVnodeQueue: VNodeQueue): Node {
      let i: any
      let data = vnode.data
      
      if (data !== undefined) {
        // 执行用户设置的 init 钩子函数
        const init = data.hook?.init
        if (isDef(init)) {
          init(vnode)
          data = vnode.data
        }
      }
      const children = vnode.children
      const sel = vnode.sel
      if (sel === '!') {
        // 如果选择器是!，创建注释节点
        if (isUndef(vnode.text)) {
          vnode.text = ''
        }
        vnode.elm = api.createComment(vnode.text!)
      } else if (sel !== undefined) {
        // 如果选择器不为空
        // 解析选择器
        // Parse selector
        const hashIdx = sel.indexOf('#')
        const dotIdx = sel.indexOf('.', hashIdx)
        const hash = hashIdx > 0 ? hashIdx : sel.length
        const dot = dotIdx > 0 ? dotIdx : sel.length
        const tag = hashIdx !== -1 || dotIdx !== -1 ? sel.slice(0, Math.min(hash, dot)) : sel
        const elm = vnode.elm = isDef(data) && isDef(i = data.ns)
          ? api.createElementNS(i, tag)  // 一般是SVG
          : api.createElement(tag)  // 创建DOM元素
        if (hash < dot) elm.setAttribute('id', sel.slice(hash + 1, dot))
        if (dotIdx > 0) elm.setAttribute('class', sel.slice(dot + 1).replace(/\./g, ' '))
        // 遍历执行模块的 create 钩子函数
        for (i = 0; i < cbs.create.length; ++i) cbs.create[i](emptyNode, vnode)
        // 如果 vnode 中有子节点，创建子 vnode 对应的 DOM 元素并追加到 DOM 树上
        if (is.array(children)) {
          for (i = 0; i < children.length; ++i) {
            const ch = children[i]
            if (ch != null) {
              api.appendChild(elm, createElm(ch as VNode, insertedVnodeQueue))
            }
          }
        } else if (is.primitive(vnode.text)) {
          // 如果 vnode 的 text 值是 string/number，创建文本节点并追加到 DOM 树
          api.appendChild(elm, api.createTextNode(vnode.text))
        }
        const hook = vnode.data!.hook
        if (isDef(hook)) {
          // 执行用户传入的钩子 create
          hook.create?.(emptyNode, vnode)
          if (hook.insert) {
            // 把 vnode 添加到队列中，为后续执行 insert 钩子做准备
            insertedVnodeQueue.push(vnode)
          }
        }
      } else {
        // 如果选择器为空，创建文本节点
        vnode.elm = api.createTextNode(vnode.text!)
      }
      // 返回新创建的 DOM                                
      return vnode.elm
    }
  ```

#### removeVnodes

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

invokeDestroyHook

```typescript
function invokeDestroyHook (vnode: VNode) {
  const data = vnode.data
  if (data !== undefined) {
    data?.hook?.destroy?.(vnode)
    for (let i = 0; i < cbs.destroy.length; ++i) cbs.destroy[i](vnode)
    if (vnode.children !== undefined) {
      for (let j = 0; j < vnode.children.length; ++j) {
        const child = vnode.children[j]
        if (child != null && typeof child !== 'string') {
          invokeDestroyHook(child)
        }
      }
    }
  }
}
```

createRmCb

```typescript
function createRmCb (childElm: Node, listeners: number) {
  return function rmCb () {
    if (--listeners === 0) {
      const parent = api.parentNode(childElm) as Node
      api.removeChild(parent, childElm)
    }
  }
}
```

#### addVnodes

```typescript
function addVnodes (
  parentElm: Node,  // 父元素
  before: Node | null,  // 参考节点，vnode定义的节点插入到before之前
  vnodes: VNode[],  // 添加的节点
  startIdx: number,  // 开始索引
  endIdx: number,  // 结束索引
  insertedVnodeQueue: VNodeQueue  // 存储刚刚插入的具有insert钩子函数的vnode节点
) {
  for (; startIdx <= endIdx; ++startIdx) {
    const ch = vnodes[startIdx]
    if (ch != null) {
      api.insertBefore(parentElm, createElm(ch, insertedVnodeQueue), before)
    }
  }
}
```

#### patchVnode

- 功能
  - `patchVnode(oldVnode, vnode, insertedVnodeQueue)`
  - 对比`oldVnode`和`vnode`的差异，把差异渲染到DOM
- **执行过程**
  - 首先执行**用户**设置的`prepatch`钩子函数
  - 执行`create`钩子函数
    - 首先执行**模块**的`create`钩子函数
    - 然后执行**用户**设置的`create`钩子函数
  - 如果**vnode.text**未定义
    - 如果`oldVnode.children`和`vnode.children`都有值
      - 调用`updateChildren()`
      - 使用diff算法对比子节点，更新子节点
    - 如果`vnode.children`有值，`oldVnode.children`无值
      - 清空DOM元素
      - 调用`addVnodes()`，批量添加子节点
    - 如果`oldVnode.children`有值，`vnode.children`无值
      - 调用`removeVnode()`，批量移除子节点
    - 如果`oldVnode.text`有值
      - 清空DOM元素的内容
  - 如果设置了`vnode.text`并且和`oldVnode.text`不等
    - 如果老节点有子节点，全部移除
    - 设置DOM元素的`textContent`为`vnode.text`
  - 最后执行用户设置的`postpatch`钩子函数

![](http://5coder.cn/img/aSVb3ZNoyTWgeck.png)

源码位置：src/package/init.ts

```typescript
function patchVnode (oldVnode: VNode, vnode: VNode, insertedVnodeQueue: VNodeQueue) {
    const hook = vnode.data?.hook
    // 首先执行用户设置的 prepatch 钩子函数
    hook?.prepatch?.(oldVnode, vnode)
    const elm = vnode.elm = oldVnode.elm!
    const oldCh = oldVnode.children as VNode[]
    const ch = vnode.children as VNode[]
  	// 如果新老 vnode 相同返回
    if (oldVnode === vnode) return
    if (vnode.data !== undefined) {
      // 执行模块的 update 钩子函数
      for (let i = 0; i < cbs.update.length; ++i) cbs.update[i](oldVnode, vnode)
      // 执行用户设置的 update 钩子函数
      vnode.data.hook?.update?.(oldVnode, vnode)
    }
  	// 如果 vnode.text 未定义
    if (isUndef(vnode.text)) {
      // 如果新老节点都有 children
      if (isDef(oldCh) && isDef(ch)) {
        // 调用 updateChildren 对比子节点，更新子节点
        if (oldCh !== ch) updateChildren(elm, oldCh, ch, insertedVnodeQueue)
      } else if (isDef(ch)) {
        // 如果新节点有 children，老节点没有 children
      	// 如果老节点有text，清空dom 元素的内容
        if (isDef(oldVnode.text)) api.setTextContent(elm, '')
        // 批量添加子节点
        addVnodes(elm, null, ch, 0, ch.length - 1, insertedVnodeQueue)
      } else if (isDef(oldCh)) {
        // 如果老节点有children，新节点没有children
      	// 批量移除子节点
        removeVnodes(elm, oldCh, 0, oldCh.length - 1)
      } else if (isDef(oldVnode.text)) {
        // 如果老节点有 text，清空 DOM 元素
        api.setTextContent(elm, '')
      }
    } else if (oldVnode.text !== vnode.text) {
      // 如果没有设置 vnode.text
      if (isDef(oldCh)) {
        // 如果老节点有 children，移除
        removeVnodes(elm, oldCh, 0, oldCh.length - 1)
      }
      // 设置 DOM 元素的 textContent 为 vnode.text
      api.setTextContent(elm, vnode.text!)
    }
    // 最后执行用户设置的 postpatch 钩子函数
    hook?.postpatch?.(oldVnode, vnode)
  }
```

#### updateChildren

- **功能**

  - diff算法的核心，对比新旧节点的children，更新DOM

- **执行过程：**

  - 要对比两棵树的差异，我们可以取第一棵树的没一个节点一次和第二棵树的每一个节点比较，但是这样的时间复杂度为O(n^3)

  - 在DOM操作的时候我们很少很少会把一个**父节点移动/更新到某一个子节点**

  - 因此只需要找**同级别**的**子节点**一次比较，然后**再找下一级别的节点比较**，这样算法的时间复杂度为O(n)

    ![](http://5coder.cn/img/HOKszpbk76tA9yZ.png)

  - 在进行同级别节点比较的时候，首先会对新老节点数组的**开始和结尾**节点设置**标记索引**，遍历的过程中移动索引

  - 在对**开始和结束节点**比较的时候，总共会有四种情况：

    - `oldStartVnode` / `newStartVnode`（旧开始节点 / 新开始节点）

    - `oldEndVnode` / `newEndVnode`（旧结束节点 / 新结束节点）

    - `oldStartVnode` / `newEndVnode`（旧开始节点 / 新结束节点）

    - `oldEndVnode` / `newStartVnode`（旧结束节点 / 新开始节点）

      ![](http://5coder.cn/img/ZjSoAHM1vYNJCm5.png)

  - 开始节点和结束节点比较，这两种情况类似

    - `oldStartVnode` / `newStartVnode`（旧开始节点 / 新开始节点）
    - `oldEndVnode` / `newEndVnode`（旧结束节点 / 新结束节点）

  - 如果`oldStartVnode`和`newStartVnode`是`sameVnode`（key和sel相同）

    - 调用`patchVnode`对比和更新节点

    - 把旧开始和新开始索引往后移动`oldStartIdx++` / `oldEndIdx++`

      ![](http://5coder.cn/img/njXLUz5tsFNWvql.png)

  - `oldStartVnode` / `newEndVnode`（旧开始节点 / 新结束节点）相同

    - 调用`patchVnode()`对比和更新节点

    - 把`oldStartVnode`对应的DOM元素，移动到右边

    - 更新索引

      ![](http://5coder.cn/img/image-20200103125428541.png)

  - `oldEndVnode` / `newStartVnode`（旧结束节点 / 新开始节点）相同

    - 调用`patchVnode()`对比和更新节点

    - 把`oldEndVnode`对应的DOM元素，移动到左边

    - 更新索引

      ![](http://5coder.cn/img/image-20200103125735048.png)

  - 如果不是以上四种情况

    - 遍历新节点，使用`newStartNode`的`key`在老节点数组中找相同节点

    - 如果没有找到，说明`newStartNode`是新节点

      - 创建新节点对应的DOM元素，插入到DOM树中

    - 如果找到了

      - 判断新节点和找到的老节点的sel选择器是否相同

        - 如果不同，说明节点被修改了
          - 重新创建对应的DOM元素，插入到DOM树中
        - 如果相同，把`elmToMove`对应的DOM元素，移动到左边

        ![](http://5coder.cn/img/image-20200109184822439.png)

  - 循环结束

    - 当老节点的所有子节点先遍历完（`oldStartIdx > oldEndIdx`），循环结束
    - 新节点的所有子节点先遍历完（`newStartIdx < newEndIdx`），循环结束

  - 如果老节点的数组先遍历完（`oldStartIdx > oldEndIdx`），说明新节点有剩余，把剩余节点批量插入到右边

    ![](http://5coder.cn/img/image-20200103150918335.png)

  - 如果新节点的数组先遍历完（`newStartIdx > newEndIdx`），说明老节点有剩余，把剩余节点批量删除

    ![](http://5coder.cn/img/image-20200109194751093.png)

- 源码位置：src/package/init.ts

  ```typescript
  function updateChildren (parentElm: Node,
    oldCh: VNode[],
    newCh: VNode[],
    insertedVnodeQueue: VNodeQueue) {
    let oldStartIdx = 0
    let newStartIdx = 0
    let oldEndIdx = oldCh.length - 1
    let oldStartVnode = oldCh[0]
    let oldEndVnode = oldCh[oldEndIdx]
    let newEndIdx = newCh.length - 1
    let newStartVnode = newCh[0]
    let newEndVnode = newCh[newEndIdx]
    let oldKeyToIdx: KeyToIndexMap | undefined
    let idxInOld: number
    let elmToMove: VNode
    let before: any
  
    while (oldStartIdx <= oldEndIdx && newStartIdx <= newEndIdx) {
      // 索引变化后，可能会把节点设置为空
      if (oldStartVnode == null) {
        // 节点为空移动索引
        oldStartVnode = oldCh[++oldStartIdx] // Vnode might have been moved left
      } else if (oldEndVnode == null) {
        oldEndVnode = oldCh[--oldEndIdx]
      } else if (newStartVnode == null) {
        newStartVnode = newCh[++newStartIdx]
      } else if (newEndVnode == null) {
        newEndVnode = newCh[--newEndIdx]
      // 比较开始和结束节点的四种情况
      } else if (sameVnode(oldStartVnode, newStartVnode)) {
        // 1. 比较老开始节点和新的开始节点
        patchVnode(oldStartVnode, newStartVnode, insertedVnodeQueue)
        oldStartVnode = oldCh[++oldStartIdx]
        newStartVnode = newCh[++newStartIdx]
      } else if (sameVnode(oldEndVnode, newEndVnode)) {
        // 2. 比较老结束节点和新的结束节点
        patchVnode(oldEndVnode, newEndVnode, insertedVnodeQueue)
        oldEndVnode = oldCh[--oldEndIdx]
        newEndVnode = newCh[--newEndIdx]
      } else if (sameVnode(oldStartVnode, newEndVnode)) { // Vnode moved right
        // 3. 比较老开始节点和新的结束节点
        patchVnode(oldStartVnode, newEndVnode, insertedVnodeQueue)
        api.insertBefore(parentElm, oldStartVnode.elm!, api.nextSibling(oldEndVnode.elm!))
        oldStartVnode = oldCh[++oldStartIdx]
        newEndVnode = newCh[--newEndIdx]
      } else if (sameVnode(oldEndVnode, newStartVnode)) { // Vnode moved left
        // 4. 比较老结束节点和新的开始节点
        patchVnode(oldEndVnode, newStartVnode, insertedVnodeQueue)
        api.insertBefore(parentElm, oldEndVnode.elm!, oldStartVnode.elm!)
        oldEndVnode = oldCh[--oldEndIdx]
        newStartVnode = newCh[++newStartIdx]
      } else {
        // 开始节点和结束节点都不相同
        // 使用 newStartNode 的 key 再老节点数组中找相同节点
        // 先设置记录 key 和 index 的对象
        if (oldKeyToIdx === undefined) {
          oldKeyToIdx = createKeyToOldIdx(oldCh, oldStartIdx, oldEndIdx)
        }
        // 遍历 newStartVnode, 从老的节点中找相同 key 的 oldVnode 的索引
        idxInOld = oldKeyToIdx[newStartVnode.key as string]
        // 如果是新的vnode
        if (isUndef(idxInOld)) { // New element
          // 如果没找到，newStartNode 是新节点
          // 创建元素插入 DOM 树
          api.insertBefore(parentElm, createElm(newStartVnode, insertedVnodeQueue), oldStartVnode.elm!)
        } else {
          // 如果找到相同 key 相同的老节点，记录到 elmToMove 遍历
          elmToMove = oldCh[idxInOld]
          if (elmToMove.sel !== newStartVnode.sel) {
            // 如果新旧节点的选择器不同
            // 创建新开始节点对应的 DOM 元素，插入到 DOM 树中
            api.insertBefore(parentElm, createElm(newStartVnode, insertedVnodeQueue), oldStartVnode.elm!)
          } else {
            // 如果相同，patchVnode()
            // 把 elmToMove 对应的 DOM 元素，移动到左边
            patchVnode(elmToMove, newStartVnode, insertedVnodeQueue)
            oldCh[idxInOld] = undefined as any
            api.insertBefore(parentElm, elmToMove.elm!, oldStartVnode.elm!)
          }
        }
        // 重新给 newStartVnode 赋值，指向下一个新节点
        newStartVnode = newCh[++newStartIdx]
      }
    }
    // 循环结束，老节点数组先遍历完成或者新节点数组先遍历完成
    if (oldStartIdx <= oldEndIdx || newStartIdx <= newEndIdx) {
      if (oldStartIdx > oldEndIdx) {
        // 如果老节点数组先遍历完成，说明有新的节点剩余
        // 把剩余的新节点都插入到右边
        before = newCh[newEndIdx + 1] == null ? null : newCh[newEndIdx + 1].elm
        addVnodes(parentElm, before, newCh, newStartIdx, newEndIdx, insertedVnodeQueue)
      } else {
        // 如果新节点数组先遍历完成，说明老节点有剩余
        // 批量删除老节点
        removeVnodes(parentElm, oldCh, oldStartIdx, oldEndIdx)
      }
    }
  }
  ```


#### 调试updateChildren

```html
<ul>
  <li>首页</li>
  <li>微博</li>
  <li>视频</li>
</ul>

<ul>
  <li>首页</li>
  <li>视频</li>
  <li>微博</li>
</ul>
```