---
layout: post
title: pipenv+virtualenv配置全新的python环境
categories: [python, pipenv]
description: 让python项目运行在任意Linux上
keywords: python, pipenv, linux
---

### 提示信息说三遍，本文最终的结果并不如人意，只是一些探索的过程记录。问题在于：当使用paramiko库时会提示openssh服务，而如果继续封装就有点违背当初的想法，应该有更优秀的解决方案。


### 提示信息说三遍，本文最终的结果并不如人意，只是一些探索的过程记录。问题在于：当使用paramiko库时会提示openssh服务，而如果继续封装就有点违背当初的想法，应该有更优秀的解决方案。

### 提示信息说三遍，本文最终的结果并不如人意，只是一些探索的过程记录。问题在于：当使用paramiko库时会提示openssh服务，而如果继续封装就有点违背当初的想法，应该有更优秀的解决方案。

## pipenv+virtualenv配置全新的python环境

如果需要用python写个项目，并且允许其运行在稍低版本的Linux下，需要构建一套完整的虚拟环境，这中间有许多坑，花了一个星期终于打包出来了。

总的来说，

- 首先需要构造完整的python环境
- 再构造一个虚拟环境以便于启动
- 打包相应的glibc包
- 执行指令时用绝对路径来运行命令。

全篇遇到了不少坑，主要依据这篇文章进行操作[制作python虚拟环境包](https://seekplum.github.io/virtualenv/)，大体上没有什么问题，但是更注重于操作，而缺少一些解释，以及没有glibc包的打包过程。

### 创建完整的python环境

如果只是用virtualenv或者pipenv等工具直接创建虚拟环境，那么虚拟环境中的很多.py文件都只是软连接指向系统自带的python环境对应的.py文件。

这样的话，即便虚拟环境ok了，在另一个python版本不对或者没有python环境的机器上就会找不到对应的位置而报错。

可以通过查看虚拟环境中的lib目录得知指向的位置，

![](http://pkxuy5e31.bkt.clouddn.com/virtual_env_ref_to_system_env.png)

所以在创建虚拟环境前需要创建完整的python环境。

由于那篇博客关于安装环境说得足够详细，所以这里不再赘述，请直接从[制作python虚拟环境包](https://seekplum.github.io/virtualenv/)的`Centos换源`到`安装python`进行操作，相关依赖最好直接安装好，包括zlib和openssl相关的依赖，前者主要作用在打包压缩，后者主要作用在加密解密。

> tips:虽然理论上可以通过python2.6直接装2.7甚至3.x的python，但是由于版本古老，可能（大概率）python2.6下的virtualenv工具无法使用，因为python2.6不支持字典推导式，会报语法错误。尽量使用python2.7以上的版本。

> tips2: centos6.x系统使用的是python2.6.6，centos7系统使用的是python2.7.5。

> tips3: MacOSX上的/tmp并不是/tmp，而是/private/tmp。

>> python2.6安装pip，可以直接wget https://bootstrap.pypa.io/2.6/get-pip.py下载get-pip.py文件，然后python get-pip.py来安装

### 构造一个虚拟环境

在指定的目录创建好完整的python环境了，为什么还需要构造虚拟环境？

以我（浅薄的眼光）看来，安装好的python环境可以通过绝对路径调用，但是很多环境还是会调用系统自身的，这样会造成一种紊乱，我们需要用虚拟环境打包这个完整环境，给它换个皮，创建个单独的空间。

由于那篇博客关于安装虚拟环境说得足够详细，所以这里不再赘述，请直接看[制作python虚拟环境包](https://seekplum.github.io/virtualenv/)的`虚拟环境操作`进行操作，一般情况下会安装的特别快，如果出现了`ImportError: No module named zlib`那就是缺少zlib环境。

还记得前文提到的，“虚拟环境中的很多.py文件都只是软连接指向系统自带的python环境对应的.py文件”，此时我们再去看下虚拟环境的lib目录，可以看出虽然有指向，但指向的是之前安装的完整环境，所以理论上可以在任何Linux环境上使用。
![](http://pkxuy5e31.bkt.clouddn.com/virtual_venv_ref_to_now_dir.png)

### 打包glibc环境

一般情况下，创建完虚拟环境，就可以直接上传到测试机器，然后激活环境`source .venv/bin/activate`，然后执行项目入口文件就行了`python run.py`，如果不出错，那么就可以了，以下的步骤不用看了。

但是我的测试机系统是rhel6.7，会出现一个`python: /lib64/libc.so.6: version 'GLIBC_2.14' not found (required by python)`错误。

既然是/lib64/libc.so.6下报的错误，那么应该和glibc版本有关系。

通过查找资料，这篇文章[解决libc.so.6: version \`GLIBC_2.14' not found问题](https://blog.csdn.net/cpplang/article/details/8462768)写得足够详细，`原因是系统的glibc版本太低，软件编译时使用了较高版本的glibc引起的`，解决方法上面的文章也可以解决，注意将glib安装到之前设置的文件夹下，方便打包。

> tips:一般我会将虚拟环境安装在.venv下，而将lib相关的包安装在.lib下

### 用绝对路径来运行命令

既然glibc也打包了，那么上传到测试机器，如何让python使用高版本的glibc而不使用系统自带的glibc？

直接思路当然是

```
export LD_LIBRARY_PATH=/YourDir/.lib/glibc-2.14/lib:$LD_LIBRARY_PATH
```

强制先使用自己制定的glibc，某些时候可以成功，某些时候会报另外一种错，

```
python: error while loading shared libraries: __vdso_time: invalid mode for dlopen(): Invalid argument
```

通过查找StackFlow，发现了一个人的遭遇和我一摸一样，[Error while using a newer version of glibc](https://stackoverflow.com/questions/40932215/error-while-using-a-newer-version-of-glibc)，给出的理由是export LD\_LIBRARY_PATH覆盖的范围太广了，python不知道该使用哪一个glibc，按照给出的解决方案，测试过了并没有什么用。

之后在知乎找到了调用方法，可见[10859 在 glibc < 2.17 的系统上安装 TensorFlow](https://zhuanlan.zhihu.com/p/33059558)中的`调用新版 glibc`这一节，直接使用自己打包的glibc去执行指令，这里最好使用绝对路径去执行。

```
# 这里的GLIBC_DIR指的是glibc安装的位置
$GLIBC_DIR/ld-2.17.so --library-path $GLIBC_DIR:/lib64:$LD_LIBRARY_PATH <command>

# 注意， --library-path后面跟的参数可以更多点，例如$GLIBC_DIR:/lib64:/usr/lib64:$LD_LIBRARY_PATH等等
```

假设此时执行python会报错，
`ImportError: cannot import name md5`，这是因为--library-path范围不够广，查找下对应的openssl在哪里，添加到--library-path参数就行了。

### 参考链接:

  - [制作python虚拟环境包](https://seekplum.github.io/virtualenv/)
  - [解决libc.so.6: version \`GLIBC_2.14' not found问题](https://blog.csdn.net/cpplang/article/details/8462768)
  - [Error while using a newer version of glibc](https://stackoverflow.com/questions/40932215/error-while-using-a-newer-version-of-glibc)
  - [10859 在 glibc < 2.17 的系统上安装 TensorFlow](https://zhuanlan.zhihu.com/p/33059558)
  - [Python 2.7 not working anymore: cannot import name md5](https://stackoverflow.com/questions/47884422/python-2-7-not-working-anymore-cannot-import-name-md5)