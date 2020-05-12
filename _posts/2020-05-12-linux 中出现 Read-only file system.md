---
layout: post
title: Linux 中出现 Read-only file system
categories: [Linux]
description:
keywords: 
---

# Linux 中出现 Read-only file system

当 Linux 操作系统启动出现 root 用户也无法进行任何的文件写操作时，无论什么用户(包括 root)写文件保存或者删除文件，且对操作文件或目录都有写权限时，还任然报错: `E212: Can't open file for writing 或者 Read-only file system。`

这种情况下，已经不是权限的问题了，更大的可能是因为当前的文件系统进入了只读模式，所以不能进行写操作。

## 重新挂载根目录

```
# 让“/”根文件系统重新挂载并有可读写模式
$ sudo mount -o remount rw /
```

## 修复磁盘

```
# 对报错分区进行检测并尝试修复
$ sudo fsck -y /dev/sda1
```

## 转载信息

版权声明：本文为CSDN博主「Aidon-东哥博客」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u010839779/java/article/details/77062347
