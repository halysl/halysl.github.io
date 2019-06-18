---
layout: post
title: bumpversion的简单学习
categories: [Python, Python模块, 转载]
description: 使用bumpversion模块简化打版本信息
keywords: python, python module, bumpversion
---

# bumpversion 的简单学习

如果只是闭门造车，写点小脚本的话可以不用在意版本的问题。

但是一旦脚本或者项目需要被他人使用，如果没有版本信息，又出现了 bug，那么你很难定位他使用的是什么版本，这个 bug 到底有没有修复，有了版本信息你可以很确定一些 feather 或者 bug 是否实现。

最简单的版本信息制作，在项目下新建一个 VERSION 文件，在该文件中记录版本号，做了些代码修改就手动修改 VERSION。

但是这样会带来更多问题，你只能在修改过 VERSION 后做个 git commit 才能够更好地跟踪；多个文件会提到版本信息该怎么处理；大版本和 patch 版本如何区分？

bumpversion 横空出世，给上述的问题给了些答案。Bumpversion 是一个简化工程版本号修改的工具，可以通过 pip 安装。使用它可以一键将当前工程的文件中的旧版本号替换成新版本号还可以顺便 Commit 和 打上 Tag（如有需要）。

## 语法

`bumpversion [options] part [file]`

这里面 part 是关键，它可以简化很多事。

## 使用

先看一个简单的例子：

工程里有 main.py 和 Makefile 两个文件。

main.py 打印当前的版本号：

```python
version = '0.0.1'

if __name__ == '__main__':
    print(version)
```

Makefile 将 py 文件压缩起来：

```txt
VERSION = 0.0.1
.PHONY: build
build:
    tar zcvf tellversion-v$(VERSION).tar.gz main.py
```

要使用 Bumpversion 需要在目录里添加 .bumpversion.cfg 文件：

```cfg
[bumpversion]
current_version = 0.0.1
commit = True
tag = True

[bumpversion:file:main.py]
[bumpversion:file:Makefile]
```

配置好 .bumpversion.cfg 后，在工程的目录里运行 `bumpversion patch` 会发现上面三个文件的 0.0.1 都变成了 0.0.2。

再运行 `bumpversion minor` 会发现 0.0.2 变成了 0.1.0 

运行 `git log` 能看到一条 Bump version: 0.0.2 → 0.1.0 的 commit 

运行 `git tag` 会发现多了一个 v0.1.0 的 tag

这一切看起来相当方便了，它是怎么做到的呢？

从 .bumversion.cfg 可以看到，配置文件指定了包含版本号的两个文件和当前版本号，bumpversion 只需要将两个文件中的 0.0.1 替换成 0.0.2 就可以了，而 0.0.1 是变成 0.0.2 还是 0.1.0 则是参数 patch 和 minor 的功劳。Bumversion 默认的版本号格式是 {major}.{minor}.{patch} 每次提升一个版本都要在命令中告知提升哪一part。

实际使用中会遇到两个问题，一个是文件中有多个 0.0.1 这样的字符串，其中只有一部分是需要修改的；另一个是希望可以定制版本号格式。

对于第一个问题 Bumpversion 的方案是配置匹配规则，例如下面例子表示 main.py 文件要求版本号前面有 version = ' 的才进行替换

```cfg
[bumpversion:file:main.py]
search = version = '{current_version}'
replace = version = '{new_version}'
```

对于第二个问题 Bumpversion 提供了配置项设置特定格式，假如需要 1.2.3-beta 这样的版本号，可以这样设置：

```cfg
parse = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(\-(?P<step>[a-z]+))?
serialize = 
    {major}.{minor}.{patch}-{step}
    {major}.{minor}.{patch}

[bumpversion:part:step]
optional_value = release
values = 
    alpha
    beta
    release
```

- parse 使用 [Python的正则语法](https://docs.python.org/2/library/re.html#regular-expression-syntax) 定义如何解析出版本号的每一个部分。 
- serialize 使用 [Python的格式化语法](https://docs.python.org/2/library/string.html#format-string-syntax) 拼凑出新的版本号。 

[bumpversion:part:step] 定义了 step 这一部分的取值，其中 values 是有顺序的。

需要注意的是，在上面这种设置下， 1.2.3 和 1.2.3-release 是一样的， 这时如果 bumpversion step 就会提示错误，因为 release 之后没有下一个 step 版本了。

## 转载信息

- author：两片
- url：https://zhuanlan.zhihu.com/p/34680549
