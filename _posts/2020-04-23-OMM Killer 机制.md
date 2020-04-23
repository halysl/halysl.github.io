---
layout: post
title: Linux OOM Killer 机制
categories: [Linux]
description:
keywords: 
---

# Linux OOM Killer 机制

最近在做一项测试，总内存 256 GB，当程序“吃”了 200 G左右内存的时候就突然中止了。通过查找 `dmesg | egrep -i -B100 'killed process'`，发现有个 `out of Memory killed` 将这个测试程序干掉了，这就是 Linux 的 OOM Killer 机制。

由于 `按需分配物理页面`，所以程序可以预先获取很多的虚拟内存，当真的有数据需要填充才会分配物理内存；当多个进程真的要用这些内存了，系统发现物理内存不够用了，就启动 OMM killer 机制。这个机制简单的理解就是，内存不够用，找个内存消耗最高的干掉就好了（实际情况比较复杂）。

遇到这种问题，三个思路去处理：

- 增加物理内存（或虚拟内存）
- 查看程序是否有内存消耗 bug
- 系统层面配置 OOM Killer 机制

## 系统层面配置 OOM Killer 机制

这里又分为两个思路，要么提升 killer 执行时的阈值，要么降低 killer 执行力度。

### Overcommit 配置

这里的配置项，控制内存的申请量。

在 Linux 中，可以通过内核参数 vm.overcommit_memory 去控制是否允许 overcommit：

- 默认值是 0，在这种情况下，只允许轻微的 overcommit，而比较明显的 overcommit 将不被允许。
- 如果设置为 1，表示总是允许 overcommit。
- 如果设置为 2，则表示总是禁止 overcommit。也就是说，如果某个申请内存的操作将导致 overcommit，那么这个操作将不会得逞。

那么对内核来说，怎样才算 overcommit 呢？Linux 设定了一个阈值，叫做 CommitLimit，如果所有进程申请的总内存超过了 CommitLimit，那就算是 overcommit 了。在/proc/meminfo中可以看到 CommitLimit 的大小：

```sh
$ cat /proc/meminfo | grep CommitLimit
CommitLimit:     3829768 kB

$ sysctl -a|grep vm.overcommit_ratio
vm.overcommit_ratio = 50
```

CommitLimit 的值是这样计算的：

```
CommitLimit = [swap size] + [RAM size] * vm.overcommit_ratio / 100
```

其中的 vm.overcommit_ratio 也是内核参数，它的默认值是 50。

### OOM Killer 配置

```
$ sudo echo [-17, 15] > /proc/$(pidof xxx)/oom_adj
```

## 参考

- [Linux 的 OOM Killer 机制分析](http://senlinzhan.github.io/2017/07/03/oom-killer/)
- [Linux OMM配置](https://www.linuxba.com/archives/7744)
