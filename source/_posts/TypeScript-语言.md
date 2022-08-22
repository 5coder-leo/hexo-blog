---
title: TypeScript 语言
tags: TypeScript
category: 大前端
abbrlink: 50148
date: 2021-05-19 22:54:34
top: false
---

# TypeScript语言-前置知识

## ①、强类型与弱类型、静态类型与动态类型

### 1.强类型与弱类型（类型安全）

**①、强类型语言**：强类型语言也称为强类型定义语言。是一种总是强制类型定义的语言，要求变量的使用要严格符合定义，所有变量都必须先定义后使用。**java、.NET、C++**等都是强制类型定义的。也就是说，一旦一个变量被指定了某个数据类型，如果不经过强制转换，那么它就永远是这个数据类型了。

1974年美国两个专家做出解释：语言层面限制函数的实参类型必须与形参类型相同

个人理解：强类型语言不允许有各种方式的隐式转换

例如你有一个整数，如果不显式地进行转换，你不能将其视为一个字符串。

```java
class Main {
    // 接受一个整形的参数
    static void foo(int num) {
        System.out.println(num);
    }
    
    public static void main(String[] args) {
        Main.foo(100);  // ok
        
        Main.foo("100"); // error "100" is a string，不允许传入其他类型的值
        
        Main.foo(Interger.parseInt("100"))  // ok，强制类型转换
    }
}
```

```shell
D:\DeskTop\lagou\Flow>python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> '100' - 50
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for -: 'str' and 'int'
>>> abs('foo')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: bad operand type for abs(): 'str'
>>>
```

与其相对应的是弱类型语言：数据类型可以被忽略的语言。它与强类型定义语言相反， 一个变量可以赋不同数据类型的值。

**②、弱类型语言：**弱类型语言也称为弱类型定义语言。与强类型定义相反。像**vb、php、js**等就属于弱类型语言，语言层面不会限制实参的类型。

个人理解：弱类型语言则允许任意的数据隐式类型转换

```js
function (num) {
    console.log(num);
}
foo(100); // ok
foo('100');  // ok
foo(parseInt('100'));  // ok
```

```shell
Microsoft Windows [版本 10.0.18363.1139]
(c) 2019 Microsoft Corporation。保留所有权利。

D:\DeskTop\lagou\Flow>node
Welcome to Node.js v12.19.0.
Type ".help" for more information.
> '100' - 50
50
> Math.floor('foo')
NaN
> Math.floor(true)
1
```

JavaScript中所有的类型错误都是在代码执行（逻辑判断）的过程中抛出的，并不是在语法层面进行抛出。

### 2.静态类型与动态类型（类型检查）

- 静态类型语言

  一种在编译时，数据类型是固定的语言。大多数静态类型定义语言强制这一点，它要求你在使用所有变量之前要声明它们的数据类型。Java和C是静态类型定义语言。

- 动态类型语言

  一种在执行期间才去发现数据类型的语言，与静态类型定义相反。VBScript和Python是动态类型定义的，因为它们是在第一次给一个变量赋值的时候找出它的类型的。

  ```js
  var foo = 100;
  foo = 'bar';
  console.log(foo);
  // 在JavaScript中，变量是没有类型的。而变量中存放的值是有类型的
  ```

![](http://5coder.cn/img/fPas346JDgeFwyu.png)


### 3.JavaScript类型系统特征

JavaScript为弱类型且动态类型，语言本身的系统非常薄弱，甚至说JavaScript根本没有类型系统----【任性】，其缺失类型系统的可靠性【不靠谱】。

早期JavaScript的目的并没有想到去处理很多程序，很多项目只有几十行上百行代码。

### 4.弱类型的问题及强类型的优势

- **弱类型的问题**，运行阶段才能发现类型异常问题。例如在setTimeout中，当时间结束时才会发现错误，如果调试过程中没有等到足够的时间，那么这个类型错误就会形成隐患。

示例一：运行时才能发现错误

```js
const obj = {};
obj.foo();

// obj.foo();
// ^
//
// TypeError: obj.foo is not a function
// at Object.<anonymous> (D:\DeskTop\lagou\Flow\01\01-getting-started.js:2:5)
// at Module._compile (internal/modules/cjs/loader.js:1015:30)
// at Object.Module._extensions..js (internal/modules/cjs/loader.js:1035:10)
// at Module.load (internal/modules/cjs/loader.js:879:32)
// at Function.Module._load (internal/modules/cjs/loader.js:724:14)
// at Function.executeUserEntryPoint [as runMain] (internal/modules/run_main.js:60:12)
// at internal/main/run_main_module.js:17:47
```

示例二：非预期结果

```js
function sum(a, b) {
	return a + b;
}

console.log(sum(100, 100));
console.log(sum('100', '100'));

// 200
// 100100
```

示例三：数据错误

```js
const obj = {};
obj[true] = 100
console.log(obj['true']);  // 100
```

- **强类型的优势**：错误更早的暴露、代码更智能，编码更准确、重构更方便、减少不必要的类型判断

## ②、Flow概述及方法

### 1.概述

flow是 facebook 出品的 JavaScript **静态类型检查工具，https://flow.org/en/docs/usage/**  这是其官方文档链接。Vue.js 的源码利用了Flow 做了静态类型检查。

**JavaScript** 是**动态类型语言**，它的灵活性有目共睹，但是过于灵活的副作用是很容易就写出**非常隐蔽的隐患代码**，在**编译期**甚至看上去都**不会报错**，但在**运行阶段**就可能出现**各种奇怪的 bug**

**类型检查的定义**：类型检查，就是在**编译期**尽早发现（**由类型错误引起的**）bug，又**不影响代码运行**（不需要运行时动态检查类型），使编写 JavaScript 具有和编写 Java 等强类型语言相近的体验

**在vue中使用Flow做静态类型检查**，是因为 **Babel** 和 **ESLint** 都有对应的 **Flow 插件**以支持语法，可以完全沿用**现有的构建配置**，非常小成本的改动就可以拥有**静态类型检查的能力**

类型注解

```js
function add(x: number, y: number): number {
  return x + y      //x的类型是number,y的类型是number，函数的返回值类型是number
}
add('Hello', 11)
```

### 2.快速上手

1. 初始化模块

   - yarn init -yes

2. 安装flow

   - yarn add flow-bin -dev

3. 使用flow类型注解

   - 必须在文件文件开始处标记：@flow

   - 关闭VS Code语法校验：setting，搜索JavaScript validate，找到enable，取消勾选


```js

// @flow

function sum(a:number, b:number) {
	return a + b;
}

sum(100, 100)
sum('100', '100')

let num:number = 100
num = '100'
```

使用

```shell
yarn flow init
yarn flow  # 第一次会很慢，后续会很快
# yarn flow stop # 结束flow

#Error ---------------------------------------------------------------------------------------------------- 01/01.js:8:12

#Cannot call `sum` with `'100'` bound to `b` because string [1] is incompatible with number [2]. [incompatible-call]

#   01/01.js:8:12
#   8| sum('100', '100')
#                 ^^^^^ [1]

#References:
#   01/01.js:3:26
#   3| function sum(a:number, b:number) {
#                               ^^^^^^ [2]

```

### 3.编译移除注解

- 方案一：自动移除类型注解，官方提供的模块：flow-remove-types

```shell
yarn add flow-remove-types --dev
yarn flow-remove-types . -d dist
# yarn flow-remove-types [需要移除注解的文件，一般为src] -d [输出目录，如果不存在则新建，一般为dist]
```

- 方案二：babel

```shell
yarn add @babel/core @babel/cli @babel/preset-flow --dev
```

然后在项目中添加项目文件-【.babelrc】,然后在文件中输入：

```js
{
    "presets":["@babel/preset-flow"]
}
```

随后使用命令行

```shell
yarn babel src -d dist
```

### 4.开发者工具插件

> **VS Code搜索插件【flow language support】,flow官方提供的插件，可以实时显示类型异常。**默认情况下，修改完代码，需要重新保存后才会检测类型异常。
>
> flow官网：https://flow.org/en/docs/editors

### 5.类型推断

flow支持在代码编写过程中就进行类型推断，例如下面代码中，需要算一个数的平方，当传入非数字类型时，flow会进行代码提示，抛出类型错误。

```js
// @flowfunction square(n: number) {	return n * n;}square('100')
```

### 6.类型注解

在绝大多数情况下一样，它可以帮我们推断出来变量，或者是参数的具体类型，但是没有必要给所有的成员都去添加，它可以更明确的去限制类型注解，而且对我们后期去理解，也是有帮助的可能去使用。

```js
let num:number = 100;// num = 'string',此时只能赋值数字类型function foo():number {    return 100}// 此时函数只能返回数字类型，如果函数没有返回值，默认返回undefined，那么也会提醒报错。没有返回值的函数，我们需要将函数返回值类型标注为void
```

### 7.原始类型

在用法上flow，几乎没有任何的难度，无外乎就是使用flow命令去根据我们代码当中添加的类型注解，去检测我们代码当中的那些类型使用上的异常。值得我们再去了解的无外乎就是flow当中，具体支持哪些类型，以及，我们在类型注解上有没有一些更高级的用法，这里呢，我们具体来看。

flow中能使用的类型有很多，最简单的就是JavaScript中的原始类型，目前原始类型共有6中，number、Boole、string、null、undefined、symbol。以下进行快速尝试：

```js
/**
 * 原始类型
 *
 * @flow
 */

const a: string = 'foobar'

const b: number = Infinity // NaN // 100

const c: boolean = false // true

const d: null = null

const e: void = undefined

const f: symbol = Symbol()
```

### 8.数组类型

```js
/**
 * 数组类型
 *
 * @flow
 */

const arr1: Array<number> = [1, 2, 3]

const arr2: number[] = [1, 2, 3]

// 元组
const foo: [string, number] = ['foo', 100]
```

### 9.对象类型

```js
/**
 * 对象类型
 *
 * @flow
 */

const obj1: { foo: string, bar: number } = { foo: 'string', bar: 100 }

const obj2: { foo?: string, bar: number } = { bar: 100 }

const obj3: { [string]: string } = {}

obj3.key1 = 'value1'
obj3.key2 = 'value2'
```

### 10.函数类型

```js
/**
 * 函数类型
 *
 * @flow
 */

function foo (callback: (string, number) => void) {
  callback('string', 100)
}

foo(function (str, n) {
  // str => string
  // n => number
})
```

### 11.特殊类型

```js
/**
 * 特殊类型
 *
 * @flow
 */

// 字面量类型

const a: 'foo' = 'foo'

const type: 'success' | 'warning' | 'danger' = 'success'

// ------------------------

// 声明类型

type StringOrNumber = string | number

const b: StringOrNumber = 'string' // 100

// ------------------------

// Maybe 类型

const gender: ?number = undefined
// 相当于
// const gender: number | null | void = undefined

```

### 12.Mixed与Any

```js
/**
 * Mixed Any
 *
 * @flow
 */

// string | number | boolean | ....
function passMixed (value: mixed) {
  if (typeof value === 'string') {
    value.substr(1)
  }

  if (typeof value === 'number') {
    value * value
  }
}

passMixed('string')

passMixed(100)

// ---------------------------------

function passAny (value: any) {
  value.substr(1)

  value * value
}

passAny('string')

passAny(100)
```

# TypeScript语言

## 一、TypeScript概述

TypeScript是一种由微软开发的自由和开源的编程语言。它是 JavaScript 的一个超集，而且本质上向这个语言添加了可选的静态类型和基于类的面向对象编程。

TypeScript 扩展了 JavaScript 的句法，所以任何现有的 JavaScript 程序可以不加改变的在 TypeScript下工作。TypeScript 是为大型应用之开发而设计，而编译时它产生 JavaScript 以确保兼容性。任何一种JavaScript运行环境都支持TypeScript开发。

- 缺点一：语言多了很多概念，提高学习成本。但其属于渐进式的，所以可以按照JavaScript标准语法来使用，在学习过程中了解到一个特性就可以使用一个特性。

- 缺点二：项目初期，TypeScript会增加一些时间成本，需要很多的类型声明。

## 二、TypeScript快速上手

1. 安装TypeScript

   ```shell
   yarn init --yes  # 初始化项目目录
   yarn add typescript --dev  # 开发依赖
   ```

2. 新建TypeScript文件，文件名01-getting-started.ts,其文件扩展名默认为**.ts**

   ```js
   // 可以完全按照 JavaScript 标准语法编写代码
   
   const hello = (name: any) =>  {
     console.log(`Hello, ${name}`)
   }
   
   hello('TypeScript')
   ```

3. 使用TypeScript编译上述文件

   ```shell
   yarn tsc 01-getting-started.ts
   ```

   编译后的文件01-getting-started.js：

   ```js
   "use strict";
   // 可以完全按照 JavaScript 标准语法编写代码
   var hello = function (name) {
       console.log("Hello, " + name);
   };
   hello('TypeScript');
   //# sourceMappingURL=01-getting-started.js.map
   ```

## 三、TypeScript配置文件

tsc不仅仅可以编译单个文件，还可以编译整个项目或者整个工程。在编译整个项目前，我们需要先给整个项目创建一个TypeScript的配置文件。

使用命令自动生成配置文件：

```shell
yarn tsc --init
```

在根目录下会多出tsconfig.json文件

```js
{
  "compilerOptions": {
    /* Basic Options */
    // "incremental": true,                   /* Enable incremental compilation */
    "target": "ES2015",                          /* Specify ECMAScript target version: 'ES3' (default), 'ES5', 'ES2015', 'ES2016', 'ES2017', 'ES2018', 'ES2019' or 'ESNEXT'. */
    "module": "commonjs",                     /* Specify module code generation: 'none', 'commonjs', 'amd', 'system', 'umd', 'es2015', or 'ESNext'. */
    "lib": ["ES2015", "DOM", "ES2017"],                             /* Specify library files to be included in the compilation. */
    // "allowJs": true,                       /* Allow javascript files to be compiled. */
    // "checkJs": true,                       /* Report errors in .js files. */
    // "jsx": "preserve",                     /* Specify JSX code generation: 'preserve', 'react-native', or 'react'. */
    // "declaration": true,                   /* Generates corresponding '.d.ts' file. */
    // "declarationMap": true,                /* Generates a sourcemap for each corresponding '.d.ts' file. */
    "sourceMap": true,                     /* Generates corresponding '.map' file. */
    // "outFile": "./",                       /* Concatenate and emit output to single file. */
    "outDir": "dist",                        /* Redirect output structure to the directory. */
    "rootDir": "src",                       /* Specify the root directory of input files. Use to control the output directory structure with --outDir. */
.
.
.

    /* Experimental Options */
    // "experimentalDecorators": true,        /* Enables experimental support for ES7 decorators. */
    // "emitDecoratorMetadata": true,         /* Enables experimental support for emitting type metadata for decorators. */

    /* Advanced Options */
    "forceConsistentCasingInFileNames": true  /* Disallow inconsistently-cased references to the same file. */
  }
}

```

## 四、TypeScript原始类型

```typescript
// 原始数据类型

const a: string = 'foobar'

const b: number = 100 // NaN Infinity

const c: boolean = true // false

// 在非严格模式（strictNullChecks）下，
// string, number, boolean 都可以为空
// const d: string = null
// const d: number = null
// const d: boolean = null

const e: void = undefined

const f: null = null

const g: undefined = undefined

```

## 五、TypeScript标准库声明

标准库就是内置对象多对应的声明，代码中使用内置对象就必须引用对应的标准库，否则TypeScript就会报错。

```js
// Symbol 是 ES2015 标准中定义的成员，
// 使用它的前提是必须确保有对应的 ES2015 标准库引用
// 也就是 tsconfig.json 中的 lib 选项必须包含 ES2015
// "lib": ["ES2015", "DOM", "ES2017"],TypeScript把BOM和DOM都归结到一个标准库中，为DOM
const h: symbol = Symbol()

// Promise

// const error: string = 100
```

在上述**const h: symbol = Symbol()**中，如果配置文件中“target"为es5，那么会提示错误，因为，我们的symbol是es2015中新增的类型，所以需要将target改为es2015或以上才可以使用。

## 六、TypeScript中文错误消息

使TypeScript显示中文的错误消息，这样方便国人进行快速定位问题。

```shell
tsc --local zh-CN  # 绝大多数会使用中文
```

VS Code中，搜索TypeScript local，将TypeScript：local设置为zh-CN，此时VS Code报出的错误提示也会是中文的。不过，并不推荐这样做，锻炼英语，之后更便捷的阅读官方文档，这才是我这种菜鸟程序员的挑战。

## 七、TypeScript作用域问题

不同文件中会有相同变量名的情况，此时TypeScript就会报出错误，重复定义变量。为解决这个办法，我们需要将变量放到不同的作用域或者使用exports导出，这样文件就作为一个模块，模块是有单独的作用域的。

## 八、TypeScript Object类型

TypeScript中的object并不单独指对象类型，而是泛指所有的非原始类型，也就是对象、数组、函数。

```js
// Object 类型

export {} // 确保跟其它示例没有成员冲突

// object 类型是指除了原始类型以外的其它类型
const foo: object = function () {} // [] // {}  可以接受对象、数组、函数

// 如果需要明确限制对象类型，则应该使用这种类型对象字面量的语法，或者是「接口」
const obj: { foo: number, bar: string } = { foo: 123, bar: 'string' }

// 接口的概念后续介绍
```

## 九、TypeScript数组类型

TypeScript中定义数组的方式，与Flow中几乎完全一致。他有两种方式，第一种就是使用array泛型。第二种使用元素类型加方括号的形式。

```js
// 数组类型

export {} // 确保跟其它示例没有成员冲突

// 数组类型的两种表示方式

const arr1: Array<number> = [1, 2, 3]

const arr2: number[] = [1, 2, 3]
```

TypeScript中使用强类型的优势：

```js
// 案例 -----------------------

// 如果是 JS，需要判断是不是每个成员都是数字
// 使用 TS，类型有保障，不用添加类型判断
function sum (...args: number[]) {
  return args.reduce((prev, current) => prev + current, 0)
}
// reduce回顾：第一个参数prev为累加的和，第二个参数为当前循环的项，函数体中写业务代码，默认值为0

sum(1, 2, 3) // => 6
```

**一般情况下，数组应该保持同质，也就是说数组中的元素应该具有相同的类型。**

## 十、TypeScript元组类型

元组是array的一种子类型，是定义数组的一种特殊类型。长度固定，各索引位置上的值具有固定的已知类型。与其他多数类型不同，声明元组时必须显示注解类型。这是因为，创建元组使用的语法与数组相同（都使用方括号），而TypeScript遇到方括号，推导出来的是数组的类型。

```js
export {}
const tuple:[number, string] = [10,'Leo']
// const age = tuple[0]
// const name = tuple[1]

const [age, name] = tuple
// ---------------------

const entries: [string, number][] = Object.entries({
  foo: 123,
  bar: 456
})

const [key, value] = entries[0]
// key => foo, value => 123
```

## 十一、TypeScript枚举类型

枚举的作用是列举类型中包含的各个值。这是一种无序数结构，把键映射到值上。枚举可以理解为编译时键的固定访问对象，访问键时，TypeScript将检查指定的键是否存在。示例如下：

```js
export {}

// 文章对象
const post = {
    title: "TypeScript介绍",
    content: "简单介绍一下TypeScript语言",
    status: 2 // 1  0,
}
```

这里**0表示草稿，1表示未发布，2代表已发布**，为了防止出现其他值出现，我么可以使用枚举来限定其值。

枚举特点：

- 给一组数值起一个更好理解的名字
- 一个枚举中只会存在几个固定的值，并不会出现超出范围的可能性

```js
// 用对象模拟枚举
const PostStatus = {
  Draft: 0,
  Unpublished: 1,
  Published: 2
}

// 标准的数字枚举
enum PostStatus2 {
  Draft = 0,
  Unpublished = 1,
  Published = 2
}

// 数字枚举，枚举值自动基于前一个值自增，如果不指定每个枚举类型的值，那么其值会从0自增
enum PostStatus3 {
  Draft = 6,
  Unpublished, // => 7
  Published // => 8
}

// 字符串枚举，需要手动给每个成员明确一个初始化的值
enum PostStatus4 {
  Draft = 'aaa',
  Unpublished = 'bbb',
  Published = 'ccc'
}

// 常量枚举，不会侵入编译结果
const enum PostStatus5 {
  Draft,
  Unpublished,
  Published
}
```

然后根据上面的枚举值，我们可以将文章状态的写法进行如下转换：

```js
const post = {
  title: 'Hello TypeScript',
  content: 'TypeScript is a typed superset of JavaScript.',
  status: PostStatus.Draft // 3 // 1 // 0
}
// PostStatus[0] // => Draft
```

使用常量进行枚举时，编译ts文件后的js文件中会移出键值对形式的数组，改为在需要枚举的地方直接写入值，其他值则以注释的方式出现，如下为编译后的js文件：

```js
"use strict";// 枚举（Enum）Object.defineProperty(exports, "__esModule", { value: true });var post = {    title: 'Hello TypeScript',    content: 'TypeScript is a typed superset of JavaScript.',    status: 0 /* Draft */ // 3 // 1 // 0};// PostStatus[0] // => Draft//# sourceMappingURL=07-enum-types.js.map
```

## 十二、TypeScript函数类型

函数的类型约束无外乎就是对函数的输入、输出进行类型限制，输入指的就是函数的参数，输出指的是函数的返回值。JavaScript中有两种函数声明方式，分别是函数声明和函数表达式。所以我们需要了解在这两种声明方式下，我们如何进行函数的类型约束。

- 函数声明式：

```js
// 函数类型

export {} // 确保跟其它示例没有成员冲突

function func1 (a: number, b: number = 10, ...rest: number[]): string {
    return 'func1'
}
// a类型为数字类型，b类型为数字类型，...rest为参数默认值类型为数字，:string为函数返回值约束，如果没有...rest，则实参和形参个数必须相同
function func0 (a: number, b？: number = 10, ...rest: number[]): string {
    return 'func1'
}
// 在参数声明冒号前加问号？，表示这个参数为可选值，无论可选参数或参数默认值，都只能出现在参数最后面

func1(100, 200)

func1(100)

func1(100, 200, 300)
```

- 函数表达式：

```js
const func2: (a: number, b: number) => string = function (a: number, b: number): string {
  return 'func2'
}
```

## 十三、TypeScript任意类型

JavaScript本身是弱类型的语言，很多内置的API本身就支持接收任意类型的参数。而TypeScript又是基于JavaScript基础之上的，所以会在代码中用一个变量去接收任意一个类型的值。例：

```js
function stringify (value: any) {
    return JSON.stringify(value)
}
stringify('string')

stringify(100)

stringify(true)
```

any属于动态类型

```js
let foo: any = 'string'

foo = 100

foo.bar()  // 语法上不会报错，TypeScript不会对any进行类型检查，any 类型是不安全的
```

## 十四、TypeScript隐式类型推断

在TypeScript中，如果我们没有通过类型注解取标记一个变量的类型，TypeScript会根据变量的使用情况去推断变量的类型。这种特性叫：隐式类型推断

```js
// 隐式类型推断export {} // 确保跟其它示例没有成员冲突let age = 18 // number// age = 'string'  // 语法上会出现错误// 如果TypeScript无法对变量进行类型推断，那TypeScript就会对这个变量的类型注解为anylet foofoo = 100foo = 'string'  // 变量赋值任意类型的值，语法上都不会报错
```

虽然在TypeScript中支持隐式类型推断，这种隐式类型推断可以帮我们简化代码，但我们仍然建议大家对每个变量添加类型注解，这样便于我们后续更加直观的理解代码。

## 十五、TypeScript类型断言

特殊情况下，TypeScript无法推断出变量的具体类型，开发者根据代码的使用情况，总是根据使用情况可以知道变量是什么类型的。

```js
// 类型断言export {} // 确保跟其它示例没有成员冲突// 假定这个 nums 来自一个明确的接口const nums = [110, 120, 119, 112]const res = nums.find(i => i > 0)// const square = res * res，TypeScript此时推断返回值为number或undefined，即无法找到大于0的数字const num1 = res as number  // 开发者告诉TypeScript：你相信我，我断言res为number类型const num2 = <number>res // JSX 下不能使用
```

类型断言的方式有两种：

- as关键词（推荐使用）

  ```js
  const num1 = res as number
  ```

- 变量前面使用<类型>进行断言

  ```js
  const num2 = <number>res // JSX 下不能使用
  ```

> **！注意：类型断言并不是类型转换**

## 十六、TypeScript接口

Interfases接口，约定对象的结构，我们使用一个接口，就必须遵循这个接口全部的约定。TypeScript中，接口最直观的体现就是**约定一个对象中应该有哪些成员**，而且，成员的类型是固定的。

```js
function printPost (post) {    console.log(post.title)    console.log(post.content)}
```

此时该函数对于接受的参数post有一定的要求，也就是说post一定要有title和content属性，只不过这种要求为隐形的，并没有明确的表达，这时我们可以用接口明确的表达出来，此时我们可以定义一个接口：使用interface关键词。

```js
interface Post {    title: string  // 类型限定，可以使用逗号分隔多个成员，更标准的是使用分号，当然也可以省略    content: string}function printPost (post: Post) {    // 显示的要求传入的对象必须要有title和content成员	console.log(post.title)	console.log(post.content)}printPost({    title: 'Hello TypeScript',    content: 'A javascript superset'})
```

> 接口中可以使用**逗号**分隔多个成员，更标准的是使用**分号**，当然也可以省略，根据自己团队习惯来

编译完成后的JavaScript文件，发现在js代码中并没有接口，也就是说TypeScript中的接口只是对代码进行类型约束的，在实际运行的阶段，接口并无意义。

```js
"use strict";// 接口Object.defineProperty(exports, "__esModule", { value: true });function printPost(post) {    console.log(post.title);    console.log(post.content);}printPost({    title: 'Hello TypeScript',    content: 'A javascript superset'});//# sourceMappingURL=12-interface-basic.js.map
```

对于接口中约定的成员，还有一些特殊的用法。

- **可选成员**

```js
// 可选成员、只读成员、动态成员

export {} // 确保跟其它示例没有成员冲突

// -------------------------------------------

interface Post {
  title: string
  content: string
  subtitle?: string  // 表示为可选成员，其实就是将subtitle类型标注为string|undefined
  readonly summary: string
}

const hello: Post = {
  title: 'Hello TypeScript',
  content: 'A javascript superset',
  summary: 'A javascript'
}
```

- **只读成员**

```js
// 可选成员、只读成员、动态成员

export {} // 确保跟其它示例没有成员冲突

// -------------------------------------------

interface Post {
  title: string
  content: string
  readonly summary: string  // readonly表示此成员只读不能修改，在summary初始化完成后不能修改
}

const hello: Post = {
  title: 'Hello TypeScript',
  content: 'A javascript superset',
  summary: 'A javascript'
}
```

- 动态成员

```js
interface Cache {
    [prop: string]: string
}

const cache: Cache = {}

cache.foo = 'value1'  // cache可以任意添加成员，只不过需要遵循成员必须为string类型
cache.bar = 'value2'
```

## 十七、TypeScript类的基本使用

类**classes**，可以用来描述一类具体事务的抽象特征，例如手机属于一种类型，特征是可以打电话、发短信，在这种类型下，又可以细分某智能手机、某非智能手机（具体事物）。ES6以前，JavaScript都是由函数+原型模拟实现类，ES6开始，JavaScript中有了专门的class，TypeScript中除了使用ES6中类的所有用法，它还额外添加一些用法功能。

```js
// 类（Class）

export {} // 确保跟其它示例没有成员冲突

class Person {
    name: string // = 'init name'
    age: number

    constructor(name: string, age: number) {
        this.name = name
        this.age = age
    }

    sayHi(msg: string): void {
        console.log(`I am ${this.name}, ${msg}`)
    }
}
```

在类的构造函数中，并不能直接使用this.name,需要在类中直接声明属性才可以使用。

## 十八、TypeScript类的访问修饰符

TypeScript中类的特殊用法，首先是类成员的访问修饰符，接着使用上面定义的person

```js
// 类的访问修饰符

export {} // 确保跟其它示例没有成员冲突

class Person {
    public name: string // = 'init name'  共有成员，默认的修饰符，加不加都一样，但建议加上
    private age: number  // 私有属性，只能在类内部访问
    protected gender: boolean  // 受保护的属性，

    constructor(name: string, age: number) {
        this.name = name
        this.age = age
        this.gender = true
    }

    sayHi(msg: string): void {
        console.log(`I am ${this.name}, ${msg}`)
        console.log(this.age)
    }
}

class Student extends Person {
    private constructor(name: string, age: number) {
        super(name, age)
        console.log(this.gender)  这里可以访问到projected修饰符修饰的属性
    }  构造函数默认的修饰符为public，当它修饰符为private时，外部无法访问，使用静态方法可以访问

    static create(name: string, age: number) {
        return new Student(name, age)  使用静态方法创建对象实例
    }
}

const tom = new Person('tom', 18)
console.log(tom.name)
// console.log(tom.age)  无法访问age属性，为私有属性
// console.log(tom.gender)  无法访问gender，不能再外部使用，与private的区别是，projected只允许在此类中访问成员

// const jack = Student.create('jack', 18)  使用静态方法创建对象实例
```

## 十九、TypeScript类的只读属性

对于类属性的修饰，还可以使用readonly进行修饰,只允许访问，不允许修改。

```js
// 类的只读属性export {} // 确保跟其它示例没有成员冲突class Person {    public name: string // = 'init name'    private age: number    // 只读成员    protected readonly gender: boolean  // readonly跟在访问修饰符后面，对于只读属性可以再类型声明的时候直接初始化，也可以在构造函数中初始化，二者选     // 其一    constructor(name: string, age: number) {        this.name = name        this.age = age        this.gender = true    }    sayHi(msg: string): void {        console.log(`I am ${this.name}, ${msg}`)        console.log(this.age)    }}const tom = new Person('tom', 18)console.log(tom.name)// tom.gender = false
```

## 二十、TypeScript类与接口

相比于类，接口的概念更抽象。使用前面说到的手机的例子，手机是一个类型，这个类型的实例都是可以打电话发短信，但是能够打电话的不仅仅只有手机，座机也可以打电话，但座机并不属于手机这个类目，而是一个单独的类目，因为它不能发短信。这种情况下，这两个类之间有公共的特征，公共的特征我们一般使用接口进行抽象。第一次使用可能会有一些吃力，多从生活的角度思考。

```js
// 类与接口

export {} // 确保跟其它示例没有成员冲突

// 一个接口只实现一个方法
interface Eat {
    eat(food: string): void
}

interface Run {
    run(distance: number): void
}
    
// 人类
class Person implements Eat, Run {
    eat(food: string): void {
        console.log(`优雅的进餐: ${food}`)
    }

    run(distance: number) {
        console.log(`直立行走: ${distance}`)
    }
}

// 动物类
class Animal implements Eat, Run {
    eat(food: string): void {
        console.log(`呼噜呼噜的吃: ${food}`)
    }

    run(distance: number) {
        console.log(`爬行: ${distance}`)
    }
}
```

## 二十一、TypeScript抽象类

抽象类在某种程度上说与接口有点类似，他也是可以用来约束子类中必须要有某个成员。但是不同的是，抽象类可以办函一些具体的实现。

```js
// 抽线类

export {} // 确保跟其它示例没有成员冲突

// abstract抽象类，在被abstract声明后，他只能被继承，不能被new一个实例对象
abstract class Animal {
    eat(food: string): void {
        console.log(`呼噜呼噜的吃: ${food}`)
    }
	
    abstract run(distance: number): void  // 抽象方法，不需要方法体，当父类中有抽象方法时，子类必须实现这个方法
}

// dog继承自animal
class Dog extends Animal {
    run(distance: number): void {
        console.log('四脚爬行', distance)
    }

}

const d = new Dog()
d.eat('狗粮')
d.run(100)
```

## 二十二、TypeScript泛型

泛型指我们在定义函数、接口或类的时候，没有去指定具体的类型，等到使用的时候再去指定具体类型的特征。以函数为例，泛型就是我们在声明这个函数的时候，不去指定具体的类型，只在函数调用的时候去传递一个类型。作用是极大程度的复用我们的代码。

```js
// 泛型

export {} // 确保跟其它示例没有成员冲突
// 创建一个指定长度的数组，数组元素为数字，返回值为数字类型的数组
function createNumberArray(length: number, value: number): number[] {
    // ES6中的fill方法，Array创建一个长度为length，元素类型为number的空数组，然后使用fill填充值
    // Array为泛型类，在调用之前并不知道需要什么类型元素的数组，使用泛型参数进行声明元素类型<number>
    const arr = Array<number>(length).fill(value)
    return arr
}

function createStringArray(length: number, value: string): string[] {
    const arr = Array<string>(length).fill(value)
    return arr
}

function createArray<T>(length: number, value: T): T[] {
    const arr = Array<T>(length).fill(value)
    return arr
}

// const res = createNumberArray(3, 100)
// res => [100, 100, 100]

const res = createArray<string>(3, 'foo')

```

上述方法createNumberArray创建了一个数字类型的数组，但是当我们需要创建一个字符串类型的数组是，最笨的办法是再创建一个函数，更改其参数，这样就会造成冗余。更合理的办法就是使用泛型。将string或number变成一个参数createArray<T>,一般泛型参数为**大写T**。在使用的时候，我们在T的位置传递想要的类型，这样就可以同时满足上述两个需求了。

## 二十三、TypeScript类型声明

在实际开发过程中，我们会经常使用到一些第三方的npm模块，而这些npm模块并不一定都是使用TypeScript编写的。所以他提供的成员就不会有强类型的体验。

```shell
yarn add lodash
```

```js
// 类型声明
// camelCase将字符串转换为驼峰格式
import { camelCase } from 'lodash'
import qs from 'query-string'  // 

qs.parse('?key=value&key2=value2')

// declare function camelCase (input: string): string  // 如果我们使用的第三方模块没有对应的类型声明模块，我们需要declare手动进行类型声明

const res = camelCase('hello typed')
```

在直接导入时，会报错，无法找到类型声明文件**import { camelCase } from <u>'lodash'</u>**

目前很多第三方模块会提供类型声明的模块，我们安装@types-lodash。并且越来越多的模块在内部会直接支持类型声明。比如上面query-string模块。



