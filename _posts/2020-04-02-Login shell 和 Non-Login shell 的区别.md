---
layout: post
title: Login shell 和 Non-Login shell 的区别
categories: [Linux]
description:
keywords: 
---

# Login shell 和 Non-Login shell 的区别

[Difference between Login shell and Non login shell](http://howtolamp.com/articles/difference-between-login-and-non-login-shell#login)

shell 程序，例如 Bash，使用了一系列启动脚本去创建环境。每一个脚本有独特的作用，对登陆环境有不同的影响。后续执行的脚本的可以覆盖先前执行的急哦啊笨产生的值。

对于登录Shell和非登录Shell，启动配置有所不同。

1. Login shells
2. Non login shells

## Login shells

使用 /bin/login 通过读取 /etc/passwd 文件成功登录后，将启动 Login shell。登录 shell 程序是在登录会话时在用户 ID 下执行的第一个过程。Login 进程告诉 shell 程序遵循以下约定：传递参数0（通常是 shell 程序可执行文件的名称，例如 bash），并带有“-”字符。例如，对于Bash shell，它将是-bash。

当 bash 被调用为 Login shell：

- -> `登陆进程` 调用 `/etc/profile`
- -> `/etc/profile` 调用 `/etc/profile.d/` 下的脚本
- -> `登陆进程` 调用 `~/.bash_profile`
- -> `~/.bash_profile` 调用 `~/.bashrc`
- -> `~/.bashrc` 调用 `/etc/bashrc`

Login shell 出现包括以下情况：

- 显式调用 login 程序，从而创建的 shell

例如：

```sh
$ su - 
$ su -l 
$ su --login 
$ su USERNAME - 
$ su -l USERNAME 
$ su --login USERNAME 
$ sudo -i
```

- 通过登录程序，例如连接主机的 tty 界面，一般都是Login： 等待

可以通过以下过程识别 Login shell。

```sh
$ echo $0
-bash
```

例如 `-bash`, `-su`。


## Non Login shells

一个 Non Login shell 并不通过 login 进程开始。在这种情况下，程序仅传递 shell 可执行文件的名称。例如，对于 Bash shell，它将仅仅是 bash。

当 bash 被调用为 Non Login shell：

- -> `Non-login` 进程调用 `~/.bashrc`
- -> `~/.bashrc` 调用 `/etc/bashrc`
- -> `/etc/bashrc` 调用 `/etc/profile.d/ 下的脚本`

Non Login shell 出现包括以下情况：

- 通过 su 命令创建的 shell
- 图形终端
- 可执行脚本
- 任何其他bash实例

可以通过以下过程识别 Non Login shell。

```sh
$ echo $0
bash
```

例如 `bash`, `su`。
