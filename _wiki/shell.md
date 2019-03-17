---
layout: wiki
title: Shell 的学习
categories: [Shell, Syntax]
description: Shell 的学习
keywords: Shell, Syntax
---

# Shell 脚本编程

## 什么是 Shell脚本

例子：

```shell
#!/bin/sh
cd ~
mkdir shell_tut
cd shell_tut

for ((i=0; i<10; i++)); do
	touch test_$i.txt
done
```

解释：

- 第1行：指定脚本解释器，这里是用/bin/sh做解释器的
- 第2行：切换到当前用户的home目录
- 第3行：创建一个目录shell_tut
- 第4行：切换到shell_tut目录
- 第5行：循环条件，一共循环10次
- 第6行：创建一个test_0…9.txt文件
- 第7行：循环体结束

mkdir, touch都是系统自带的程序，一般在/bin或者/usr/bin目录下。for, do, done是sh脚本语言的关键字。

## shell 编程环境

只要有一个能编写代码的文本编辑器和一个能解释执行的脚本解释器就可以了。

### 操作系统
Linux 操作系统或者 Unix 操作系统或者 MacOS 可以直接运行 shell 脚本，因为安装了 shell 解释器。

### 脚本解释器

#### sh

即Bourne shell，POSIX（Portable Operating System Interface）标准的shell解释器，它的二进制文件路径通常是/bin/sh，由Bell Labs开发。

本文讲的是sh，如果你使用其它语言用作shell编程，请自行参考相应语言的文档。

#### bash

Bash是Bourne shell的替代品，属GNU Project，二进制文件路径通常是/bin/bash。业界通常混用bash、sh、和shell，比如你会经常在招聘运维工程师的文案中见到：熟悉Linux Bash编程，精通Shell编程。

## 第一个 shell 脚本

### 编写

打开文本编辑器，新建一个文件，扩展名为sh（sh代表shell），扩展名并不影响脚本执行，见名知意就好。

输入一些代码，第一行一般是这样：

```shell
#!/bin/bash
```
“#!”是一个约定的标记，叫做`Shebang`，它告诉系统这个脚本需要什么解释器来执行。

### 运行

#### 作为可执行程序

```shell
chmod +x test.sh
./test.sh
```

前提是 test.sh 第一行有解释器位置:

```shell
#!/bin/bash
```

否则使用第二种方式运行。

#### 作为解释器参数

```shell
/bin/bash test.sh
```

这种的好处是，不需要对 test.sh 赋予执行权限，也不需要在第一行写上解释器信息。（但为了统一，最好都写上。）

## 语法

### 变量

#### 定义变量

定义变量时，变量名不加美元符号（`$`），如：

```shell
your_name="light"
```

注意，变量名和等号之间不能有空格，这可能和你熟悉的所有编程语言都不一样。

除了显式地直接赋值，还可以用语句给变量赋值，如：

```shell
for file in `ls /etc`
```

#### 使用变量

使用一个定义过的变量，只要在变量名前面加 `$` 即可，如：

```shell
your_name="qinjx"
echo $your_name
echo ${your_name}
```

变量名外面的花括号是可选的，加不加都行，加花括号是为了帮助解释器识别变量的边界，比如下面这种情况：

```shell
for skill in Ada Coffe Action Java; do
	echo "I am good at ${skill}Script"
done
```

如果不给 skill 变量加花括号，写成

```
echo "I am good at $skillScript"
```

解释器就会把 `$skillScript` 当成一个变量（其值为空），代码执行结果就不是我们期望的样子了。

推荐给所有变量加上花括号，这是个好的编程习惯。

### 注释

以 `#` 开头的行就是注释，会被解释器忽略。

多行注释，每行加 `#`。

### 字符串

字符串是shell编程中最常用最有用的数据类型，字符串可以用单引号，也可以用双引号，也可以不用引号。

#### 单引号

```shell
str='this is a string'
```

单引号字符串的限制：

- 单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的
- 单引号字串中不能出现单引号（对单引号使用转义符后也不行）

#### 双引号

```shell
your_name='qinjx'
str="Hello, I know your are \"$your_name\"! \n"
```

- 双引号里可以有变量
- 双引号里可以出现转义字符

#### 字符串操作

##### 拼接字符串

```shell
a="123"
b="abc"
c="${a}-${b}"
echo ${a} ${b} ${c}
```

##### 获取字符串长度：

```
string="123-abc"
echo ${#string} #输出：7
```

##### 提取子字符串

```shell
string="Lengen...wait for it...dary!Lengendary!"
echo ${string:1:4} #输出：enge
```

##### 查找子字符串

```
string="Lengen...wait for it...dary!Lengendary!"
echo `expr index "$string" g`
# 输出：3，这个语句的意思是：找出字母g在这名话中的位置，要在linux下运行，mac下会报错
```

### 数组

shell 里的数组并没有
