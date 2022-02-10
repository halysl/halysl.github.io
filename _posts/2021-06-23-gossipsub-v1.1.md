# gossipsub v1.1: Security extensions to improve on attack resilience and bootstrapping

[gossipsub v1.1: Security extensions to improve on attack resilience and bootstrapping](https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.1.md)

v1.1 是对 v1.0 的扩展，改善了引导和协议康攻击性，完全兼容 v1.0。

## 协议扩展

### 显式对等协定

现在的协议（GossipSub）支持节点操作间现式的对等协定。应用程序可以指定一个 peers 列表，保持连接并无条件地将消息传递给彼此，而不受对等点评分系统和其他防御措施的影响。对于每个显式 peer，路由器必须建立并维护一个连接。连接最初是在路由器启动时建立的，如果连接丢失，则定期检查连接和重新连接。建议的连接检查时间为5分钟。显式的对等点存在于网格（即 full-message 组成的网络）之外: 每个新的有效传入消息都被转发给直接的对等点，并且传入的 rpc 总是被它们接受。在显式对等点上进行 GRAFT 是错误的，应该用 PRUNE 记录并拒绝这种尝试。

### 修剪退避和对等交换

GossipSub 依赖环境中的 peer 发现，以便在感兴趣的话题中找到 peer。这给实现可扩展的 peer 发现服务带来了压力，该服务可以支持该协议。有了 Peer Exchange，该协议现在可以从一小部分节点启动，而不依赖外部的 peer 发现服务。对等体交换（PX）在因超额订阅而修剪网状结构时起作用。修剪的 peer 不是简单地告诉被修剪的 peer 离开，而是提供一组其他peer，被修剪的 peer 可以连接到这些 peer，以重建其网格。

此外，被修剪的 peer 和修剪的 peer 都会从对方那里增加一个退避期，在这个退避期内它们不会尝试重新嫁接。修剪 peer 和被修剪 peer 都将在后退期内立即修剪 GRAFT 并延长后退期。当一个 peer 试图过早地重新嫁接时，修剪 peer 可以对该行为进行行为惩罚，并通过P₇对 peer 进行惩罚。

建议退避期的持续时间为1分钟，同时建议交换的 peer 数量大于 D_hi，以便被修剪的 peer 能够可靠地形成一个完整的网状。为了正确地同步两个 peer，修剪的 peer 应该在 PRUNE 消息中包括回避期。peer 在试图再次嫁接之前，必须等待完整的退避期--再加上一些松弛，以考虑到在下一次清除退避期的心跳之前的偏移--否则，如果它过早地试图嫁接，就会有嫁接被拒绝和被惩罚的危险。

为了实现PX，我们扩展了PRUNE控制消息，以包括被修剪的 peer 可以连接的可选 peers 集合。这个 peers 集合包括peer ID 和每个交换的 peer 的签名对等体记录。为了促进过渡到 libp2p 生态系统中签名的对等体记录的使用，如果发射的 peer 没有签名的 peer 记录，允许它省略。在这种情况下，被修剪的 peer 将不得不依赖环境中的 peer 发现服务（如果设置了）来发现 peer 的地址。

```
message ControlPrune {
	optional string topicID = 1;
	repeated PeerInfo peers = 2; // gossipsub v1.1 PX
	optional uint64 backoff = 3; // gossipsub v1.1 backoff time (in seconds)
}

message PeerInfo {
	optional bytes peerID = 1;
	optional bytes signedPeerRecord = 2;
}
```

### Flood Publishing 

在 gossipsub v1.0 中，如果对等体订阅了他们要发布的主题，他们就会向其网状结构的成员发布新消息。对等体也可以向他们没有订阅的主题发布，在这种情况下，他们将从他们的扇形扩展图中选择对等体。

在 gossipsub v1.1 中，发布是通过向`所有分数高于``发布阈值`的连接对等体发布消息来完成的（可选）。无论发布者是否订阅了该主题，这都适用。在启用洪水发布的情况下，在传播来自其他对等体的消息时，会使用网状结构，但对等体自己的消息会一直发布给主题中的所有已知对等体。

这种行为是为了对抗日蚀攻击，并确保一个诚实节点新发布的消息会到达所有连接的诚实节点，并传到整个网络中。当使用洪流发布时，当对等体是一个没有订阅主题的纯发布者时，利用扇形扩展图或传播流言就没有意义了。

### Adaptive Gossip Dissemination

在 gossipsub v1.0 中，流言传播到一个固定数量的对等体，由 D_lazy 参数指定。在 gossipsub v1.1 中，流言的传播是自适应的；我们不是向固定数量的对等体传播流言，而是向最小 D_lazy 对等体的百分比传递流言。

控制流言传播的参数被称为流言因子。当一个节点想在心跳期间传播流言时，首先它选择所有对等体得分高于流言阈值的对等体。从这些对等体中，它随机选择具有最小 D_lazy 的流言因子对等体，并向选定的对等体传播流言。

流言因子的推荐值是 0.25，与每条消息 3 轮流言的默认值一起，确保每个对等体至少有 50% 的机会收到关于一条消息的流言。更具体地说，对于 3 轮流言，一个对等体没有收到关于一个新消息的流言的概率是（3/4）³=27/64=0.421875。因此，每个对等体以0.578125的概率收到关于一个新消息的流言。

这种行为是为了对抗女巫攻击而规定的，并确保来自诚实节点的信息以高概率在网络中传播。

### Outbound Mesh Quotas

在 gossipsub v1.0 中，网状对等体是随机选择的，没有对连接的方向给予任何权重。相比之下，gossipsub v1.1 实现了对外连接配额，因此一个对等体试图在网状结构中始终保持一定数量的外向连接。具体来说，我们定义了一个新的叠加参数  `d_out`，它必须设置在 `d_lo` 之下，最多设置为 `d/2`。

- 当对等体因为超额订阅而修剪时，路由在至少 D_out 个对等体是外向连接的约束下选择幸存的对等体。
- 当对等体在超额订阅时收到GRAFT（网状程度为 D_hi 或更高），如果它是一个出站连接，它只接受网状中的新对等体。
- 在心跳维护期间，如果对等体在网状中已经有至少 D_lo 对等体，但没有足够的出站连接，那么它就会选择尽可能多的需要的对等体来填补配额，并把它们移植到网状中。

这种行为被认为是为了对抗女巫攻击，并确保协调的入站攻击永远无法完全接管目标对等体的网状结构。

### Peer Scoring

在 gossipsub v1.1 中，我们引入了一个 peer 评分组件：每个单独的 peer 为其他 peer 保持一个分数。分数是由每个单独的 peer 根据观察到的行为在本地计算出来的，并不共享。分数是一个真实的值，作为参数的加权混合计算，具有可插拔的特定应用评分。分数是在所有（配置的）主题中以加权混合的方式计算的，这样，一个主题中的错误行为会渗透到其他主题中。此外，当一个 peer 断开连接时，分数会被保留一段时间，这样，当分数下降到负值时，恶意的 peer 就不能轻易重置他们的分数，而行为良好的 peer 不会因为断开连接而失去他们的状态。

这样做的目的是为了检测恶意或错误的行为，并以负分来惩罚行为不良的 peer。

### Score Thresholds

分数被插入各种流言算法中，这样一来，分数为负的对等体就被从网状结构中移除。如果分数降得太低，具有严重负分的对等体将被进一步惩罚，甚至被忽略。

- 0：基线阈值；得分低于该阈值的对等体在心跳期间被从网状结构中剪除，并在寻找对等体嫁接时被忽略。此外，不会向这些对等体发出任何PX信息，并且忽略它们的PX。此外，在执行PX时，只有具有非负分的对等体被交换。
- gossipThreshold：当一个对等体的分数下降到该阈值以下时，不会向该对等体发出八卦信息，并且忽略来自该对等体的八卦信息。这个阈值应该是负的，这样一些信息就可以传播给轻微负分的对等体。
- publishThreshold：当一个对等体的分数下降到这个阈值以下时，在（洪水）发布时，不会向这个对等体传播自己发布的信息。这个阈值应该是负的，并且小于或等于流言的阈值。
- graylistThreshold：当一个对等体的分数下降到这个阈值以下时，该对等体被列入灰名单，其RPC被忽略。这个阈值必须是负的，并且小于 gossip/publish 阈值。
- acceptPXThreshold：如果发起对等体的分数超过这个阈值，当它向我们发送带有修剪的PX信息时，我们只接受它并连接到所提供的对等体。这个阈值应该是非负值，为了提高安全性，只有引导者和其他受信任的连接良好的对等体才能达到一个大的正值。
- opportunisticGraftThreshold：当网状结构中的对等体得分低于这个值时，路由器可以选择更多得分高于中位数的对等体在网状结构中进行机会性嫁接（见下文的机会性嫁接）。这个阈值应该是正值，与通过话题贡献实现的分数相比，这个值相对较小。

#### Heartbeat Maintenance

分数在心跳维护期间被明确检查。

- 得分为负的对等体被从所有网格中修剪掉。即不再拥有 full-message peering，仅有 metadata-only peering。
- 当因为超额订阅而修剪时，对等体保留最好的 D_score 得分的对等体，并随机选择其余对等体来保留。这可以保护网格不受`接管攻击`，并确保最佳得分的对等体被保留在网格中。同时，我们确实保留了一些随机的对等体，这样协议就能对加入网状结构的新对等体做出反应。选择是在 D_out 对等体是出站连接的约束条件下进行的；如果评分加随机选择不能产生足够的出站连接，那么我们就用出站连接对等体替换选择中的随机和低分对等体。
- 在选择因订阅不足而要嫁接的对等体时，负分的对等体被忽略。

#### Opportunistic Grafting

It may be possible that the router gets stuck with a mesh of poorly performing peers, either due to churn of good peers or because of a successful large scale cold boot or covert flash attack. When this happens, the router will normally react through mesh failure penalties (see The Score Function below), but this reaction time may be slow: the peers selected to replace the negative scoring peers are selected at random among the non-negative scoring peers, which may result in multiple rounds of selections amongst a sybil poisoned pool. Furthermore, the population of sybils may be so large that the sticky mesh failure penalties completely decay before any good peers are selected, thus making sybils re-eligible for grafting.

In order to recover from such disaster scenarios and generally adaptively optimize the mesh over time, gossipsub v1.1 introduces an opportunistic grafting mechanism. Periodically, the router checks the median score of peers in the mesh against the opportunisticGraftThreshold. If the median score is below the threshold, the router opportunistically grafts (at least) two peers with score above the median in the mesh. This improves an underperforming mesh by introducing good scoring peers that may have been gossiping at us. This also allows the router to get out of sticky disaster situations by replacing sybils attempting an eclipse with peers which have actually forwarded messages through gossip recently.

The recommended period for opportunistic grafting is 1 minute, while the router should graft 2 peers (with the default parameters) so that it has the opportunity to become a conduit between them and establish a score in the mesh. Nonetheless, the number of peers that are opportunistically grafted is controlled by the application. It may be desirable to graft more peers if the application has configured a larger mesh than the default parameters.

#### The Score Function

The score function is a weighted mix of parameters, 4 of them per topic and 3 of them globally applicable.

```
Score(p) = TopicCap(Σtᵢ*(w₁(tᵢ)*P₁(tᵢ) + w₂(tᵢ)*P₂(tᵢ) + w₃(tᵢ)*P₃(tᵢ) + w₃b(tᵢ)*P₃b(tᵢ) + w₄(tᵢ)*P₄(tᵢ))) + w₅*P₅ + w₆*P₆ + w₇*P₇
```

其中 `tᵢ` 是主题本身的权重，由应用程序指定。 

- P₁: Time in Mesh。一个主题在Mesh中的时间。这是一个对等体在Mesh中的时间，上限为一个小值，并与一个小的正数权重混合。这是为了提高已经在网状结构中的对等体，这样他们就不会因为超额订阅而过早地被剪除。
- P₂: First Message Deliveries for a topic。一个主题的首次消息传递量。这是该主题中对等体首次传递的消息数量，与一个正的权重混合。这旨在奖励首先转发有效消息的对等体。
- P₃: Mesh Message Delivery Rate for a topic。一个主题的网状消息传递率。该参数是该主题中网状结构内预期消息传递率的阈值。如果交付数量高于阈值，则其值为0。如果数量低于阈值，则参数值为赤字的平方。这样做的目的是为了惩罚网状结构中没有交付预期数量信息的对等体，以便将其从网状结构中删除。该参数与负权重混合。
- P₃b。Mesh Message Delivery Failures for a topic。一个主题的网状信息传递失败率。这是一个粘性参数，计算网状消息传递失败的数量。每当一个对等体以负分修剪时，该参数就会被修剪时的比率赤字所增加。这样做的目的是为了保持修剪的历史，这样一个因为传递不足而被修剪的对等体就不能很快被重新嫁接到网格中。该参数与负权重混合。
- P₄:  Invalid Messages for a topic。一个主题的无效消息。这是在主题中交付的无效消息的数量。这是为了根据特定应用的验证规则，惩罚传送无效信息的对等体。它与一个负的权重混合。
- P₅: Application-Specific score。特定应用的得分。这是由应用程序本身使用特定的应用程序规则分配给对等体的分数成分。权重是正的，但参数本身有一个任意的实值，因此应用程序可以用负的分数发出错误行为的信号，或者在特定于应用程序的握手完成之前对对等体进行屏蔽。
- P₆: IP Colocation Factor。IP同位因子。该参数是使用同一IP地址的对等体数量的阈值。如果同一IP的对等体数量超过阈值，那么该值为盈余的平方，否则为0。这是为了使使用少量IP的对等体难以进行Sybil攻击。该参数与负权重混合。
- P₇: Behavioural Penalty。行为惩罚。该参数反映了对不当行为的惩罚。该参数有一个相关的（衰减的）计数器，由路由器在特定事件中明确增加。该参数的值是计数器的平方，并与负权重混合。
