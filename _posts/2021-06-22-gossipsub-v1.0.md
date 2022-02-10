# gossipsub v1.0: An extensible baseline pubsub protocol

[gossipsub v1.0: An extensible baseline pubsub protocol](https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.0.md)

## In the beginning was floodsub

在 GossipSub 实现前，使用的是 floodSub。它的传播策略非常简单，洪泛淹没。每个 peer 直接向特定主题的每个 peer 传递完整数据。

优势：

- 直接实现
- 数据延迟低
- 稳定，需要维护的状态少

劣势：

- 没有边界
- 带宽需求高
- 大量 peer 扩展成本高

## gossipsub: The gossiping mesh router

流言网状路由。几个关键点的解释：

- 流言：同一个主题内，有部分peer知道完整的信息，同时peer会向其他peer发送IHAVE信息，就像是流言蜚语一样，其他接收到的peer如果一直没听到流言，可以反过去询问消息（发送IWANT信息）。最后整个主题下的 peer 都知道该完整信息，但传递的过程进行了简化，peer 不会听到太多重复的流言。
- 网状：对于单个 peer 来说，它与其他的 peer 的连接形成了一张网
- 路由：每个 peer 在节点中的功能相对复杂了很多，同时需要实现路由的功能（选择传递完整信息给哪些peer）

## Parameters

GossipSub 可配置参数。

|参数|用途|默认值|
|----|----|----|
|D|网络期待传播度|6|
|D_low|网络传播度下限|4|
|D_high|网络传播度上限|12|
|D_lazy|（可选）流言传播度|D|
|heartbeat_interval|心跳间隔|1 second|
|fanout_ttl|fan-out生存周期|60 seconds|
|mcache_len|消息缓存中历史窗口的数量|5|
|mcache_gossip|发出流言时使用的历史窗口数|3|
|seen_ttl|缓存所见消息ID的过期时间|2 minutes|

## Router State

- peering stat
- state related to the message cache

### peering stat

- peers：一组所有支持 gossipsub 或 floodsub 的已知 peer 的 id
- mesh：一个订阅的主题与该主题的覆盖网中的 peer 集合的映射
- fanout：与mesh类似，但映射包含我们没有订阅的话题

### Message Cache

消息缓存（或称mcache）是一个数据结构，用于存储消息ID和其相应的消息，被分割成 "历史窗口"。每个窗口对应一个心跳间隔（heartbeat_interval），窗口在流言传播后的心跳过程中被移位。历史窗口的数量由 mcache_len 参数决定，而传播流言时检查的窗口数量则由 mcache_gossip 控制。

消息缓存支持以下操作。

- mcache.put(m): 添加一条消息到当前窗口和缓存中
- mcache.get(id): 通过ID从缓存中检索一条消息，如果它所在的窗口还没过期
- mcache.get_gossip_ids(topic): 检索最近的历史窗口中的信息ID，范围是给定的主题。检查的窗口数量由 mcache_gossip 参数控制
- mcache.shift(): 转移当前窗口，丢弃比缓存的历史长度（mcache_len）更早的消息。

除了消息缓存外，还有一个 `看到的哦缓存（seen cache）`。这是一个定时的`最少最近`使用的消息ID的缓存，是我们最近观察到的。”最近“ 的是由参数 seed_ttl 决定的，默认值是两分钟。这个值应该在接近覆盖层中的传播延迟。

seen cache 有两个好处：

- 转发消息前，查看seen cache，避免重复发送消息
- 在 GossipSub 中，处理 IHAVE 消息时，可以查看 seen cache，再发送对应的 IWANT 消息请求消息

## Topic Membership

四种消息。

- SUBSCRIBE
- UNSUBSCRIBE
- JOIN
- LEAVE

前两个消息主体是 peer，需要在主题已经存在的情况下进行订阅/取消订阅。那么主题该如何出现？

主题成员的加入/离开是由应用程序控制的。

当应用程序调用 JOIN(topic) 时，路由器将通过从其本地对等状态中选择多达 D（可配置） 个 peer，首先检查扇形扩展图来形成一个主题网。如果有 peer 在 `fanout[topic]` 中，路由器将把这些 peer 从 fanout 地图中移到 `mesh[topic]` 中。如果主题不在扇形扩展图中，或者 `fanout[topic]` 中的 peer 数量少于 D，路由器将尝试用 `peers.gossipsub[topic]` 中的 peer 填充 `mesh[topic]`。

无论 peers 是来自 fanout 还是 peers.gossipsub，路由器都会通过向他们发送 GRAFT 控制消息来通知 `mesh[topic]` 的新成员，peers 已经被加入到 mesh 中。

应用程序可以调用 LEAVE(topic) 来退订某个主题。路由器会通过发送 PRUNE 控制消息通知 `mesh[topic]` 中的peer，这样他们就可以从自己的话题网中删除链接。在发送 PRUNE 消息后，路由器将忘记 `mesh[topic]`，并将其从本地状态中删除。

## Control Messages

- GRAFT：嫁接，metadata-only convert to full-message
- PRUNE：修剪，full-message convert to metadata-only
- IHAVE：流言传播，告知其他 peer 有什么新消息
- IWANT：流言请求，某个 peer 发现自己没有流言的完整消息，就向发送 IHAVE 的 peer 请求数据

## Message Processing

收到消息后，peer 将处理消息payload（实际数据信息）。payload 处理包括三步：根据应用定义的规则验证消息、检查自身的 seen cache 是否存在该消息、确认自己是不是消息的来源。

如果消息是有效的，同时也不是该 peer 发布的，也并不存在于 seen cahce，那么该 peer 将转发该消息。首先，它将把消息转发到 `peers.floodsub[topic]` 中的每个 peer，以便向后兼容 floodsub。接下来，它将把消息转发到其本地 `gossipsub` `mesh[topic]` 中的每个 peer。

在处理完消息的 payload 后，peer 将处理控制消息。在收到 `GRAFT(topic)` 消息时，peer 将检查它是否确实订阅了该消息中确定的话题。如果是，peer 将把发件人添加到 `mesh[topic]`。如果 peer 不再订阅该主题，它将回应一个 `PRUNE(topic)` 消息，通知发件人它应该删除其网状链接。

在收到 `PRUNE(topic)` 消息时，peer 将从 `mesh[topic]` 中删除发件人。

在收到 `IHAVE(ids)` 消息时，peer 将检查其看到的缓存(包括 message cache 和 seen cache)。如果 IHAVE 消息中包含未被看到的消息 ID，peer 将用 IWANT 消息请求它们。

在收到 `IWANT(ids)` 消息时，peer 将检查其缓存，并将任何请求的消息转发到存在于缓存中的peer，即发送 IWANT 消息的人。

除了转发收到的消息，peer 当然也可以以自己的名义发布消息，这些消息来自于应用层。这与转发收到的消息非常相似。首先，消息被发送到 `peers.floodsub[topic]` 中的每个 peer。如果 peer 订阅了该主题，它将把消息发送给 `mesh[topic]` 中的所有 peer。如果 peer 没有订阅该主题，它将检查 `fanout[topic]` 中的 peer 集合。如果这个集合是空的，路由器将从 `peers.gossipsub[topic]` 中最多选择D个 peer，并将它们加入 `fanout[topic]`。

## Heartbeat

每个 peer 以固定的时间间隔运行一个称为 "心跳程序 "的定期稳定过程。心跳的频率由参数 heartbeat_interval 控制，合理的默认值是1秒。

心跳有三个功能：网状维护、扇形扩展维护和流言传播。

### Mesh Maintenance

```
for each topic in mesh:
 if |mesh[topic]| < D_low:
   select D - |mesh[topic]| peers from peers.gossipsub[topic] - mesh[topic]
    ; i.e. not including those peers that are already in the topic mesh.
   for each new peer:
     add peer to mesh[topic]
     emit GRAFT(topic) control message to peer

 if |mesh[topic]| > D_high:
   select |mesh[topic]| - D peers from mesh[topic]
   for each new peer:
     remove peer from mesh[topic]
     emit PRUNE(topic) control message to peer
```

- D: 网络期待传播度
- D_low: 网络期待传播度下限。如果 `mesh[topic]` 小于这个值，会转化 metadata-only 为 full-message，发送嫁接信息
- D_high: 网络期待传播度上限. 如果 `mesh[topic]` 小于这个值，会随机选择 peer 转化 full-message 为 metadata-only ，发送修剪信息

### Fanout Maintenance

```
for each topic in fanout:
  if time since last published > fanout_ttl
    remove topic from fanout
  else if |fanout[topic]| < D
    select D - |fanout[topic]| peers from peers.gossipsub[topic] - fanout[topic]
    add the peers to fanout[topic]
```

- D: 网络期待传播度
- fanout_ttl: 我们为每个主题保留 fanout 状态的时间。如果我们在 fanout_ttl 内没有向某个主题发布，`fanout[topic]` 就会被丢弃

### Gossip Emission

```
for each topic in mesh+fanout:
  let mids be mcache.get_gossip_ids(topic)
  if mids is not empty:
    select D peers from peers.gossipsub[topic]
    for each peer not in mesh[topic] or fanout[topic]
      emit IHAVE(mids)

shift the mcache
```

在一般情况下，流言的传播度和消息的传播度一样，这并不规范。可以使用独立的参数 `D_lazy` 来指定流言的传播度。

## Protobuf

```
message RPC {
    // ... see definition in pubsub interface spec
	optional ControlMessage control = 3;
}

message ControlMessage {
	repeated ControlIHave ihave = 1;
	repeated ControlIWant iwant = 2;
	repeated ControlGraft graft = 3;
	repeated ControlPrune prune = 4;
}

message ControlIHave {
	optional string topicID = 1;
	repeated bytes messageIDs = 2;
}

message ControlIWant {
	repeated bytes messageIDs = 1;
}

message ControlGraft {
	optional string topicID = 1;
}

message ControlPrune {
	optional string topicID = 1;
}
```
