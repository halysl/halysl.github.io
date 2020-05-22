---
layout: post
title: redhat 系使用 scl 工具临时使用高级开发工具
categories: [Linux]
description:
keywords: 
---

# redhat 系使用 scl 工具临时使用高级开发工具

最近在做一次编译任务中，出现了 cc 指令错误，显示未找到 a.c 文件，猜测可能因为 gcc 版本问题。检测到可以在 Ubuntu 18.04 正常编译使用的 gcc 版本是 7.5，而基于 Centos7 的 Aliyun Linux 2.1903 却还是 4.8 版本。先升级 gcc 版本再测试编译问题。

在 redhat 系中升级 gcc 有两种方案，一种是下载源码进行编译，另外一种是借助 scl 工具。前者不推荐，一是因为编译速度慢，二是因为编译可能出现各种问题需要手动处理。后者 SCL 软件集（Software Collections）是为了给 RHEL/CentOS 用户提供一种以方便、安全地安装和使用应用程序和运行时环境的多个（而且可能是更新的）版本的方式，同时避免把系统搞乱。

## 普通 RHEL/Centos 使用 scl

```
# 安装 scl 源：
$ yum install centos-release-SCL scl-utils-build

# 查看从 scl 中安装的包的列表：
$ scl –list

# 列出 scl 源有哪些包可以用：
$ yum list all --enablerepo='centos-sclo-rh'

# 安装高版本的 gcc、gcc-c++
yum install devtoolset-7-gcc devtoolset-7-gcc-c++
# devtoolset-3: gcc 4.9
# devtoolset-4: gcc 5
# devtoolset-6: gcc 6
# devtoolset-7: gcc 7
# devtoolset-8: gcc 8

# 测试下是否成功
$ scl enable devtoolset-7 'gcc --version'
gcc (GCC) 7.3.1 20180303 (Red Hat 7.3.1-5)
Copyright (C) 2017 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

## Aliyun Linux 2.1903 使用 scl

```
# 先安装scl-utils
$ yum install -y scl-utils
# 打开YUM仓库支持
$ yum install -y alinux-release-experimentals
# 从YUM源安装您需要的软件包，以下示例命令同时安装了SCL插件方式支持的所有开发工具包
$ yum install -y devtoolset-7-gcc devtoolset-7-gdb devtoolset-7-binutils devtoolset-7-make
# 运行相关的SCL软件
$ scl enable devtoolset-7 'gcc --version'
gcc (GCC) 7.3.1 20180303 (Red Hat 7.3.1-5)
Copyright (C) 2017 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

## 使用高版本的开发工具

- 使用绝对路径
- 添加可执行文件路径到 PATH 环境变量
- 使用官方推荐的加载命令：scl enable devtoolset-x bash, x为要启用的版本
- 执行安装软件自带的脚本： source /opt/rh/devtoolset-x/enable，x为要启用的版本

推荐后两种方案。

```
# 单次编译
$ scl enable devtoolset-7 `make`

# 多次编译
$ source /opt/rh/devtoolset-7/enable
$ make a
$ make b
```

## 参考资料

- [CentOS 7上升级/安装gcc](https://juejin.im/post/5d0ef5376fb9a07ef63fe74e)
- [Aliyun Linux 2概述](https://help.aliyun.com/document_detail/111881.html)
