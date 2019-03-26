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

数组中可以存放多个值。Bash Shell 只支持一维数组（不支持多维数组），初始化时不需要定义数组大小（与 PHP 类似）。

与大部分编程语言类似，数组元素的下标由0开始。

Shell 数组用括号来表示，元素用"空格"符号分割开，语法格式如下：

```shell
array_name=(value1 ... valuen)

my_array=(A B "C" D)

${array_name[index]}
```

```shell
my_array=(A B "C" D)

echo "第一个元素为: ${my_array[0]}"
echo "第二个元素为: ${my_array[1]}"
echo "第三个元素为: ${my_array[2]}"
echo "第四个元素为: ${my_array[3]}"
```

```shell
my_array[0]=A
my_array[1]=B
my_array[2]=C
my_array[3]=D

echo "数组的元素为: ${my_array[*]}"
echo "数组的元素为: ${my_array[@]}"

echo "数组元素个数为: ${#my_array[*]}"
echo "数组元素个数为: ${#my_array[@]}"
```

### 运算符

Shell 和其他编程语言一样，支持多种运算符，包括：

- 算数运算符
- 关系运算符
- 布尔运算符
- 字符串运算符
- 文件测试运算符

原生bash不支持简单的数学运算，但是可以通过其他命令来实现，例如 awk 和 expr，expr 最常用。

expr 是一款表达式计算工具，使用它能完成表达式的求值操作。

```shell
val=`expr 2 + 2`
echo "两数之和为 : $val"

两数之和为 : 4
```

> - 表达式和运算符之间要有空格，例如 2+2 是不对的，必须写成 2 + 2，这与我们熟悉的大多数编程语言不一样。
> - 完整的表达式要被 ` ` 包含，注意这个字符不是常用的单引号，在 Esc 键下边。

#### 算术运算符

假定变量 a 为 10，变量 b 为 20。

|运算符	|说明|举例|
|------|---|----|
|+	|加法|`expr $a + $b` 结果为 30。|
|-	|减法|`expr $a - $b` 结果为 -10。|
|*	|乘法|`expr $a \* $b` 结果为  200。|
|/	|除法|`expr $b / $a` 结果为 2。|
|%	|取余|`expr $b % $a` 结果为 0。|
|=	|赋值|a=$b 将把变量 b 的值赋给 a。|
|==	|相等。用于比较两个数字，相同则返回 true。|[ $a == $b ] 返回 false。|
|!=	|不相等。用于比较两个数字，不相同则返回 true。|[ $a != $b ] 返回 true。|

> - 条件表达式要放在方括号之间，并且要有空格，例如: [$a==$b] 是错误的，必须写成 [ $a == $b ]。

```shell
a=10
b=20

val=`expr $a + $b`
echo "a + b : $val"

val=`expr $a - $b`
echo "a - b : $val"

val=`expr $a \* $b`
echo "a * b : $val"

val=`expr $b / $a`
echo "b / a : $val"

val=`expr $b % $a`
echo "b % a : $val"

if [ $a == $b ]
then
   echo "a 等于 b"
fi
if [ $a != $b ]
then
   echo "a 不等于 b"
fi
```

```shell
a + b : 30
a - b : -10
a * b : 200
b / a : 2
b % a : 0
a 不等于 b
```

> - 乘号(*)前边必须加反斜杠(\)才能实现乘法运算；
> - if...then...fi 是条件语句，后续将会讲解。
> - 在 MAC 中 shell 的 expr 语法是：$((表达式))，此处表达式中的 "*" 不需要转义符号 "\" 。

#### 关系运算符

不同于一般语言的关系运算符，shell 的关系运算符只支持数字，不支持字符串，除非字符串的值是数字。

假定变量 a 为 10，变量 b 为 20。

|运算符|说明|举例|
|-----|---|----|
|-eq|检测两个数是否相等，相等返回 true|[ $a -eq $b ] 返回 false。|
|-ne|检测两个数是否不相等，不相等返回 true|[ $a -ne $b ] 返回 true。|
|-gt|检测左边的数是否大于右边的，如果是，则返回 true|[ $a -gt $b ] 返回 false。|
|-lt|检测左边的数是否小于右边的，如果是，则返回 true|[ $a -lt $b ] 返回 true。|
|-ge|检测左边的数是否大于等于右边的，如果是，则返回 true|[ $a -ge $b ] 返回 false。|
|-le|检测左边的数是否小于等于右边的，如果是，则返回 true|[ $a -le $b ] 返回 true。|

```shell
a=10
b=20

if [ $a -eq $b ]
then
   echo "$a -eq $b : a 等于 b"
else
   echo "$a -eq $b: a 不等于 b"
fi
if [ $a -ne $b ]
then
   echo "$a -ne $b: a 不等于 b"
else
   echo "$a -ne $b : a 等于 b"
fi
if [ $a -gt $b ]
then
   echo "$a -gt $b: a 大于 b"
else
   echo "$a -gt $b: a 不大于 b"
fi
if [ $a -lt $b ]
then
   echo "$a -lt $b: a 小于 b"
else
   echo "$a -lt $b: a 不小于 b"
fi
if [ $a -ge $b ]
then
   echo "$a -ge $b: a 大于或等于 b"
else
   echo "$a -ge $b: a 小于 b"
fi
if [ $a -le $b ]
then
   echo "$a -le $b: a 小于或等于 b"
else
   echo "$a -le $b: a 大于 b"
fi
```

```shell
10 -eq 20: a 不等于 b
10 -ne 20: a 不等于 b
10 -gt 20: a 不大于 b
10 -lt 20: a 小于 b
10 -ge 20: a 小于 b
10 -le 20: a 小于或等于 b
```

#### 布尔运算符

|运算符	|说明|举例|
|---|----|---|
|!	|非运算，表达式为 true 则返回 false，否则返回 true。|[ ! false ] 返回 true。|
|-o	|或运算，有一个表达式为 true 则返回 true。|[ $a -lt 20 -o $b -gt 100 ] 返回 true。|
|-a	|与运算，两个表达式都为 true 才返回 true。|[ $a -lt 20 -a $b -gt 100 ] 返回 false。|

```shell
a=10
b=20

if [ $a != $b ]
then
   echo "$a != $b : a 不等于 b"
else
   echo "$a != $b: a 等于 b"
fi
if [ $a -lt 100 -a $b -gt 15 ]
then
   echo "$a 小于 100 且 $b 大于 15 : 返回 true"
else
   echo "$a 小于 100 且 $b 大于 15 : 返回 false"
fi
if [ $a -lt 100 -o $b -gt 100 ]
then
   echo "$a 小于 100 或 $b 大于 100 : 返回 true"
else
   echo "$a 小于 100 或 $b 大于 100 : 返回 false"
fi
if [ $a -lt 5 -o $b -gt 100 ]
then
   echo "$a 小于 5 或 $b 大于 100 : 返回 true"
else
   echo "$a 小于 5 或 $b 大于 100 : 返回 false"
fi
```

```shell
10 != 20 : a 不等于 b
10 小于 100 且 20 大于 15 : 返回 true
10 小于 100 或 20 大于 100 : 返回 true
10 小于 5 或 20 大于 100 : 返回 false
```

#### 逻辑运算符


|运算符|说明|举例|
|-----|---|----|
|&&|逻辑的 AND|[[ $a -lt 100 && $b -gt 100 ]] 返回 false|
|\|\||逻辑的 OR|[[ $a -lt 100 \|\| $b -gt 100 ]] 返回 true|

```shell
a=10
b=20

if [[ $a -lt 100 && $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"
fi

if [[ $a -lt 100 || $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"
fi
```

```shell
返回 false
返回 true
```

#### 字符串运算符

a="abc"
b="def"


|运算符|说明|举例|
|-----|---|----|
|=	|检测两个字符串是否相等，相等返回 true。	|[ $a = $b ] 返回 false。|
|!=	|检测两个字符串是否相等，不相等返回 true。	|[ $a != $b ] 返回 true。|
|-z	|检测字符串长度是否为0，为0返回 true。		|[ -z $a ] 返回 false。|
|-n	|检测字符串长度是否为0，不为0返回 true。	|[ -n "$a" ] 返回 true。|
|$	|检测字符串是否为空，不为空返回 true。		|[ $a ] 返回 true。|

```shell
a="abc"
b="efg"

if [ $a = $b ]
then
   echo "$a = $b : a 等于 b"
else
   echo "$a = $b: a 不等于 b"
fi
if [ $a != $b ]
then
   echo "$a != $b : a 不等于 b"
else
   echo "$a != $b: a 等于 b"
fi
if [ -z $a ]
then
   echo "-z $a : 字符串长度为 0"
else
   echo "-z $a : 字符串长度不为 0"
fi
if [ -n "$a" ]
then
   echo "-n $a : 字符串长度不为 0"
else
   echo "-n $a : 字符串长度为 0"
fi
if [ $a ]
then
   echo "$a : 字符串不为空"
else
   echo "$a : 字符串为空"
fi
```

```shell
abc = efg: a 不等于 b
abc != efg : a 不等于 b
-z abc : 字符串长度不为 0
-n abc : 字符串长度不为 0
abc : 字符串不为空
```

#### 文件测试运算符

`！重要`

文件测试运算符用于检测 Unix 文件的各种属性。

|操作符|说明|举例|
|-----|----|---|
|-b file| 检测文件是否是块设备文件，如果是，则返回 true。|[ -b $file ] 返回 false。|
|-c file| 检测文件是否是字符设备文件，如果是，则返回 true。|[ -c $file ] 返回 false。|
|-d file| 检测文件是否是目录，如果是，则返回 true。|[ -d $file ] 返回 false。|
|-f file| 检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。|[ -f $file ] 返回 true。|
|-g file| 检测文件是否设置了 SGID 位，如果是，则返回 true。|[ -g $file ] 返回 false。|
|-k file| 检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。|[ -k $file ] 返回 false。|
|-p file| 检测文件是否是有名管道，如果是，则返回 true。|[ -p $file ] 返回 false。|
|-u file| 检测文件是否设置了 SUID 位，如果是，则返回 true。|[ -u $file ] 返回 false。|
|-r file| 检测文件是否可读，如果是，则返回 true。|[ -r $file ] 返回 true。|
|-w file| 检测文件是否可写，如果是，则返回 true。|[ -w $file ] 返回 true。|
|-x file| 检测文件是否可执行，如果是，则返回 true。|[ -x $file ] 返回 true。|
|-s file| 检测文件是否为空（文件大小是否大于0），不为空返回 true。|[ -s $file ] 返回 true。|
|-e file| 检测文件（包括目录）是否存在，如果是，则返回 true。|[ -e $file ] 返回 true。|

```shell
file="/tmp/test.sh"
if [ -r $file ]
then
   echo "文件可读"
else
   echo "文件不可读"
fi
if [ -w $file ]
then
   echo "文件可写"
else
   echo "文件不可写"
fi
if [ -x $file ]
then
   echo "文件可执行"
else
   echo "文件不可执行"
fi
if [ -f $file ]
then
   echo "文件为普通文件"
else
   echo "文件为特殊文件"
fi
if [ -d $file ]
then
   echo "文件是个目录"
else
   echo "文件不是个目录"
fi
if [ -s $file ]
then
   echo "文件不为空"
else
   echo "文件为空"
fi
if [ -e $file ]
then
   echo "文件存在"
else
   echo "文件不存在"
fi
```

```shell
文件可读
文件可写
文件可执行
文件为普通文件
文件不是个目录
文件不为空
文件存在
```
