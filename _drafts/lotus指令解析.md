# Lotus 指令解析

## lotus

### 总揽

```shell
NAME:
   lotus - Filecoin 分布式存储网络客户端

USAGE:
   lotus [global options] command [command options] [arguments...]

VERSION:
   0.7.0

COMMANDS:
     daemon            启动一个守护进程
     auth              RPC 权限管理
     chain             filecoin 区块链交互信息
     client            处理交易、存储数据、检索数据
     createminer       创建全新的存储矿工（暂未使用）
     fetch-params      获得证明参数
     mpool             信息池 管理
     net               P2P 网络管理
     paych             报酬支付管理
     send              账户间转账
     state             filecoin 链上状态
     sync              链上同步模块
     version           打印版本
     wallet            钱包管理
     help, h           帮助文件

GLOBAL OPTIONS:
   --help, -h     show help (default: false)
   --version, -v  print the version (default: false)
```

### lotus daemon

启动 Lotus 后台服务。

```shell
NAME:
   lotus daemon - Start a lotus daemon process

USAGE:
   lotus daemon [command options] [arguments...]

OPTIONS:
   --api value      (default: "1234")
   --genesis value  genesis file to use for first node run
   --bootstrap      (default: true)
   --help, -h       show help (default: false)
```

默认的配置会连接到公链，如果需要连接私链，需要手动配置 --bootstrap 和 --genesis。

### lotus auth

[wait....]

### lotus chain

filecoin 区块链交互信息。

```shell
NAME:
   lotus chain - Interact with filecoin blockchain

USAGE:
   lotus chain command [command options] [arguments...]

COMMANDS:
     head        打印链头（最新一项）
     getblock    获得特定块的信息
     read-obj    读取特定块信息并转成二进制
     getmessage  Get and print a message by its cid
     sethead     人为设置本地节点头部（注意：通常仅用于恢复）
     list        查一整块的链上信息（默认30个）
```

`lotus chain head` 返回最新的链头

`lotus chain getblock block-id` 该 id 可以通过 `lotus chain head` 和 `lotus chain list` 获取。返回结果比较重要。

`lotus chain read-obj block-id` 原始数据

#### lotus chain getblock block-id 的结果

返回一个 json 数据结构。

```json
{
  "Miner": "t01002", // 矿工名
  "Ticket": {  // 选票信息
    "VRFProof": "hFVn5AlPJMiv//oArwHcF7K7inN/ n01VLU0KODtepZTAXDw1I1FPAKlsx+YHb6ZeFLwTEgT2s7m3EDgHQzm3sTvAQUrRAPFZzFPuuonpoSSg67Z2AoAzzElhrzWi5X0i"  // VRF 证明
  },
  "EPostProof": { // EPost 证明
    "Proof": "maioEUYP2Ldgt8xTzmUZpIaVDV6+oQOmyDqNwo2ECTAe/m6oVy63U/yvOFXfiInrqth7hap2Py4zMZpevL7Lkj7/V5+M74eTUBwEHhS3jHCejB76aZeRJG8/sjF4qyorC33UoCPCJ3tEzzpC72LDxbg+q5AohLAkA2cJG29HCM3hDraB+zKnc+sV6gEleSKYlGqU5YKOfMOvycDkzvE6kBPdSxg0RIJBAcNFLgq4kLygoTQg+QAw9NxwtvhQXe2h", // 证明信息
    "PostRand": "peNP75G6wZZKjmqEvvZr5gzYnM/Rvg5YGAeW2StIy0cU5tIfj2JBc6dBo4OW0bAEGV1pKjCh3TQAoayNTQFU+zmf1c/NkgxmGaowArdqCsz4RJOQNWKuyjsg+I3qAk1n", // 提交随机
    "Candidates": [  // 候选人
      {
        "Partial": "Y3JWpHDZFQFI37t7eCvb5FzfB0O00VGZrRiEIjeCDDg=",
        "SectorID": 1,
        "ChallengeIndex": 0
      }
    ]
  },
  "Parents": [ // 父链信息
    {
      "/": "bafy2bzacedl2tjmci637mw72thezibn3nkloklajc2buemsaar6g6xdqnliwm"
    },
    {
      "/": "bafy2bzaceaaupypmv6dlqnrelt5vhoyp3refw5mrpkdr5kss3ck7beoptxs6c"
    }
  ],
  "ParentWeight": "1483923", // 父链权重
  "Height": 205, // 块高
  "ParentStateRoot": { // 父链状态
    "/": "bafy2bzacedf2znux35fi3tpk7skrijxuqwr26hluhdrjf62amd6rh4e7pgpgc"
  },
  "ParentMessageReceipts": { // 父链信息收据
    "/": "bafy2bzaceaa43et73tgxsoh2xizd4mxhbrcfig4kqp25zfa5scdgkzppllyuu"
  },
  "Messages": { // 信息
    "/": "bafy2bzacecgw6dqj4bctnbnyqfujltkwu7xc7ttaaato4i5miroxr4bayhfea"
  },
  "BLSAggregate": {
    "Type": "bls",
    "Data": "wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
  },
  "Timestamp": 1575357999, // 时间戳
  "BlockSig": { // 块签名
    "Type": "bls",
    "Data": "mNTR7BXir41EWZOZaunYpqaJoiLhaSFCfXAhS8aB5MtsAOzDcwfu5jcyKLqTrhPCBZGdJFR0BIRaLEkV1NanoknfLbaDAwgdNywJGP3kAgmXny/vRHBFYNA/5UfAOl6I"
  },
  "BlsMessages": [
    
  ],
  "SecpkMessages": [
    
  ],
  "ParentReceipts": null,
  "ParentMessages": [
    
  ]
}
```

其中有不少概念还没明确，需要看代码和 spec 文档熟悉。

### lotus client

处理交易、存储数据、检索数据。

```sh
NAME:
   lotus client - Make deals, store data, retrieve data

USAGE:
   lotus client command [command options] [arguments...]

COMMANDS:
     import      导入本地数据
     local       查看本地已导入数据
     deal        和一个矿工初始化交易
     find        从网络上查找数据
     retrieve    从网络中收回数据
     query-ask   向矿工询价
     list-deals  列出市场所有交易
```

`lotus client import $FILEPATH` 导入文件

`lotus client deal $DATA-CID $MINER-ID $PRICE $DURATION`：$DATA-CID 可以通过 `lotus client local` 查出，$MINER-ID 可以通过 `lotus state list-miners` 查出， $PRICE 和 $DURATION 自定，分别是价格和持续时间。

`lotus client find $DATA-CID`：$DATA-CID 可以通过 `lotus client local` 查出

`lotus client retrieve $DATA-CID $OUTPUTPATH`：$DATA-CID 可以通过 `lotus client local` 查出

### lotus mpool

[wait...]

### lotus net

P2P网络的管理。

```shell
NAME:
   lotus net - Manage P2P Network

USAGE:
   lotus net command [command options] [arguments...]

COMMANDS:
     peers    打印出节点信息
     connect  连接一个对端节点
     listen   列出本机监听地址
     id       获得当前节点认证ID
```

### lotus paych

[wait...]

### lotus send

资金流动。

```shell
NAME:
   lotus send - Send funds between accounts

USAGE:
   lotus send [command options] <target> <amount>

OPTIONS:
   --source value  optinally specifiy the account to send funds from
```

`lotus send [--source=$SOURCE-CID] $DES-CID $NUMBER`：$SOURCE-CID 和 $DES-CID 指的是钱包地址，可以通过 `lotus wallet list` 查询

### lotus state

filecoin 链上状态。

```shell
NAME:
   lotus state - Interact with and query filecoin chain state

USAGE:
   lotus state command [command options] [arguments...]

COMMANDS:
     power              询问网络或者矿工的算力
     sectors            询问矿工有的区块集合
     proving            询问矿工可以提供的区块
     pledge-collateral  获得矿工承诺抵押
     list-actors        列出网络中所有角色
     list-miners        列出网络中所有矿工
     get-actor          打印出角色详情
     lookup             找到相应的 ID 地址
```

`lotus state power [$MINER-ID]`：默认全网算力，可指定矿工 id

### lotus sync

链上同步模块，后台也在执行。

```shell
NAME:
   lotus sync - Inspect or interact with the chain syncer

USAGE:
   lotus sync command [command options] [arguments...]

COMMANDS:
     status   查看同步状态
     wait     等待同步完成
```

### lotus wallet

钱包相关功能。

```shell
NAME:
   lotus wallet - Manage wallet

USAGE:
   lotus wallet command [command options] [arguments...]

COMMANDS:
     new          创建一个新的给定类型的钱包
     list         展示所有钱包地址
     balance      获取钱包余额
     export       导出 key
     import       导入 key
     default      获得默认钱包地址
     set-default  设置默认钱包地址
```

`lotus wallet new [bls|secp256k1]`：创建 bls 或者 secp256k1 类型的钱包

`lotus wallet balance [$WALLET-ADDRESS]`：不指定则默认查看默认钱包的余额


## Lotus-storage-miner

```sh
NAME:
   lotus-storage-miner - Filecoin decentralized storage network storage miner

USAGE:
   lotus-storage-miner [global options] command [command options] [arguments...]

VERSION:
   0.7.0

COMMANDS:
     run               Start a lotus storage miner process
     init              Initialize a lotus storage miner repo
     info              Print storage miner info
     store-garbage     store random data in a sector
     sectors           interact with sector store
     auth              Manage RPC permissions
     chain             Interact with filecoin blockchain
     client            Make deals, store data, retrieve data
     createminer       Create a new storage market actor
     fetch-params      Fetch proving parameters
     mpool             Manage message pool
     net               Manage P2P Network
     paych             Manage payment channels
     send              Send funds between accounts
     state             Interact with and query filecoin chain state
     sync              Inspect or interact with the chain syncer
     unregister-miner  Manually unregister miner actor
     version           Print version
     wallet            Manage wallet
     help, h           Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --storagerepo value  (default: "~/.lotusstorage") [$LOTUS_STORAGE_PATH]
   --help, -h           show help (default: false)
   --version, -v        print the version (default: false)
   ```
   