---
layout: post
title: virtualenv 实际场景使用
categories: [Python, Python模块]
description: python虚拟环境
keywords: python, virtualenv, Linux
---

# virtualenv 实际场景使用

virtualenv 是一个用来创建“独立” python 环境的工具，网上相关的资料相当多，但是很少有基于实际场景来叙述的，而且这个双引号独立也另有所指。

## 下载 virtualenv

virtualenv 已经集成在 python3.3 之后标准库的 venv 模块下，这里只说 3.3 之前的版本，着重说 python2.6 和 python2.7 两个版本下的 virtualenv 使用。

下载方式: `pip install virtualenv`

> tips:虽然理论上可以通过 python2.6 直接装 2.7 甚至 3.x 的python，但是由于版本古老，可能（大概率）python2.6 下的 virtualenv 工具无法使用，因为 python2.6 不支持字典推导式，会报语法错误。尽量使用 python2.7 以上的版本。

> tips2: centos6.x 系统使用的是 python2.6.6，centos7 系统使用的是 python2.7.5。

>> python2.6 安装 pip，可以直接 `wget https://bootstrap.pypa.io/2.6/get-pip.py` 下载 get-pip.py 文件，然后 python get-pip.py 来安装

## 直接使用 virtualenv

用法：
`virtualenv [OPTIONS] DEST_DIR`

可选项(基于virtualenv version：15.2.0)：

|指令|说明|备注|
|---|----|---|
|--version|显示版本|-|
|-h, --help|输出帮助文本|-|
|-v, --verbose|结果详细输出|-|
|-q, --quiet|结果简略输出|-|
|-p PYTHON_EXE, --python=PYTHON_EXE|指定 python 版本，例如：--python=python3.5 将会使用 python3.5 创建虚拟环境。如不指定该选项，则默认指定 python 解释器为(/usr/bin/python)|用得最多的选项。|
|--clear|清除非root用户安装并从头开始。|注：我没用过这个选项，一般装错直接删除目录。|
|--no-site-packages|已过时。仅保留向后兼容性。已成为默认选项。|很多资料显示使用这个参数，在当前版本下已经不需要指定该参数|
|--system-site-packages|为虚拟环境提供 目标python环境 已安装的包|-|
|--always-copy|总是复制文件而不是符号连接。|用的比较多的选项，后面会详细说|
|--relocatable|使一个现有的 virtualenv 环境可重定位。这会修复脚本，并生成相对的所有.pth文件|没用过，但应该会重新适配pth，之前遇到过一个环境路径问题，但只影响pip安装，不影响python使用（前提配置了路径）|
|--no-setuptools|不要在新的virtualenv中安装setuptools|-|
|--no-pip|不要在新的virtualenv中安装pip|-|
|--no-wheel|不要在新的virtualenv中安装wheel|-|
|--extra-search-dir=DIR|此选项允许您提供自己的setuptools或pip版本，而不是virtualenv附带的嵌入式版本。可多次使用。|-|
|--download|从PyPI下载预安装的软件包。|没用过。|
|--no-download, --never-download|不要从PyPI下载预安装的软件包。|没用过。|
|--prompt=PROMPT|为此环境提供备用提示前缀。|激活环境时的显示前缀|
|--setuptools|已过时。仅保留向后兼容性。该选项无用。|-|
|--distribute|已过时。仅保留向后兼容性。该选项无用。|-|
|--unzip-setuptools|已过时。仅保留向后兼容性。该选项无用。|-|

  ### 常用方法和实例

  1. virtualenv test

安装截图：
![](/images/blog/20190213-01.png)

查看lib/python2.6/文件夹：
![](/images/blog/20190213-02.png)

可以看到直接使用的符号连接，这会导致一个问题，那就是虚拟环境迁移到其他主机上就会找不到路径。

  2. virtualenv --always-copy test

直接使用这个指令在 python2.6 环境下无法使用，会出现`OSError: Command /tmp/test/bin/python - setuptools<37 pip wheel<0.30 failed with error code 1`。其实就是版本低了，很多配套模块无法兼容，这里可以手动安装 setuptools 和 pip wheel 解决（没试过，不确定），但没必要这么做了，让我们直接指定 python2.7 以上环境吧。

  3. virtualenv --always-copy -p /tmp/python27/bin/python test

安装截图：
![](/images/blog/20190213-03.png)

查看lib/python2.7/文件夹：
![](/images/blog/20190213-04.png)

可以看到这里不再是符号连接了。那么这样的话就可以迁移环境到其他主机上了吗？

答案是不能，由多种原因。

- glibc 的环境不同
- 虚拟环境仍旧不是一个完整的包

## 一个实际的场景

上面三种场景对于个人开发者已经足够了，只需要用 virtualenv 做环境隔离就行了。

但是现在设想一个复杂的场景。

- 一个 python 写的工程需要在 Linux 上工作
- 解压即可使用，不需安装三方包
- 需要兼容多种发行版

原生的 virtualenv 不能做到，准确说我摸索出来的方法也有点蠢，但确实可以正常工作。

根据复杂场景设想一些解决方案的细节：

- 创建可以直接使用的 python 环境
- 装好三方库
- 为了兼容多个发行版，这里指的是 redhat 6 和 redhat 7，这两者的区别已经够大，但是可以走高版本兼容低版本的路

大致的实现方法为：

- 在你需要兼容的系统列表选择最低级的，为了最小化的 glibc
- 确定一个固定的路径，这边记为 $path
- mkdir $path/python/
- 源码安装python，指令:`./configure --prefix=$path/python --enable-optimizations && make && make install`，源码安装以后会再开一篇，以官方文档为准。
- virtualenv -p $path/python/bin/python venv_name
- source $path/bin/activate
- which python 查看 python 是否已经在虚拟环境中了
- pip install xxx 安装一些三方包
- tar -zcvf 可以打出一个环境包，之后就可以在其他机器上使用了

上面的操作不算复杂，按照我实际的操作，大致需要花费 20 分钟，就可以实现在 redhat 6 和 redhat 7两个系统上随意创建虚拟环境。

因为python源文件已经在包内了，这会导致虚拟环境有些大，未压缩前 163 MB, 压缩后越 34 MB，可以接受的范围。

## 参考文档

- [Virtualenv doc](https://virtualenv.pypa.io/en/latest/)
- [Python开发必备神器之一：virtualenv](http://codingpy.com/article/virtualenv-must-have-tool-for-python-development/)
- [Pipenv & 虚拟环境](https://pythonguidecn.readthedocs.io/zh/latest/dev/virtualenvs.html)
- [解决libc.so.6: version `GLIBC_2.14' not found问题](https://blog.csdn.net/cpplang/article/details/8462768)
- [Error while using a newer version of glibc](https://stackoverflow.com/questions/40932215/error-while-using-a-newer-version-of-glibc)
- [制作python虚拟环境包](https://seekplum.github.io/virtualenv/)
- [pipenv+virtualenv配置全新的python环境
](https://halysl.github.io/2019/01/04/pipenv+ve%E9%85%8D%E7%BD%AE%E5%85%A8%E6%96%B0%E7%9A%84python%E7%8E%AF%E5%A2%83/)