---
layout: post
title: 【转载】Linux Locale 设置
categories: [Linux, 转载]
description:
keywords: 
---

# 【转载】Linux Locale 设置

说明： Locale是根据计算机用户所使用的语言，所在国家或者地区，以及当地的文化传统所定义的一个软件运行时的语言环境。

如果 Linux 机器上出现字符乱码的问题，可以优先确定是否因为 Locale 设置不对而导致的，其次再去排查文件本身编码问题。

## Locale 分类

```
- LC_CTYPE：语言符号及其分类
- LC_NUMERIC：数字
- LC_COLLATE：比较和排序习惯
- LC_TIME：时间显示格式
- LC_MONETARY：货币单位
- LC_MESSAGES：信息主要是提示信息,错误信息, 状态信息, 标题, 标签, 按钮和菜单等
- LC_NAME：姓名书写方式
- LC_ADDRESS：地址书写方式
- LC_TELEPHONE：电话号码书写方式
- LC_MEASUREMENT：度量衡表达方式
- LC_PAPER：默认纸张尺寸大小
- LC_IDENTIFICATION：Locale 对自身包含信息的概述 
```

```sh
$ locale
LANG=en_US.UTF-8
LC_CTYPE="en_US.UTF- 8"          #用户所使用的语言符号及其分类
LC_NUMERIC="en_US.UTF- 8"        #数字
LC_TIME="en_US.UTF-8"            #时间显示格式
LC_COLLATE="en_US.UTF-8"         #比较和排序习惯
LC_MONETARY="en_US.UTF-8"        #LC_MONETARY
LC_MESSAGES="en_US.UTF- 8"       #信息主要是提示信息,错误信息, 状态信息, 标题, 标签, 按钮和菜单等
LC_PAPER="en_US.UTF- 8"          #默认纸张尺寸大小
LC_NAME="en_US.UTF-8"            #姓名书写方式
LC_ADDRESS="en_US.UTF-8"         #地址书写方式
LC_TELEPHONE="en_US.UTF-8"       #电话号码书写方式
LC_MEASUREMENT="en_US.UTF-8"     #度量衡表达方式
LC_IDENTIFICATION="en_US.UTF-8"  #对自身包含信息的概述
LC_ALL=
```

## Locale 文件位置

- Locale 定义文件在 `/usr/share/i18n/locales`
- Locale 用户定义文件在 `/usr/lib/locale/`

## Locale 设定的优先级关系

设定 Locale 就是设定 12 大类的 Locale 分类属性，即12个LC_*。

除了这12个变量可以设定以外，为了简便起见，还有两个变量：`LC_ALL` 和 `LANG`。

它们之间有一个优先级的关系：LC_ALL > LC_* >LANG。可以这么说，LC_ALL 是最上级设定或者强制设定，而 LANG 是默认设定值。

- 如果设定了 LC_ALL＝zh_CN.UTF-8，那么不管 LC_* 和 LANG 设定成什么值，它们都会被强制服从 LC_ALL 的设定，成为 zh_CN.UTF-8 
- 假如设定了 LANG＝zh_CN.UTF-8，而其他的 LC_*=en_US.UTF-8，并且没有设定 LC_ALL 的话，那么系统的 Locale 设定以 LC_*=en_US.UTF-8
- 假如设定了 LANG＝zh_CN.UTF-8，而其他的 LC_*，和 LC_ALL 均未设定的话，系统会将 LC_* 设定成默认值，也就是 LANG 的值 zh_CN.UTF-8 
- 假如设定了 LANG＝zh_CN.UTF-8，LC_CTYPE=en_US.UTF-8，其他的 LC_*，和 LC_ALL 均未设定的话，那么系统的 Locale 设定将是：LC_CTYPE=en_US.UTF-8，其余的 LC_COLLATE，LC_MESSAGES 等等均会采用默认值，也就是 LANG 的值，也就是 LC_COLLATE＝LC_MESSAGES＝……＝ LC_PAPER＝LANG＝zh_CN.UTF-8  

## Locale 设定命令

```sh
localedef -c -f UTF-8 -i zh_CN zh_CN.utf8 
export LC_ALL=zh_CN.utf8 
```

上面第一步是用来产生编码文件，这一步不是必须，编码文件一般都存在，运行 `localedef –help` 能查看当前编码文件所在的路径。第二步更改当前的编码为 `zh_CN.utf8`，如果要永久更改，运行：

```sh
echo "export LC_ALL=zh_CN.utf8">> /etc/profile 
```

## 转载信息

原始转载信息已不可查，转载链接为 https://blog.csdn.net/hunanchenxingyu/article/details/37542271。
