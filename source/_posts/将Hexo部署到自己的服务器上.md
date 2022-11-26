---
title: 将Hexo部署到自己的服务器上
author: 5coder
tags: Hexo
category: 大前端
abbrlink: 62067
date: 2022-11-26 09:50:30
password:
keywords:
top:
cover:
---

# 部署Hexo到自己的Linux服务器上

## 第一部分：服务器端操作

### 1.安装git和nginx

```shell
yum install -y nginx git
```

### 2.添加一个git用户

```shell
useradd git
passwd git

# 给git用户配置sudo权限
chmod 740 /etc/sudoers
vim /etc/sudoers
# 找到root ALL=(ALL) ALL，在它下方加入一行
git ALL=(ALL) ALL

chmod 400 /etc/sudoers
```

### 3.给git用户添加ssh秘钥

```shell
su - git
mkdir -p ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorzied_keys
chmod 700 ~/.ssh
vim ~/.ssh/authorized_keys    #将ssh密钥粘贴进去
# 秘钥在自己本地电脑-用户/5coder/.ssh中找
```

### 4.创建git仓库并使用git-hooks实现自动部署

```shell
sudo mkdir -p /var/repo    #新建目录，这是git仓库的位置
sudo mkdir pp /var/www/hexo
cd /var/repo  #转到git仓库的文件夹
sudo git init --bare blog.git #创建一个名叫blog的仓库
sudo vim /var/repo/blog.git/hooks/post-update
```

`post-update`的内如如下：

```shell
#!/bin/bash
git --work-tree=/var/www/hexo --git-dir=/var/repo/blog.git checkout -f
```

**给post-update授权**：

```shell
cd /var/repo/blog.git/hooks/
sudo chown -R git:git /var/repo/
sudo chown -R git:git /var/www/hexo
sudo chmod +x post-update  #赋予其可执行权限
```

### 5.配置Nginx

```shell
cd /etc/nginx/conf.d/
vim blog.conf
```

`blog.conf`的内如如下：

```json
server {
    listen    80 default_server;
    listen    [::] default_server;
    server_name    blog.59devops.com;
    root    /var/www/hexo
}
```

检查Nginx语法并重载nginx：

![](http://5coder.cn/img/1669427779_a8f394610c1430143ec6d31d62013047.png)

### 6.修改git用户的默认shell环境

```shell
vim /etc/passwd
#修改最后一行
#将/bin/bash修改为/usr/bin/git-shell
```

### 7.解析域名

到你购买域名的供应商控制台，将域名解析到你的服务器即可。
