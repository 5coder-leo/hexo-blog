---
title: yarn与npm命令对比
author: 5coder
abbrlink: 24626
date: 2021-05-20 22:43:12
summary:
tags: 
- yarn
- npm
category: 大前端
---

# yarn与npm命令对比

> 注：x 代表包名
>
> | 代表有两个方式都可以 比如 npm i | install 可以直接npm i 或者 npm install
>
> yarn global 这个顺序不可以改变
>
> npm ls -g --depth 0 查看npm安装过的全局包

| npm                         | yarn                         |                        |
| --------------------------- | ---------------------------- | ---------------------- |
| npm init                    | yarn init                    | 初始化                 |
| npm i \| install            | yarn (install)               | 安装依赖包             |
| npm i x --S \| --save       | yarn add x                   | 安装生产依赖并保存包名 |
| npm i x --D \| --save-dev   | yarn add x -D                | 安装开发依赖并保存报名 |
| npm un \| uninstall x       | yarn remove                  | 删除依赖包             |
| npm i -g \| npm -g i x      | yarn global add x            | 全局安装               |
| npm un -g x                 | yarn global remove x         | 全局卸载               |
| npm run dev                 | yarn dev \| run dev          | 运行命令               |
| npm config set registry url | yarn config set registry url | 设置下载镜像地址       |

## yarn

### 常用指令

```sh
# 生成 package.json 文件（需要手动选择配置）
yarn init

# 生成 package.json 文件（使用默认配置）
yarn init -y

# 一键安装 package.json 下的依赖包
yarn

# 在项目中安装包名为 xxx 的依赖包（配置在 dependencies 下）,同时 yarn.lock 也会被更新
yarn add xxx

# 在项目中安装包名为 xxx 的依赖包（配置在配置在 devDependencies 下）,同时 yarn.lock 也会被更新
yarn add xxx --dev

# 全局安装包名为 xxx 的依
yarn global add xxx

# 运行 package.json 中 scripts 下的命令
yarn xxx
```

### 不常用指令

```shell
# 列出 xxx 包的版本信息
yarn outdated xxx

# 验证当前项目 package.json 里的依赖版本和 yarn 的 lock 文件是否匹配
yarn check

# 将当前模块发布到 npmjs.com，需要先登录
yarn publish
```

## npm

### 常用指令

```shell
# 查看全局安装过的模块
npm list -g --depth 0

# 查看node版本
node --version

# 生成 package.json 文件（需要手动选择配置）
npm init

# 生成 package.json 文件（使用默认配置）
npm init -y

# 一键安装 package.json 下的依赖包
npm i

# 在项目中安装包名为 xxx 的依赖包（配置在 dependencies 下）
npm i xxx

# 在项目中安装包名为 xxx 的依赖包（配置在 dependencies 下）
npm i xxx --save

# 在项目中安装包名为 xxx 的依赖包（配置在 devDependencies 下）
npm i xxx --save-dev

# 全局安装包名为 xxx 的依赖包
npm i -g xxx

# 运行 package.json 中 scripts 下的命令
npm run xxx
```

### 不常用指令

```shell
# 打开 xxx 包的主页
npm home xxx

# 打开 xxx 包的代码仓库
npm repo xxx

# 将当前模块发布到 npmjs.com，需要先登录
npm publish
```

