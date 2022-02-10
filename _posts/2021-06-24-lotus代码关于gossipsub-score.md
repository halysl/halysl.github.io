# lotus代码关于gossipsub-score

需要专注于：业务中哪些地方会用到这个评分？哪些地方会影响到这些评分？

## 得分说明

```
Score(p) = TopicCap(Σtᵢ*(w₁(tᵢ)*P₁(tᵢ) + w₂(tᵢ)*P₂(tᵢ) + w₃(tᵢ)*P₃(tᵢ) + w₃b(tᵢ)*P₃b(tᵢ) + w₄(tᵢ)*P₄(tᵢ))) + w₅*P₅ + w₆*P₆ + w₇*P₇
```

其中 `tᵢ` 是主题本身的权重，由应用程序指定。 

- P₁: Time in Mesh。一个主题在Mesh中的时间。这是一个对等体在Mesh中的时间，上限为一个小值，并与一个小的正数权重混合。这是为了提高已经在网状结构中的对等体，这样他们就不会因为超额订阅而过早地被剪除。
- P₂: First Message Deliveries for a topic。一个主题的首次消息传递量。这是该主题中对等体首次传递的消息数量，与一个正的权重混合。这旨在奖励首先转发有效消息的对等体。
- P₃: Mesh Message Delivery Rate for a topic。一个主题的网状消息传递率。该参数是该主题中网状结构内预期消息传递率的阈值。如果交付数量高于阈值，则其值为0。如果数量低于阈值，则参数值为赤字的平方。这样做的目的是为了惩罚网状结构中没有交付预期数量信息的对等体，以便将其从网状结构中删除。该参数与负权重混合。
- P₃b。Mesh Message Delivery Failures for a topic。一个主题的网状信息传递失败率。这是一个粘性参数，计算网状消息传递失败的数量。每当一个对等体以负分修剪时，该参数就会被修剪时的比率赤字所增加。这样做的目的是为了保持修剪的历史，这样一个因为传递不足而被修剪的对等体就不能很快被重新嫁接到网格中。该参数与负权重混合。
- P₄:  Invalid Messages for a topic。一个主题的无效消息。这是在主题中交付的无效消息的数量。这是为了根据特定应用的验证规则，惩罚传送无效信息的对等体。它与一个负的权重混合。

上面四个是针对 topic 的，下面三个是属于程序定义的。

- P₅: Application-Specific score。特定应用的得分。这是由应用程序本身使用特定的应用程序规则分配给对等体的分数成分。权重是正的，但参数本身有一个任意的实值，因此应用程序可以用负的分数发出错误行为的信号，或者在特定于应用程序的握手完成之前对对等体进行屏蔽。
- P₆: IP Colocation Factor。IP同位因子。该参数是使用同一IP地址的对等体数量的阈值。如果同一IP的对等体数量超过阈值，那么该值为盈余的平方，否则为0。这是为了使使用少量IP的对等体难以进行Sybil攻击。该参数与负权重混合。
- P₇: Behavioural Penalty。行为惩罚。该参数反映了对不当行为的惩罚。该参数有一个相关的（衰减的）计数器，由路由器在特定事件中明确增加。该参数的值是计数器的平方，并与负权重混合。


## GossipSub 基础属性配置

```
# 非引导节点
    # 每个peer自身的网状结构至少有的数量，对于一个peer，至少保持有8个full-message peering
    pubsub.GossipSubD = 8
	# peer进行修剪时必须保证6个对等点是高分的
	pubsub.GossipSubDscore = 6
	# peer修剪时保证3个对外连接，防止日蚀攻击，一般小于GossipSubDlo，且小于GossipSubD/2
	pubsub.GossipSubDout = 3
	# peer自身的网络的对等体下限和上限，如果缺少/超过，则在下次心跳中进行嫁接/修剪
	pubsub.GossipSubDlo = 6
	pubsub.GossipSubDhi = 12
	# peer要向12个对等体传递流言
	pubsub.GossipSubDlazy = 12
	# peer直接连接对等体前的初始延迟，可以理解为手动配置peer
	pubsub.GossipSubDirectConnectInitialDelay = 30 * time.Second
	# 在 IHAVE 广播之后，等待通过 IWANT 请求的消息的时间。如果在这个窗口内消息没被peer接收到，就会宣布该peer违背承诺，路由器可能会对其进行行为处罚。
	pubsub.GossipSubIWantFollowupTime = 5 * time.Second
	# 窗口数，消息缓存的量
	pubsub.GossipSubHistoryLength = 10
	# 流言传播的动态因子，按照一个消息会被IHAVE发送三轮，那么 1-0.9*0.9*0.9 =0.27，peer大致27%的概率获得新消息
	pubsub.GossipSubGossipFactor = 0.1
```

相比于 GossipSub 的默认设置，Lotus的网络做了更严格的要求，可以从GossipSubD和GossipSubDscore看出，这主要是为了提升消息的传递效率。

```
# GossipSub 相关阈值
&pubsub.PeerScoreThresholds{
				GossipThreshold:             -500,
				PublishThreshold:            -1000,
				GraylistThreshold:           -2500,
				AcceptPXThreshold:           1000,
				OpportunisticGraftThreshold: 3.5,
			},
```

## Lotus Topic 配置（得分相关）

Lotus 三个 Topic，drand、block、message，三者因为特性不一致，所以topic设置不太一致。

```
drandTopicParams := &pubsub.TopicScoreParams{
		// expected 2 beaconsn/min
		// 5倍于常规topic的权重，意味着对peer来说，该topic下的消息比较重要，至于极限值还不知道怎么算
		TopicWeight: 0.5, // 5x block topic; max cap is 62.5

        // peer在网络内的时间的权重，最上方公式的 P1
		// 1 tick per second, maxes at 1 after 1 hour
		TimeInMeshWeight:  0.00027, // ~1/3600
		TimeInMeshQuantum: time.Second,
		TimeInMeshCap:     1,

        // peer在网络内第一个传递消息的权重，也就是最上方公式的P2
		// deliveries decay after 1 hour, cap at 25 beacons
		FirstMessageDeliveriesWeight: 5, // max value is 125
		// 衰减指数，计算公式是：math.Pow(decayToZero, 1/(float64(decay / base)))一般 decayToZero为0.01，base为1 time.Second，下面不再赘述
		// 在这里大概是 0.9987216039048303
		FirstMessageDeliveriesDecay:  pubsub.ScoreParameterDecay(time.Hour),
		FirstMessageDeliveriesCap:    25, // the maximum expected in an hour is ~26, including the decay

        // 没有启用网络传输失败的设定，主要原因是数据少。也就是上方公式的P3。
		// Mesh Delivery Failure is currently turned off for beacons
		// This is on purpose as
		// - the traffic is very low for meaningful distribution of incoming edges.
		// - the reaction time needs to be very slow -- in the order of 10 min at least
		//   so we might as well let opportunistic grafting repair the mesh on its own
		//   pace.
		// - the network is too small, so large asymmetries can be expected between mesh
		//   edges.
		// We should revisit this once the network grows.

        // 非法的消息会惩罚1000分。也就是上方公式的P4。
		// invalid messages decay after 1 hour
		InvalidMessageDeliveriesWeight: -1000,
		InvalidMessageDeliveriesDecay:  pubsub.ScoreParameterDecay(time.Hour),
	}

	topicParams := map[string]*pubsub.TopicScoreParams{
		build.BlocksTopic(in.Nn): {
			// expected 10 blocks/min
			// topic权重为0.1，网络超过最大连接数会扣10分，选出非法的消息扣100分
			TopicWeight: 0.1, // max cap is 50, max mesh penalty is -10, single invalid message is -100

			// 1 tick per second, maxes at 1 after 1 hour
			TimeInMeshWeight:  0.00027, // ~1/3600
			TimeInMeshQuantum: time.Second,
			TimeInMeshCap:     1,

			// deliveries decay after 1 hour, cap at 100 blocks
			FirstMessageDeliveriesWeight: 5, // max value is 500
			// 大约 0.9987216039048303
			FirstMessageDeliveriesDecay:  pubsub.ScoreParameterDecay(time.Hour),
			FirstMessageDeliveriesCap:    100, // 100 blocks in an hour

            // 同理没有启用网络传输失败
			// Mesh Delivery Failure is currently turned off for blocks
			// This is on purpose as
			// - the traffic is very low for meaningful distribution of incoming edges.
			// - the reaction time needs to be very slow -- in the order of 10 min at least
			//   so we might as well let opportunistic grafting repair the mesh on its own
			//   pace.
			// - the network is too small, so large asymmetries can be expected between mesh
			//   edges.
			// We should revisit this once the network grows.
			//
			// // tracks deliveries in the last minute
			// // penalty activates at 1 minute and expects ~0.4 blocks
			// MeshMessageDeliveriesWeight:     -576, // max penalty is -100
			// MeshMessageDeliveriesDecay:      pubsub.ScoreParameterDecay(time.Minute),
			// MeshMessageDeliveriesCap:        10,      // 10 blocks in a minute
			// MeshMessageDeliveriesThreshold:  0.41666, // 10/12/2 blocks/min
			// MeshMessageDeliveriesWindow:     10 * time.Millisecond,
			// MeshMessageDeliveriesActivation: time.Minute,
			//
			// // decays after 15 min
			// MeshFailurePenaltyWeight: -576,
			// MeshFailurePenaltyDecay:  pubsub.ScoreParameterDecay(15 * time.Minute),

            // 非法的消息会惩罚1000分。也就是上方公式的P4。
			// invalid messages decay after 1 hour
			InvalidMessageDeliveriesWeight: -1000,
			InvalidMessageDeliveriesDecay:  pubsub.ScoreParameterDecay(time.Hour),
		},
		build.MessagesTopic(in.Nn): {
			// expected > 1 tx/second
			// topic权重为0.1，选出非法的消息扣100分
			TopicWeight: 0.1, // max cap is 5, single invalid message is -100

			// 1 tick per second, maxes at 1 hour
			TimeInMeshWeight:  0.0002778, // ~1/3600
			TimeInMeshQuantum: time.Second,
			TimeInMeshCap:     1,

			// deliveries decay after 10min, cap at 100 tx
			FirstMessageDeliveriesWeight: 0.5, // max value is 50
			FirstMessageDeliveriesDecay:  pubsub.ScoreParameterDecay(10 * time.Minute),
			FirstMessageDeliveriesCap:    100, // 100 messages in 10 minutes

			// Mesh Delivery Failure is currently turned off for messages
			// This is on purpose as the network is still too small, which results in
			// asymmetries and potential unmeshing from negative scores.
			// // tracks deliveries in the last minute
			// // penalty activates at 1 min and expects 2.5 txs
			// MeshMessageDeliveriesWeight:     -16, // max penalty is -100
			// MeshMessageDeliveriesDecay:      pubsub.ScoreParameterDecay(time.Minute),
			// MeshMessageDeliveriesCap:        100, // 100 txs in a minute
			// MeshMessageDeliveriesThreshold:  2.5, // 60/12/2 txs/minute
			// MeshMessageDeliveriesWindow:     10 * time.Millisecond,
			// MeshMessageDeliveriesActivation: time.Minute,

			// // decays after 5min
			// MeshFailurePenaltyWeight: -16,
			// MeshFailurePenaltyDecay:  pubsub.ScoreParameterDecay(5 * time.Minute),

			// invalid messages decay after 1 hour
			InvalidMessageDeliveriesWeight: -1000,
			InvalidMessageDeliveriesDecay:  pubsub.ScoreParameterDecay(time.Hour),
		},
	}
```

|topic name|topic weight|P1|P2|P3|P4|
|----------|------------|---|---|---|---|
|drand|0.5|0.00027;max 1|5;max 125|0|-1000|
|block|0.1|0.00027;max 1|5;max 500|0|-1000|
|message|0.1|0.00027;max 1|0.5;max 50|0|-1000|

## 得分通用参数

```
// 如果是 BootstrapNode 或者 drandBootstrappers，那么获得高分，这有利于应用peer在修剪时保留这些peer
// 也就是公式的 P5
AppSpecificScore: func(p peer.ID) float64 {
	// return a heavy positive score for bootstrappers so that we don't unilaterally prune
	// them and accept PX from them.
	// we don't do that in the bootstrappers themselves to avoid creating a closed mesh
	// between them (however we might want to consider doing just that)
	_, ok := bootstrappers[p]
	if ok && !isBootstrapNode {
		return 2500
	}

	_, ok = drandBootstrappers[p]
	if ok && !isBootstrapNode {
		return 1500
	}

	// TODO: we want to  plug the application specific score to the node itself in order
	//       to provide feedback to the pubsub system based on observed behaviour
	return 0
},
AppSpecificWeight: 1,

// 使用 IP 主机托管超过5个会进行惩罚.公式的 P6
// This sets the IP colocation threshold to 5 peers before we apply penalties
IPColocationFactorThreshold: 5,
IPColocationFactorWeight:    -100,
IPColocationFactorWhitelist: ipcoloWhitelist,

// 行为惩罚。公式的P7
// P7: behavioural penalties, decay after 1hr
BehaviourPenaltyThreshold: 6,
BehaviourPenaltyWeight:    -10,
BehaviourPenaltyDecay:     pubsub.ScoreParameterDecay(time.Hour),
```

## Trace

所有的分数计算都是在 go-libp2p-pubsub 中进行（准确说是 score.go）。而 lotus 这边只负责给定参数启动一个 p2p 网络，在程序运行时，通过 Trace 进行相关参数的变动。按照上面提到的打分规则，对于 topic 来说，有四个相关参数：

- Time in Mesh
- First Message Deliveries for a topic
- Mesh Message Delivery Rate for a topic
- Mesh Message Delivery Failures for a topic（基本没启用）
- Invalid Messages for a topic

这个评分仅仅是当前 peer 认为的网络情况。按照上述常用的四项参数，在 GossipSub 的 peer 待在 full-message 的时间越长，这个值越高；最先拿到消息的peer可以得分；传递消息快的可以拿分；传递非法消息的需要扣分。

`lotus net scores` 指的是从 lotus 启动到现在所有连接过的 peer 的分数，所以数量是一直增加的。

`lotus net peers` 指的是当前 lotus 存在的连接，取得8个作为自己的 full-message， 其他的 peer 都是 metadata-only。

由于 p2p 的理想化，只要保证网络的稳定性，这个分数就不会很低，只要大于 -500 分，就可以得到消息。归根结底还是要回归到网络状态本身。

理论上可以通过手动重启lotus的方式重新选择 peers，也可以通过 `lotus net connect` 手动选择高分数的节点，这样可以保证对端节点的稳定性好，传播效率高。

```
tips: 主要实现代码
- lotus/node/modules/lp2p/pubsub.go
- ~/go/pkg/mod/github.com/libp2p/go-libp2p-pubsub@v0.4.2-0.20210212194758-6c1addf493eb/score.go
- ~/go/pkg/mod/github.com/libp2p/go-libp2p-pubsub@v0.4.2-0.20210212194758-6c1addf493eb/gossipsub.go
```