---
title: Vuex 状态管理
author: 5coder
tags: Vuex
category: 大前端
keywords: Vuex
abbrlink: 31096
date: 2021-07-19 21:22:53
top:
cover:
---

# Vuex状态管理

## 课程目标

- 组件通信方式回顾
- Vuex核心概念和基本使用
- 购物车案例
- 模拟实现Vuex

## 组件内的状态管理流程

Vue最核心的两个功能：数据驱动和组件化

组件化开发给我们带来了：

- 更快的开发效率
- 更好的可维护性

每个组件都有自己的状态、视图和行为等组成部分

```js
new Vue({
// state
  data () {
    return {
      count: 0
    }
  },
// view
  template: `
<div>{{ count }}</div>
`,
// actions
  methods: {
    increment () {
      this.count++
    }
  }
})
```

状态管理包含一下几部分：

- **state**，驱动应用的数据源
- **view**，以声明方式将state映射到视图
- **actions**，响应在view上的用户输入导致的状态变化

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210719213045881.png)

## 组件间通信方式回顾

大多数场景下的组件都并不是独立存在的，而是相互协作共同构成了一个复杂的业务功能。在 Vue 中为不同的组件关系提供了不同的通信规则。

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210719213508962.png)

### [父传子：Props Down](https://cn.vuejs.org/v2/guide/components.html#%E9%80%9A%E8%BF%87-Prop-%E5%90%91%E5%AD%90%E7%BB%84%E4%BB%B6%E4%BC%A0%E9%80%92%E6%95%B0%E6%8D%AE)

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210719213708568.png)

![](https://gitee.com/coder5leo/markdown-picture-bed/raw/master/img/image-20210719213815350.png)

### [子传父：Event Up](https://cn.vuejs.org/v2/guide/components.html#%E7%9B%91%E5%90%AC%E5%AD%90%E7%BB%84%E4%BB%B6%E4%BA%8B%E4%BB%B6)



### [非父子组件：Event Bus](https://cn.vuejs.org/v2/guide/migration.html#dispatch-%E5%92%8C-broadcast-%E6%9B%BF%E6%8D%A2)

### [父直接访问子组件：通过ref获取子组件](https://cn.vuejs.org/v2/guide/components-edge-cases.html#%E8%AE%BF%E9%97%AE%E5%AD%90%E7%BB%84%E4%BB%B6%E5%AE%9E%E4%BE%8B%E6%88%96%E5%AD%90%E5%85%83%E7%B4%A0)

## 简易的状态管理方案

## Vuex回顾

### 什么是Vuex

### 什么情况下使用Vuex

### 核心概念回顾

## 购物车案例

### 功能列表

### 商品列表

### 商品列表-弹出购物车窗口

### 购物车

### 本地存储

### 严格模式

## Vuex模拟实现

### 实现思路

### install方法

### Stroe类

### 使用自己实现的Vuex

