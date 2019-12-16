---
layout: post
title: 一些技巧
categories: [Linux, Python]
description: some word here
keywords: Linux, Python, skill
---

# 一些技巧

这里是工作中，学习中遇到的一些痛点技巧，难度不大，但是很杂，先记个笔记做下索引搜索，等技巧多了，可以写个工具集。

## Linux方面

### 设置dns

```shell
echo 'nameserver 114.114.114.114' >> /etc/resolv.conf
service network restart
ping smtp.163.com
```

###  类似于Windows下的tree指令

```shell
find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
```

### 杀死多进程

```shell
# 主要是xargs的使用
ps -aux|grep $keyword|grep -v grep | awk '{print $2}' | xargs kill -9
```

### 查看指定端口状态

```shell
lsof -i:port
netstat -anp|grep port
```

### 统计字符出现的次数

```shell
grep -o objStr  filename|wc -l
grep -o 'objStr1\|objStr2'  filename|wc -l
```

### 统计文件夹下的文件数目

```shell
# 统计当前目录下文件的个数（不包括目录）
ls -l | grep "^-" | wc -l
# 统计当前目录下文件的个数（包括子目录）
ls -lR| grep "^-" | wc -l
# 查看某目录下文件夹(目录)的个数（包括子目录）
ls -lR | grep "^d" | wc -l
```

### 查找文件内容

```shell
# 查找某文件中的xxx
grep 'xxx'  filename
# 查找当前文件夹中的所有文件中的xxx
find . |xargs grep 'xxx'
```

### 获取终端宽度

```shell
$ echo $LINES  # 查看终端的高度
$ echo $COLUMNS  # 查看终端的宽度
$ tput lines  # 查看终端的高度
$ tput cols  # 查看终端的宽度
$ stty size  # 同时返回高度和宽度
$ resize [-cu][-s <列数> <行数>]
## -c 　就算用户环境并非C Shell，也用C Shell指令改变视窗大小。
## -s <列数> <行数> 　设置终端机视窗的垂直高度和水平宽度。
## -u 　就算用户环境并非Bourne Shell，也用Bourne Shell指令改变视窗大小。
```

```python
>>> import shutil
>>> res = shutil.get_terminal_size()
>>> print(res.lines, res.columns)  # 输出终端的高度和宽度
```

### 查看内核版本和发行版本

```shell
$ uname -a # 内核版本
$ cat /etc/redhat-release # 查看 Redhat 发行版
$ cat /etc/issue # 查看 Ubuntu 发行版
```

### 在 Ubuntu 中使用 NTP 进行时间同步

https://linux.cn/article-8091-1.html

### Kill User Session

```shell
$ sudo pkill -9 -u username
$ ps -fp $(pgrep -d, -u userNameHere)
```

## vi
[vi块操作](https://blog.csdn.net/sinat_36053757/article/details/78183506)
### 多行选中并在开头加字符
```vi
V # 进入可视化行
j/k # 选择需要修改的行
:%s/^/modiStr # 开头加字符
:%s/$/modiStr % 结尾加字符
```

## python

### 打包过滤脚本
```python
# -*- coding=utf-8 -*-

import os
import tarfile
import re

curr_path = os.path.dirname(os.path.abspath(__file__))

tar = tarfile.open("test.tar.gz", "w:gz")

for root, dir, files in os.walk(os.getcwd()):
    for file in files:
        fullpath = os.path.join(root, file)
        if re.search(".git|.ipynb|.idea|.tar.gz|tar_func.py|.pyc|.log|", fullpath):
            continue
        else:
            print(fullpath)
            tar.add(fullpath)
tar.close()
```

## shell

### 显示执行过程

方法一：

```shell
#!/bin/sh下增加一行
set -x
```

方法二：以下面的方式执行脚本

```shell
$ bash -x strtst.sh 
```
## Git

- [git-quick-stats:快速查看git统计信息](https://github.com/arzzen/git-quick-stats#macos-homebrew)
- [gitstats:生成图表（丑）](https://github.com/hoxu/gitstats)
- [gitinspector:生成图表（帅）](https://github.com/ejwa/gitinspector)

## 杂项

- [base64加解密](https://www.bejson.com/enc/base64/)
- [Shell脚本编程30分钟入门](https://github.com/qinjx/30min_guides/blob/master/shell.md)
- [json校验](https://www.bejson.com/)
- [在线正则表达式测试](http://tool.oschina.net/regex)
