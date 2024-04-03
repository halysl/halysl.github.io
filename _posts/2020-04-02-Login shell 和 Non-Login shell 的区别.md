---
layout: post
title: Login shell 和 Non-Login shell 的区别
categories: [Linux]
description:
keywords: 
---

# Login shell 和 Non-Login shell 的区别

[Difference between Login shell and Non login shell](http://howtolamp.com/articles/difference-between-login-and-non-login-shell#login)

shell 程序，例如 Bash，使用了一系列启动脚本去创建环境。每一个脚本有独特的作用，对登陆环境有不同的影响。后续执行的脚本的可以覆盖先前执行的脚本产生的值。

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

## 附录：文件说明

假设用户使用的是BASH。

### /etc/profile

此文件为系统的环境变量，它为每个用户设置环境信息，当用户第一次登录时，该文件被执行。并从 `/etc/profile.d` 目录的配置文件中搜集 shell 的设置。这个文件，是任何用户登陆操作系统以后都会读取的文件（如果用户的 shell 是 csh 、tcsh 、zsh，则不会读取此文件），用于获取系统的环境变量，只在登陆的时候读取一次。

### /etc/bashrc

在执行完 /etc/profile 内容之后，如果用户的 SHELL 运行的是 bash ，那么接着就会执行此文件。另外，当每次一个新的 bash shell 被打开时, 该文件被读取。每个使用 bash 的用户在登陆以后执行完 /etc/profile 中内容以后都会执行此文件，在新开一个 bash 的时候也会执行此文件。因此，如果你想让每个使用 bash 的用户每新开一个 bash 和每次登陆都执行某些操作，或者给他们定义一些新的环境变量，就可以在这个里面设置。

### ~/.bash_profile

每个用户都可使用该文件输入专用于自己使用的 shell 信息。当用户登录时，该文件仅仅执行一次，默认情况下，它设置一些环境变量，最后执行用户的 .bashrc 文件。单个用户此文件的修改只会影响到他以后的每一次登陆系统。因此，可以在这里设置单个用户的特殊的环境变量或者特殊的操作，那么它在每次登陆的时候都会去获取这些新的环境变量或者做某些特殊的操作，但是仅仅在登陆时。

### ~/.bashrc

该文件包含专用于单个人的 bash shell 的 bash 信息，当登录时以及每次打开一个新的 shell 时, 该该文件被读取。单个用户此文件的修改会影响到他以后的每一次登陆系统和每一次新开一个 bash 。因此，可以在这里设置单个用户的特殊的环境变量或者特殊的操作，那么每次它新登陆系统或者新开一个 bash ，都会去获取相应的特殊的环境变量和特殊操作。

### ~/.bash_logout

当每次退出系统( 退出bash shell) 时, 执行该文件。

### ~/.bash_aliases

默认在 ~/.bashrc 里会调用这个文件，导入系统环境。该文件保存别名信息。
