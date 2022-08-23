---
title: JavaScript 性能优化
tags: JavaScript
category: 大前端
abbrlink: 53564
date: 2021-05-19 22:54:45
top: false
cover: true
coverImg: http://5coder.cn/img/1661217409_231c34477d76b417436b72abc101413b.jpg
---

## 一、性能优化介绍

- 性能优化时不可避免的

- 哪些内容可以看做是性能优化

  任何一种可以提升程序运行效率，降低程序开销的行为，我们都可以看做是一种优化操作。这就意味着在软件开发的过程中，必然存在着很多值得优化的地方。

- 无处不在的前端性能优化

  特别是在前端开发过程中，性能优化时无处不在的，例如请求资源时的网络、数据的传输方式，开发过程中所使用的的框架等。

本篇的核心是JavaScript语言的优化，具体来说就是认知内存空间的使用，垃圾回收的方式介绍。从而可以让我们编写出高效的JavaScript代码。

**内容概要**：

- 内存管理
  - 为什么内存需要管理
  - 内存管理的基本流程
- 垃圾回收与常见的GC算法
- V8引擎的垃圾回收
  - V8中的GC算法实现垃圾回收
- Performance工具
- 代码优化实例


## 二、内存管理

> Memory Management

### 1.内存为什么需要管理

随着近些年硬件技术的不断发展，同时高级编程语言中也都自带了GC（Garbage Collection）机制，这样的变化，让我们在不需要注意内存使用的情况下，也能够正常的完成相应的功能开发。

```js
function fn() {
    arrList = [];
    arrList[100000] = 'Leo is a coder'
}
fn()
```

上述函数体内定义一个数组，数组长度足够大，为了当前函数在调用的时，程序可以向内存申请比较大的内存空间。执行函数过程中，我们使用性能检测工具，我们会发现，内存变化如下，内存持续升高，且并没有回落，这就是**内存泄漏**。内存泄漏会导致我们的页面处于卡顿状态，因此需要对内存进行人为管理。

![](http://5coder.cn/img/1ygFrKDCSvhGX6m.png)



### 2.内存管理介绍

- 内存：由可读写单元组成，表示一片可操作性空间
- 管理：**人为的去操作**一片空间的申请、使用和释放
- 内存管理：开发者主动申请空间、使用空间、释放空间
- 管理流程：申请-使用-释放

**JavaScript中的内存管理**

和其他语言相通，JavaScript内存管理的流程也是申请内存空间-使用内存空间-释放内存空间。但是由于**ECMAScript中并没有提供操作内存的相关API**，所以JavaScript语言不能像C或者C++那样，由开发者主动去调用相应的API来完成内存管理。不过，我们仍然可以通过js脚本去演示当前空间的生命周期是怎样完成的。

```js
// 申请空间
let obj = {}
// 使用空间
obj.name = 'Leo'
// 释放空间
obj = null
```

### 3.JavaScript中的垃圾回收

 JavaScript中的垃圾

- JavaScript中的内存管理时自动的
- 对象不再被引用时是垃圾
- 对象不能从根上访问到时是垃圾

JavaScript中的可达对象

- 可以访问到的对象就是可达对象（引用、作用域链）
- 可达的标准就是从根触发是否能够被找到
- JavaScript中的根可以理解为全局变量

引用说明代码示例：

```js
let obj = {name:'leo'};  // obj引用leo对象，全局可达
let bai = obj;  // bai引用leo内存地址
obj = null;  // obj不再引用，但bai依然在引用
```

可达说明代码示例：

```js
function objGroup(obj1, obj2){
    obj1.next = obj2;
    obj2.prev = obj1;
    
    return {
        o1:obj1,
        o2:obj2
    }
}
let obj = objGroup({name:'obj1'}, {name:'obj2'})
console.log(obj)
// {
//     o1: {name: 'obj1', next: {name: 'obj2', prev: [Circular]}},
//     o2: {name: 'obj2', prev: {name: 'obj1', prev: [Circular]}},   
// }
```

**可达对象图示**

![](http://5coder.cn/img/dnkGj8bH4vzoZCp.png)


如果我们在代码中做一些操作，比如使用delete将obj上的o1的应用以及o2中对obj1的应用删除掉，那么出现下面的情况：o1无法被找到，则被标记为垃圾。

![](http://5coder.cn/img/WgRhFJ7xmadZzfu.png)



## 三、GC算法介绍

### 1.GC定义与作用

- GC就是垃圾回收机制的简写（Garbage Collection）
- GC可以找到内存中的垃圾、并释放和回收空间

### 2.GC里的垃圾是什么

- 程序中不再需要使用的对象

  ```js
  function func() {
      name = 'leo';
      return `${name} is a coder`
  }
  func()
  ```

  上面例子中，当我们函数调用完成后，name不再被需要，因此它成为了一个垃圾

- 程序中不能再访问到的对象

  ```js
  function func() {
      const name = 'leo';
      return `${name} is a coder`
  }
  func()
  ```

  上面例子中，由于使用了const关键字进行声明变量，因此当函数执行结束后，外界无法再访问到它，它也会成为一个垃圾。

### 3.GC算法是什么

- GC是一种机制，垃圾回收器完成具体的工作
- 工作内容就是查找垃圾、释放空间、回收空间
- 算法就是工作时查找和回收所遵循的规则

常见的GC算法有以下几种：

- 引用计数
- 标记清除
- 标记整理
- 分代回收

### 4.引用计数算法

所谓的引用计数法就是给每个对象一个引用计数器，每当有一个地方引用它时，计数器就会加1；当引用失效时，计数器的值就会减1；任何时刻计数器的值为0的对象就是不可能再被使用的。

这个引用计数法时没有被Java所使用的，但是python有使用到它。而且最原始的引用计数法没有用到GC Roots。

- 核心思想：设置引用数，判断当前引用数是否为0
- 引用计数器
- 引用关系改变时修改引用数字
- 引用数字为0时立即回收

**优点：**

1. 可即时回收垃圾，在该方法中，每个对象始终知道自己是否有被引用，当被引用的数值为0时，对象马上可以把自己当做空闲空间链接到空闲链表；
2. 最大暂停时间短；
3. 没有必要沿着指针查找；

**缺点：**

1. 计数器的增减处理非常繁重；
2. 计算器需要占用很多位；
3. 实现繁琐；
4. 循环引用无法回收；

### 5.标记清除算法

该算法分为**标记**和**清除**两个阶段。标记就是把所有活动对象都做上标记的阶段；清除就是将没有做上标记的对象进行回收的阶段。

- 核心思想：分标记和清除两个阶段完成
- 遍历所有对象找标记活动对象
- 遍历所有对象清除没有标记对象
- 回收相应的空间

![](http://5coder.cn/img/EbjthkT2PHoQWar.png)



**优点：**

1. 实现简单
2. 与保守式GC算法兼容（保守式GC在后面介绍）

**缺点：**

![](http://5coder.cn/img/1661161556_6cda0071f708177d2abb214294ebde19.png)

1. 碎片化：如上图所示，在回收过程中会产生被细化的分块，到后面，即时堆中分块的总大小够用，但是却因为分块太小而不能执行分配
2. 分配速度：因为分块不是连续的，因此每次分块都要遍历空闲链表，找到足够大的分块，从而造成时间短的浪费
3. 与写时复制技术不兼容：所谓写时复制就是fork的时候，内存空间只引用而不复制，只有当该进程的数据发生变化时，才会将数据复制到该进程的内存空间。这样，当两个进程中的内存数据相同的时候，就能节约大量的内存空间了。而对于标记-清除算法，它的每个对象都有一个标志位来表示它是否被标记，在每一次运行标记-清除算法的时候，被引用的对象都会进行标记操作，这个仅仅标记位的改变，也会变成对象数据的改变，从而引发写时复制的复制过程，与写时复制的初衷就背道而驰了。

### 6.标记整理算法

标记-整理算法与标记-清理算法类似，只是后续步骤是让所有存活的对象移动到一端，然后直接清除掉端边界以外的内存。

- 标记整理可以看作是标记清除的增强
- 标记阶段的操作和标记清除一致
- **清除阶段会先执行整理，移动对象位置**
  ![](http://5coder.cn/img/fix37uO2hUNelFv.png)
  ![](http://5coder.cn/img/YEVdhFxWa9CJPHw.png)


优缺点：该算法可以有效的利用堆，但是整理需要花比较多的时间成本

## 四、V8引擎

### 1.认识V8

- V8引擎是一个JavaScript实现，最初由一些语言方面专家设计，后被谷歌收购，随后谷歌对其进行了开源；
- V8使用c++开发，在运行JavaScript之前，相比其他的JavaScript的引擎转换成字节码或解释执行，V8将其编译成原生机器码（IA-32, x86-64, ARM, or MIPS CPUs），并且使用了如**内联缓存**（Inline caching）等方法来提高性能
- 有了这些功能，JavaScript程序在V8引擎下的运行速度媲美二进制程序
- V8支持众多操作系统，如Windows、Linux、Android等，也支持其他硬件架构，如IA32、X64、ARM等，具有很好的可移植和跨平台特性
- V8内存设限（64位1.5GB，32位不超过800MB）

### 2.V8垃圾回收策略

- 采用分代回收的思想
- 内存分为新生代、老生代
- 针对不同对象采用不同算法

V8 使用了分代和大数据的内存分配，在回收内存时使用精简整理的算法标记未引用的对象，然后消除没有标记的对象，最后整理和压缩那些还未保存的对象，即可完成垃圾回收。

![](http://5coder.cn/img/UDEPWurlJf38TgN.png)


**V8中常用的GC算法**

- 分代回收
- 空间复制
- 标记清除
- 标记整理
- 标记增量

### 3.V8回收新生代对象

> **年轻分代**中的对象垃圾回收主要通过Scavenge算法进行垃圾回收。在Scavenge的具体实现中，主要采用了Cheney算法：通过复制的方式实现的垃圾回收算法。它将堆内存分为两个 semispace，**一个处于使用中（From空间）**，**另一个处于闲置状态（To空间）**。当分配对象时，先是在From空间中进行分配。当开始进行垃圾回收时，会检查From空间中的存活对象，这些存活对象将被复制到To空间中，而非存活对象占用的空间将会被释放。完成复制后，From空间和To空间的角色发生对换。在垃圾回收的过程中，就是通过将存活对象在两个 semispace 空间之间进行复制。
>
> **年轻分代中的对象有机会晋升为年老分代，条件主要有两个：一个是对象是否经历过Scavenge回收，一个是To空间的内存占用比超过限制。**

![](http://5coder.cn/img/8MIBQo1xF6SYPz4.png)

V8**内存分配**

- V8内存空间一分为二
- 小空间用于存储新生代对象（32M|16M）（From+To）
- 新生代值得是存货时间较短的对象

**新生代对象回收实现**

- 回收过程采用复制算法+标记整理算法
- 新生代内存分为两个等大小空间
- 使用空间为From，空闲空间为To
- 活动对象存储于From空间
- 标记整理后将活动对象拷贝至To
- From与To交换空间完成释放
- 回收细节说明：
  - 拷贝过程中可能出现晋升
  - 晋升就是将新生代对象移动至老生代
  - 一轮GC还存活的新生代需要晋升
  - To的使用率超过25%

![](http://5coder.cn/img/1661175081_4eed18a482b32b1ce1ce23ac145b288d.png)

### 4.V8回收老生代对象

- 老年代对象放在右侧老生代区域
- **64位操作系统1.4G，32位操作系统700M**
- 老年代对象就是指存活时间较长的对象（全局变量、闭包中的数据）

> 对于年老分代中的对象，由于存活对象占较大比重，再采用上面的方式会有两个问题：一个是存活对象较多，复制存活对象的效率将会很低；另一个问题依然是浪费一半空间的问题。为此，V8在年老分代中主要采用了Mark-Sweep（标记清除）标记清除和Mark-Compact（标记整理）相结合的方式进行垃圾回收。

**老年代对象回收实现**

- 主要采用标记清除、标记整理、增量标记
- 首先使用标记清除完成垃圾空间的回收（主要采用标记清除）
- 采用标记整理进行空间优化（当新生代中的内容往老生代移动时，当老生代空间不足的时候，会进行整理空间）
- 采用增量标记进行效率优化

老生代与新生代回收对象细节对比：

- 新生代区域垃圾回收使用空间换时间-复制算法。每时每刻都会有空闲的空间存在，但是该部分空间很小。
- 老生代区域垃圾回收不适合复制算法
  - 老生代存储空间比较大，一分为二的话就会有大量的空间被浪费
  - 老生代数据比较多，复制时消耗的时间就会比较多


**增量标记优化垃圾回收**

![](http://5coder.cn/img/15sl9QVXnHtSxwo.png)

图示中，程序在标记阶段被暂停运行，等待标记完成自动运行，当遇到大块需要标记的对象时，程序需要暂停很长一段时间，对用户体验很不友好，因此采用增量标记，将一大块分解为多个小块进行标记，减少每次程序暂停的时长，优化用户体验。最后标记完成后统一进行回收。例如第一步先遍历查找第一层可达的属性，第二步进行查找第二层可达，最终完成清除。这样的垃圾回收对用户暂停的体验就比较友好了。

### 5.V8垃圾回收总结

- V8是一款主流的JavaScript引擎
- V8设置内存上限
- V8采用基于分代回收思想实现垃圾回收
- V8内存分为新生代和老生代
- V8垃圾回收常见的GC算法

## 五、Performance工具

### 1.Performance工具介绍

使用Chrome DevTools的**performance**面板可以记录和分析页面在运行时的所有活动。

为什么我们需要使用Performance工具，其原因有以下几点：

- GC的目的是为了实现内存空间的良性循环
- 良性循环的基石是合理使用
- 时刻关注才能确定是否合理
- 由于ECMAScript中未向开发者提供操作内存空间的API
- Performance工具提供了多种监控方式

Performance使用步骤为：

1. 打开浏览器输入目标地址
2. 进入开发人员工具面板（F12），选择Performance
3. 开启录制功能，访问具体界面
4. 执行用户行为，一段时间后停止录制
5. 分析界面中记录的内存信息

### 2.内存问题的体现

内存问题的体现分为外在表现和内在表现。

内存问题的外在表现：

- 页面出现延迟加载或经常性暂停
- 页面持续性出现糟糕的性能
- 页面的性能随时间延长越来越差

内存问题的内在表现：

- 内存泄漏：内存使用持续升高
- 内存膨胀：在多数设备上都存在性能问题
- 频繁垃圾回收：通过内存变化图进行分析

### 3.监控内存的几种方式

#### 3.1任务管理器监控内存

打开浏览器，按键【Shift】+ 【Esc】，调出浏览器任务管理器。找到我们的目标标签页，刚开始可能没有JavaScript内存，可以在目标标签页任务上右键，然后选择JavaScript内存。

记录JavaScript内存（**JavaScript堆占用的内存，表示界面中所有可达对象占用的内存**）及内存占用空间（**原生内存，DOM节点占用的内存**），点击按钮，记录每次内存的变化。

![](http://5coder.cn/img/SPLj7pfv2G8uIgr.gif)

> 注意：以上动图中，数组超过最大长度，为录制的时候失误，请调整数组长度后，点击按钮进行观察结果
>
> array的最大长度为Math.pow(2,32)-1
> var arr = new Array(Math.pow(2,32));//报错Invalid array length
> 为什么呢，无符号int型的最大长度为2的32次方-1
> 为什么是2的32次方-1
> 整型为4个字节，一个字节8，即32位，本来第一位为符号位，无符号整型就从第一位开始计数了，所以范围为0到2的32次方-1

#### 3.2Timeline记录内存

上述浏览器任务管理器更多的是用于判断当前脚本是否存在内存问题，而不能具体定位到问题。我们使用Timeline时间线记录内存变化，更精确的记录到内存变化。

![](http://5coder.cn/img/R7IQYzxwmM5WTnK.gif)


#### 3.3堆快照查找分离DOM

什么是分离DOM

- 界面元素存货在DOM树上
- 垃圾对象时的DOM节点（当前DOM从存活的DOM树上分离，且js中没有应用这个DOM）
- 分离状态的DOM节点（当前DOM节点从当前DOM树分离，但js中还在应用它）

![](http://5coder.cn/img/sG2P5SjBt6xdKRU.gif)


在点击按钮后，DOM中生成了分离的DOM，造成内存空间的浪费，因此我们需要将代码中的temEle置空，这样让GC对垃圾进行回收即可。

#### 3.4判断是否存在频繁GC

为什么要确定频繁垃圾回收

- GC工作时应用程序是停止的
- 频繁且过长的GC会导致应用假死
- 用户使用中感知应用卡顿

确定频繁的垃圾回收：

- Timeline中频繁的上升下降
- 任务管理器中的数据频繁增加减小

## 六、代码优化

### 1.代码优化介绍

如何精准测试JavaScript性能：

- 本质上就是采集大量的执行脚本进行数学统计和分析
- 使用基于Benchmark.js的https://jsbench.me/使用

![](http://5coder.cn/img/dK9hqBWRvkMaZEy.png)


代码需要优化的原因：

- JavaScript中的内存管理自动完成
- 执行引擎会使用不同的GC算法
- 算法工作的目的是为了实现内存空间良性循环
- Performance工具检测内存变化
- JavaScript是单线程机制的解释性语言

### 2.慎用全局变量及缓存全局变量

全局变量的特点：

- 全局变量挂载在window下
- 全局变量至少有一个引用计数
- 全局变量存货更久，但持续占用内存

全局查找相关：

- 目标变量不存在于当前作用域内，通过作用域链向上查找
- 减少全局查找降低的时间消耗
- 减少不必要的全局变量定义
- 全局变量数据局部化

慎用全局变量：

- 全局变量定义在全局执行上下文，是否有作用域链的顶端
- 全局执行上下文一直存在于上下文执行栈，指导程序退出
- 如果某个局部作用于初夏了同名的变量则会遮蔽或午饭全局

**慎用全局变量**代码演示：

```js
function fn() {
  name = 'lg'
  console.log(`${name} is a coder`)
}

fn() 


function fn() {
  const name = 'lg'
  console.log(`${name} is a coder`)
}

fn() 
```

测试结果：

![](http://5coder.cn/img/IHKBSgCf3hk5eT7.png)


```js
var i, str = ''
for (i = 0; i < 1000; i++) {
  str += i
}

for (let i = 0; i < 1000; i++) {
  let str = ''
  str += i
}

```

![](http://5coder.cn/img/YCe95UdsnzbRIGy.png)


**缓存全局变量**代码演示：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>缓存全局变量</title></head>
<body><input type="button" value="btn" id="btn1"> <input type="button" value="btn" id="btn2"> <input type="button"
                                                                                                     value="btn"
                                                                                                     id="btn3"> <input
        type="button" value="btn" id="btn4">
<p>1111</p>  <input type="button" value="btn" id="btn5"> <input type="button" value="btn" id="btn6">
<p>222</p>  <input type="button" value="btn" id="btn7"> <input type="button" value="btn" id="btn8">
<p>333</p>  <input type="button" value="btn" id="btn9"> <input type="button" value="btn" id="btn10">
<script>    function getBtn() {
  let oBtn1 = document.getElementById('btn1')
  let oBtn3 = document.getElementById('btn3')
  let oBtn5 = document.getElementById('btn5')
  let oBtn7 = document.getElementById('btn7')
  let oBtn9 = document.getElementById('btn9')
}

function getBtn2() {
  let obj = document
  let oBtn1 = obj.getElementById('btn1')
  let oBtn3 = obj.getElementById('btn3')
  let oBtn5 = obj.getElementById('btn5')
  let oBtn7 = obj.getElementById('btn7')
  let oBtn9 = obj.getElementById('btn9')
}  </script>
</body>
</html>
```

测试结果：

![](http://5coder.cn/img/qkaxNHsS9b51AV7.png)


### 3.通过原型对象添加附加方法

代码演示：

```js
var fn1 = function () {
  this.foo = function () {
    console.log(11111)
  }
}
let f1 = new fn1()
var fn2 = function () {
}
fn2.prototype.foo = function () {
  console.log(11111)
}
let f2 = new fn2()
```

测试结果：

![](http://5coder.cn/img/gB4rej8DLWpXE1V.png)


### 4.避开闭包陷阱

关于闭包：

- 闭包是一种强大的语法
- 闭包使用不当很容易出现内存泄漏
- 不要为了闭包而闭包

代码示例：

```js
function test(func) {
  console.log(func())
}

function test2() {
  var name = 'lg'
  return name
}

test(function () {
  var name = 'lg'
  return name
})
test(test2)
```

### 5.避免属性访问方法使用

- JavaScript不需要属性的访问方法，所有属性都是外部可见的
- 使用属性访问方法只会增加一层重定义，没有访问的控制力

代码示例：

```js
function Person() {
  this.name = 'icoder'
  this.age = 18
  this.getAge = function () {
    return this.age
  }
}

const p1 = new Person()
const a = p1.getAge()

function Person() {
  this.name = 'icoder'
  this.age = 18
}

const p2 = new Person()
const b = p2.age
```

测试结果：

![](http://5coder.cn/img/DJc2S8mXkajpEtM.png)


### 6.For循环优化及选择最优循环方法

代码示例：

```js
var arrList = []
arrList[10000] = 'icoder'
for (var i = 0; i < arrList.length; i++) {
  console.log(arrList[i])
}
for (var i = arrList.length; i; i--) {
  console.log(arrList[i])
}
```

测试结果：

![](http://5coder.cn/img/Wxw3UcVpADs6IjO.png)


**选择最优循环方法**

代码示例：

```js
var arrList = new Array(1, 2, 3, 4, 5)
arrList.forEach(function (item) {
  console.log(item)
})
for (var i = arrList.length; i; i--) {
  console.log(arrList[i])
}
for (var i in arrList) {
  console.log(arrList[i])
}
```

测试结果（forEach效率最高）：

![](http://5coder.cn/img/tes9K4yoF3XQH6T.png)


### 7.文档碎片优化节点添加、克隆优化节点操作

代码示例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>优化节点添加</title></head>
<body>
<script>    for (var i = 0; i < 10; i++) {
  var oP = document.createElement('p')
  oP.innerHTML = i
  document.body.appendChild(oP)
}
const fragEle = document.createDocumentFragment()
for (var i = 0; i < 10; i++) {
  var oP = document.createElement('p')
  oP.innerHTML = i
  fragEle.appendChild(oP)
}
document.body.appendChild(fragEle)  </script>
</body>
</html>
```

测试结果：

![](http://5coder.cn/img/rvEJSaMpK26j54Z.png)


**克隆优化节点操作**

代码示例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>克隆优化节点操作</title></head>
<body><p id="box1">old</p>
<script>    for (var i = 0; i < 3; i++) {
  var oP = document.createElement('p')
  oP.innerHTML = i
  document.body.appendChild(oP)
}
var oldP = document.getElementById('box1')
for (var i = 0; i < 3; i++) {
  var newP = oldP.cloneNode(false)
  newP.innerHTML = i
  document.body.appendChild(newP)
}  </script>
</body>
</html>
```

测试结果：

![](http://5coder.cn/img/fzEUXm5dwyingl7.png)


### 8.直接量替换new Object

代码示例：

```js
var a = [1, 2, 3]
var a1 = new Array(3)a1[0] = 1a1[1] = 2a1[2] = 3
```

测试结果：
![](http://5coder.cn/img/BUjOkDgVzJPSIT9.png)

### 9.堆栈中的JS执行过程

```js
let a = 10;

function foo(b) {
  let a = 2;

  function baz(c) {
    console.log(a + b + c);
  }

  return baz
}

let fn = foo(2);
fn(3);
```

![](http://5coder.cn/img/FgN4vncbWzUrQp9.jpg)


### 10.减少判断层

```js
function doSomething(part, chapter) {
  const parts = ['ES2015', '工程化', 'Vue', 'Reach', 'Node'];
  if (part) {
    if (parts.includes(part)) {
      console.log('属于当前课程')
      if (chapter > 5) {
        console.log('您需要提供VIP身份')
      }
    }
  } else {
    console.log('请确认模块信息')
  }
}

doSomething('ES2015', 6)

function doSomething2(part, chapter) {
  const parts = ['ES2015', '工程化', 'Vue', 'Reach', 'Node'];
  if (!part) {
    console.log('确认模块信息')
    return
  }
  if (!parts.includes(part)) return;
  console.log('属于当前课程')
  if (chapter > 5) {
    console.log('您需要提供VIP身份')
  }
}

doSomething2('ES2015', 6)
```

### 11.减少作用域链查找层级

代码示例：

```js
var name = 'zce';

function foo() {
  name = 'zce666'  // 这里的name是全局的    
  function baz() {
    var age = 28
    console.log(age)
    console.log(name)
  }

  baz()
}

foo()
var name = 'zce';

function foo() {
  var name = 'zce666'// 这里的name是全局的    
  function baz() {
    var age = 28
    console.log(age)
    console.log(name)
  }

  baz()
}
foo()
```

测试结果：

![](http://5coder.cn/img/eFGblMkyauDAO8K.png)


### 12.减少数据读取次数

代码示例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>减少数据读取次数</title></head>
<body>
<div id="skip" class="skip"></div>
<script>        var oBox = document.getElementById('skip')

function hasEle(ele, cls) {
  return ele.className === cls
}

function hasEle(ele, cls) {
  var className = ele.className
  return className === cls
}

console.log(hasEle(oBox, 'skip'))    </script>
</body>
</html>
```

测试结果：

![](http://5coder.cn/img/53YtRCWn2o1jsaT.png)


### 13.字面量与构造式

代码示例：

```js
var test = () => {
  let obj = new Object();
  obj.name = 'zce';
  obj.age = '28';
  obj.slogan = '我为前端而活'
  return obj
}
var test = () => {
  let obj = {name: 'zce', age: '28', slogan: '喔喔前端而活'}
  return obj
}
console.log(test())
```

测试结果：

![](http://5coder.cn/img/LUPtoS5zT64Nx8B.png)


### 14.减少循环体中活动

代码示例：

```js
var test = () => {
  var i
  var arr = ['zce', 28, '我为前端而活']
  for (let i = 0; i < arr.length; i++) {
    console.log(arr[i])
  }
}
var test = () => {
  var i
  var arr = ['zce', 28, '我为前端而活']
  var len = arr.length
  for (let i = 0; i < len; i++) {
    console.log(arr[i])
  }
}
```

测试结果：

![](http://5coder.cn/img/Lw4hojUnXibfu2x.png)

### 15.惰性函数与性能

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title></head>
<body>
<button id="btn"></button>
<script>        var oBtn = document.getElementById('btn');

function foo() {
  console.log(this)
}

function addEvent(obj, type, fn) {
  if (obj.addEventListener()) {
    obj.addEventListener(type, fn, false)
  } else if (obj.attachEvent) {
    obj.attachEvent('on' + type, fn)
  } else {
    obj['on' + type] = fn
  }
}

function addEvent(obj, type, fn) {
  if (obj.addEventListener()) {
    addEvent = obj.addEventListener(type, fn, false)
  } else if (obj.attachEvent) {
    addEvent = obj.attachEvent('on' + type, fn)
  } else {
    addEvent = obj['on' + type] = fn
  }
  return addEvent
}        </script>
</body>
</html>
```

### 16.减少声明及语句数

代码示例：

```js
var test = () => {
  let w = 200
  let h = 300
  return w * h
}
var test = () => {
  return 200 * 300
}
```

### 17.采用事件绑定

代码示例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title></head>
<body>
<ul id="ul">
    <li>Leo</li>
    <li>28</li>
    <li>我为前端而活</li>
</ul>
<script>    var list = document.querySelectorAll('li')

function showText(ev) {
  console.log(ev.target.innerHTML)
}

for (let listElement of list) {
  item.onclick = showText
}
var oUl = document.getElementById('ul')
oUl.addEventListener('click', showText, true)</script>
</body>
</html>
```

