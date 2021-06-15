---
layout: post
title: supervisord 与 worker 的应用
categories: [cate1, cate2]
description: some word here
keywords: keyword1, keyword2
---

# supervisord 与 worker 的应用

首先，目前使用 nohup 的方式启动，比较难托管，日志也是个问题，好处是方便灵活，同时只能通过 node_exporter 的 text-collector 或者 process_exporter 的方式进行进程监控。

换个思路，使用 supervisord 对 worker 进程进行托管，所有的环境变量都可以配置在 conf 文件中，版本变更，只需要更新二进制文件即可，启动过程直接 stop 或者 restart，同时可以添加预检测脚本。node_exporter 有一个 flag 即可检测 supervisourd 服务。

以 127.0.0.1 作为测试机器，已经测通。可以实现任务启动，日志重定输出，自动重启，进程监控。

首先给出 worker.conf 的配置。

```
# /etc/supervisor/conf.d/worker.conf
[program:lotus-worker]
command=/opt/cache/lotus-worker run --address=127.0.0.1:6969
directory=/opt/cache
autorstart=true
autorestart=true
user=Development
stopsignal=QUIT
redirect_stderr = true
stdout_logfile_backups = 10
stdout_capture_maxbytes = 100MB
stdout_logfile=/opt/cache/log/%(program_name)s_log.log
stderr_logfile_backups = 10
stderr_capture_maxbytes = 100MB
stderr_logfile=/opt/cache/log/%(program_name)s_error.log
environment =
  PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games",
  NLS_LANG=".AL32UTF8",
  IP=127.0.0.1,
  LOTUS_PATH=/opt/cache/repo,
  LOTUS_STORAGE_PATH=/opt/cache/lotusstorage,
  WORKER_PATH=/opt/cache/worker-path,
  FIL_PROOFS_PARAMETER_CACHE=/opt/lotus/v28-proof/,
  TMPDIR=/opt/cache,
  FIL_PROOFS_MAXIMIZE_CACHING=1,
  FIL_PROOFS_USE_GPU_COLUMN_BUILDER=1,
  FIL_PROOFS_PARENT_CACHE=/opt/cache/filecoin-parent/,
  MIN_AVAILABLE_MEMORY=640,
  SDR_WAIT_TIME=90,
  IPFS_GATEWAY="https://proof-parameters.s3.cn-south-1.jdcloud-oss.com/ipfs/",
  FIL_PROOFS_USE_GPU_TREE_BUILDER=1,
  RUST_LOG=Debug,
  STORAGE_API_INFO=xxxyy:/ip4/10.0.0.1/tcp/10002/http
```

这里面会提到IP指定，所以需要依赖于 ansible 做模版，使用 ansible_facts['default_ipv4']['address']  作为key。

为了实现进程监控，需要修改两个东西：

```
# /etc/supervisor/supervisord.conf
; supervisor config file

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
chmod=0700                       ; sockef file mode (default 0700)

[supervisord]
logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)

; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL  for a unix socket

; The [include] section can just contain the "files" setting.  This
; setting can list multiple files (separated by whitespace or
; newlines).  It can also contain wildcards.  The filenames are
; interpreted as relative to this file.  Included files *cannot*
; include files themselves.

[inet_http_server]
port = 127.0.0.1:9001

[include]
files = /etc/supervisor/conf.d/*.conf
```

```
# /lib/systemd/system/node_exporter.service
[Unit]
Description=node exporter service

[Service]
User=firefly
Group=firefly
Type=simple
ExecStart=/home/firefly/monitor/node_exporter/node_exporter --web.listen-address=:10003 --collector.supervisord.url="http://localhost:9001/RPC2" --collector.supervisord
Restart=on-success

[Install]
WantedBy=multi-user.target
```

在 prometheus 里通过 node_supervisord_up 进行进程状态判断以及告警配置。

## 参考

- [prometheus通过node_exporter进行supervisor监控](https://www.jianshu.com/p/7137cec03214)
- [RD文档-配置文件](https://www.rddoc.com/doc/Supervisor/3.3.1/zh/configuration/#unix-http-server-section-values)
- [Supervisor使用教程](https://juejin.im/entry/6844903745587773448)
