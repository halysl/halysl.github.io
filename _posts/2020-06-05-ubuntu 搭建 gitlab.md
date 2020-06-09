---
layout: post
title: Ubuntu 搭建 Gitlab
categories: [Linux, Ubuntu]
description:
keywords: 
---

# Ubuntu 搭建 Gitlab

## 准备工作

```
$ sudo apt-get install ruby vim curl openssh-server ca-certificates
$ gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/
$ bundle config mirror.https://rubygems.org https://mirrors.tuna.tsinghua.edu.cn/rubygems

```

## 安装 Gitlab

Gitlab 官网找到的下载链接都是 30 天适用的企业版本，其实把 gitlab-ee 改成 gitlab-ce 即可。

```
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash
# GitLab:       13.0.1 (74623c80da9) FOSS
# GitLab Shell: 13.2.0
# PostgreSQL:   11.7
sudo apt-get install gitlab-ce
```

后面就通过浏览器访问，配置自定义项目。

关于公钥密钥数据传输，这里掠过不谈。

## 备份数据

```
# 会自动在 /var/opt/gitlab/backups 目录下生成一个备份文件
gitlab-rake gitlab:backup:create
```

```
# 修改备份地址
vi /etc/gitlab/gitlab.rb

...
gitlab_rails['backup_path'] = "/var/opt/gitlab/backups"
...
```

```
vi /etc/crontab

# 添加定时任务，每天凌晨两点，执行 gitlab 备份
0  2    * * *   root    /opt/gitlab/bin/gitlab-rake gitlab:backup:create CRON=1
```

## 恢复数据

确认新老机器的gitlab服务版本一致。

假设备份文件叫做 1591207223_2020_06_04_13.0.1_gitlab_backup.tar。

```
chmod 777 1591207223_2020_06_04_13.0.1_gitlab_backup.tar
mv 1591207223_2020_06_04_13.0.1_gitlab_backup.tar /var/opt/gitlab/backups/
gitlab-ctl stop unicorn
gitlab-ctl stop sidekiq
gitlab-rake gitlab:backup:restore BACKUP=1591207223_2020_06_04_13.0.1

> yes
> yes

sudo gitlab-ctl start
```

## 参考

- [如何在Ubuntu 18.04上安装和配置GitLab](https://www.howtoing.com/how-to-install-and-configure-gitlab-on-ubuntu-18-04)
- [Gitlab如何进行备份恢复与迁移？](https://blog.csdn.net/qq446282412/article/details/77070977)
