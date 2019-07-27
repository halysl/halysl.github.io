---
layout: post
title: windows7 下安装 utunbu 的几件头疼事
categories: [Linux, 逃离CSDN]
description: windows7 下安装 utunbu 的几件头疼事
keywords: Linux, 逃离CSDN
---

# windows7 下安装 utunbu 的几件头疼事

## 一、系统及硬件说明

- Windows版本：Windows7旗舰版
- Linux版本：ubuntukylin-16.10-desktop-amd64

![](https://img-blog.csdn.net/20170318190358352?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvQ2xvdWRfU3RyaWZlMA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

我的笔记本上有两块硬盘，其中一块是 1000GB 机械硬盘，分为五个区，另一块是固态 120GB，用作装系统。

大致的分区情况如下：

![](https://img-blog.csdn.net/20170318185308518?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvQ2xvdWRfU3RyaWZlMA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

## 二、安装双系统前的准备

我的想法是，将 sda5 中的空间分出来 50G 用于安装 ubuntu，中间的什么压缩卷，转移数据就不赘述了，分好的空间就开始做 U 盘 Linux 系统盘，使用的软件是软碟通，然后等待刻录完成，开机驱动选择U盘启动，然后就开始了安装之旅，噩梦刚刚开始。

## 三、安装过程

一路确定下去，直到分区的时候，选择自定义分区，推荐 /boot 设置在最前面，然后是 swap 分区，/ 分区，/home 分区，具体分多少看个人喜好，然后就是等待。过了一会儿安装好了，重启。

## 四、设置开机引导

推荐在 Windows 下进行开机引导，我使用的是 easybcd，添加新条目的时候发现不对劲，按照网上的教程，这时候 /boot 分区前面应该有 Linux 字样，但是我这样安装之后并没有 Linux 字样，但是死马当活马医，还是把 /boot 分区作为引导项，然后重启。

![](https://img-blog.csdn.net/20170318191044152?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvQ2xvdWRfU3RyaWZlMA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

重启之后，有两个登录选项，选择 linux 不能进入 ubuntu，而是进入 grub 引导，难道是我安装的时候分区错误吗，然后我重新安装了一次，仍然在 sda5 上安装了几次，但都是没出现过 Linux 字样。

## 五、思考

为什么我按照网上的教程多次实践也查了很多原因，看了《Linux鸟哥的私房菜》第三版里 p105 4.4.2 旧主机有两块以上硬盘多重引导该怎么办。开机流程是这样的，BIOS 启动，然后看下用户设定的第一启动盘是什么硬件，然后把权利交给该硬件（前面用U盘启动就是改了这个顺序）。我这个情况，就是给了 sdb 里的 mbr，但是之前用 easybcd 做的引导应该就是把 /boot 传输给 sdb 里的 mbr，让用户开机的时候可以选择，那么为什么进不去 Linux 呢。

我思考了下我机器所处的环境到底有什么不同，第一是有两块硬盘，第二是 sdb 是系统盘，而我把 Linux 装在了第一块硬盘，不知道这是不是有什么关系，说干就干。新的设想是把两个系统都装在sdb上，格式化 ssd，先把 Windows7 重新安装，然后直接安装 Ubuntu。

这次成功使用 easybcd 做好了引导，万事俱备。已成功开启了 ubuntu。

## 六、装好之后

切换到 Ubuntu 后连接无线网，输入账号密码，成功登陆。然后重启电脑进入 win7，意外地发现 win7 上连接上那个无线网络但是无法正确访问网络，手动更改 ip 和 dns 设置也并没有用，最后的解决方法是重装了 Windows 的网卡驱动。具体的原因不知道，估计可能是因为双系统用的同一块网卡，写入网络信息之类的，诶，计算机网络和tcp/ip协议还是要好好学习。
