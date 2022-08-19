---
title: ECMAScript 新特性
tags: ECMAScript
category: 大前端
abbrlink: 1486
date: 2021-05-19 22:54:24
---

![](http://5coder.cn/img/WA5K6I3aVkFueLb.png)

## 一、ECMAScript概述

ECMAScript，即 ECMA-262 定义的语言，并不局限于 Web 浏览器。事实上，这门语言没有输入和输出之类的方法。ECMA-262 将这门语言作为一个基准来定义，以便在它之上再构建更稳健的脚本语言。

Web 浏览器只是 ECMAScript 实现可能存在的一种宿主环境（host environment）。宿主环境提供ECMAScript 的基准实现和与环境自身交互必需的扩展。扩展（比如 DOM）使用 ECMAScript 核心类型和语法，提供特定于环境的额外功能。其他宿主环境还有服务器端 JavaScript 平台 Node.js 和即将被淘汰的 Adobe Flash。

日常使用的Web环境下，JavaScript语言包括：ECMAScript、浏览器提供的BOM对象、DOM树。

Node.js环境下，JavaScript包括：ECMAScript、Node API（fs、net、etc.）

## 二、ES2015概述

ECMA-262 阐述了什么是 ECMAScript 符合性。要成为 ECMAScript 实现，必须满足下列条件：

- 支持 ECMA-262 中描述的所有“类型、值、对象、属性、函数，以及程序语法与语义”；

- 支持 Unicode 字符标准。

此外，符合性实现还可以满足下列要求。

- 增加 ECMA-262 中未提及的“额外的类型、值、对象、属性和函数”。ECMA-262 所说的这些额外内容主要指规范中未给出的新对象或对象的新属性。

- 支持 ECMA-262 中没有定义的“程序和正则表达式语法”（意思是允许修改和扩展内置的正则表达式特性）。

以上条件为实现开发者基于 ECMAScript 开发语言提供了极大的权限和灵活度，也是其广受欢迎的原因之一。

## 三、ES2015 let 与块级作用域

具体详情请阅读《JavaScript高级程序设计·第四版》中的第三章第三节（3.3）

### 1.var

- var定义的变量会预解析，简单的说就是如果变量没有定义就直接使用的话，JavaScript回去解析这个变量，代码不会报错，只会输出undefined。

```js
console.log(foo)  // undefined
var foo = 'foo';
```

- var定义的变量可以反复去定义，当然后面的会覆盖前面的

```js
var a = 1;
var a = 2;
```

- var在循环中使用的时候，循环体外依然可以使用

```js
for (var i = 0; i < 3; i++) {
	for (var i = 0; i < 3; i++) {
		console.log(i)
	}
	console.log('内层结束 i = ' + i)
}
//0
//1
//2
//内层结束 i = 3
```

- 在循环绑定事件过程中，var定义的变量无法保存，循环会在瞬间执行完

```js
var elements = [{}, {}, {}]
for (var i = 0; i < elements.length; i++) {
	elements[i].onclick = (function (i) {
		return
	})
}
elements[1].onclick()
```

### 2.let

- let定义的变量不会预解析，必须先声明再使用，否则会报错

```js
console.log(b);  // 报错
let b = 'bar'
```

- let不能定义已经定义过的变量（无论之前是用var定义的还是let或者const定义的）

```js
let b = 3;
let b = 4;  // 报错
```

- let是块级作用域，函数内部使用let定义后，对函数外部无影响，简单说就是在一个{}里面生效

```js
for (let i = 0; i < 3; i++) {
	let i = 'foo';
	console.log(i)  // foo
}
```

- 由于let是块级作用域，在循环绑定事件过程中let会在这个循环中生效，再次循环时let会重新定义生效

```js
let elements = [{}, {}, {}]
for (let i = 0; i < elements.length; i++) {
	elements[i].onclick = (function (i) {
		console.log(i)
	})
}
elements[0].onclick()
```

## 四、ES2015 const

- const定义的变量不会预解析，必须先声明再使用，否则会报错

```js
console.log(a);  // 报错 undefined
const a = 'foo'; 
```

- const定义的变量不允许修改

  ```js
  const a = 5;
  a = 6;  // err
  ```

  - 但是，在数组里面，const的值是允许被修改的，这是因为const存储的是地址，值的内容可以变化

  ```js
  const arr = [1,2,3,4,5]
  arr[1] = 'array'
  console.log(arr);
  ```

## 五、ES2015 数组的解构

ECMAScript2015 新增了一种从数组或者对象获取指定元素的快捷方式，这是一种新的语法，这种新语法叫做**解构**。如下代码所示，定义一个数组：

```js
const arr = [100, 200, 300]

const foo = arr[0]
const bar = arr[1]
const baz = arr[2]
console.log(foo, bar, baz)
```

在 ECMAScript2015 之前想要获取这个数组中的元素，需要通过索引访问对应的值，然后将访问的结果赋值给一个变量。

而在 ECMAScript2015 之后，可以通过数组的解构这种方式快速获取数组中的指定成员。如下代码所示：

```js
const arr = [100, 200, 300]

const [foo, bar, baz] = arr
console.log(foo, bar, baz)
```

这里会根据变量的位置进行分配数组中对应位置的成员。如果只要获取某一个位置上的成员，比如上个数组中的最后一个位置的成员，只需要保留前两个占位就可以了。如下代码所示：

```js
const arr = [100, 200, 300]
const [, , baz] = arr
console.log(baz)
```

除此之外，还可以在变量名前面增加 `...` 来获取从当前位置到数组最后的所有成员。如下代码所示：

```js
const arr = [100, 200, 300]

const [foo, ...rest] = arr
console.log(rest)  // [ 200, 300 ]
```

> **这里需要注意的是**，这种解构的用法只能在成员变量的最后一个变量上才能使用。

如果解构的变量数量少于数组的成员数量的话，那会按照从前到后的顺序进行获取。如下代码所示：

```js
const arr = [100, 200, 300]

const [foo] = arr
console.log(foo)  // 100
```

从打印的结果可以看到，数组中剩下的成员都不会被获取到。反之，如果解构的变量数量多于数组的成员数量的话，那多出来的变量的值为 `undefined`。如下代码所示：

```js
const arr = [100, 200, 300]

const [foo, bar, baz, more] = arr
console.log(more)  // undefined
```

使用 ECMAScript2015 之后的解构将大大进行简化。如下代码所示：

```js
const path = 'foo/bar/baz'

const [, rootDir] = path.split('/')
console.log(rootDir)
```

## 六、ES2015 对象的解构

在 ECMAScript2015 中，除了数组可以被解构之外，对象同样也可以被解构。只不过对象的解构，是需要通过属性名来获取，而不是位置。如下代码所示：

```javascript
const obj = {
  name: '拉勾大前端',
  age: 3
}

const {
  name
} = obj
console.log(name)
```

上述代码的运行结果如下：

```shell
拉勾大前端
```

这里解构中的变量名还有一个很重要的作用，就是匹配解构对象中的成员，从而获取指定成员的值。比如上述代码结构总的 `name` 获取了 `obj` 对象中的 `name` 属性值。

因为对象的解构的这种特性，如果当前作用域中存在一个同名的变量，就会产生冲突。如下代码所示：

```javascript
const obj = {
  name: '拉勾大前端',
  age: 3
}

const name = '拉勾大前端2'
const {
  name
} = obj
console.log(name)
```

上述代码的运行结果如下：

```shell
object-destructuring.js:13
  name
  ^

SyntaxError: Identifier 'name' has already been declared
    at createScript (vm.js:80:10)
    at Object.runInThisContext (vm.js:139:10)
    at Module._compile (module.js:599:28)
    at Object.Module._extensions..js (module.js:646:10)
    at Module.load (module.js:554:32)
    at tryModuleLoad (module.js:497:12)
    at Function.Module._load (module.js:489:3)
    at Function.Module.runMain (module.js:676:10)
    at startup (bootstrap_node.js:187:16)
    at bootstrap_node.js:608:3
```

因为 `obj` 对象的 `name` 属性必须在解构中定义 `name` 变量进行获取，那么这一冲突就无法避免。这个时候可以通过重命名的方式来解决这样的问题，如下代码所示：

```javascript
const obj = {
  name: '拉勾大前端',
  age: 3
}

const name = '拉勾大前端'
const {
  name: objName
} = obj
console.log(objName)
```

## 七、ES2015模板字符串

### 1.模板字面量

ECMAScript 6 新增了使用模板字面量定义字符串的能力。与使用单引号或双引号不同，模板字面量保留换行字符，可以跨行定义字符串：

> 使用键盘区域Esc下方【数字1左边】的反引号

```js
let myMultiLineString = 'first line\nsecond line'; 
let myMultiLineTemplateLiteral = `first line 
second line`; 
console.log(myMultiLineString); 
// first line 
// second line" 
console.log(myMultiLineTemplateLiteral); 
// first line
// second line
console.log(myMultiLineString === myMultiLinetemplateLiteral); // true
```

所以说，当我们需要写HTML模板时，这个方法非常有用：

```js
let pageHTML = ` 
<div> 
 <a href="#"> 
 <span>Jake</span> 
 </a> 
</div>`;
```

由于模板字面量会保持反引号内部的空格，因此在使用时要格外注意。格式正确的模板字符串看起来可能会缩进不当。

### 2.字符串插值

> 模板字面量最常用的一个特性是支持字符串插值，也就是可以在一个连续定义中插入一个或多个值。技术上讲，**模板字面量不是字符串，而是一种特殊的 JavaScript 句法表达式，只不过求值后得到的是字符串。**模板字面量在定义时立即求值并转换为字符串实例，任何插入的变量也会从它们最接近的作用域中取值。

字符串插值通过在${}中使用一个 JavaScript 表达式实现：

```js
let value = 5; 
let exponent = 'second'; 
// 以前，字符串插值是这样实现的：
let interpolatedString = value + ' to the ' + exponent + ' power is ' + (value * value); 
// 现在，可以用模板字面量这样实现：
let interpolatedTemplateLiteral = `${ value } to the ${ exponent } power is ${ value * value }`; 
console.log(interpolatedString); // 5 to the second power is 25 
console.log(interpolatedTemplateLiteral); // 5 to the second power is 25
// 所有插入的值都会使用 toString()强制转型为字符串，而且任何 JavaScript 表达式都可以用于插值。
```

### 3.模板字面量标签函数

模板字面量也支持定义**标签函数（tag function）**，而通过标签函数可以**自定义插值行为**。标签函数会接收**被插值记号分隔后的模板**和**对每个表达式求值的结果**。

标签函数本身是一个常规函数，通过前缀到模板字面量来应用自定义行为，如下例所示。标签函数接收到的参数依次是原始字符串数组和对每个表达式求值的结果。这个函数的返回值是对模板字面量求值得到的字符串。

这样概念解释很不清楚，通过下方的例子来加强理解：

```js
let a = 6; 
let b = 9; 
function simpleTag(strings, ...expressions) { 
 	console.log(strings); 
 	for(const expression of expressions) { 
 		console.log(expression); 
 	} 
 	return 'foobar'; 
} 
let taggedResult = simpleTag`${ a } + ${ b } = ${ a + b }`; 
// ["", " + ", " = ", ""] 
// 6 
// 9 
// 15 
console.log(taggedResult); // "foobar"
```

## 八、ES2015参数默认值

在 ECMAScript5.1 及以前，实现默认参数的一种常用方式就是检测某个参数是否等于 undefined，如果是则意味着没有传这个参数，那就给它赋一个值：

```js
function makeKing(name) { 
     name = (typeof name !== 'undefined') ? name : 'Henry'; 
     return `King ${name} VIII`; 
} 
console.log(makeKing()); // 'King Henry VIII' 
console.log(makeKing('Louis')); // 'King Louis VIII'
```

ECMAScript 6 之后就不用这么麻烦了，因为它支持**显式定义默认参数**了。下面就是与前面代码等价的 ES6 写法，只要在函数定义中的参数后面用=就可以为参数赋一个默认值：

```js
function makeKing(name = 'Henry') { 
 	return `King ${name} VIII`; 
} 
console.log(makeKing('Louis')); // 'King Louis VIII' 
console.log(makeKing()); // 'King Henry VIII'
```

**上面给参数传 undefined 相当于没有传值**，不过这样可以利用多个独立的默认值：

```js
function makeKing(name = 'Henry', numerals = 'VIII') { 
 	return `King ${name} ${numerals}`; 
} 
console.log(makeKing()); // 'King Henry VIII' 
console.log(makeKing('Louis')); // 'King Louis VIII' 
console.log(makeKing(undefined, 'VI')); // 'King Henry VI'
```

在使用默认参数时，arguments 对象的值不反映参数的默认值，只反映传给函数的参数。当然，跟 ES5 严格模式一样，修改命名参数也不会影响 arguments 对象，它始终以调用函数时传入的值为准：

```js
function makeKing(name = 'Henry') { 
     name = 'Louis'; 
     return `King ${arguments[0]}`; 
} 
console.log(makeKing()); // 'King undefined' 
console.log(makeKing('Louis')); // 'King Louis'
```

默认参数值并不限于原始值或对象类型，也可以使用调用函数返回的值：

```js
let romanNumerals = ['I', 'II', 'III', 'IV', 'V', 'VI']; 
let ordinality = 0; 
function getNumerals() { 
     // 每次调用后递增
     return romanNumerals[ordinality++]; 
} 
function makeKing(name = 'Henry', numerals = getNumerals()) { 
     return `King ${name} ${numerals}`; 
} 
console.log(makeKing()); // 'King Henry I'
console.log(makeKing('Louis', 'XVI')); // 'King Louis XVI' 
console.log(makeKing()); // 'King Henry II' 
console.log(makeKing()); // 'King Henry III'
```

函数的默认参数只有在函数被调用时才会求值，不会在函数定义时求值。而且，计算默认值的函数只有在调用函数但未传相应参数时才会被调用。

箭头函数同样也可以这样使用默认参数，只不过在只有一个参数时，就必须使用括号而不能省略了：

```js
let makeKing = (name = 'Henry') => `King ${name}`; console.log(makeKing()); // King Henry
```

## 九、ES2015展开数组(Spread)

在 ECMAScript5.1 及以前，我们从打印出数组中的元素很麻烦，最笨的办法是：

```js
const arr = ['foo', 'bar', 'baz'];console.log(	arr[0],	arr[1],	arr[2])// foo bar baz
```

但是当数组的个数不确定是，就不能使用这个方法，并且这个方法属于硬展，我们可以使用函数的apply方法，第一个参数this指向console对象，第二个参数是要传递的数组对象：

```js
const arr = ['foo', 'bar', 'baz'];console.log.apply(console, arr)// foo bar baz
```

在ES6中，我们可以更简单的使用数组展开的方法，形式同与收集剩余参数，使用...arr展开数组，这样写起来非常方便：

```js
const arr = ['foo', 'bar', 'baz'];console.log(...arr)// foo bar baz
```

## 十、ES2015箭头函数

ECMAScript 6 新增了使用胖箭头（=>）语法定义函数表达式的能力。很大程度上，箭头函数实例化的函数对象与正式的函数表达式创建的函数对象行为是相同的。任何可以使用函数表达式的地方，都可以使用箭头函数：

```js
let arrowSum = (a, b) => { 
 	return a + b; 
}; 
let functionExpressionSum = function(a, b) { 
 	return a + b; 
}; 
console.log(arrowSum(5, 8)); // 13 
console.log(functionExpressionSum(5, 8)); // 13
```

如果只有一个参数，那也可以不用括号。只有没有参数，或者多个参数的情况下，才需要使用括号：

```js
// 以下两种写法都有效
let double = (x) => { return 2 * x; }; 
let triple = x => { return 3 * x; };
// 没有参数需要括号
let getRandom = () => { return Math.random(); }; 
// 多个参数需要括号
let sum = (a, b) => { return a + b; }; 
// 无效的写法：
let multiply = a, b => { return a * b; };
```

箭头函数也可以不用大括号，但这样会改变函数的行为。使用大括号就说明包含“函数体”，可以在一个函数中包含多条语句，跟常规的函数一样。如果不使用大括号，那么箭头后面就只能有一行代码，比如一个赋值操作，或者一个表达式。而且，省略大括号会隐式返回这行代码的值：

```js
// 以下两种写法都有效，而且返回相应的值
let double = (x) => { return 2 * x; }; 
let triple = (x) => 3 * x; 
// 可以赋值
let value = {}; 
let setName = (x) => x.name = "Matt"; 
setName(value); 
console.log(value.name); // "Matt" 
// 无效的写法：
let multiply = (a, b) => return a * b;
```

箭头函数虽然语法简洁，但也有很多场合不适用。箭头函数不能使用 arguments、super 和new.target，也不能用作构造函数。此外，箭头函数也没有 prototype 属性。

另外，箭头函数中的this指向也与普通函数不同，请参考一篇文章：

[ES6箭头函数里的this]: （https://www.jianshu.com/p/c1ee12a328d2/）

## 十一、ES2015对象

### 1.对象字面量的增强

ES6中增强了对象的字面量，在之前，我们声明对象只能使用键+冒号+值的方式：

```js
let bar = '345'const obj = {    name: 'leo',    age: '26',    bar: bar}
```

而在ES6中,当我们的属性名与其值都为变量且相同时，我们可以省略冒号以及后面的值：

```js
let bar = '345'const obj = {    name: 'leo',    age: '26',    bar}
```

同样，当我们需要使用动态的属性名时，之前的做法是在对象声明过后，再对对象赋值动态属性名的值：

```js
const obj = {    name: 'leo',    age: '26',    bar}obj[Math.random()] = 'random'
```

在ES6中，我们可以直接使用方括号+表达式对对象添加动态的属性名，这种方式称之为【**计算属性名**】，方括号内部可以为任意表达式，表达式结果作为最终的属性名：

```js
const obj = {    name: 'leo',    age: '26',    bar,    [Math.random()]: 'random'}
```

### 2.Object扩展方法

- Object.assign

此方法可以将多个源对象中的属性复制到一个目标对象中，如果对象之间有相同的属性名，那么源对象中的属性就会覆盖掉目标对象中的属性。源对象与目标对象都是普通的对象，只不过用处不同

```js
const source1 = {      a: 123,      b: 123}const source2 = {      b: 789,      d: 789}const target = {      a: 456,      c: 456}const result = Object.assign(target, source1, source2)console.log(target)console.log(result === target)// { a: 123, c: 456, b: 789, d: 789 }// true
```

应用场景：

```js
function func (obj) {      // obj.name = 'func obj'      // console.log(obj)      const funcObj = Object.assign({}, obj)      funcObj.name = 'func obj'      console.log(funcObj)}const obj = { name: 'global obj' }func(obj)console.log(obj)
```

assign方法多用于options对象参数设置默认值。

- Object.is

用来判断两个值是否相等，在之前我们使用==和===分别判断值是否相等以及是否全等（值与类型都相等），在==中，js默认使用toString方法来进行隐式转换，而在ES6中，提供了全新的方法Object.is方法进行判断：

```js
console.log(  // 0 == false              // => true  // 0 === false             // => false  // +0 === -0               // => true  // NaN === NaN             // => false  // Object.is(+0, -0)       // => false  // Object.is(NaN, NaN)     // => true)
```

在实际使用中，仍然建议使用===来判断。

## 十二、ES2015 Proxy

> 在 ES6 之前，ECMAScript 中并没有类似代理的特性。由于代理是一种新的基础性语言能力，很多转译程序都不能把代理行为转换为之前的 ECMAScript 代码，因为代理的行为实际上是无可替代的。为此，代理和反射只在百分之百支持它们的平台上有用。可以检测代理是否存在，不存在则提供后备代码。不过这会导致代码冗余，因此并不推荐。

### 1.空代理

最简单的代理是空代理，即除了作为一个抽象的目标对象，什么也不做。默认情况下，在代理对象上执行的所有操作都会无障碍地传播到目标对象。因此，在任何可以使用目标对象的地方，都可以通过同样的方式来使用与之关联的代理对象。

如下面的代码所示，在代理对象上执行的任何操作实际上都会应用到目标对象。唯一可感知的不同就是代码中操作的是代理对象。

```js
const target = { 
 	id: 'target' 
}; 
const handler = {}; 
const proxy = new Proxy(target, handler); 
// id 属性会访问同一个值
console.log(target.id); // target 
console.log(proxy.id); // target 
// 给目标属性赋值会反映在两个对象上
// 因为两个对象访问的是同一个值
target.id = 'foo'; 
console.log(target.id); // foo 
console.log(proxy.id); // foo 
// 给代理属性赋值会反映在两个对象上
// 因为这个赋值会转移到目标对象
proxy.id = 'bar'; 
console.log(target.id); // bar 
console.log(proxy.id); // bar 
// hasOwnProperty()方法在两个地方
// 都会应用到目标对象
console.log(target.hasOwnProperty('id')); // true 
console.log(proxy.hasOwnProperty('id')); // true 
// Proxy.prototype 是 undefined 
// 因此不能使用 instanceof 操作符
console.log(target instanceof Proxy); // TypeError: Function has non-object prototype 
'undefined' in instanceof check 
console.log(proxy instanceof Proxy); // TypeError: Function has non-object prototype 
'undefined' in instanceof check 
// 严格相等可以用来区分代理和目标
console.log(target === proxy); // false
```

### 2.定义捕获器：

使用代理的主要目的是可以定义捕获器（trap）。捕获器就是在处理程序对象中定义的“基本操作的拦截器”。每个处理程序对象可以包含零个或多个捕获器，每个捕获器都对应一种基本操作，可以直接或间接在代理对象上调用。每次在代理对象上调用这些基本操作时，代理可以在这些操作传播到目标对象之前先调用捕获器函数，从而拦截并修改相应的行为。

例如，可以定义一个 get()捕获器，在 ECMAScript 操作以某种形式调用 get()时触发。下面的例子定义了一个 get()捕获器：

```js
const target = { 
 	foo: 'bar' 
}; 
const handler = { 
     // 捕获器在处理程序对象中以方法名为键
     get() { 
     	return 'handler override'; 
     } 
}; 
const proxy = new Proxy(target, handler); 
console.log(target.foo); // bar 
console.log(proxy.foo); // handler override 
console.log(target['foo']); // bar 
console.log(proxy['foo']); // handler override 
console.log(Object.create(target)['foo']); // bar 
console.log(Object.create(proxy)['foo']); // handler override
```

捕获器可以定义get、delete、set等方法。

## 十三、ES2015 class类

ECMAScript 6 新引入的 class 关键字具有正式定义类的能力。类（class）是ECMAScript 中新的基础性语法糖结构，因此刚开始接触时可能会不太习惯。虽然 ECMAScript 6 类表面上看起来可以支持正式的面向对象编程，但实际上它背后使用的仍然是原型和构造函数的概念。

### 1.类的定义

与函数类型相似，定义类也有两种主要方式：类声明和类表达式。这两种方式都使用 class 关键字加大括号：

```js
// 类声明class Person {} // 类表达式const Animal = class {};
```

类可以包含构造函数方法、实例方法、获取函数、设置函数和静态类方法，但这些都不是必需的。空的类定义照样有效。默认情况下，类定义中的代码都在严格模式下执行。

与函数构造函数一样，多数编程风格都建议类名的首字母要大写，以区别于通过它创建的实例（比如，通过 class Foo {}创建实例 foo）：

```js
// 空类定义，有效 class Foo {} // 有构造函数的类，有效class Bar {  	constructor() {} } // 有获取函数的类，有效class Baz {  	get myBaz() {} } // 有静态方法的类，有效class Qux {  	static myQux() {} }
```

### 2.类构造函数

**constructor** 关键字用于在类定义块内部创建类的构造函数。方法名 constructor 会告诉解释器在使用 new 操作符创建类的新实例时，应该调用这个函数。构造函数的定义不是必需的，不定义构造函数相当于将构造函数定义为空函数。

使用 new 操作符实例化 Person 的操作等于使用 new 调用其构造函数。唯一可感知的不同之处就是，JavaScript 解释器知道使用 new 和类意味着应该使用 constructor 函数进行实例化。

使用 new 调用类的构造函数会执行如下操作。

- 在内存中创建一个新对象。

- 这个新对象内部的[[Prototype]]指针被赋值为构造函数的 prototype 属性。

- 构造函数内部的 this 被赋值为这个新对象（即 this 指向新对象）。

- 执行构造函数内部的代码（给新对象添加属性）。

- 如果构造函数返回非空对象，则返回该对象；否则，返回刚创建的新对象。

```js
class Animal {} class Person {      constructor() {      	console.log('person ctor');      } } class Vegetable {      constructor() {      	this.color = 'orange';      } } let a = new Animal(); let p = new Person(); // person ctor let v = new Vegetable(); console.log(v.color); // orange
```

### 3.实例、原型、类成员

类的语法可以非常方便地定义应该存在于实例上的成员、应该存在于原型上的成员，以及应该存在于类本身的成员。

每次通过new调用类标识符时，都会执行类构造函数。在这个函数内部，可以为新创建的实例（this）添加“自有”属性。至于添加什么样的属性，则没有限制。另外，在构造函数执行完毕后，仍然可以给实例继续添加新成员。

每个实例都对应一个唯一的成员对象，这意味着所有成员都不会在原型上共享：

```js
class Person {      constructor() {          // 这个例子先使用对象包装类型定义一个字符串         // 为的是在下面测试两个对象的相等性         this.name = new String('Jack');          this.sayName = () => console.log(this.name);          this.nicknames = ['Jake', 'J-Dog']      } } let p1 = new Person(),  	p2 = new Person(); p1.sayName(); // Jack p2.sayName(); // Jack console.log(p1.name === p2.name); // false console.log(p1.sayName === p2.sayName); // false console.log(p1.nicknames === p2.nicknames); // false p1.name = p1.nicknames[0]; p2.name = p2.nicknames[1]; p1.sayName(); // Jake p2.sayName(); // J-Dog
```

静态类成员在类定义中使用 static 关键字作为前缀。在静态成员中，this 引用类自身。其他所有约定跟原型成员一样：

```js
class Person { 
     constructor() { 
         // 添加到 this 的所有内容都会存在于不同的实例上
         this.locate = () => console.log('instance', this); 
     } 
     // 定义在类的原型对象上
     locate() { 
        console.log('prototype', this); 
     } 
 	// 定义在类本身上
     static locate() { 
        console.log('class', this); 
     } 
} 
let p = new Person(); 
p.locate(); // instance, Person {} 
Person.prototype.locate(); // prototype, {constructor: ... } 
Person.locate(); // class, class Person {}
```

### 4.继承

ES6 类支持单继承。使用 extends 关键字，就可以继承任何拥有[[Construct]]和原型的对象。很大程度上，这意味着不仅可以继承一个类，也可以继承普通的构造函数（保持向后兼容）：

```js
class Vehicle {} 
// 继承类
class Bus extends Vehicle {} 
let b = new Bus(); 
console.log(b instanceof Bus); // true 
console.log(b instanceof Vehicle); // true 
function Person() {} 
// 继承普通构造函数
class Engineer extends Person {} 
let e = new Engineer(); 
console.log(e instanceof Engineer); // true 
console.log(e instanceof Person); // true
```

## 十四、ES2015 Set数据结构

ECMAScript 6 新增的 Set 是一种新集合类型，为这门语言带来集合数据结构。Set 在很多方面都像是加强的 Map，这是因为它们的大多数 API 和行为都是共有的。

使用 new 关键字和 Set 构造函数可以创建一个空集合：

```js
const m = new Set();
```

```js
// 使用数组初始化集合 const s1 = new Set(["val1", "val2", "val3"]); alert(s1.size); // 3 // 使用自定义迭代器初始化集合const s2 = new Set({      [Symbol.iterator]: function*() {          yield "val1";          yield "val2";          yield "val3";      } }); alert(s2.size); // 3
```

初始化之后，可以使用 add()增加值，使用 has()查询，通过 size 取得元素数量，以及使用 delete()和 clear()删除元素：

```js
const s = new Set(); 
alert(s.has("Matt")); // false 
alert(s.size); // 0 
s.add("Matt") 
 .add("Frisbie"); // add函数返回的依然是set对象，所以可以使用链式调用
alert(s.has("Matt")); // true 
alert(s.size); // 2 
s.delete("Matt"); 
alert(s.has("Matt")); // false 
alert(s.has("Frisbie")); // true 
alert(s.size); // 1 
s.clear(); // 销毁集合实例中的所有值
alert(s.has("Matt")); // false 
alert(s.has("Frisbie")); // false 
alert(s.size); // 0
```

## 十五、ES2015 Map数据结构

作为 ECMAScript 6 的新增特性，Map 是一种新的集合类型，为这门语言带来了真正的键/值存储机制。Map 的大多数特性都可以通过 Object 类型实现，但二者之间还是存在一些细微的差异。具体实践中使用哪一个，还是值得细细甄别。

使用 new 关键字和 Map 构造函数可以创建一个空映射：

```js
const m = new Map();
```

如果想在创建的同时初始化实例，可以给 Map 构造函数传入一个可迭代对象，需要包含键/值对数组。可迭代对象中的每个键/值对都会按照迭代顺序插入到新映射实例中：

```js
// 使用嵌套数组初始化映射
const m1 = new Map([ 
     ["key1", "val1"], 
     ["key2", "val2"], 
     ["key3", "val3"] 
]); 
alert(m1.size); // 3 

// 映射期待的键/值对，无论是否提供
const m3 = new Map([[]]); 
alert(m3.has(undefined)); // true 
alert(m3.get(undefined)); // undefined
```

```js
const m = new Map()

const tom = { name: 'tom' }

m.set(tom, 90)

console.log(m)

console.log(m.get(tom))

// 输出
// Map { { name: 'tom' } => 90 }
// 90
// 90 { name: 'tom' }
```

同样，map也有has()、delete()、clear()方法。

## 十六、Symbol符号

在ES6之前，对象的属性名都是用字符串表示，而这样会导致，对象的属性名重复造成冲突，例如属性值覆盖等问题。

```js
// shared.js ====================================

const cache = {}

// a.js =========================================

cache['foo'] = Math.random()

// b.js =========================================

cache['foo'] = '123'

console.log(cache['foo'])  // 123
```

之前的解决方式基本为约定，例如a.js文件中的键名都为a_foo,b.js文件中的键名为b_foo，这样就不会造成属性名重复冲突的问题。而约定只是为了规避这个问题，并没有实际解决这个问题。

ES6中为了解决这个问题，提出了一个新的数据类型**（Symbol）符号**。符号是原始值，且符号实例是唯一、不可变的。符号的用途是确保对象属性使用唯一标识符，不会发生属性冲突的危险。

### 1.基本使用--Symbol()

```js
const s = Symbol()
console.log(s)
console.log(typeof s)

// 两个 Symbol 永远不会相等

console.log(
  Symbol() === Symbol()
)  // false
```

调用 Symbol()函数时，也可以传入一个字符串参数作为对符号的描述（description），将来可以通过这个字符串来调试代码。但是，这个字符串参数与符号定义或标识完全无关：

```js
let genericSymbol = Symbol(); 
let otherGenericSymbol = Symbol(); 
let fooSymbol = Symbol('foo'); 
let otherFooSymbol = Symbol('foo'); 
console.log(genericSymbol == otherGenericSymbol); // false
console.log(fooSymbol == otherFooSymbol); // false
```

**符号没有字面量语法**，这也是它们发挥作用的关键。按照规范，你只要创建 Symbol()实例并将其用作对象的新属性，就可以保证它不会覆盖已有的对象属性，无论是符号属性还是字符串属性。

```js
let genericSymbol = Symbol(); 
console.log(genericSymbol); // Symbol() 
let fooSymbol = Symbol('foo'); 
console.log(fooSymbol); // Symbol(foo);
```

最重要的是，Symbol()函数不能与 new 关键字一起作为构造函数使用。这样做是为了避免创建符号包装对象，像使用 Boolean、String 或 Number 那样，它们都支持构造函数且可用于初始化包含原始值的包装对象：

```js
let myBoolean = new Boolean(); 
console.log(typeof myBoolean); // "object" 
let myString = new String(); 
console.log(typeof myString); // "object" 
let myNumber = new Number(); 
console.log(typeof myNumber); // "object" 
let mySymbol = new Symbol(); // TypeError: Symbol is not a constructor
```

### 2.使用全局符号注册表--Symbol.for()

如果运行时的不同部分需要共享和重用符号实例，那么可以用一个字符串作为键，在全局符号注册表中创建并重用符号。也就是说可以使用一个字符串参数作为Symbol的描述符，这样在使用过程中可以重用这一定义的symbol。

```js
let fooGlobalSymbol = Symbol.for('foo'); // 创建新符号
let otherFooGlobalSymbol = Symbol.for('foo'); // 重用已有符号
console.log(fooGlobalSymbol === otherFooGlobalSymbol); // true
```

Symbol.for()对每个字符串键都执行幂等操作。第一次使用某个字符串调用时，它会检查全局运行时**注册表(也可以理解为一个映射关系表)**，发现不存在对应的符号，于是就会生成一个新符号实例并添加到注册表中。后续使用相同字符串的调用同样会检查注册表，发现存在与该字符串对应的符号，然后就会返回该符号实例。

即使采用相同的符号描述，在全局注册表中定义的符号跟使用 Symbol()定义的符号也并不等同：

```js
let localSymbol = Symbol('foo'); 
let globalSymbol = Symbol.for('foo'); 
console.log(localSymbol === globalSymbol); // false
```

全局注册表中的符号必须使用**字符串**来创建，因此传递给Symbol的任何参数都会被转换为字符串：

```js
const boolSymbol = Symbol.for(true);
const stringSymbol = Symbol.for('true');
console.log(boolSymbol === stringSymbol); // true
```

还可以使用**Symbol.keyFor()**来查询全局注册表，这个方法接收符号，返回该全局符号对应的字符串键。如果查询的不是全局符号，则返回 undefined。

```js
// 创建全局符号
let s = Symbol.for('foo'); 
console.log(Symbol.keyFor(s)); // foo 
// 创建普通符号
let s2 = Symbol('bar'); 
console.log(Symbol.keyFor(s2)); // undefined 
// 如果传给 Symbol.keyFor()的不是符号，则该方法抛出 TypeError：
Symbol.keyFor(123); // TypeError: 123 is not a symbol
```

### 3.使用符号作为属性

**凡是可以使用字符串或数值作为属性的地方，都可以使用符号。**这就包括了对象字面量属性和**Object.defineProperty()/Object.defineProperties()**定义的属性。对象字面量只能在计算属性语法中使用符号作为属性。

```js
let s1 = Symbol('foo'), 
    s2 = Symbol('bar'), 
    s3 = Symbol('baz'), 
    s4 = Symbol('qux'); 
let o = { 
 [s1]: 'foo val' 
}; 
// 这样也可以：o[s1] = 'foo val'; 
console.log(o); 
// {Symbol(foo): foo val} 
Object.defineProperty(o, s2, {value: 'bar val'}); 
console.log(o); 
// {Symbol(foo): foo val, Symbol(bar): bar val} 
Object.defineProperties(o, { 
    [s3]: {value: 'baz val'}, 
    [s4]: {value: 'qux val'} 
}); 
console.log(o); 
// {Symbol(foo): foo val, Symbol(bar): bar val, 
// Symbol(baz): baz val, Symbol(qux): qux val}
```

类似于 **Object.getOwnPropertyNames()返回对象实例的常规属性数组**，**Object.getOwnPropertySymbols()返回对象实例的符号属性数组**。这两个方法的返回值彼此互斥。**Object.getOwnPropertyDescriptors()会返回同时包含常规和符号属性描述符的对象。Reflect.ownKeys()会返回两种类型的键**：

```js
let s1 = Symbol('foo'), 
	s2 = Symbol('bar'); 
let o = { 
    [s1]: 'foo val', 
    [s2]: 'bar val', 
    baz: 'baz val', 
    qux: 'qux val' 
}; 
console.log(Object.getOwnPropertySymbols(o)); 
// [Symbol(foo), Symbol(bar)] 返回对象实例的符号属性数组
console.log(Object.getOwnPropertyNames(o)); 
// ["baz", "qux"] 返回对象实例的常规属性数组
console.log(Object.getOwnPropertyDescriptors(o)); 
// {baz: {...}, qux: {...}, Symbol(foo): {...}, Symbol(bar): {...}} 返回同时包含常规和符号属性描述符的对象
console.log(Reflect.ownKeys(o)); 
// ["baz", "qux", Symbol(foo), Symbol(bar)]返回两种类型的键**
```

因为符号属性是对内存中符号的一个引用，所以直接创建并用作属性的符号不会丢失。但是，如果没有显式地保存对这些属性的引用，那么必须遍历对象的所有符号属性才能找到相应的属性键：

```js
let o = {     [Symbol('foo')]: 'foo val',     [Symbol('bar')]: 'bar val' }; console.log(o); // {Symbol(foo): "foo val", Symbol(bar): "bar val"} let barSymbol = Object.getOwnPropertySymbols(o)  .find((symbol) => symbol.toString().match(/bar/)); console.log(barSymbol); // Symbol(bar)
```

### 4.常用内置符号

ECMAScript 6 也引入了一批常用内置符号（well-known symbol），用于暴露语言内部行为，开发者可以直接访问、重写或模拟这些行为。这些内置符号都以 Symbol 工厂函数字符串属性的形式存在。这些内置符号最重要的用途之一是重新定义它们，从而改变原生结构的行为。比如，**我们知道for-of 循环会在相关对象上使用 Symbol.iterator 属性，那么就可以通过在自定义对象上重新定义Symbol.iterator 的值，来改变 for-of 在迭代该对象时的行为。**

> **for of中的Symbol.iterator我们会在下面的一节讲到**

这些内置符号也没有什么特别之处，它们就是全局函数 Symbol 的普通字符串属性，指向一个符号的实例。所有内置符号属性都是不可写、不可枚举、不可配置的。

> 注意 在提到 ECMAScript 规范时，经常会引用符号在规范中的名称，前缀为@@。比如，@@iterator 指的就是 Symbol.iterator。

### 5.Symbol方法

Symbol提供了一些方法，方法如下所示，具体使用技巧可查看**MDN**或《**JavaScript高级程序设计第四版**》

-  **Symbol.asyncIterator**<!--一个方法，该方法返回对象默认的 AsyncIterator。 由 for-await-of 语句使用-->
-  **Symbol.hasInstance**<!--一个方法，该方法决定一个构造器对象是否认可一个对象是它的实例。由 instanceof 操作符使用-->
-  **Symbol.isConcatSpreadable**<!--一个布尔值，如果是 true，则意味着对象应该用 Array.prototype.concat()打平其数组元素-->
-  **Symbol.iterator**<!--一个方法，该方法返回对象默认的迭代器。由 for-of 语句使用-->
-  **Symbol.match**<!--一个正则表达式方法，该方法用正则表达式去匹配字符串。由 String.prototype.match()方法使用-->
-  **Symbol.replace**<!--一个正则表达式方法，该方法替换一个字符串中匹配的子串。由 String.prototype.replace()方法使用-->
-  **Symbol.search**<!--一个正则表达式方法，该方法返回字符串中匹配正则表达式的索引。由 String.prototype.search()方法使用-->
-  **Symbol.species**<!--一个函数值，该函数作为创建派生对象的构造函数-->
-  **Symbol.split**<!--一个正则表达式方法，该方法在匹配正则表达式的索引位置拆分字符串。由 String.prototype.split()方法使用-->
-  **Symbol.toPrimitive**<!--一个方法，该方法将对象转换为相应的原始值。由 ToPrimitive 抽象操作使用-->
-  **Symbol.toStringTag**<!--一个字符串，该字符串用于创建对象的默认字符串描述。由内置方法 Object.prototype.toString()使用-->
-  **Symbol.unscopables**<!--一个对象，该对象所有的以及继承的属性，都会从关联对象的 with 环境绑定中排除-->

## 十七、for...of循环

在ECMAScript中，遍历数据有很多的方法。例如，for循环通常用来遍历数组，for...in循环通常用来遍历键值对，函数式的遍历方法如：forEach方法。这些方法都会有一定的局限性。所有ES2015引入了一种全新的遍历方式，for...of，其作为以后遍历所有数据结构的统一方式。

for-of 语句是一种严格的迭代语句，用于遍历可迭代对象的元素，语法如下:

```js
for (property of expression) statement// 示例for (const el of [2,4,6,8]) { 	document.write(el); }
```

在这个例子中，我们使用 for-of 语句显示了一个包含 4 个元素的数组中的所有元素。循环会一直持续到将所有元素都迭代完。与 for 循环一样，这里控制语句中的 const 是非必需的。但为了确保这个局部变量不被修改，推荐使用 const。

for-of 循环会按照可迭代对象的 next()方法产生值的顺序迭代元素。关于可迭代对象，将在下面进行详细介绍。

如果尝试迭代的变量不支持迭代，则 for-of 语句会抛出错误。

```js
const arr = [100, 200, 300, 400]for (const item of arr) {    console.log(item)}// for...of 循环可以替代 数组对象的 forEach 方法
```

其可替代forEach方法进行遍历，而且优点是可以随时使用break方法终止循环：

```js
arr.forEach(item => {
    console.log(item)
})

for (const item of arr) {
  console.log(item)
    if (item > 100) {
    break
  }

// forEach 无法跳出循环，必须使用 some 或者 every 方法
```

除了数组可以使用for...of遍历，一些伪数组同样也可以进行循环遍历，例如：函数中arguments对象、DOM中元素节点列表，他们与普通数组对象没有任何区别，这里就不单独演示了。

Set和Map对象：

```js
// 遍历 Set 与遍历数组相同

const s = new Set(['foo', 'bar'])

for (const item of s) {
  console.log(item)
}
// foo
// bar

// 遍历 Map 可以配合数组结构语法，直接获取键值

const m = new Map()
m.set('foo', '123')
m.set('bar', '345')

for (const [key, value] of m) {
    // 使用数组展开方法
    console.log(key, value)
}

// foo 123
// bar 345
```

普通对象不能被for...of遍历，至于原因，请看下面的可迭代接口，其中包含了一下Symbol.iterator：

```js
// 普通对象不能被直接 for...of 遍历

const obj = { foo: 123, bar: 456 }

for (const item of obj) {
  console.log(item)
}
```

## 十八、可迭代接口

ES中能够表示有结构的数据类型越来越多，从最早的数组和对象，到现在新增了set和map，并且还可以组合使用这些类型。为了提供一种统一的遍历方式，ES2015提供了一种统一的Iterable接口。例如ES中任意一种数据类型都有toString方法，这就是他们都实现了统一的规格标准（统一的接口）

实现Iterable接口就是for...of的前提，只要数据结构实现了可迭代接口，他就能被for...of遍历，也就是说之前的所有数据类型都实现了可迭代接口。

### 1.Iterator

在chrome浏览器的控制台进行测试：

> Chrome-console控制台

```js
console.log([]);  // 打印数组[]    length: 0    __proto__: Array(0)        ...        Symbol(Symbol.iterator): ƒ values()  // Symbol.iterator可迭代接口        Symbol(Symbol.unscopables): {copyWithin: true, entries: true, fill: true, find: true, findIndex: true, …}        __proto__: Object
```

```js
console.log(new Set());  // 打印SetSet(0) {}    [[Entries]]    size: (...)    __proto__: Set        add: ƒ add()        ...        Symbol(Symbol.iterator): ƒ values()  // Symbol.iterator可迭代接口        Symbol(Symbol.toStringTag): "Set"        get size: ƒ size()        __proto__: Object
```

```js
console.log(new Map());  // 打印MapMap(0) {}    [[Entries]]    size: (...)    __proto__: Map        clear: ƒ clear()        ...        Symbol(Symbol.iterator): ƒ entries()  // Symbol.iterator可迭代接口        Symbol(Symbol.toStringTag): "Map"        get size: ƒ size()        __proto__: Object
```

继续看看Symbol.iterator到底实现了什么：

> Chrome-console控制台

```js
const arr = ['foo', 'bar', 'baz']undefinedarr[Symbol.iterator]()Array Iterator {}	__proto__: Array Iterator    	next: ƒ next()		arguments: (...)        caller: (...)        length: 0        name: "next"		...const iterator = arr[Symbol.iterator]()undefinediterator.next(){value: "foo", done: false}
```

value中的就是数组中的第一个元素，done为false，当再次调用时，结果为相同的结构，此时的done为false。

> Chrome-console控制台

```js
iterator.next(){value: "bar", done: false}iterator.next(){value: "bar", done: true}
```

done属性的作用就是表示数组内部的属性是否全部遍历完成。

模拟迭代器：

```js
// 迭代器（Iterator）const set = new Set(['foo', 'bar', 'baz'])const iterator = set[Symbol.iterator]()console.log(iterator.next())  // { value: 'foo', done: false }console.log(iterator.next())  // { value: 'bar', done: false }console.log(iterator.next())  // { value: 'baz', done: false }console.log(iterator.next())  // { value: undefined, done: true }console.log(iterator.next())  // { value: undefined, done: true }while (true) {  const current = iterator.next()  if (current.done) {    break // 迭代已经结束了，没必要继续了  }  console.log(current.value)}
```

### 2.实现iterator接口

```js
// 实现可迭代接口（Iterable）const obj = {    // 实现了可迭代接口，Iterable，约定内部必须有用于范湖迭代器的iterator方法    [Symbol.iterator]: function () {        // 实现了迭代器接口，iterator其内部有用于迭代的next方法        return {            next: function () {                // 迭代结果接口，iterationResult，约定对象内部必须要有value属性，来表示当前被迭代到的数据，值为任意类型，done属性用来表示迭代是否结束                return {                    value: 'zce',                    done: true                }            }        }    }}
```

```js
const obj = {    store: ['foo', 'bar', 'baz'],    [Symbol.iterator]: function () {        let index = 0        const self = this        return {            next: function () {                const result = {                    value: self.store[index],                    done: index >= self.store.length                }                index++                return result            }        }    }}
```

### 3.迭代器模式

迭代器模式（特别是在 ECMAScript 这个语境下）描述了一个方案，即可以把有些结构称为“可迭代对象”（iterable），因为它们实现了正式的 Iterable 接口，而且可以通过迭代器 Iterator 消费。

```js
// 迭代器设计模式// 场景：你我协同开发一个任务清单应用// 我的代码 ===============================const todos = {  life: ['吃饭', '睡觉', '打豆豆'],  learn: ['语文', '数学', '外语'],  work: ['喝茶'],  // 提供统一遍历访问接口  each: function (callback) {    const all = [].concat(this.life, this.learn, this.work)    for (const item of all) {      callback(item)    }  },  // 提供迭代器（ES2015 统一遍历访问接口）  [Symbol.iterator]: function () {    const all = [...this.life, ...this.learn, ...this.work]    let index = 0    return {      next: function () {        return {          value: all[index],          done: index++ >= all.length        }      }    }  }}// 你的代码 ===============================// 实现统一遍历接口之前// for (const item of todos.life) {//   console.log(item)// }// for (const item of todos.learn) {//   console.log(item)// }// for (const item of todos.work) {//   console.log(item)// }// 实现统一遍历接口之后todos.each(function (item) {  console.log(item)})console.log('-------------------------------')for (const item of todos) {  console.log(item)}
```

## 十九、生成器及生成器的应用

生成器是 ECMAScript 6 新增的一个极为灵活的结构，拥有在一个函数块内暂停和恢复代码执行的能力。这种新能力具有深远的影响，比如，使用生成器可以自定义迭代器和实现协程。其可以避免异步编程中回调嵌套过深的问题，提供更好的额异步编程解决方案。

### 1.基本用法

生成器的形式是一个函数，函数名称前面加一个星号（*）表示它是一个生成器。只要是可以定义函数的地方，就可以定义生成器。

```js
// 生成器函数声明
function* generatorFn() {}

// 生成器函数表达式
let generatorFn = function* () {}
// 作为对象字面量方法的生成器函数
let foo = {
    * generatorFn() {}
}

// 作为类实例方法的生成器函数
class Foo {
    * generatorFn() {}
}

// 作为类静态方法的生成器函数
class Bar {
    static* generatorFn() {}
}

```

调用生成器函数会产生一个生成器对象。生成器对象一开始处于暂停执行（suspended）的状态。与迭代器相似，生成器对象也实现了 Iterator 接口，因此具有 next()方法。调用这个方法会让生成器开始或恢复执行。

```js
function* foo() {
  console.log('zce')
  return 100
}

const result = foo()
console.log(result)  // Object [Generator] {}
console.log(result.next())  // { value: 100, done: false }
```

yield 关键字可以让生成器停止和开始执行，也是生成器最有用的地方。生成器函数在遇到 yield关键字之前会正常执行。遇到这个关键字后，执行会停止，函数作用域的状态会被保留。停止执行的生成器函数只能通过在生成器对象上调用 next()方法来恢复执行：

```js
function* foo() {    console.log('1111')    yield 100    console.log('2222')    yield 200    console.log('3333')    yield 300}const generator = foo()console.log(generator.next()) // 第一次调用，函数体开始执行，遇到第一个 yield 暂停console.log(generator.next()) // 第二次调用，从暂停位置继续，直到遇到下一个 yield 再次暂停console.log(generator.next()) // 。。。console.log(generator.next()) // 第四次调用，已经没有需要执行的内容了，所以直接得到 undefined
```

### 2.实际应用

在生成器对象上显式调用 next()方法的用处并不大。其实，如果把生成器对象当成可迭代对象，那么使用起来会更方便：

```js
function* generatorFn() {     yield 1;     yield 2;     yield 3; } for (const x of generatorFn()) {     console.log(x); } // 1 // 2 // 3
```

```js
// Generator 应用// 案例1：发号器function* createIdMaker() {    let id = 1    while (true) {        yield id++    }}const idMaker = createIdMaker()console.log(idMaker.next().value)  // 1console.log(idMaker.next().value)  // 2console.log(idMaker.next().value)  // 3console.log(idMaker.next().value)  // 4// 案例2：使用 Generator 函数实现 iterator 方法const todos = {    life: ['吃饭', '睡觉', '打豆豆'],    learn: ['语文', '数学', '外语'],    work: ['喝茶'],    [Symbol.iterator]: function* () {        const all = [...this.life, ...this.learn, ...this.work]        for (const item of all) {            yield item        }    }}for (const item of todos) {    console.log(item)}
```

## 二十、ES2016和ES2017概述

### 1.ES2016

> 新增数组实例对象的includes方法，检查数组中是否包含某个指定元素

```js
const arr = ['foo', 1, NaN, false]

// 找到返回元素下标
console.log(arr.indexOf('foo'))
// 找不到返回 -1
console.log(arr.indexOf('bar'))
// 无法找到数组中的 NaN
console.log(arr.indexOf(NaN))

includes方法
// 直接返回是否存在指定元素
console.log(arr.includes('foo'))
// 能够查找 NaN
console.log(arr.includes(NaN))
```

> 新增指数运算符

```js
console.log(Math.pow(2, 10))
console.log(2 ** 10)  // 语言本身的运算符与加减乘除相同
```

### 2.ES2017

> object对象的三个扩展方法

- Object.values
- Object.entries
- Object.getOwnPropertyDescriptiors

```js
const obj = {
    foo: 'value1',
    bar: 'value2'
}
// Object.values -------------------返回对象中所有值组成的数组----------------------------------------
console.log(Object.values(obj))

// Object.entries ------------------以数组的形式返回对象中所有的键值对----------------------------------------
console.log(Object.entries(obj))
// 可以直接使用for...of遍历
for (const [key, value] of Object.entries(obj)) {
    console.log(key, value)
}
// 将对象转换为Map类型的对象
console.log(new Map(Object.entries(obj)))

// Object.getOwnPropertyDescriptors ----------获取对象中属性的完整描述信息------------------------------

const p1 = {
    firstName: 'Lei',
    lastName: 'Wang',
    get fullName() {
        return this.firstName + ' ' + this.lastName
    }
}
console.log(p1.fullName)

const p2 = Object.assign({}, p1)
p2.firstName = 'zce'
console.log(p2)

const descriptors = Object.getOwnPropertyDescriptors(p1)
console.log(descriptors)
const p2 = Object.defineProperties({}, descriptors)
p2.firstName = 'zce'
console.log(p2.fullName)
```

> 字符串方法

- String.prototype.padStart
- String.prototype.padEnd

```js
const books = {
    html: 5,
    css: 16,
    javascript: 128
}

for (const [name, count] of Object.entries(books)) {
    console.log(name, count)
}

for (const [name, count] of Object.entries(books)) {
    console.log(`${name.padEnd(16, '-')}|${count.toString().padStart(3, '0')}`)
}
//html 5
//css 16
//javascript 128
//html------------|005
//css-------------|016
//javascript------|128
```



