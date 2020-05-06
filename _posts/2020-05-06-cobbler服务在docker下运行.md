---
layout: post
title: cobbler 服务在 docker 下运行
categories: [Linux, docker, Cobbler]
description: cobbler 服务在 docker 下运行
keywords: 
---

# cobbler 服务在 docker 下运行

主要参考 [Cobbler 批量装机](https://github.com/jasonlix5/docker-cobbler)。

在宿主机上的 /mnt 内挂载镜像。

```sh
$ sudo mkdir /mnt/ubuntu18.04
$ sudo mkdir /mnt/centos
$ sudo mount -t iso9660 -r -o ro,loop /tmp/ubuntu-18.04.3-server-amd64.iso /mnt/ubuntu18.04
$ sudo mount -t iso9660 -r -o ro,loop /tmp/CentOS-7-x86_64-DVD-1908.iso /mnt/centos
```

编辑自动应答脚本 ubuntu1804.seed：

```txt
d-i debian-installer/locale     string  en_US.UTF-8

d-i console-setup/ask_detect    boolean false

d-i keyboard-configuration/layoutcode   string  us
d-i keyboard-configuration/variantcode  string

d-i netcfg/choose_interface select  auto
d-i netcfg/get_hostname     string  $myhostname
d-i netcfg/get_nameservers  string  192.168.31.1
d-i netcfg/get_ipaddress    string
d-i netcfg/get_netmask      string  255.255.255.0
d-i netcfg/get_gateway      string  192.168.31.1
d-i netcfg/confirm_static   boolean true
d-i netcfg/without_default_route boolean true
d-i netcfg/enable boolean false

d-i time/zone string    Asia/Shanghai

d-i clock-setup/utc         boolean     true
d-i clock-setup/ntp         boolean     true
d-i clock-setup/ntp-server  string      ntp.ubuntu.com

d-i mirror/country          string  manual
d-i mirror/http/hostname    string  $http_server
d-i mirror/http/directory   string  $install_source_directory
d-i mirror/http/proxy       string

d-i live-installer/net-image    string  http://$http_server/cobbler/links/$distro_name/install/filesystem.squashfs

# d-i partman-auto/disk               string  /dev/sda
# d-i partman-auto/method             string  regular
# d-i partman-auto/choose_recipe      select  fsm
# d-i partman-lvm/device_remove_lvm   boolean true
# d-i partman-md/device_remove_md     boolean true
# d-i partman-auto/expert_recipe      string \
# fsm :: \
# 1024 100% 1024 linux-swap method{ swap } \
# format{ } \
# . \
# 20480 20480 20480 ext4 method{ format } \
# mountpoint{ /tmp } \
# format{ } use_filesystem{ } filesystem{ ext4 } \
# options/relatime{ relatime } \
# . \
# 1 2048 1000000000 ext4 method{ format } \
# mountpoint{ /data } \
# format{ } use_filesystem{ } filesystem{ ext4 } \
# options/relatime{ relatime } \
# .
# d-i partman-lvm/confirm_nooverwrite                 boolean true
# d-i partman-lvm/confirm                             boolean true
# d-i partman-partitioning/confirm_write_new_label    boolean true
# d-i partman/confirm_nooverwrite                     boolean true
# d-i partman/confirm                                 boolean true
# d-i partman/choose_partition \
# select Finish partitioning and write changes to disk

d-i passwd/root-login               boolean true
d-i passwd/root-password-crypted    paddssword $1$root$6lvA6eQ6m1Qum8aZ4VWPV1
d-i passwd/make-user                boolean true
d-i passwd/user-fullname            string firefly
d-i passwd/username                 string firefly
d-i passwd/user-password-crypted    password $1$firefly$AbmnMjNadI/O7S/2vlojK.
d-i passwd/user-uid                 string
d-i passwd/user-default-groups      string sudo adm cdrom dialout lpadmin plugdev sambashare

d-i user-setup/allow-password-weak  boolean false
d-i user-setup/encrypt-home         boolean false

d-i apt-setup/services-select       multiselect security
d-i apt-setup/security_host         string mirrors.aliyun.com
d-i apt-setup/security_path         string /ubuntu

d-i debian-installer/allow_unauthenticated  string false
$SNIPPET('preseed_apt_repo_config')

d-i pkgsel/include string ntp ssh wget vim
d-i pkgsel/include string vim openssh-server

d-i grub-installer/skip             boolean false
d-i lilo-installer/skip             boolean false
d-i grub-installer/only_debian      boolean true
d-i grub-installer/with_other_os    boolean true

d-i finish-install/keep-consoles        boolean false
d-i finish-install/reboot_in_progress   note

d-i cdrom-detect/eject boolean true

d-i debian-installer/exit/halt      boolean false
d-i debian-installer/exit/poweroff  boolean false

d-i preseed/early_command string wget -O- \
   http://$http_server/cblr/svc/op/script/$what/$name/?script=preseed_early_default | \
   /bin/sh -s
d-i preseed/late_command string   wget -O /target/etc/apt/sources.list    http://$http_server/sources.list ; \
 wget -O /target/etc/locale.conf   http://$http_server/locale.conf ; \
 wget -O /target/etc/default/locale   http://$http_server/locale ; \
 cd /target ; \
 chroot ./ apt-get update

```

启动虚拟机，并进入。

```sh
$ git clone https://github.com/jasonlix5/docker-cobbler.git
$ cd docker-cobbler
$ vi cobbler.env  # 修改基本信息
$ vi Dockerfile  # yum 增加一个 file 的安装；通过 ADD 添加 自动应答脚本 到 image 里（也可以后面直接进入 docker 里增加
$ docker-compose up -d
$ docker exec -it docker-cobbler_cobbler_1 bash
```

cobbler import 镜像

```sh
$ cobbler import --path=/mnt/ubuntu18.04 --name=ubuntu-18.04.3 --kickstart=/var/lib/cobbler/kickstarts/ubuntu1804.seed --arch=x86_64
$ cobbler import --path=/mnt/centos --name=centos-7 --arch=x86_64 
$ cobbler sync
```

打开虚拟机，设置 pxe 启动，可以自动进入 cobbler 界面，并出现 ubuntu18.04 和 centos 的安装选项。

> 如果宿主机的 mnt 更新了新的镜像，那么需要重启下 docker-cobbler_cobbler_1 实例。

## 参考

- [Cobbler 批量装机](https://github.com/jasonlix5/docker-cobbler)
- [Cobbler in a Docker Container](https://blog.container-solutions.com/cobbler-in-a-docker-container)
- [用docker快速布署cobbler装机系统](https://blog.51cto.com/qingwa/2129931)
- [Cobbler 安装与配置](https://liuzhinet.cn/archives/cobbler%E5%AE%89%E8%A3%85%E4%B8%8E%E9%85%8D%E7%BD%AE)
