---
title: 第二章：HTML中的JavaScript
author: 5coder
tags: JavaScript高级程序设计
category: JavaScript高级程序设计
abbrlink: 32552
date: 2022-10-10 09:37:16
password:
keywords:
top:
cover:
---

# 第二章：HTML中的JavaScript

## 2.1`<script>`元素

将JavaScript插入HTML的主要方法是使用 `<script>`元素。

`<script>`元素有下列8个属性：

- async: 可选。表示应该立即开始下载脚本，但不阻止其他页面动作。只对外部脚本文件有效。
- charset: 可选。使用src属性指定的代码字符集。很少用，因为大部分浏览器不在乎它的值。
- crossorigin: 可选。配置相关请求的CORS(跨域资源共享)设置。
- defer: 可选。 表示在文档解析和显示完成后再执行脚本是没有问题的。只对外部脚本文件有效。
- integrity: 可选。允许比对接收到的资源和指定的加密签名以验证子资源完整性(SRI, Subresource Intergrity)。
- language: 废弃。
- src: 可选。表示包含要执行的代码的外部文件
- type: 可选。 代替language，表示代码块中脚本语言的内容类型(也称MIME类型)。如果这个值是module，则代代码会被当成ES6模块，这时才可以出现import和export关键字。

要嵌入行内JavaScript代码，直接把代码放在`<script>`元素中就行：

```html
<script>
	function sayHi(){
    	console.log("Hi!");
	}
</script>
```

包含在`<script>`内的代码会被从上到下解释。

注意代码中不能出现字符串`</script>`，下面的代码会导致浏览器报错：

```html
<script>
	function sayScript(){
    	console.log("</script>");
	}
</script>
```

需要使用转义字符串

```html
<script>
  function sayScript(){
      console.log("<\/script>");
  }
</script>
```

要包含外部文件中的Javascript，就必须使用src属性。

使用了src属性的`<script>`元素不应该再在`<script>`和`</script>`标签中再包含其他JavaScript代码，浏览器会忽略行内代码。

浏览器在解析这样的资源时，会向src属性指定的路径发送一个GET请求。**这个初始的请求不受浏览器同源策略限制**，但返回并执行的JavaScript则受限制。

```html
<script src="example.js"></script>
```

### 2.1.1标签位置

过去，所有`<script>`元素都被放在`<head>`标签内。这种做法目的是把外部CSS和JavaScript文件都集中到一起。但这意味着必须把所有JavaScript代码都下载、解析和解释完成后，才能开始渲染页面。这会导致页面渲染的明显延迟，在此期间浏览器窗口完全空白。

**现代Web应用程序通常将所有JavaScript引用放在`<body>`元素中的页面内容后面**。

```html
<!DOCTYPE html> 
<html> 
   <head> 
   		<title>Example HTML Page</title> 
   </head> 
   <body> 
   <!-- 这里是页面内容 --> 
   <script src="example1.js"></script> 
   <script src="example2.js"></script> 
   </body> 
</html>
```

### 2.1.2推迟执行脚本

在`<script>`元素上设置defer属性会告诉浏览器应该立即开始下载，但执行应该推迟。

```html
<script defer src="example.js"></script>
```

脚本会在浏览器解析到结束的<html>标签后才执行。HTML5规范要求脚本应该按照它们出现的顺序执行，因此第一个推迟的脚本会在第二个推迟的脚本之前执行，而且都会在DOMContentLoaded事件之前执行。**不过实际当中，不一定保证严格顺序，也不一定保证执行时间**，因此最好只包含一个这样的脚本。

### 2.1.3 异步执行脚本

HTML5为`<script>`元素定义了async属性。从改变脚本处理方式上看，async与defer类似。**但标记为async的脚本并不保证按照出现顺序的次序执行**。

```html
<!DOCTYPE html> 
<html> 
   <head> 
   <title>Example HTML Page</title> 
   <script async src="example1.js"></script> 
   <script async src="example2.js"></script> 
   </head> 
   <body> 
   <!-- 这里是页面内容 --> 
   </body> 
</html>
```

给脚本添加async属性的目的是告诉浏览器，不必等脚本下载和执行完成后再加载页面，同样也不必等到该异步脚本下载和执行后再加载其他脚本。**正因如此，异步脚本不应该在加载期间修改DOM**。

异步脚本保证会在页面的load事件前执行，但可能会在DOMContentLoaded之前或之后。

### 2.1.4动态加载脚本

除了`<script>`标签，还有其他方式可以加载脚本。因为 JavaScript 可以使用 DOM API，所以通过向 DOM 中动态添加 script 元素同样可以加载指定的脚本。只要创建一个 script 元素并将其添加到DOM 即可。

```js
let script = document.createElement('script'); 

script.src = 'gibberish.js'; 

document.head.appendChild(script); 
```

当然，在把 HTMLElement 元素添加到 DOM 且执行到这段代码之前不会发送请求。默认情况下，以这种方式创建的`<script>`元素是以异步方式加载的，相当于添加了 async 属性。不过这样做可能会有问题，因为所有浏览器都支持 createElement()方法，但不是所有浏览器都支持 async 属性。因此，如果要统一动态脚本的加载行为，可以明确将其设置为同步加载：

```javascript
let script = document.createElement('script'); 

script.src = 'gibberish.js'; 

script.async = false; 

document.head.appendChild(script); 
```

以这种方式获取的资源对浏览器预加载器是不可见的。这会严重影响它们在资源获取队列中的优先级。根据应用程序的工作方式以及怎么使用，这种方式可能会严重影响性能。要想让预加载器知道这些动态请求文件的存在，可以在文档头部显式声明它们：

```html
<link rel="preload" href="gibberish.js"> 
```

## 2.2行内代码与外部文件

虽然可以直接在HTML文件中嵌入JavaScript代码，但通常认为最佳实践是尽可能将JavaScript代码放在外部文件中。理由如下：

- **可维护性**。用一个目录保存所有JavaScript文件更容易维护。开发者可以独立于HTML页面来编辑代码。
- **缓存**。浏览器会根据特定的设置缓存所有外部链接的JavaScript文件。
- 适应未来。通过把JavaScript放到外部文件中，就不必考虑用XHTML或前面提到的注释黑科技。包含外部JavaScript文件的语法在HTML和XHTML中是一样的。



## 2.3文档模式

最初的文档模式有两种：**混杂模式**(quirks mode)和**标准模式**(standards mode)。前者让IE像IE5一样(支持一些非标准的特性)，后者让IE具有兼容标准的行为。

IE初次支持文档模式切换以后，其他浏览器也跟着实现了。随着浏览器的普遍实现，又出现了第三种文档模式：**准标准模式**(almost standards mode)。

准标准模式与标准模式非常接近，很少需要区分。

标准模式通过下列几种文档类型声明开启：

```html
<!-- HTML 4.01 Strict --> 

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" 

"http://www.w3.org/TR/html4/strict.dtd"> 
```

```html
<!-- XHTML 1.0 Strict --> 

<!DOCTYPE html PUBLIC 

"-//W3C//DTD XHTML 1.0 Strict//EN" 

"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
```


准标准模式通过过渡性文档类型（Transitional）和框架集文档类型（Frameset）来触发：

```html
<!-- HTML 4.01 Transitional --> 

<!DOCTYPE HTML PUBLIC 


"-//W3C//DTD HTML 4.01 Transitional//EN" 

"http://www.w3.org/TR/html4/loose.dtd"> 

<!-- HTML 4.01 Frameset --> 

<!DOCTYPE HTML PUBLIC 


"-//W3C//DTD HTML 4.01 Frameset//EN" 

"http://www.w3.org/TR/html4/frameset.dtd"> 

<!-- XHTML 1.0 Transitional --> 

<!DOCTYPE html PUBLIC 


"-//W3C//DTD XHTML 1.0 Transitional//EN" 

"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 

<!-- XHTML 1.0 Frameset --> 

<!DOCTYPE html PUBLIC 


"-//W3C//DTD XHTML 1.0 Frameset//EN" 

"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"> 
```

## 2.4`<noscript>`元素

针对早期浏览器不支持 JavaScript 的问题，需要一个页面优雅降级的处理方案。

`<noscript>`元素可以包含任何可以出现在`<body>`中的 HTML 元素，<script>除外。在下列两种

情况下，浏览器将显示包含在`<noscript>`中的内容：

- 浏览器不支持脚本；
- 浏览器对脚本的支持被关闭。

```html
<!DOCTYPE html> 
<html> 
 <head> 
 <title>Example HTML Page</title> 
 <script defer="defer" src="example1.js"></script> 
 <script defer="defer" src="example2.js"></script> 
 </head> 
 <body> 
 <noscript> 
 <p>This page requires a JavaScript-enabled browser.</p> 
 </noscript> 
 </body> 
</html>
```

这个例子是在脚本不可用时让浏览器显示一段话。如果浏览器支持脚本，则用户永远不会看到它。

## 2.5小结

JavaScript 是通过`<script>`元素插入到 HTML 页面中的。这个元素可用于把 JavaScript 代码嵌入到HTML 页面中，跟其他标记混合在一起，也可用于引入保存在外部文件中的 JavaScript。本章的重点可以总结如下。

- 要包含外部 JavaScript 文件，必须将 src 属性设置为要包含文件的 URL。文件可以跟网页在同一台服务器上，也可以位于完全不同的域。
- 所有`<script>`元素会依照它们在网页中出现的次序被解释。在不使用 defer 和 async 属性的情况下，包含在`<script>`元素中的代码必须严格按次序解释。
- 对不推迟执行的脚本，浏览器必须解释完位于`<script>`元素中的代码，然后才能继续渲染页面的剩余部分。为此，通常应该把`<script>`元素放到页面末尾，介于主内容之后及`</body>`标签之前。
- 可以使用 defer 属性把脚本推迟到文档渲染完毕后再执行。推迟的脚本原则上按照它们被列出的次序执行。
- 可以使用 async 属性表示脚本不需要等待其他脚本，同时也不阻塞文档渲染，即异步加载。异步脚本不能保证按照它们在页面中出现的次序执行。
- 通过使用`<noscript>`元素，可以指定在浏览器不支持脚本时显示的内容。如果浏览器支持并启用脚本，则`<noscript>`元素中的任何内容都不会被渲染。
