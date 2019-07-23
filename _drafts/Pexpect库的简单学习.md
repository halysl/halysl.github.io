
# Pexpect 库的简单学习

## 一、简单介绍及安装

- expect 主要用于模拟人机对话，简单地说就是可以使用正则匹配捕捉系统的提问（例如 rm 操作的确认，ssh 登录需要输入密码等），并且根据捕捉到的提问进行不同的操作。
- pexpect 是 Python 语言的类 Expect 实现。
- 安装：`pip install pexpect`

## 二、基本使用流程

pexpect 的执行流程其实就三步：

- 首先用 spawn 来执行一个程序
- 用 expect 来等待指定的关键字，这个关键字是被执行的程序打印到标准输出上面的，也就是计算机要问你的
- 当发现某个关键字之后，就进入到某些操作，操作结束后退出循环（或者操作进入下一个 expect）

举个简单的例子，ftp 的连接（[代码来源](https://github.com/pexpect/pexpect/blob/master/examples/ftp.py)）。

```python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pexpect
import sys

# 用spawn来执行一个指令
child = pexpect.spawn('ftp ftp.openbsd.org')
# 用expect等待指定的关键字’name‘
child.expect('(?i)name .*: ')
# 若上一步匹配到了，则向计算机输入name
child.sendline('anonymous')
# 用expect等待指定的关键字’password‘
child.expect('(?i)password')
# 若上一步匹配到了，则向计算机输入password
child.sendline('pexpect@sourceforge.net')
# 用expect等待指定的关键字’ftp>‘
child.expect('ftp> ')
# 若上一步成功匹配，则意味着进入了ftp连接，现在做一些操作
child.sendline('cd /pub/OpenBSD/3.7/packages/i386')
child.expect('ftp> ')
child.sendline('bin')
child.expect('ftp> ')
child.sendline('prompt')
child.expect('ftp> ')
child.sendline('pwd')
child.expect('ftp> ')
print("Escape character is '^]'.\n")
sys.stdout.write (child.after)
sys.stdout.flush()
child.interact() # Escape character defaults to ^]
# At this point this script blocks until the user presses the escape character
# or until the child exits. The human user and the child should be talking
# to each other now.

# At this point the script is running again.
print('Left interactve mode.')

# The rest is not strictly necessary. This just demonstrates a few functions.
# This makes sure the child is dead; although it would be killed when Python exits.
if child.isalive():
    child.sendline('bye') # Try to ask ftp child to exit.
    child.close()
# Print the final state of the child. Normally isalive() should be FALSE.
if child.isalive():
    print('Child did not exit gracefully.')
else:
    print('Child exited gracefully.')
```

## 三、API

### 1、spawn()
spawn() 执行一个程序，返回这个程序的操作句柄。

```
process = pexpect.spawn('ftp sw-ftp')
```

spawn() 有两种调用方式

- 传递一个参数，参数即将执行的命令字符串

```
process = pexpect.spawn('ftp sw-ftp')
```

- 传递两个参数，第一个参数是主程序，第二个参数是主程序的参数

```
cmd = 'ftp sw-ftp'
process = pexpect.spawn('/bin/bash', ["-c", cmd])
```

推荐使用第二种调用方式，虽然代码看起来复杂了很多，但它可以避免一些事，例如命令行执行时出现特殊字符‘*’等。

举个例子：我想查找当前目录下 ta 开头的文件信息

- 使用第一种方法

```python
process = pexpect.spawn('ls ta*')
```

执行过后会爆出这个错误。

```shell
pexpect.exceptions.EOF: End Of File (EOF). Exception style platform.
```

- 使用第二种方法

```python
cmd = 'ls ta*'
process = pexpect.spawn('/bin/bash', ['-c', cmd])
```

结果正常执行。

spawn 除了那两种传递指令的方法，还有一些关键字参数，例如：

- timeout 超时
- maxread 缓存设置
- searchwindowsize 模式匹配阈值
- logfile 日志文件
- env 指定环境变量
- cwd 指定执行目录
- [更多请参考spawn() - 执行程序](https://www.jianshu.com/p/cfd163200d12)

### 2、expect()

当拿到程序句柄后，可以调用句柄的expect()方法正则匹配寻找关键字，并根据关键字执行不同的操作。
`写不下去了TAT`

## 参考文档
[Pexpect 模块使用说明](https://www.jianshu.com/p/cfd163200d12)
[探索 Pexpect，第 1 部分：剖析 Pexpect](https://www.ibm.com/developerworks/cn/linux/l-cn-pexpect1/index.html)
[Pexpect version 4.6](https://pexpect.readthedocs.io/en/stable/)
