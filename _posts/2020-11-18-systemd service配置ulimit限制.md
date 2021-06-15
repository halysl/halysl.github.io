---
layout: post
title: systemd service 配置 ulimit 限制
categories: [Linux,systemd]
description: some word here
keywords: keyword1, keyword2
---

# systemd service 配置 ulimit 限制

在 bash 中，有个 ulimit 命令，提供了对 shell 及该 shell 启动的进程的可用资源控制。主要包括打开文件描述符数量、用户的最大进程数量、coredump 文件的大小等。

在 CentOS 5/6 等版本中，资源限制的配置可以在 /etc/security/limits.conf 设置，针对 root/user 等各个用户或者 \* 代表所有用户来设置。 当然，/etc/security/limits.d/ 中可以配置，系统是先加载 limits.conf 然后按照英文字母顺序加载 limits.d 目录下的配置文件，后加载配置覆盖之前的配置。 一个配置示例如下：

```conf
soft   nofile    100000
*     hard   nofile    100000
*     soft   nproc     100000
*     hard   nproc     100000
*     soft   core      100000
*     hard   core      100000
```

不过，在 CentOS 7 or RHEL 7 的系统中，使用 Systemd 替代了之前的 SysV，因此 /etc/security/limits.conf 文件的配置作用域缩小了一些。limits.conf 这里的配置，只适用于通过 PAM 认证登录用户的资源限制，它对 systemd 的 service 的资源限制不生效。登录用户的限制，与上面讲的一样，通过 /etc/security/limits.conf 和 limits.d 来配置即可。
对于systemd service的资源限制，如何配置呢？

全局的配置，放在文件:

- /etc/systemd/system.conf
- /etc/systemd/user.conf
- /etc/systemd/system.conf.d/*.conf
- /etc/systemd/user.conf.d/*.conf

其中，system.conf 是系统实例使用的，user.conf 用户实例使用的。一般的 sevice，使用system.conf 中的配置即可。systemd.conf.d/*.conf 中配置会覆盖 system.conf。

```
DefaultLimitCORE=infinity
DefaultLimitNOFILE=100000
DefaultLimitNPROC=100000
```

注意：修改了 system.conf 后，需要重启系统才会生效。

针对单个Service，也可以设置，以 nginx 为例。

编辑（两者皆可）：

- /usr/lib/systemd/system/nginx.service
- /usr/lib/systemd/system/nginx.service.d/my-limit.conf 

```
[Service]
LimitCORE=infinity
LimitNOFILE=100000
LimitNPROC=100000
```

```
sudo systemctl daemon-reload
sudo systemctl restart nginx.service
```

## 一些常见的配置项和 ulimit 的对应关系

```
Directive        ulimit equivalent     Unit
LimitCPU=        ulimit -t             Seconds      
LimitFSIZE=      ulimit -f             Bytes
LimitDATA=       ulimit -d             Bytes
LimitSTACK=      ulimit -s             Bytes
LimitCORE=       ulimit -c             Bytes
LimitRSS=        ulimit -m             Bytes
LimitNOFILE=     ulimit -n             Number of File Descriptors 
LimitAS=         ulimit -v             Bytes
LimitNPROC=      ulimit -u             Number of Processes 
LimitMEMLOCK=    ulimit -l             Bytes
LimitLOCKS=      ulimit -x             Number of Locks 
LimitSIGPENDING= ulimit -i             Number of Queued Signals 
LimitMSGQUEUE=   ulimit -q             Bytes
LimitNICE=       ulimit -e             Nice Level 
LimitRTPRIO=     ulimit -r             Realtime Priority  
LimitRTTIME=     No equivalent
```

```
# /lib/systemd/system/node_exporter.service
[Unit]
Description=node exporter service

[Service]
User=aaa
Group=aaa
Type=simple
LimitNOFILE=infinity
ExecStart=/path/node_exporter --web.listen-address=:9002 --collector.supervisord.url="http://localhost:9001/RPC2" --collector.supervisord --collector.textfile.directory /path/node_exporter/textfile/
Restart=on-success

[Install]
WantedBy=multi-user.target
```

## 转载信息

- [CentOS7系统中设置systemd service的ulimit限制](https://blog.51cto.com/kusorz/1917143)
- [How to set ulimits on service with systemd?](https://unix.stackexchange.com/questions/345595/how-to-set-ulimits-on-service-with-systemd)


