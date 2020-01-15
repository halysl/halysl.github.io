---
layout: post
title: 【转载】Supervisord 的使用
categories: [Linux, Ubuntu, Supervisord, 转载]
description:
keywords: 
---

# 【转载】Supervisord 的使用

Supervisor（http://supervisord.org/）是用 Python 开发的一个 client/server 服务，是 Linux/Unix 系统下的一个进程管理工具，不支持 Windows 系统。它可以很方便的监听、启动、停止、重启一个或多个进程。用 Supervisor 管理的进程，当一个进程意外被杀死， supervisort 监听到进程死后，会自动将它重新拉起，很方便的做到进程自动恢复的功能，不再需要自己写 shell 脚本来控制。

因为 Supervisor 是 Python 开发的，安装前先检查一下系统否安装了 Python2.4 以上版本。
下面以 Ubuntu 18.04，Python2.7 版本环境下，介绍 Supervisor 的安装与配置步聚：

## 安装 supervisor

```sh
sudo apt-get install supervisor
```

supervisor 安装完成后会生成三个执行程序：supervisortd、supervisorctl、echo_supervisord_conf，分别是 supervisor 的守护进程服务（用于接收进程管理命令）、客户端（用于和守护进程通信，发送管理进程的指令）、生成初始配置文件程序。

## 配置

运行 supervisord 服务的时候，需要指定 supervisor 配置文件，如果没有显示指定，默认在以下目录查找：

```sh
# $CWD表示运行supervisord程序的目录。
$CWD/supervisord.conf
$CWD/etc/supervisord.conf
/etc/supervisord.conf
/etc/supervisor/supervisord.conf (since Supervisor 3.3.0)
../etc/supervisord.conf (Relative to the executable)
../supervisord.conf (Relative to the executable)
```

可以通过运行 `echo_supervisord_conf` 程序生成supervisor的初始化配置文件，如下所示：

```sh
mkdir /etc/supervisor
echo_supervisord_conf > /etc/supervisor/supervisord.conf
```

## 配置文件参数说明

supervisor 的配置参数较多，下面介绍一下常用的参数配置，详细的配置及说明，请参考官方文档介绍。
注：分号（;）开头的配置表示注释

```conf
[unix_http_server]
file=/tmp/supervisor.sock   ;UNIX socket 文件，supervisorctl 会使用
;chmod=0700                 ;socket文件的mode，默认是0700
;chown=nobody:nogroup       ;socket文件的owner，格式：uid:gid

;[inet_http_server]         ;HTTP服务器，提供web管理界面
;port=127.0.0.1:9001        ;Web管理后台运行的IP和端口，如果开放到公网，需要注意安全性
;username=user              ;登录管理后台的用户名
;password=123               ;登录管理后台的密码

[supervisord]
logfile=/tmp/supervisord.log ;日志文件，默认是 $CWD/supervisord.log
logfile_maxbytes=50MB        ;日志文件大小，超出会rotate，默认 50MB，如果设成0，表示不限制大小
logfile_backups=10           ;日志文件保留备份数量默认10，设为0表示不备份
loglevel=info                ;日志级别，默认info，其它: debug,warn,trace
pidfile=/tmp/supervisord.pid ;pid 文件
nodaemon=false               ;是否在前台启动，默认是false，即以 daemon 的方式启动
minfds=1024                  ;可以打开的文件描述符的最小值，默认 1024
minprocs=200                 ;可以打开的进程数的最小值，默认 200

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ;通过UNIX socket连接supervisord，路径与unix_http_server部分的file一致
;serverurl=http://127.0.0.1:9001 ; 通过HTTP的方式连接supervisord

; [program:xx]是被管理的进程配置参数，xx是进程的名称
[program:xx]
command=/opt/apache-tomcat-8.0.35/bin/catalina.sh run  ; 程序启动命令
autostart=true       ; 在supervisord启动的时候也自动启动
startsecs=10         ; 启动10秒后没有异常退出，就表示进程正常启动了，默认为1秒
autorestart=true     ; 程序退出后自动重启,可选值：[unexpected,true,false]，默认为unexpected，表示进程意外杀死后才重启
startretries=3       ; 启动失败自动重试次数，默认是3
user=tomcat          ; 用哪个用户启动进程，默认是root
priority=999         ; 进程启动优先级，默认999，值小的优先启动
redirect_stderr=true ; 把stderr重定向到stdout，默认false
stdout_logfile_maxbytes=20MB  ; stdout 日志文件大小，默认50MB
stdout_logfile_backups = 20   ; stdout 日志文件备份数，默认是10
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile=/opt/apache-tomcat-8.0.35/logs/catalina.out
stopasgroup=false     ;默认为false,进程被杀死时，是否向这个进程组发送stop信号，包括子进程
killasgroup=false     ;默认为false，向进程组发送kill信号，包括子进程

;包含其它配置文件
[include]
files = relative/directory/*.ini    ;可以指定一个或多个以.ini结束的配置文件
```

include示例：

```sh
[include]
files = /opt/absolute/filename.ini /opt/absolute/*.ini foo.conf config??.ini
```

## 配置管理进程

进程管理配置参数，不建议全都写在 supervisord.conf 文件中，应该每个进程写一个配置文件放在 include 指定的目录下包含进 supervisord.conf 文件中。

- 创建 /etc/supervisor/config.d 目录，用于存放进程管理的配置文件
- 修改 /etc/supervisor/supervisord.conf 中的 include 参数，将 /etc/supervisor/conf.d 目录添加到 include 中

```conf
[include]
files = /etc/supervisor/config.d/*.ini
```

下面是配置Tomcat进程的一个例子：

```conf
[program:tomcat]
command=/opt/apache-tomcat-8.0.35/bin/catalina.sh run
stdout_logfile=/opt/apache-tomcat-8.0.35/logs/catalina.out
autostart=true
autorestart=true
startsecs=5
priority=1
stopasgroup=true
killasgroup=true
```

## 启动 Supervisor 服务

```sh
supervisord -c /etc/supervisor/supervisord.conf
```

## 控制进程

### 交互终端

supervisord 启动成功后，可以通过 supervisorctl 客户端控制进程，启动、停止、重启。运行 supervisorctl 命令，不加参数，会进入 supervisor 客户端的交互终端，并会列出当前所管理的所有进程。

输入 help 可以查看可以执行的命令列表，如果想看某个命令的作用，运行 help 命令名称，如：help stop

```sh
stop tomcat  // 表示停止tomcat进程
stop all     // 表示停止所有进程
```

### bash终端

```sh
supervisorctl status
supervisorctl stop tomcat
supervisorctl start tomcat
supervisorctl restart tomcat
supervisorctl reread
supervisorctl update
```

### Web管理界面

出于安全考虑，默认配置是没有开启 web 管理界面，需要修改 supervisord.conf 配置文件打开 http 访权限，将下面的配置：

```conf
;[inet_http_server]         ; inet (TCP) server disabled by default
;port=127.0.0.1:9001        ; (ip_address:port specifier, *:port for all iface)
;username=user              ; (default is no username (open server))
;password=123               ; (default is no password (open server))
```

修改成：

```conf
[inet_http_server]         ; inet (TCP) server disabled by default
port=0.0.0.0:9001          ; (ip_address:port specifier, *:port for all iface)
username=user              ; (default is no username (open server))
password=123               ; (default is no password (open server))
```

- port：绑定访问IP和端口，这里是绑定的是本地IP和9001端口
- username：登录管理后台的用户名
- password：登录管理后台的密码

> 如果想配置 node_exporter 里监控 supervisord 服务状态，那么需要根据 username，password 指定 collector.supervisord.url 参数，或者直接注释 username，password

## 开机启动 Supervisor 服务

略。

## 转载信息

- 版权声明：本文为CSDN博主「xyang0917」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
- 原文链接：https://blog.csdn.net/xyang81/article/details/51555473
