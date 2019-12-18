---
layout: post
title: 【转】Mac 上制作 Linux 系统 U 盘安装盘
categories: [Linux, MacOS]
description: Mac 上制作 Linux 系统 U 盘安装盘
keywords: 
---

# 【转】Mac 上制作 Linux 系统 U 盘安装盘

Mac 下将 iso 镜像写入 U 盘可使用命令行工具 dd，操作如下：

- 找出 U 盘挂载的路径，使用如下命令：`diskutil list`
- 将 U 盘 unmount（将 N 替换为挂载路径）：`diskutil unmountDisk /dev/disk[N]`
- 写入 U 盘：`sudo dd if=iso_path of=/dev/rdisk[N] bs=1m`，rdisk 中加入 r 可以让写入速度加快

## 查看所有的disk

```sh
$ diskutil list
/dev/disk2 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     Apple_partition_scheme                        *15.7 GB    disk2
   1:        Apple_partition_map                         4.1 KB     disk2s1
   2:                  Apple_HFS                         2.6 MB     disk2s2
```

## 解除其挂载

```
$ diskutil unmountDisk /dev/disk2
Unmount of all volumes on disk2 was successful
```

## 用 dd 命令将 iso 写入

```sh
$ sudo dd if=/Users/light/media/CentOS-7-x86_64-DVD-1908.iso of=/dev/rdisk2 bs=1m
```

## 利用 pv 监控克隆进度

使用 homebrew 安装 pv 工具，之后使用以下的命令来实现进度条的显示：

```sh
$ brew install pv
==> Downloading https://mirrors.aliyun.com/homebrew/homebrew-bottles/bottles/pv-1.6.6.high_sierra.bottle.tar.gz
######################################################################## 100.0%
==> Pouring pv-1.6.6.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/pv/1.6.6: 5 files, 75.5KB
```

```sh
$ sudo pv -cN source < /Users/light/media/CentOS-7-x86_64-DVD-1908.iso | sudo dd of=/dev/rdisk2 bs=4m
source: 1.47GiB 0:05:49 [5.00MiB/s] [===================>                                         ] 33% ETA 0:11:22
```

sudo pv -cN source < /Users/kacperwang/Downloads/CentOS-7-x86_64-Everything-1511.iso | sudo dd of=/dev/disk2 bs=4m

## 操作完毕后将 U 盘弹出

```sh
$ diskutil eject /dev/disk2
Disk /dev/disk2 ejected
```
