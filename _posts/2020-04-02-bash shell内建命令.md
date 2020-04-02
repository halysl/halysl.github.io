---
layout: post
title: bash shell buildin command
categories: [Linux, bash]
description:
keywords: 
---

# bash shell buildin command

这里肤浅的以 bash 为例，实际概念应该是 shell buildin commond。

前几天，突发奇想，Linux 的可执行命令，例如 ls，cat，echo 都是可执行文件，一般在 /bin/ 下。但是 cd 却一直找不到（Ubuntu 18.04 server），通过 find 全盘搜索也找不到。

昨天在处理一个系统环境的问题时，发现 source 也找不到所在路径，就很好奇这到底是怎么了，系统如何知道 cd 或者 source 在哪里，在 path 路径中完全找不到。

在查找资料中，想起了一件事，所谓的 Linux 系统，是指 Linux 内核，而人和 Linux 打交道是通过 shell 实现的。所以 shell 可以更人性化，例如正则批量。而 source 也是 bash 的一个特性，用来导入环境变量。

可以通过 type 判断一个命令属于什么。

```txt
type: type [-afptP] name [name ...]
    Display information about command type.

    For each NAME, indicate how it would be interpreted if used as a
    command name.

    Options:
      -a	display all locations containing an executable named NAME;
    		includes aliases, builtins, and functions, if and only if
    		the `-p' option is not also used
      -f	suppress shell function lookup
      -P	force a PATH search for each NAME, even if it is an alias,
    		builtin, or function, and returns the name of the disk file
    		that would be executed
      -p	returns either the name of the disk file that would be executed,
    		or nothing if `type -t NAME' would not return `file'
      -t	output a single word which is one of `alias', `keyword',
    		`function', `builtin', `file' or `', if NAME is an alias,
    		shell reserved word, shell function, shell builtin, disk file,
    		or not found, respectively

    Arguments:
      NAME	Command name to be interpreted.

    Exit Status:
    Returns success if all of the NAMEs are found; fails if any are not found.
```

```sh
$ type -a cd
cd is a shell builtin
$ type -a source
source is a shell builtin
$ type -a echo
echo is a shell builtin
echo is /bin/echo
```

可以看到 echo 是内建命令，但也是系统命令，那么会使用哪一个呢。

shell 内建命令是指 bash（或其它版本）工具集中的命令。一般都会有一个与之同名的系统命令，比如 bash 中的 echo 命令与 /bin/echo 是两个不同的命令，尽管他们行为大体相仿。当在 bash 中键入一个命令时系统会先看他是否是一个内建命令，如果不是才会查看是否是系统命令或第三方工具。所以在 bash 中键入 echo 命令实际上执行 bash 工具集中的 echo 命令也就是内建命令，而不是 /bin/echo 这个系统命令。

内建命令要比系统论命令有比较高的执行效率。外部命令执行时往往需要fork出（产生出）一个子进程，而内建命令一般不用。

> 扩展：[Shell Builtin Commands](https://www.gnu.org/software/bash/manual/html_node/Shell-Builtin-Commands.html)
