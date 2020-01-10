---
layout: post
title: Linux Bond 配置（Ubuntu 18.04）
categories: [Linux, Ubuntu]
description:
keywords: 
---

# Linux Bond 配置（Ubuntu 18.04）

Linux bonding驱动提供了一个把多个网络接口设备捆绑为单个的网络接口设置来使用，用于网络负载均衡及网络冗余。

## 七种模式

|俗称|配置简称|英文名|中文名|解释|
|---|--------|----|-----|---|
|bond0|balance-rr|Round-robin policy|平衡轮询策略|传输数据包顺序是依次传输，直到最后一个传输完毕，此模式提供负载平衡和容错能力。|
|bond1|active-backup|Active-backup policy|活动备份策略|只有一个设备处于活动状态。一个宕掉另一个马上由备份转换为主设备。mac地址是外部可见得。此模式提供了容错能力。|
|bond2|balance-xor|XOR policy|平衡策略|传输根据 `(源MAC地址 xor 目标MAC地址) mod 设备数量` 的布尔值选择传输设备。 此模式提供负载平衡和容错能力。|
|bond3|broadcast|Broadcast policy|广播策略|将所有数据包传输给所有设备。此模式提供了容错能力。|
|bond4|802.3ad|IEEE 802.3ad Dynamic link aggregation|IEEE 802.3ad 动态链接聚合|创建共享相同的速度和双工设置的聚合组。此模式提供了容错能力。每个设备需要基于驱动的重新获取速度和全双工支持；如果使用交换机，交换机也需启用 802.3ad 模式。|
|bond5|balance-tlb|Adaptive transmit load balancing|适配器传输负载均衡|通道绑定不需要专用的交换机支持。发出的流量根据当前负载分给每一个设备。由当前设备处理接收，如果接受的设 备传不通就用另一个设备接管当前设备正在处理的mac地址。|
|bond6|balance-alb|Adaptive load balancing|适配器负载均衡|包括mode5，由 ARP 协商完成接收的负载。bonding驱动程序截获 ARP在本地系统发送出的请求，用其中之一的硬件地址覆盖从属设备的原地址。就像是在服务器上不同的人使用不同的硬件地址一样。|

- mode0，mode2 和 mode3 理论上需要静态聚合方式
- bond1，mode5 和 mode6 不需要交换机端的设置，网卡能自动聚合
- bond4 需要支持 802.3ad，配置交换机

## 目的

整合两个千兆网口，将速率突破 1000 Mb/s。决定使用 bond6 实现。

## 配置过程

Ubuntu 18.04 server 使用 netplan 工具配置网络，简化了很多步骤。

### bonding 模块检查

```sh
# 看有没有这个模块，若没有需要重新编译内核（基本上发行版都有）
$ modinfo bonding |more
filename:       /lib/modules/4.15.0-55-generic/kernel/drivers/net/bonding/bonding.ko
author:         Thomas Davis, tadavis@lbl.gov and many others
description:    Ethernet Channel Bonding Driver, v3.7.1
version:        3.7.1
license:        GPL
alias:          rtnl-link-bond
srcversion:     D03C823DA32FECC796F6013
depends:
retpoline:      Y
intree:         Y
name:           bonding
vermagic:       4.15.0-55-generic SMP mod_unload

# 载入模块
$ sudo modprobe bonding 

# 查看模块,如果模块已经加载，显示出来
$ sudo lsmod|grep bonding
bonding               163840  0
``` 

### 写配置文件

写 netplan 的配置文件，可以参考 [Netplan reference:bonds](https://netplan.io/reference#properties-for-device-type-bonds) 和 [Netplan configuration examples](https://netplan.io/examples#bonding)，下面给一个大致的写法。

```sh
# /etc/netplan/02-bond-config.yaml
# 上面的是文件名，记住是
# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    eno2:
      dhcp4: no
    eno3:
      dhcp4: no
    eno4:
      dhcp4: no
    eno5:
      dhcp4: no
  bonds:
    bond6:
      interfaces:
        - eno2
        - eno3
      parameters:
        mode: balance-alb
        mii-monitor-interval: 100
      addresses: 
        - "192.168.1.101/24"
      gateway4: "192.168.1.1"
      nameservers:
        addresses: 
          - "192.168.1.101"
          - "8.8.8.8"
          - "8.8.4.4"
```

### 应用服务

```sh
# netplan 应用
$ sudo netplan -v apply
# 查看 bond6 网卡的状态 
$ ethtool bond6
Settings for bond6:
	Supported ports: [ ]
	Supported link modes:   Not reported
	Supported pause frame use: No
	Supports auto-negotiation: No
	Supported FEC modes: Not reported
	Advertised link modes:  Not reported
	Advertised pause frame use: No
	Advertised auto-negotiation: No
	Advertised FEC modes: Not reported
	Speed: 2000Mb/s
	Duplex: Full
	Port: Other
	PHYAD: 0
	Transceiver: internal
	Auto-negotiation: off
Cannot get wake-on-lan settings: Operation not permitted
	Link detected: yes

# 拔掉一根网线，查看 bond6 网卡的状态 
$ ethtool bond6
Settings for bond6:
	Supported ports: [ ]
	Supported link modes:   Not reported
	Supported pause frame use: No
	Supports auto-negotiation: No
	Supported FEC modes: Not reported
	Advertised link modes:  Not reported
	Advertised pause frame use: No
	Advertised auto-negotiation: No
	Advertised FEC modes: Not reported
	Speed: 1000Mb/s
	Duplex: Full
	Port: Other
	PHYAD: 0
	Transceiver: internal
	Auto-negotiation: off
Cannot get wake-on-lan settings: Operation not permitted
	Link detected: yes
```

## 测试

从多个主机同时发送数据到配置了 bond6 的机器上，同时使用 iftop 分别监控 bond6，eno2 和 eno3 三块网卡。

```sh
# bond6 网络 I/O
$ sudo iftop -i bond6
                          204Mb                     407Mb                      611Mb                     814Mb                0.99Gb
└─────────────────────────┴─────────────────────────┴──────────────────────────┴─────────────────────────┴──────────────────────────
bond-test                                            => 192.168.1.103                                       1.44Mb  1.60Mb   428Kb
                                                     <=                                                       296Mb   345Mb  89.3Mb
bond-test                                            => 192.168.1.102                                       1.63Mb  1.39Mb   740Kb
                                                     <=                                                       324Mb   280Mb   155Mb
bond-test                                            => 192.168.1.101                                       1.46Mb  1.40Mb  1.07Mb
                                                     <=                                                       284Mb   279Mb   255Mb
bond-test                                            => 192.168.1.140                                       12.1Kb  11.5Kb  10.9Kb
                                                     <=                                                      3.86Kb  3.49Kb  4.24Kb
bond-test                                            => xxxxxxxxx                                               0b    126b    394b
                                                     <=                                                         0b    126b    410b
all-systems.mcast.net                                => 0.0.0.0                                                 0b      0b      0b
                                                     <=                                                         0b      0b      6b
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
TX:             cum:   11.1MB   peak:   4.58Mb                                                      rates:   4.55Mb  4.41Mb  2.22Mb
RX:                    2.44GB            921Mb                                                                905Mb   904Mb   500Mb
TOTAL:                 2.45GB            925Mb                                                                909Mb   908Mb   502Mb

# eno2 网络 I/O
$ sudo iftop -i eno2
                         204Mb                     407Mb                      611Mb                     814Mb                0.99Gb
└─────────────────────────┴─────────────────────────┴──────────────────────────┴─────────────────────────┴──────────────────────────
bond-test                                            => 192.168.1.102                                        390Kb   741Kb   185Kb
                                                     <=                                                      73.2Mb   221Mb   243Mb
bond-test                                            => 192.168.1.101                                        509Kb   982Kb   960Kb
                                                     <=                                                         0b      0b      0b
bond-test                                            => 192.168.1.103                                          0b    341Kb   419Kb
                                                     <=                                                         0b      0b      0b
bond-test                                            => 192.168.1.140                                          0b      0b   2.76Kb
                                                     <=                                                      2.84Kb  2.88Kb  3.18Kb




────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
TX:             cum:   7.66MB   peak:   3.07Mb                                                      rates:    899Kb  2.02Mb  1.53Mb
RX:                    1.19GB            547Mb                                                               73.2Mb   221Mb   243Mb
TOTAL:                 1.19GB            548Mb                                                               74.0Mb   223Mb   245Mb

# eno3 网络 I/O
$ sudo iftop -i eno3
                         204Mb                     407Mb                      611Mb                     814Mb                0.99Gb
└─────────────────────────┴─────────────────────────┴──────────────────────────┴─────────────────────────┴──────────────────────────
bond-test                                            => 192.168.1.103                                       1.44Mb  1.38Mb  0.99Mb
                                                     <=                                                       336Mb   327Mb   315Mb
bond-test                                            => 192.168.1.101                                          0b      0b      0b
                                                     <=                                                       295Mb   218Mb   244Mb
bond-test                                            => 192.168.1.140                                       10.1Kb  11.0Kb  10.8Kb
                                                     <=                                                         0b      0b      0b
bond-test                                            => 192.168.1.102                                          0b      0b    703Kb
                                                     <=                                                         0b      0b      0b
bond-test                                            => xxxxxxxxx                                               0b      0b     31b
                                                     <=                                                         0b      0b     31b



────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
TX:             cum:   12.3MB   peak:   2.87Mb                                                      rates:   1.45Mb  1.39Mb  1.68Mb
RX:                    3.52GB            692Mb                                                                631Mb   545Mb   560Mb
TOTAL:                 3.53GB            694Mb                                                                632Mb   546Mb   561Mb

```

从上述结果做分析，可以看出，bond6 网卡的传输速度上限还是 1000 Mb/s。

再去看 bond6 实现原理：bonding 驱动截获本机发送的 ARP 应答，并把源硬件地址改写为 bond 中某个 slave 的唯一硬件地址，从而使得不同的对端使用不同的硬件地址进行通信。`所以对交换机来说只有一个端口可以用，所以瓶颈可能在千兆交换机上`。等换了万兆交换机再做测试。

## 参考

- [Netplan reference:bonds](https://netplan.io/reference#properties-for-device-type-bonds)
- [Netplan configuration examples](https://netplan.io/examples#bonding)
- [Linux 配置双网卡绑定，实现负载均衡](https://blog.51cto.com/balich/2131991)
- [Linux下多网卡绑定bonding bond6](https://blog.csdn.net/morigejile/article/details/78699618)
- [Bond轻松提高网速，将网卡协商速率从1000Mb/s提升到2000Mb/s](https://www.jianshu.com/p/772b31b4a394)
- [Linux(CentOS)网络流量实时监控（iftop）](https://blog.csdn.net/gaojinshan/article/details/40781241)
- [Linux 网卡bond的七种模式](https://www.jianshu.com/p/b93027ae1e94)
- [深入浅出多网卡绑定技术](https://blog.51cto.com/alanwu/1095566)
- [网卡bonding模式 - bond0、1、4配置](https://www.cnblogs.com/kaishirenshi/p/10245228.html)
- [linux——如何添加网卡做bond5聚合？](https://blog.51cto.com/13859004/2144578)
- [Linux Bonding](https://www.learnfuture.com/InnerSite/ArticleContent?code=6524)
