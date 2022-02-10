# GossipSub Quick Start

流言订阅机制。

[publish-subscribe](https://docs.libp2p.io/concepts/publish-subscribe/)

## peer-to-peer pub/sub system 设计目标

- Reliability（可靠）: All messages get delivered to all peers subscribed to the topic.
- Speed（快速）: Messages are delivered quickly.
- Efficiency（高效率）: The network is not flooded with excess copies of messages.
- Resilience（高弹性）: Peers can join and leave the network without disrupting it. There is no central point of failure.
- Scale（大规模）: Topics can have enormous numbers of subscribers and handle a large throughput of messages.
- Simplicity（简单）: The system is simple to understand and implement. Each peer only needs to remember a small amount of state.

## Discovery peer

- Distributed hash tables：分布式哈希表
- Local network broadcasts：本地网络广播
- Exchanging peer lists with existing peers：与现有对等体交换对等体名单
- Centralized trackers or rendezvous points：集中式跟踪器或会合点
- Lists of bootstrap peers：引导性对等体的列表

## Types of peering（对等互联的分类）

![types_of_peering](https://docs.libp2p.io/concepts/publish-subscribe/types_of_peering.png)

单个的点称之为 peer，多个独立的点称之为 peers，而两个点的连线称之为 peering。peering有两种：

- full-message：peer 间传递完整的信息。network degree 是一个很重要的概念，它表明一个 peer 需要向多少个 peer 传递完整消息，默认等级为6，允许设置成4-12。过多的连接会导致信息冗余但同时增加网络弹性，过少则会降低网络弹性
- metadata-only：peer 间只传递元信息，它传递较少的数据，同时负责维护 full-message 网络。

## Grafting and pruning（嫁接和修剪）

- Grafting：metadata-only convert to full-message
- pruning：full-message convert to metadata-only

对等关系是双向的，这意味着对于任何两个连接的对等体，两个对等体都认为他们的连接是全信息的，或者两个对等体都认为他们的连接是纯元数据的。任何一个对等体都可以通过通知对方来改变连接类型。

当一个对等体有太少的全消息对等体时，它将随机嫁接一些仅有元数据的对等体，成为全消息对等体。相反，当一个对等体有太多的全消息对等体时，它将随机地将其中一些对等体修剪成只包含元数据。

每个对等体每隔1秒执行一系列的检查。这些检查被称为 "心跳"。嫁接和修剪就发生在这段时间。

## Subscribing and unsubscribing

整个网络会存在多个主题（topic），一个对等点可以订阅多个topic。上述的对等互联的分类以及嫁接修剪都要建立在主题下。

简单的说，一个 p2p 网络中存在100个节点，存在5个主题，每个主题各有30个对等点进行数据交互。在同一个主题下才会区分 full-message 和 metadata-only。

两个 peer 连接的第一件事就是互相通知各自的主题订阅信息。当一个 peer 订阅或者退订都会通知它所连接的所有 peer。

订阅和取消订阅消息与嫁接和修剪消息是并行的。当一个对等体订阅一个主题时，它将挑选一些对等体成为该主题的全消息对等体，并在订阅消息的同时向它们发送嫁接消息。当一个对等体从一个主题退订时，它将在发送退订消息的同时通知其全消息对等体，他们的连接已被剪除。

## Sending messages

当一个对等体想要发布消息时，它会向它所连接的所有全消息对等体发送一个副本。同样，当一个对等体收到另一个对等体的新消息时，它存储该消息，并将其副本转发给它所连接的所有其他全消息对等体。

在 GossipSub 规范中，对等体也被称为路由器，因为它们具有在网络中路由消息的功能。对等体记住一个最近的消息列表。这让对等体只在第一次看到消息时采取行动，而忽略已经看到的消息的重传。

对等体也可以选择验证收到的每条消息的内容。什么是有效的和无效的取决于应用。例如，一个聊天应用程序可能会强制要求所有消息必须短于100个字符。如果应用程序告诉 libp2p 一条消息是无效的，那么这条消息就会被丢弃，不会通过网络进一步复制。

## Gossip

除了常规的 full-message 的对等点进行完整数据传输，还存在一个 `流言机制`。

`流言机制`指的是：对等体对他们最近看到的消息进行流言传播。每隔1秒，每个对等体随机选择6个metadata-only的对等体，并向他们发送最近看到的消息的列表。这里的消息称之为 IHAVE。如果 metadata-only 的对等体的消息列表里没收到过这个 full-message，那么它会向 IHAVE 发送方请求数据，这里的消息称之为 IWANT。这个机制可以防止某个对等体错过某个消息。

## Fan-out（扇形扩展连接）

peer 允许向它们没有订阅的主题发布消息。当一个 peer 第一次想向它没有订阅的主题发布消息时，它会随机挑选 6个订阅了该主题的peer，并将它们记为该主题的Fan-out peering。这是一种单向的连接，所以像电风扇一样，由一个 peer 向六个 peer 单方向的发送数据。

当该 peer 也订阅了这个主题，它会倾向于直接将 Fan-out peering 转换为 Full-message。

该 peer 两分钟没有通过 Fan-out peering 传输数据，Fan-out peering 自动中断。

## Network packets

![](https://docs.libp2p.io/concepts/publish-subscribe/network_packet_structure.png)

## State

- Subscriptions: 订阅主题
- Fan-out topics: 扇形扩展主题，未订阅但发送过信息的主题
- List of peers currently connected to: 当前连接的 peer 列表
- Recently seen messages: 最近看到的消息
