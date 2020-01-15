---
layout: post
title: Ubuntu 安装 ftp 服务
categories: [Linux, Network, Ubuntu]
description:
keywords: 
---

# Ubuntu 安装 ftp 服务

这是一个很简单的需求，相关的博文也相当多，安装的过程非常简单，但是配置相关的说明有些分散。

主要几步：

- 可选：创建目录
- 安装服务
- 写配置文件
- 访问服务

最麻烦的在于 写配置文件，ftp 通过文本格式的配置文件实现了权限管理，用户管理，目录管理和网络管理。

## 安装服务

```sh
$ apt-get install vsftpd
```

vsftpd 意思为 “very secure FTP daemon(非常安全的FTP进程)”，当然只有更安全没有最安全。

那它到底安全在哪里呢，主要体现在以下两点：

- 权限控制，vsftpd 以一般用户登录，用户权限相对较小，对于系统就越安全，对于用户需要的系统级指令大部分被整合到 vsftpd 中了，用户不需要申请更高权限就足以完成绝大部分 ftp 指令；此外对于 ftp 本身内部的读写控制，vsftpd 也足以通过配置文件控制了；
- 目录限制，vsftpd 通过 chroot 可以控制 ftp 登录用户所能看到的目录范围，即限定 ftp 用户看到的根目录为系统中某一个目录，如此一个 ftp 用户就除了看到自己的 ftp 根目录不能看到其他比如配置文件、系统更目录等，保护了系统。

## 写配置文件

从安全的角度来看，尽量不要启用匿名；同时尽量使用一个统一的目录，方便管理（这样的考虑是因为将 ftp 作为一个统一的文件传输管理系统，如果每个用户单独目录就很难提到共享这个概念）。

还有个 主动模式/被动模式 的区别，具体的区别可以参考 [Ubuntu 14.04 配置vsftpd实现FTP服务器 - 通过FTP连接AWS](https://www.jianshu.com/p/9ea295f9e513) 的第 2 章。我的需求是使用被动模式。

从上述所说，重要的配置如下：

```sh
anonymous_enable=NO  # 不允许匿名用户登录
local_enable=YES  # 允许本地用户组的用户登录

write_enable=YES  # 允许本地用户上传文件
local_root = /home/xxxx/ftp  # 本地用户登入时，将被切换到定义的目录下，默认值为各用户的家目录，通过这个指定目录，该目录需要手动创建


#使用被动模式
pasv_enable=YES
pasv_min_port=1024
pasv_max_port=1048
pasv_address=你的访问IP（服务器外网IP）
```

更多的配置信息可以参考文末的参考链接前两项。

## 访问服务

- 方法一：打开浏览器，输入 ftp://ip，输入账号密码登陆，可以查看并下载，但无法上传数据
- 方法二：打开终端，输入 ftp ip，输入账号密码登陆，可以做所有操作

## 参考链接

- [Ubuntu 14.04 配置vsftpd实现FTP服务器 - 通过FTP连接AWS](https://www.jianshu.com/p/9ea295f9e513)
- [Ubuntu使用vsftpd搭建ftp服务器](https://cndaqiang.github.io/2017/09/27/ubuntu-vsftps/)
- [ubuntu LTS下搭建FTP服务器](https://www.jianshu.com/p/d8e43ed427cc)
- [ubuntu 16.04 搭建ftp服务器](https://blog.csdn.net/lj402159806/article/details/78209103)
- [Ubuntu16.04配置ftp服务器](https://blog.csdn.net/yehuohan/article/details/51864863)
- [Linux（Ubuntu 16.04）搭建ftp服务器(最简单版)](https://blog.csdn.net/null_qiao/article/details/76919234)
