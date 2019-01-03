---
layout: post
title: pipenv+virtualenv配置全新的python环境
categories: [python, pipenv]
description: some word here
keywords: keyword1, keyword2
---

## pipenv+virtualenv配置全新的python环境

如果需要用python写个项目，并且允许其运行在稍低版本的Linux下，需要构建一套完整的虚拟环境，这中间有许多坑，花了一个星期终于打包出来了。

总的来说，首先需要构造完整的python环境，再构造一个虚拟环境以便于启动，打包相应的glibc包，执行指令时用完全地址来运行命令。

/tmp/QDataReport/.lib/glibc-2.14/lib/ld-2.17.so --library-path /tmp/QDataReport/.lib/glibc-2.14/lib:/lib64:/usr/lib64:$LD_LIBRARY_PATH /tmp/QDataReport/.venv/bin/python