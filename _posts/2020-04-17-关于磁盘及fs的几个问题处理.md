---
layout: post
title: 关于磁盘及 fs 的几个问题处理
categories: [Linux]
description:
keywords: 
---

# 关于磁盘及 fs 的几个问题处理

有块磁盘出现了错误，其挂载的分区可以 cd 进入，但无法通过 ls 列出当前目录文件，显示错误为：

```
cannot list ......:Bad message
```

没遇到这个问题，没办法，可能与之前的 dd 操作有关？

查到的资料显示可能是 inode 损坏，那么就尝试清理 inode。

```sh
First list bad file with inode e.g.

$ ls –il
Output

14071947 -rw-r--r-- 1 dba 0 2010-01-27 15:49 -®Å

Note: 14071947 is inode number.

Now Use find command to delete file by inode:
$ find . -inum 14071947 -exec rm -f {} ;
It will find that bad file and will remove it with force i.e remove without prompt.
```

但并不奏效，因为这个目录都无法再列出文件，而不是这个问题提出者遇到的无法 rm 的问题。

先重新格式化再挂 LVM 吧。

## device is busy

```sh
$ sudo umonunt /your/path
umount: /your/path: device is busy,

# 原因是因为有程序在使用 /your/path 目录，我们可以使用 fuser 查看那些程序的进程，
$ sudo fuser -m /your/path
/your/path: 10278c 10279c 10280c 10281c 10282c 10295 10365 18222c
$ sudo fuser -m -v -k -i /your/path
$ sudo umount /your/path 
```

## call failed: Structure needs cleaning.

卸载了磁盘，就应该格式化并重新分区，但会遇到这个问题。

```sh
$ sudo mkfs.ext4 /dev/xxx
call failed: Structure needs cleaning.
```

得，文件系统都崩了，先修复这个吧。

```sh
$ sudo fsck.ext4 /dev/sda[NUMBER]
# sudo fsck.ext4 -y /dev/sda[NUMBER]
```

后面都是水到渠成了。

## 参考

- [How to get rid of “Bad Message” file?](https://forum.manjaro.org/t/how-to-get-rid-of-bad-message-file/94991)
- [Linux fuser 命令详解](https://www.jianshu.com/p/a7d69cc9e704)
- [“Structure needs cleaning” error - cannot mount partition](https://askubuntu.com/questions/910078/structure-needs-cleaning-error-cannot-mount-partition)
