---
layout: post
title: grafana-backup的使用
categories: [Linux, 监控]
description:
keywords: 
---

# grafana-backup的使用

这个工具依赖于 grafana api 实现数据的备份和恢复，和服务具体的部署无关，仅需要接口地址和 token。（如果需要备份组织和用户则需要配置admin的账号密码）。

## 安装

两种方式：

- 直接安装 `pip install grafana-backup`
- 源码安装

```
git clone https://github.com/ysde/grafana-backup-tool.git
cd grafana-backup-tool
pip install .
```

### tip：centos7 安装pip以及换源

```
yum -y install epel-release
yum install python-pip
pip install --upgrade pip
```

```
mkdir ~/.pip
echo '[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple' > ~/.pip/pip.conf
```

## 备份

备份和恢复都需要依赖配置文件，这个工具支持三种方式：

- 环境变量
- 配置硬编码
- ~/.grafana-backup.json 配置

推荐使用第三种方式。

一个简易的配置类似于：

```
{
  "general": {
    "debug": true,
    "verify_ssl": true,
    "backup_dir": "_OUTPUT_",
    "backup_file_format": "%Y%m%d%H%M",
    "pretty_print": false
  },
  "grafana": {
    "url": "http://{{ ip }}:{{ port }}",
    "token": "{{ token }}",
    "search_api_limit": 5000,
    "default_password": "00000000",
    "admin_account": "",
    "admin_password": ""
  }
}
```

上述的配置中，需要根据实际情况填写ip和端口。token的申请则使用 grafana 的 admin 用户在 web 页面上申请 admin 权限的 API 即可拿到。大致的操作路径：`Configuration` --> `API keys` --> `Add API key` --> `Role=admin` --> `Add`。

上述配置文件完成后，一行指令即可备份：

```
grafana-backup backup
```

则会在当前文件夹下的 \_OUTPUT_ 出现一个日期的 tar.gz 包。（这也是由配置声明的）。

## 恢复

同理，在新的 grafana 环境上先安装 grafana-backup 和配置 ~/.grafana-backup.json。然后使用备份的数据进行恢复。

```
grafana-backup restore 202101081550.tar.gz
```

如果没有报错则数据恢复成功。

## 参考链接

- [ysde/grafana-backup-tool](https://github.com/ysde/grafana-backup-tool)
- [教你一分钟内导出 Grafana 所有的 Dashboard](https://mp.weixin.qq.com/s/jAQIs75XdpU8gKSfBWJUWQ)
