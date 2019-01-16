https://blog.csdn.net/luckytanggu/article/details/51793218

https://stackoverflow.com/questions/1506010/how-to-use-export-with-python-on-linux

## python中使用shell command

这个问题没什么太多难度，这里只是做个记录。

只使用标准库的情况下，有四种方法去实现。

### 方法一: os.system(cmd)

在子终端运行系统命令，不能获取命令执行后的返回信息以及执行返回的状态。

```
import os
os.system('date')
# 2019年 1月16日 星期三 18时14分21秒 CST
```

### 方法二： os.popen(cmd)

不仅执行命令而且返回执行后的信息对象(常用于需要获取执行命令后的返回信息)

```
import os
nowtime = os.popen('date')
print nowtime.read()
# 2019年 1月16日 星期三 18时14分21秒 CST
```

### 方法三： commands模块

方法|说明
----|---
getoutput|获取执行命令后的返回信息
getstatus|获取执行命令的状态值(执行命令成功返回数值0，否则返回非0)
getstatusoutput|获取执行命令的状态值以及返回信息

```
import commonds
status, output = commands.getstatusoutput('date')
print status    # 0
print output    # 2019年 1月16日 星期三 18时14分21秒 CST
```


### 方法四：subprocess模块

这是最复杂的模块（实现系统指令），但也是功能最多的模块。学会了subprocess模块，再去看paramiko或者其他（实现系统指令）模块会更轻松。