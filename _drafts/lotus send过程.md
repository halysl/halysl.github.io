# Lotus send 全过程

lotus send 可以在钱包间转账。

## 大致过程

- 获得操作句柄（拿到api）
- 计算对方钱包地址
- 计算转账量
- 使用api的默认钱包地址或者指定的钱包地址
- 将转账信息记录到 mpool 里

## 获得操作句柄

- 通过 repo 参数（默认为~/.lotus），找到一个存储数据的路径，记为 PATH
- 从 $PATH/api 拿到 api 端点信息，通过 multiaddr.NewMultiaddr 转换为 byte 数组， 记为 apiInfo
- apiInfo 通过 manet.DialArgs 解析出协议和 Linux 网络地址
- 从 $PATH/token 拿到 token 信息，并加在默认 http.header 里，至此已经拿到了 `网络地址` 和 `带 token 的 header`
- 再根据拿到的两个数据通过一次 NewFullNodeRPC 处理，拿到操作句柄（暂时是一个struct），网络关闭函数

## 计算对方钱包位置

- 从命令行拿到原始的数据，记为 wls
- 对 wls 进行解码，根据 wls 的第二位判断协议类型，从第三位到结尾则是原始数据，记为 raw，进入下一步解码
- 使用一个自定义的 encoding 对 raw 进行解密，然后拆分成 payload 和 cksm
- 使用 ValidateChecksum 检测 payload 是否有效
- 通过 protocol 和 payload 创建新的地址，此时就拿到了钱包地址

## 计算转账量

- 这个纯粹就是通过字符串进行数学运算，牵扯到的过程还挺复杂的，主要依赖了 math/big/Rat 结构体，它表示任意精度的商 a / b
- 比较重要的一步转换是通过创建一个 big.NewRat(build.FilecoinPrecision, 1)，然后对转账量进行一个处理，简单来说就是放大 10^18 次方（针对十进制），并且使b为1

## 使用api的默认钱包地址或者指定的钱包地址

- 如果指定了 source 信息，则类似 计算对方钱包位置 一样计算一个钱包地址
- 如果没有指定，则使用 api 的 WalletDefaultAddress 方法实现
- 通过 ~/.lotus/keystore 里的文件进行查询

## 将转账信息记录到 mpool 里

- 构建一个 message 结构，目前 GasLimit 和 GasPrice 都是固定的
- 使用 api 的 MpoolPushMessage 方法实现
  - 通过 message 进行处理，判断余额是否足够传递
  - 通过 mp.getNonceLocked 拿到 nonce
  - 将 nonce 加入到 message里，对 message 的每一项数据根据类型进行不同处理，将结果写入到buffer，记为data，然后根据data生成一个cid，这两个参数通过 block.NewBlockWithCid 获取新块
  - 通过 message 的 from address 和 cid 信息，创建签名文件
  - 通过 PubSubPublish 进行数据传递
- 数据传递过程

问题：api 到底是个什么东西
