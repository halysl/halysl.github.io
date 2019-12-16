---
layout: post
title: Lotus daemon 全过程
categories: [Go, Lotus, 区块链]
description: 
keywords: 
---

# Lotus daemon 全过程

`lotus daemon` 会生成一个守护进程，那么它在这个过程中做了哪些事？

## 大致过程

- 通过命令行读取参数
- 拿到指定的 repo 或者使用默认的 repo(就是一个路径值)，计作 $PATH，根据它进行服务初始化的操作
  - 根据是否存在 $PATH/datastore，判断是否已经运行过服务，如果运行过就报警告，否则创建 $PATH 目录
  - 创建默认的 $PATH/config.toml 文件
  - 创建 $PATH/keystore 文件夹
- 根据 build/proof-parameters.json/parameters.json 里的数据对 /var/tmp/filecoin-proof-parameters/ 的证明参数文件进行校验
- 如果制定了 genesis 参数，则使用，否则从 build/genesis/devnet.car 生成，生成块逻辑比较复杂，如果指定了 lotus-make-random-genesis 和 genesis-presealed-sectors 参数，则可以通过逻辑生成一个，逻辑比较复杂
- 然后就是创建一个逻辑节点，先声明了一个接口，定为 api
  - 通过 node.New 生成一个完整节点，第一步先把 子系统的api 和主节点的 api 绑定在一起，具体实现依赖的是子系统
  - 根据节点类型，会更新一些配置项，配置项分为：调用，模块，会有非常多的模块，比较重要的有 SetApiEndpointKey
- 通过 serveRPC 返回一个 rpc 服务
