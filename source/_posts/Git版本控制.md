---
title: Git版本控制
author: 5coder
abbrlink: 64901
date: 2021-05-20 22:41:12
summary:
tags: Git
category: Git
---

## Git版本控制

**为什么要进行版本控制？**  最简单的例子，当我们用文字处理软件工作时（如Word）时需要进行修改，而有时候又不确定修改的内容是不是需要的，因此会产生许多个文件，如图：  

![img/v2-5baa32dc2504ef9f6a1fbc427f6370a9_b](https://i.loli.net/2021/05/20/uMiyGdlK5oNjr7J.jpg)

每一个文件都是在之前的文件基础上进行微小的修改，久而久之，不但文件冗杂，而且还不清楚修改的内容是什么，是一种很杂乱的方式。

而版本控制就是解决这一问题——通过记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统。

采取版本控制后，你可以将文件还原到之前的状态，比较各状态之间的细节从而查出是修改了哪个地方，找出哪里出了问题。甚至你可以随意删改项目中的文件，照样可以恢复到之前的样子，因而增加了容错率，提供了更多可能性。

版本控制有三种，第一种是本地式版本控制，也就是在本地的硬盘上用数据库记录历代文件；第二种是集中式版本控制，通过一个服务器，多个用户连接到服务器进行文件的记录。 而第三种是我们着重介绍的*分布式版本控制*，它将前两种结合起来，在本地和服务器都建立数据库，每次工作时从服务器克隆（clone）下来，同时又与服务器交互，从而兼顾协同性和安全性。

*我们所说的git就是一个分布式版本控制软件，GitHub就是一个git的托管服务。*

​    

## git本地操作

git设计简单，是完全分布式，允许成千上万个并行开发的分支(Branch)，有能力管理超大规模的项目，是目前首选的版本控制软件。

## 一、工作流程

git的三个工作区域，对应着三种状态：


![img/v2-f3c1e1cc39be62f9ff2dc8f1654f98cd_b](https://i.loli.net/2021/05/20/BcNz6ulgRbY47rO.png)


 git 工作流程如下：    

1.  在工作目录中修改文件。（modified）  

2.  暂存文件，将文件的快照放入暂存区域。（staged）  

3.  提交更新，找到暂存区域的文件，将快照永久性存储到 git 仓库目录。（committed）

这是最基本的流程，需要时刻记住。  

## 二、安装git

[git官方网站](https://link.zhihu.com/?target=https%3A//git-scm.com/downloads)下载对应自己电脑的版本，按照指引进行安装。

## 三、git使用知识

首先我们需要在本地创建一个仓库，用于存放历代版本。

1.命令行中运用cd指令进入项目的目录，输入  

```text
$ git init
```

这将创建一个名为.git的隐藏子目录。    

2.git status:查看哪些文件处于什么状态  

```text
$ git status
On branch master
nothing to commit, working directory clean
（创建git仓库后目录下没有文件时的情况）
```

创建一个文件（test）后再使用git status命令，将会看到一个新的提示  

```text
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Untracked files:
(use "git add <file>..." to include in what will be committed)

test

nothing added to commit but untracked files present (use "git add" to track)

（新建的“test”文件出现在Untracked files下）
```

3.git add：跟踪文件 运行     

```text
$ git add test
```

此时再运行git status，会看到test文件已被跟踪，处于暂存状态(staged)，显示Changes to be committed    

```text
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
(use "git reset HEAD <file>..." to unstage)

test
```

4.git commit：提交更新至仓库  

先用git status命令确定暂存区域准备妥当， 再运行$git commit -m ”提交信息”（提交信息指本次提交的说明，类似于注释）    

```text
$ git commit -m "first"
[master 5e43df6] first
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 test
```

此时会显示提交成功的信息。  

5.git diff：显示尚未暂存的改动（并不是所有改动）

6.git rm test：删除暂存区域中的文件test

7.git log:查看提交历史  

```text
$ git log
commit 5e43df6b6d003ea70444ee3125456fd75b066803
Author: *** <****@gmail.com>
Date:   Thu Mar 16 19:37:52 2017 +0800

first

commit 1c83e2a07f0279ea510e2a323fada53166c3c657
Author: *** <****@gmail.com>
Date:   Thu Mar 16 19:16:26 2017 +0800

test
```

8.版本回退  

在git log命令中我们可以看到类似*5e43......6803*的一大串字符，那就是版本号（commit id）我们可以用 git reset命令回退到之前任何一个版本:    

```text
$ git reset --hard 1c83e2a0
   HEAD is now at 1c83e2a test
```

（版本号不必补全，Git会自动去查找）

以上就是git的本地基本操作，包括创建一个仓库，更改、暂存和提交，查看仓库的提交历史，版本回退。  

## 分支

分支是把工作从主线上分离开来，以免影响开发主线。在不同的分支上你可以尝试各种各样的增删改，实现不同的设想。而git的分支模型是它最突出的特点，也是git脱颖而出的原因。

## 一、分支概念

在版本回退里，你可以回溯到之前的任意版本，而这些版本都是处于一条时间线上，这条时间线就是一个分支。
 默认的分支为master分支，本身可以看做一个指针，HEAD指针则指向master指针，如图：    

![img/v2-2bdaaedcea49b643d9054b364fcc9d7b_b](https://i.loli.net/2021/05/20/xqTbYZVLBHgvUSO.png)

每次提交都会多出一个节点，指针也随之移动。
 当我们创建新的分支时，也就创建了一个新的指针，我们通过命令将HEAD指针移到新指针上：  


![img/v2-eaa71af7dbc7af4d88dd4269c0aadb94_b](https://i.loli.net/2021/05/20/wW73NTMyfGx81cm.png)



新提交一次后，新指针向前移动，master指针不变，这就产生了分支：
 我们可以将两条分支合并，之后可以删掉新分支。

![img/v2-5e29021a13b221d13909abec8d7ff735_b](https://i.loli.net/2021/05/20/LzUaQ6nmJgcH8E1.png)





![img/v2-a1c29dbcd27b8b5be9899afbb2bb0b24_b](https://i.loli.net/2021/05/20/q9Y3DC4PpFKeSNI.png)

这样就完成了分支的合并。

## 二、分支使用

1.git branch：查看当前所有分支      

```text
$ git branch

* master
```

（*标示当前分支，默认处于master分支）  

2.git branch testing : 创建testing分支      

```text
$ git branch testing
```

此时创建了testing分支，运行git branch命令验证       

```text
$git branch    

*master
testing
```

3.git checkout testing： 切换到testing分支      

```text
$ git checkout testing
Switched to branch 'testing'
```

此时主分支位于testing，运行git branch命令验证   

```text
$ git branch
  master

* testing
```

4.git merge testing：将master分支和testing分支合并  （假设处于master分支）      

```text
$ git merge testing
Already up-to-date.
```

如果在两个不同的分支中，对同一个文件的同一个部分进行了不同的修改，则会产生冲突从而无法合并，只能手动解决后再合并。    

5.git branch -d删除分支  

```text
$ git branch -d testing
Deleted branch testing (was 1c83e2a).
```

## 使用GitHub

GitHub 是最大的 Git 版本库托管商，尽管这不是 Git 开源项目的直接部分，但如果想要专业地使用 Git，你将不可避免地与 GitHub 打交道。  

### 创建帐户及配置

1.访问[https://github.com](https://link.zhihu.com/?target=https%3A//github.com)进行注册  

2.SSH访问：    

```text
$ cd ~/.ssh
$ ls
 id_rsa     id_rsa.pub  known_hosts
```

寻找到id_rsa命名的文件，.pub文件是公钥，另一个是私钥。    

如果找不到，可以运行如下命令创建它们    

```text
$ ssh-keygen
```

进入github的帐户设置，点击左侧的SSH and GPG keys，将~/.ssh/id_rsa.pub公钥文件的内容粘贴到文本区，然后点击"Add key"    

SSH访问配置成功     

### 创建、维护和管理你自己的项目。

1.点击页面右上角的＋号，点击New repository按钮


![img/v2-3cf6e399f56ab213b6626c3420fee410_b](E:\lagou\笔记整理\版本控制\img\v2-3cf6e399f56ab213b6626c3420fee410_b.png)

![img/v2-f518348e215125a7cf1e044adf9567cb_b](E:\lagou\笔记整理\版本控制\img\v2-f518348e215125a7cf1e044adf9567cb_b.png)

Respository name是必填项目，而其余都是选填项，可以默认。
 点击Create respository按钮  ，即创建了一个新的仓库
 这时候可以将项目分享给其他人，通过HTTP和SSH的形式。  

![img/v2-b64a2c230b6caf84981af0d587ece07a_b](https://i.loli.net/2021/05/20/vy49qSW5N8QOPjX.png)



2.对仓库进行操作，使本地和github同步  

```text
$ git remote add origin     **********（仓库地址）   
（添加远程仓库至本地）

 $ git pull --rebase origin master    
（更新远程更新到本地）

 $ git push -u origin master  
（将本地仓库和远程仓库合并）
```

在今后的项目工作中就是用以上命令同步本地和Github，需要记住。  

3.克隆仓库  我们可以将远程仓库的内容克隆到本地

```text
$ git clone git@github.com:Liuwt1997/github-photo.git
Cloning into 'github-photo'...
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), 196.28 KiB | 67.00 KiB/s, done.
Checking connectivity... done.
```

此时远程仓库的文件全部克隆至本地。

4.添加合作者
 点击边栏的 “Settings” 链接，然后从左侧菜单中选择 “Collaborators” 。 然后，在输入框中填写用户名，点击 “Add collaborator.” 此时可以给予他们提交的权限。  



![img/v2-a93bf672a283a3dda24584ff833f799d_b](https://i.loli.net/2021/05/20/j3IYiDwG8thgmC7.png)

5.Fork按钮可以将他人项目派生下来，在你的空间中创建一个完全属于你的项目副本。  



![img/v2-aceaaf541576e6be2edc65ce951928c4_b](https://i.loli.net/2021/05/20/mKhoDRjUB7QSwc9.png)



如何对项目做出贡献呢？    

1.  将派生出的副本克隆到本地

2.  创建出名称有意义的分支

3.  修改代码

4.  检查改动

5.  将改动提交到分支中

6.  将新分支推送到 GitHub 的副本中    

现在到 GitHub 上查看之前的项目副本，可以看到 GitHub 提示我们有新的分支，并且显示了一个大大的绿色按钮让我们可以检查我们的改动，并给源项目创建合并请求。    

如果你点击了那个绿色按钮，就会看到一个新页面，在这里我们可以对改动填写标题和描述，让项目的拥有者考虑一下我们的改动。通常花点时间来编写个清晰有用的描述是个不错的主意，这能让作者明白为什么这个改动可以给他的项目带来好处，并且让他接受合并请求。