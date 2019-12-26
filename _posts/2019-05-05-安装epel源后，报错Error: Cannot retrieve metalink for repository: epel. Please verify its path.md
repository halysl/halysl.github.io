---
layout: post
title: 【转载】安装epel源后，报错Error
categories: [Linux]
description: Cannot retrieve metalink for repository epel. Please verify its path
keywords: Linux, 转载, Centos
---

# 【转载】安装epel源后，报错Error: Cannot retrieve metalink for repository: epel. Please verify its path..

## 问题
`wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm`

`rpm -ivh epel-release-latest-6.noarch.rpm`

`yum -y install iftop`

>报错：Error: Cannot retrieve metalink for repository: epel. Please verify its path and try again

**是因为/etc/yum.repos.d/epel.repo配置文件中源地址没有生效**

## 解决方案

`vim /etc/yum.repos.d/epel.repo`

```
[epel]

name=Extra Packages for Enterprise Linux 6 - $basearch

#baseurl=http://download.fedoraproject.org/pub/epel/6/$basearch

mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=$basearch

failovermethod=priority

enabled=1

gpgcheck=1

gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
```


修改成：

```
[epel]

..

baseurl=http://download.fedoraproject.org/pub/epel/6/$basearch

#mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=$basearch

...
```

保存退出后，清理源

`yum clean all`

`yum -y install iftop`

既可以成功安装。

## 转载信息
## 转载信息

- 作者：jalyzjs
- 来源：51CTO
- 原文：https://blog.51cto.com/jschu/1750177
- 版权声明：本文为博主原创文章，转载请附上博文链接！
