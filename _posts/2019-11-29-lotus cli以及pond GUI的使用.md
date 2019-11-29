---
layout: post
title: Lotus CLI 以及 Pond GUI 的使用
categories: [Go, Lotus, 区块链]
description: Lotus 是基于 IPFS 技术上的激励层 FileCoin 的一种实现，它区别于 go-filecoin 是一种不同的实现，但是底层的架构极为相似。Lotus CLI 是实现 Lotus 的命令行界面工具。Pond GUI 是基于 Lotus 的图形用户界面。
keywords: 
---


# Lotus CLI 以及 Pond GUI 的使用

## 说明

[Lotus](https://github.com/filecoin-project/lotus) 是基于 IPFS 技术上的激励层 FileCoin 的一种实现，它区别于 [go-filecoin](https://github.com/filecoin-project/go-filecoin) 是一种不同的实现，但是底层的架构极为相似。

Lotus CLI 是实现 Lotus 的命令行界面工具。

Pond GUI 是基于 Lotus 的图形用户界面。

## Lotus 的安装

### 需要依赖

- go (1.13 or higher)
- gcc (7.4.0 or higher)
- git (version 2 or higher)
- bzr (some go dependency needs this)
- jq
- pkg-config
- opencl-icd-loader
- opencl driver (like nvidia-opencl on arch) (for GPU acceleration)
- opencl-headers (build)
- rustup (proofs build)
- llvm (proofs build)
- clang (proofs build)

### 下载

```shell
$ git clone https://github.com/filecoin-project/lotus.git
$ cd lotus/
```

### 安装

```shell
$ make clean all
$ sudo make install
```

安装过程会出现不少问题，其中一个就是没有 rustup 工具。可以参考 [Rust 版本管理工具: rustup](https://wiki.jikexueyuan.com/project/rust-primer/install/rustup.html)。安装完 rustup 可以[配置 Rust Crates 镜像](https://lug.ustc.edu.cn/wiki/mirrors/help/rust-crates)，以加快安装编译的速度。

## Pond UI

Pond UI 是基于 Lotus 的图形用户界面，除了页面上执行 Lotus CLI 的功能，它还可以模拟一个简单的 filecoin 网络，我们先编译下，然后再运行。

```shell
$ make pond
$ ./pond run
Listening on http://127.0.0.1:2222
```

打开 `http://127.0.0.1:2222` 就可以看到可视化界面了，我们点到左下角的 `open pond` 就可以打开模拟界面，但是里面的按钮对应关系是什么，就得看看 Lotus CLI 做了什么。

> 如果模拟的中途出现了 `wait for init...` 等消息，观察终端输出，是否在下载加密文件，如果是，等待就好，但是默认的 `IPFS_GATEWAY` 可能连接过慢，可以尝试在 [Public IPFS Gateways](https://ipfs.github.io/public-gateway-checker/) 平台寻找一个快点的 `IPFS_GATEWAY`， 终端 export 下就好了。

> 注意: 不要让 Pond 长时间无人值守(10小时以上) ，web-ui 最终会消耗掉所有可用的 RAM。

## Devnet(开发网络？)

### 大致流程

- 启动 Lotus 节点
- 同步链接网络
- 创建钱包地址
- 去 [LOTUS DEVNET FAUCET](https://lotus-faucet.kittyhawk.wtf/) 拿点启动资金
- 根据钱包地址去 [CREATING STORAGE MINER](https://lotus-faucet.kittyhawk.wtf/miner.html) 创建矿工
- 初始化矿工
- 开始挖矿(?)
- 构建将要保存的数据
- 交易
- 查询和收回

### 启动 Lotus 节点

```shell
$ lotus daemon
```

后台会运行 Lotus 程序，此时我们保持这个 session，另起一个 session 去执行 Lotus CLI 所提供的功能。

检查是否连接到网络：

```shell
$ lotus net peers | wc -l
2
```

### 同步链接网络

```shell
$ lotus sync wait
```

### 创建钱包并拿到启动资金

```shell
$ lotus wallet new bls
t3...
```

 > t3.... 是一个钱包地址

去 [LOTUS DEVNET FAUCET](https://lotus-faucet.kittyhawk.wtf/) 拿点启动资金，复制钱包地址获取资金

```shell
$ # 查看余额
$ lotus wallet balance [optional address t3.....]
```

### 挖矿

1. 确保存在一个 BLS 钱包地址
2. 去 [CREATING STORAGE MINER](https://lotus-faucet.kittyhawk.wtf/miner.html) 创建矿工，输入钱包地址
3. 等待页面返回，应该会有：`New storage miners address is: t0..`
4. 初始化矿工：`lotus-storage-miner init --actor=t01.. --owner=t3....  `
5. 开始挖矿：`lotus-storage-miner run`

> t0....指的是矿工的地址

查看用于交易的矿工id:

```shell
$ lotus-storage-miner info
```

对区块写入随机数据以拿到 PoSts(Proof-of-Storage，存储工作量证明)：

```shell
$ lotus-storage-miner store-garbage
```

根据矿工 id 查看存储矿工的电源和扇区使用信息：

```shell
$ lotus-storage-miner state power <miner_id>
$ lotus-storage-miner state sectors <miner_id>
```

### 构建数据

通过导入的方式构建一些简单的数据，拿到对应的数据 id，即 Data CID。

```shell
# Create a simple file
$ echo "Hi my name is $USER" > hello.txt

# Import the file into lotus & get a Data CID
$ lotus client import ./hello.txt
<Data CID>

# List imported files by CID, name, size, status
$ lotus client local
```

> CID 指的是 Content Identifier，用来自我描述内容地址，它是一个加密散列，唯一映射到数据并验证数据没有更改。

### 交易

交易不限制交易双方所在的节点，即需求方可以在同一个 Lotus Node 上与矿工达成协议。

```shell
# 展示系统中所有的矿工
$ lotus state list-miners
# 询问矿工
$ lotus client query-ask <miner>
# 和矿工提出交易 价格以 attoFIL/byte/block 为单位 持续时间以 block 为单位
$ lotus client deal <Data CID> <miner> <price> <duration>
```

如果交易成功，返回一个 deal CID，它和前面的 data CID 是不一样的。

### 搜索和获取数据

通过 Data CID 搜索/获取。

```shell
$ lotus client find <Data CID>
LOCAL
RETRIEVAL <miner>@<miner peerId>-<deal funds>-<size>
```

```shell
$ lotus client retrieve <Data CID> <outfile>
```
