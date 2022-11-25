---
title: Webpack Resolve文档
author: 5coder
tags: Webpack Resolve
category: 大前端
abbrlink: 49845
date: 2022-11-25 23:25:53
password:
keywords:
top:
cover:
---

# 解析(Resolve)

这些选项能设置模块如何被解析。webpack 提供合理的默认值，但是还是可能会修改一些解析的细节。关于 resolver 具体如何工作的更多解释说明，请查看[模块解析](https://www.webpackjs.com/concepts/module-resolution)。

## resolve

```
object
```

配置模块如何解析。例如，当在 ES2015 中调用 `import 'lodash'`，`resolve` 选项能够对 webpack 查找 `'lodash'` 的方式去做修改（查看[`模块`](https://www.webpackjs.com/configuration/resolve/#resolve-modules)）。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    // configuration options
  },
};
```

### resolve.alias

```
object
```

创建 `import` 或 `require` 的别名，来确保模块引入变得更简单。例如，一些位于 `src/` 文件夹下的常用模块：

**webpack.config.js**

```js
const path = require('path');

module.exports = {
  //...
  resolve: {
    alias: {
      Utilities: path.resolve(__dirname, 'src/utilities/'),
      Templates: path.resolve(__dirname, 'src/templates/'),
    },
  },
};
```

现在，替换“在导入时使用相对路径”这种方式，就像这样：

```js
import Utility from '../../utilities/utility';
```

你可以这样使用别名：

```js
import Utility from 'Utilities/utility';
```

也可以在给定对象的键后的末尾添加 `$`，以表示精准匹配：

**webpack.config.js**

```js
const path = require('path');

module.exports = {
  //...
  resolve: {
    alias: {
      xyz$: path.resolve(__dirname, 'path/to/file.js'),
    },
  },
};
```

这将产生以下结果：

```js
import Test1 from 'xyz'; // 精确匹配，所以 path/to/file.js 被解析和导入
import Test2 from 'xyz/file.js'; // 非精确匹配，触发普通解析
```

下面的表格展示了一些其他情况：

| `alias:`                           | `import 'xyz'`                        | `import 'xyz/file.js'`               |
| :--------------------------------- | :------------------------------------ | :----------------------------------- |
| `{}`                               | `/abc/node_modules/xyz/index.js`      | `/abc/node_modules/xyz/file.js`      |
| `{ xyz: '/abc/path/to/file.js' }`  | `/abc/path/to/file.js`                | error                                |
| `{ xyz$: '/abc/path/to/file.js' }` | `/abc/path/to/file.js`                | `/abc/node_modules/xyz/file.js`      |
| `{ xyz: './dir/file.js' }`         | `/abc/dir/file.js`                    | error                                |
| `{ xyz$: './dir/file.js' }`        | `/abc/dir/file.js`                    | `/abc/node_modules/xyz/file.js`      |
| `{ xyz: '/some/dir' }`             | `/some/dir/index.js`                  | `/some/dir/file.js`                  |
| `{ xyz$: '/some/dir' }`            | `/some/dir/index.js`                  | `/abc/node_modules/xyz/file.js`      |
| `{ xyz: './dir' }`                 | `/abc/dir/index.js`                   | `/abc/dir/file.js`                   |
| `{ xyz: 'modu' }`                  | `/abc/node_modules/modu/index.js`     | `/abc/node_modules/modu/file.js`     |
| `{ xyz$: 'modu' }`                 | `/abc/node_modules/modu/index.js`     | `/abc/node_modules/xyz/file.js`      |
| `{ xyz: 'modu/some/file.js' }`     | `/abc/node_modules/modu/some/file.js` | error                                |
| `{ xyz: 'modu/dir' }`              | `/abc/node_modules/modu/dir/index.js` | `/abc/node_modules/modu/dir/file.js` |
| `{ xyz$: 'modu/dir' }`             | `/abc/node_modules/modu/dir/index.js` | `/abc/node_modules/xyz/file.js`      |

如果在 `package.json` 中定义，`index.js` 可能会被解析为另一个文件。

`/abc/node_modules` 也可能在 `/node_modules` 中解析。

###### Warning

`resolve.alias` 优先级高于其它模块解析方式。

###### Warning

[`null-loader`](https://github.com/webpack-contrib/null-loader) 在webpack5中被废弃。使用 `alias: { xyz$: false }` 或绝对路径 `alias: {[path.resolve(__dirname, './path/to/module')]: false }`

###### Warning

`[string]` 字符串值在 webapck 5 中被支持。

```js
module.exports = {
  //...
  resolve: {
    alias: {
      _: [
        path.resolve(__dirname, 'src/utilities/'),
        path.resolve(__dirname, 'src/templates/'),
      ],
    },
  },
};
```

将 `resolve.alias` 设置为 `false` 将告知 webpack 忽略模块。

```js
module.exports = {
  //...
  resolve: {
    alias: {
      'ignored-module': false,
      './ignored-module': false,
    },
  },
};
```

### resolve.aliasFields

```
[string]: ['browser']
```

指定一个字段，例如 `browser`，根据 [此规范](https://github.com/defunctzombie/package-browser-field-spec)进行解析。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    aliasFields: ['browser'],
  },
};
```

### resolve.cacheWithContext

```
boolean
```

如果启用了不安全缓存，请在缓存键(cache key)中引入 `request.context`。这个选项被 [`enhanced-resolve`](https://github.com/webpack/enhanced-resolve/) 模块考虑在内。从 webpack 3.1.0 开始，在配置了 resolve 或 resolveLoader 插件时，解析缓存(resolve caching)中的上下文(context)会被忽略。这解决了性能衰退的问题。

### resolve.conditionNames

```
string[]
```

[`exports` 配置项](https://nodejs.org/api/packages.html#packages_exports) （定义一个库的入口）的 conditionName。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    conditionNames: ['require', 'node'],
  },
};
```

Webpack 将会匹配列在 `resolve.conditionNames` 数组中的 [export conditions](https://nodejs.org/api/packages.html#conditional-exports)。

`exports` 字段中的键顺序很重要。在条件匹配期间，较早的入口具有更高的优先级并优先于后面的入口。

例如，

**package.json**

```json
{
  "name": "foo",
  "exports": {
    ".": {
      "import": "./index-import.js",
      "require": "./index-require.js",
      "node": "./index-node.js"
    },
    "./bar": {
      "node": "./bar-node.js",
      "require": "./bar-require.js"
    },
    "./baz": {
      "import": "./baz-import.js",
      "node": "./baz-node.js"
    }
  }
}
```

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    conditionNames: ['require', 'node'],
  },
};
```

importing

- `'foo'` 将解析为 `'foo/index-require.js'`
- `'foo/bar'`将解析为 `'foo/bar-node.js'`，因为在条件导出对象中， `"node"` 字段在 `"require"` 之前。
- `'foo/baz'` 将解析为 `'foo/baz-node.js'`

### resolve.descriptionFiles

```
[string] = ['package.json']
```

用于描述的 JSON 文件。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    descriptionFiles: ['package.json'],
  },
};
```

### resolve.enforceExtension

```
boolean = false
```

如果是 `true`，将不允许无扩展名文件。默认如果 `./foo` 有 `.js` 扩展，`require('./foo')` 可以正常运行。但如果启用此选项，只有 `require('./foo.js')` 能够正常工作。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    enforceExtension: false,
  },
};
```

### resolve.extensionAlias

```
object
```

一个将拓展名与拓展名别名映射的对象。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    extensionAlias: {
      '.js': ['.ts', '.js'],
      '.mjs': ['.mts', '.mjs'],
    },
  },
};
```

### resolve.extensions

```
[string] = ['.js', '.json', '.wasm']
```

尝试按顺序解析这些后缀名。如果有多个文件有相同的名字，但后缀名不同，webpack 会解析列在数组首位的后缀的文件 并跳过其余的后缀。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    extensions: ['.js', '.json', '.wasm'],
  },
};
```

能够使用户在引入模块时不带扩展：

```js
import File from '../path/to/file';
```

请注意，以上这样使用 `resolve.extensions` 会 **覆盖默认数组**，这就意味着 webpack 将不再尝试使用默认扩展来解析模块。然而你可以使用 `'...'` 访问默认拓展名：

```js
module.exports = {
  //...
  resolve: {
    extensions: ['.ts', '...'],
  },
};
```

### resolve.fallback

```
object
```

当正常解析失败时，重定向模块请求。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    fallback: {
      abc: false, // do not include a polyfill for abc
      xyz: path.resolve(__dirname, 'path/to/file.js'), // include a polyfill for xyz
    },
  },
};
```

webpack 5 不再自动 polyfill Node.js 的核心模块，这意味着如果你在浏览器或类似的环境中运行的代码中使用它们，你必须从 NPM 中安装兼容的模块，并自己包含它们。以下是 webpack 在 webpack 5 之前使用过的 polyfill 包列表：

```js
module.exports = {
  //...
  resolve: {
    fallback: {
      assert: require.resolve('assert'),
      buffer: require.resolve('buffer'),
      console: require.resolve('console-browserify'),
      constants: require.resolve('constants-browserify'),
      crypto: require.resolve('crypto-browserify'),
      domain: require.resolve('domain-browser'),
      events: require.resolve('events'),
      http: require.resolve('stream-http'),
      https: require.resolve('https-browserify'),
      os: require.resolve('os-browserify/browser'),
      path: require.resolve('path-browserify'),
      punycode: require.resolve('punycode'),
      process: require.resolve('process/browser'),
      querystring: require.resolve('querystring-es3'),
      stream: require.resolve('stream-browserify'),
      string_decoder: require.resolve('string_decoder'),
      sys: require.resolve('util'),
      timers: require.resolve('timers-browserify'),
      tty: require.resolve('tty-browserify'),
      url: require.resolve('url'),
      util: require.resolve('util'),
      vm: require.resolve('vm-browserify'),
      zlib: require.resolve('browserify-zlib'),
    },
  },
};
```

### resolve.mainFields

```
[string]
```

当从 npm 包中导入模块时（例如，`import * as D3 from 'd3'`），此选项将决定在 `package.json` 中使用哪个字段导入模块。根据 webpack 配置中指定的 [`target`](https://www.webpackjs.com/concepts/targets) 不同，默认值也会有所不同。

当 `target` 属性设置为 `webworker`, `web` 或者没有指定：

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    mainFields: ['browser', 'module', 'main'],
  },
};
```

对于其他任意的 target（包括 `node`），默认值为：

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    mainFields: ['module', 'main'],
  },
};
```

例如，考虑任意一个名为 `upstream` 的类库 `package.json` 包含以下字段：

```json
{
  "browser": "build/upstream.js",
  "module": "index"
}
```

在我们 `import * as Upstream from 'upstream'` 时，这实际上会从 `browser` 属性解析文件。在这里 `browser` 属性是最优先选择的，因为它是 `mainFields` 的第一项。同时，由 webpack 打包的 Node.js 应用程序首先会尝试从 `module` 字段中解析文件。

### resolve.mainFiles

```
[string] = ['index']
```

解析目录时要使用的文件名。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    mainFiles: ['index'],
  },
};
```

### resolve.exportsFields

```
[string] = ['exports']
```

在 package.json 中用于解析模块请求的字段。欲了解更多信息，请查阅 [package-exports guideline](https://www.webpackjs.com/guides/package-exports/) 文档。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    exportsFields: ['exports', 'myCompanyExports'],
  },
};
```

### resolve.modules

```
[string] = ['node_modules']
```

告诉 webpack 解析模块时应该搜索的目录。

绝对路径和相对路径都能使用，但是要知道它们之间有一点差异。

通过查看当前目录以及祖先路径（即 `./node_modules`, `../node_modules` 等等）， 相对路径将类似于 Node 查找 'node_modules' 的方式进行查找。

使用绝对路径，将只在给定目录中搜索。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    modules: ['node_modules'],
  },
};
```

如果你想要添加一个目录到模块搜索目录，此目录优先于 `node_modules/` 搜索：

**webpack.config.js**

```js
const path = require('path');

module.exports = {
  //...
  resolve: {
    modules: [path.resolve(__dirname, 'src'), 'node_modules'],
  },
};
```

### resolve.unsafeCache

```
RegExp` `[RegExp]` `boolean: true
```

启用，会主动缓存模块，但并 **不安全**。传递 `true` 将缓存一切。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    unsafeCache: true,
  },
};
```

正则表达式，或正则表达式数组，可以用于匹配文件路径或只缓存某些模块。 例如，只缓存 utilities 模块：

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    unsafeCache: /src\/utilities/,
  },
};
```

###### Warning

修改缓存路径可能在极少数情况下导致失败。

### resolve.useSyncFileSystemCalls

```
boolean
```

对 resolver 使用同步文件系统调用。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    useSyncFileSystemCalls: true,
  },
};
```

### resolve.plugins

[`[Plugin\]`](https://www.webpackjs.com/plugins/)

应该使用的额外的解析插件列表。 它允许插件，如 [`DirectoryNamedWebpackPlugin`](https://www.npmjs.com/package/directory-named-webpack-plugin)。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    plugins: [new DirectoryNamedWebpackPlugin()],
  },
};
```

### resolve.preferRelative

```
boolean
```

当启用此选项时，webpack 更倾向于将模块请求解析为相对请求，而不使用来自 `node_modules` 目录下的模块。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    preferRelative: true,
  },
};
```

**src/index.js**

```js
// let's say `src/logo.svg` exists
import logo1 from 'logo.svg'; // this is viable when `preferRelative` enabled
import logo2 from './logo.svg'; // otherwise you can only use relative path to resolve logo.svg

// `preferRelative` is enabled by default for `new URL()` case
const b = new URL('module/path', import.meta.url);
const a = new URL('./module/path', import.meta.url);
```

### resolve.preferAbsolute

```
boolean
```

5.13.0+

解析时，首选的绝对路径为 [`resolve.roots`](https://www.webpackjs.com/configuration/resolve/#resolveroots)。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    preferAbsolute: true,
  },
};
```

### resolve.symlinks

```
boolean = true
```

是否将符号链接(symlink)解析到它们的符号链接位置(symlink location)。

启用时，符号链接(symlink)的资源，将解析为其 *真实* 路径，而不是其符号链接(symlink)的位置。注意，当使用创建符号链接包的工具（如 `npm link`）时，这种方式可能会导致模块解析失败。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    symlinks: true,
  },
};
```

### resolve.cachePredicate

```
function(module) => boolean
```

决定请求是否应该被缓存的函数。函数传入一个带有 `path` 和 `request` 属性的对象。 必须返回一个 boolean 值。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    cachePredicate: (module) => {
      // additional logic
      return true;
    },
  },
};
```

### resolve.restrictions

```
[string, RegExp]
```

解析限制列表，用于限制可以解析请求的路径。

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    restrictions: [/\.(sass|scss|css)$/],
  },
};
```

### resolve.roots

```
[string]
```

A list of directories where requests of server-relative URLs (starting with '/') are resolved, defaults to [`context` configuration option](https://www.webpackjs.com/configuration/entry-context/#context). On non-Windows systems these requests are resolved as an absolute path first.

**webpack.config.js**

```js
const fixtures = path.resolve(__dirname, 'fixtures');
module.exports = {
  //...
  resolve: {
    roots: [__dirname, fixtures],
  },
};
```

### resolve.importsFields

```
[string]
```

Fields from `package.json` which are used to provide the internal requests of a package (requests starting with `#` are considered internal).

**webpack.config.js**

```js
module.exports = {
  //...
  resolve: {
    importsFields: ['browser', 'module', 'main'],
  },
};
```

### resolve.byDependency

通过 module 请求类型来配置 resolve 选项。

- Type: `[type: string]: ResolveOptions`

- Example:

  ```js
  module.exports = {
    // ...
    resolve: {
      byDependency: {
        // ...
        esm: {
          mainFields: ['browser', 'module'],
        },
        commonjs: {
          aliasFields: ['browser'],
        },
        url: {
          preferRelative: true,
        },
      },
    },
  };
  ```

## resolveLoader

```
object { modules [string] = ['node_modules'], extensions [string] = ['.js', '.json'], mainFields [string] = ['loader', 'main']}
```

这组选项与上面的 `resolve` 对象的属性集合相同， 但仅用于解析 webpack 的 [loader](https://www.webpackjs.com/concepts/loaders) 包。

**webpack.config.js**

```js
module.exports = {
  //...
  resolveLoader: {
    modules: ['node_modules'],
    extensions: ['.js', '.json'],
    mainFields: ['loader', 'main'],
  },
};
```

###### Tip

请注意你可以在这里使用别名和 resolve 中熟悉的其他特性。例如 `{ txt: 'raw-loader' }` 将会 shim `txt!templates/demo.txt` 使用 `raw-loader`。
