---
layout: post
title: centos-root LVM 扩容问题
categories: [Linux]
description:
keywords: 
---

# centos-root LVM 扩容问题

最近开了一个 jumpserver 服务，突然挂了，一查原来是系统的根目录只有50G，数据写不下了，只剩 40k 的空间。好在 centos7 默认使用 LVM 进行文件系统的挂载，那只有加盘了。

加上 1 TiB 的硬盘，通过 `pvcreate /dev/sdb `，出现 `Device /dev/sdb excluded by a filter`。此时因为该盘可能因为有分区，所以不行，可以尝试 `wipefs -a /dev/sdb` 来解决问题。

然后再让 vg：centos 增加一块 pv ：`vgextend centos /dev/sdb`。此时可能会出现 `Couldn't create temporary archive name`。这是因为根目录可用空间太少了，删点日志再执行这个指令就可以了。

接着 vg 就有可用空间了，使用 lvextend 增加容量：`lvextend -L +1024G /dev/mapper/centos-root`。这里一般不会有什么问题，会直接通过。

但是上部操作完成后，查看 `df -h` 还是只有 50G，因为没有让系统知道这件事。国内的资料显示需要执行：`e2fsck -f /dev/mapper/centos-root` 和 `resize2fs /dev/mapper/centos-root`。但我执行都不可以，会说 root 已经挂载，那么只能在维护模式下使用？那不就还是要重启？

在一篇英文资料中提到，可以执行 `fsadm resize /dev/centos/root` 通知系统文件系统大小已经变更。

```
$ wipefs -a /dev/sdb
$ pvcreate /dev/sdb
$ vgextend centos /dev/sdb
$ lvextend -L +1024G /dev/mapper/centos-root
$ fsadm resize /dev/centos/root
```

## 参考

- [pvcreate : “device excluded by a filter”](https://serverfault.com/questions/917650/vgextend-device-excluded-by-a-filter)
- [vgextend fail on Couldn't create temporary archive name](https://unix.stackexchange.com/questions/465719/vgextend-fail-on-couldnt-create-temporary-archive-name)
- [Logical Volume /dev/centos/root is extended but /dev/mapper/centos-root is not](https://serverfault.com/questions/934024/logical-volume-dev-centos-root-is-extended-but-dev-mapper-centos-root-is-not)
- [Linux LVM扩容](https://www.jianshu.com/p/b41c7b2fffe1)
