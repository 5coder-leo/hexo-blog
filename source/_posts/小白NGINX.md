---
title: 小白NGINX
author: 5coder
abbrlink: 37541
date: 2021-05-20 22:49:37
summary:
tags: Nginx
category: Linux
---

*Nginx 是一个采用主从架构的 Web 服务器，可用于反向代理、负载均衡器、邮件代理和 HTTP 缓存*。

Emmm，上面的 Nginx 介绍看过去有些复杂而且充满了不明觉厉的术语。Relax，在这篇文章里，我（原作者）会先带你理解 Nginx 的架构和专有术语，最后实践一把安装和配置 **Nginx**。

![](http://5coder.cn/img/q7r9OEdkxBVuwln.jpg)

简单来说，你只要记住一点：*Nginx 是个神奇的 Web 服务器*。（注：神奇之处下文会娓娓道来）

那什么是 Web 服务器呢？简而言之，Web 服务器就是一个中间人。举个例子，你要访问 `hellogithub.com`（注：原文例子为 dev.to），在地址栏输入 `https://hellogithub.com` 时，你的浏览器会找到 `https://hellogithub.com` 的网络服务器地址并将它指向后端服务器，后端服务器再返回响应给客户端。

## **代理 vs 反向代理** 

Nginx 的基本特性是代理，所以你一定要明白什么是**代理**和**反向代理**。

### **代理**

看个小例子，现在我们有 N 个客户端（N >= 1），一个中间 Web 服务器（在本例中，我们称之为代理）和一个服务器。这个例子主要的场景是，服务器不知道哪个客户端在请求（响应）。是不是有点难以理解？下面让我用示意图讲解下：

![](http://5coder.cn/img/dHWV6JLXwz4rgmI.jpg)

如图，*client1* 和 *client2* 通过代理服务器向服务器发送请求 *request1* 和 *request2*，此时后端服务器不知道 *request1* 是由 *client1* 发送的还是 *client2* 发送的，但会执行（响应）操作。

### **反向代理**

简单来说，反向代理与代理的功能相反。现在我们有一个客户端、一个中间 Web 服务器和 N 个后端服务器（N >= 1），同样的来看下示意图：

![](http://5coder.cn/img/v2-2d5a169d1b6781b636e6fa27d7402399_b.jpg)

如图，客户端将通过 Web 服务器发送请求。而 Web 服务器会通过一个算法，当中最有意思的算法是轮询，直接将请求指向许多后端服务器中的一个，并通过 Web 服务器将响应返回给客户端。因此，在上面的例子中，客户端其实并不知道在与哪个后端服务器进行交互。

## **负载均衡** 

又是枯燥的一个名词：负载均衡，不过它很好理解，因为负载均衡本身就是**反向代理**的一个实例。

来看看负载均衡和反向代理的本质区别。在负载均衡中，你必须有 2 个或者更多的后端服务器，但在反向代理中，多台服务器不是必需的，甚至一台后端服务器也能运作。我们再深入点，如果我们有很多来自客户端的请求，负载均衡器会检查每个后端服务器的状态，均匀地分配请求，更快地向客户端发送响应。

## **有状态 vs 无状态应用** 

Okay，在我们开始实践 Nginx 之前，先搞清所有的基本知识！

### **有状态应用**

有状态应用存了一个额外变量，只用来保存服务器中单个实例使用所需的信息。

![](http://5coder.cn/img/8QLK1FxkDNntWyB.jpg)

如图所示，一个后端服务器 *server1* 存储了一些信息，服务器 *server2* 并不存储此信息，因此，客户端 (上图 Bob) 的交互可能会也可能不会得到想要的结果，因为它可能会与 *server1* 或 *server2* 交互。在本例中，*server1* 允许 Bob 查看数据文件，但 *server2* 不允许。因此，虽然有状态应用避免对数据库的多次 API 调用，并且（响应）速度更快，但它可能会在不同的服务器上导致这个（无法得到想要结果）问题。

### **无状态应用**

无状态应用有更多的数据库 API 调用，但当客户端与不同后端服务器的交互时，无状态应用却存在更少的问题。

![](http://5coder.cn/img/XQiwhWptVSuzdvU.jpg)

没明白？简单来说，如果我通过 Web 服务器从客户端向后端服务器 *server1* 发送请求，它将向客户端返回一个令牌，用于任何进一步的访问请求。客户端可以使用令牌并向 Web 服务器发送请求。此 Web 服务器将请求连同令牌一起发送到任意后端服务器，而每个后端服务器都能提供相同的所需结果。

## **Nginx 是什么?** 

Nginx 是网络服务器，到目前为止，我的整个博客一直在用这个网络服务器。老实说，Nginx 这就像个**中间人**。

![](http://5coder.cn/img/v2-0502aeb476680bcae43090ec92467803_b.jpg)

这个图不难理解，它是目前为止所有概念的一个组合。在这里，我们有 3 个后端服务器运行在 3001、3002 和 3003 端口，这些后端服务器都能访问同一个运行在 5432 端口的数据库。

当一个客户端向 `https://localhost` （默认端口 443）发起一个 `GET /employees` 请求时，Nginx 将基于算法向任意后端服务器发送请求，从数据库获取数据并将 JSON 数据返回 Nginx Web 服务器再发送给客户端。

如果我们使用一个诸如轮询这样的算法，它让 *client2* 向 `https://localhost` 发送一个请求，然后 Nginx 服务器会先将请求传到 3000 端口并将响应返回给客户端。对另一个请求，Nginx 会把请求传给 3002 端口，以此类推。

知识储备完成！到这里，你对 Nginx 是什么以及 Nginx 所涉及的术语有了一个清晰的理解。是时候，了解安装和配置技术了。

## **开始安装 Nginx** 

时机到了，如果你了解了上面的概念，可以动手开始 Nginx 实践了。

![img](http://5coder.cn/img/v2-dce888494829e097fdbe8e3695bb056a_b.jpg)

嗯，Nginx 的安装过程对任何系统来说都很简单。我是一个 Mac OSX 用户，所以例子的命令是基于 macOS 的， **[Ubuntu](https://link.zhihu.com/?target=https%3A//ubuntu.com/tutorials/install-and-configure-nginx%232-installing-nginx)**、**[Windows](https://link.zhihu.com/?target=https%3A//www.maketecheasier.com/install-nginx-server-windows/)** 和其他 Linux 发行版操作和例子类似。

```text
$ brew install Nginx
```

只要执行上面这步，你的系统就有 Nginx 了！是不是很神奇！

### **运行 Nginx 如此简单**  

要检查 Nginx 是否运行也很简单。

```text
$ nginx 
# OR 
$ sudo nginx
```

执行上面指令，再打开浏览器并输入 `http://localhost:8080/` 回车查看下，你会看到以下画面！

![img](http://5coder.cn/img/v2-5e6766e81f555711aabf7a1cd1554fba_b.jpg)

## **Nginx 基本配置 & 示例** 

下面，我们通过实操来感受下 Nginx 的魔力。

首先，在本地创建如下的目录结构:

```text
.
├── nginx-demo
│  ├── content
│  │  ├── first.txt
│  │  ├── index.html
│  │  └── index.md
│  └── main
│    └── index.html
└── temp-nginx
  └── outsider
    └── index.html
```

当然，**.html** 和 **.md** 文件中要包含基本信息。

**我们想要得到什么呢？**

这里，我们有两个单独的文件夹 `nginx-demo` 和 `temp-nginx`，每个文件夹都包含静态 HTML 文件。我们将着力在一个公共端口上运行这两个文件夹，并设置我们想要的规则。

回到之前说的，如果要修改 Nginx 默认配置，得修改 `usr/local/etc/nginx` 目录下的 `nginx.conf`文件。我的系统中有 vim，所以在这里用 vim 来更改 Nginx 配置，你可以用自己的编辑器来修改配置。

```text
$ cd /usr/local/etc/nginx
$ vim nginx.conf
```

上面的命令会打开一个 Nginx 默认配置文件，我真的不想直接使用默认配置。因此，我通常的做法是复制这个配置文件，然后对主文件进行更改。这里也不例外。

```text
$ cp nginx.conf copy-nginx.conf
$ rm nginx.conf && vim nginx.conf 
```

上面命令将打开一个空文件，我们将为它添加配置。

1. 添加配置的基本设置。一定要添加 `events {}`，因为在 Nginx 架构中，它通常用来表示 worker 的数量。在这里我们用 `http` 告诉 Nginx 我们将在 **[OSI 模型](https://link.zhihu.com/?target=https%3A//www.forcepoint.com/cyber-edu/osi-model)** 的第 7 层作业。
   这里，我们告诉 Nginx 监听 5000 端口，并指向 main 文件夹中的静态文件。

   ```shell
   http {
   
    server {
      listen 5000;
      root /path/to/nginx-demo/main/; 
      }
   
   }
   
   events {}
   ```

    

2. 接下来我们将为 `/content` 和 `/outsider` URL 添加其他的规则，其中 **outsider** 将指向第一步中提到的根目录之外的目录。
   这里的 `location /content`  表示无论我在叶（leaf）目录中定义了什么根（root），**content** 子 URL 都会被添加到定义的根 URL 的末尾。因此，当我指定 root 为 `root /path/to/nginx-demo/`时，这仅仅意味着我告诉 Nginx 在 `http://localhost:5000/path/to/nginx-demo/content/` 文件夹中显示静态文件的内容。

   ```shell
   http {
   
    server {
        listen 5000;
        root /path/to/nginx-demo/main/; 
   
         location /content {
            root /path/to/nginx-demo/;
         }   
   
         location /outsider {
             root /path/temp-nginx/;
         }
     }
   
   }
   
   events {}
   ```

     酷毙了！现在 Nginx 不仅能定义 URL 根路径，还可以设置规则，这样我们就能阻止客户端访问某个文件了。

    

3. 接下来，我们在主服务器上编写一个规则来防止任意 **.md** 文件被访问。我们可以在 Nginx 中使用正则表达式，因此我们将这样定义规则：

   ```shell
   location ~ .md {
       return 403;
   }
   ```

   

4. 最后，让我们学习下 `proxy_pass` 命令来结束这个章节。我们已经了解了什么是代理和反向代理，在这里我们从定义另一个运行在 8888 端口上的后端服务器开始。现在，我们在 5000 和 8888 端口上运行了 2 个后端服务器。
   我们要做的是，当客户端通过 Nginx 访问 8888 端口时，将这个请求传到 5000 端口，并将响应返回给客户端！

   ```shell
   server {
       listen 8888;
   
       location / {
           proxy_pass http://localhost:5000/;
       }
   
       location /new {
           proxy_pass http://localhost:5000/outsider/;
       }
   } 
   ```

看下，这是所有的配置信息  

```shell
http {

    server {
        listen 5000;
        root /path/to/nginx-demo/main/; 

        location /content {
            root /path/to/nginx-demo/;
        }   

        location /outsider {
            root /path/temp-nginx/;
        }

                location ~ .md {
          return 403;
        }
    }

      server {
        listen 8888;

        location / {
            proxy_pass http://localhost:5000/;
        }

        location /new {
            proxy_pass http://localhost:5000/outsider/;
        }
  }

}

events {}
```

使用 `sudo nginx` 来运行此配置。

## **其他 Nginx 命令** 

1. 首次启动 Nginx Web 服务器。

   ```shell
   $ nginx *#OR* $ sudo nginx
   ```

    

2. 重新加载正在运行的 Nginx Web 服务器。

   ```shell
   $ nginx -s reload*#OR* $ sudo nginx -s reload
   ```

    

3. 停止正在运行中的 Nginx Web 服务器。

   ```shell
   $ nginx -s stop*#OR* $ sudo nginx -s stop
   ```

    

4. 查看系统上运行的 Nginx 进程。

   ```shell
   $ ps -ef | grep Nginx
   ```

   

第 4 条命令很重要，如果前 3 条命令产生了一些问题，通常你可以用第 4 条命令找到所有正在运行的 Nginx 进程并杀死进程，然后重新启动它们。

要杀死一个进程，你需要 PID，再用以下命令杀死它：

```shell
$ kill -9 <PID>#OR $ sudo kill -9 <PID>
```

结束本文之前，声明下，文中我用了些来自 Google 的图片和 **[Hussein Nasser](https://link.zhihu.com/?target=https%3A//www.youtube.com/user/GISIGeometry)** 发布在油管的视频教程。