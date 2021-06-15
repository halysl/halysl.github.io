---
layout: post
title: Linux 下使用 swap 文件系统
categories: [Linux, swap]
description:
keywords: 
---

# Linux 下使用 swap 文件系统

- 检查 swap 空间，先检查一下系统里有没有既存的 swap 文件

```
swapon -s
```

如果返回的信息概要是空的，则表示 swap 文件不存在。

- 确定 swap 文件的大小，单位为 M。将该值乘以 1024 得到块大小。例如，64MB 的 swap 文件的块大小是 65536。

- 创建 swap 文件，下面使用 dd 命令来创建 Swap 文件。

```
dd if=/dev/zero of=/swapfile bs=1024 count=4194304
```

```
【参数说明】

- if=文件名：输入文件名，缺省为标准输入。即指定源文件。< if=input file >
- of=文件名：输出文件名，缺省为标准输出。即指定目的文件。< of=output file >
- bs=bytes：同时设置读入/输出的块大小为bytes个字节
- count=blocks：仅拷贝blocks个块，块大小等于bs指定的字节数。
```

- 创建好 swap 文件，还需要格式化后才能使用。运行命令：

```
mkswap /swapfile
```

- 激活 swap ，运行命令：

```
swapon /swapfile
```

- 如果要机器重启的时候自动挂载 swap ，那么还需要修改 fstab 配置。

```
echp '/swapfile   swap   swap    defaults 0 0' >> /etc/fstab
```

当下一次系统启动时，新的 swap 文件就打开了。

- 添加新的 swap 文件并开启后，检查 cat /proc/swaps 或者 free 命令的输出来查看 swap 是否已打开。

- 最后，赋予 swap 文件适当的权限：

```
chown root:root /swapfile 
chmod 0600 /swapfile
```

> tips: 删除SWAP分区

```
$ swapoff  /swapfile  #卸载swap文件
$ 并修改/etc/fstab文件 #从配置总删除
$ rm -rf /swapfile  #删除文件
```
