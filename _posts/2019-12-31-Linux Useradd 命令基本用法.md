---
layout: post
title: 【转载】Linux Useradd 命令基本用法
categories: [Linux, 转载]
description:
keywords: 
---

# 【转载】Linux Useradd 命令基本用法

在 Linux 中 useradd 是个很基本的命令，但是使用起来却很不直观。以至于在 Ubuntu 中居然添加了一个 adduser 命令来简化添加用户的操作。本文主要描述笔者在学习使用 useradd 命令时的一些测试结果。

说明：本文中的所有试验都是在 Ubuntu14.04 上完成。

## 功能

在 Linux 中 useradd 命令用来创建或更新用户信息。

useradd 命令属于比较难用的命令 (low level utility for adding users)，所以 Debian 系的发行版中建议管理员使用 adduser 命令。其实 adduser 命令只是一个调用了 useradd 命令的脚本文件。

本文将详细分析群组和家目录相关的选项。并且以实例的方式介绍常用的 useradd 命令写法。

## 语法和基本选项

注意：本文并不是一个完整的文档，所以仅列出部分常用的选项进行说明。

```sh
useradd [option] username

[option]:

-d, --home-dir HOME_DIR 指定用户登入时的目录

-g, --gid GROUP 设置初始群组

-G, --groups GROUPS 添加用户到已有群组

-m, --create-home 自动创建用户的家目录

-M, --no-create-home 不要创建用户的家目录

-N, --no-user-group 不要创建以用户名称为名的群组

-s, --shell SHELL 指定用户登入后所使用的shell

-u, --uid UID 　指定用户ID

-p, --password PASSWORD 设置密码
```

## 细说用户组

首先我们要搞清楚，什么是初始群组？简单来说在 /etc/passwd 文件中，每行的第四个字段指定的就是用户的初始群组。用户登录后立即就拥有了初始群组中的权限。

下面我们通过不同的命令来查看群组选项的用法：

```sh
$ sudo useradd tester1
```

没有使用任何群组相关的参数，默认在创建用户 tester1 的同时会创建一个同名的群组。用户 tester1 的初始群组就是这个新建的群组。

```sh
$ sudo useradd tester2 -N
```

这次我们使用了 -N 选项，即不要生成与用户同名的群组。查看下 /etc/passwd 文件，发现 tester2 用户的初始群组ID是100。这个100是哪来的？有ID为100的群组吗？其实100作为 -N 的默认值是写在配置文件中的。不管有没有ID为100的群组，都是这个值。当然我们也可以通过修改配置文件来改变这个默认值！

```sh
$ sudo useradd tester3 -g sudo
```

sudo 是一个非常有权势的群组，我决定把 tester3 加入到这个群组。好，现在去查看一下 /etc/passwd 和 /etc/group 文件，看看有没有新的群组被创建？ tester3 的初始群组又是谁？这次没有创建与 tester3 同名的群组。用户 tester3 的初始群组变成了 sudo。

```sh
$ sudo useradd tester4 -G sudo
```

和上一条命令相比我们只是把小写的g替换成了大写的G。但结果可相差太多了，请您一定要好好的检查 /etc/passwd 和 /etc/group 文件。因为这次不仅创建了群组 tester4，它还是用户 tester4 的初始群组。和tester1 的唯一不同是 tester4 被加入了 sudo 群组。

在实际的使用中，tester3 和 tester4 的场景都是比较常见的，需要根据实际情况进行区分。

## 细说家目录

Useradd 命令对用户家目录的处理让人困惑，下面我们将通过实验来了解家目录相关的不同选项的使用方法：

```sh
$ sudo useradd tester1
```

让我们重新看看创建用户 tester1 这条命令。它不会为用户 tester1 创建名为 tester1 的目录作为家目录，但是我们打开 /etc/passwd 文件，发现 tester1 的记录中居然包含了家目录 /home/tester1。

```cfg
tester1:x:1005:1005::/home/tester1:
```

这让人不可思议，但这条命令确实是这么实现的。

```sh
# 若要在创建用户的同时创建用户的家目录，必须指定 -m 选项
$ sudo useradd -m tester5
```

```sh
# 我们希望自己指定家目录，此时不生成目录 abc
$ sudo useradd -d /home/abc tester6
```

```sh
# 此时生成目录 abcd，并且目录下默认存在文件
$ sudo useradd -d /home/abcd -m tester7
```

## 常见用例

```sh
$ # Case 1: 创建一个带有家目录并且可以登录 bash 的用户
$ sudo useradd -m -s /bin/bash tester1

$ # Case 2: 指定创建用户家目录的路径，/home/xxx目录会被创建
$ sudo useradd -m -d /home/xxx tester2

$ # Case 3: 创建一个没有家目录且不能登录的用户
$ sudo useradd -s /sbin/nologin tester3

$ # Case 4: 创建时把用户加入不同的用户组，注意过个组名使用逗号分隔，不能有空格
$ sudo useradd -m -G xxx,sudo tester4
```

## 转载信息

- 作者：sparkdev
- 出处：http://www.cnblogs.com/sparkdev/
- 本文版权归作者和博客园共有，欢迎转载，但未经作者同意必须保留此段声明，且在文章页面明显位置给出原文连接，否则保留追究法律责任的权利。
