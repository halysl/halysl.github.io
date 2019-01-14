---
layout: post
title: ssh服务介绍及使用
categories: [ssh, linux]
description: ssh是什么，以及如何使用
keywords: ssh, linux
---

# ssh服务介绍及使用

## 简介
ssh 是个非常通用的服务，但凡用过 Linux 系统的人就不会没使用过这个工具。

SSH (即 Secure Shell)，是一项创建在应用层和传输层基础上的安全协议，为计算机 Shell 提供安全的传输和使用环境。

而 SSH 是目前较可靠，专为远程登录会话和其他网络服务提供安全性的协议。利用 SSH 协议可以有效防止远程管理过程中的信息泄露问题。通过 SSH 可以对所有传输的数据进行加密，也能够防止 DNS 欺骗和 IP 欺骗。

SSH 之另一项优点为其传输的数据可以是经过压缩的，所以可以加快传输的速度。SSH 有很多功能，它既可以代替 Telnet，又可以为 FTP、POP、甚至为 PPP 提供一个安全的“通道”。

## 安装

现在的 ssh 通常指的是开源的OpenSSH，一般而言，Linux 发行版以及 MacOSX 都应该直接可以使用，部分操作系统会默认关闭 ssh 服务。

```shell
# Debian系Linux安装
sudo apt-get install openssh-client  # openssh 客户端
sudo apt-get install openssh-server  # openssh 服务端
```

开启 ssh 服务：

不同操作系统对于服务的启停并不一致，以 ubuntu 为例

```shell
ps -e | grep ssh
# 如果看到 sshd 那说明 ssh-server 已经启动了。
# 如果没有则可以这样启动：
sudo /etc/init.d/ssh start 
# 或者 
service ssh start
```

更多其他操作系统的启停，请直接 Google。

## 使用

ssh 指令有很多的参数，可以实现很多功能。在这里只会提出常用的功能。更多的功能可以去看 [SSH Examples, Tips & Tunnels](https://hackertarget.com/ssh-examples-tunnels/?utm_source=wanqu.co&utm_campaign=Wanqu+Daily&utm_medium=website) 。

### 1、直接连接

```
# 以username用户登陆hostname主机
# username常见的为root，hostname常见的为ip
# example ssh root@192.168.1.1
ssh username@hostname

# 以当前用户登陆hostname主机
ssh hostname

```

### 2、指定端口

```
ssh -p PORT username@hostname
```

<br><br>
好了，结束了，可以使用了。

but，每一次连接都要输那么长的指令，懒癌犯了怎么办。

看别人使用ssh服务可以很短的指令就登陆，并且不用输密码。

为什么在Windows下的xshell工具那么好用，而Linux下那么繁琐，还需要手动输入用户名、密码、端口、ip，能不能放个地方保存一键就调用呢？

这就要深入理解ssh运行的原理了，知道了原理才可以有的放矢。

请看原理篇和配置篇。