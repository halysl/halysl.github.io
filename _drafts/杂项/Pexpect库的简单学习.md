
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

```python
process = pexpect.spawn('ftp sw-ftp')
```

spawn() 有两种调用方式

- 传递一个参数，参数即将执行的命令字符串

```python
process = pexpect.spawn('ftp sw-ftp')
```

- 传递两个参数，第一个参数是主程序，第二个参数是主程序的参数

```python
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

|关键字参数|默认值|作用|
|---------|-----|----|
|timeout|30秒|超时。程序被启动之后会有输出，我们也会在脚本中检查输出中的关键字是否是已知并处理的，如果指定时间内没找到程序就会出错返回。|
|maxread|2000字符|指定一次性试着从命令输出中读多少数据。如果设置的数字比较大，那么从 TTY 中读取数据的次数就会少一些。设置为 1 表示关闭读缓存。设置更大的数值会提高读取大量数据的性能，但会浪费更多的内存。这个值的设置与 searchwindowsize 合作会提供更多功能。缓存的大小并不会影响获取的内容，也就是说如果一个命令输出超过2000个字符以后，先前缓存的字符不会丢失掉，而是放到其他地方去，当你用 self.before （这里 self 代表 spawn 的实例）还是可以取到完整的输出的。|
|searchwindowsize|None|searchwindowsize 参数是与 maxread 参数一起合作使用的，它的功能比较微妙，但可以显著减少缓存中有很多字符时的匹配时间。
默认情况下， expect() 匹配指定的关键字都是这样：每次缓存中取得一个字符时就会对整个缓存中的所有内容匹配一次正则表达式，你可以想像如果程序的返回特别多的时候，性能会多么的低。设置 searchwindowsize 的值表示一次性收到多少个字符之后才匹配一次表达式，比如现在有一条命令会出现大量的输出，但匹配关键字是标准的 FTP 提示符 ftp> ，显然要匹配的字符只有 5 个（包括空格），但是默认情况下每当 expect 获得一个新字符就从头匹配一次这几个字符，如果缓存中已经有了 1W 个字符，一次一次的从里面匹配是非常消耗资源的，这个时候就可以设置 searchwindowsize=10, 这样 expect 就只会从最新的（最后获取的） 10 个字符中匹配关键字了，如果设置的值比较合适的话会显著提升性能。不用担心缓存中的字符是否会被丢弃，不管有多少输出，只要不超时就总会得到所有字符的，这个参数的设置仅仅影响匹配的行为。这个参数一般在 expect() 命令中设置， pexpect 2.x 版本似乎有一个 bug ，在 spawn 中设置是不生效的。|
|logfile|None|当给 logfile 参数指定了一个文件句柄时，所有从标准输入和标准输出获得的内容都会写入这个文件中（注意这个写入是 copy 方式的），如果指定了文件句柄，那么每次向程序发送指令（process.send）都会刷新这个文件（flush）。文件里，既包含了程序运行时的输出，也包含了 spawn 向程序发送的内容，有的时候你也许不希望这样，因为某些内容出现了2次。|
|logfile_read|None|记录执行程序中返回的所有内容，也就是去掉你发出去的命令，而仅仅只包括命令结果的部分。但输入内容大多也会被回显，所以照样可以记录。|
|logfile_send|None|记录向执行程序发送的所有内容。|
|cwd|./(当前路径)|指定命令执行的目录。cwd 用来指定命令发送的命令在哪个路径下执行，它一般是用在 send() 系列命令中，比如在 Linux 中，你想在 /etc 目录下执行 ls –l 命令，那么完全不需要用 sendline("cd /etc && ls -l") 这样的方式，而是用 sendline("ls –l", cwd="/etc") 就可以了。|
|env|None|指定环境变量的值，这个值是一个字典，如果你发送的命令要使用一些环境变量，那么可以在这里提供。|
|ignore_sighup|True|这个参数是 pexpect 3.1 开始引入的，在 3.1 之前（比如 pexpect 2.3），spawn 的子程序会过滤 SIGHUP 信号，也就是用 Ctrl+C 是不能终止子程序的，3.1的默认值也继承了这个行为，但是如果设置 ignore_sighup = False 就可以改变这个行为。|
|delaybeforesend|0.05|一个隐藏参数用来设置发送字符串之前的延时。|

### 2、expect()

当拿到程序句柄后，可以调用句柄的expect()方法正则匹配寻找关键字，并根据关键字执行不同的操作。

```python
# pattern_list      正则表达式列表，表示要匹配这些内容
# timeout           不设置或者设置为-1的话，超时时间就采用self.timeout的值，默认是30秒。也可以自己设置。
# searchwindowsize  功能和 spawn 上的一样，但是！请注意这个但是！下面会实际说明
process.expect(pattern_list, timeout=-1, searchwindowsize=None)
```

- 最简单的匹配方式

```python
process.expect('[Nn]ame')
```

上面的代码表示：匹配 process 这个句柄（代表 spawn 方法的例子中我们启动的 ftp 连接）中的 name 关键字，其中 n 不分大小写。

上面的关键字一旦匹配，就会返回0表示匹配成功，但是如果一直匹配不到呢？默认是会一直等下去，但是如果设置了 timeout 的话就会超时。

- 匹配一系列输出

实际上， expect() 可以匹配一系列输出，通过检查匹配到的输出，我们可以做不同的事情。比如之前 spawn 的 ftp 连接，如果我们输入用户名之后有不同的情况，就可以通过监控这些不同情况来做不同的动作，比如：

```python
index = process.expect([
    'Permission Denied',
    'Terminal type',
    'ftp>',
])
if index == 0:
    print "Permission denied at host, can't login."
    process.kill(0)
elif index == 1:
    print "Login ok, set up terminal type…"
    process.sendline('vty100')
    process.expect("ftp>")
elif index == 2:
    print "Login Ok, please send your command"
    process.interact()
```

上面的代码中，expect 方法中的是一个列表，列表中的每个元素都是一个关键字的正则表达式，也就是说我们期待这 3 种情况之一，而 expect 返回一个顺序值来代表我匹配到了哪一个元素（也就是发生了哪种情况了），这个顺序值是从 0 开始计算的。

当expect之后，下面的 if 语句就开始处理这 3 种情况了：

- 权限不足，这可能是 ftp 服务器出现问题，或者没有这个帐号，或者其他什么情况，反正只要发现这种情况的话，我们就给用户提示一下，然后杀掉这个进程。
- 登陆成功，但还要用户指定终端模式才能真正使用，所以我们在代码中指定了 vty100 这种模式，然后看是不是能真正使用了。
- 还是登陆成功了，而且还可以直接输入命令操作 ftp 服务器了，于是我们提示用户，然后把操作权限交给用户。

另外有一种特殊情况，如果同时有2个被匹配到，那么怎么办？简单来说就是这样：

- 原始流中，第一个被关键字匹配到的内容会被使用
- 匹配关键字列表中，最左边的会被使用

给个例子：

```python
# 如果流里面的内容是 "hello world"
index = process.expect(["hi", "hello", "hello world"])
```

返回的值是 1，也就是 'hello' 被匹配到了，哪怕真正最好的匹配是 "hello world" 但因为放在后面所以仍然无效。

使用技巧

- 如果要检查或者匹配 expect.EOF 和 expect.TIMEOUT 这两种情形，那么必须将它们放进匹配列表里面去，这样可以通过检查返回的数字来处理它们。如果没放进列表的话，就会发生 EOF 或者 TIMEOUT 错误，程序就会中途停止了。

- 匹配规则中有些特殊语法，比如下面的规则中前 2 个匹配都是大小写无关的，关键就是这个 (?i) 匹配规则，它相当于 re.IGNORE 或者 re.I 这个关键字，因为毕竟不是真正的正则表达式引擎，所以 pexpect 使用这样特殊语法：

```python
child.expect(['(?i)etc', '(?i)readme', pexpect.EOF, pexpect.TIMEOUT])
```

### 3、expect_exact() - 精确匹配

它的使用和 expect() 是一样的，唯一不同的就是它的匹配列表中不再使用正则表达式。
从性能上来说 expect_exact() 要更好一些，因为即使你没有使用正则表达式而只是简单的用了几个字符 expect() 也会先将它们转换成正则表达式模式然后再搜索，但 expect_exact() 不会，而且也不会把一些特殊符号转换掉。

### 4、expect_list() - 预转换匹配

使用方式和 expect() 一样，唯一不同的就是它里面接受的正则表达式列表只会转换一次。
expect() 稍微有点笨，每调用一次它都会将内部的正则表达式转换一次（当然也有其他办法避免），如果你是在以后循环中调用 expect() 的话，多余的转换动作就会降低性能，在这种情况下建议用 expect_list() 来代替。

使用方法：

```python
# timeout 为 -1 的话使用 self.timeout 的值
# searchwindowsize 为 -1 的话，也使用系统默认的值
process.expect_list(pattern_list, timeout=-1, searchwindowsize=-1)
```

### 5、expect_loop()

用于从标准输入中获取内容，loop这个词代表它会进入一个循环，必须要从标准输入中获取到关键字才会往下继续执行。

使用方法：

```python
expect_loop(self, searcher, timeout=-1, searchwindowsize=-1)
```

### 6、send() - 发送关键字

send() 作为3个关键操作之一，用来向程序发送指定的字符串，它的使用没什么特殊的地方，比如：

```python
process.expect("ftp>")
process.send("by\n")
```

这个方法会返回发送字符的数量。

### 7、sendline() - 发送带回车符的字符串

sendline() 和 send() 唯一的区别就是在发送的字符串后面加上了回车换行符，这也使它们用在了不同的地方：

- 只需要发送字符就可以的话用send()
- 如果发送字符后还要回车的话，就用 sendline()

它也会返回发送的字符数量

### 8、sendcontrol() - 发送控制信号

sendcontrol() 向子程序发送控制字符，比如 <kbd>ctrl+C</kbd> 或者 <kbd>ctrl+D</kbd> 之类的，比如你要向子程序发送 <kbd>ctrl+G</kbd>，那么就这样写：

```python
process.sendcontrol('g')
```

### 9、sendeof() - 发送 EOF 信号

向子程序发送 End Of File 信号。

### 10、sendintr() - 发送终止信号

向子程序发送 SIGINT 信号，相当于 Linux 中的 kill 2 ，它会直接终止掉子进程。

### 11、interact() - 将控制权交给用户

interact() 表示将控制权限交给用户（或者说标准输入）。一般情况下 pexpect 会接管所有的输入和输出，但有的时候还是希望用户介入，或者仅仅是为了完成一部分工作的时候， interact() 就很有用了。

比如：

- 登陆 ftp 服务器的时候，在输入用户密码阶段希望用户手工输入密码，然后脚本完成剩余工作时（将用户密码写在脚本中可不安全）
- 只希望完成登陆工作，比如要 ssh 连接到一台远方的服务器，但中间要经过好几跳，用手工输入实在太麻烦，所以就用脚本先跳到目的服务器上，然后再把控制权限还给用户做操作。

使用方法：

```python
# escape_character 就是当用户输出这里指定的字符以后表示自己的操作完成了，将控制权重新交给 pexpect
process.interact(escape_character='\x1d', input_filter=None, output_filter= None)
```

详细来说，这个方法将控制权交给用户（或者说用户操作的键盘），然后简单的将标准输出、标准错误输出和标准输入绑定到系统上来。

通过设置 escape_character 的值，可以定义返回码，默认是 <kbd>ctrl+]</kbd> 或者说 <kbd>^]</kbd>，当输入了返回码以后，脚本会将控制权从用户那里重新拿回来，然后继续向下执行。

### 12、close() - 停止应用程序

如果想中途关闭子程序，那么可以用 close 来完成，调用这个方法后会返回这个程序的返回值。
如果设置 force=True 会强行关闭这个程序，大概的过程就是先发送 SIGHUP 和 SIGINT 信号，如果都无效的话就发 SIGKILL 信号，反正不管怎么样都会保证这个程序被关闭掉。
多次调用这个方法是允许的，但是不保证每次都能返回正确的返回值。尽量不要这么做，如果想保证程序被关闭的话只要设置 force 的值就可以了。

下面是实例：

```python
process.close(force=True)
```

### 13、terminate() - 停止应用程序

可以看作是上面 close() 的别名，因为不管是功能还是使用方法都是一样的。

### 14、Kill() - 发送 SIGKILL 信号

向子程序发送 SIGKILL 的信号。

### 15、flush()

什么都不干，只是为了与文件方法兼容而已。

### 16、isalive() - 检查子程序运行状态

检查被调用的子程序是否正在运行，这个方法是运行在非阻断模式下面的。
如果获得的返回是 True 表示子程序正在运行；返回 False 则表示程序运行终止。
isatty() - 检查是否运行在 TTY 设备上
返回 True 表示打开和连接到了一个 tty 类型的设备，或者返回 False 表示未连接。

### 17、next() - 返回下一行内容

和操作文件一样，这个方法也是返回缓存中下一行的内容。

### 18、read() - 返回剩下的所有内容

获取子程序返回的所有内容，一般情况下我们可以用 expect 来期待某些内容，然后通过 process.before 这样的方式来获取，但这种方式有一个前提：那就是必须先 expect 某些字符，然后才能用 process.before 来获取缓存中剩下的内容。

read() 的使用很不同，它期待一个 EOF 信号，然后将直到这个信号之前的所有输出全部返回，就像读一个文件那样。

一般情况下，交互式程序只有关闭的时候才会返回 EOF ，比如用 by 命令关闭 ftp 服务器，或者用 exit 命令关闭一个 ssh 连接。

这个方法使用范围比较狭窄，因为完全可以用 expect.EOF 方式来代替。当然如果是本机命令，每执行完一次之后都会返回 EOF ，这种情况下倒是很有用：

```python
process = pexpect.spawn('ls –l')
output = process.read()
print output
```

看起来这么做有点无聊？但我想一定有什么理由支持这个方法。

可以用指定 read(size=-1) 的方式来设置返回的字符数，如果没有设置或者设置为负数则返回所有内容，正数则返回指定数量的内容，返回的内容是字符串形式。

### 19、readline() - 返回一行输出

返回一行输出，返回的内容包括最后的\r\n字符。

也可以设置 readline(size=-1) 来指定返回的字符数，默认是负数表示返回所有的。

### 20、readlines() - 返回列表模式的所有输出

返回一个列表，列表中的每个元素都是一行（包括\r\n字符）。

### 21、setecho() - 子程序响应模式

设置子程序运行时的响应方式，一般情况下向子程序发送字符的时候，这些字符都会在标准输出上显示出来，这样你可以看到你发送出去的内容，但是有的时候，我们不需要显示，那么就可以用这个方法来设置了。

注意，必须在发送字符之前设置，设置之后在之后的代码中都一直有效。比如：

```python
process = pexpect.spawn('cat')

# 默认情况下，下面的1234这个字符串会显示2次，一次是pexpect返回的，一次是cat命令返回的
process.sendline("1234")

# 现在我们关闭pexpect()的echo功能
process.setecho(False)

# 下面的字符只会显示一次了，这是由cat返回的
process.sendline("abcd")

# 现在重新开启echo功能，就可以再次看到我们发送的字符了
process.setecho(True)
```

### 22、setwinsize() - 控制台窗口大小

如果子程序是一个控制台（TTY），比如 SSH 连接、 Telnet 连接这种通过网络登陆到系统并发送命令的都算控制台，那么可以用这个方法来设置这个控制台的大小（或者说长宽）。

它的调用方式是 `process.setwinsize(r, c)`。

默认值是 `setwinsize(24, 80)`，其中 24 是高度，单位是行； 80 是宽度，单位是字符。

为什么要用它？想像下面的场景：

有的时候你通过pexpect登陆到某个ssh控制台之后，又用 interact() 来将控制权交给用户，然后用户到控制台里面写自己的命令，如果命令比较长，就会发现当命令到屏幕边缘之后不会自动换行，而是又返回到这一行的最前面重新覆盖前面的字符；这不会影响命令的实际效果，但是很恼人。

这种情况用 setwinsize() 就可以解决，找到自己终端支持的长度，重新设置一下，比如 setwinsize(25, 96 )，如果设置的正确的话就可以解决了。

### 23、wait() - 执行等待

直到被调用的子程序执行完毕之前，程序都停止（或者说等待）执行。它不会从被调用的子程序中读取任何内容。

### 24、waitnoecho()

它使用的地方比较特殊，唯一匹配的地方就是：当子程序的 echo 功能被设置为 Fals 时。

看起来很奇怪？其实这个功能是基于一个很让人难以置信但的确是真实的情况：

在命令行模式下，很多要求输入密码的地方，比如 FTP/SSH 等，密码实际上都会在你输入之后又重新返回并打印出来的，但是为什么我们看不到我们自己输入的密码呢？这就是因为密码在要打印出来之前被程序将 echo 功能设置为 False 了。

现在知道为什么有这么一个方法了吧？比如要进行一个 ssh 连接时，如何检查是否要输入密码？用关键字 password 是一个方法，但还有一个方法就是这样：

```python
# 启动ssh连接
process = pexpect.spawn("ssh user@example.com")

# 等待echo被设置为False，这就意味着本地不会有回显
process.waitnoecho()
process.sendline('mypassword')
```

可以设置超时时间，默认是：waitnoecho(timeout=-1)，表示和系统设置的超时时间相同，也可以设置为 None 表示永远等待，直到回显被设置为 False ，当然还可以设置其他的数字来表示超时时间。

### 25、write() - 发送字符串

类似于send()命令，只不过不会返回发送的字符数。

### 26、writelines() - 发送包含字符串的列表

类似于 write() 命令，只不过接受的是一个字符串列表， writelines() 会向子程序一条一条的发送列表中的元素，但是不会自动在每个元素的最后加上回车换行符。

与 write() 相似的是，这个方法也不会返回发送的字符数量。

## pexpect 的特殊变量

### pexpect.EOF - 匹配终止信号

EOF 变量使用范围很广泛，比如检查 ssh/ftp/telnet 连接是否终止啊，文件是否已经到达末尾啊。 pexpect 大部分脚本的最后都会检查 EOF 变量来判断是不是正常终止和退出，比如下面的代码：

```python
process.expect("ftp>")
process.sendline("by")
process.expect(pexpect.EOF)
print "ftp connect terminated."
```

### pexpect.TIMEOUT - 匹配超时信号

TIMEOUT 变量用来匹配超时的情况，默认情况下 expect 的超时时间是 60 秒，如果超过 60 秒还没有发现期待的关键字，就会触发这个行为，比如：

```python
# 匹配pexpect.TIMEOUT的动作，只有超时事件发生的时候才会有效
index = process.expect(['ftp>', pexpect.TIMEOUT],)
if index == 1:
    process.interactive()   ; # 将控制权交给用户
elif index == 2:
    print "Time is out."
    process.kill(0)         ; # 杀掉进程



# 那么怎么改变超时时间呢？其实可以修改spawn对象里的timeout参数：
# 下面的例子仅仅加了一行，这样就改变了超时的时间了
process.timeout = 300   ; # 注意这一行
index = process.expect(['ftp>', pexpect.TIMEOUT],)
if index == 1:
    process.interactive()   ; # 将控制权交给用户
elif index == 2:
    print "Time is out."
    process.kill(0)         ; # 杀掉进程
```

### process.before/after/match - 获取程序运行输出

当 expect() 过程匹配到关键字（或者说正则表达式）之后，系统会自动给3个变量赋值，分别是 before, after 和 match

- process.before - 保存了到匹配到关键字为止，缓存里面已有的所有数据。也就是说如果缓存里缓存了 100 个字符的时候终于匹配到了关键字，那么 before 就是除了匹配到的关键字之外的所有字符
- process.after - 保存匹配到的关键字，比如你在 expect 里面使用了正则表达式，那么表达式匹配到的所有字符都在 after 里面
- process.match - 保存的是匹配到的正则表达式的实例，和上面的 after 相比一个是匹配到的字符串，一个是匹配到的正则表达式实例

如果 expect() 过程中发生错误，那么 before 保存到目前位置缓存里的所有数据， after 和 match 都是 None

### self.exitstatus | self.signalstatus

上面的2个值用来保存spawn子程序的退出状态，但是注意：只有使用了 process.close() 命令之后这 2 个参数才会被设置。

## 其他说明

### CR/LF约定

众所周知的是：世界上有很多种回车换行约定，它们给我们造成了很多麻烦，比如：

- windows 中用 \r\n 表示回车换行
- Linux like 系统中用 \r 表示回车换行
- Mac 系统中用 \n 表示回车换行

这种种回车换行约定对代码移植造成了很大的困难，几乎所有全平台支持的程序语言都有它们自己的解决方案，而 pexpect 的解决方案就是：

**不管哪个平台，回车换行都替换成 \r\n**

所以，如果我们要在expect中匹配回车换行符号的话，就必须这么做：

```python
process.expect('\r\n')

# 想匹配一行里的最后一个单词：
process.expect('\w+\r\n')

# 下面的匹配方式是错误的（在其他脚本语言中是正确的，比如TCL语言的Expect实现中，这也是很容易搞混淆的地方）：
process.expect('\r')
```

### $ * + 约定

正则表达式中， $ 符号表示从一行中的最后开始匹配——但是在 pexpect 中是无效的。如果要匹配一行的最后，那么必须有一行数据存在，也就是有回车换行符，但是 pexpect 的处理不是按行来进行的，它一次仅仅读一个并且处理一个字符，而且不会处理【未来】的数据。

**所以不管什么时候，都不要在 expect() 中用 $ 符号来匹配。**

正因为pexpect一次仅仅处理一个字符，所以加号 (+) 、星号 (*) 的功能也无效了，比如：

```python
# 无论何时，都只会返回一个字符
process.expect(".+")

# 无论何时，都只会返回空字符
process.expect(".*")
```

### 程序调试

```python
str(processHandle)

# 通过 pexpect.spawn() 可以创建一个进程，并通过操作这个进程的句柄来控制程序。
# 但是如果将这个句柄用 str() 函数重载一下呢？它会显示这个控制句柄的一系列内部信息，比如：
process = pexpect.spawn("ftp sw-tftp")
print str(process)
# <pexpect.spawn object at 0x2841cacc>
version: 2.3 ($Revision: 399 $)
command: /usr/bin/ftp
args: ['/usr/bin/ftp', 'sw-tftp']
searcher: searcher_re:
    0: EOF
buffer (last 100 chars):
before (last 100 chars): was 14494 bytes in 1 transfers.
221-Thank you for using the FTP service on sw-tftp.
221 Goodbye.

after: <class 'pexpect.EOF'>
match: <class 'pexpect.EOF'>
match_index: 0
exitstatus: 0
flag_eof: True
pid: 50733
child_fd: 3
closed: False
timeout: 30
delimiter: <class 'pexpect.EOF'>
logfile: None
logfile_read: None
logfile_send: None
maxread: 2000
ignorecase: False
searchwindowsize: None
delaybeforesend: 0.05
delayafterclose: 0.1
delayafterterminate: 0.1
```

### 技巧和陷阱

#### 循环匹配

Python 的 pexpect 模块与 TCL 的 expect 相比有些功能明显支持不足，其中就包括循环匹配。 TCL 的 expect 模块可以给出一系列匹配关键字，然后通过 continue 语句的设置保证同一个 expect 可以在关键字列表中重新循环。

比如一个 expect 有 3 个关键字，其中匹配到第二个关键字的时候会碰见 continue 语句，那么下一次匹配就重复这个 expect 过程，这是一个很有用的功能，比如超时时间设置为 10 秒，然后重复 3 次才会真正超时的情况。

可惜的是 Python 的 pexpect 没有这样的功能。但是想模拟这种情况也不是不可以，可以通过 while 语句来完成，比如：

```python
while True:
    index = process.expect([
        pexpect.TIMEOUT,
        pexpect.EOF,
    ]}
    if index == 0:
        print "time is out"
        # 重新从开始匹配
        continue
elif index == 1:
    print "Terminate."
    # 终止循环
    break
```

#### 获取 before 中内容的战略与清空 buffer

绝大多数情况下我们都会利用before变量来获取命令执行的结果。但是，你真的知道怎么用好 before 么？

before 中到底什么时候保存你所需的内容？这个细节必须非常清楚，我们以一个调用一个命令为例子：

这里我们预计是在 linux 系统中，下面的 handle 是一个 spawn 后的句柄，而 prompt 则是 bash 的提示符。我们预计做这样的步骤：

- 匹配提示符，以此判断系统已经准备好接受命令
- 发送命令
- 获取命令执行后的结果

```python
handle.expect(prompt)
handle.sendline("ls –l")
handle.expect(prompt)
output = handle.before
```

一共 4 个语句，就可以获取 ls –l 命令的结果了，但是且慢，是否发现有什么不合理的地方？
第一句和第二句分别是匹配系统提示符和发送命令，这都是比较正常的。

但是为什么第三句是再次匹配系统提示符？在一般的想像下，发送命令之后，设备就会执行并返回结果了，那么完全就可以用 handle.before 语句来获取到这些内容了才对啊？

实际上，从 before 这个单词就可以大概明白，它并不是实时生效的，它里面的内容，实际上是上一次 expect 匹配之后，除掉匹配到的关键字本身，系统缓存中剩余下来的全部内容。也就是说，如果第三句就是 output = handle.before的话，那么它里面的内容就是第一句的那个 expect 中去掉 prompt 内容后缓存中剩下来的内容。显然，这里面不会包括后面 ls –l 命令的内容了。
那么想获取 ls –l 的内容，唯一的办法是再增加一个 expect 关键字匹配。这是非常关键的一点。
另外， pexpect 中的 buffer 是一个关键，但又不能被直接操作的变量，它保存的是运行过程中每一个 expect 之后的所有内容，随时被更新。而 before/after 都是直接源于它的，而 expect 的关键字匹配本身也是在 buffer 中做匹配的。
正因为它的重要性，对这个变量中的内容需要特别的警惕。比如我们将登陆设备，发送命令，退出设备这3个步骤写进3个函数的时候，最好保证每个步骤都不会影响下一个步骤，在每个步骤开始的时候，最好做这样的操作：

```
handle.buffer = ""
```

## 代码实例

### FTP服务器的登陆


下面的代码比较简单，就是登陆到一个 FTP 服务器，并自动输入密码，等进入服务器以后，先输入几个预定义的命令，然后将控制权交还给用户，用户操作完成后按 <kbd>ctrl+]</kbd> 表示自己操作完成了，脚本再自动退出 ftp 登陆。

```python
#!/usr/bin/env python

import sys
import pexpect

# FTP服务器的标准提示符
ftpPrompt = 'ftp>'

# 启动FTP服务器，并将运行期间的输出都放到标准输出中
process = pexpect.spawn('ftp sw-tftp')
process.logfile_read = sys.stdout

# 服务器登陆过程
process.expect('[Nn]ame')
process.sendline('dev')
process.expect('[Pp]assword')
process.sendline('abcd1234')

# 先自动输入一些预定命令
cmdList = ("passive", 'hash')

for cmd in cmdList:
    process.expect(ftpPrompt)
    process.sendline(cmd)

process.expect(ftpPrompt)

# 在这里将FTP控制权交还给用户，用户输入完成后按 ctrl+] 再将控制权还给脚本
# ctrl+] 交还控制权给脚本是默认值，用户还可以设置其他的值，比如 ‘\x2a’
# 就是用户按星号的时候交还。这个值实际上是 ASCII 的16进制码，它们的对应关系
# 可以自己去其他地方找一下，但是注意必须是16进制的，并且前缀是 \x
process.interact()

# 当用户将控制权交还给脚本后，再由脚本退出ftp服务器
# 注意下面这个空的sendline()命令，它很重要。用户将控制权交还给脚本的时候，
# 脚本缓存里面是没任何内容的，所以也不可能匹配，这里发送一个回车符会从服务器取得
# 一些内容，这样就可以匹配了。
# 最后的EOF是确认FTP连接完成的方法。
process.sendline()
process.expect(ftpPrompt)
process.sendline('by')
process.expect(pexpect.EOF)
```

上面的脚本实际上缺少很多错误处理，比如登陆以后用户名或者密码错误，或者无法连接服务器之类的，但是核心动作已经完整了。

## 参考文档
[Pexpect 模块使用说明](https://www.jianshu.com/p/cfd163200d12)
[探索 Pexpect，第 1 部分：剖析 Pexpect](https://www.ibm.com/developerworks/cn/linux/l-cn-pexpect1/index.html)
[Pexpect version 4.6](https://pexpect.readthedocs.io/en/stable/)

## 转载说明

作者：羽风之歌
链接：https://www.jianshu.com/p/cfd163200d12
来源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

权当记录，不对外开放。
