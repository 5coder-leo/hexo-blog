---
title: Webpack 5
author: 5coder
tags: Webpack
category: 大前端
abbrlink: 21855
date: 2022-11-20 21:12:56
password:
keywords:
top:
cover:
---

# Webpack5

##  1.Why Webpack

**个人将前端开发分为三个阶段：**

### 1.1 Web1.0

Web1.0前端主要工作：

- 前端主要编写静态页面
- 对于JavaScript的使用，主要是进行表单验证和动画效果制作

### 1.2 Web2.0之AJAX

伴随着AJAX的诞生，前端的工作模式也发生了很大变化，前端不仅仅是展示界面，而且还可以管理数据以及和用户进行数据的交互。在这样的阶段过程中，诞生了像jQuery这样的优秀前端工具库。

### 1.3 大前端开发（现代Web开发）

在这个阶段中，前端的工作变得更加多样化和复杂化，例如现在前端不仅仅需要开发PC端Web界面，还有移动端的Web界面，以及小程序和公众号，甚至有些时候还需要做App和桌面客户端。

伴随着需要做的事情越来越多，流程也越来越复杂，因此就会出现一些问题。比如说：

现代Web开发“问题”

- 采用模块化开发

  不同浏览器对模块化的支持不同，而且模块化本身存在多种实现规范，这些给最终产出带来了影响

- 使用新特性提高效率保证安全性

  编码过程中，为了提高开发效率，还会使用ES6+、TypeScript、Saas、Less，这些条件浏览器在默认情况下不能正常处理

- 实时监听开发过程使用热更新

- 项目结果打包压缩优化

需要有一个工具站出来解决问题，可以让开发者在入口的地方随心所欲，用个人喜欢的技术栈完成开发，从而不需要关系过程，但是最终的结果可以在浏览器上正常展示，因此这里就会用到打包工具。当前Vue、React、Angular本身集成Webpack。

## 2.Webpack 上手

Webpack定义：为现代JavaScript应用提供静态模块打包

Webpack功能:

- 打包：将不同类型资源按模块处理进行打包。可以把js、css、img等资源按照模块的方式处理，然后统一的打包输出
- 静态：打包后最终产出静态资源
- 模块：Webpack支持不同规范的模块化开发（ES Module、CommonJS、AMD等）

构件如图目录结构，并编码

![](http://5coder.cn/img/1667394396_beb492fc34507f1b076b9fb246228fe8.png)

在web server中进行预览，发现虽然在index.html中使用了`type="module"`，但是依然无法同时识别ES Module和CommonJS。

![](http://5coder.cn/img/1667394497_bd4fe136ff1a0362f3de8235307b626b.png)

此时，提前安装好的Webpack就起了作用，在命令行终端输入：`Webpack`，这时发现目录中输出了dist目录。这里需要注意，Webpack打包会默认找到项目目录下的src目录，并且找到index.js作为入口文件，对依赖进行打包处理，并输出到dist目录中，输出结果默认为`main.js`。如下图：

![image-20221102211043151](http://5coder.cn/img/1667394643_8920810d9d8143e706363a4a30b5877a.png)

观察main.js，发现当前Webpack并未解决ES6+的语法兼容问题

此时将index.html中引入的js文件变更为`dist/main.js`。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>上手Webpack</title>
</head>
<body>

<script type="module" src="./src/index.js"></script>
</body>
</html>
```

展示结果如下：

![](http://5coder.cn/img/1667394718_2c1aa2d11029ec079ff81e34b7d91f28.png)

## 3.Webpack 配置文件

目录结构：![image-20221102221622090](http://5coder.cn/img/1667398582_585326854b7b0cc74ebbd31f5df7a061.png)

自定义打包入口文件和打包输出目录及输出文件名。

- 通过命令行参数进行打包

  `yarn Webpack --entry ./src/main.js --output-path ./build`，其中`--entry`指定入口文件，`--output-path`指定输入路径

- 通过package.json配置简短命令

  ```json
  ...
  "scripts": {
    "build": "Webpack --entry ./src/main.js --output-path ./build"
  }
  ...
  ```

  通过命令行运行`yarn build`进行打包

- 通过**Webpack.config.js**配置文件进行配置

  ```js
  const path = require('path')
  module.exports = {
    entry: './src/index.js',
    output: {
      filename: 'build.js',
      path: path.resolve(__dirname, 'dist')  // 必须使用绝对路径，不然会Webpack抛出错误
    }
  }
  ```

## 4.Webpack 依赖图

![](https://img-blog.csdnimg.cn/img_convert/cfbef08b888d5b8e76b5b2f65bdfa1f2.png)

目录结构：

![](http://5coder.cn/img/1667400704_189acc0e75d0f3517b266b900b30bae9.png)

![](http://5coder.cn/img/1667401452_afd07c7cbc8d07f5ca7e4ce692b51594.png)

在index.js中引入lg.js，随后在index.html中引入dist目录下的main.js。Webpack在打包过程中会自动寻找依赖关系并引入，最终打包为main.js。

> 上文提到可以使用命令行参数对入口文件、输出目录及输出文件名做配置，这里使用--config参数可以对Webpack配置文件进行自定义。例如：
>
> ```json
> ...
> {
> "scripts" : {
> "build": "Webpack --config my-Webpack-config.js"
> }
> }
> ...
> ```
>
> 此时Webpack就会从my-Webpack-config.js读取配置进行打包处理。

## 5.CSS-Loader

### 5.1 为什么需要loader

在项目中，模拟创建dom元素，并给dom元素赋css样式，如下代码：

![](http://5coder.cn/img/1667403009_b94ceac11425ea170af7849b1dc6b1db.png)

- index.html中script引入打包后的main.js

- index.js入口文件中引入login.js

  ```js
  // login.js
  function createDom() {
    const h2 = document.createElement('h2')
    h2.innerHTML = '拉勾教育'
    h2.className = 'title'
    return h2
  }
  document.body.appendChild(createDom())
  ```

- 此时，需要.title添加css样式

  ```css
  /*
  login.css
  */
  .title {
    color: red
  }
  ```

- 在login.js中引入login.css，并进行Webpack打包，此时会抛出异常，css文件并不是一个模块。

  ```js
  import '../css/login.css'
  
  function login() {
    const oH2 = document.createElement('h2')
    oH2.innerHTML = '拉勾教育前端'
    oH2.className = 'title'
    return oH2
  }
  
  document.body.appendChild(login())
  
  ```

  

### 5.2 loader是什么

loader是一个模块，内部使用js实现具体逻辑，比如现在需要一个loader让login.css代码转换为Webpack能识别的模块。

### 5.3 css-loader

- 安装css-loader

  `yarn add css-loader`

**Webpack4中对loader的使用一般分为三种：**

- 行内loader
- 配置文件loader
- Webpack-cli命令行中使用loader

**Webpack5中对cli中使用loader不建议使用，已废弃**

- 行内使用loader，多个loader使用英文**!**进行分隔

```js
import 'css-loader!../css/login.css'


function login() {
  const oH2 = document.createElement('h2')
  oH2.innerHTML = '拉勾教育前端'
  oH2.className = 'title'
  return oH2
}

document.body.appendChild(login())
```

重新执行`yarn Webpack`，虽然没有语法报错，但是样式并未生效。还需要使用一个`style-loader`。

- 配置文件中使用`css-loader`

  ```js
  const path = require('path')
  
  module.exports = {
    entry: './src/index.js',
    output: {
      filename: 'main.js',
      path: path.resolve(__dirname, 'dist')
    },
    module: {
      rules: [
        // {
        //   test: /\.css$/, // 一般就是一个正则表达式，用于匹配我们需要处理的文件类型
        //   use: [
        //     {
        //       loader: 'css-loader'
        //     }
        //   ]
        // },
        // {
        //   test: /\.css$/,
        //   loader: 'css-loader'
        // },
        {
          test: /\.css$/,
          use: ['css-loader']
        }
      ]
    }
  }
  ```


## 6.style-loader 使用

然后回到**Webpack.config.js**下，将入口文件的路径指向新创建的css文件。随后配置loader组件，test值为正则表达式/.css$/，use配置一个数组，分别为style-loader以及style-loader

```js
const path = require('path')

module.exports = {
  mode: 'none',
  entry: './src/main.css',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist')
  },
  module: {
    // rules数组针对于其它资源模块的加载规则，每个规则对象的都需要设置两个属性。
    rules: [
      {
        test: /.css$/,  // test用来去匹配在打包过程当中所遇到的文件路径
        // use用来去指定我们匹配到的文件，需要去使用的loader
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  }
}

```

命令行启动，yarn Webpack，通过serve . 运行，在浏览器中访问就可以看到我们的css生效了。

**ps**:use中，如果配置了多个loader，其执行顺序是从数组最后一个元素往前执行。所以这里一定要把css-loader放到最后，因为我们必须要先通过css-loader把css代码转换为模块才可以正常打包。

style-loader工作代码在bundle.js中，部分代码如下：

![](https://img-blog.csdnimg.cn/img_convert/f78c11744afcfdb8ab25fd48aa08da6f.png)

**loader是Webpack实现整个前端模块化的核心，通过不同的loader就可以实现加载任何类型的资源。**

## 7.less-loader

在项目中使用less编写css代码，首先在login.js中正常引入login.less，正常使用Webpack进行编译，发现报错基本与未使用css-loader相同。Webpack默认不支持less文件的编译，所以按照思路，需要先将less文件编译为css文件，然后使用css-loader与style-loader搭配使用，将css样式引入到index.html。下面进行尝试：

首先安装less，尝试把login.less编译为index.css

```bash
npm i less -D  # 安装less
npx less ./src/css/login.less index.css  # 使用less将login.less编译为index.css
```

![](http://5coder.cn/img/1667513100_6f31e299a2fb9d937e093e6d8a85d6db.png)

其次在login.js中将其引入：

![](http://5coder.cn/img/1667513148_9af2e39e6be0b32c985eac5017a454ba.png)

此时运行Webpack进行打包，发现会抛出错误，错误类型与上面提到的Webpack无法编译css文件时相同。

![](http://5coder.cn/img/1667513263_b6821fb4eacb9e0df5f041adc53aa93b.png)

回到初始思路上，我们需要less-loader将less文件编译为css文件，其次使用css-loader搭配style-loader，将css样式编译至html文件中，所以需要进行配置，配置思路与css相同。如下代码：

```js
const path = require('path')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.less$/,
        use: ['style-loader', 'css-loader', 'less-loader']
      }
    ]
  }
}
```

ps:记住loader加载使用顺序是：**从右到左，从下到上**

![](http://5coder.cn/img/1667513408_036968181be9a03b7517c5c59223e60a.png)

## 8.browserslistrc 工作流程

caniuse.com

.browserslistrc 是在不同的前端工具之间共用目标浏览器和 [node](https://so.csdn.net/so/search?q=node&spm=1001.2101.3001.7020) 版本的配置文件。它主要被以下工具使用：

> Autoprefixer
> Babel
> post-preset-env
> [eslint](https://so.csdn.net/so/search?q=eslint&spm=1001.2101.3001.7020)-plugin-compat
> stylelint-unsupported-browser-features
> [postcss](https://so.csdn.net/so/search?q=postcss&spm=1001.2101.3001.7020)-normalize

**Webpack默认会安装browserlistrc**

前端工程需要在package.json中配置

```json
{
  "browserslist": [
    "last 1 version",
    "> 1%",
    "maintained node versions",
    "not dead"
  ]
}
```

也可在.browserslistrc中配置

```
# 注释是这样写的，以#号开头
last 1 version #最后的一个版本
> 1%  #代表全球超过1%使用的浏览器
maintained node versions #所有还被 node 基金会维护的 node 版本
not dead
```

不配置默认为：**> 0.5%, last 2 versions, Firefox ESR, not dead**
在当前目录下查询目标浏览器 **npx browserslist**

**查询条件列表**
你可以用如下查询条件来限定浏览器和 node 的版本范围（大小写不敏感）：

```
> 5%: 基于全球使用率统计而选择的浏览器版本范围。>=,<,<=同样适用。
> 5% in US : 同上，只是使用地区变为美国。支持两个字母的国家码来指定地区。
> 5% in alt-AS : 同上，只是使用地区变为亚洲所有国家。这里列举了所有的地区码。
> 5% in my stats : 使用定制的浏览器统计数据。
cover 99.5% : 使用率总和为99.5%的浏览器版本，前提是浏览器提供了使用覆盖率。
cover 99.5% in US : 同上，只是限制了地域，支持两个字母的国家码。
cover 99.5% in my stats :使用定制的浏览器统计数据。
maintained node versions :所有还被 node 基金会维护的 node 版本。
node 10 and node 10.4 : 最新的 node 10.x.x 或者10.4.x 版本。
current node :当前被 browserslist 使用的 node 版本。
extends browserslist-config-mycompany :来自browserslist-config-mycompany包的查询设置
ie 6-8 : 选择一个浏览器的版本范围。
Firefox > 20 : 版本高于20的所有火狐浏览器版本。>=,<,<=同样适用。
ios 7 :ios 7自带的浏览器。
Firefox ESR :最新的火狐 ESR（长期支持版） 版本的浏览器。
unreleased versions or unreleased Chrome versions : alpha 和 beta 版本。
last 2 major versions or last 2 ios major versions :最近的两个发行版，包括所有的次版本号和补丁版本号变更的浏览器版本。
since 2015 or last 2 years :自某个时间以来更新的版本（也可以写的更具体since 2015-03或者since 2015-03-10）
dead :通过last 2 versions筛选的浏览器版本中，全球使用率低于0.5%并且官方声明不在维护或者事实上已经两年没有再更新的版本。目前符合条件的有 IE10,IE_Mob 10,BlackBerry 10,BlackBerry 7,OperaMobile 12.1。
last 2 versions :每个浏览器最近的两个版本。
last 2 Chrome versions :chrome 浏览器最近的两个版本。
defaults :默认配置> 0.5%, last 2 versions, Firefox ESR, not dead。
not ie <= 8 : 浏览器范围的取反。
可以添加not在任和查询条件前面，表示取反
```

**注意：**
**1.可以使用如下写法，从另外一个输出 browserslist 配置的包导入配置数据:**

```
"browserslist": [
	"extends browserslist-config-mycompany"
]
```

为了安全起见，额外的配置包只支持前缀 browserslist-config- 的包命名. npm包作用域也同样支持 @scope/browserslist-config,例如：
`@scope/browserslist-config or @scope/browserslist-config-mycompany.`

```
#When writing a shared Browserslist package, just export an array.
#browserslist-config-mycompany/index.js:
module.exports = [
  'last 1 version',
  '> 1%',
  'ie 10'
]
```

**2.环境的差异化配置**
你可以为不同的环境配置不同的浏览器查询条件。Browserslist 将依赖BROWSERSLIST_ENV 或者 NODE_ENV查询浏览器版本范围。如果两个环境变量都没有配置正确的查询条件，那么优先从 production 对应的配置项加载查询条件，如果再不行就应用默认配置。
在 package.json:

```json
  "browserslist": {
    "production": [
      "> 1%",
      "ie 10"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version"
    ]
  }
```

在配置文件`.broswerslistrc`中

```txt
[production staging]
> 1%
ie 10

[development]
last 1 chrome version
last 1 firefox version
```

## 9.postcss 工作流程



官网说：“PostCSS，一个使用 JavaScript 来处理CSS的框架”。这句话高度概括了 PostCSS 的作用，但是太抽象了。按我理解，PostCSS 主要做了三件事：

1. `parse`：把 CSS 文件的字符串解析成抽象语法树（Abstract Syntax Tree）的框架，解析过程中会检查 CSS 语法是否正确，不正确会给出错误提示。
2. `runPlugin`: 执行插件函数。PostCSS 本身不处理任何具体任务，它提供了以特定属性或者规则命名的事件。有特定功能的插件（如 autoprefixer、CSS Modules）会注册事件监听器。PostCSS 会在这个阶段，重新扫描 AST，执行注册的监听器函数。
3. `generate`: 插件对 AST 处理后，PostCSS 把处理过的 AST 对象转成 CSS string。

![](https://ask.qcloudimg.com/http-save/yehe-2427692/2386c26e21218e76656ede2fa05d6826.png?imageView2/2/w/1620)

**「如果没有插件」**，那么初始传入的 CSS string 和 generate 生成的 CSS string 是一样的。由此可见，PostCSS 本身并不处理任何具体的任务，只有当我们为其附加各种插件之后，它才具有实用性。

### 9.1 第一阶段：parse

**CSS 语法简述**

CSS 规则集（rule-set）由选择器和声明块组成：

![img](https://ask.qcloudimg.com/http-save/yehe-2427692/25e995bac82d1baee8c2845c288e9f5f.png?imageView2/2/w/1620);

- 选择器指向您需要设置样式的 HTML 元素。
- 声明块包含一条或多条用分号分隔的声明。
- 每条声明都包含一个 CSS 属性名称和一个值，以冒号分隔。
- 多条 CSS 声明用分号分隔，声明块用花括号括起来。

**五类对象**

AST 用五类对象描述 CSS 语法。这里举个具体的例子，再打印出对应的 AST 结果，对照了解 AST 五类对象和 CSS 语法的对应关系。

`app.css` 文件中写如下内容：

```javascript
@import url('./app-02.css');

.container {
  color: red;
}
```



**Declaration（声明） 对象**

Declaration 对象用来描述 CSS 中的每一条声明语句。

- type 标记当前对象的类型
- parent 记录父对象的实例
- prop 记录声明中的属性名
- value 记录声明中的值
- raws 字段记录声明前的字符串、声明属性和值之间的符号的字符串
- 其余字段解释见代码中的注释。

上边 CSS 文件中的`color: red;`会被描述成如下对象：

```javascript
{
    parent: Rule,       // 外层的选择器被转译成 Rule 对象，是当前声明对象的 parent
    prop: "color",      // prop 字段记录声明的属性
    raws: {             // raws 字段记录声明前、后的字符串，声明属性和值之间的字符串，以及前边语句是否分号结束。
        before: '\n ',  // raws.before 字段记录声明前的字符串
        between: ': ', // raws.between 字段记录声明属性和值之间的字符串
    },
    source: {          // source 字段记录声明语句的开始、结束位置，以及当前文件的信息
        start: { offset: 45, column: 3, line: 4 },
        end: { offset: 55, column: 13, line: 4 },
        input: Input {
            css: '@import url('./app-02.css');\n\n.container {\n  color: red;\n}',
            file: '/Users/admin/temp/postcss/app.css',
            hasBOM: false,
            Symbol(fromOffsetCache): [0, 29, 30, 43, 57]
        }
    },
    Symbol('isClean'): false,  // Symbol(isClean) 字段默认值都是 false，用于记录当前对象关联的 plugin 是否执行。plugin 会在后续解释
    Symbol('my'): true,        // Symbol(my) 字段默认值都是 true，用于记录当前对象是否是对应对象的实例，如果不是，可以根据类型把对象的属性设置为普通对象的 prototype 属性
    type: 'decl',            // type 记录对象类型，是个枚举值，声明语句的 type 固定是 decl
    value: "red"             // value 字段记录声明的值
}
```



每个字段的含义和功能已经以注释的形式进行了解释。

**Rule 对象**

Rule 对象是描述选择器的。

- type 记录对象的类型
- parent 记录父对象的实例
- nodes 记录子对象的实例
- selector 记录选择器的字符串
- raws 记录选择器前的字符串、选择器和大括号之间的字符串、最后一个声明和结束大括号之间的字符串
- 其余字段解释见代码中的注释。

上边 app.css 文件中`.container`经过 postcss 转译后的对象是(每个字段的含义和功能已经以注释的形式进行了解释)：

```javascript
{
    nodes: [Declaration], // nodes 记录包含关系，Rule 对象包含 Declaration 对象
    parent: Root,        // 根对象是 Root 对象，是当前声明对象的 parent
    raws: {              // raws 字段记录如下
        before: '\n\n',  // raws.before 字段记录选择器前的字符串
        between: ' ',    // raws.between 字段记录选择器和大括号之间的字符串
        semicolon: true, // raws.semicolon 字段记录前置声明语句是正常分号结束
        after: '\n'      // raws.after 字段记录最后一个声明和结束大括号之间的字符串
    },
    selector:'.container', // selector 记录 selector
    source: {            // source 字段记录选择器语句的开始、结束位置，以及当前文件的信息
        start: { offset: 30, column: 1, line: 3 },
        input: Input {
            css: '@import url('./app-02.css');\n\n.container {\n  color: red;\n}',
            file: '/Users/admin/temp/postcss/app.css',
            hasBOM: false,
            Symbol(fromOffsetCache): [0, 29, 30, 43, 57]
        },
        end: { offset: 57, column: 1, line: 5 }
    },
    Symbol('isClean'): false,  // Symbol(isClean) 字段默认值都是 false，用于记录当前对象关联的 plugin 是否执行。plugin 会在后续解释
    Symbol('my'): true,        // Symbol(my) 字段默认值都是 true，用于记录当前对象是否是对应对象的实例，如果不是，可以根据类型把对象的属性设置为普通对象的 prototype
    type: 'rule'           // type 记录对象类型，是个枚举值，声明语句的 type 固定是 rule
}
```



**Root 对象**

Root 对象是 AST 对象的根对象。

- type 记录当前对象的类型
- nodes 属性记录子节点对应对象的实例。

上边 app.css 文件中 root 对象是(每个字段的含义和功能已经以注释的形式进行了解释)：

```javascript
{
    nodes: [AtRule, Rule], // nodes 记录子对象（选择器和 @开头的对象），AtRule 对象会在后边提到
    raws: {                // raws 字段记录如下
        semicolon: false,  // raws.semicolon 最后是否是分号结束
        after: ''          // raws.after 最后的空字符串
    },
    source: {              // source 字段记录根目录语句的开始，以及当前文件的信息
        start: { offset: 0, column: 1, line: 1 },
        input: Input {
            css: '@import url('./app-02.css');\n\n.container {\n  color: red;\n}',
            file: '/Users/admin/temp/postcss/app.css',
            hasBOM: false,
            Symbol(fromOffsetCache): [0, 29, 30, 43, 57]
        }
    },
    Symbol('isClean'): false,  // Symbol(isClean) 字段默认值都是 false，用于记录当前对象关联的 plugin 是否执行。plugin 会在后续解释
    Symbol('my'): true,        // Symbol(my) 字段默认值都是 true，用于记录当前对象是否是对应对象的实例，如果不是，可以根据类型把对象的属性设置为普通对象的 prototype
    type: 'root'           // type 记录对象类型，是个枚举值，声明语句的 type 固定是 root
}
```



**AtRule 对象**

CSS 中除了选择器，还有一类语法是 `@` 开头的，例如 `@import`、`@keyframes`、`@font-face`，PostCSS 把这类语法解析成 AtRule 对象。

- type 记录当前对象的类型
- parent 记录当前对象的父对象
- name 记录`@`紧跟着的单词
- params 记录 name 值

例如 `@import url("./app-02.css");` 将被解析成如下对象：

```javascript
{
    name: "import",                  // name 记录 @ 紧跟着的单词
    params: "url('./app-02.css')",   // params 记录 name 值
    parent: Root,                    // parent 记录父对象
    raws: {                          // raws 字段记录如下
        before: '',                  // raws.before 记录 @语句前的空字符串
        between: '',                 // raws.between 记录 name 和 { 之间的空字符串
        afterName: '',                // raws.afterName 记录 name 和 @ 语句之间的空字符串
        after: '',                   // raws.after 记录大括号和上一个 rule 之间的空字符串
        semicolon: false             // raws.semicolon 上一个规则是否是分号结束
    },
    source: {                        // source 字段记录@语句的开始，以及当前文件的信息
        start: { offset: 0, column: 1, line: 1 },
        end: { offset: 27, column: 28, line: 1 },
        input: Input {
            css: '@import url('./app-02.css');\n\n.container {\n  color: red;\n}',
            file: '/Users/admin/temp/postcss/app.css',
            hasBOM: false,
            Symbol(fromOffsetCache): [0, 29, 30, 43, 57]
        }
    },
    Symbol('isClean'): false,  // Symbol(isClean) 字段默认值都是 false，用于记录当前对象关联的 plugin 是否执行。plugin 会在后续解释
    Symbol('my'): true,        // Symbol(my) 字段默认值都是 true，用于记录当前对象是否是对应对象的实例，如果不是，可以根据类型把对象的属性设置为普通对象的 prototype
    type: 'atrule'          // type 记录对象类型，是个枚举值，声明语句的 type 固定是 atrule
}
```



**Comment 对象**

css 文件中的注释被解析成 Comment 对象。text 字段记录注释内容。`/* 你好 */`被解析成：

```javascript
{
    parent: Root,             // parent 记录父对象
    raws: {                   // raws 字段记录如下
        before: '',           // raws.before 记录注释语句前的空字符串
        left: ' ',            // raws.left 记录注释语句左侧的空字符串
        right: ' '            // raws.right 记录注释语句右侧的空字符串
    },
    source: {                 // source 字段记录注释语句的开始、结束位置，以及当前文件的信息
        start: {…}, input: Input, end: {…}
    },
    Symbol('isClean'): false,  // Symbol(isClean) 字段默认值都是 false，用于记录当前对象关联的 plugin 是否执行。plugin 会在后续解释
    Symbol('my'): true,        // Symbol(my) 字段默认值都是 true，用于记录当前对象是否是对应对象的实例，如果不是，可以根据类型把对象的属性设置为普通对象的 prototype
    text: '你好',             // text 记录注释内容
    type: 'comment'          // type 记录对象类型，是个枚举值，声明语句的 type 固定是 comment
}
```



**图解五类对象之间的继承关系**

从上一段可以知道，CSS 被解析成 Declaration、Rule、Root、AtRule、Comment 对象。这些对象有很多公共方法，PostCSS 用了面向对象的继承思想，把公共方法和公共属性提取到了父类中。

Root、Rule、AtRule 都是可以有子节点的，都有 nodes 属性，他们三个继承自 Container 类，对 nodes 的操作方法都写在 Container 类中。Container、Declaration、Comment 继承自 Node 类，所有对象都有 Symbol('isClean')、Symbol('my')、raws、source、type 属性，都有toString()、error()等方法，这些属性和方法都定义在 Node 类中。

Container、Node 是用来提取公共属性和方法，不会生成他们的实例。

五个类之间的继承关系如下图所示：

![img](https://ask.qcloudimg.com/http-save/yehe-2427692/108df3f074ded115ffa140ef93701175.png?imageView2/2/w/1620);

图中没有穷举类的方法，好奇的同学可以看直接看源码文件: https://github.com/postcss/postcss/tree/main/lib 。

**把 CSS 语法解析成 AST 对象的具体算法**

算法对应源码中位置是：`postcss/lib/parser.js`中的`parse`方法，代码量不大，可自行查看。

### 9.2 第二阶段：runPlugin

PostCSS 本身并不处理任何具体的任务，只有当我们为其附加各种插件之后，它才具有实用性。

PostCSS 在把 CSS string 解析成 AST 对象后，会扫描一边 AST 对象，每一种 AST 的对象都可以有对应的监听器。在遍历到某类型的对象时，如果有对象的监听器，就会执行其监听器。

**第一类监听器**

PostCSS 提供的**「以特定属性或者规则命名」**的事件监听器，如下：

> CHILDREAN 代表子节点的事件监听器。

```javascript
// root
['Root', CHILDREN, 'RootExit']

// AtRule
['AtRule', 'AtRule-import', CHILDREN, 'AtRuleExit', 'AtRuleExit-import']

// Rule
['Rule', CHILDREN, 'RuleExit']

// Declaration
['Declaration', 'Declaration-color', 'DeclarationExit', 'DeclarationExit-color']

// Comment
['Comment', 'CommentExit']
```

PostCSS 以深度优先的方式遍历 AST 树。

- 遍历到 Root 根对象，第一步会执行所有插件注册的 Root 事件监听器，第二步检查 Root 是否有子对象，如果有，则遍历子对象，执行子对象对应的事件监听器；如果没有子对象，则直接进入第三步，第三步会执行所有插件注册的 RootExit 事件监听器。插件注册的 Root、RootExit 事件的监听器只能是函数。函数的第一个参数是当前访问的 AST 的 Root 对象，第二个参数是 postcss 的 Result 对象和一些其他属性，通过 Result 对象可以获取 css string、opts 等信息。

```javascript
{
  Root: (rootNode, helps) => {},
  RootExit: (rootNode, helps) => {}
}
```

- 遍历到 Rule 对象，则和访问 Root 根对象是一样的逻辑，先执行所有插件注册的 Rule 事件监听器，再遍历子对象，最后执行所有插件注册的 RuleExit 事件监听器。插件注册的 Rule、RuleExit 事件的监听器只能是函数。

```javascript
{
  Rule: (ruleNode, helps) => {},
  RuleExit: (ruleNode, helps) => {}
}
```

- 遍历到 AtRule 对象。插件注册的 AtRule 的事件监听器可以是函数，也可以是对象。对象类型的监听器，对象属性的 key 是 AtRule 对象的 name 值，value 是函数。AtRuleExit 是一样的逻辑。事件的执行顺序是：`['AtRule', 'AtRule-import', CHILDREN, 'AtRuleExit', 'AtRuleExit-import']`。CHILDREAN 代表子节点的事件。``` // 函数 { AtRule: (atRuleNode, helps) => {} }

```javascript
// 对象
{
  AtRule: {
      import: (atRuleNode, helps) => {},
      keyframes: (atRuleNode, helps) => {}
  }
}
```

- 遍历到 Declaration 对象。插件注册的 Declaration 的事件监听器可以是函数，也可以是对象，对象属性的 key 是 Declaration 对象的 prop 值，value 是函数。DeclarationExitExit 是一样的逻辑。事件的执行顺序是：`['Declaration', 'Declaration-color', 'DeclarationExit', 'DeclarationExit-color']`。Declaration 没有子对象，只需要执行当前对象的事件，不需要深度执行子对象的事件。

```javascript
// 函数
{
  Declaration: (declarationNode, helps) => {}
}

// 对象
{
  Declaration: {
      color: (declarationNode, helps) => {},
      border: (declarationNode, helps) => {}
  }
}
```

- 遍历到 Comment 对象。依次执行所有插件注册的 Comment 事件监听器，再执行所有插件注册的 CommentExit 事件监听器。

**第二类监听器**

除以特定属性或者规则命名的事件监听器，PostCSS 还有以下四个：

```javascript
{
  postcssPlugin: string,
  prepare: (result) => {},
  Once: (root, helps) => {},
  OnceExit: (root, helps) => {},
}
```

PostCSS 插件事件的整体执行是：`[prepare, Once, ...一类事件，OnceExit]`，postcssPlugin 是插件名称，不是事件监听器。

- postcssPlugin：字符串类型，插件的名字，在插件执行报错，提示用户是哪个插件报错了。
- prepare：函数类型，prepare 是最先执行的，在所有事件执行前执行的，插件多个监听器间共享数据时使用。prepare 的入参是 Result 对象，返回值是监听器对象，通过 Result 对象可以获取 css string、opts 等信息。

```javascript
{
  postcssPlugin: "PLUGIN NAME",
  prepare(result) {
    const variables = {};
    return {
      Declaration(node) {
        if (node.variable) {
          variables[node.prop] = node.value;
        }
      },
      OnceExit() {
        console.log(variables);
      },
    };
  },
};
```

- Once：函数类型，在 prepare 后，一类事件前执行，Once 只会执行一次。

```javascript
{
   Once: (root, helps) => {}
}
```

- OnceExit: 函数类型，在一类事件后执行，OnceExit 只会执行一次。

**插件源码截图**

此时再看市面上流行的基于 postcss 的工具，有没有醍醐灌顶？

| autoprefixer | postcss-import-parser | postcss-modules | postcss-modules |
| :----------- | :-------------------- | :-------------- | :-------------- |
|              |                       |                 |                 |

**插件有哪些？**

基于 postcss 的插件有很多，可查阅：https://github.com/postcss/postcss/blob/main/docs/plugins.md。

### 9.3 第三阶段：generate

generate 的过程依旧是以深度优先的方式遍历 AST 对象，针对不同的实例对象进行字符串的拼接。算法对应源码中位置是：`postcss/lib/stringifier.js`中的`stringify`方法，代码量不大，可自行查看。

## 10.postcss-loader 处理兼容

css3自动加前缀 -webkit

```js
const path = require('path')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader',
            {
              loader:'postcss-loader',
                options:{ // Webpack选项
                    postcssOptions:{ // loader配置选项
                        plugins:[
                            require('autoprefixer')
                        ]
                    }
                }
            }
          
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      }
    ]
  }
}
```

**处理颜色的8进制**

color: #12345678后两位用于指定透明度

`postcss-preset-env`预设就是插件的集合，`postcss-preset-env`已经包含了`autoprefixer`，所以可以只使用`postcss-preset-env`

```js
const path = require('path')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader',
            {
              loader:'postcss-loader',
                options:{ // Webpack选项
                    postcssOptions:{ // loader配置选项
                        plugins:[
                            require('postcss-preset-env')
                        ]
                    }
                }
            }
          
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      }
    ]
  }
}
```

单独使用配置文件配置postcss插件

postcss.config.js

```js
module.exports = {
  plugins: [
    require('postcss-preset-env')
  ]
}
```

## 11.importLoaders 属性

问题：
test.css的内容如下：

```css
.title {
    transition: all .5s;
    user-select: none;
}
```

login.css的内容如下：


/* 导入test.css */

```css
@import './test.css';
.title {
    color: #12345678;
}
```

再次npm run build发现运行之后的test.css里面的代码并没有做兼容性处理。

问题分析：

- login.css @import 语句导入了test.css
- login.css可以被匹配，当它被匹配到之后就是postcss-loader进行工作
- 基于当前的代码，postcss-loader拿到了login.css当中的代码之后分析基于我们的筛选条件并不需要做额外的处理
- 最终就将代码交给了css-loader
- 此时css-loader是可以处理@import media、 url ... ,这个时候它又拿到了test.css文件，但是loader不会回头找
- 最终将处理好的css代码交给style-loader进行展示

解决问题：修改Webpack.config.js给css-loader设置一些属性。

```js
const path = require('path')
module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'build.js',
        //output必须设置绝对路径,所以这里导入path模块
        path: path.resolve(__dirname, 'dist')
    },
    module: {
        rules: [
           
            {
                //简写方式
                test: /\.css$/,
                //先执行style-loader再执行css-loader
                //顺序规则，从右往左，从下往上,因为兼容性处理要在css调用之前，所以需要将postcss-loader的配置放在css-loader右边
                use: ['style-loader', {
                    loader: 'css-loader',
                    options: {
                        // css-loader工作时，遇到css文件时，再往前找一个loader,即追回到postcss-loader
                        importLoaders: 1
                    }
                }, 'postcss-loader']
            },
            {
                //简写方式
                test: /\.less$/,
                //先执行style-loader再执行css-loader
                //顺序规则，从右往左，从下往上
                use: ['style-loader', 'css-loader', 'postcss-loader', 'less-loader']
            }
        ]
    }
}
```

再次运行成功。运行结果如下，test.css的内容也被修改成功。

![](http://5coder.cn/img/1667523998_a40fade5dc9ef7c41562b6bf11dc09b3.png)

## 12.file-loader 处理图片

### 12.1  JS导入图片并写入HTML

在js文件中引入img图片并输出到页面上

要处理jpg、png等格式的图片，我们也需要有对应的loader： file-loader。file-loader的作用就是帮助我们处理**import/require()等方式**引入的一个文件资源，并且会将它放到我们**输出的文件夹中**；当然也可以修改它的名字和所在文件夹

安装`file-loader`

```bash
npm install file-loader -D
```

目录结构：
![](http://5coder.cn/img/1667877331_aabbbe7b7bf3ef5f744a5f1c101dbc9c.png)

Image.js中导入图片并显示在页面上：

```js
import oImgSrc from '../img/01.wb.png'


function packImg() {
  // 01 创建一个容器元素
  const oEle = document.createElement('div')

  // 02 创建 img 标签，设置 src 属性
  const oImg = document.createElement('img')
  oImg.width = 600
  // 写法1：使用require...default取值
  // require导入默认一个对象，有一个default的键，代表的导入的内容
  // oImg.src = require('../img/01.wb.png').default


  // 写法2：lg.Webpack.js配置文件搭配使用，不需要写default取值
  // esModule: false // 不转为 esModule
  // oImg.src = require('../img/01.wb.png')


  // 写法3：使用import导入，不需要写default或者config配置esModule
  oImg.src = oImgSrc
  oEle.appendChild(oImg)

  return oEle
}

document.body.appendChild(packImg())

```

lg.Webpack.js

```js
const path = require('path')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        // use: [
        //   {
        //     loader: 'file-loader',
        //     options: {
        //       esModule: false // 不转为 esModule,在js导入时无需写default取值
        //     }
        //   }
        // ]
        use: ['file-loader']
      }
    ]
  }
}
```

最终效果：

![](http://5coder.cn/img/1667877822_042ac9ef62d22e9a70cd74e7bb6a40ec.png)

### 12.2  JS导入图片并设置到css样式

**css-loader处理时，会默认将`background-image: url('../img/02.react.png')`处理为require的形式，而require会返回一个ESModule，所以需要在Webpack配置中添加css-loader的属性值->`esModule: false`**

```js
{
  test: /\.css$/,
    use: [
      'style-loader',
      {
        loader: 'css-loader',
        options: {
          importLoaders: 1,
          esModule: false
        }
      },
      'postcss-loader'
    ]
},
```

img.css

```css
.bgBox {
  width: 240px;
  height: 310px;
  border: 1px solid #000;
  background-image: url('../img/02.react.png');
}
```

Image.js

```js
import oImgSrc from '../img/01.wb.png'
import '../css/img.css'


function packImg() {
  // 01 创建一个容器元素
  const oEle = document.createElement('div')

  // 02 创建 img 标签，设置 src 属性
  const oImg = document.createElement('img')
  oImg.width = 600
  // 写法1：使用require...default取值
  // require导入默认一个对象，有一个default的键，代表的导入的内容
  // oImg.src = require('../img/01.wb.png').default


  // 写法2：lg.Webpack.js配置文件搭配使用，不需要写default取值
  // esModule: false // 不转为 esModule
  // oImg.src = require('../img/01.wb.png')


  // 写法3：使用import导入，不需要写default或者config配置esModule
  oImg.src = oImgSrc
  oEle.appendChild(oImg)

  // 03 设置背景图片
  const oBgImg = document.createElement('div')
  oBgImg.className = 'bgBox'
  oEle.appendChild(oBgImg)

  return oEle
}

document.body.appendChild(packImg())
```

lg.Webpack.js

```js
const path = require('path')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        // use: [
        //   {
        //     loader: 'file-loader',
        //     options: {
        //       esModule: false // 不转为 esModule
        //     }
        //   }
        // ]
        use: ['file-loader']
      }
    ]
  }
}
```



## 13.设置图片名称与输出

修改file-loader的options用于设置图片名称和输出。

常见占位符：

```txt
[ext]: 扩展名 
[name]: 文件名称 
[hash]: 文件内容+MD4生成128为占位置，作为文件名 
[contentHash]: 文件内容+MD4生成128为占位置，作为文件名 
[hash:<length>]: hash截取，作为文件名
[path]: 文件路径
```

lg.Webpack.js

```js
{
  test: /\.(png|svg|gif|jpe?g)$/,
  use: [
    {
      loader: 'file-loader',
      options: {
        name: 'img/[name].[hash:6].[ext]',
        // outputPath: 'img'
      }
    }
  ]
}
```

其中，目录有两种写法，一种为添加`outputPath: 'img'`，另一种为直接在name处写入`img/`重新打包后，目录如下：

![](http://5coder.cn/img/1667894065_4b9a6a984dd32f12e69b32b2e8ecf450.png)

## 14.url-loader 处理图片

### 14.1 什么是 url-loader

`url-loader` 会将引入的文件进行编码，生成 `DataURL`，相当于把文件翻译成了一串字符串，再把这个字符串打包到 `JavaScript`。

### 14.2 什么时候使用

一般来说，我们会发请求来获取图片或者字体文件。如果图片文件较多时（比如一些 `icon`），会频繁发送请求来回请求多次，这是没有必要的。此时，我们可以考虑将这些较小的图片放在本地，然后使用 `url-loader` 将这些图片通过 `base64` 的方式引入代码中。这样就节省了请求次数，从而提高页面性能。

### 14.3 什么时候使用

一般来说，我们会发请求来获取图片或者字体文件。如果图片文件较多时（比如一些 `icon`），会频繁发送请求来回请求多次，这是没有必要的。此时，我们可以考虑将这些较小的图片放在本地，然后使用 `url-loader` 将这些图片通过 `base64` 的方式引入代码中。这样就节省了请求次数，从而提高页面性能。

### 14.4 如何使用

1. 安装 `url-loader`

```text
npm install url-loader --save-dev
```

2. 配置 `webapck`

```js
module.exports = {
  module: {
    rules: [
      {
        test: /\.(png|jpg|gif)$/,
        use: [
          {
            loader: 'url-loader',
            options: {},
          },
        ],
      },
    ],
  },
};
```

3. 引入一个文件，可以是 `import`（或 `require`）

```js
import logo from '../assets/image/logo.png';
console.log('logo的值: ', logo); // 打印一下看看 logo 是什么
```

简单三步就搞定了。

4. 见证奇迹的时刻

```text
Webpack
```

执行 `Webpack` 之后，`dist` 目录只生成了一个 `bundle.js`。和 `file-loader` 不同的是，没有生成我们引入的那个图片。上文说过，`url-loader` 是将图片转换成一个 `DataURL`，然后打包到 `JavaScript` 代码中。

![](http://5coder.cn/img/1667894853_757a8174372edf3c903391580938c268.png)

那我们就看看 `bundle.js` 是否有我们需要的 `DataURL`：

```js
// bundle.js
(function(module, exports) {
module.exports = "data:image/jpeg;base64.........."; // 省略无数行
})
```

我们可以看到这个模块导出的是一个标准的 `DataURL`。

> 一个标准的DataURL: `data:[<mediatype>][;base64],<data>`

通过这个 `DataURL`，我们就可以从本地加载这张图片了，也就不用将图片文件打包到 `dist` 目录下。

使用 `base64` 来加载图片也是有两面性的：

- 优点：节省请求，提高页面性能
- 缺点：增大本地文件大小，降低加载性能

所以我们得有取舍，只对部分小 `size` 的图片进行 `base64` 编码，其它的大图片还是发请求吧。

`url-loader` 自然是已经做了这个事情，我们只要通过简单配置即可实现上述需求。

### 14.5 options

- limit: 文件阈值，当文件大小大于 `limit` 的时候使用 `fallback` 的 `loader` 来处理文件
- fallback: 指定一个 `loader` 来处理大于 `limit` 的文件，默认值是 `file-loader`

我们来试试设一个 `limit`：

```js
{
  test: /\.(png|jpg|gif)$/,
  use: [
    {
      loader: 'url-loader',
      options: {
        name: 'img/[name].[hash:6].[ext]',
        limit: 25 * 1024  // 25kb
      }
    }
  ]
},
/**
 * 01 url-loader base64 uri 文件当中，减少请求次数
 * 02 file-loader 将资源拷贝至指定的目录，分开请求
 * 03 url-loader 内部其实也可以调用 file-loader
 * 04 limit
 */
```

重新执行 `Webpack`，由于我们引入的 `logo.png` 大于 `1000`，所以使用的是 `file-loader` 来处理这个文件。图片被打包到 `dist` 目录下，并且返回的值是它的地址：

```js
(function(module, exports, __Webpack_require__) {
module.exports = __Webpack_require__.p + "dab1fd6b179f2dd87254d6e0f9f8efab.png";
}),
```

### 14.6 源码解析

`file-loader` 的代码也不多，就直接复制过来通过注释讲解了：

```js
import { getOptions } from 'loader-utils'; // loader 工具包
import validateOptions from 'schema-utils'; // schema 工具包
import mime from 'mime';

import normalizeFallback from './utils/normalizeFallback'; // fallback loader
import schema from './options.json'; // options schema

// 定义一个是否转换的函数
/*
 *@method shouldTransform
 *@param {Number|Boolean|String} limit 文件大小阈值
 *@param {Number} size 文件实际大小
 *@return {Boolean} 是否需要转换
*/
function shouldTransform(limit, size) {
  if (typeof limit === 'boolean') {
    return limit;
  }

  if (typeof limit === 'number' || typeof limit === 'string') {
    return size <= parseInt(limit, 10);
  }

  return true;
}

export default function loader(src) {
  // 获取 Webpack 配置里的 options
  const options = getOptions(this) || {};

  // 校验 options
  validateOptions(schema, options, {
    name: 'URL Loader',
    baseDataPath: 'options',
  });

  // 判断是否要转换，如果要就进入，不要就往下走
  // src 是一个 Buffer，所以可以通过 src.length 获取大小
  if (shouldTransform(options.limit, src.length)) {
    const file = this.resourcePath;
    // 获取文件MIME类型，默认值是从文件取，比如 "image/jpeg"
    const mimetype = options.mimetype || mime.getType(file);

    // 如果 src 不是 Buffer，就变成 Buffer
    if (typeof src === 'string') {
      src = Buffer.from(src);
    }

    // 构造 DataURL 并导出
    return `module.exports = ${JSON.stringify(
      `data:${mimetype || ''};base64,${src.toString('base64')}`
    )}`;
  }

  // 判断结果是不需要通过 url-loader 转换成 DataURL，则使用 fallback 的 loader
  const {
    loader: fallbackLoader,
    options: fallbackOptions,
  } = normalizeFallback(options.fallback, options);

  // 引入 fallback loader
  const fallback = require(fallbackLoader);

  // fallback loader 执行环境
  const fallbackLoaderContext = Object.assign({}, this, {
    query: fallbackOptions,
  });

  // 执行 fallback loader 来处理 src
  return fallback.call(fallbackLoaderContext, src);
}

// 默认情况下 Webpack 对文件进行 UTF8 编码，当 loader 需要处理二进制数据的时候，需要设置 raw 为 true
export const raw = true;
```

## 15.asset 处理图片

在 `Webpack` 出现之前，前端开发人员会使用 `grunt` 和 `gulp` 等工具来处理资源，并
将它们从 `/src` 文件夹移动到 `/dist` 或 `/build` 目录中。`Webpack` 最出色的功能之一就是，除了引入 `JavaScript`，还可以内置的资源模块 `Asset Modules` 引入任何其他类型的文件。

在`Webpack4`的时候以及之前，我们通常是使用`file-loader`与`url-loader`来帮助我们加载其他资源类型。

### 15.1 Asset Modules Type的四种类型

而Webpack5可以使用资源模块来帮助我们，称之为`Asset Modules`，它允许我们打包其他资源类型，比如`字体文件、图表文件、图片文件`等。

其中，资源模块类型我们称之为`Asset Modules Type`，总共有四种，来代替`loader`，分别是：

1. `asset/resource`：发送一个单独的文件并导出URL，替代`file-loader`
2. `asset/inline`：导出一个资源的`data URI`，替代`url-loader`
3. `asset/source`：导出资源的源代码，之前通过使用`raw-loader`实现
4. `asset`：介于`asset/resource`和`asset/inline`之间，在导出一个资源`data URI`和发送一个单独的文件并导出`URL`之间做选择，之前通过`url-loader+limit`属性实现。

不过在介绍这四种资源模块类型之前，我们先说一下怎么自定义这些输出的资源模块的文件名

### 15.2 自定义资源模块名称

#### 15.2.1 assetModuleFilename

第一种方式，就是在 `Webpack` 配置中设置 `output.assetModuleFilename` 来修改此模板字符串，其中assetModuleFilename默认会处理文件名后缀的点，所以无需手动添加点。此方式为公共的处理方法，当需要同时处理图片资源和字体资源时，通用方法会导致两种资源类型放在同一个目录下，此处不建议使用assetModuleFilename。

![](http://5coder.cn/img/1667910431_9394e5b6598baec3968fc661d681ae8a.png)

比如关于图片的输出文件名，我们可以让其都输出在`images`文件夹下面，`[contenthash]`表示文件名称，`[ext]`表示图片文件的后缀，比如.png、.jpg、.gif、jpeg等，`[query]`表可能存在的参数

```js
output: {
   ···
   assetModuleFilename: 'images/[contenthash][ext][query]' 
   ···
},
```

#### 15.2.2 geneator属性

第二种方式，就是在module.rules里面某种资源文件配置的时候，加上`geneator`属性，例如

```js
rules: [
	{ 
		test: /\.png/, 
		type: 'asset/resource', 
		generator: { 
	      	filename: 'images/[contenthash][ext][query]' 
	 	} 
	}
]
```

【注意】
**`generator 的优先级高于 assetModuleFilename`**

### 15.3 四种类型的导入

首先我们先新建一个文件夹来测试，文件夹目录如下，我们在src下面新建一个assets文件夹，里面放上事先准备好的集中不同类型的图片

![](http://5coder.cn/img/1667898776_d606595b7674189ce5502f5f433e0e3a.png)

index.js

```js
import hello from './hello'
import img1 from './assets/man.jpeg'
import img2 from './assets/store.svg'
import img3 from './assets/women.jpg'
import Txt from './assets/wenzi.txt'
import dynamic from './assets/dongtu.gif'
hello()

const IMG1 = document.createElement('img')
IMG1.src = img1
document.body.appendChild(IMG1)

const IMG2 = document.createElement('img')
IMG2.src = img2
IMG2.style.cssText = 'width:200px;height:200px'
document.body.appendChild(IMG2)

const IMG3 = document.createElement('img')
IMG3.src = img3
document.body.appendChild(IMG3)

const TXT = document.createElement('div')
TXT.textContent = Txt
TXT.style.cssText = 'width:200px;height:200px;backGround:aliceblue'
document.body.appendChild(TXT)

const DYNAMIC = document.createElement('img')
DYNAMIC.src = dynamic
document.body.appendChild(DYNAMIC)
```

hello.js

```js
function hello(){
    console.log("hello-world!!!")
}

export default hello

```

index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>你是,永远的神</title>
</head>
<body>
</body>
</html>

```

Webpack.config.js

```js
const path = require('path')
const HtmlWebpackPlugin = require('html-Webpack-plugin')

module.exports = {
    entry : './src/index.js',

    output : {
        filename:'bundle.js',
        path:path.resolve(__dirname,'./dist'),
        clean:true,
        //如果不设置，打包完之后资源会直接打包在dist目录下
        assetModuleFilename:'images/[contenthash][ext][query]'
    },

    mode : 'development',

    devtool:'inline-source-map',

    plugins:[
        new HtmlWebpackPlugin({
            template:'./index.html',
            filename:'app.html',
            inject:"body"
        })
    ],

    devServer:{
        static:'./dist'
    },

    module:{
        rules:[{
            test:/\.jpeg$/,
            type:"asset/resource",
            generator:{
               filename:'images/[contenthash][ext][query]'
            }
        },{
            test:/\.svg$/,
            type:'asset/inline'
        },{
            test:/\.txt$/,
            type:'asset/source'
        },{
            test:/\.(gif|jpg)$/,
            type:'asset',
            parser:{
                dataUrlCondition:{
                    maxSize : 10 * 1024 * 1024
                }
            }
        }]
    }
    
}
```

#### 15.3.1 resource 资源类型

`asset/resource`可以发送一个单独的文件并导出URL

我们将`.jpeg`后缀的图片设置`type`为`asset/resource`，我们在`index.js`里面导入该图片并插入在body中，即将其当成资源显示在页面上

`npx Webpack`打包之后，dist文件夹下的images文件中就出现该图片

![](http://5coder.cn/img/1667898899_5df0787e6c6834ba806c78a6443c83bf.png)

`npx Webpack-dev-server --open``自动打开浏览器，我们在控制台中查看该图片类型，发现``asset/resource``类型确实可以`导出一个文件`和其`URL路径



![](http://5coder.cn/img/1667898939_7adc65d4fe392fb78bb718f039bd9085.png)

#### 15.3.2 inline资源类型

`asset/inline`导出一个资源的`data URI`

仿照上面的方式，我们将`.svg`后缀的图片设置type为`asset/inline`，我们在`index.js`里面导入该图片并插入在body中，即将其当成资源显示在页面上，同时我们简单设置一下样式

不过不同的是，`npx Webpack`打包之后，dist文件夹下面并没有打包过`.svg`类型的图片

`npx Webpack-dev-server --open``自动打开浏览器，我们在控制台中查看该图片类型，发现`asset/inline`类型确实可以`导出Data URI形式的路径`

![](http://5coder.cn/img/1667899086_6db380698c5f300aa8f603a96259c3ef.png)

#### 15.3.3 source资源类型

`source`资源，导出资源的源代码

仿照上面的方式，我们创建一个`.txt`后缀的文本文件，设置type为`asset/source`，我们在`index.js`里面导入该文本并插入在body中，即将其当成资源显示在页面上，同时我们简单设置一下样式

不过不同的是，`npx Webpack`打包之后，dist文件夹下面并没有打包过`.txt`类型的文本文件

`npx Webpack-dev-server --open`自动打开浏览器，我们在控制台中查看该文本类型，发现`asset/source`类型确实可以`导出资源的源代码`

![](http://5coder.cn/img/1667899189_d9d22dc526187d10484207e0b38c1266.png)

#### 15.3.4 asset通用资源类型

`asset`会介于`asset/resource`和`asset/inline`之间，在`发送一个单独的文件并导出URL`和 `导出一个资源data URI`之间做选择

默认情况下，Webpack5会以`8k`为界限来判断：

- 当资源大于8k时，自动按`asset/resource`来判断
- 当资源小于8k时，自动按`asset/inline`来判断

我们可以手动更改临界值，设置`parser（解析）`，其是个对象，里面有个固定的属性，叫`dataUrlCondition`，顾名思义，data转成url的条件，也就是转成bas64的条件，`maxSize`是就相当于Limit了

```js
module:{
        rules:[
        ···
        {
            test:/\.(gif|jpg)$/,
            type:'asset',
            parser:{
                dataUrlCondition:{
                    maxSize : 100 * 1024 
                }
            }
        }
        ···
        ]
    }
```

这里我们设置100 * 1024即100kb，来作为临界值
`【1b * 1024 = 1kb，1kb * 1024 = 1M】`

仿照上面的方式，我们将`.gif`和`.jpg`后缀的图片设置type为`asset`资源类型，我们在`index.js`里面导入2张图片并插入在body中，即将其当成资源显示在页面上，其中`.gif`大小为128.11kb（超过了100kb的临界值），`.jpg`大小为12kb（未超过100kb的临界值）

`npx Webpack`打包之后，dist文件夹下面有打包过的`.gif`类型的图片，但是没有打包过`.jpg`类型的图片

`npx Webpack-dev-server --open`自动打开浏览器，我们在控制台中查看2种图片类型，发现`.gif`图片是单独一个文件的URL路径，而`.jpg`图片是Data URI格式的base64路径

![](http://5coder.cn/img/1667899418_6168a6a4282b474fe1aaea7627e36b46.png)

## 16.asset处理图标字体

同上面所说，处理字体图标文件时，需要将其视为`resource`资源直接复制，所以需要使用`asset/resource`。此时准备好的字体文件及其目录如下：

![](http://5coder.cn/img/1667912567_615bc7ed1f6fdaa5eb09f02bc8918739.png)

在`font`目录中，准备了`iconfont.css`及其字体文件，其中`iconfont.css`中对`font-family`进行赋值对应的字体。

单独常见`font.js`文件，并在文件中引入`iconfont.css`以及自定义的`index.css`文件，创建页面`DOM`元素并显示。

iconfont.css

```css
@font-face {
  font-family: "iconfont"; /* Project id 2250626 */
  src: url('iconfont.woff2?t=1628066777598') format('woff2'),
       url('iconfont.woff?t=1628066777598') format('woff'),
       url('iconfont.ttf?t=1628066777598') format('truetype');
}

.iconfont {
  font-family: "iconfont" !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.icon-linggan:before {
  content: "\e602";
}

.icon-publish:before {
  content: "\e635";
}

.icon-image:before {
  content: "\e629";
}


```

index.css

```css
.lg-icon {
  color: red;
  font-size: 50px;
}
```

Font.js

```js
import '../font/iconfont.css'
import '../css/index.css'

function packFont() {
  const oEle = document.createElement('div')

  const oSpan = document.createElement('span')
  oSpan.className = 'iconfont icon-linggan lg-icon'
  oEle.appendChild(oSpan)

  return oEle
}

document.body.appendChild(packFont())
```

当然，此时直接运行`yarn build`肯定会报错，因为此时`Webpack`不认识`ttf/woff/woff2`等资源，所以需要单独使用`asset/resouce`进行打包配置。

lg.Webpack.js

```js
const path = require('path')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
    // assetModuleFilename: "img/[name].[hash:4][ext]"
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',  // 使用资源复制
        generator: {
          filename: 'font/[name].[hash:3][ext]'  // 指定字体文件输出路径
        }
      }
    ]
  }
}

```

此时执行`yarn build`，我们发现在dist目录下新增了font目录，font目录中的字体文件为Webpack拷贝而来。打开页面可以看到iconfont.css以及自定义的index.css文件样式已经生效。

![](http://5coder.cn/img/1667913036_9f76982be902d51c5e6be32d1a6fccfa.png)

## 17.Webpack 插件使用

插件机制是Webpack当中另外一个核心特性‌‌，它目的是为了增强Webpack项目自动化方面的能力‌‌，loader就是负责实现各种各样的资源模块的加载‌‌，从而实现整体项目打包‌‌，plugin则是用来去解决项目中除了资源以外，其它的一些自动化工作‌，例如：

- plugin可以帮我们去实现自动在打包之前去清除dist目录‌‌，也就是上一次打包的结果‌‌；
- 又或是它可以用来去帮我们拷贝那些不需要参与打包的资源文件到输出目录‌‌；
- 又或是它可以用来去帮我们压缩我们打包结果输出的代码‌‌。

总之‌‌，有了plugin的Webpack，几乎无所不能的实现了前端工程化当中绝大多数经常用到的部分‌‌，这也正是很多初学者会有Webpack就是前端工程化的这种理解的原因‌‌。

`clean-Webpack-plugin`：自动清空dist目录

之前的测试中，每次都需要用户手动的删除dist目录，我们希望Webpack每次打包时，先将之前的dist目录删除，再进行打包，这里使用`clean-Webpack-plugin`进行处理。

同样的，需要先进行安装`clean-Webpack-plugin`

```bash
yarn add clean-Webpack-plugin -D
```

之后按照其使用方法，在lg.Webpack.js中进行插件配置。首先使用`require`导入`clean-Webpack-plugin`，其中导出东西过多，需要进行解构：`const { CleanWebpackPlugin } = require('clean-Webpack-plugin')`。其次每个导出对象都是一个类，都有其自己的构造函数`constructor`，在plugins中使用时需要`new CleanWebpackPlugin`。代码如下：

```js
const path = require('path')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
    // assetModuleFilename: "img/[name].[hash:4][ext]"
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {
          filename: 'font/[name].[hash:3][ext]'
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin()  // 每个插件就是一个类
  ]
}
```

先使用`yarn build`进行打包，生成`dist`目录，随后在`dist`目录中手动添加一个`a.txt`文件，如果再次执行`yarn build`后`a.txt`被删除了，说明`clean-Webpack-plugin`已经正常工作了。

## 18.html-webapck-plugin 使用

除了清理dist的目录以外，‌‌还有一个非常常见的需求就是自动去生成使用打包结果的HTML，在这之前HTML‌‌都是通过硬编码的方式单独去存放在项目根目录下的。‌‌

`index.html`每次打包完成之后手动需要修改`title`，以及打包产生的文件由于分包过后文件类型或者数量比较多，需要用户手动的进行修改，这些行为都可以通过`html-Webpack-plugin`进行处理

默认情况下，**不需要手动创建index.html文件**，`Webpack`在使用`html-Webpack-plugin`插件后会默认在打包结果`dist`目录自动创建`index.html`文件。

首先手动删除准备好的`index.html`，没有使用`html-Webpack-plugin`插件时，执行`yarn build`进行打包，通过观察发现`dist`目录中并没有生成`index.html`文件。

![](http://5coder.cn/img/1667914785_8d45e0e8120d5e0dc3edf14f8b3759f6.png)![](http://5coder.cn/img/1667914858_ff92b990b60bdedc40962aa84176a90e.png)

### 18.1 使用默认index.html模板

在配置文件中，首先导入html-Webpack-plugin。

`const HtmlWebpackPlugin = require('html-Webpack-plugin')`

在plugins字段中进行使用：

```js
const HtmlWebpackPlugin = require('html-Webpack-plugin')
...
plugins: [
  new HtmlWebpackPlugin()
]
...
```

此时进行yarn build打包处理，可以发现dist目录中已经有了index.html文件。

![](http://5coder.cn/img/1667915057_650596a463dae3f02e60811981b2bdb8.png)

此时`index.html`内容是`html-Webpack-plugin`默认提供的，可以在`node_modules`中找到`html-Webpack-plugin`中的`default_index.ejs`查看。

![](http://5coder.cn/img/1667915174_fabdac71f6146e0a8cf9243e301e19e1.png)

### 18.2 使用自定义index.html模板

其中默认模板中的占位符在[官方文档](https://www.npmjs.com/package/html-Webpack-plugin)中有详细描述。

| Name                     | Type                            | Default                                                      | Description                                                  |
| ------------------------ | ------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **`title`**              | `{String}`                      | `Webpack App`                                                | The title to use for the generated HTML document             |
| **`filename`**           | `{String|Function}`             | `'index.html'`                                               | The file to write the HTML to. Defaults to `index.html`. You can specify a subdirectory here too (eg: `assets/admin.html`). The `[name]` placeholder will be replaced with the entry name. Can also be a function e.g. `(entryName) => entryName + '.html'`. |
| **`template`**           | `{String}`                      | ``                                                    | `Webpack` relative or absolute path to the template. By default it will use `src/index.ejs` if it exists. Please see the [docs](https://github.com/jantimon/html-Webpack-plugin/blob/master/docs/template-option.md) for details |                                                              |
| **`templateContent`**    | `{string|Function|false}`       | false                                                        | Can be used instead of `template` to provide an inline template - please read the [Writing Your Own Templates](https://github.com/jantimon/html-Webpack-plugin#writing-your-own-templates) section |
| **`templateParameters`** | `{Boolean|Object|Function}`     | `false`                                                      | Allows to overwrite the parameters used in the template - see [example](https://github.com/jantimon/html-Webpack-plugin/tree/master/examples/template-parameters) |
| **`inject`**             | `{Boolean|String}`              | `true`                                                       | `true || 'head' || 'body' || false` Inject all assets into the given `template` or `templateContent`. When passing `'body'` all javascript resources will be placed at the bottom of the body element. `'head'` will place the scripts in the head element. Passing `true` will add it to the head/body depending on the `scriptLoading` option. Passing `false` will disable automatic injections. - see the [inject:false example](https://github.com/jantimon/html-Webpack-plugin/tree/master/examples/custom-insertion-position) |
| **`publicPath`**         | `{String|'auto'}`               | `'auto'`                                                     | The publicPath used for script and link tags                 |
| **`scriptLoading`**      | `{'blocking'|'defer'|'module'}` | `'defer'`                                                    | Modern browsers support non blocking javascript loading (`'defer'`) to improve the page startup performance. Setting to `'module'` adds attribute [`type="module"`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#applying_the_module_to_your_html). This also implies "defer", since modules are automatically deferred. |
| **`favicon`**            | `{String}`                      | ``                                                           | Adds the given favicon path to the output HTML               |
| **`meta`**               | `{Object}`                      | `{}`                                                         | Allows to inject `meta`-tags. E.g. `meta: {viewport: 'width=device-width, initial-scale=1, shrink-to-fit=no'}` |
| **`base`**               | `{Object|String|false}`         | `false`                                                      | Inject a [`base`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/base) tag. E.g. `base: "https://example.com/path/page.html` |
| **`minify`**             | `{Boolean|Object}`              | `true` if `mode` is `'production'`, otherwise `false`        | Controls if and in what ways the output should be minified. See [minification](https://www.npmjs.com/package/html-Webpack-plugin#minification) below for more details. |
| **`hash`**               | `{Boolean}`                     | `false`                                                      | If `true` then append a unique `Webpack` compilation hash to all included scripts and CSS files. This is useful for cache busting |
| **`cache`**              | `{Boolean}`                     | `true`                                                       | Emit the file only if it was changed                         |
| **`showErrors`**         | `{Boolean}`                     | `true`                                                       | Errors details will be written into the HTML page            |
| **`chunks`**             | `{?}`                           | `?`                                                          | Allows you to add only some chunks (e.g only the unit-test chunk) |
| **`chunksSortMode`**     | `{String|Function}`             | `auto`                                                       | Allows to control how chunks should be sorted before they are included to the HTML. Allowed values are `'none' | 'auto' | 'manual' | {Function}` |
| **`excludeChunks`**      | `{Array.<string>}`              | ``                                                           | Allows you to skip some chunks (e.g don't add the unit-test chunk) |
| **`xhtml`**              | `{Boolean}`                     | `false`                                                      | If `true` render the `link` tags as self-closing (XHTML compliant) |

![](http://5coder.cn/img/1667915415_704784ee69f5f9963d59803a0654d2a0.png)

对于占位符，我们可以在plugin中进行传参，赋予其默认值。

```js
new HtmlWebpackPlugin({
  title: 'html-Webpack-plugin',  // title占位符
})
```

```js
const path = require('path')
const { DefinePlugin } = require('Webpack')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
    // assetModuleFilename: "img/[name].[hash:4][ext]"
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {
          filename: 'font/[name].[hash:3][ext]'
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'html-Webpack-plugin',  // title占位符
    })
  ]
}

```

再次`yarn build`进行打包后，`index.html`的`title`已经更新了。

![](http://5coder.cn/img/1667915567_3ee1db61989a64a973f455dd2737c232.png)

此时我们使用的是html-Webpack-plugin内置的html模板文件。但是在实际使用过程中，我们可能需要使用特殊的模板文件。此时使用`template`字段去定义自己的index.html模板。

```js
new HtmlWebpackPlugin({
  title: 'html-Webpack-plugin',
  template: './public/index.html'
}),
```

![](http://5coder.cn/img/1667915917_7b522c7f1cb8a09b5f8cd99d0737cd66.png)

此时使用`yarn build`打包后，就会使用自定义的`index.html`模板文件。

![](http://5coder.cn/img/1667916002_f8ee2c8686f67178183532bc854975bd.png)

此时，网站图标的路径使用`<link rel="icon" href="<%= BASE_URL %>favicon.ico">`，再使用`DefinePlugin`（Webpack默认，无需安装）进行定义全局配置的常量。

```js
new DefinePlugin({
	BASE_URL: '"./"'
})
```

此时，完整的配置文件如下：

```js
const path = require('path')
const { DefinePlugin } = require('Webpack')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
    // assetModuleFilename: "img/[name].[hash:4][ext]"
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {
          filename: 'font/[name].[hash:3][ext]'
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'html-Webpack-plugin',
      template: './public/index.html'
    }),
    new DefinePlugin({
      BASE_URL: '"./"'  // Webpack会将常量原封不动的拿走，所以需要使用引号包裹
    })
  ]
}
```

再次进行打包后，结果如下：

![](http://5coder.cn/img/1667916420_f344a9bd9dd0b61dbbede8ea828a5f33.png)

除了自定义输出文件的内容，同时输出多个页面文件也是一个非常常见的需求。其实配置非常简单，配置文件中添加一个新的HtmlWebpackPlugin对象，配置如下：

```js
  plugins: [
    new CleanWebpackPlugin(),
    // 用于生成 index.html
    new HtmlWebpackPlugin({
      title: 'Webpack Plugin Sample',
      meta: {
        viewport: 'width=device-width'
      },
      template: './src/index.html'
    }),
    // 用于生成 about.html
    new HtmlWebpackPlugin({
      filename: 'about.html',  // 用于指定生成的文件名称，默认值是index.html
      title: 'About html'
    })
  ]
```

## 19.copy-Webpack-plugin

在项目中，一般还有一些不需要参与构建的静态文件，‌‌它们最终也需要发布到线上，‌‌例如我们网站的`favicon.icon`，‌‌一般会把这一类的文件统一放在项目的`public`目录当中，‌‌希望`Webpack`在打包时，可以一并将它们复制到输出目录。

‌‌对于这种需求，可以借助于`copy-Webpack-plugin`，‌‌先安装一下这个插件‌‌，然后再去导入这个插件的类型，‌‌最后同样在这个`plugin`属性当中去添加一个这个类型的实例，‌‌这类型的构造函数它要求传入一个数组，‌‌用于去指定需要去拷贝的文件路径，它可以是一个通配符，也可以是一个目录或者是文件的相对路径，‌‌这里使用plugin，‌‌它表示在打包时会将所有的文件全部拷贝到输出目录，‌‌再次运行Webpack指令，‌‌打包完成过后，public目录下所有的文件就会同时拷贝到输出目录。

```js
const path = require('path')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')
const CopyWebpackPlugin = require('copy-Webpack-plugin')

module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.join(__dirname, 'dist'),
    // publicPath: 'dist/'
  },
  module: {
    rules: [
      {
        test: /.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /.png$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10 * 1024 // 10 KB
          }
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    // 用于生成 index.html
    new HtmlWebpackPlugin({
      title: 'Webpack Plugin Sample',
      meta: {
        viewport: 'width=device-width'
      },
      template: './src/index.html'
    }),
    // 用于生成 about.html
    new HtmlWebpackPlugin({
      filename: 'about.html'
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'public',
          globOptions: {
            ignore: ['**/index.html']  // 必须写入**/, ** 两个星号的意思是在当前路径
          }
        }
      ]
    })
  ]
}

```

## 20.babel 使用

由于`Webpack`默认就能处理代码当中的`import`和`export`，‌‌所以很自然都会有人认为`Webpack`会自动编译的`ES6`代码。实则不然，‌‌那是`Webpack`的仅仅是对模块去完成打包工作，‌‌所以说它才会对代码当中的`import`和`export`做一些相应的转换，‌‌它并不能去转换我们代码当中其它的`ES6`特性。

如果需要将`ES6`的代码打包并编译为`ES5`的代码，需要一些其它的编译形加载器。这里安装一些额外的插件。

首先，`Webpack`是可以识别`ES6+`的语法的，这里来测试一下，在`index.js`中写入`ES6+`的语法，使用`yarn build`进行打包，观察打包过后的代码可以发现，`Webpack`原封不动的把`index.js`中的`ES6+`语法代码拿了过来，并没有进行任何处理。

![](http://5coder.cn/img/1667947261_ee8f7219f4b7bf9dca9e203d4f4027bb.png)

![](http://5coder.cn/img/1667947238_251f12837e5e7523db1342b57f63cb46.png)

所以针对ES6+语法，需要使用特殊工具进行处理，这里安装`@babel/core`以及命令行工具`@babel/cli`进行代码测试，看babel默认是否会帮助处理ES6+语法。

```bash
yarn add @babel/core @babel/cli
yarn babel 
```

使用后发现，babel仍然没有帮我们处理ES6+语法，这是为什么呢？原因是babel还需要使用特殊插件进行处理。

yarn babel 目标路径 --out-put 输出路径

```bash
yarn babel src --out-put build
```

![](http://5coder.cn/img/1667947490_5c2c7717e68d8c26a65293437efc76f5.png)

因此，我们需要特殊的插件来对箭头函数或者const、let关键字进行处理。

- `@babel/plugin-transform-arrow-functions`（处理箭头函数）
- `@babel/plugin-transform-block-scoping`（处理块级作用域）

```bash
yarn add @babel/plugin-transform-arrow-functions @babel/plugin-transform-block-scoping
# 执行babel
yarn babel src --out-dir build --plugins=@babel/plugin-transform-arrow-functions,@babel/plugin-transform-block-scoping
```

重新执行后，发现箭头函数和`let、const`关键字作用域已经被处理成`var`关键字。

![image-20221109082655277](http://5coder.cn/img/1667953615_535e5755aa4aa4cb7eb2c5d4cefec5e4.png)

但是我们发现，每次需要处理不同的特殊情况，都需要安装不同的`babel`插件，特别不方便。因此`babel`将绝大多数有关`ES6+`语法以及`stage`草案的插件组合成一个集合`@babel/preset-env`,以后只需要使用这一个集合就可以处理绝大多数的`ES6+`语法。

```bash
# 安装@babel/preset-env
yarn add @babel/preset-env
# 使用babel进行编译
yarn babel src --out-dir build --presets=@babel/preset-env
```

![](http://5coder.cn/img/1667953874_6dc93182a1639912e914389f540c6e32.png)

## 21.babel-loader 使用

使用`babel-loader`对`js`文件进行处理，在`lg.Webpack.js`配置文件中配置js文件规则。

**使用单独的插件进行转换**

![](http://5coder.cn/img/1667954191_25e5f00880922a2fb42ebc2fab6fdf41.png)

**使用预设进行转换**

使用babel.config.js配置文件进行babel配置

![](http://5coder.cn/img/1667954271_b6136550e30bb4e3b0d9e3b19e2cdce4.png)

```js
const path = require('path')
const CopyWebpackPlugin = require('copy-Webpack-plugin')
const { DefinePlugin } = require('Webpack')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  output: {
    filename: 'js/main.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {
          filename: 'font/[name].[hash:3][ext]'
        }
      },
      {
        test: /\.js$/,
        use: ['babel-loader']
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'copyWebpackPlugin',
      template: './public/index.html'
    }),
    new DefinePlugin({
      BASE_URL: '"./"'
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'public',
          globOptions: {
            ignore: ['**/index.html']
          }
        }
      ]
    })
  ]
}

```

> 对于是否转换ES6+语法，此处还需要看`.browserslistrc`文件的配置，如果在`.browserslistrc`只配置了如：`chrome 91`，由于`chrome 91`版本已经支持`const`以及`箭头函数`，所以此时`babel`并不会对`箭头函数`及`块级作用域`进行转换。
>
> 如果有`.browserslistrc`文件配置，还有`presets targets`配置，`babel`会优先以`targets`为主。
>
> `presets targets`配置
>
> ![](http://5coder.cn/img/1667954688_2dad09a585dc4355b8803b123aeeda12.png)

## 22.polyfill 配置

**`Webpack4`时不需要进行单独的`polyfill`处理，因为`Webpack4`默认已经加入的`polyfill`，但是正因为默认加入了`polyfill`，导致打包后的产出内容特别大。到了`Webpack5`之后，基于优化打包速度的考虑，默认情况下，`polyfill`就被移除掉了。如果需要用到，就需要自己进行安装配置。**

**什么是polyfill**

> `Polyfill` 是一块代码（通常是 Web 上的 JavaScript），用来为旧浏览器提供它没有原生支持的较新的功能。

**为什么使用polyfill**

首先在index.js中写入ES6新增的promise语法，然后执行打包，查看打包结果。

![](http://5coder.cn/img/1667974119_77cf12b719deca37f02b0f4be2926f9b.png)

可以发现，打包过后的`main.js`中保留了`Promise`。但是有个问题，如果直接把`main.js`放入浏览器中运行，例如`.browserslistrc`中包含了IE7、IE8、IE9等低版本浏览器，那些不支持`Promise`的浏览器就会报错。所以想要的是希望打包时，`Webpack`可以帮助我们定义一个`Promise`函数，用于支持低版本的浏览器。所以这时候，就需要一个`Polyfill`的存在，处理`babel-preset-env`不能处理的更新的语法（`generator、symbol、promise`等），以适配低版本浏览器。

更早的时候会使用`@babel/polyfill`，根据安装提示，查看官方文档。目前已经不建议直接安装`@babel/polyfill`，建议使用`core-js/stable`以及`regenerator-runtime/runtime`。

![](http://5coder.cn/img/1667974614_6f424794992b1ac4c3af2f66bdbcc2ac.png)

所以卸载`@babel/polyfill`，重新安装`core-js/stable`和`regenerator-runtime/runtime`

```bash
yarn add core-js regenerator-runtime
```

接下来配置`babel-loader`，之前我们的`babel-loader`放到了单独的配置文件`babel.config.js`中。

index.js导入`core-js/stable`、`regenerator-runtime/runtime`

```js
import "core-js/stable";
import "regenerator-runtime/runtime"

const title = '前端'
const foo = () => {
  console.log(title)
}

const p1 = new Promise((resolve, reject) => {
  console.log(111)
})
console.log(p1)

foo()
```

babel-config.js

```js
module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        // false: 不对当前的JS处理做 polyfill 的填充
        // usage: 依据用户源代码当中所使用到的新语法进行填充
        // entry: 依据我们当前筛选出来的浏览器.browserslistrc决定填充什么
        useBuiltIns: 'usage',
        corejs: 3
      }
    ]
  ]
}
```

![](http://5coder.cn/img/1667977622_cbb3f3d54082c955ce3622f3e2c5f998.png)

## 23.Webpack-dev-server 初始

在前端开发过程中，我们希望在一个项目的里程碑的时候对一些功能进行测试或者调试，在手动修改js代码后，希望Webpack重新打包，并自动刷新浏览器操作。之前可以使用--watch的模式进行监听。--watch有两种使用方法，第一种是package.json的scripts中添加命令行参数：

```js
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "Webpack --config lg.Webpack.js --watch",
  },
```

第二种是在lg.Webpack.js中添加watch字段，并赋值为true（默认为false）

![](http://5coder.cn/img/1667978251_880f07ce27fa56829f244eea35b04912.png)

watch和live server的不足：

* 一个文件改动，所有源代码都会重新编译，耗时长
* 每次编译成功后都需要进行文件读写（dist目录）
* live server是node生态下的
* 模块化开发过程中，一个页面的由多个组件组成，我们希望一个组件改动后，只针对该部分组件进行刷新，而不是整个页面都刷新

Webpack Dev Server是Webpack官方推出的一个开发工具，根据名字，就应该知道它提供了一个开发服务器，并且，它将自动编译和自动刷新浏览器等一系列对开发非常友好的功能全部集成在了一起。这个工具可以直接解决我们之前的问题。

打开命令行，以开发依赖安装

```bash
yarn add Webpack-dev-server --dev
```

它提供了一个Webpack-dev-server的cli程序，那我们同样可以直接通过yarn去运行这个cli，或者，可以把它定义到npm script中。运行这个命令 **yarn Webpack-dev-server**，它内部会自动去使用Webpack去打包应用，并且会启动一个HTTP server去运行打包结果。在运行过后，它还会去监听我们的代码变化，一旦语言文件发生变化，它就会自动立即重新打包，这一点，与watch模式是一样的。不过这里也需要注意Webpack-dev-serverr为了提高工作效率，**它并没有将打包结果写入到磁盘当中**，它是将打包结果，暂时存放在内存当中，而内部的HTTP server从内存当中把这些文件读出来，然后发送给浏览器。这样一来的话它就会减少很多不必要的磁盘读写操作，从而大大提高我们的构建效率。

这里，我们还可以为这个命令传入一个**–open**的参数，它可以用于去自动唤起浏览器，去打开我们的运行地址，打开浏览器过后（如果说你有两块屏幕的话），你就可以把浏览器放到另外一块屏幕当中，然后，我们去体验这种一边编码，一边即时预览的开发环境了。

```shell
yarn Webpack-dev-server --open
```

在package.json中配置server命令：

![](http://5coder.cn/img/1667978583_a0c20a388cbae967fdce6e6f84c9f8c3.png)

运行`yarn serve`，这时动态的更改`index.js`，发现浏览器会自动刷新并打印。

![](http://5coder.cn/img/1667979164_83af7b9da42d731acd6d59d37d879e67.png)

![](http://5coder.cn/img/1667978925_01825062418cb4b1949c80e2e4fdfaf1.png)

> 当当前端口8080被占用时，我们需要手动指定端口进行启动服务，命令如下：`"serve": "Webpack serve --config lg.Webpack.js --port 3000"`

## 24.Webpack-dev-middleware 使用

`Webpack-dev-middleware` 是一个容器(wrapper)，它可以把 Webpack 处理后的文件传递给一个服务器(server)。 `Webpack-dev-server` 在内部使用了它，同时，它也可以作为一个单独的包来使用，以便进行更多自定义设置来实现更多的需求。

首先需要明确，在实际开发阶段很少使用`Webpack-dev-middleware`，但是我们需要理解这样做的目的是什么，可以对打包过程做一个自由度非常高的定制。具体实现思路是：

1. 在本地利用express开启一个服务
2. 将Webpack打包的结果交给这个服务
3. 浏览器进行访问

具体实施步骤：

安装`express`和`Webpack-dev-middleware`

```bash
yarn add express Webpack-dev-middleware
```

利用`express`自己实现一个server

Server.js

```js
const express = require('express')
const WebpackDevMiddleware = require('Webpack-dev-middleware')
const Webpack = require('Webpack')

const app = express()

// 获取Webpack打包的配置文件
const config = require('./Webpack.config')
const compiler = Webpack(config)

app.use(WebpackDevMiddleware(compiler))

// 开启端口上的服务
app.listen(3000, () => {
  console.log('Server 运行在3000端口上')
})
```

使用`node ./Server.js`启动之后，使用浏览器打开既可以看到我们打包过后的内容。

![](http://5coder.cn/img/1667985169_f226c9deae68b804821a85e89a82005c.png)

## 25.HMR 功能使用

HMR全称是**Hot Module Replacement**，叫做**模块热替换或者叫做模块热更新**。计算机行业经常听到一个叫做**热拔插**的名词，那指的就是可以在一个正在运行的机器上随时去插拔设备，而机器的运行状态是不会受插设备的影响，而且插上的设备可以立即开始工作，例如电脑上的USB端口就是可以热拔插的。

模块热替换当中的这个**热**，跟刚刚提到的热拔插实际上是一个道理，它们都是在运行过程中的**即时变化**，那**Webpack中的模块热替换指的就是可以在应用程序运行的过程中实时的去替换掉应用中的某个模块，而应用的运行状态不会因此而改变**。

> 例如在应用程序的运行过程中，修改了某个模块，通过自动刷新就会导致整个应用整体的刷新，页面中的状态信息都会丢失掉，而如果这个地方使用的是热替换的话，就可以实现只将刚刚修改的这个模块实时的去替换到应用当中，不必去完全刷新应用。

在src/index.js中打印文字，并且在Webpack.config.js中进行配置相应字段：`target: 'web'`、`devServer: {hot: true}`

Webpack.config.js

```js
const path = require('path')
const CopyWebpackPlugin = require('copy-Webpack-plugin')
const { DefinePlugin } = require('Webpack')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')

module.exports = {
  mode: 'development',
  devtool: false,
  entry: './src/index.js',
  output: {
    filename: 'js/main.js',
    path: path.resolve(__dirname, 'dist')
  },
  target: 'web',
  devServer: {
    hot: true
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {
          filename: 'font/[name].[hash:3][ext]'
        }
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'copyWebpackPlugin',
      template: './public/index.html'
    }),
    new DefinePlugin({
      BASE_URL: '"./"'
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'public',
          globOptions: {
            ignore: ['**/index.html']
          }
        }
      ]
    })
  ]
}

```

这是启动yarn serve命令，发现我们手动修改index.js中的打印内容后，页面也会随之变化。

![](http://5coder.cn/img/1667999781_c28fc53bdbdcd5352bd5537f3c22a4ee.png)

但是，我们发现，当在文本框内输入内容后，再次修改index.js打印内容，页面刷新后输入框中的内容也随之消失，整个界面被全部刷新，这并不符合我们的局部模块热更新的需求。

新建与index.js同目录的title.js文件，其中打印字符串，并在index.js做如下配置。修改过后，重新启动yarn serve，然后依次修改title.js中的打印内容。我们发现，html文件的打印内容随着变化，并且console中的打印历史纪录也不会被清空。随后在页面输入框内输入文字，再次修改title.js中的打印内容，Webpack热更新过后，发现页面的输入框文字并没有消失，而且打印内容也随之变化。这样就实现了HMR热更新效果。

![](http://5coder.cn/img/1668000484_0fe145a3fc87b7bdc516d1d33141a530.png)

![](http://5coder.cn/img/1668000539_7449d399990b0b80d479fced3b67334d.png)

## 26.React 组件支持热更新

第一步：Webpack支持jsx打包；第二步：Webpack支持react的热更新。

第一步创建`App.jsx` React组件，在其中书写`title`文字内容。其次在`index.js`中进行导入，并挂在到提前准备好的`index.html`模板中的`id="app"`中。其次在`Webpack.config.js`中引入针对`jsx`的`loader`。此时，启动`yarn serve`，发现每当修改`title.js`中的打印内容时，`console`会随之变化。但是当修改`App.jsx`中的`title`文字时，发现`console`中已经热更新的打印内容被清除了。这是因为目前还没有实现针对`React`组件模块的热更新效果。

第二步，需要实现针对`React`组件的热更新效果。在Webpack.config.js中引入`@pmmmwh/react-refresh-Webpack-plugin`，并且在相应的`plugins`中进行创建`new ReactRefreshWebpackPlugin()`。随后在babel.config.js中进行单独的配置`react-refresh/babel`，使其提供模块热更新的能力。

随后，再次修改`title.js`中内容后，我们发现对应的`console`中为打印结果已经被修改。再次修改`React`组件`App.jsx`中的`title`文字内容后，发现`console`中的打印内容被保留了下来，至此我们就实现了`React`组件支持热更新功能。

```js
module.exports = {
  presets: [
    ['@babel/preset-env'],
    ['@babel/preset-react'],
  ],
  plugins: [
    ['react-refresh/babel']
  ]
}
```

![](http://5coder.cn/img/1668001625_826de514c8ec5cc909dcb45e68ae10b2.png)

![](http://5coder.cn/img/1668001674_a7806168060433aac226ae50c0eed946.png)

![](http://5coder.cn/img/1668001758_c054454583a1115cf239ec98fac12cfa.png)

## 27.Vue 组件支持热更新

提前准备App.vue

```vue
<template>
  <div class="example">{{ msg }}</div>
</template>

<script>
export default {
  data() {
    return {
      msg: 'Hello world!',
    }
  },
}
</script>

<style>
.example {
  color: orange;
}
</style>
```

当前`Webpack`并不能识别`.vue`结尾的文件，所以需要在`Webpack.confiog.js`中针对.`vue`结尾的文件进行处理.在Vue2中使用vue-loader14版本的时候只需要做如下配置。

```js
{
  test: /\.vue$/,
    use: ['vue-loader']
}
```

但是在VUe2中使用vue-loader15版本时，需要单独引入`vue-loader/lib/plugin`。

![](http://5coder.cn/img/1668004796_e3fbaf42d273631b503ad0c9eaa4693a.png)

根据Webpack官方文档的提示，vue-loader是其默认提供的，不需要单独安装。

> `vue-loader`的16版本是专门提供给`Vue3`的，不能在`Vue2`中使用。其次`Vue2`中，如果使用`vue-loader`14版本的，可以做到开箱即用。但是如果升级到15版本后，需要单独的引入`vue-loader/lib/plugin`，并且进行new操作才可以正常实现HMR功能。

![](http://5coder.cn/img/1668003480_323ea361dbf104d652fd08c670a62aea.png)

下一步就是在index.js中引入App.vue文件，将其挂在到依赖图当中。

```js
import './title'
import Vue from 'vue'
import App from './App.vue'

if (module.hot) {
  module.hot.accept(['./title.js'], () => {
    console.log('title.js模块更新')
  })
}

new Vue({
  render: h => h(App)
}).$mount('#root')

```

随后，依据上一个内容的测试，分别修改title.js与App.vue中的内容，发现已经实现了Vue的HMR模块热更新的功能。

## 28.output 中的 path

- path：所有输出文件的目标路径;打包后文件在硬盘中的存储位置。
- publicPath：输出解析文件的目录，指定资源文件引用的目录 ，打包后浏览器访问服务时的 url 路径中通用的一部分。

区别：

path是[Webpack](https://so.csdn.net/so/search?q=Webpack&spm=1001.2101.3001.7020)所有文件的输出的路径，必须是绝对路径，比如：output输出的js,url-loader解析的图片，HtmlWebpackPlugin生成的html文件，都会存放在以path为基础的目录下。publicPath 并不会对生成文件的路径造成影响，主要是对你的页面里面引入的资源的路径做对应的补全，常见的就是css文件里面引入的图片。

output：“path”项和“publicPath”项

output项告诉Webpack怎样存储输出结果以及存储到哪里。output的两个配置项“path”和“publicPath”可能会造成困惑。“path”仅仅告诉Webpack结果存储在哪里，然而“publicPath”项则被许多Webpack的插件用于在生产模式下更新内嵌到css、html文件里的url值。

例如，在localhost（译者注：即本地开发模式）里的css文件中边你可能用“./test.png”这样的url来加载图片，但是在生产模式下“test.png”文件可能会定位到CDN上并且你的Node.js服务器可能是运行在HeroKu上边的。这就意味着在生产环境你必须手动更新所有文件里的url为CDN的路径。

然而你也可以使用Webpack的“publicPath”选项和一些插件来在生产模式下编译输出文件时自动更新这些url。

```js
// 开发环境：Server和图片都是在localhost（域名）下
.image { 
  background-image: url('./test.png');
 }
// 生产环境：Server部署下HeroKu但是图片在CDN上
.image { 
  background-image: url('https://someCDN/test.png');
 }
```

## 29.devserver 中的 path

> 这个配置其实是蛮有讲头的，他的本意也是路径前缀，但是跟其他`publicPath`有所区别：
>
> 首先，`devServer`配置起作用需要两个条件：
>
> 安装了`Webpack-dev-server`
> 使用开发环境起服务，脚本一般为`Webpack serve`
> 有了以上的前缀，现在具体来讲讲这个配置的具体应用：

> 比如`publicPath`设置成了`/yuhua/`，那么意思就是访问服务需要带上公共资源路径`/yuhua/`，也就是说，不写`publicPath`，那么访问在`http://localhost:8080`,如果`publicPath`为`/yuhua/`，那么访问就在`http://localhost:8080/yuhua/`，包括访问打包产物，也是在`http://localhost:8080/yuhua/`下访问。

```js
const path = require('path');
module.exports = {
    devServer: {
        publicPath: '/yuhua/', // 服务会起在/yuhua/下，比如不写这个publicPath的时候，访问是http://localhost:8080/,那么写了之后就是http://localhost:8080/yuhua就能访问到首页，以及dist打包出来的资源都以后者为路径前缀
        contentBase: path.resolve(__dirname, 'public'), // 额外的静态文件目录内容，所谓的额外的，就是指不会被打包进去的，但是我可以将contentBase作为静态服务器资源目录，其实就相当于景台服务器，浏览器可以直接访问对应目录下的文件
      },
}
```

如果在`output`中也设置了`publicPath`，这其实是不冲突的，比如下面的代码,那么你所有的打包产物的访问地址会有两步处理：

打包出的结果，引用资源都会加上output下的publicPath。起开发服务后，会在服务地址后加上devServer下的publicPath。所以综上所述

- 起的开发服务地址是：`http://localhost:8080/[devServer下的publicPath]`
- 起的开发服务下打包资源地址是：`http://localhost:8080/[devServer下的publicPath]/[output下的publicPath]`

```js
const path = require('path');
module.exports = {
    output: {
        path: ptah.resolve(__dirname, 'dist')
        filename: 'main.js',
        publicPath: 'abc/' // 这里配置，那么html中引用的图片<img src="./a,png"/>就会打包成<img src="abc/a.png">
    },
    devServer: {
        publicPath: '/yuhua/', // 服务会起在/yuhua/下，比如不写这个publicPath的时候，访问是http://localhost:8080/,那么写了之后就是http://localhost:8080/yuhua就能访问到首页，以及dist打包出来的资源都以后者为路径前缀
        contentBase: path.resolve(__dirname, 'public'), // 额外的静态文件目录内容，所谓的额外的，就是指不会被打包进去的，但是我可以将contentBase作为静态服务器资源目录，其实就相当于景台服务器，浏览器可以直接访问对应目录下的文件
      },
}
```

devServer还有一个属性叫做contentBase，这个属性用于额外的静态文件目录内容，所谓的额外的，就是指不会被打包进去的，但是我可以将contentBase作为静态服务器资源目录，其实就相当于景台服务器，浏览器可以直接访问对应目录下的文件。另外，如果找不到dist下（内存中）的静态文件，就会去这个目录下找。

举例说明：

有一个public文件夹下的text.txt，内容为123。同时，contentBase属性的值就是path.resolve(__dirname, 'public')，那么这时候访问text.txt文件的地址为：http://localhost:8080/test.txt。意思就是我将contentBase对应的目录，所谓我静态资源服务目录，可以直接访问。

那么`contentBase`与`publicPath`有关系吗？其实没有什么关系，不论是`output`的`publicPath`还是`devServer`的`publicPath`,都没关系

```js
const path = require('path');
module.exports = {
    output: {
        path: ptah.resolve(__dirname, 'dist')
        filename: 'main.js',
        publicPath: 'abc/'
    },
    devServer: {
        publicPath: '/yuhua/',
        contentBase: path.resolve(__dirname, 'public'),
      },
}
```

## 30.devServer 常用配置

使用Webpack-dev-server是，有其他可用配置，可使得开发阶段拥有跟好的体验和性能。

- `hotOnly：true`

  当我们的某个组件发生语法性错误时，`Webpack`会自动帮我们抛出错误，但是当我们修改完错误后，`Webpack-dev-server`会自动刷新整个页面，这就导致某些已经拥有数据的组件会重新刷新初始化。我们希望在修改完错误后，只针对修改错误的组件进行刷新，这时就可以开启`hotOnly`只针对当前错误组件进行刷新，保留其他组件的状态。

- `port：4000`

  `Webpack-dev-server`默认的端口号是8080，但是如果我们的8080端口号被其他服务占用时，可以开启`port`配置，并设置自己想要`Webpack-dev-serve`提供服务的端口号。

- `open：true`

  `Webpack-dev-server`打包完成后，默认情况下不会帮我们打开浏览器，需要用户手动打开浏览器访问`localhost:8080`。这时可以设置`open`为`true`，当`Webpack-dev-server`打包完成后，自动打开浏览器。但是，当我们修改其中的文件后，`Webpack-dev-server`会帮我们再次打开浏览器，这就导致有多个浏览器进程存在，影响性能。所以一般情况下，我们保持关闭`false`状态。

- `compress：true`

  `Webpack-dev-server`默认打包的资源不会进行压缩，可以开启`compress`选项，对文件进行`gzip`压缩，提高页面访问性能。

- `historyApiFallback：true`

  一般情况下，当我们使用`Vue`或`React`时，提供路由跳转功能，当前端路由跳转后，浏览器路径为前端控制。但是当我们手动对当前页面刷新（相当于重新向服务器索要about页面），会出现`404`状态。`historyApiFallback`开启后，会将`404`重定向到`index.html`。

## 31.proxy 代理设置

为什么开发阶段需要设置代理，在开发阶段，我们需要请求后端接口，但是一般后端接口地址和我们本地的不在同一个服务中提供，这时进行访问就会存在跨域的问题，所以我们需要对我们的请求进行转啊操作。模拟跨域请求代码如下：

> https://api.github.com/users是github提供的公开接口，可正常请求
>
> ![](http://5coder.cn/img/1668299754_3f7aeb1cda34d7b7f2ba5f4d53876fe9.png)

在React demo中，index.js使用axios进行请求。

```js
import './title'
import React from 'react'
import ReactDOM from 'react-dom'
import App from './App.jsx'
import axios from 'axios'

if (module.hot) {
  module.hot.accept(['./title.js'], () => {
    console.log('title.js模块更新')
  })
}

ReactDOM.render(<App />, document.getElementById('app'))

axios.get('/api/users').then((res) => {
  console.log(res.data)
})
```

![](http://5coder.cn/img/1668299987_f500e961d4371fe2467dc27d904f15fc.png)

> 由于该接口不存在跨域问题，**这里默认他会存在这个问题**

```js
...
    proxy: {
      // /api/users
      // http://localhost:4000/api/users
      // https://api.github.com/info/users
      // /api/users---> 返回
      '/api': {
        target: 'https://api.github.com',
        pathRewrite: { "^/api": "" },
        changeOrigin: true
      }
    }
...
```

首先，在devServer配置中添加proxy配置，添加`/api`标记，当我们本地服务进行接口请求时，通过`/api`标记会进入下面的配置中。

设置target属性，告诉Webpack-dev-server检测到该标记后，去请求那个路径（`target: 'https://api.github.com'`）。配置过后，我们回到index.js中，修改请求的路径为`/api/users`，这是发现依然无法请求成功，该接口依然抛出500服务端异常。

这是因为，github提供的接口下，并没有一个名为`/api`的服务，所以需要对/api接口 进行路径重写，添加pathRewrite配置，将其值配置为`pathRewrite: { "^/api": "" }`，告诉Webpack-dev-server遇到`https://api.github.com/api`时，自动替换路径为`https://api.github.com/`。

这时我们依然发现无法访问，这又是因为github对我们的请求来源进行校验，他拒绝了我们的请求。需要设置`changeOrigin`属性，更改`host`来源，`changeOrigin: true`。

这时就可以正常访问该接口。

## 32.[resolve](https://www.Webpackjs.com/configuration/resolve/#resolve) 模块解析规则

> 配置模块如何解析。例如，当在 ES2015 中调用 `import 'lodash'`，`resolve` 选项能够对 Webpack 查找 `'lodash'` 的方式去做修改（查看[`模块`](https://www.Webpackjs.com/configuration/resolve/#resolve-modules)）。
>
> resolve文档

### 32.1  什么是 resolve 模块解析

在开发中我们会有各种各样的模块依赖，例如 js 文件、css 文件、vue 文件等，有自己编写的，也有[第三方库](https://so.csdn.net/so/search?q=第三方库&spm=1001.2101.3001.7020)。resolve 可以让 [Webpack](https://so.csdn.net/so/search?q=Webpack&spm=1001.2101.3001.7020) 在 require/import 语句中，找到需要解析的模块代码

### 32.2  配置自动寻找依赖的路径

模块路径：在 resolve.modules 中配置：到时导入下载好的依赖就会去 node_modules 文件夹里找

```js
resolve: {
    module: ["node_modules"], // 到时就会在 node_modules文件夹里面查找依赖包
}
```

拓展名配置：配置指定文件后就可以不写此文件的扩展名了

```js
resolve: {
    module: ["node_modules"], // 到时就会在 node_modules文件夹里面查找依赖包
    extendsions: [".js", ".json", ".mjs", "vue"], // 添加了 vue 后导入 vue 文件就不需要加文件扩展名了
  },
```

配置路径别名：为了简化相对路径的书写，我们直接配置路径给它一个别名：alias 

![](http://5coder.cn/img/1668434322_f87a0fd49cf77c6d70677ed855a5c9b1.png)

我们需要在 index.js 导入 js 里面的 api.js 时，我们需要写成 ./js/api.js

我们希望写成 js/api ，配置如下：

```js
 resolve: {
    modules: ["node_modules"], // 到时就会在 node_modules文件夹里面查找依赖包
    extensions: [".js", ".json", ".mjs", "vue"], // 添加了 vue 后导入 vue 文件就不需要加文件扩展名了
    alias: {
      "js": path.resolve(__dirname, "./js"), // '以后可以使用 js 代替 ./js
      "@": path.resolve(__dirname, "./src"), // @ 替换根目录
    },
  },
```

### 32.3  不同环境下的 Webpack 配置文件

我们在不同的环境下需要不同的配置，显然一个 Webpack.config.js 配置文件是不够的，在不同的环境使用不同的配置，比如我们在生产环境不需要 clearn-Webpack-plugin 的插件清理旧文件。

我们在根目录下新键文件夹：config，在里面新建 三个文件，一个是公共的配置、一个开发环境、一个生产环境。![](http://5coder.cn/img/1668434394_52864808e988dd7ead829b210f0852d1.png)

配置：

先把 Webpack.config.js 文件内容复制一份去 comm.config.js 里, 然后按需提取至不同的配置文件。

把共同的文件留在 comm.config.js 里，使用插件再去各自合并

merge 插件：

安装：`npm install Webpack-merge -D`

使用：将公共配置和开发环境的配置结合在一起

```js
const { merge } = require("Webpack-merge");
 
const commconfig = require("./Webpack.comm.config");
 
module.exports = merge(commconfig, {
  开发环境的配置
});
```

注意相对路径的变化，除了有些路径的会默认根目录查找，其他正常路径需要修改。

完整代码演示：

![](http://5coder.cn/img/1668434546_48fab64f2986e4db46d365b5cfb916d9.png)

## 33.source-map 作用

js变异之后生成的具体源码，然后再找回到编译之前的源代码的source-map操作。

代码目录如下：

![](http://5coder.cn/img/1668434922_80f88054bb28d9d5d3af157258775dfc.png)

**顺带一提`mode`**

### 33.1 模式(Mode)

提供 `mode` 配置选项，告知 Webpack 使用相应模式的内置优化。

```
string = 'production': 'none' | 'development' | 'production'
```

#### 用法

只需在配置对象中提供 `mode` 选项：

```javascript
module.exports = {
  mode: 'development',
};
```

或者从 [CLI](https://www.Webpackjs.com/api/cli/) 参数中传递：

```bash
Webpack --mode=development
```

支持以下字符串值：

| 选项          | 描述                                                         |
| :------------ | :----------------------------------------------------------- |
| `development` | 会将 `DefinePlugin` 中 `process.env.NODE_ENV` 的值设置为 `development`. 为模块和 chunk 启用有效的名。 |
| `production`  | 会将 `DefinePlugin` 中 `process.env.NODE_ENV` 的值设置为 `production`。为模块和 chunk 启用确定性的混淆名称，`FlagDependencyUsagePlugin`，`FlagIncludedChunksPlugin`，`ModuleConcatenationPlugin`，`NoEmitOnErrorsPlugin` 和 `TerserPlugin` 。 |
| `none`        | 不使用任何默认优化选项                                       |

**如果没有设置，Webpack 会给 `mode` 的默认值设置为 `production`。**

> 如果 `mode` 未通过配置或 CLI 赋值，CLI 将使用可能有效的 `NODE_ENV` 值作为 `mode`。

#### Mode: development

如果设置为development时，Webpack会自动帮我们加上`devtool:'eval'`，这就是下图红框中的内容。

```js
// Webpack.development.config.js
module.exports = {
  mode: 'development',
};
```

![](http://5coder.cn/img/1668435209_ce94bad51364bc076d5d2ba2049acce1.png)

#### Mode: production（默认值）

```js
// Webpack.production.config.js
module.exports = {
  mode: 'production',
};
```

![](http://5coder.cn/img/1668435239_9db537d3aafe6d9df4882209ff19f53b.png)

#### Mode: none

```js
// Webpack.custom.config.js
module.exports = {
  mode: 'none',
};
```

如果要根据 *Webpack.config.js* 中的 **mode** 变量更改打包行为，则必须将配置导出为函数，而不是导出对象：

```javascript
var config = {
  entry: './app.js',
  //...
};

module.exports = (env, argv) => {
  if (argv.mode === 'development') {
    config.devtool = 'source-map';
  }

  if (argv.mode === 'production') {
    //...
  }

  return config;
};
```

当我们代码中出现了一些错误，但是我们并未设置source-map配置项，这就导致在浏览器中的报错，我们无法定位到具体报错的位置，如下图：

![](http://5coder.cn/img/1668436017_bdd5e0e139cfdd3ba93df6ddaca0a86b.png)

在配置了source-map的时候，本地进行yarn build打包过后，发现打包结果多了`main.js.map`文件，同时`main.js`中的内容也更利于查看。

![](http://5coder.cn/img/1668436292_372753f1ee03f8a48ac150a218a19e3a.png)

![](http://5coder.cn/img/1668436361_d38397b81e486dffb741031fbe5be365.png)

![](http://5coder.cn/img/1668436387_dbf4eeaa5fe9ade31936053ca97f3127.png)

source-map工作流程

- 根据源文件中的源代码，生成source-map文件
- 浏览器开启source-map功能，浏览器基于生成的source-map来进行查找



## 34.devtool 详细说明

此选项控制是否生成，以及如何生成 source map。

使用 [`SourceMapDevToolPlugin`](https://www.Webpackjs.com/plugins/source-map-dev-tool-plugin) 进行更细粒度的配置。查看 [`source-map-loader`](https://www.Webpackjs.com/loaders/source-map-loader) 来处理已有的 source map。

#### devtool

```
string = 'eval'` `false
```

选择一种 [source map](http://blog.teamtreehouse.com/introduction-source-maps) 风格来增强调试过程。不同的值会明显影响到构建(build)和重新构建(rebuild)的速度。

> Webpack 仓库中包含一个 [显示所有 `devtool` 变体效果的示例](https://github.com/Webpack/Webpack/tree/master/examples/source-map)。这些例子或许会有助于你理解这些差异之处。

> 你可以直接使用 `SourceMapDevToolPlugin`/`EvalSourceMapDevToolPlugin` 来替代使用 `devtool` 选项，因为它有更多的选项。切勿同时使用 `devtool` 选项和 `SourceMapDevToolPlugin`/`EvalSourceMapDevToolPlugin` 插件。`devtool` 选项在内部添加过这些插件，所以你最终将应用两次插件。

| devtool                                    | performance                              | production | quality        | comment                                                      |
| :----------------------------------------- | :--------------------------------------- | :--------- | :------------- | :----------------------------------------------------------- |
| (none)                                     | **build**: fastest  **rebuild**: fastest | yes        | bundle         | Recommended choice for production builds with maximum performance. |
| **`eval`**                                 | **build**: fast  **rebuild**: fastest    | no         | generated      | Recommended choice for development builds with maximum performance. |
| `eval-cheap-source-map`                    | **build**: ok  **rebuild**: fast         | no         | transformed    | Tradeoff choice for development builds.                      |
| `eval-cheap-module-source-map`             | **build**: slow  **rebuild**: fast       | no         | original lines | Tradeoff choice for development builds.                      |
| **`eval-source-map`**                      | **build**: slowest  **rebuild**: ok      | no         | original       | Recommended choice for development builds with high quality SourceMaps. |
| `cheap-source-map`                         | **build**: ok  **rebuild**: slow         | no         | transformed    |                                                              |
| `cheap-module-source-map`                  | **build**: slow  **rebuild**: slow       | no         | original lines |                                                              |
| **`source-map`**                           | **build**: slowest  **rebuild**: slowest | yes        | original       | Recommended choice for production builds with high quality SourceMaps. |
| `inline-cheap-source-map`                  | **build**: ok  **rebuild**: slow         | no         | transformed    |                                                              |
| `inline-cheap-module-source-map`           | **build**: slow  **rebuild**: slow       | no         | original lines |                                                              |
| `inline-source-map`                        | **build**: slowest  **rebuild**: slowest | no         | original       | Possible choice when publishing a single file                |
| `eval-nosources-cheap-source-map`          | **build**: ok  **rebuild**: fast         | no         | transformed    | source code not included                                     |
| `eval-nosources-cheap-module-source-map`   | **build**: slow  **rebuild**: fast       | no         | original lines | source code not included                                     |
| `eval-nosources-source-map`                | **build**: slowest  **rebuild**: ok      | no         | original       | source code not included                                     |
| `inline-nosources-cheap-source-map`        | **build**: ok  **rebuild**: slow         | no         | transformed    | source code not included                                     |
| `inline-nosources-cheap-module-source-map` | **build**: slow  **rebuild**: slow       | no         | original lines | source code not included                                     |
| `inline-nosources-source-map`              | **build**: slowest  **rebuild**: slowest | no         | original       | source code not included                                     |
| `nosources-cheap-source-map`               | **build**: ok  **rebuild**: slow         | no         | transformed    | source code not included                                     |
| `nosources-cheap-module-source-map`        | **build**: slow  **rebuild**: slow       | no         | original lines | source code not included                                     |
| `nosources-source-map`                     | **build**: slowest  **rebuild**: slowest | yes        | original       | source code not included                                     |
| `hidden-nosources-cheap-source-map`        | **build**: ok  **rebuild**: slow         | no         | transformed    | no reference, source code not included                       |
| `hidden-nosources-cheap-module-source-map` | **build**: slow  **rebuild**: slow       | no         | original lines | no reference, source code not included                       |
| `hidden-nosources-source-map`              | **build**: slowest  **rebuild**: slowest | yes        | original       | no reference, source code not included                       |
| `hidden-cheap-source-map`                  | **build**: ok  **rebuild**: slow         | no         | transformed    | no reference                                                 |
| `hidden-cheap-module-source-map`           | **build**: slow  **rebuild**: slow       | no         | original lines | no reference                                                 |
| `hidden-source-map`                        | **build**: slowest  **rebuild**: slowest | yes        | original       | no reference. Possible choice when using SourceMap only for error reporting purposes. |

| shortcut                | explanation                                                  |
| :---------------------- | :----------------------------------------------------------- |
| performance: build      | How is the performance of the initial build affected by the devtool setting? |
| performance: rebuild    | How is the performance of the incremental build affected by the devtool setting? Slow devtools might reduce development feedback loop in watch mode. The scale is different compared to the build performance, as one would expect rebuilds to be faster than builds. |
| production              | Does it make sense to use this devtool for production builds? It's usually `no` when the devtool has a negative effect on user experience. |
| quality: bundled        | You will see all generated code of a chunk in a single blob of code. This is the raw output file without any devtooling support |
| quality: generated      | You will see the generated code, but each module is shown as separate code file in browser devtools. |
| quality: transformed    | You will see generated code after the preprocessing by loaders but before additional Webpack transformations. Only source lines will be mapped and column information will be discarded resp. not generated. This prevents setting breakpoints in the middle of lines which doesn't work together with minimizer. |
| quality: original lines | You will see the original code that you wrote, assuming all loaders support SourceMapping. Only source lines will be mapped and column information will be discarded resp. not generated. This prevents setting breakpoints in the middle of lines which doesn't work together with minimizer. |
| quality: original       | You will see the original code that you wrote, assuming all loaders support SourceMapping. |
| `eval-*` addition       | generate SourceMap per module and attach it via eval. Recommended for development, because of improved rebuild performance. Note that there is a windows defender issue, which causes huge slowdown due to virus scanning. |
| `inline-*` addition     | inline the SourceMap to the original file instead of creating a separate file. |
| `hidden-*` addition     | no reference to the SourceMap added. When SourceMap is not deployed, but should still be generated, e. g. for error reporting purposes. |
| `nosources-*` addition  | source code is not included in SourceMap. This can be useful when the original files should be referenced (further config options needed). |

> 验证 devtool 名称时， 我们期望使用某种模式， 注意不要混淆 devtool 字符串的顺序， 模式是： `[inline-|hidden-|eval-][nosources-][cheap-[module-]]source-map`.

> 其中一些值适用于开发环境，一些适用于生产环境。对于开发环境，通常希望更快速的 source map，需要添加到 bundle 中以增加体积为代价，但是对于生产环境，则希望更精准的 source map，需要从 bundle 中分离并独立存在。

> 查看 [`output.sourceMapFilename`](https://www.Webpackjs.com/configuration/output#output-sourcemapfilename) 自定义生成的 source map 的文件名。

#### 品质说明(quality)

`打包后的代码` - 将所有生成的代码视为一大块代码。你看不到相互分离的模块。

`生成后的代码` - 每个模块相互分离，并用模块名称进行注释。可以看到 Webpack 生成的代码。示例：你会看到类似 `var module__Webpack_IMPORTED_MODULE_1__ = __Webpack_require__(42); module__Webpack_IMPORTED_MODULE_1__.a();`，而不是 `import {test} from "module"; test();`。

`转换过的代码` - 每个模块相互分离，并用模块名称进行注释。可以看到 Webpack 转换前、loader 转译后的代码。示例：你会看到类似 `import {test} from "module"; var A = function(_test) { ... }(test);`，而不是 `import {test} from "module"; class A extends test {}`。

`原始源代码` - 每个模块相互分离，并用模块名称进行注释。你会看到转译之前的代码，正如编写它时。这取决于 loader 支持。

`无源代码内容` - source map 中不包含源代码内容。浏览器通常会尝试从 web 服务器或文件系统加载源代码。你必须确保正确设置 [`output.devtoolModuleFilenameTemplate`](https://www.Webpackjs.com/configuration/output/#output-devtoolmodulefilenametemplate)，以匹配源代码的 url。

`（仅限行）` - source map 被简化为每行一个映射。这通常意味着每个语句只有一个映射（假设你使用这种方式）。这会妨碍你在语句级别上调试执行，也会妨碍你在每行的一些列上设置断点。与压缩后的代码组合后，映射关系是不可能实现的，因为压缩工具通常只会输出一行。

#### 对于开发环境

以下选项非常适合开发环境：

`eval` - 每个模块都使用 `eval()` 执行，并且都有 `//# sourceURL`。此选项会非常快地构建。主要缺点是，由于会映射到转换后的代码，而不是映射到原始代码（没有从 loader 中获取 source map），所以不能正确的显示行数。

`eval-source-map` - 每个模块使用 `eval()` 执行，并且 source map 转换为 DataUrl 后添加到 `eval()` 中。初始化 source map 时比较慢，但是会在重新构建时提供比较快的速度，并且生成实际的文件。行数能够正确映射，因为会映射到原始代码中。它会生成用于开发环境的最佳品质的 source map。

`eval-cheap-source-map` - 类似 `eval-source-map`，每个模块使用 `eval()` 执行。这是 "cheap(低开销)" 的 source map，因为它没有生成列映射(column mapping)，只是映射行数。它会忽略源自 loader 的 source map，并且仅显示转译后的代码，就像 `eval` devtool。

`eval-cheap-module-source-map` - 类似 `eval-cheap-source-map`，并且，在这种情况下，源自 loader 的 source map 会得到更好的处理结果。然而，loader source map 会被简化为每行一个映射(mapping)。

#### 特定场景

以下选项对于开发环境和生产环境并不理想。他们是一些特定场景下需要的，例如，针对一些第三方工具。

`inline-source-map` - source map 转换为 DataUrl 后添加到 bundle 中。

`cheap-source-map` - 没有列映射(column mapping)的 source map，忽略 loader source map。

`inline-cheap-source-map` - 类似 `cheap-source-map`，但是 source map 转换为 DataUrl 后添加到 bundle 中。

`cheap-module-source-map` - 没有列映射(column mapping)的 source map，将 loader source map 简化为每行一个映射(mapping)。

`inline-cheap-module-source-map` - 类似 `cheap-module-source-map`，但是 source mapp 转换为 DataUrl 添加到 bundle 中。

#### 对于生产环境

这些选项通常用于生产环境中：

`(none)`（省略 `devtool` 选项） - 不生成 source map。这是一个不错的选择。

`source-map` - 整个 source map 作为一个单独的文件生成。它为 bundle 添加了一个引用注释，以便开发工具知道在哪里可以找到它。

> 你应该将你的服务器配置为，不允许普通用户访问 source map 文件！

`hidden-source-map` - 与 `source-map` 相同，但不会为 bundle 添加引用注释。如果你只想 source map 映射那些源自错误报告的错误堆栈跟踪信息，但不想为浏览器开发工具暴露你的 source map，这个选项会很有用。

> 你不应将 source map 文件部署到 web 服务器。而是只将其用于错误报告工具。

`nosources-source-map` - 创建的 source map 不包含 `sourcesContent(源代码内容)`。它可以用来映射客户端上的堆栈跟踪，而无须暴露所有的源代码。你可以将 source map 文件部署到 web 服务器。

> 这仍然会暴露反编译后的文件名和结构，但它不会暴露原始代码。

> 如果默认的 Webpack `minimizer` 被覆盖 (例如自定义 `terser-Webpack-plugin` 选项)， 请确保将其替换配置为 `sourceMap: true` 以启用 SourceMap 支持。
>
> 由上面了解到，设置为development后，默认的devtool为eval，这里我们将它更改为source-map

## 35.ts-loader 编译 TS

在项目开发中我们可能使用`TypeScript`进行编码开发，所以需要使用`Webpack`对`TypeScript`进行编译，编译为`JavaScript`文件。

首先对`ts-loader`进行安装

```bash
yarn add ts-loader
```

安装完成后，查看项目目录及`TypeScript`代码：

![](http://5coder.cn/img/1668465254_884e41b204c4fc3525218b686302e5ca.png)

`TypeScript`的编译可以使用`TypeScript Compiler`进行编译：

```bash
tsc ./scr/index.ts
```

编译完成后，在src目录下生成`index.js`文件。但是这样会存在问题，比如需要编译很多TypeScript文件，或者需要将打包好的文件放到指定的目录。

 ![](http://5coder.cn/img/1668465467_8098f1b7a1aa61aa5ac7165eeedb0e6e.png)

`TypeScript`的编译可以使用ts-loader进行编译。

Webpack.config.js配置

```js
const path = require('path')
const { DefinePlugin } = require('Webpack')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')

module.exports = {
  mode: 'development',
  entry: './src/index.ts',
  devtool: 'nosources-source-map',
  output: {
    filename: 'js/main.js',
    path: path.resolve(__dirname, 'dist')
  },
  target: 'web',
  devServer: {
    hot: true,
    port: 4000
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        use: ['babel-loader']
      },
      {
        test: /\.ts$/,
        use: ['ts-loader']
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'copyWebpackPlugin',
      template: './public/index.html'
    }),
    new DefinePlugin({
      BASE_URL: '"./"'
    })
  ]
}

// source-map  cheap-module-source-map
```

编译完成后，在浏览器中可以正常执行。

![](http://5coder.cn/img/1668465609_6b2937469203f1ef4c834099bf1ead17.png)

## 36.babel-loader 编译 TS

当`TypeScript`中存在较新的`JavaScript`代码，比如`Promise`，可以发现使用`ts-loader`进行编译没有报错，但是在编译后的文件中，并没有对`Promise`进行特殊的兼容性处理。所以需要使用`babel-loader`对`TypeScript`进行编译。

![](http://5coder.cn/img/1668472149_9807cd5867dd16916b0044cf70c73cc9.png)

之前一直在使用`@bebel/preset-env`，这里我们需要使用`@bebel/preset-typescript`预设对`TypeScript`进行编译兼容性处理。

![](http://5coder.cn/img/1668471866_e1f2f5c1d27856c46f432655acc12cdd.png)

安装`@bebel/preset-typescript`

```shell
yarn add @babel/preset-typescript
```

在babel.config.js中进行相应配置：

```js
module.exports = {
  presets: [
    ['@babel/preset-env', {
      useBuiltIns: 'usage',
      corejs: 3
    }],
    ['@babel/preset-typescript']
  ]
}
```

![](http://5coder.cn/img/1668472433_b0a7f2fd7f8c6173a65afbf84db3ea06.png)

再次打包编译后，发现编译后的main.js代码量大了很多，对Promise等ES6+的语法也做了相应的兼容。

**ts-loader和@babel/preset-typescript的区别：**

`ts-loader`虽然不能在编译阶段进行`polyfill`的填充，但是他可以在编译阶段，提前暴露出来语法错误问题。

反而`babel-loader`可以进行`polyfill`填充，但是在编译阶段它不可以进行提前暴露错误，只有在运行阶段时才抛出错误。

如果既想要对TypeScript进行语法转换又想要实时的暴露出错误，TypeScript官网也给出了建议，分先后，在打包之前对语法先做校验，完事之后再做build操作。

![](http://5coder.cn/img/1668472853_48dd0844c210557a2be07119de54fb12.png)

## 37.加载 vue 文件

`Webpack`对`.vue`文件加载操作：

![](http://5coder.cn/img/1668473101_ea3aba5660d59c6bb32a1002e93e3607.png)

创建App.vue，并安装`vue`、`vue-loader`、`vue-template-compiler`。

首先，在index.js中导入vue

```js
import Vue from 'vue'
import App from './App.vue'

new Vue({
  render: h => h(App)
}).$mount('#app')
```

其次在Webpack.config.js中配置相应的`loader`，由于vue文件中存在`less`模式的`css`样式，所以需要单独对`css`文件进行`loader`转换。

```js
const path = require('path')
const { DefinePlugin } = require('Webpack')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')
const VueLoaderPlugin = require('vue-loader/lib/plugin')

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  devtool: false,
  output: {
    filename: 'js/main.js',
    path: path.resolve(__dirname, 'dist')
  },
  target: 'web',
  devServer: {
    hot: true,
    port: 4000
  },
  module: {
    rules: [
      {
        test: /\.less$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 2
            }
          },
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.jsx?$/,
        use: ['babel-loader']
      },
      {
        test: /\.ts$/,
        use: ['babel-loader']
      },
      {
        test: /\.vue$/,
        use: ['vue-loader']
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'copyWebpackPlugin',
      template: './public/index.html'
    }),
    new DefinePlugin({
      BASE_URL: '"./"'
    }),
    new VueLoaderPlugin()
  ]
}

```

完成打包编译后，发现页面正常显示，样式文件也生效了。

![](http://5coder.cn/img/1668473589_c90b0b463d6f3f77cf89fabea7b4ac61.png)

## 38.区分打包环境

尝试为不同的工作环境以创建不同的Webpack配置。创建不同的环境配置的方式主要有两种：

- 第一种是在配置文件中添加相应的配置判断条件，根据环境的判断条件的不同导出不同的配置。

  Webpack配置文件支持导出函数，函数中返回所需要的的配置对象，函数接受两个参数，第一个是env（cli传递的环境名参数），第二个是argv（运行cli过程中传递的所有参数）。可以借助这样一个特点来去实现不同的开发环境和生产环境分别返回不同的配置。

  ```js
  const Webpack = require('Webpack')
  const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
  const HtmlWebpackPlugin = require('html-Webpack-plugin')
  const CopyWebpackPlugin = require('copy-Webpack-plugin')
  
  module.exports = (env, argv) => {
    const config = {
      mode: 'development',
      entry: './src/main.js',
      output: {
        filename: 'js/bundle.js'
      },
      devtool: 'cheap-eval-module-source-map',
      devServer: {
        hot: true,
        contentBase: 'public'
      },
      module: {
        rules: [
          {
            test: /\.css$/,
            use: [
              'style-loader',
              'css-loader'
            ]
          },
          {
            test: /\.(png|jpe?g|gif)$/,
            use: {
              loader: 'file-loader',
              options: {
                outputPath: 'img',
                name: '[name].[ext]'
              }
            }
          }
        ]
      },
      plugins: [
        new HtmlWebpackPlugin({
          title: 'Webpack Tutorial',
          template: './src/index.html'
        }),
        new Webpack.HotModuleReplacementPlugin()
      ]
    }
  
    if (env === 'production') {
      config.mode = 'production'
      config.devtool = false
      config.plugins = [
        ...config.plugins,  // ES6将几个数组组合起来，生产环境下需要clean-Webpack-plugin和copy-Webpack-plugin
        new CleanWebpackPlugin(),
        new CopyWebpackPlugin(['public'])
      ]
    }
    return config
  }
  
  ```

  命令行运行：yarn Webpack，当没有传递env参数时，Webpack会默认mode为开发阶段（development），对应的public下的文件不会被复制。

  命令行运行：yarn Webpack --env production，传递env参数后，Webpack以生产环境（production）进行打包，额外的插件会工作，public目录下的文件会被复制。

  这就是通过在导出函数中对环境进行判断，从而去实现为不同的环境倒出不同的配置，当然也可以直接在全局去判断环境变量，然后直接导出不同的配置，这样也是可以的。

- 第二种是为不同的环境单独添加一个配置文件，确保每一个环境下面都会有一个对应的配置文件。

  通过判断环境参数数据返回不同的配对象，这种方式只适用于中小型项目。因为一旦项目变得复杂，配置文件也会一起变得复杂起来，所以说对于大型的项目，还是建议大家使用不同环境去对应不同配置文件的方式来实现。一般在这种方式下面，项目当中至少会有三个Webpack配置文件，其中两个（Webpack.dev.js/Webpack.prod.js）是用来适配不同的环境的，那另外一个是一个公共的配置(Webpack.common.js)。因为开发环境和生产环境并不是所有的配置都完全不同，所以说需要一个公共的文件来去抽象两者之间相同的配置。

  项目目录：

  ![image-20210106222819337](https://img-blog.csdnimg.cn/img_convert/c190385f1777089a4fcff11e656b2b29.png)

  Webpack.common.js

  ```js
  const HtmlWebpackPlugin = require('html-Webpack-plugin')
  
  module.exports = {
    entry: './src/main.js',
    output: {
      filename: 'js/bundle.js'
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            'style-loader',
            'css-loader'
          ]
        },
        {
          test: /\.(png|jpe?g|gif)$/,
          use: {
            loader: 'file-loader',
            options: {
              outputPath: 'img',
              name: '[name].[ext]'
            }
          }
        }
      ]
    },
    plugins: [
      new HtmlWebpackPlugin({
        title: 'Webpack Tutorial',
        template: './src/index.html'
      })
    ]
  }
  
  ```

  Webpack.dev.js

  ```js
  const Webpack = require('Webpack')
  const merge = require('Webpack-merge')
  const common = require('./Webpack.common')
  
  module.exports = merge(common, {
    mode: 'development',
    devtool: 'cheap-eval-module-source-map',
    devServer: {
      hot: true,
      contentBase: 'public'
    },
    plugins: [
      new Webpack.HotModuleReplacementPlugin()
    ]
  })
  ```

  Webpack.prod.js

  ```js
  const merge = require('Webpack-merge')
  const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
  const CopyWebpackPlugin = require('copy-Webpack-plugin')
  const common = require('./Webpack.common')
  
  module.exports = merge(common, {
    mode: 'production',
    plugins: [
      new CleanWebpackPlugin(),
      new CopyWebpackPlugin(['public'])
    ]
  })
  ```

  Webpack-merge提供了更加智能的配置合并，使用yarn add Webpack-merge --dev安装到生产环境中。将common中的配置分别于dev和prod组合，生产新的配置。

  命令行运行

  ```shell
  yarn Webpack --config Webpack.prod.js  # --config用于指定配置文件
  # 或者 yarn Webpack --config Webpack.dev.js
  ```

  如果觉得使用命令行太过麻烦，也可以在package.json进行配置

  ```js
    "scripts": {
      "prod": "Webpack --config Webpack.prod.js",
      "dev": "Webpack --config Webpack.dev.js"
    },
  ```

  随后命令行运行

  ```shell
  yarn prod  # 或者yarn dev
  ```


## 39.合并生产环境配置

代码目录如下：

![](D:/media/202211/2022-11-16_083157_7965410.4980056499150869.png)

通过`package.json`中的`scripts`命令，指定`webpac`k打包的配置文件（build、build2）。

```json
{
  "name": "02_Webpack_config_start",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "Webpack",
    "serve": "Webpack serve",
    "build2": "Webpack --config ./config/Webpack.common.js --env production",
    "serve2": "Webpack serve --config ./config/Webpack.common.js --env development"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@babel/cli": "^7.14.8",
    "@babel/core": "^7.15.0",
    "@babel/plugin-transform-arrow-functions": "^7.14.5",
    "@babel/plugin-transform-block-scoping": "^7.14.5",
    "@babel/preset-env": "^7.15.0",
    "@babel/preset-react": "^7.14.5",
    "@pmmmwh/react-refresh-Webpack-plugin": "^0.4.3",
    "autoprefixer": "^10.3.1",
    "axios": "^0.21.1",
    "babel-loader": "^8.2.2",
    "clean-Webpack-plugin": "^4.0.0-alpha.0",
    "copy-Webpack-plugin": "^9.0.1",
    "css-loader": "^6.2.0",
    "html-Webpack-plugin": "^5.3.2",
    "less": "^4.1.1",
    "less-loader": "^10.0.1",
    "postcss": "^8.3.6",
    "postcss-cli": "^8.3.1",
    "postcss-loader": "^6.1.1",
    "postcss-preset-env": "^6.7.0",
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-refresh": "^0.10.0",
    "react-router-dom": "^5.2.0",
    "style-loader": "^3.2.1",
    "Webpack": "^5.47.1",
    "Webpack-cli": "^4.7.2",
    "Webpack-dev-server": "^3.11.2",
    "Webpack-merge": "^5.8.0"
  },
  "dependencies": {
    "core-js": "^3.16.0",
    "express": "^4.17.1",
    "regenerator-runtime": "^0.13.9",
    "Webpack-dev-middleware": "^5.0.0"
  }
}

```

**paths.js**

```js
const path = require('path')

const appDir = process.cwd()

const resolveApp = (relativePath) => {
  return path.resolve(appDir, relativePath)
}

module.exports = resolveApp

```

**Webpack.common.js**

```js
const resolveApp = require('./paths')
const HtmlWebpackPlugin = require('html-Webpack-plugin')
const { merge } = require('Webpack-merge')

// 导入其它的配置
const prodConfig = require('./Webpack.prod')
const devConfig = require('./Webpack.dev')

// 定义对象保存 base 配置信息
const commonConfig = {
  entry: './src/index.js',  // 反而没有报错（ 相对路径 ）
  resolve: {
    extensions: [".js", ".json", '.ts', '.jsx', '.vue'],
    alias: {
      '@': resolveApp('./src')
    }
  },
  output: {
    filename: 'js/main.js',
    path: resolveApp('./dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {
          filename: 'font/[name].[hash:3][ext]'
        }
      },
      {
        test: /\.jsx?$/,
        use: ['babel-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'copyWebpackPlugin',
      template: './public/index.html'
    })
  ]
}

module.exports = (env) => {
  const isProduction = env.production

  // 依据当前的打包模式来合并配置
  const config = isProduction ? prodConfig : devConfig

  const mergeConfig = merge(commonConfig, config)

  return mergeConfig
}
```

**Webpack.dev.js**

```js
const path = require('path')
const CopyWebpackPlugin = require('copy-Webpack-plugin')
const { DefinePlugin } = require('Webpack')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')
const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-Webpack-plugin')



module.exports = (env) => {
  const isProduction = env.production
  return {
    mode: 'development',
    devtool: false,
    entry: './src/index.js',
    resolve: {
      extensions: [".js", ".json", '.ts', '.jsx', '.vue'],
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    output: {
      filename: 'js/main.js',
      path: path.resolve(__dirname, 'dist')
    },
    target: 'web',
    devServer: {
      hot: true,
      hotOnly: true,
      port: 4000,
      open: false,
      compress: true,
      historyApiFallback: true,
      proxy: {
        '/api': {
          target: 'https://api.github.com',
          pathRewrite: { "^/api": "" },
          changeOrigin: true
        }
      }
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            'style-loader',
            {
              loader: 'css-loader',
              options: {
                importLoaders: 1,
                esModule: false
              }
            },
            'postcss-loader'
          ]
        },
        {
          test: /\.less$/,
          use: [
            'style-loader',
            'css-loader',
            'postcss-loader',
            'less-loader'
          ]
        },
        {
          test: /\.(png|svg|gif|jpe?g)$/,
          type: 'asset',
          generator: {
            filename: "img/[name].[hash:4][ext]"
          },
          parser: {
            dataUrlCondition: {
              maxSize: 30 * 1024
            }
          }
        },
        {
          test: /\.(ttf|woff2?)$/,
          type: 'asset/resource',
          generator: {
            filename: 'font/[name].[hash:3][ext]'
          }
        },
        {
          test: /\.jsx?$/,
          use: ['babel-loader']
        }
      ]
    },
    plugins: [
      new CleanWebpackPlugin(),
      new HtmlWebpackPlugin({
        title: 'copyWebpackPlugin',
        template: './public/index.html'
      }),
      new DefinePlugin({
        BASE_URL: '"./"'
      }),
      new CopyWebpackPlugin({
        patterns: [
          {
            from: 'public',
            globOptions: {
              ignore: ['**/index.html']
            }
          }
        ]
      }),
      new ReactRefreshWebpackPlugin()
    ]
  }
}
```

**Webpack.prod.js**

```js
const CopyWebpackPlugin = require('copy-Webpack-plugin')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')

module.exports = {
  mode: 'production',
  plugins: [
    new CleanWebpackPlugin(),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'public',
          globOptions: {
            ignore: ['**/index.html']
          }
        }
      ]
    })
  ]
}
```


## 40.合并开发环境配置

代码目录结构如下：

![](D:/media/202211/2022-11-16_083724_5479610.34202323107310295.png)

同样通过`package.json`中的`scripts`指定`Webpack`配置文件

**package.json**

```json
{
  "name": "02_Webpack_config_start",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "Webpack",
    "serve": "Webpack serve",
    "build2": "Webpack --config ./config/Webpack.common.js --env production",
    "serve2": "Webpack serve --config ./config/Webpack.common.js --env development"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@babel/cli": "^7.14.8",
    "@babel/core": "^7.15.0",
    "@babel/plugin-transform-arrow-functions": "^7.14.5",
    "@babel/plugin-transform-block-scoping": "^7.14.5",
    "@babel/preset-env": "^7.15.0",
    "@babel/preset-react": "^7.14.5",
    "@pmmmwh/react-refresh-Webpack-plugin": "^0.4.3",
    "autoprefixer": "^10.3.1",
    "axios": "^0.21.1",
    "babel-loader": "^8.2.2",
    "clean-Webpack-plugin": "^4.0.0-alpha.0",
    "copy-Webpack-plugin": "^9.0.1",
    "css-loader": "^6.2.0",
    "html-Webpack-plugin": "^5.3.2",
    "less": "^4.1.1",
    "less-loader": "^10.0.1",
    "postcss": "^8.3.6",
    "postcss-cli": "^8.3.1",
    "postcss-loader": "^6.1.1",
    "postcss-preset-env": "^6.7.0",
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-refresh": "^0.10.0",
    "react-router-dom": "^5.2.0",
    "style-loader": "^3.2.1",
    "Webpack": "^5.47.1",
    "Webpack-cli": "^4.7.2",
    "Webpack-dev-server": "^3.11.2",
    "Webpack-merge": "^5.8.0"
  },
  "dependencies": {
    "core-js": "^3.16.0",
    "express": "^4.17.1",
    "regenerator-runtime": "^0.13.9",
    "Webpack-dev-middleware": "^5.0.0"
  }
}

```

**paths.js**

```js
const path = require('path')

const appDir = process.cwd()

const resolveApp = (relativePath) => {
  return path.resolve(appDir, relativePath)
}

module.exports = resolveApp

```

**Webpack.common.js**

```js
const resolveApp = require('./paths')
const HtmlWebpackPlugin = require('html-Webpack-plugin')
const { merge } = require('Webpack-merge')

// 导入其它的配置
const prodConfig = require('./Webpack.prod')
const devConfig = require('./Webpack.dev')

// 定义对象保存 base 配置信息
const commonConfig = {
  entry: './src/index.js',  // 反而没有报错（ 相对路径 ）
  resolve: {
    extensions: [".js", ".json", '.ts', '.jsx', '.vue'],
    alias: {
      '@': resolveApp('./src')
    }
  },
  output: {
    filename: 'js/main.js',
    path: resolveApp('./dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {
          filename: 'font/[name].[hash:3][ext]'
        }
      },
      {
        test: /\.jsx?$/,
        use: ['babel-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'copyWebpackPlugin',
      template: './public/index.html'
    })
  ]
}

module.exports = (env) => {
  const isProduction = env.production

  process.env.NODE_ENV = isProduction ? 'production' : 'development'

  // 依据当前的打包模式来合并配置
  const config = isProduction ? prodConfig : devConfig

  const mergeConfig = merge(commonConfig, config)

  return mergeConfig
}
```

**Webpack.dev.js**

```js
const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-Webpack-plugin')

module.exports = {
  mode: 'development',
  devtool: 'cheap-module-source-map',
  target: 'web',
  devServer: {
    hot: true,
    hotOnly: true,
    port: 4000,
    open: false,
    compress: true,
    historyApiFallback: true,
    proxy: {
      '/api': {
        target: 'https://api.github.com',
        pathRewrite: { "^/api": "" },
        changeOrigin: true
      }
    }
  },
  plugins: [
    new ReactRefreshWebpackPlugin()
  ]
}
```

**Webpack.prod.js**

```js
const CopyWebpackPlugin = require('copy-Webpack-plugin')
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')

module.exports = {
  mode: 'production',
  plugins: [
    new CleanWebpackPlugin(),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'public',
          globOptions: {
            ignore: ['**/index.html']
          }
        }
      ]
    })
  ]
}
```

**babel.config.js**

```js
const presets = [
  ['@babel/preset-env'],
  ['@babel/preset-react'],
]

const plugins = []

console.log(process.env.NODE_ENV, '<------')

// 依据当前的打包模式来决定plugins 的值 
const isProduction = process.env.NODE_ENV === 'production'
if (!isProduction) {
  plugins.push(['react-refresh/babel'])
}

module.exports = {
  presets,
  plugins
}
```

## 41.代码拆分方式

通过Webpack实现前端项目整体模块化的优势很明显，但是它同样存在一些弊端，那就是项目当中所有的代码最终都会被打包到一起，试想一下，如果说应用非常复杂，模块非常多的话，那打包结果就会特别的大，很多时候超过两三兆也是非常常见的事情。而事实情况是，大多数时候在应用开始工作时，并不是所有的模块都是必须要加载进来的，但是，这些模块又被全部打包到一起，需要任何一个模块，都必须得把整体加载下来过后才能使用。而应用一般又是运行在浏览器端，这就意味着会浪费掉很多的流量和带宽。

更为合理的方案就是把的打包结果按照一定的规则去分离到多个`bundle.js`当中，然后根据应用的运行需要，按需加载这些模块，这样的话就可以大大提高应用的响应速度以及它的运行效率。可能有人会想起来在一开始的时候说过Webpack就是把项目中散落的那些模块合并到一起，从而去提高运行效率，那这里又在说它应该把它分离开，这两个说法是不是自相矛盾？其实这并不是矛盾，只是物极必反而已，**资源太大了也不行，太碎了更不行**，项目中划分的这种模块的颗粒度一般都会非常的细，很多时候一个模块只是提供了一个小小的工具函数，它并不能形成一个完整的功能单元，如果不把这些散落的模块合并到一起，就有可能再去运行一个小小的功能时，会加载非常多的模块。而目前所主流的这种HTTP1.1协议，它本身就有很多缺陷，例如并不能同时对同一个域名下发起很多次的并行请求，而且每一次请求都会有一定的延迟，另外每次请求除了传输具体的内容以外，还会有额外的header请求头和响应头，当大量的这种请求的情况下，这些请求头加在一起，也是很大的浪费。

综上所述，模块打包肯定是有必要的，不过像应用越来越大过后，要开始慢慢的学会变通。为了解决这样的问题，**Webpack支持一种分包的功能，也可以把这种功能称之为代码分割，它通过把模块，按照所设计的一个规则打包到不同的bundle.js当中，从而去提高应用的响应速度，目前的Webpack去实现分包的方式主要有两种：**

- 第一种就是根据业务去配置不同的打包入口，也就是会有同时多个打包入口同时打包，这时候就会输出多个打包结果；

- 第二种是多入口文件，单独打包依赖包的形式；

- 第三种就是采用ES Module的动态导入的功能，去实现模块的按需加载，这个时候Webpack会自动的把动态导入的这个模块单独输出的一个bundle.js当中。

### 41.1 多入口文件打包

多入口打包一般适用于传统的“多页”应用程序。最常见的划分规则是一个页面对应一个打包入口，对于不同页面之间公共的部分再去提取到公共的结果中。

目录结构

![](http://5coder.cn/img/1668693399_f1ae678365103e2f9d491c815f3d4209.png)

一般Webpack.config.js配置文件中的entry属性只会一个文件路径（打包入口），如果需要配置多个打包入口，则需要将entry属性定义成为一个对象（注**意不是数组，如果是数组的话，那就是将多个文件打包到一起，对于整个应用来讲依然是一个入口**）。一旦配置为多入口，输出的文件名也需要修改**"[name].bundle.js**"，[name]最终会被替换成入口的名称，也就是index和album。

```js
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')

module.exports = {
  mode: 'none',
  entry: {
    index: './src/index.js',  // 多入口
    album: './src/album.js'
  },
  output: {
    filename: '[name].bundle.js'  // [name]占位符，最终被替换为入口名称index和album
  },
  optimization: {
    splitChunks: {
      // 自动提取所有公共模块到单独 bundle
      chunks: 'all'
    }
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/index.html',
      filename: 'index.html',
    }),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/album.html',
      filename: 'album.html',
    })
  ]
}
```

命令行运行yarn Webpack命令，打开dist目录发现已经有两个js文件。

### 41.2 多入口依赖包单独打包

多入口打包本身非常容易理解，也非常容易使用，但是它也存在一个小小的问题，就是在不同的打包入口当中，它一定会有那么一些公共的部分，按照目前这种多入口的打包方式，不同的打包结果当中就会出现相同的模块，例如在我们这里index入口和album入口当中就共同使用了global.css和fetch.js这两个公共的模块，因为实例比较简单，所以说重复的影响不会有那么大，但是如果共同使用的是jQuery或者Vue这种体积比较大的模块，那影响的话就会特别的大，所以说需要把这些公共的模块去。提取到一个单独的bundle.js当中，Webpack中实现公共模块提取的方式也非常简单，只需要在优化配置当中去开启一个叫splitChunks的一个功能就可以了，回到配置文件当中，配置如下：

```js
const { CleanWebpackPlugin } = require('clean-Webpack-plugin')
const HtmlWebpackPlugin = require('html-Webpack-plugin')

module.exports = {
  mode: 'none',
  entry: {
    index: './src/index.js',
    album: './src/album.js'
    // 或者使用下面的写法
    // index: { import : './src/index.js', dependOn: 'shared' },
    // album: { import : './src/album.js', dependOn: 'shared' },
    // shared: ['jquery', 'lodash']
  },
  output: {
    filename: '[name].bundle.js'
  },
  optimization: {
    splitChunks: {
      // 自动提取所有公共模块到单独 bundle
      chunks: 'all'  // 表示会把所有的公共模块都提取到单独的bundle.js当中
    }
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/index.html',
      filename: 'index.html',
      chunks: ['index']
    }),
    new HtmlWebpackPlugin({
      title: 'Multi Entry',
      template: './src/album.html',
      filename: 'album.html',
      chunks: ['album']
    })
  ]
}
```

打开命令行运行yarn Webpack后发现，公共模块的部分被打包进album~index.bundle.js中去了。

### 41.3 动态导入的形式打包

按需加载是开发浏览器应用当中一个非常常见的需求，一般常说的按需加载指的是加载数据，这里所说的按需加载指的是在应用运行过程中需要某个模块时才去加载这个模块，这种方式可以极大的节省**带宽和流量**。Webpack支持使用动态导入的这种方式来去实现模块的按需加载，而且所有动态导入的模块都会被自动提取到单独的bundle.js当中，从而实现分包，相比于**多入口**的方式，动态导入更为灵活，因为通过代码的逻辑去控制，需不需要加载某个模块，或者是时候加的某个模块。而分包的目的中就有很重要的一点就是：让模块实现按需加载，从而去提高应用的响应速度。

具体来看如何使用，这里已经提前设计好了一个可以发挥按需加载作用的场景，在这个页面的主体区域，如果访问的是文章页的话，得到的就是一个文章列表，如果访问的是相册页，显示的就是相册列表。

项目目录：

![](http://5coder.cn/img/1668693691_8fc97aa5f5a1d482e70e11ae86826b41.png)

动态导入使用的就是ESM标准当中的动态导入，在需要动态导入组件的地方，通过这个函数导入指定的路径，这个方法返回的就是一个promise，promise的方法当中就可以拿到模块对象，由于网站是使用的默认导出，所以说这里需要去解构模块对象当中的default，然后把它放到post的这个变量当中，拿到这个成员过后，使用mainElement.appendChild(posts())创建页面元素，album组件也是如此。完成以后再次回到浏览器，此时页面仍然可以正常工作的。

```js
// import posts from './posts/posts'
// import album from './album/album'

const render = () => {
  const hash = window.location.hash || '#posts'
  console.log(hash)
  const mainElement = document.querySelector('.main')

  mainElement.innerHTML = ''

  if (hash === '#posts') {
    // mainElement.appendChild(posts())
    // 这个方法返回的就是一个promise，promise的方法当中就可以拿到模块对象，由于网站是使用的默认导出，所以说这里需要去解构模块对象当中的default，然后把它放到post的这个变量当中
    import('./posts/posts').then(({ default: posts }) => {
      mainElement.appendChild(posts())
    })
  } else if (hash === '#album') {
    // mainElement.appendChild(album())
    import('./album/album').then(({ default: album }) => {
      mainElement.appendChild(album())
    })
  }
}

render()

window.addEventListener('hashchange', render)
```

这时再回到开发工具当中，然后重新去运行打包，然后去看看此时打包的结果是什么样子的，打包结束，打开dist目录，此时dist目录下就会多出3个js文件，那这三个js文件，实际上就是由动态导入自动分包所产生的。这3个文件的分别是刚刚导入的两个模块index.js/album.js，以及这两个模块当中公共模块fetch.js。

![](http://5coder.cn/img/1668693735_0abaef9539abad0d157664b059ba6660.png)

动态导入整个过程无需配置任何一个地方，只需要按照ESM动态导入成员的方式去导入模块就可以，内部会自动处理分包和按需加载，如果说你使用的是单页应用开发框架，比如react或者Vue的话，在你项目当中的路由映射组件，就可以通过这种动态导入的方式实现**按需加载**。

## 42.splitchunks 配置

最初，chunks（以及内部导入的模块）是通过内部 Webpack 图谱中的父子关系关联的。`CommonsChunkPlugin` 曾被用来避免他们之间的重复依赖，但是不可能再做进一步的优化。

从 Webpack v4 开始，移除了 `CommonsChunkPlugin`，取而代之的是 `optimization.splitChunks`。

### 默认值

开箱即用的 `SplitChunksPlugin` 对于大部分用户来说非常友好。

默认情况下，它只会影响到按需加载的 chunks，因为修改 initial chunks 会影响到项目的 HTML 文件中的脚本标签。

Webpack 将根据以下条件自动拆分 chunks：

- 新的 chunk 可以被共享，或者模块来自于 `node_modules` 文件夹
- 新的 chunk 体积大于 20kb（在进行 min+gz 之前的体积）
- 当按需加载 chunks 时，并行请求的最大数量小于或等于 30
- 当加载初始化页面时，并发请求的最大数量小于或等于 30

当尝试满足最后两个条件时，最好使用较大的 chunks。

### 配置

Webpack 为希望对该功能进行更多控制的开发者提供了一组选项。

> 选择了默认配置为了符合 Web 性能最佳实践，但是项目的最佳策略可能有所不同。如果要更改配置，则应评估所做更改的影响，以确保有真正的收益。

### optimization.splitChunks

下面这个配置对象代表 `SplitChunksPlugin` 的默认行为。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      chunks: 'async',
      minSize: 20000,
      minRemainingSize: 0,
      minChunks: 1,
      maxAsyncRequests: 30,
      maxInitialRequests: 30,
      enforceSizeThreshold: 50000,
      cacheGroups: {
        defaultVendors: {
          test: /[\\/]node_modules[\\/]/,
          priority: -10,
          reuseExistingChunk: true,
        },
        default: {
          minChunks: 2,
          priority: -20,
          reuseExistingChunk: true,
        },
      },
    },
  },
};
```

> 当 Webpack 处理文件路径时，它们始终包含 Unix 系统中的 `/` 和 Windows 系统中的 `\`。这就是为什么在 `{cacheGroup}.test` 字段中使用 `[\\/]` 来表示路径分隔符的原因。`{cacheGroup}.test` 中的 `/` 或 `\` 会在跨平台使用时产生问题。

> 从 Webpack 5 开始，不再允许将 entry 名称传递给 `{cacheGroup}.test` 或者为 `{cacheGroup}.name` 使用现有的 chunk 的名称。

#### splitChunks.automaticNameDelimiter

```
string = '~'
```

默认情况下，Webpack 将使用 chunk 的来源和名称生成名称（例如 `vendors~main.js`）。此选项使你可以指定用于生成名称的分隔符。

#### splitChunks.chunks

```
string = 'async'` `function (chunk)
```

这表明将选择哪些 chunk 进行优化。当提供一个字符串，有效值为 `all`，`async` 和 `initial`。设置为 `all` 可能特别强大，因为这意味着 chunk 可以在异步和非异步 chunk 之间共享。

Note that it is applied to the fallback cache group as well (`splitChunks.fallbackCacheGroup.chunks`).

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      // include all types of chunks
      chunks: 'all',
    },
  },
};
```

或者，你也可以提供一个函数去做更多的控制。这个函数的返回值将决定是否包含每一个 chunk。

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      chunks(chunk) {
        // exclude `my-excluded-chunk`
        return chunk.name !== 'my-excluded-chunk';
      },
    },
  },
};
```

你可以将此配置与 [HtmlWebpackPlugin](https://Webpack.docschina.org/plugins/html-Webpack-plugin/) 结合使用。它将为你注入所有生成的 vendor chunks。

#### splitChunks.maxAsyncRequests

```
number = 30
```

按需加载时的最大并行请求数。

#### splitChunks.maxInitialRequests

```
number = 30
```

入口点的最大并行请求数。

#### splitChunks.defaultSizeTypes

```
[string] = ['javascript', 'unknown']
```

Sets the size types which are used when a number is used for sizes.

#### splitChunks.minChunks

```
number = 1
```

拆分前必须共享模块的最小 chunks 数。

#### splitChunks.hidePathInfo

```
boolean
```

为由 maxSize 分割的部分创建名称时，阻止公开路径信息。

#### splitChunks.minSize

```
number = 20000` `{ [index: string]: number }
```

生成 chunk 的最小体积（以 bytes 为单位）。

#### splitChunks.minSizeReduction

```
number` `{ [index: string]: number }
```

生成 chunk 所需的主 chunk（bundle）的最小体积（以字节为单位）缩减。这意味着如果分割成一个 chunk 并没有减少主 chunk（bundle）的给定字节数，它将不会被分割，即使它满足 `splitChunks.minSize`。

> 为了生成 chunk，`splitChunks.minSizeReduction` 与 `splitChunks.minSize` 都需要被满足。

#### splitChunks.enforceSizeThreshold

#### `splitChunks.cacheGroups.{cacheGroup}.enforceSizeThreshold`

```
number = 50000
```

强制执行拆分的体积阈值和其他限制（minRemainingSize，maxAsyncRequests，maxInitialRequests）将被忽略。

#### splitChunks.minRemainingSize

#### `splitChunks.cacheGroups.{cacheGroup}.minRemainingSize`

```
number = 0
```

在 Webpack 5 中引入了 `splitChunks.minRemainingSize` 选项，通过确保拆分后剩余的最小 chunk 体积超过限制来避免大小为零的模块。 ['development' 模式](https://Webpack.docschina.org/configuration/mode/#mode-development) 中默认为 `0`。对于其他情况，`splitChunks.minRemainingSize` 默认为 `splitChunks.minSize` 的值，因此除需要深度控制的极少数情况外，不需要手动指定它。

> `splitChunks.minRemainingSize` 仅在剩余单个 chunk 时生效。

#### splitChunks.layer

#### `splitChunks.cacheGroups.{cacheGroup}.layer`

```
RegExp` `string` `function
```

按模块层将模块分配给缓存组。

#### splitChunks.maxSize

```
number = 0
```

使用 `maxSize`（每个缓存组 `optimization.splitChunks.cacheGroups[x].maxSize` 全局使用 `optimization.splitChunks.maxSize` 或对后备缓存组 `optimization.splitChunks.fallbackCacheGroup.maxSize` 使用）告诉 Webpack 尝试将大于 `maxSize` 个字节的 chunk 分割成较小的部分。 这些较小的部分在体积上至少为 `minSize`（仅次于 `maxSize`）。 该算法是确定性的，对模块的更改只会产生局部影响。这样，在使用长期缓存时就可以使用它并且不需要记录。`maxSize` 只是一个提示，当模块大于 `maxSize` 或者拆分不符合 `minSize` 时可能会被违反。

当 chunk 已经有一个名称时，每个部分将获得一个从该名称派生的新名称。 根据 `optimization.splitChunks.hidePathInfo` 的值，它将添加一个从第一个模块名称或其哈希值派生的密钥。

`maxSize` 选项旨在与 HTTP/2 和长期缓存一起使用。它增加了请求数量以实现更好的缓存。它还可以用于减小文件大小，以加快二次构建速度。



> `maxSize` 比 `maxInitialRequest/maxAsyncRequests` 具有更高的优先级。实际优先级是 `maxInitialRequest/maxAsyncRequests < maxSize < minSize`。



> 设置 `maxSize` 的值会同时设置 `maxAsyncSize` 和 `maxInitialSize` 的值。

#### splitChunks.maxAsyncSize

```
number
```

像 `maxSize` 一样，`maxAsyncSize` 可以为 cacheGroups（`splitChunks.cacheGroups.{cacheGroup}.maxAsyncSize`）或 fallback 缓存组（`splitChunks.fallbackCacheGroup.maxAsyncSize` ）全局应用（`splitChunks.maxAsyncSize`）

`maxAsyncSize` 和 `maxSize` 的区别在于 `maxAsyncSize` 仅会影响按需加载 chunk。

#### splitChunks.maxInitialSize

```
number
```

像 `maxSize` 一样，`maxInitialSize` 可以对 cacheGroups（`splitChunks.cacheGroups.{cacheGroup}.maxInitialSize`）或 fallback 缓存组（`splitChunks.fallbackCacheGroup.maxInitialSize`）全局应用（splitChunks.maxInitialSize）。

`maxInitialSize` 和 `maxSize` 的区别在于 `maxInitialSize` 仅会影响初始加载 chunks。

#### splitChunks.name

```
boolean = false` `function (module, chunks, cacheGroupKey) => string` `string
```

每个 cacheGroup 也可以使用：`splitChunks.cacheGroups.{cacheGroup}.name`。

拆分 chunk 的名称。设为 `false` 将保持 chunk 的相同名称，因此不会不必要地更改名称。这是生产环境下构建的建议值。

提供字符串或函数使你可以使用自定义名称。指定字符串或始终返回相同字符串的函数会将所有常见模块和 vendor 合并为一个 chunk。这可能会导致更大的初始下载量并减慢页面加载速度。

如果你选择指定一个函数，则可能会发现 `chunk.name` 和 `chunk.hash` 属性（其中 `chunk` 是 `chunks` 数组的一个元素）在选择 chunk 名时特别有用。

如果 `splitChunks.name` 与 [entry point](https://Webpack.docschina.org/configuration/entry-context/#entry) 名称匹配，entry point 将被删除。

`splitChunks.cacheGroups.{cacheGroup}.name` can be used to move modules into a chunk that is a parent of the source chunk. For example, use `name: "entry-name"` to move modules into the `entry-name` chunk. You can also use on demand named chunks, but you must be careful that the selected modules are only used under this chunk.

**main.js**

```js
import _ from 'lodash';

console.log(_.join(['Hello', 'Webpack'], ' '));
```

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          // cacheGroupKey here is `commons` as the key of the cacheGroup
          name(module, chunks, cacheGroupKey) {
            const moduleFileName = module
              .identifier()
              .split('/')
              .reduceRight((item) => item);
            const allChunksNames = chunks.map((item) => item.name).join('~');
            return `${cacheGroupKey}-${allChunksNames}-${moduleFileName}`;
          },
          chunks: 'all',
        },
      },
    },
  },
};
```

使用以下 `splitChunks` 配置来运行 Webpack 也会输出一组公用组，其下一个名称为：`commons-main-lodash.js.e7519d2bb8777058fa27.js`（以哈希方式作为真实世界输出示例）。

在为不同的拆分 chunk 分配相同的名称时，所有 vendor 模块都放在一个共享的 chunk 中，尽管不建议这样做，因为这可能会导致下载更多代码。

#### splitChunks.usedExports

#### `splitChunks.cacheGroups{cacheGroup}.usedExports`

```
boolean = true
```

弄清哪些 export 被模块使用，以混淆 export 名称，省略未使用的 export，并生成有效的代码。 当它为 `true` 时：分析每个运行时使用的出口，当它为 `"global"` 时：分析所有运行时的全局 export 组合）。

#### splitChunks.cacheGroups

缓存组可以继承和/或覆盖来自 `splitChunks.*` 的任何选项。但是 `test`、`priority` 和 `reuseExistingChunk` 只能在缓存组级别上进行配置。将它们设置为 `false`以禁用任何默认缓存组。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        default: false,
      },
    },
  },
};
```

#### `splitChunks.cacheGroups.{cacheGroup}.priority`

```
number = -20
```

一个模块可以属于多个缓存组。优化将优先考虑具有更高 `priority`（优先级）的缓存组。默认组的优先级为负，以允许自定义组获得更高的优先级（自定义组的默认值为 `0`）。

#### `splitChunks.cacheGroups.{cacheGroup}.reuseExistingChunk`

```
boolean = true
```

如果当前 chunk 包含已从主 bundle 中拆分出的模块，则它将被重用，而不是生成新的模块。这可能会影响 chunk 的结果文件名。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        defaultVendors: {
          reuseExistingChunk: true,
        },
      },
    },
  },
};
```

#### `splitChunks.cacheGroups.{cacheGroup}.type`

```
function` `RegExp` `string
```

允许按模块类型将模块分配给缓存组。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        json: {
          type: 'json',
        },
      },
    },
  },
};
```

#### splitChunks.cacheGroups.test

#### `splitChunks.cacheGroups.{cacheGroup}.test`

```
function (module, { chunkGraph, moduleGraph }) => boolean` `RegExp` `string
```

控制此缓存组选择的模块。省略它会选择所有模块。它可以匹配绝对模块资源路径或 chunk 名称。匹配 chunk 名称时，将选择 chunk 中的所有模块。

为 `{cacheGroup}.test` 提供一个函数：

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        svgGroup: {
          test(module) {
            // `module.resource` contains the absolute path of the file on disk.
            // Note the usage of `path.sep` instead of / or \, for cross-platform compatibility.
            const path = require('path');
            return (
              module.resource &&
              module.resource.endsWith('.svg') &&
              module.resource.includes(`${path.sep}cacheable_svgs${path.sep}`)
            );
          },
        },
        byModuleTypeGroup: {
          test(module) {
            return module.type === 'javascript/auto';
          },
        },
      },
    },
  },
};
```

为了查看 `module` and `chunks` 对象中可用的信息，你可以在回调函数中放入 `debugger;` 语句。然后 [以调试模式运行 Webpack 构建](https://Webpack.docschina.org/contribute/debugging/#devtools) 检查 Chromium DevTools 中的参数。

向 `{cacheGroup}.test` 提供 `RegExp`：

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        defaultVendors: {
          // Note the usage of `[\\/]` as a path separator for cross-platform compatibility.
          test: /[\\/]node_modules[\\/]|vendor[\\/]analytics_provider|vendor[\\/]other_lib/,
        },
      },
    },
  },
};
```

#### `splitChunks.cacheGroups.{cacheGroup}.filename`

```
string` `function (pathData, assetInfo) => string
```

仅在初始 chunk 时才允许覆盖文件名。 也可以在 [`output.filename`](https://Webpack.docschina.org/configuration/output/#outputfilename) 中使用所有占位符。



也可以在 `splitChunks.filename` 中全局设置此选项，但是不建议这样做，如果 [`splitChunks.chunks`](https://Webpack.docschina.org/plugins/split-chunks-plugin/#splitchunkschunks) 未设置为 `'initial'`，则可能会导致错误。避免全局设置。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        defaultVendors: {
          filename: '[name].bundle.js',
        },
      },
    },
  },
};
```

若为函数，则：

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        defaultVendors: {
          filename: (pathData) => {
            // Use pathData object for generating filename string based on your requirements
            return `${pathData.chunk.name}-bundle.js`;
          },
        },
      },
    },
  },
};
```

通过提供以文件名开头的路径 `'js/vendor/bundle.js'`，可以创建文件夹结构。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        defaultVendors: {
          filename: 'js/[name]/bundle.js',
        },
      },
    },
  },
};
```

#### `splitChunks.cacheGroups.{cacheGroup}.enforce`

```
boolean = false
```

告诉 Webpack 忽略 [`splitChunks.minSize`](https://Webpack.docschina.org/plugins/split-chunks-plugin/#splitchunksminsize)、[`splitChunks.minChunks`](https://Webpack.docschina.org/plugins/split-chunks-plugin/#splitchunksminchunks)、[`splitChunks.maxAsyncRequests`](https://Webpack.docschina.org/plugins/split-chunks-plugin/#splitchunksmaxasyncrequests) 和 [`splitChunks.maxInitialRequests`](https://Webpack.docschina.org/plugins/split-chunks-plugin/#splitchunksmaxinitialrequests) 选项，并始终为此缓存组创建 chunk。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        defaultVendors: {
          enforce: true,
        },
      },
    },
  },
};
```

#### `splitChunks.cacheGroups.{cacheGroup}.idHint`

```
string
```

设置 chunk id 的提示。 它将被添加到 chunk 的文件名中。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        defaultVendors: {
          idHint: 'vendors',
        },
      },
    },
  },
};
```

### Examples

#### Defaults: Example 1

```js
// index.js

import('./a'); // dynamic import
// a.js
import 'react';

//...
```

**结果：** 将创建一个单独的包含 `react` 的 chunk。在导入调用中，此 chunk 并行加载到包含 `./a` 的原始 chunk 中。

为什么：

- 条件1：chunk 包含来自 `node_modules` 的模块
- 条件2：`react` 大于 30kb
- 条件3：导入调用中的并行请求数为 2
- 条件4：在初始页面加载时不影响请求

这背后的原因是什么？`react` 可能不会像你的应用程序代码那样频繁地更改。通过将其移动到单独的 chunk 中，可以将该 chunk 与应用程序代码分开进行缓存（假设你使用的是 chunkhash，records，Cache-Control 或其他长期缓存方法）。

#### Defaults: Example 2

```js
// entry.js

// dynamic imports
import('./a');
import('./b');
// a.js
import './helpers'; // helpers is 40kb in size

//...
// b.js
import './helpers';
import './more-helpers'; // more-helpers is also 40kb in size

//...
```

**结果：** 将创建一个单独的 chunk，其中包含 `./helpers` 及其所有依赖项。在导入调用时，此 chunk 与原始 chunks 并行加载。

为什么：

- 条件1：chunk 在两个导入调用之间共享
- 条件2：`helpers` 大于 30kb
- 条件3：导入调用中的并行请求数为 2
- 条件4：在初始页面加载时不影响请求

将 `helpers` 的内容放入每个 chunk 中将导致其代码被下载两次。通过使用单独的块，这只会发生一次。我们会进行额外的请求，这可以视为一种折衷。这就是为什么最小体积为 30kb 的原因。

#### Split Chunks: Example 1

创建一个 `commons` chunk，其中包括入口（entry points）之间所有共享的代码。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          name: 'commons',
          chunks: 'initial',
          minChunks: 2,
        },
      },
    },
  },
};
```



此配置可以扩大你的初始 bundles，建议在不需要立即使用模块时使用动态导入。

#### Split Chunks: Example 2

创建一个 `vendors` chunk，其中包括整个应用程序中 `node_modules` 的所有代码。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },
};
```



这可能会导致包含所有外部程序包的较大 chunk。建议仅包括你的核心框架和实用程序，并动态加载其余依赖项。

#### Split Chunks: Example 3

创建一个 `custom vendor` chunk，其中包含与 `RegExp` 匹配的某些 `node_modules` 包。

**Webpack.config.js**

```js
module.exports = {
  //...
  optimization: {
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'vendor',
          chunks: 'all',
        },
      },
    },
  },
};
```



这将导致将 `react` 和 `react-dom` 分成一个单独的 chunk。 如果你不确定 chunk 中包含哪些包，请参考 [Bundle Analysis](https://Webpack.docschina.org/guides/code-splitting/#bundle-analysis) 部分以获取详细信息。

## 43.import 动态导入配置

Webpack打包过程中利用动态导入的方式对代码进行拆包。之前使用`import './title'`的同步的方式进行导入，可以选择splitChunks选项进行配置。

![](http://5coder.cn/img/1668723845_28e60607e094c76ab2633c59f5091a08.png)

此时，我们更改导入的方式为异步导入，即使用`import('./title')`的方式进行导入，并且将splitChunks配置项删除，观察打包后的结果。

![](http://5coder.cn/img/1668723988_cf928cc7464dba0d4421496aae8ed187.png)

可以看到打包后的结果为`198.bundle.js`文件。这是Webpack自身就会配置好的属性，无需进行其他配置。基于这个特点，对其周边进行补充。

### 44.1 chunkIds

根据官网介绍，`chunkIds`有几个配置的值，这里只针对`natural`、`named`、`deterministic`进行测试。

> ## optimization.chunkIds
>
> ```
> boolean = false` `string: 'natural' | 'named' | 'size' | 'total-size' | 'deterministic'
> ```
>
> 告知 Webpack 当选择模块 id 时需要使用哪种算法。将 `optimization.chunkIds` 设置为 `false` 会告知 Webpack 没有任何内置的算法会被使用，但自定义的算法会由插件提供。`optimization.chunkIds` 的默认值是 `false`：
>
> - 如果环境是开发环境，那么 `optimization.chunkIds` 会被设置成 `'named'`，但当在生产环境中时，它会被设置成 `'deterministic'`
> - 如果上述的条件都不符合, `optimization.chunkIds` 会被默认设置为 `'natural'`
>
> 下述选项字符串值均为被支持：
>
> | 选项值            | 描述                                                         |
> | :---------------- | :----------------------------------------------------------- |
> | `'natural'`       | 按使用顺序的数字 id。                                        |
> | `'named'`         | 对调试更友好的可读的 id。                                    |
> | `'deterministic'` | 在不同的编译中不变的短数字 id。有益于长期缓存。在生产模式中会默认开启。 |
> | `'size'`          | 专注于让初始下载包大小更小的数字 id。                        |
> | `'total-size'`    | 专注于让总下载包大小更小的数字 id。                          |

#### 44.1.1 natural

> 按使用顺序的数字 id。一般不使用，在多个导入的过程中，例如同时导入了`title.js`和`a.js`，打包过后会生成`1.bundle.js`和`2.bundle.js`，但是当我们不再需要`title.js`时，再次进行打包，会生成`1.bundle.js`，这是浏览器就会存在缓存问题。

打包结果：![](http://5coder.cn/img/1668724297_ab7eb298dbef04db07877f9f98b353f0.png)

#### 44.1.2 named

> 对调试更友好的可读的 id。

![](http://5coder.cn/img/1668724505_b01c65ada36e259e5eed23f863e6d506.png)

这里很明确的知道src_title_js.bundle.js是title.js打包生成后的结果。对于开发阶段没有任何影响，但是对于生产阶段，就会并不需要进行任何调试，就不需要更好的阅读。

#### 44.1.3 deterministic

> 在不同的编译中不变的短数字 id。有益于长期缓存。在生产模式中会默认开启。

![](http://5coder.cn/img/1668724633_1d5bb6b68998aee02c5df43aaf763c21.png)

在设置`chunkIds`为`deterministic`时，发现就回到了最初的状态`198.bundle.js`，因为这是`Webpack5`中默认提供的。

### 44.2 chunkFilename

在动态导入中，还可以配置chunkFilename选项，对打包的结果进行重命名文件名。

![](http://5coder.cn/img/1668724770_d89488670fb8248962ef2fd34bd41381.png)

此时`js/chunk_[name].js`中的name与`js/chunk_[name]_[id].js`中的id指向的都是198。可以使用**魔法注释**的功能对打包结果的文件名进行重置。

![](http://5coder.cn/img/1668724898_98fd1a1fa4f17b19ba4370413f907288.png)

这样就可以很好的识别某个打包文件对应的源文件。

## 44.runtimeChunk 优化配置

针对`Webpack`中的`optimization`的优化过程中，还有一个`runtimeChunk`的配置。

> ## optimization.runtimeChunk
>
> ```
> object` `string` `boolean
> ```
>
> 将 `optimization.runtimeChunk` 设置为 `true` 或 `'multiple'`，会为每个入口添加一个只含有 runtime 的额外 chunk。此配置的别名如下：
>
> **Webpack.config.js**
>
> ```js
> module.exports = {
> //...
> optimization: {
>  runtimeChunk: {
>    name: (entrypoint) => `runtime~${entrypoint.name}`,
>  },
> },
> };
> ```
>
> 值 `"single"` 会创建一个在所有生成 chunk 之间共享的运行时文件。此设置是如下设置的别名：
>
> **Webpack.config.js**
>
> ```js
> module.exports = {
> //...
> optimization: {
>  runtimeChunk: {
>    name: 'runtime',
>  },
> },
> };
> ```
>
> 通过将 `optimization.runtimeChunk` 设置为 `object`，对象中可以设置只有 `name` 属性，其中属性值可以是名称或者返回名称的函数，用于为 runtime chunks 命名。
>
> 默认值是 `false`：每个入口 chunk 中直接嵌入 runtime。
>
> ###### Warning
>
> 对于每个 runtime chunk，导入的模块会被分别初始化，因此如果你在同一个页面中引用多个入口起点，请注意此行为。你或许应该将其设置为 `single`，或者使用其他只有一个 runtime 实例的配置。
>
> **Webpack.config.js**
>
> ```js
> module.exports = {
> //...
> optimization: {
>  runtimeChunk: {
>    name: (entrypoint) => `runtimechunk~${entrypoint.name}`,
>  },
> },
> };
> ```

runtimeChunk，直观翻译是运行时的chunk文件，其作用是啥呢，通过调研了解了一波，在此记录下。

### 44.1 何为运行时代码？

形如`import('abc').then(res=>{})`这种异步加载的代码，在Webpack中即为运行时代码。在VueCli工程中常见的异步加载路由即为runtime代码。

```js
{
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* WebpackChunkName: "about" */ '../views/About.vue')
    // component: About
  }
```

### 44.2 搭建工程测试功效

1、搭建简单的vue项目，使用vuecli新建一个只需要router的项目，脚手架默认路由配置了一个异步加载的about路由，如上图所示

2、不设置runtimeChunk时，查看打包文件，此时不需要做任何操作，因为其默认是false，直接yarn build，此时生成的主代码文件的hash值为`7d50fa23`。

![](http://5coder.cn/img/1668725819_27b73e8ac73091b2847687ca05099197.webp)

3、接着改变about.vue文件的内容，再次build，查看打包结果，发现app文件的hash值发生了变化。

![发现app文件的hash值发生了变化。](http://5coder.cn/img/1668725855_48efad691b8b5cd537d2915bc0037778.webp)

> 设置runtimeChunk是将包含`chunks 映射关系`的 list单独从 app.js里提取出来，因为每一个 chunk 的 id 基本都是基于内容 hash 出来的，所以每次改动都会影响它，如果不将它提取出来的话，等于app.js每次都会改变。缓存就失效了。设置runtimeChunk之后，Webpack就会生成一个个runtime~xxx.js的文件。
> 然后每次更改所谓的运行时代码文件时，打包构建时app.js的hash值是不会改变的。如果每次项目更新都会更改app.js的hash值，那么用户端浏览器每次都需要重新加载变化的app.js，如果项目大切优化分包没做好的话会导致第一次加载很耗时，导致用户体验变差。现在设置了runtimeChunk，就解决了这样的问题。所以`这样做的目的是避免文件的频繁变更导致浏览器缓存失效，所以其是更好的利用缓存。提升用户体验。`

4、新建vue.config.js，配置runtimeChunk，第一次打包，然后修改about，在打包一次，查看2次打包之后app文件的hash值的变化。

```java
// vue.config.js
module.exports = {
  productionSourceMap: false,
  configureWebpack: {
     runtimeChunk: true
  }
}
```

![](http://5coder.cn/img/1668725916_22246dec5670a904e996e01daa4d17d3.webp)

通过截图看到2次打包生成的app文件的hash值没有改变。和上面说的作用一致。

### 44.3 你以为这就完了？

1、查看下runtime~xxx.js文件内容:

```jsx
function a(e){return i.p+"js/"+({about:"about"}[e]||e)+"."+{about:"3cc6fa76"}[e]+".js"}f
```

发现文件很小，且就是加载chunk的依赖关系的文件。虽然每次构建后app的hash没有改变，但是runtime~xxx.js会变啊。每次重新构建上线后，浏览器每次都需要重新请求它，它的 http 耗时远大于它的执行时间了，所以建议不要将它单独拆包，而是将它内联到我们的 index.html 之中。这边我们使用[script-ext-html-Webpack-plugin](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fnumical%2Fscript-ext-html-Webpack-plugin)来实现。（也可使用html-Webpack-inline-source-plugin，其不会删除runtime文件。）

```js
// vue.config.js
const ScriptExtHtmlWebpackPlugin = require('script-ext-html-Webpack-plugin')
module.exports = {
  productionSourceMap: false,
  configureWebpack: {
    optimization: {
      runtimeChunk: true
    },
    plugins: [
      new ScriptExtHtmlWebpackPlugin({
        inline: /runtime~.+\.js$/  //正则匹配runtime文件名
      })
    ]
  },
  chainWebpack: config => {
    config.plugin('preload')
      .tap(args => {
        args[0].fileBlacklist.push(/runtime~.+\.js$/) //正则匹配runtime文件名，去除该文件的preload
        return args
      })
  }
}
```

重新打包，查看index.html文件

```html
<!DOCTYPE html>
<html lang=en>

<head>
    <meta charset=utf-8>
    <meta http-equiv=X-UA-Compatible content="IE=edge">
    <meta name=viewport content="width=device-width,initial-scale=1">
    <link rel=icon href=/favicon.ico>
    <title>runtime-chunk</title>
    <link href=/js/about.cccc71df.js rel=prefetch>
    <link href=/css/app.b087a504.css rel=preload as=style>
    <link href=/js/app.9f1ba6f7.js rel=preload as=script>
    <link href=/css/app.b087a504.css rel=stylesheet>
</head>

<body><noscript><strong>We're sorry but runtime-chunk doesn't work properly without JavaScript enabled. Please enable it
            to continue.</strong></noscript>
    <div id=app></div>
    <script>(function (e) { function r(r) { for (var n, a, i = r[0], c = r[1], l = r[2], f = 0, s = []; f < i.length; f++)a = i[f], Object.prototype.hasOwnProperty.call(o, a) && o[a] && s.push(o[a][0]), o[a] = 0; for (n in c) Object.prototype.hasOwnProperty.call(c, n) && (e[n] = c[n]); p && p(r); while (s.length) s.shift()(); return u.push.apply(u, l || []), t() } function t() { for (var e, r = 0; r < u.length; r++) { for (var t = u[r], n = !0, a = 1; a < t.length; a++) { var c = t[a]; 0 !== o[c] && (n = !1) } n && (u.splice(r--, 1), e = i(i.s = t[0])) } return e } var n = {}, o = { "runtime~app": 0 }, u = []; function a(e) { return i.p + "js/" + ({ about: "about" }[e] || e) + "." + { about: "cccc71df" }[e] + ".js" } function i(r) { if (n[r]) return n[r].exports; var t = n[r] = { i: r, l: !1, exports: {} }; return e[r].call(t.exports, t, t.exports, i), t.l = !0, t.exports } i.e = function (e) { var r = [], t = o[e]; if (0 !== t) if (t) r.push(t[2]); else { var n = new Promise((function (r, n) { t = o[e] = [r, n] })); r.push(t[2] = n); var u, c = document.createElement("script"); c.charset = "utf-8", c.timeout = 120, i.nc && c.setAttribute("nonce", i.nc), c.src = a(e); var l = new Error; u = function (r) { c.onerror = c.onload = null, clearTimeout(f); var t = o[e]; if (0 !== t) { if (t) { var n = r && ("load" === r.type ? "missing" : r.type), u = r && r.target && r.target.src; l.message = "Loading chunk " + e + " failed.\n(" + n + ": " + u + ")", l.name = "ChunkLoadError", l.type = n, l.request = u, t[1](l) } o[e] = void 0 } }; var f = setTimeout((function () { u({ type: "timeout", target: c }) }), 12e4); c.onerror = c.onload = u, document.head.appendChild(c) } return Promise.all(r) }, i.m = e, i.c = n, i.d = function (e, r, t) { i.o(e, r) || Object.defineProperty(e, r, { enumerable: !0, get: t }) }, i.r = function (e) { "undefined" !== typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }), Object.defineProperty(e, "__esModule", { value: !0 }) }, i.t = function (e, r) { if (1 & r && (e = i(e)), 8 & r) return e; if (4 & r && "object" === typeof e && e && e.__esModule) return e; var t = Object.create(null); if (i.r(t), Object.defineProperty(t, "default", { enumerable: !0, value: e }), 2 & r && "string" != typeof e) for (var n in e) i.d(t, n, function (r) { return e[r] }.bind(null, n)); return t }, i.n = function (e) { var r = e && e.__esModule ? function () { return e["default"] } : function () { return e }; return i.d(r, "a", r), r }, i.o = function (e, r) { return Object.prototype.hasOwnProperty.call(e, r) }, i.p = "/", i.oe = function (e) { throw console.error(e), e }; var c = window["WebpackJsonp"] = window["WebpackJsonp"] || [], l = c.push.bind(c); c.push = r, c = c.slice(); for (var f = 0; f < c.length; f++)r(c[f]); var p = l; t() })([]);</script>
    <script src=/js/chunk-vendors.1e5c55d3.js></script>
    <script src=/js/app.9f1ba6f7.js></script>
</body>
</html>
```

index.html中已经没有对runtime~xxx.js的引用了，而是直接将其代码写入到了index.html中，故不会在请求文件，减少http请求。

> runtimeChunk作用是为了线上更新版本时，充分利用浏览器缓存，使用户感知的影响到最低。

## 45.代码懒加载

https://www.jianshu.com/p/6fc86fa8ee81

模块懒加载本身与Webpack没有关系，Webpack可以让懒加载的模块代码打包到单独的文件中，实现真正的按需加载。Webpack会自动对异步代码进行分割。

示例代码如下：

```js
function getComponent() {
    return import(/* WebpackChunkName: "lodash" */ 'lodash').then(({default: _})=>{
        var element = document.createElement('div')
        element.innerHTML = _.join(['a','b'],'-')
        return element
    })
}

document.addEventListener('click', ()=>{
    getComponent().then(element => {
        document.body.appendChild(element)
    })
})
```

需要配置`@babel/preset-env`的`"useBuiltIns": "usage"`

```json
{
   "presets": [
     ["@babel/preset-env",{
       "targets": {
          "chrome": "67"
        },
        "useBuiltIns": "usage",
        "corejs": "3"
     }
     ],
     "@babel/preset-react"
   ],
    "plugins": [
      "@babel/plugin-syntax-dynamic-import"
    ]
}
```

执行打包指令，打包后的文件如下：

![](http://5coder.cn/img/1668913136_00d998d800383439c34c682cbb41dfc1.webp)

生成了vendors~lodash.js文件。
浏览器打开打包后的html文件，查看Network如下：

![](http://5coder.cn/img/1668913155_ba324a1f740faa748800e18eab034dc6.png)

点击后才会加载vendors~lodash.js

![12665637-7023b80413d6c86e](http://5coder.cn/img/1668913178_2890bba4f9d4fb1a88e2419d01c831e0.webp)

实现了模块按需加载。

**异步函数的方式：**

```js
async function getComponent(){
    const { default: _} = await import(/* WebpackChunkName: "lodash" */ 'lodash')
    const element = document.createElement('div')
    element.innerHTML = _.join(['a','b'],'-')
    return element
}


document.addEventListener('click', ()=>{
    getComponent().then(element => {
        document.body.appendChild(element)
    })
})
```

## 46.prefetch 与 preload

Webpack v4.6.0+ 增加了对预获取和预加载的支持。

在声明 import 时，使用下面这些内置指令，可以让 Webpack 输出 "resource hint(资源提示)"，来告知浏览器：

- **prefetch**(预获取)：将来某些导航下可能需要的资源
- **preload**(预加载)：当前导航下可能需要资源

下面这个 prefetch 的简单示例中，有一个 `HomePage` 组件，其内部渲染一个 `LoginButton` 组件，然后在点击后按需加载 `LoginModal` 组件。

**LoginButton.js**

```js
//...
import(/* WebpackPrefetch: true */ './path/to/LoginModal.js');
```

这会生成 `<link rel="prefetch" href="login-modal-chunk.js">` 并追加到页面头部，指示着浏览器在闲置时间预取 `login-modal-chunk.js` 文件。

> Tips:只要父 chunk 完成加载，Webpack 就会添加 prefetch hint(预取提示)。

与 prefetch 指令相比，preload 指令有许多不同之处：

- preload chunk 会在父 chunk 加载时，以并行方式开始加载。prefetch chunk 会在父 chunk 加载结束后开始加载。
- preload chunk 具有中等优先级，并立即下载。prefetch chunk 在浏览器闲置时下载。
- preload chunk 会在父 chunk 中立即请求，用于当下时刻。prefetch chunk 会用于未来的某个时刻。
- 浏览器支持程度不同。

下面这个简单的 preload 示例中，有一个 `Component`，依赖于一个较大的 library，所以应该将其分离到一个独立的 chunk 中。

我们假想这里的图表组件 `ChartComponent` 组件需要依赖一个体积巨大的 `ChartingLibrary` 库。它会在渲染时显示一个 `LoadingIndicator(加载进度条)` 组件，然后立即按需导入 `ChartingLibrary`：

**ChartComponent.js**

```js
//...
import(/* WebpackPreload: true */ 'ChartingLibrary');
```

在页面中使用 `ChartComponent` 时，在请求 ChartComponent.js 的同时，还会通过 `<link rel="preload">` 请求 charting-library-chunk。假定 page-chunk 体积比 charting-library-chunk 更小，也更快地被加载完成，页面此时就会显示 `LoadingIndicator(加载进度条)` ，等到 `charting-library-chunk` 请求完成，LoadingIndicator 组件才消失。这将会使得加载时间能够更短一点，因为只进行单次往返，而不是两次往返。尤其是在高延迟环境下。

> Tips：不正确地使用 `WebpackPreload` 会有损性能，请谨慎使用。

有时你需要自己控制预加载。例如，任何动态导入的预加载都可以通过异步脚本完成。这在流式服务器端渲染的情况下很有用。

```js
const lazyComp = () =>
  import('DynamicComponent').catch((error) => {
    // 在发生错误时做一些处理
    // 例如，我们可以在网络错误的情况下重试请求
  });
```

如果在 Webpack 开始加载该脚本之前脚本加载失败（如果该脚本不在页面上，Webpack 只是创建一个 script 标签来加载其代码），则该 catch 处理程序将不会启动，直到 [chunkLoadTimeout](https://www.Webpackjs.com/configuration/output/#outputchunkloadtimeout) 未通过。此行为可能是意料之外的。但这是可以解释的 - Webpack 不能抛出任何错误，因为 Webpack 不知道那个脚本失败了。Webpack 将在错误发生后立即将 onerror 处理脚本添加到 script 中。

为了避免上述问题，你可以添加自己的 onerror 处理脚本，将会在错误发生时移除该 script。

```html
<script
  src="https://example.com/dist/dynamicComponent.js"
  async
  onerror="this.remove()"
></script>
```

在这种情况下，错误的 script 将被删除。Webpack 将创建自己的 script，并且任何错误都将被处理而没有任何超时。

## 47.第三方扩展设置 CDN

### 47.1 什么是CDN

[传送门](https://zhuanlan.zhihu.com/p/52362950)

  cdn全称是内容分发网络。其目的是让用户能够更快速的得到请求的数据。简单来讲，cdn就是用来加速的，他能让用户就近访问数据，这样就更更快的获取到需要的数据。举个例子，现在服务器在北京，深圳的用户想要获取服务器上的数据就需要跨越一个很远的距离，这显然就比北京的用户访问北京的服务器速度要慢。但是现在我们在深圳建立一个cdn服务器，上面缓存住一些数据，深圳用户访问时先访问这个cdn服务器，如果服务器上有用户请求的数据就可以直接返回，这样速度就大大的提升了。

![](http://5coder.cn/img/1668915042_dade06d710e0267a4ef6aefd1102d101.gif)

**cdn的整个工作过程**![](http://5coder.cn/img/1668915002_6088ee87663e721bf73fee75512642be.png)

### 47.2 如何设置CDN

`Webpack`中我们引入一个不想被打包的第三方包，可能是由于该包的体积过大或者其他原因，这对与`Webpack`打包来说是有优势的，因为减少第三包的打包会提高`Webpack`打包的速度。比如在实际使用中，我们使用到了`lodash`第三方包，我们又没有自己的CDN服务器，这是就需要借助别人的`CDN`服务器进行对该包的引入（一般是官方的`CDN`服务）。

#### 47.2.1 有自己的CDN服务器

如果有自己的CDN服务器，我们可以在Webpack配置文件中的`output`中设置`publicPath`目录，其中写入`CDN`的服务器地址，如下：

![](http://5coder.cn/img/1668915516_f0840e7839e35d9847ae649b12e12830.png)

这样在打包过后，打开index.htm可以看到，我们对所有的资源都会从该CDN服务器下查找。

![](http://5coder.cn/img/1668915598_c32bedf4a7b76542aa0d8aed93e8961d.png)

#### 47.2.2 使用第三方资源官方的CDN服务

在Webpack官网中，可以看到，设置`externals`属性，可以选择我们不需要打包的第三方资源，具体配置如下：

**防止**将某些 `import` 的包(package)**打包**到 bundle 中，而是在运行时(runtime)再去从外部获取这些*扩展依赖(external dependencies)*。

例如，从 CDN 引入 [jQuery](https://jquery.com/)，而不是把它打包：

**index.html**

```html
<script
  src="https://code.jquery.com/jquery-3.1.0.js"
  integrity="sha256-slogkvB1K3VOkzAI8QITxV3VzpOnkeNVsKvtkYLMjfk="
  crossorigin="anonymous"
></script>
```

**Webpack.config.js**

```javascript
module.exports = {
  //...
  externals: {
    jquery: 'jQuery',
  },
};
```

这样就剥离了那些不需要改动的依赖模块，换句话，下面展示的代码还可以正常运行：

```javascript
import $ from 'jquery';

$('.my-element').animate(/* ... */);
```

上面 `Webpack.config.js` 中 `externals` 下指定的属性名称 `jquery` 表示 `import $ from 'jquery'` 中的模块 `jquery` 应该从打包产物中排除。 为了替换这个模块，`jQuery` 值将用于检索全局 `jQuery` 变量，因为默认的外部库类型是 `var`，请参阅 [externalsType](https://www.Webpackjs.com/configuration/externals/#externalstype)。

虽然我们在上面展示了一个使用外部全局变量的示例，但实际上可以以以下任何形式使用外部变量：全局变量、CommonJS、AMD、ES2015 模块，在 [externalsType](https://www.Webpackjs.com/configuration/externals/#externalstype) 中查看更多信息。

## 48.打包 Dll 库

在Webpack4往后或者Webpack5，本身其打包的速度已经足够优化，因此在高版本Vue脚手架、React脚手架中已经移除了DLL库的使用。 但是从打包内容的多少以及打包的速度上来讲，如果使用了DLL库，它的确可以提高构建速度。

### 48.1 DLL库是什么

`DllPlugin` 和 `DllReferencePlugin` 用某种方法实现了拆分 bundles，同时还大幅度提升了构建的速度。"DLL" 一词代表微软最初引入的动态链接库（有一些东西可以进行共享，共享的东西可以提前准备好，将其变为一个库。将来在不同的项目中，对其进行使用的时候，只需要将该库导入即可）。

### 48.2 打包DLL库

这里已React和React Dom为例。

项目目录以及package.json

![](http://5coder.cn/img/1668918984_0dcd78e5d8d2ae6a4a558f111765fa19.png)

`Webpack.config.js`

```js
const path = require('path')
const Webpack = require('Webpack')
const TerserPlugin = require('terser-Webpack-plugin')

module.exports = {
  mode: "production",
  entry: {
    react: ['react', 'react-dom']
  },
  output: {
    path: path.resolve(__dirname, 'dll'),
    filename: 'dll_[name].js',
    library: 'dll_[name]'
  },
  optimization: {
    minimizer: [
      new TerserPlugin({
        extractComments: false
      }),
    ],
  },
  plugins: [
    new Webpack.DllPlugin({
      name: 'dll_[name]',
      path: path.resolve(__dirname, './dll/[name].manifest.json')
    })
  ]
}
```

执行yarn dll后，发现dll目录中生成两个文件`dll_react`.js和`react.manifest.json`。其中在其他项目中使用该`dll`库时，会先引入`react.manifest.json`文件，根据其中的引用路径，再对应找到`js`文件进行打包。

![](http://5coder.cn/img/1668919197_eaa00481c828db00c57f305b7d81a9f7.png)

react.manifest.json

```json
{
  "name": "dll_react",
  "content": {
    "./node_modules/react/index.js": {
      "id": 294,
      "buildMeta": {
        "exportsType": "dynamic",
        "defaultObject": "redirect"
      },
      "exports": [
        "Children",
        "Component",
        "Fragment",
        "Profiler",
        "PureComponent",
        "StrictMode",
        "Suspense",
        "__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED",
        "cloneElement",
        "createContext",
        "createElement",
        "createFactory",
        "createRef",
        "forwardRef",
        "isValidElement",
        "lazy",
        "memo",
        "useCallback",
        "useContext",
        "useDebugValue",
        "useEffect",
        "useImperativeHandle",
        "useLayoutEffect",
        "useMemo",
        "useReducer",
        "useRef",
        "useState",
        "version"
      ]
    },
    "./node_modules/react-dom/index.js": {
      "id": 935,
      "buildMeta": {
        "exportsType": "dynamic",
        "defaultObject": "redirect"
      },
      "exports": [
        "__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED",
        "createPortal",
        "findDOMNode",
        "flushSync",
        "hydrate",
        "render",
        "unmountComponentAtNode",
        "unstable_batchedUpdates",
        "unstable_createPortal",
        "unstable_renderSubtreeIntoContainer",
        "version"
      ]
    }
  }
}
```

## 49.使用 Dll 库

目录结构

![](http://5coder.cn/img/1668920895_3af3c0f0ea9e322dcd02a0c0a7fa20b3.png)

`Webpack.config.js`

```js
const resolveApp = require('./paths')
const HtmlWebpackPlugin = require('html-Webpack-plugin')
const { merge } = require('Webpack-merge')
const TerserPlugin = require('terser-Webpack-plugin')
const Webpack = require('Webpack')
const AddAssetHtmlPlugin = require('add-asset-html-Webpack-plugin')

// 导入其它的配置
const prodConfig = require('./Webpack.prod')
const devConfig = require('./Webpack.dev')

// 定义对象保存 base 配置信息
const commonConfig = {
  entry: {
    index: './src/index.js'
  },
  optimization: {
    minimizer: [
      new TerserPlugin({
        extractComments: false
      })
    ],
    runtimeChunk: false,
    splitChunks: {
      chunks: 'all',
      minSize: 20000,
      maxSize: 20000,
      minChunks: 1,
      cacheGroups: {
        reactVendors: {
          test: /[\\/]node_modules[\\/]/,
          filename: 'js/[name].vendor.js'
        }
      }
    }
  },
  resolve: {
    extensions: ['.js', '.json', '.wasm', '.jsx', '.ts', '.vue'],
    alias: {
      '@': resolveApp('./src')
    }
  },
  output: {
    filename: 'js/[name].[contenthash:8]._bundle.js',
    path: resolveApp('./dist'),

  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              esModule: false
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          'style-loader',
          'css-loader',
          'postcss-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|svg|gif|jpe?g)$/,
        type: 'asset',
        generator: {
          filename: "img/[name].[hash:4][ext]"
        },
        parser: {
          dataUrlCondition: {
            maxSize: 30 * 1024
          }
        }
      },
      {
        test: /\.(ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {
          filename: 'font/[name].[hash:3][ext]'
        }
      },
      {
        test: /\.jsx?$/,
        use: ['babel-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'copyWebpackPlugin',
      template: './public/index.html'
    }),
    new Webpack.DllReferencePlugin({
      context: resolveApp('./'),
      manifest: resolveApp('./dll/react.manifest.json')
    }),
    new AddAssetHtmlPlugin({
      outputPath: 'js',
      filepath: resolveApp('./dll/dll_react.js')
    })
  ]
}

module.exports = (env) => {
  const isProduction = env.production

  process.env.NODE_ENV = isProduction ? 'production' : 'development'

  // 依据当前的打包模式来合并配置
  const config = isProduction ? prodConfig : devConfig

  const mergeConfig = merge(commonConfig, config)

  return mergeConfig
}
```

![](http://5coder.cn/img/1668921184_a71ccbf2b473f8e41e0b4cdb01c964c7.png)

打包后的index.html

![](http://5coder.cn/img/1668921259_41811dba52c9da64fdd5486cc1d94224.png)

![](http://5coder.cn/img/1668921308_86e68df3834b7ce347bb60a1ef703811.png)

## 50.CSS 抽离和压缩

### CSS抽离和压缩

`Webpack`中，如果正常在`js`中引入`css`文件样式，在`Webpack`打包时会将改`css`文件也打包进入`js`的`bundle`中。我们希望在`js`中引入的`css`样式文件单独抽离出来并且打包和压缩，这里需要使用`Webpack`提供的`MiniCssExtractPlugin`来实现。

代码目录

![](http://5coder.cn/img/1668933986_89bde74d2718d2304653e70122138c02.png)

由于将css单独抽离打包的需求在开发阶段并不需要，且不适合，所以需要区分环境进行使用。在webpack.common.js和webpack。prod.js中分别进行单独配置。

```js
const resolveApp = require('./paths')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const { merge } = require('webpack-merge')
const TerserPlugin = require("terser-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin")

// 导入其它的配置
const prodConfig = require('./webpack.prod')
const devConfig = require('./webpack.dev')

// 定义对象保存 base 配置信息
const commonConfig = (isProduction) => {
  return {
    entry: {
      index: './src/index.js'
    },
    resolve: {
      extensions: [".js", ".json", '.ts', '.jsx', '.vue'],
      alias: {
        '@': resolveApp('./src')
      }
    },
    output: {
      filename: 'js/[name].[contenthash:8].bundle.js',
      path: resolveApp('./dist'),
    },
    optimization: {
      runtimeChunk: true,
      minimizer: [
        new TerserPlugin({
          extractComments: false,
        }),
      ]
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
            {
              loader: 'css-loader',
              options: {
                importLoaders: 1,
                esModule: false
              }
            },
            'postcss-loader'
          ]
        },
        {
          test: /\.less$/,
          use: [
            'style-loader',
            'css-loader',
            'postcss-loader',
            'less-loader'
          ]
        },
        {
          test: /\.(png|svg|gif|jpe?g)$/,
          type: 'asset',
          generator: {
            filename: "img/[name].[hash:4][ext]"
          },
          parser: {
            dataUrlCondition: {
              maxSize: 30 * 1024
            }
          }
        },
        {
          test: /\.(ttf|woff2?)$/,
          type: 'asset/resource',
          generator: {
            filename: 'font/[name].[hash:3][ext]'
          }
        },
        {
          test: /\.jsx?$/,
          use: ['babel-loader']
        }
      ]
    },
    plugins: [
      new HtmlWebpackPlugin({
        title: 'copyWebpackPlugin',
        template: './public/index.html'
      })
    ]
  }
}

module.exports = (env) => {
  const isProduction = env.production

  process.env.NODE_ENV = isProduction ? 'production' : 'development'

  // 依据当前的打包模式来合并配置
  const config = isProduction ? prodConfig : devConfig

  const mergeConfig = merge(commonConfig(isProduction), config)

  return mergeConfig
}
```

在webpack.common.js中将配置文件作为function的导出数据使用，可以使用传参的方式来判断当前的环境（生产或者开发）。

![](http://5coder.cn/img/1668934186_991d97e92560f4f8d0c7d0bbfce0d40d.png)

在webpack.prodd.js中

```js
const CopyWebpackPlugin = require('copy-webpack-plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin")

module.exports = {
  mode: 'production',
  optimization: {
    minimizer: [
      new CssMinimizerPlugin()
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'public',
          globOptions: {
            ignore: ['**/index.html']
          }
        }
      ]
    }),
    new MiniCssExtractPlugin({
      filename: 'css/[name].[hash:8].css'
    })
  ]
}
```

![](http://5coder.cn/img/1668934227_b7c50ebe030466eb472723cd56921e9f.png)

执行yarn build打包后，发现在dist目录中单独抽离出来了css目录及文件。并且在使用yarn serve开发环境时，样式文件也可以正常加载。

并且使用新的插件`css-minimizer-webpack-plugin`对css文件进行压缩。

![](http://5coder.cn/img/1668934315_97485a74f8f5dbba986f76b9b207b033.png)

[MiniCssExtractPlugin官方文档](https://www.webpackjs.com/plugins/mini-css-extract-plugin/)

## 51.TerserPlugin 压缩 JS

webapck中提供了压缩 js 代码的方式，可以移除无用代码、替换变量名等，减少编译后文件体积，提升加载速度。

![](http://5coder.cn/img/1668948981_9bebd5eeff3fc52c7559f53d5a6dbacd.png)

![](http://5coder.cn/img/1668949034_ab77bc09060dd48ab23d2f2c3cda1065.png)

![](http://5coder.cn/img/1668948991_ec91eb939b0bfdd2768713e196025eed.png)

不同mode
在 webpack配置文件 webpack.config.js中通过将 mode设置为 development或者 production，会对代码进行不同的处理。
![](http://5coder.cn/img/1668948781_b854bf1e1000cbb0fafbc6a0cbe7400e.png)

可以发现，`production`模式下编译的文件，文件及变量名被修改、空格换行被去除，即使自己没有进行配置，`webpack` 也会在我们设置 `production`的模式时默认添加一些属性，比如这里js代码压缩用到的就是 `TerserPlugin `。

![](http://5coder.cn/img/1668948817_d84591956f60392871ec18a93e0c74b0.png)

### terser

`TerserPlugin`处理代码依赖的是 `terser`这个工具， `terser `是可以直接安装并独立使用的，使用的时候有非常多的配置可以自行定义，具体可参考 [官方文档](https://github.com/terser/terser)

![](http://5coder.cn/img/1668948842_025f31cb08e21d0dc26d24ce8ada39ae.png)

其中属于 compress options

arrows — 对象里的箭头函数函数体只有一句
arguments — arguments 参数进行转换
dead_code — 删除不可达的代码 (remove unreachable code)
以下属于 mangle options

toplevel — 顶层作用域要不要丑化
keep_classnames — 类名保留
keep_fnames — 保留函数名
通过 npm install terser安装依赖后，直接执行 terser 命令语句 npx terser ./src/index.js -o ./terser/default.js，这里没有进行配置，所以使用的是默认处理方式，只移除了换行。
![](http://5coder.cn/img/1668948868_86b441b494a092fd50ba1a70788b0a2c.png)

自定义js代码的编译方式，npx terser ./src/index.js -o terser/index.min.js -c arguments,arrows=true -m toplevel,keep_classnames,keep_fnames

以上配置表示

函数中使用到 arguments 时，转成形参
箭头函数体只有一句时，去除 return
丑化顶层作用域的变量，比如将变量名 message 变为 o
保留类名
保留函数名
可以看到，编译后的代码去除了空格和换行，以及一些其它指定的处理
![](http://5coder.cn/img/1668948894_d4e05e20fadcd28fb0a20199020a1db4.png)

为了更方便阅读，将编译后的代码格式化

![](http://5coder.cn/img/1668948907_da3a892a872547e33122e2f9f3ba52b5.png)

TerserPlugin
在项目中，有很多 js 文件需要进行压缩处理，自己一个个命令去指定编译规则的方式会过于麻烦，通过 TerserPlugin 统一配置能够解决这个问题。

通过 npm install terser-webpack-plugin --save-dev安装依赖后，在 webpack.config.js文件中定义对应的配置，更多配置可参考 官方文档

```js
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  // 其它配置省略 
  mode: 'production',
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            arguments: true,
            dead_code: true,
          },
          toplevel: true,
          keep_classnames: true,
          keep_fnames: true,
        },
      }),
    ],
  },
};

```

编译后文件的js代码被压缩到了一行，格式化之后可以看到对应的处理

![](http://5coder.cn/img/1668948948_66f1bab6e40f270e318a2a6277e212f5.png)

总结
terser是一个工具，有着压缩、转换处理 js 代码等功能，通过命令行可以直接对 js 文件进行编译。

但在项目中，直接使用 terser过于繁琐，所以借助 terser-webpack-plugin统一编译，当 mode为 production时，有默认的配置，也可以自行定义处理规则。

## 52.scope hoisting(2022.11.20待补充)



## 53.usedExports 配置(2022.11.20待补充)



## 54.sideEffects 配置(2022.11.20待补充)



## 55.Css-TreeShaking(2022.11.20待补充)



## 56.资源压缩(2022.11.20待补充)



## 57.inlineChunkHtmlPlugin 使用(2022.11.20待补充)



## 58.Webpack 打包 Library(2022.11.20待补充)



## 59.打包时间和内容分析(2022.11.20待补充)

