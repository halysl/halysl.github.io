---
layout: post
title: 转载-利用srvctl管理RAC数据库
categories: [Oracle, RAC, srvctl]
description: 
keywords: Oracle, 转载， RAC
---

# 【转】利用 srvctl 管理 RAC 数据库

srvctl 即 Server Control，是 Oracle 提供的一个命令行工具，用以用于管理 Oracle 的 RAC 环境。srvctl 在 Oracle 9i 中被引入，Oracle10g、11g 对其功能进行了很大的增强和改进。下面介绍下此命令的简单用法。

## 一、 查看实例状态（srvctl status）

- 查询所有实例和服务的状态：

```shell
[oracle@node-rac1 ~]$ srvctl status database -d racdb
Instance racdb2 is running on node node-rac2
Instance racdb1 is running on node node-rac1
```

- 查询实例 racdb1 的状态：

```shell
[oracle@node-rac1 ~]$ srvctl status instance -d racdb -i racdb1 
Instance racdb1 is running on node node-rac1
```

- 查询实例 racdb2 的状态：

```shell
[oracle@node-rac1 ~]$ srvctl status instance -d racdb -i racdb2
Instance racdb2 is running on node node-rac2
```

- 查询特定节点上应用程序的状态：

```shell
[oracle@node-rac1 ~]$ srvctl status nodeapps -n node-rac2
VIP is running on node: node-rac2
GSD is running on node: node-rac2
Listener is running on node: node-rac2
ONS daemon is running on node: node-rac2
```

- 查询特定节点上 ASM 实例的状态

```shell
[oracle@node-rac1 ~]$ srvctl status asm -n node-rac2
ASM instance +ASM2 is running on node node-rac2.
```

> 在上面的命令行操作中，都用到的参数是：
> 
> - -d，即 database name，表示数据库名称
> - -n，即 node name，表示节点 hostname
> - -i，即 instance name，表示实例名称

## 二、 查看 RAC 数据库设置信息（srvctl config）

- 显示 RAC 数据库的配置：

```shell
[oracle@node-rac1 ~]$ srvctl config database -d racdb
node-rac2 racdb2 /u01/oracle/product/11.0.6/rac_db
node-rac1 racdb1 /u01/oracle/product/11.0.6/rac_db
```

- 列出配置的所有数据库：

```shell
[oracle@node-rac1 ~]$ srvctl config database
racdb
```

- 显示指定节点的应用程序配置：

```shell
[oracle@node-rac1 ~]$ srvctl config nodeapps -n node-rac2
VIP exists.: /node-vip2/192.168.12.240/255.255.255.0/eth0
GSD exists.
ONS daemon exists.
Listener exists.
```

- 显示指定节点的 ASM 实例配置：

```shell
[oracle@node-rac1 ~]$ srvctl config asm -n node-rac2        
+ASM2 /u01/oracle/product/11.0.6/rac_db
```

## 三、 启动/关闭实例（srvctl start/stop）17

- 停止 Oracle RA C所有服务：

```shell
[oracle@node-rac1 ~]$ emctl stop dbconsole
[oracle@node-rac1 ~]$ srvctl stop instance -d racdb -i racdb1
[oracle@node-rac1 ~]$ srvctl stop asm -n node-rac1
[oracle@node-rac1 ~]$ srvctl stop nodeapps -n node-rac1
```

- 也可以通过一条命令停止所有实例及其启用的服务：

```shell
[oracle@node-rac1 ~]$srvctl stop database -d racdb
```

- 启动 Oracle RAC 所有服务：

```shell
[oracle@node-rac1 ~]$ srvctl start nodeapps -n node-rac1
[oracle@node-rac1 ~]$ srvctl start asm -n node-rac1
[oracle@node-rac1 ~]$ srvctl start instance -d racdb -i racdb1
[oracle@node-rac1 ~]$ emctl start dbconsole
```

- 也可以通过一条命令启动所有实例及其启用的服务：

```shell
[oracle@node-rac1 ~]$srvctl start database -d racdb
```

## 四、 增加/删除/修改实例（srvctl add/remove/modify）

- 增加一个服务，然后在节点间切换此服务：

```shell
[oracle@node-rac1 ~]$ srvctl add service -d racdb -s test -r racdb1 -a racdb2 -P BASIC
```

> 其中参数的含义如下：
> 
> - -r，表示首选实例
> - -a，表示可用的实例
> - -P，表示故障切换策略，有 none、BASIC、preconnect 三个可选项

- 在集群节点之间切换集群服务：

```shell
[oracle@node-rac1 ~]$ srvctl start service -d racdb -s test -i racdb1
[oracle@node-rac1 ~]$ srvctl status service -d racdb -s test
Service test is running on instance(s) racdb1
[oracle@node-rac1 ~]$ srvctl stop  service  -d racdb -s test -i racdb1   
[oracle@node-rac1 ~]$ srvctl start  service  -d racdb -s test -i racdb2
[oracle@node-rac1 ~]$ srvctl status  service  -d  racdb -s test
Service test is running on instance(s) racdb2
```

- 从某个实例节点移除一个服务：

```shell
[oracle@node-rac1 ~]$ srvctl remove service -d racdb -s test -i racdb2
test PREF: racdb1 racdb2 AVAIL: 
Remove service test from the instance racdb2? (y/[n]) y
```

- 使数据库服务对某个实例可用：

```shell
[oracle@node-rac1 ~]$ srvctl add service -d racdb -s test -u -a racdb2
[oracle@node-rac1 ~]$ srvctl start service -d racdb -s test           
[oracle@node-rac1 ~]$ srvctl modify service -d racdb -s test -i racdb2 –r
```

## 转载信息

- 作者：南非蚂蚁 
- 来源：51CTO
- 原文：https://blog.51cto.com/ixdba/970802
- 版权声明：本文为博主原创文章，转载请附上博文链接！