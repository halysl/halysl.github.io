# 基于 Prometheus 的监控体系设计

1. 数据整合中心
2. 数据采集器
3. 半自动化的target配置
4. 网络隔离问题
5. 告警实现
6. 展示实现
7. 监控整体部署
8. 业务监控接入

## 1. 数据整合中心

采用 Prometheus 作为数据整合中心，它具有：

- 强大的扩展性
- 极简的设计，仅需要几个配置文件和单个二进制程序就可以运行
- 运行速度快，底层使用 tsdb 进行存储，默认存储15天
- 采用 Pull 的模式进行数据整合，需要网络的畅通
- 中心化的配置管理
- 支持各种服务发现，常用的为：file_sd、consul_sd
- 支持 API 管理，也支持 Web 页面的管理
- labels 支持，方便对监控主体的描述

可使用 systemd 进行托管。

- [Prometheus.io](https://prometheus.io/)
- [Github/Prometheus](https://github.com/prometheus)

## 2. 数据采集器

- node_exporter：Linux 平台的物理信息采集，默认开启 42 大项监控，默认关闭 21 大项监控。自带 text collector 功能，允许用户自己书写脚本采集数据。[node_exporter](https://github.com/prometheus/node_exporter)
- blackbox_exporter：用于网络黑盒测试的采集器，特别的仅需要部署一个程序而不需要在每个节点都部署。可以用于 web 服务、http 服务、ssh 服务状态的检测。[black_exporter](https://github.com/prometheus/blackbox_exporter)
- mysqld_exporter：用于监控 MySQL 服务各种指标。[mysqld_exporter](https://github.com/prometheus/mysqld_exporter)
- nvidia_gpu_prometheus_exporter：基于 NVML 库，用于监控 GPU 运行状态。 [nvidia_gpu_prometheus_exporter](https://github.com/mindprince/nvidia_gpu_prometheus_exporter)
- cAdvisor：用于监控 docker 容器资源消耗等信息。[cadvisor](https://github.com/google/cadvisor)

以上采集器都是单个二进制程序运行，基本不需要配置文件，启动后都需要占据一个端口。如果实际场景只允许单个端口，那么需要做个整合。

## 3. 半自动化的 target 配置

target 在 prometheus 里面指的是监控主体，是一个复杂的混合概念，例如：

- 监控主机硬件资源占用：`ip:9100`
- 监控主机显卡状态登陆：`ip:9445`
- 监控主机容器信息：`ip:8080`

简单的说，可以理解为 target 就是 ip+端口。举个 btfs 的例子，单个物理机器使用 docker 启动了 100 个 btfs 实例，分配的端口为：50001-50100，想要获得每一个实例的状态（主要是业务信息），就对应 100 个端口：ip:50001-ip:50100。

nash 的业务环境比较复杂，从物理机器的视角来看，可能会同时运行多个业务，也有可能撤下某些业务上新的业务，这一章节想要做的事就是在业务手动分配完成后也能实现监控的切换。

对于物理机器上的监控，node_exporter、nvidia_gpu_prometheus_exporter、cAdvisor 等服务其实一次配置就可以了，基本不会随着业务变化而变化，这里可以使用 consul 的 service discover 进行管理，但这要求预先部署服务（比如container/VM里默认就运行监控服务）。（注意：监控的部署，包括业务脚本的部署是另外一回事，这里专注的是如何修改监控配置。）

对于业务需要的数据，首先是可能存在时间差，比如业务调配机器时，该业务需要监控什么内容都不清楚，监控的 target 都不明确就很难做到自动化。如果只是打个标签，某台机器开始用于什么业务，要用到 file_sd_discover。

举个例子，上架了一些机器用于 A 和 B 业务，通过 API 告知某个程序（这个程序可能还不存在），然后通过修改 target 配置文件进行变动，如果这个机器并没有配置监控程序，那么就可以在中心看到异常。

或者二开 prometheus，让其从数据库中获取 target 信息。

常见的基于 file_sd 的服务发现。

-   [Kuma](https://github.com/kumahq/kuma/tree/master/app/kuma-prometheus-sd)
-   [Lightsail](https://github.com/n888/prometheus-lightsail-sd)
-   [Netbox](https://github.com/FlxPeters/netbox-prometheus-sd)
-   [Packet](https://github.com/packethost/prometheus-packet-sd)
-   [Scaleway](https://github.com/scaleway/prometheus-scw-sd)


## 4. 网络隔离问题

网络隔离问题，一是出现在 Prometheus 的 Pull 数据问题上，二是出现在 consul 的服务发现上，后者可以不考虑。

Prometheus push gateway 这个组件并不可以 push 数据，而是可以接受 push 过来的数据，先看架构图。

![prometheus架构图](https://prometheus.io/assets/architecture.png)

可以看到 pushgateway 主要是用来接受一些“非长期任务”给出的数据。比如说某个任务，很快就可以完成，如果使用 Pull 模式，定期拉取，发现没有数据（因为任务都结束了），这种情况就可以把数据推送到 pushgateway 上，然后 Prometheus 会定期的 Pull 到 pushgateway 的数据。不推荐这种模式解决网络隔离的问题。

这里先给出两个方案：

- 类似堡垒机，监控节点可以无感接入所有机器
- 对于每个子网，设置独立的 Prometheus，告警信息和展示信息是可以在上层实现

第二种方案属于顾头不顾尾，可以解决网络隔离问题，但是第三节的半自动化的 target 配置又会很麻烦。

## 5. 告警实现

默认使用 alertmanager 组件。Prometheus 通过 PromQL 进行告警信息的发现，然后通过等待期等操作发送给 alertmanager。

alertmanager 根据接收到的告警信息，走自己的路由树，确定要从哪个途径发送给哪些人。

常见的短信、邮箱、webhook等方式均支持。

## 6. 展示实现

直接使用 Grafana。对于主机信息直接套模版，对于业务需要的展板，根据需求进行编写。

## 7. 监控整体部署

几个要求：

- 端口强制定义
- systemd 托管
- 指定特殊用户
- 统一在同样的路径，包括程序和数据

具体的部署不在细谈，都好说。

## 8. 业务监控接入

不同的业务需要不同的监控数据，一般分两种：

- 业务程序直接暴露 metrics 接口
- 需要执行业务的 cli 获得数据

对于第一种方式，直接作为 target 加入 prometheus 即可。

对于第二种方式，也可以分两种情况，如果量比较少，那么通过 node_exporter 的 text collector 实现，用户需要自己编写脚本，按照一定格式写入到指定位置，建议加入采集数据时的时间戳；如果量比较多，而项目方又不提供 metrics，那么推荐直接写个 exporter，作为 target 加入 prometheus。

对于区块链项目，除了节点自身的状态需要监控，链上数据也需要监控的，这里只能根据实际情况进行处理。
