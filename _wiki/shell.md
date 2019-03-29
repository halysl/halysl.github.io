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

### 流程控制

#### if...else...

if...

```shell
if condition
then
    command1 
    command2
    ...
    commandN 
fi
```

单行 if...

```shell
if [ $(ps -ef | grep -c "ssh") -gt 1 ]; then echo "true"; fi
```

if...else...

```shell
if condition
then
    command1 
    command2
    ...
    commandN
else
    command
fi
```

if...else-if...else...

```shell
if condition1
then
    command1
elif condition2 
then 
    command2
else
    commandN
fi
```

#### for

```shell
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done
```

单行 for

```shell
for var in item1 item2 ... itemN; do command1; command2… done;
```

```shell
for loop in 1 2 3 4 5; do echo "The value is: $loop"; done

The value is: 1
The value is: 2
The value is: 3
The value is: 4
The value is: 5
```

#### while

```shell
while condition
do
    command
done
```

```shell
#!/bin/bash
int=1
while(( $int<=5 ))
do
    echo $int
    let "int++"
done
```

```shell
1
2
3
4
5
```

#### until

until 循环执行一系列命令直至条件为 true 时停止。

until 循环与 while 循环在处理方式上刚好相反。

```shell
until condition
do
    command
done
```

```shell
#!/bin/bash

a=0

until [ ! $a -lt 10 ]
do
   echo $a
   a=`expr $a + 1`
done
```

```shell
0
1
2
3
4
5
6
7
8
9
```

#### case

Shell case语句为多选择语句。可以用case语句匹配一个值与一个模式，如果匹配成功，执行相匹配的命令。

```shell
case 值 in
模式1)
    command1
    command2
    ...
    commandN
    ;;
模式2）
    command1
    command2
    ...
    commandN
    ;;
esac
```

```shell
echo '输入 1 到 4 之间的数字:'
echo '你输入的数字为:'
read aNum
case $aNum in
    1)  echo '你选择了 1'
    ;;
    2)  echo '你选择了 2'
    ;;
    3)  echo '你选择了 3'
    ;;
    4)  echo '你选择了 4'
    ;;
    *)  echo '你没有输入 1 到 4 之间的数字'
    ;;
esac
```

#### break

跳出所有循环。

#### continue

跳出当次循环。

### 常用指令

#### echo

Shell 的 echo 指令与 PHP 的 echo 指令类似，都是用于字符串的输出。命令格式：

```shell
echo string
```

您可以使用echo实现更复杂的输出格式控制。


1. 显示普通字符串:

``` echo "It is a test"```

```echo It is a test```

这里的双引号完全可以省略.

2. 显示转义字符

```echo "\"It is a test\""```

结果将是:

```"It is a test"```

同样，双引号也可以省略。

3. 显示变量

read 命令从标准输入中读取一行,并把输入行的每个字段的值指定给 shell 变量

```shell
#!/bin/sh
read name 
echo "$name It is a test"
```

以上代码保存为 test.sh，name 接收标准输入的变量，结果将是:

```
[root@www ~]# sh test.sh
OK                     #标准输入
OK It is a test        #输出
```

4. 显示换行

```shell
#!/bin/sh
echo -e "OK! \n" # -e 开启转义
echo "It is a test"
```

输出结果：

```shell
OK!

It is a test
```

5. 显示不换行

```shell
#!/bin/sh
echo -e "OK! \c" # \c 不换行
echo "It is a test"
```

输出结果：

```shell
OK! It is a test
```

6. 显示结果定向至文件

```echo "It is a test" > myfile```

7. 原样输出字符串，不进行转义或取变量(用单引号)

```echo '$name\"'```

输出结果：

```$name\"```

8. 显示命令执行结果

```shell
echo `date`
```

注意： 这里使用的是反引号 `, 而不是单引号 '。

结果将显示当前日期

`Tue Mar 26 19:54:16 CST 2019`

#### printf

shell 里的 printf 类似于 C 语言里的 print 方法，可以格式化字符。

```shell
printf  format-string  [arguments...]
```

例子：

```shell
printf "%-10s %-8s %-4s\n" 姓名 性别 体重kg  
printf "%-10s %-8s %-4.2f\n" 郭靖 男 66.1234 
printf "%-10s %-8s %-4.2f\n" 杨过 男 48.6543 
printf "%-10s %-8s %-4.2f\n" 郭芙 女 47.9876 
```

```shell
姓名     性别   体重kg
郭靖     男      66.12
杨过     男      48.65
郭芙     女      47.99
```

转译序列：

|序列|说明|
|---|----|
|\a|警告字符，通常为ASCII的BEL字符|
|\b|后退|
|\c|抑制（不显示）输出结果中任何结尾的换行字符（只在%b格式指示符控制下的参数字符串中有效），而且，任何留在参数里的字符、任何接下来的参数以及任何留在格式字符串中的字符，都被忽略|
|\f|换页（formfeed）|
|\n|换行|
|\r|回车（Carriage return）|
|\t|水平制表符|
|\v|垂直制表符|
|\\\\|一个字面上的反斜杠字符|
|\ddd|表示1到3位数八进制值的字符。仅在格式字符串中有效|
|\0ddd|表示1到3位的八进制值字符|

#### test

test 命令可以给出一个 bool 值。

##### 数值测试

|参数|说明|
|---|----|
|-eq|等于则为真		|
|-ne|不等于则为真	|
|-gt|大于则为真		|
|-ge|大于等于则为真	|
|-lt|小于则为真		|
|-le|小于等于则为真	|

```shell
num1=100
num2=100
if test $[num1] -eq $[num2]
then
    echo '两个数相等！'
else
    echo '两个数不相等！'
fi
```

```shell
两个数相等！
```

##### 字符串测试

|参数|说明|
|---|----|
|=	|等于则为真|
|!=	|不相等则为真|
|-z 字符串|字符串的长度为零则为真|
|-n 字符串|字符串的长度不为零则为真|

```shell
num1="ru1noob"
num2="runoob"
if test $num1 = $num2
then
    echo '两个字符串相等!'
else
    echo '两个字符串不相等!'
fi
```

```shell
两个字符串不相等!
```

##### 文件测试

`!重要`

|参数		|说明|
|----------|----|
|-e 文件名	|如果文件存在则为真|
|-r 文件名	|如果文件存在且可读则为真|
|-w 文件名	|如果文件存在且可写则为真|
|-x 文件名	|如果文件存在且可执行则为真|
|-s 文件名	|如果文件存在且至少有一个字符则为真|
|-d 文件名	|如果文件存在且为目录则为真|
|-f 文件名	|如果文件存在且为普通文件则为真|
|-c 文件名	|如果文件存在且为字符型特殊文件则为真|
|-b 文件名	|如果文件存在且为块特殊文件则为真|

```shell
cd /bin
if test -e ./bash
then
    echo '文件已存在!'
else
    echo '文件不存在!'
fi
```

```shell
文件已存在!
```

另外，Shell还提供了与( -a )、或( -o )、非( ! )三个逻辑操作符用于将测试条件连接起来，其优先级为："!"最高，"-a"次之，"-o"最低。例如：

```shell
cd /bin
if test -e ./notFile -o -e ./bash
then
    echo '至少有一个文件存在!'
else
    echo '两个文件都不存在'
fi
```

```
至少有一个文件存在!
```

### 函数

```shell
[ function ] funname [()]{
    action;

    [return int;]
}
```

- 可以带function fun() 定义，也可以直接fun() 定义,不带任何参数。
- 参数返回，可以显示加：return 返回，如果不加，将以最后一条命令运行结果，作为返回值。 return后跟数值n(0-255)

```shell
demoFun(){
    echo "这是我的第一个 shell 函数!"
}
echo "-----函数开始执行-----"
demoFun
echo "-----函数执行完毕-----"
```

```shell
-----函数开始执行-----
这是我的第一个 shell 函数!
-----函数执行完毕-----
```

#### 函数参数

在Shell中，调用函数时可以向其传递参数。在函数体内部，通过 $n 的形式来获取参数的值，例如，$1表示第一个参数，$2表示第二个参数...

```shell
funWithParam(){
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
    echo "第十个参数为 ${10} !"
    echo "第十一个参数为 ${11} !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}
funWithParam 1 2 3 4 5 6 7 8 9 34 73
```

```shell
第一个参数为 1 !
第二个参数为 2 !
第十个参数为 10 !
第十个参数为 34 !
第十一个参数为 73 !
参数总数有 11 个!
作为一个字符串输出所有参数 1 2 3 4 5 6 7 8 9 34 73 !
```

`$10 不能获取第十个参数，获取第十个参数需要${10}。当n>=10时，需要使用${n}来获取参数。`

|参数处理|说明|
|-------|----|
|$#|传递到脚本的参数个数|
|$*|以一个单字符串显示所有向脚本传递的参数|
|$$|脚本运行的当前进程ID号|
|$!|后台运行的最后一个进程的ID号|
|$@|与$*相同，但是使用时加引号，并在引号中返回每个参数。|
|$-|显示Shell使用的当前选项，与set命令功能相同。|
|$?|显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。|

### 输入/输出重定向

大多数 UNIX 系统命令从你的终端接受输入并将所产生的输出发送回​​到您的终端。一个命令通常从一个叫标准输入的地方读取输入，默认情况下，这恰好是你的终端。同样，一个命令通常将其输出写入到标准输出，默认情况下，这也是你的终端。

重定向命令列表如下：

|命令|说明|
|----|----|
|command > file|将输出重定向到 file|
|command < file|将输入重定向到 file|
|command >> file|将输出以追加的方式重定向到 file|
|n > file|将文件描述符为 n 的文件重定向到 file|
|n >> file|将文件描述符为 n 的文件以追加的方式重定向到 file|
|n >& m|将输出文件 m 和 n 合并|
|n <& m|将输入文件 m 和 n 合并|
|<< tag|将开始标记 tag 和结束标记 tag 之间的内容作为输入|

#### 输出重定向

重定向一般通过在命令间插入特定的符号来实现。特别的，这些符号的语法如下所示:

`command1 > file1`

上面这个命令执行command1然后将输出的内容存入file1。

注意任何file1内的已经存在的内容将被新内容替代。如果要将新内容添加在文件末尾，请使用>>操作符。

实例:

执行下面的 who 命令，它将命令的完整的输出重定向在用户文件中(users):

$ who > users
执行后，并没有在终端输出信息，这是因为输出已被从默认的标准输出设备（终端）重定向到指定的文件。

你可以使用 cat 命令查看文件内容：

$ cat users
light    console  Mar 19 13:56
light    ttys000  Mar 19 13:56
light    ttys002  Mar 19 13:56
light    ttys003  Mar 19 13:56
light    ttys004  Mar 19 13:56
light    ttys005  Mar 22 18:07
light    ttys007  Mar 26 16:54
light    ttys009  Mar 27 10:56 

#### 输入重定向

和输出重定向一样，Unix 命令也可以从文件获取输入，语法为：

`command1 < file1`

这样，本来需要从键盘获取输入的命令会转移到文件读取内容。

`注意：输出重定向是大于号(>)，输入重定向是小于号(<)。`

实例:

接着以上实例，我们需要统计 users 文件的行数,执行以下命令：

```shell
$ wc -l users
        8 users
$  wc -l < users
        8 
```

注意：上面两个例子的结果不同：第一个例子，会输出文件名；第二个不会，因为它仅仅知道从标准输入读取内容。


`command1 < infile > outfile`

同时替换输入和输出，执行command1，从文件infile读取内容，然后将输出写入到outfile中。

#### 重定向更多细节

一般情况下，每个 Unix/Linux 命令运行时都会打开三个文件：

- 标准输入文件(stdin)：stdin的文件描述符为0，Unix程序默认从stdin读取数据。
- 标准输出文件(stdout)：stdout 的文件描述符为1，Unix程序默认向stdout输出数据。
- 标准错误文件(stderr)：stderr的文件描述符为2，Unix程序会向stderr流中写入错误信息。

`管道 (“|”, pipe line)，把上一个命令的 stdout 接到下一个命令的 stdin;`

默认情况下，command > file 将 stdout 重定向到 file，command < file 将stdin 重定向到 file。

```shell
# 如果希望 stderr 重定向到 file，可以这样写：
`$ command 2 > file`

# 如果希望 stderr 追加到 file 文件末尾，可以这样写(2 表示标准错误文件(stderr))：
$ command 2 >> file

# 如果希望将 stdout 和 stderr 合并后重定向到 file，可以这样写：
$ command > file 2>&1

# 如果希望对 stdin 和 stdout 都重定向，可以这样写:
$ command >> file 2>&1

# command 命令将 stdin 重定向到 file1，将 stdout 重定向到 file2:
$ command < file1 >file2
```

#### Here Document

```shell
command << delimiter
    document
delimiter
```

结尾的delimiter 一定要顶格写，前面不能有任何字符，后面也不能有任何字符，包括空格和 tab 缩进。
开始的delimiter前后的空格会被忽略掉。

实例：

```shell
$ wc -l << EOF
    t1
    t2
    t3
EOF
3          # 输出结果为 3 行
```

#### /dev/null 文件

如果希望执行某个命令，但又不希望在屏幕上显示输出结果，那么可以将输出重定向到 /dev/null：

`$ command > /dev/null`

/dev/null 是一个特殊的文件，写入到它的内容都会被丢弃；如果尝试从该文件读取内容，那么什么也读不到。但是 /dev/null 文件非常有用，将命令的输出重定向到它，会起到"禁止输出"的效果。

如果希望屏蔽 stdout 和 stderr，可以这样写：

`$ command > /dev/null 2>&1`

### 文件包含

和其他语言一样，Shell 也可以包含外部脚本。这样可以很方便的封装一些公用的代码作为一个独立的文件。

```shell
# 注意点号(.)和文件名中间有一空格
. filename

# 或者使用source
source filename
```
