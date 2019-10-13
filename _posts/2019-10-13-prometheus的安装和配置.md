---
layout: post
title: prometheus 的安装和配置
categories: [prometheus]
description: prometheus 的安装和配置
keywords: prometheus
---

# prometheus 的安装和配置

Prometheus 是一个开放性的监控解决方案，用户可以非常方便的安装和使用 Prometheus 并且能够非常方便的对其进行扩展。为了能够更加直观的了解 Prometheus Server，接下来我们将在本地部署并运行一个 Prometheus Server实例，通过 Node Exporter 采集当前主机的系统资源使用情况。 并通过 Grafana 创建一个简单的可视化仪表盘。

Prometheus 基于 Golang 编写，编译后的软件包，不依赖于任何的第三方依赖。用户只需要下载对应平台的二进制包，解压并且添加基本的配置即可正常启动 Prometheus Server。具体安装过程可以参考如下内容。

以 Centos7 为系统环境。

## 部署 prometheus

- 安装 prometheus

```shell
wget  https://github.com/prometheus/prometheus/releases/download/v2.9.2/prometheus-2.9.2.linux-amd64.tar.gz
tar xzvf prometheus-2.9.2.linux-amd64.tar.gz
mv prometheus-2.9.2.linux-amd64 /usr/local/prometheus
```

- 添加 prometheus 用户，非必须

```shell
groupadd prometheus
useradd -g prometheus -m -d /var/lib/prometheus -s /sbin/nologin prometheus
```

- prometheus 系统服务配置

```shell
vim /etc/systemd/system/prometheus.service

[Unit]
Description=prometheus
After=network.target
[Service]
Type=simple
User=prometheus
ExecStart=/usr/local/prometheus/prometheus -config.file=/usr/local/prometheus/prometheus.yml -storage.local.path=/var/lib/prometheus
Restart=on-failure
[Install]
WantedBy=multi-user.target
```

- 启动 prometheus

```shell
systemctl start prometheus
systemctl status prometheus
```

## 部署 node_exporter

安装在将要监控的主机上。

- 安装 node_exporter

```shell
wget https://github.com/prometheus/node_exporter/releases/download/v0.18.0/node_exporter-0.18.0.linux-amd64.tar.gz
tar -zxvf node_exporter-0.18.0.linux-amd64.tar.gz
mv node_exporter-0.18.0.linux-amd64 /usr/local/node_exporter
```

- 系统服务配置 node_exporter

```shell
vim /etc/systemd/system/node_exporter.service

[Unit]
Description=node_exporter
After=network.target
[Service]
Type=simple
User=prometheus
ExecStart=/usr/local/node_exporter/node_exporter
Restart=on-failure
[Install]
WantedBy=multi-user.target
```

- 启动 node_exporter

```shell
systemctl start node_exporter
systemctl status node_exporter
```

- 回到安装有 prometheus 的机器上，将 node_exporter 相关信息填写到 prometheus.yaml

```shell
vim  /usr/local/prometheus/prometheus.yml

  - job_name: 'linux'
    static_configs:
      - targets: ['localhost:9100']
        labels:
          instance: node1
```

- 重启 prometheus

```shell
systemctl restart prometheus
systemctl status prometheus
```

## 部署 grafana

- 安装 grafana

```shell
wget https://dl.grafana.com/oss/release/grafana-6.1.6-1.x86_64.rpm 
yum localinstall grafana-6.1.6-1.x86_64.rpm
```

- 启动 grafana-server

```shell
systemctl start grafana-server
systemctl status grafana-server
```
