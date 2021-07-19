---
title: Vue.js 源码剖析-响应式原理、虚拟 DOM、模板编译和组件化
author: 5coder
tags: Vue源码解析
category: 大前端(杂识)
abbrlink: 40057
date: 2021-07-18 21:34:37
---

## 1.请简述Vue首次渲染过程

### 1.实例创建完成后，调用`$mount()`方法

完整版中会先调用`src/platforms/web/entry-runtime-with-compiler.js`中重写的`$mount()`(即进行模板编译)，其中：

- 先判断`options`中是否有`render`，如果没有传递`render`，调用`compileToFunctions()`，生成render()函数
- 然后设置`options.render = render`

然后调用原来的`$mount()`（在`src/platform/web/runtime/index.js`中定义），其中会调用`mountComponent(this, el, hydrating)`

### 2.mountComponent(this, el, hydrating)

- 触发`beforeMount：callHook`(vm, 'beforeMount')`
- 定义函数`updateComponent = () => { vm._update(vm._render(), hydrating) }`
  - `vm._render()`生成虚拟DOM（`vm._render()`定义在`src/core/instance/render.js`中）
  - `vm._update()`将虚拟DOM转换成真是DOM(`vm._update()`定义在`src/core/instance/lifecycle.js`中)
- 创建`Watcher`实例，把`updateComponent`传递进去，`updateComponent`是在`Watcher`中通过`Watcher`的`get()`实例方法执行的
- 触发`mounted`；返回实例`return vm`

### 3.watcher.get()

首次渲染创建的是渲染`Watcher`，创建完`Watcher`实例后会调用一个get()方法，`get()`中会调用`updateComponent()`，`updateComponent()`中会调用`vm._update(VNode. hydrating)`，而其中的`VNode`是调用`vm._render()`创建`VNode`

`vm._render()`的执行过程：

- 获取创建实例时存放在`options`中的`render`函数：`const { render, _parentVnode } = vm.$options`
- 调用`render.call(vm.renderProxy, vm.$createElement)`（这个`render`是创建实例`new Vue()`时传入的`render()`，或者是编译`template`生成的`render()`），最后返回`VNode`

然后执行`vm._update(VNode, hydrating)`，其中：

- 调用`vm.__patch__(vm.$el, vnode)`挂载真实`DOM`
- 将`vm.__patch__`的返回值记录在`vm.$el`中

------

## 2.请简述 Vue 响应式原理

Vue使用观察者模式来对其数据进行响应式处理，过程如下：

### 创建观察者

- 在创建 `Vue` 实例时，调用的 `this._init(options)` 中会执行 `initInjections(vm)`、`initState(vm)`，这两个方法中分别会对 `inject` 的成员、本实例的 `props` 和 `data` 进行响应式处理
- `initInjections(vm)` 中会遍历 `inject` 的成员，通过 `defineReactive(vm, key, result[key])` 将每个成员转换成响应式属性（即劫持 `getter/setter`）
- `initState(vm)` 中调用 `initProps(vm, opts.props)`，其中编辑 `props` 属性，通过 `defineReactive(props, key, value)` 将属性转换成`getter`、`setter`，然后存入 `props`（也是 `vm._props`）中
- `initState(vm)` 中调用 `initData(vm, opts.props)`，其中调用 `observe(data, true /* asRootData */)` 对 `data` 进行响应式处理
- `defineReactive(obj, key, val, customSetter?, shallow?)`
  - 会将传入的 `key` 换成响应式属性，即其劫持 `getter/setter` （ `Object.defineProperty( obj, key, { ..., get(){...}, set(){...} } )` ）
  - 为每个属性 `key` 生成一个 `Dep` 对象 `dep`（`const dep = new Dep()`）；`dep` 会在 `getter` 中收集依赖（即相应属性的 `Watcher` 对象），在 `setter` 中调用 `dep.notify()` 派发更新；
  - 在需要递归观察子对象时，会调用 `observe(val)`（`let childOb = !shallow && observe(val)`），若 `val` 是个对象，则会为这个对象创建一个 `Observer` 对象，并返回。

- `observe (value, asRootData?)`
  - 判断 `value` 是否是对象，不是对象就返回
  - 是对象，则这个对象可称之为 观测对象 ，然后为这个对象创建一个 `Observer` 对象 ：`ob = new Observer(value)`，并返回 `ob`（在 `defineReactive` 中，这个返回的 `ob` 会在 `getter` 中收集依赖相应的依赖）
  - `Observer` 构造函数中，会新建一个 `Dep` 对象 `dep`，这里的 `dep` 是为传入的 观测对象（进行响应式处理的对象）收集依赖（`Watcher`）；与 `defineReactive` 中的 `dep` 不一样
  - 将 `Observer` 实例挂载到 观测对象 的 `__ob__` 属性：`def(value, '__ob__', this)`
  - 若 `value` 不是数组，则执行 `this.walk(value)` 方法，遍历 `value` 中的每一个属性，然后调用 `defineReactive(obj, keys[i])`
  - 若 `value` 是数组
    - `Vue` 并没有对数组对象的索引调用 `defineReactive` 来生成 `getter/setter`，而是重写了原生数组中会更改原数组的方法，调用这些新方法后，数组对象对应的 `dep` 对象会调用 dep.notify 方法来驱动视图的更新
    - 重写的数组方法：`'push'， 'pop', 'shift', 'unshift', 'splice', 'sort', 'reverse'`
    - 重写数组方法后，调用 `this.observeArray(value)`，作用是当数组中的元素存在对象时，为数组中的每一个对象创建一个 `observer` 实例

至此，创建观察者结束

### 依赖的收集

- 在进行挂载时（ 调用 `$mount()` ），会执行 `mountComponent` 方法，其中会创建一个渲染 `Watcher` 对象
- 渲染 `Watcher` 对象构造函数的最后会执行 `get()` 方法，`get()` 中会先执行 `pushTarget(this)`，`pushTarget` 中则会将 Dep.target 设置为该 `watcher`（`Dep.target = target`）
- 然后调用 `this.getter.call(vm, vm)`，即执行了 `vm._update(vm._render(), hydrating)`，而 `vm._render()` 中执行 `render.call(vm._renderProxy, vm.$createElement)` 以生成 `vnode`，这个生成 `VNode` 的过程中，会触发 相应的响应式数据的 `getter` ，然后其中的 `dep.depend()` 则会收集当前实例 `watcher`

当生成完 `VNode` 后，就完成了响应式数据的的依赖收集

### 通知的发送

但修改某个响应式数据时，会触发该数据的 `setter`

- 如果新值是对象，且需要递归观察子对象时执行 `childOb = !shallow && observe(newVal)`，将新增也进行响应式处理
- 调用 `dep.notify()` 派发更新，`notify` 会调用每个订阅者（`watcher`）的 `update` 方法实现更新
- `watcher` 的 `update` 中使用 `queueWatcher()` 判断 `watcher` 是否被处理，若没有，则把 `watcher` 添加进 `queue` 队列中，并调用 `flushSchedulerQueue()`
- `flushSchedulerQueue()` 中先触发 `beforeUpdate` 钩子函数，然后调用 `watcher.run()`
- `watcher.run()` 中会调用 `get()` 方法，`get` 中执行 `getter`，而 `getter` 就是传入的 `updateComponent` 方法，`updateComponent` 中执行 `vm._update(vm._render(), hydrating)`，如此就完成了视图的更新
- 然后 `flushSchedulerQueue()` 后续代码中 还原更新步骤的初始状态、触发 `actived` 钩子函数、触发 `updated` 钩子函数

------

## 3.请简述虚拟 DOM 中 Key 的作用和好处

`Key` 是用来优化 `Diff` 算法的。`Diff`算法核心在于同层次节点比较，`Key` 就是用于在比较同层次新、旧节点时，判断其是否相同。

`Key` 一般用于生成一列同类型节点时使用，这种情况下，当修改这些同类型节点的某个内容、变更位置、删除、添加等时，此时界面需要更新视图，`Vue` 会调用 `patch` 方法通过对比新、旧节点的变化来更新视图。其从根节点开始若新、旧 `VNode` 相同，则调用 `patchVnode`

`patchVnode` 中若新节点没有文本，且新节点和旧节点都有有子节点，则需对子节点进行 `Diff` 操作，即调用 `updateChildren`，`Key` 就在 `updateChildren` 起了大作用

`updateChildren` 中会遍历对比上步中的新、旧节点的子节点，并按 Diff 算法通过 `sameVnode` 来判断要对比的节点是否相同

- 若这里的子节点未设置 `Key`，则此时的每个新、旧子节点在执行 `sameVnode` 时会判定相同，然后再次执行一次 `patchVnode` 来对比这些子节点的子节点
- 若设置了 `Key`，当执行 `sameVnode`
  - 若 `Key` 不同 `sameVnode` 返回 `false`，然后执行后续判断；
  - 若 `Key` 相同 `sameVnode` 返回 `true`，然后再执行 patchVnode 来对比这些子节点的子节点

即，使用了 `Key` 后，可以优化新、旧节点的对比判断，减少了遍历子节点的层次，少使用很多次 `patchVnode`

------

## 4.请简述 Vue 中模板编译的过程

### Vue 模板编译入口文件执行过程

在完整版 Vue 中，`src/platforms/web/entry-runtime-with-compiler.js` 里先保留 `Vue` 实例的 `mount`方法，然后重写该`mount`方法，然后重写该`mount` 方法，这个重写的方法就是完整版 `Vue` 中的模板编译器，其中在 `$options` 上挂载了模板编译后生成的 `render` 函数。

`$options` 上的 `render` 函数是由 `compileToFunctions(template, options, vm)` 这个函数生成，即将 `template` 转换成了 `render` 函数。所以这里就是完成了首次加载时对模板的编译。

这里梳理下生成 `render` 函数的相关函数的调用过程

### 第一步

调用 `compileToFunctions(template, options, vm)`

```js
  // src/platforms/web/entry-runtime-with-compiler.js 
  // 把 template 转换成 render 函数
  const { render, staticRenderFns } = compileToFunctions(template, {
    outputSourceRange: process.env.NODE_ENV !== 'production',
    shouldDecodeNewlines,
    shouldDecodeNewlinesForHref,
    delimiters: options.delimiters,
    comments: options.comments
  }, this)
  options.render = render
  options.staticRenderFns = staticRenderFns
```

### 第二步

`compileToFunctions` 是由 src/platforms/web/compiler/index.js 里的 `createCompiler(baseOptions)` 生成的。`baseOptions` 里是一些关于指令、模块、HTML标签相关的方法，这里不予关心。

所以 **第一步** 中 `compileToFunctions` 是这里的 `createCompiler` 返回的函数。

```js
// src/platforms/web/compiler/index.js

import { baseOptions } from './options'
import { createCompiler } from 'compiler/index'

const { compile, compileToFunctions } = createCompiler(baseOptions)

export { compile, compileToFunctions }
```

### 第三步

`createCompiler` 来自于 src/compiler/index.js，其中调用了 `createCompilerCreator(function baseCompile (template, options))` 方法

所以 **第二步** 中的 `createCompiler` 来自于这里的 `createCompilerCreator` 返回的函数，`createCompilerCreator` 中传入 函数 `baseCompile` 作为参数

那么 **第一步** 中的 `compileToFunctions` 就是这里的 `createCompilerCreator` 返回的函数执行（即执行 `createCompiler(baseOptions)`）后返回的函数

```js
// src/compiler/index.js

export const createCompiler = createCompilerCreator(function baseCompile (
  template: string,
  options: CompilerOptions
): CompiledResult {
  // 把模板转换成 ast 抽象语法树
  // 抽象语法树，用来以树形的方式描述代码结构
  const ast = parse(template.trim(), options)
  if (options.optimize !== false) {
    // 优化抽象语法树
    optimize(ast, options)
  }
  // 把抽象语法树生成字符串形式的 js 代码
  const code = generate(ast, options)
  return {
    ast,
    // 渲染函数
    render: code.render,
    // 静态渲染函数，生成静态 VNode 树
    staticRenderFns: code.staticRenderFns
  }
})
```

### 第四步

`createCompilerCreator` 来自于 `src/compiler/create-compiler.js`

```js
// src/compiler/create-compiler.js
export function createCompilerCreator (baseCompile: Function): Function {
    return function createCompiler (baseOptions: CompilerOptions) {
        function compile (
          template: string,
          options?: CompilerOptions
        ): CompiledResult {
            const finalOptions = Object.create(baseOptions)
            ....
            const compiled = baseCompile(template.trim(), finalOptions)
            ...
            return compiled
        }
        
        return {
          compile,
          compileToFunctions: createCompileToFunctionFn(compile)
        }
    }
}
```

可以看出这个函数返回了 `createCompiler(baseOptions)` 函数，则往上推可知 **第二步** 中的

```js
// src/platforms/web/compiler/index.js

const { compile, compileToFunctions } = createCompiler(baseOptions)
```

其实就是执行的这里的 `function createCompiler (baseOptions: CompilerOptions){...}`，这个 `createCompiler` 函数里返回了方法 `compile、compileToFunctions`

方法 `compile` 中执行了传入的函数参数 `baseCompile`，这个 `baseCompile` 是 **第三步** 中传入的，其返回值为 `ast、render、staticRenderFns`

而方法 `compileToFunctions` 正是 **第一步** 中调用的 `compileToFunctions(template, options, vm)`，其来自于 `createCompileToFunctionFn(compile)`

### 第五步

`createCompileToFunctionFn` 来自于 `src/compiler/to-function.js`

```js
// src/compiler/to-function.js

export function createCompileToFunctionFn (compile: Function): Function {
    return function compileToFunctions (
        template: string,
        options?: CompilerOptions,
        vm?: Component
      ): CompiledFunctionResult {
        ...
        
        // 1. 读取缓存中的 CompiledFunctionResult 对象，如果有直接返回
        const key = options.delimiters
          ? String(options.delimiters) + template
          : template
        if (cache[key]) {
          return cache[key]
        }
        
        // 2. 把模板编译为编译对象(render, staticRenderFns)，字符串形式的js代码
        const compiled = compile(template, options)
        
        // 3. 把字符串形式的js代码转换成js方法
        res.render = createFunction(compiled.render, fnGenErrors)
        res.staticRenderFns = compiled.staticRenderFns.map(code => {
          return createFunction(code, fnGenErrors)
        })
        
        // 4. 缓存并返回res对象(render, staticRenderFns方法)
        return (cache[key] = res)
    }
}
```

`createCompileToFunctionFn` 返回函数 `compileToFunctions`，即 **第四步** 中 `createCompiler` 函数返回的 `compileToFunctions`，所以是 **第一步** 中调用的 `compileToFunctions` 就是在执行这里的 `compileToFunctions`。

### 总结过程

- 执行 `src/platforms/web/entry-runtime-with-compiler.js` 中的 `compileToFunctions(template, options, vm)`
- 执行 `src/compiler/to-function.js` 中的 `compileToFunctions`，`compileToFunctions` 中调用 `compile(template, options)`
- 执行 `src/compiler/create-compiler.js` 中的 `compile`，`compile` 中调用 `baseCompile(template.trim(), finalOptions)`
- 执行 `src/compiler/index.js` 传入 `createCompilerCreator` 中的函数参数 baseCompile(template, options)，返回 `ast、render、staticRenderFns`
- `src/compiler/create-compiler.js` 中 `const compiled = { ast、render、staticRenderFns }`，返回 `compiled`
- `src/compiler/to-function.js` 中返回 `res`，即返回 `render, staticRenderFns` 方法
- `src/platforms/web/entry-runtime-with-compiler.js` 获取 `render、staticRenderFns`

