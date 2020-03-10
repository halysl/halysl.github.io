
# ansible 基本操作

## 介绍

### 简介

ansible 是新出现的自动化运维工具，基于 Python 开发，集合了众多运维工具（puppet、cfengine、chef、func、fabric）的优点，实现了批量系统配置、批量程序部署、批量运行命令等功能。

ansible 是基于模块工作的，本身没有批量部署的能力。真正具有批量部署的是 ansible 所运行的模块，ansible 只是提供一种框架。

主要包括：

- 连接插件 connection plugins：负责和被监控端实现通信
- host inventory：指定操作的主机，是一个配置文件里面定义监控的主机
- 各种模块核心模块、command模块、自定义模块
- 借助于插件完成记录日志邮件等功能
- playbook：剧本执行多个任务时，非必需可以让节点一次性运行多个任务

相关链接：

- [ansible 代码](https://github.com/ansible/ansible/)
- [ansible 官网](https://docs.ansible.com)
- [playbook 分享平台](https://galaxy.ansible.com)

### 特性

- no agents：不需要在被管控主机上安装任何客户端
- no server：无服务器端，使用时直接运行命令即可
- modules in any languages：基于模块工作，可使用任意语言开发模块
- yaml，not code：使用 yaml 语言定制剧本playbook
- ssh by default：基于 SSH 工作
- strong multi-tier solution：可实现多级指挥

### 优点

- 轻量级，无需在客户端安装 agent，更新时，只需在操作机上进行一次更新即可
- 批量任务执行可以写成脚本，而且不用分发到远程就可以执行
- 使用 python 编写，维护更简单，ruby 语法过于复杂
- 支持 sudo

### 基本架构

![ansible基本架构](http://s3.51cto.com/wyfs02/M02/53/A7/wKiom1Rsxz3ToUCAAAGROYAM3EI989.jpg)

- 核心引擎：即 ansible
- 核心模块（core modules）：这些都是 ansible 自带的模块，ansible 模块资源分发到远程节点使其执行特定任务或匹配一个特定的状态
- 自定义模块（custom modules）：如果核心模块不足以完成某种功能，可以添加自定义模块
- 插件（plugins）：完成模块功能的补充，借助于插件完成记录日志、邮件等功能
- 剧本（playbook）：定义 ansible 任务的配置文件，可以将多个任务定义在一个剧本中，由 ansible 自动执行，剧本执行支持多个任务，可以由控制主机运行多个任务，同时对多台远程主机进行管理
- playbook 是 ansible 的配置、部署和编排语言，可以描述一个你想要的远程系统执行策略，或一组步骤的一般过程。如果 ansible 模块作为你的工作室工具，playbook 就是设计方案。在基本层面上，剧本可以用于管理配置和部署远程机器。在更高级的应用中，可以序列多层应用及滚动更新，并可以把动作委托给其他主机，与监控服务器和负载平衡器交互
- 连接插件（connection plugins）：ansible 基于连接插件连接到各个主机上，负责和被管理节点实现通信。虽然 ansible 是使用 ssh 连接到各被管理节点，但它还支持其他的连接方法，所以需要有连接插件
- 主机清单（host inventory）：定义 ansible 管理的主机策略，默认是在 ansible 的 hosts 配置文件中定义被管节点，同时也支持自定义动态主机清单和指定配置文件路径

ansible 采用 paramiko 协议库（Fabric 也使用这个），通过 ssh 或者 ZeroMQ 等连接主机。ansible 在控制主机主机将 ansible 模块通过 ssh 协议（或者 Kerberos、LDAP）推送到被管节点执行，执行完之后自动删除。控制主机与被管理节点之间支持 local、SSH、ZeroMQ 三种连接方式，默认使用基于 SSH 的连接。在规模较大的情况下使用 ZeroMQ 连接方式会明显改善执行速度。

### 任务执行模式（懒人，图源于网络，谢作图之人）

![ansible内部执行过程](http://s3.51cto.com/wyfs02/M01/53/A7/wKiom1Rsx2uQYJZ5AAJplY08vOQ976.jpg)

ansible 系统由控制主机对被管节点的操作方式可分为两类，即 ad-hoc 和 playbook。

- ad-hoc 模式使用单个模块，支持批量执行单条命令。
- playbook 模式是 ansible 的主要管理方式，通过多个 task 集合完成一类功能，可以简单的理解为通过组合多条 ad-hoc 操作的配置文件

### ansible 与其他配置管理软件的对比

|项目|Puppet|Saltstack|Ansible|
|---|------|---------|-------|
|开发语言|Ruby|Python|Python|
|是否有客户端|是|是|否|
|是否支持二次开发|不支持|支持|支持|
|服务器与远程机器是否相互验证|是|是|是|
|服务器与远程机器通信是否加密|是，标准SSL协议|是，使用AES加密|是，使用OpenSSH|
|是否提供 WEB UI 提供|提供|提供，但是商业版本|
|配置文件格式|Ruby语法|YAML|YAML|
|命令行执行|不支持，但可以通过配置模块实现|支持|支持|

## ansible 组件介绍

### 一、ansible cfg

ansible 的配置文件，默认文件为 /etc/ansible/ansible.cfg，可以看到可选的配置项是比较多的，可以应对很多情况，但复杂不代表好，我们可以自定义这个配置文件。

ansible.cfg 配置文件可以存在于多个地方，ansible 读取配置文件的顺序依次是

- 当前命令执行目录
- 用户根目录下的 .ansible.cfg
- /etc/ansible/ansible.cfg

可以通过执行 `ansible --version` 观察 `config file` 指向的具体是哪个文件。

常用的一种配置写法：

```ini
# /custom/path/ansible-custom/ansible.cfg
[defaults]
inventory = /custom/path/ansible-custom/hosts
remote_user = yourname
private_key_file = ~/.ssh/id_rsa
host_key_checking = False
retry_files_save_path = ./ansible-retry
```

复杂的配置根据需求进行配置，可参考：[ansible配置文件解析](https://carey.akhack.com/2017/05/28/ansible%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E8%A7%A3%E6%9E%90/)

### 二、ansible inventory

在大规模的配置管理工作中我们需要管理不同业务的机器，这些机器的信息都存放在 ansible 的 inventory 组件里。在我们工作中配置部署针对的主机必须先存放在 inventory 里，这样才能使用 ansible 对它进行操作。默认 ansible 的 inventory 是一个静态的 ini 文件 /etc/ansible/hosts。亦可通过 ANSIBLE_HOSTS 环境变量指定或者命令运行时用 -i 参数临时设置。

参考示例：

定义主机和主机组

```ini
# /etc/ansible/hosts
100.0.0.1 ansible_ssh_pass='123456'
100.0.0.2 ansible_ssh_pass='123456'
[docker]
100.0.0.1[1:3]
[docker:vars]
ansible_ssh_pass='123456'
[ansible:children]
docker
```

- 第一、二行定义一个主机，指定 ssh 登录密码
- 第三行定义了一个叫 docker 的组
- 第四行定义了 docker 组下面四个主机从 100.0.0.11-100.0.0.13
- 第五、六行定义了 docker 组的 ssh 登录密码
- 第七、八行定义了 ansible 组，ansible 组包含 docker 组
 
inventory 内置参数

|参数|解释|例子|
|---|----|--|
|ansible_ssh_host|将要连接的远程主机名，与你想要设定的主机的别名不同的话，可通过此变量设置|ansible_ssh_host=192.169.1.123|
|ansible_ssh_port|废弃。ssh端口号，默认为 22|ansible_ssh_port=5000|
|ansible_ssh_user|废弃。默认的 ssh 用户名，默认为当前用户|ansible_ssh_user=light|
|ansible_ssh_pass|废弃。ssh 密码，这种方式并不安全，推荐使用 SSH 密钥|ansible_ssh_pass=’123456’|
|ansible_sudo_pass|废弃。sudo 密码，这种方式并不安全，推荐使用 SSH 密钥|ansible_sudo_pass=’123456’|
|ansible_sudo_exe|sudo 命令路径|ansible_sudo_exe=/usr/bin/sudo|
|ansible_connection|与主机的连接类型。比如：`local`, `ssh` 或者 `paramiko`。Ansible 1.2 以前默认使用 paramiko。1.2 以后默认使用 'smart'，该方式会根据是否支持 ControlPersist, 来判断'ssh' 方式是否可行|ansible_connection=local|
|ansible_ssh_private_key_file|ssh 使用的私钥文件。适用于有多个密钥，而没有配置 ssh-agent 的情况|ansible_ssh_private_key_file=/root/key|
|ansible_shell_type|目标系统的shell类型。默认情况下，命令的执行使用 `sh` 语法，可设置为 `csh` 或 `fish`|ansible_shell_type=zsh|
|ansible_python_interpreter|目标主机的 python 路径。适用于的情况：系统中有多个 Python，或者命令路径不是 `/usr/bin/python`, 比如 /usr/bin/python 不是 2.X 版本的 Python。默认不使用 `/usr/bin/env` 机制。|ansible_python_interpreter=/usr/bin/python2.6|
|ansible_\*\_interpreter|定义其他语言解释器|ansible_*_interpreter=/usr/bin/ruby
|ansible_sudo|定义sudo用户	ansible_sudo=cxpadmin|

从 ansible v2.0 开始， ansible_ssh_user, ansible_ssh_host, ansible_ssh_port 已经改变为 ansible_user, ansible_host, ansible_port。具体参考官网http://docs.ansible.com/ansible/latest/intro_inventory.html|
 
### 三、ansible ad-hoc 模式

我们经常会通过命令行的形式使用 ansible 模块，ansible 自带很多模块，可以直接使用这些模块。目前 ansible 已经自带了 3300+ 个模块，我们可以使用 ansible-doc -l 显示所有自带模块，还可以使用 ansible-doc 模块名，查看模块的介绍以及案例。需要注意的是，如果使用 ad-hoc 模式，ansible 的一些插件功能就无法使用，比如 loop facts 功能等。

命令用法：`ansible <host-pattern> [options]`

### 四、ansible playbook

该模式很常用，属于核心功能，简单理解为多个 ad-hoc 模式下的操作集合，但除此之外还包括了例如分组，同步异步任务。

## 常用模块

常用模块：

- ping
- copy
- shell
- command
- raw
- fetch
- file
- service
- systemd
- cron
- script
- get_url
- synchronize
- [全部模块列表](https://docs.ansible.com/ansible/latest/modules/list_of_all_modules.html)

### ping 模块

ping 模块的作用与其名相同，即判断远程主机的网络是否畅通

示例：`ansible cluster_hosts -m ping`
 
### copy 模块

copy 模块在 ansible 里的角色就是把 ansible 执行机器上的文件拷贝到远程节点上。与 fetch 模块相反的操作。

|参数名|是否必须|默认值|选项|说明|
|-----|------|-----|----|-----|
|src|no|-|-|用于定位 ansible 执行的机器上的文件，需要绝对路径。如果拷贝的是文件夹，那么文件夹会整体拷贝，如果结尾是”/”,那么只有文件夹内的东西被考过去。一切的感觉很像rsync|
|content|no|-|-|用来替代 src，用于将指定文件的内容，拷贝到远程文件内|
|dest|yes|-|-|用于定位远程节点上的文件，需要绝对路径。如果 src 指向的是文件夹，这个参数也必须是指向文件夹|
|backup|no|no|yes/no|备份远程节点上的原始文件，在拷贝之前。如果发生什么意外，原始文件还能使用|
|directory_mode|no|-|-|这个参数只能用于拷贝文件夹时候，这个设定后，文件夹内新建的文件会被拷贝，而老旧的不会被拷贝|
|follow|no|no|yes/no|当拷贝的文件夹内有 link 存在的时候，那么拷贝过去的也会有 link|
|force|no|yes|yes/no|默认为 yes,会覆盖远程的内容不一样的文件（可能文件名一样）。如果是no，就不会拷贝文件，如果远程有这个文件|
|group|no|-|-|设定一个群组拥有拷贝到远程节点的文件权限|
|mode|no|-|-|等同于 chmod，参数可以为 “u+rwx or u=rw,g=r,o=r”|
|owner|no|-|-|设定一个用户拥有拷贝到远程节点的文件权限|
 
示例：将文件 copy 到测试主机

```sh
[root@node1 ansible]ansible testservers -m copy -a 'src=/root/install.log dest=/tmp/install.log owner=testuser group=testgroup'

192.168.100.131 | success >> {
"changed": true,
"checksum": "7b3626c84bb02d12472c03d2ece878fdc4756c94",
"dest": "/tmp/install.log",
"gid": 1100,
"group": "testgroup",
"md5sum": "c7d8a01a077940859e773b7770d2e07e",
"mode": "0644",
"owner": "testuser",
"size": 9458,
"src": "/root/.ansible/tmp/ansible-tmp-1456387213.94-229503410500766/source",
"state": "file",
"uid": 1000
}

192.168.100.132 | success >> {
"changed": true,
"checksum": "7b3626c84bb02d12472c03d2ece878fdc4756c94",
"dest": "/tmp/install.log",
"gid": 1100,
"group": "testgroup",
"md5sum": "c7d8a01a077940859e773b7770d2e07e",
"mode": "0644",
"owner": "testuser",
"size": 9458,
"src": "/root/.ansible/tmp/ansible-tmp-1456387213.94-186055595812050/source",
"state": "file",
"uid": 1000
}
```

示例：copy 前先备份

```sh
[root@node1 ansible]echo "test " >> /root/install.log
[root@node1 ansible]ansible testservers -m copy -a 'src=/root/install.log dest=/tmp/install.log owner=testuser group=testgroup backup=yes'

192.168.100.132 | success >> {
"backup_file": "/tmp/install.log.2016-02-25@16:01:26~",
"changed": true,
"checksum": "b5da7af32ad02eb98f77395b28f281a965b4c1f5",
"dest": "/tmp/install.log",
"gid": 1100,
"group": "testgroup",
"md5sum": "d39956add30a18019cb5ad2381a0cd43",
"mode": "0644",
"owner": "testuser",
"size": 9464,
"src": "/root/.ansible/tmp/ansible-tmp-1456387285.87-128685659798967/source",
"state": "file",
"uid": 1000
}

192.168.100.131 | success >> {
"backup_file": "/tmp/install.log.2016-02-25@16:01:26~",
"changed": true,
"checksum": "b5da7af32ad02eb98f77395b28f281a965b4c1f5",
"dest": "/tmp/install.log",
"gid": 1100,
"group": "testgroup",
"md5sum": "d39956add30a18019cb5ad2381a0cd43",
"mode": "0644",
"owner": "testuser",
"size": 9464,
"src": "/root/.ansible/tmp/ansible-tmp-1456387285.86-134452201968647/source",
"state": "file",
"uid": 1000
}

[root@node1 ansible]ansible testservers -m raw -a 'ls -lrth /tmp/install*'
192.168.100.131 | success | rc=0 >>
-rw-r--r-- 1 root root 9.3K 2 25 16:00 /tmp/install.log.2016-02-25@16:01:26~
-rw-r--r-- 1 testuser testgroup 9.3K 2 25 16:01 /tmp/install.log


192.168.100.132 | success | rc=0 >>
-rw-r--r-- 1 root root 9.3K 2 25 16:00 /tmp/install.log.2016-02-25@16:01:26~
-rw-r--r-- 1 testuser testgroup 9.3K 2 25 16:01 /tmp/install.log
```

示例：将目录copy过去

```sh
[root@node1 ansible]tree testdir
testdir
├── a
│ ├── e
│ │ └── ansible.cfg
│ ├── f
│ └── g
├── b
│ ├── e
│ ├── f
│ └── g
└── c
├── ansible.cfg
├── e
├── f
└── g


[root@node1 ansible]ansible testservers -m copy -a 'src=/etc/ansible/testdir dest=/tmp/ owner=testuser group=testgroup backup=yes'

192.168.100.131 | success >> {
"changed": true,
"dest": "/tmp/",
"src": "/etc/ansible/testdir"
}

192.168.100.132 | success >> {
"changed": true,
"dest": "/tmp/",
"src": "/etc/ansible/testdir"
}

[root@node1 ansible]ansible testservers -m command -a 'tree /tmp/testdir'

192.168.100.131 | success | rc=0 >>
/tmp/testdir
|-- a
| `-- e
| `-- ansible.cfg
|-- b
| `-- e
| `-- hosts
`-- c
`-- ansible.cfg

5 directories, 3 files

192.168.100.132 | success | rc=0 >>
/tmp/testdir
|-- a
| `-- e
| `-- ansible.cfg
|-- b
| `-- e
| `-- hosts
`-- c
`-- ansible.cfg

5 directories, 3 files

```

注意：发现有文件的目录 copy 成功，空的目录没有 copy 过去

|参数名|参数说明|返回值|返回值类型|样例|
|----|-------|-----|---------|----|
|src|位于ansible执行机上的位置|changed|string|/home/httpd/.ansible/tmp/ansible-tmp-1423796390.97-147729857856000/source|
|backup_file|将原文件备份|changed and if backup=yes|string|/path/to/file.txt.2015-02-12@22:09~|
|uid|在执行后，拥有者的ID|success|int|100|
|dest|远程节点的目标目录或文件|success|string|/path/to/file.txt|
|checksum|拷贝文件后的checksum值|success|string|6e642bb8dd5c2e027bf21dd923337cbb4214f827|
|md5sum|拷贝文件后的md5 checksum值|when supported|string|2a5aeecc61dc98c4d780b14b330e3282|
|state|执行后的状态|success|string|file|
|gid|执行后拥有文件夹、文件的群组ID|success|int|100|
|mode|执行后文件的权限|success|string|0644|
|owner|执行后文件所有者的名字|success|string|httpd|
|group|执行后文件所有群组的名字|success|string|httpd|
|size|执行后文件大小|success|int|1220|
 
### shell 模块

它负责在被 ansible 控制的节点（服务器）执行命令行。shell 模块是通过 /bin/sh 进行执行，所以 shell 模块可以执行任何命令，就像在本机执行一样。

|参数|是否必须|默认值|选项|说明|
|---|------|-----|-----|----|
|chdir  |no|跟command一样的，运行shell之前cd到某个目录|
|creates|no|跟command一样的，如果某个文件存在则不运行shell|
|removes|no|跟command一样的，如果某个文件不存在则不运行shell|
 
示例1: 让所有节点运行 somescript.sh 并把 log 输出到 somelog.txt

```sh
$ ansible -i hosts all -m shell -a "sh somescript.sh >> somelog.txt"
```

示例2: 先进入 somedir ，再在 somedir 目录下让所有节点运行 somescript.sh 并把 log 输出到 somelog.txt

```sh
$ ansible -i hosts all -m shell -a "somescript.sh >> somelog.txt" chdir=somedir/
```

示例3: 先 cd 到某个需要编译的目录，执行 condifgure 然后，编译，然后安装

```sh
$ ansible -i hosts all -m shell -a "./configure && make && make insatll" chdir=/xxx/yyy/
```
 
### command 模块

command 模块用于运行系统命令。不支持管道符和变量等（"<", ">", "|", and "&"等），如果要使用这些，那么可以使用 shell 模块。在使用 ansible 中的时候，默认的模块是 `-m command`，从而模块的参数不需要填写，直接使用即可。

|参数|是否必须|默认值|选项|说明|
|---|-------|-----|----|----|
|chdir|no|-|-|运行command命令前先cd到这个目录|
|creates|no|-|-|如果这个参数对应的文件存在，就不运行command|
|executable|no|-|-|将shell切换为command执行，这里的所有命令需要使用绝对路径|
|removes|no|-|-|如果这个参数对应的文件不存在，就不运行command|

示例1：ansible 命令调用command

```sh
ansible -i hosts all -m command -a "/sbin/shutdown -t now"
```

ansible 命令行调用 -m command 模块，-a 表示双引号内的为执行的 command 命令，该命令为关机。 

那么对应的节点(192.168.10.12,127.152.112.13)都会执行关机。

示例2：利用 creates 参数，判断 /path/to/database 这个文件是否存在，存在就跳过 command 命令，不存在就执行 command 命令

```sh
ansible -i hosts all -m command -a "/usr/bin/make_database.sh arg1 arg2 creates=/path/to/database"
```

### raw 模块

raw 模块的功能与 shell 和 command 类似。但 raw 模块运行时不需要在远程主机上配置 python 环境

示例：在 10.1.1.113 节点上运行 hostname 命令

```sh
ansible 10.1.1.113 -m raw-a 'hostname|tee'
```

### fetch 模块

文件拉取模块主要是将远程主机中的文件拷贝到本机中，和 copy 模块的作用刚刚相反，并且在保存的时候使用 hostname 来进行保存，当文件不存在的时候，会出现错误，除非设置了选项 fail_on_missing 为 yes。

|参数|必填|默认值|选项|说明|
|---|----|-----|----|----|
|dest|yes|-|-|用来存放文件的目录，例如存放目录为 backup，源文件名称为 /etc/profile 在主机 pythonserver 中，那么保存为 /backup/pythonserver/etc/profile|
|fail_on_missing|no|no|yes/no|当源文件不存在的时候，标识为失败|
|flat|no|-|-|允许覆盖默认行为从 hostname/path 到 /file 的，如果 dest 以 / 结尾，它将使用源文件的基础名称|
|src|yes|-|-|在远程拉取的文件，并且必须是一个 file，不能是目录|
|validate_checksum|no|yes|yes/no|当文件 fetch 之后进行 md5 检查|

示例1：fetch 一个文件保存，src 表示为远程主机上需要传送的文件路径，dest 表示为本机上的路径，在传送过来的文件，是按照 IP 地址进行分类，然后路径是源文件的路径。在拉取文件的时候，必须拉取的是文件，不能拉取文件夹。

```sh
ansible pythonserver -m fetch -a "src=/root/123 dest=/root"
SSH password:
192.168.1.60 | success >> {
    "changed": true,
    "dest": "/root/192.168.1.60/root/123",
    "md5sum": "31be5a34915d52fe0a433d9278e99cac",
    "remote_md5sum": "31be5a34915d52fe0a433d9278e99cac"
}
```

示例2：指定路径目录进行保存。在使用参数为 flat 的时候，如果 dest 的后缀名为/，那么就会保存在目录中，然后直接保存为文件名。当 dest 后缀不为 / 的时候，那么就会直接保存为 kel 的文件。主要是在于 dest 是否已/结尾，从而来区分这是个目录还是路径。

```sh
ansible pythonserver -m fetch -a "src=/root/Ssh.py dest=/root/kel/ flat=yes"
SSH password:
192.168.1.60 | success >> {
    "changed": true,
    "dest": "/root/kel/Ssh.py",
    "md5sum": "63f8a200d1d52d41f6258b41d7f8432c",
    "remote_md5sum": "63f8a200d1d52d41f6258b41d7f8432c"
}
```
 
### file 模块

主要用来设置文件、链接、目录的属性，或者移除文件、链接、目录，很多其他的模块也会包含这种作用，例如 copy，assemble 和 template。

|参数|必填|默认|选项|说明|
|---|----|----|---|---|
|follow|no|no|yes/no|这个标识说明这是系统链接文件，如果存在，应该遵循|
|force|no|no|yes/no|强制创建链接在两种情况下：源文件不存在（过会会存在）；目标存在但是是文件（创建链接文件替代）|
|group|no|-|-|文件所属用户组|
|mode|no|-|-|文件所属权限|
|owner|no|-|-|文件所属用户|
|path|yes|-|-|要控制文件的路径|
|recurse|no|no|yes/no|当文件为目录时，是否进行递归设置权限|
|src|no|-|-|文件链接路径，只有状态为 link 的时候，才会设置，可以是绝对相对不存在的路径
|state|no|File|File/link/directory/hard/touch/absent|参考[ansible:file-module](https://docs.ansible.com/ansible/latest/modules/file_module.html#file-module)|

示例1：设置文件属性。文件路径为 path，表示文件路径，设定所属用户和所属用户组，权限为0644。文件路径为 path，使用文件夹进行递归修改权限，使用的参数为 recurse 表示为递归。

```sh
ansible pythonserver -m file -a "path=/root/123 owner=kel group=kel mode=0644"
SSH password:
192.168.1.60 | success >> {
    "changed": true,
    "gid": 500,
    "group": "kel",
    "mode": "0644",
    "owner": "kel",
    "path": "/root/123",
    "size": 294,
    "state": "file",
    "uid": 500
}

ansible pythonserver -m file -a "path=/tmp/kel/ owner=kel group=kel mode=0644 recurse=yes"
SSH password:
192.168.1.60 | success >> {
    "changed": true,
    "gid": 500,
    "group": "kel",
    "mode": "0644",
    "owner": "kel",
    "path": "/tmp/kel/",
    "size": 4096,
    "state": "directory",
    "uid": 500
}
```

示例2：创建目录。创建目录，使用的参数主要是 state 为 directory。

```sh
ansible pythonserver -m file -a "path=/tmp/kel state=directory mode=0755"
SSH password:
192.168.1.60 | success >> {
    "changed": true,
    "gid": 0,
    "group": "root",
    "mode": "0755",
    "owner": "root",
    "path": "/tmp/kel",
    "size": 4096,
    "state": "directory",
    "uid": 0
}
```

示例3：修改权限。直接使用 mode 来进行修改权限。

```sh
ansible pythonserver -m file -a "path=/tmp/kel mode=0444"
SSH password:
192.168.1.60 | success >> {
    "changed": true,
    "gid": 0,
    "group": "root",
    "mode": "0444",
    "owner": "root",
    "path": "/tmp/kel",
    "size": 4096,
    "state": "directory",
    "uid": 0
}
```

示例4：创建软连接。src 表示已经存在的文件，dest 表示创建的软连接的文件名，最后的 state 状态为 link。

```sh
ansible pythonserver -m file -a "src=/tmp/1 dest=/tmp/2 owner=kel state=link"
SSH password:
192.168.1.60 | success >> {
    "changed": true,
    "dest": "/tmp/2",
    "gid": 0,
    "group": "root",
    "mode": "0777",
    "owner": "kel",
    "size": 6,
    "src": "/tmp/1",
    "state": "link",
    "uid": 500
}
```

### service 模块

service 模块其实就是 linux 下的 service 命令。用于 service 服务管理。

|参数名|是否必须|默认值|选项|说明|
|-----|-------|-----|---|----|
|enabled|no|yes/no|启动 os 后启动对应 service 的选项。使用 service 模块的时候，enabled 和 state 至少要有一个被定义|
|name|yes|-|-|需要进行操作的 service 名字|
|state|no|-|-|stared/stoped/restarted/reloaded|service最终操作后的状态|

示例1：启动服务。

```sh
ansible host31 -m service -a "name=httpd state=started" host31 | SUCCESS => { "changed": true, "name": "httpd", "state": "started" }
```

示例2：停止服务。

```sh
ansible host31 -m service -a "name=httpd state=stopped" host31 | SUCCESS => { "changed": true, "name": "httpd", "state": "stopped" }
```

示例3：设置服务开机自启动。

```sh
ansible host31 -m service -a "name=httpd enabled=yes state=restarted" host31 | SUCCESS => { "changed": true, "enabled": true, "name": "httpd", "state": "started" }
```

### systemd 模块

控制 systemd 服务。

|Parameter|Defaults|Choices|Comments|
|---------|--------|------|---------|
|daemon_reexec|no|yes/no|Run daemon_reexec command before doing any other operations, the systemd manager will serialize the manager state.|
|daemon_reload|no|yes/no|Run daemon-reload before doing any other operations, to make sure systemd has read any changes.When set to yes, runs daemon-reload even if the module does not start or stop anything.|
|enabled|-|yes/no|Whether the service should start on boot. At least one of state and enabled are required.|
|force|-|yes/no|Whether to override existing symlinks.
|masked|-|yes/no|Whether the unit should be masked or not, a masked unit is impossible to start.
|name|-|-|Name of the service. This parameter takes the name of exactly one service to work with.When using in a chroot environment you always need to specify the full name i.e. (crond.service).|
|no_block|no|yes/no|Do not synchronously wait for the requested operation to finish. Enqueued job will continue without Ansible blocking on its completion.|
|scope|-|system/user/global|run systemctl within a given service manager scope, either as the default system scope (system), the current user's scope (user), or the scope of all users (global).For systemd to work with 'user', the executing user must have its own instance of dbus started (systemd requirement). The user dbus process is normally started during normal login, but not during the run of Ansible tasks. Otherwise you will probably get a 'Failed to connect to bus: no such file or directory' error.|
|state|-|reloaded/restarted/started/stopped|started/stopped are idempotent actions that will not run commands unless necessary. restarted will always bounce the service. reloaded will always reload.|
|user|no|yes/no|(deprecated) run ``systemctl`` talking to the service manager of the calling user, rather than the service manager of the system.This option is deprecated and will eventually be removed in 2.11. The ``scope`` option should be used instead.|

example

```yml
- name: Make sure a service is running
  systemd:
    state: started
    name: httpd

- name: stop service cron on debian, if running
  systemd:
    name: cron
    state: stopped

- name: restart service cron on centos, in all cases, also issue daemon-reload to pick up config changes
  systemd:
    state: restarted
    daemon_reload: yes
    name: crond

- name: reload service httpd, in all cases
  systemd:
    name: httpd
    state: reloaded

- name: enable service httpd and ensure it is not masked
  systemd:
    name: httpd
    enabled: yes
    masked: no

- name: enable a timer for dnf-automatic
  systemd:
    name: dnf-automatic.timer
    state: started
    enabled: yes

- name: just force systemd to reread configs (2.4 and above)
  systemd:
    daemon_reload: yes

- name: just force systemd to re-execute itself (2.8 and above)
  systemd:
    daemon_reexec: yes
```

### cron 模块

cron 模块用于管理计划任务。

|参数名|是否必须|默认值|选项|说明|
|----|-------|-----|----|---|
|backup|-|-|-|对远程主机上的原任务计划内容修改之前做备份|
|cron_file|-|-|-|如果指定该选项，则用该文件替换远程主机上的cron.d目录下的用户的任务计划|
|day|-|-|-|日（1-31，*，*/2,……）|
|hour|-|-|-|小时（0-23，*，*/2，……）|
|minute|-|-|-|分钟（0-59，*，*/2，……）|
|month|-|-|-|月（1-12，*，*/2，……）|
|weekday|-|-|-|周（0-7，*，……）|
|job|-|-|-|要执行的任务，依赖于state=present|
|name|-|-|-|该任务的描述|
|special_time|-|-|-|指定什么时候执行，参数：reboot,yearly,annually,monthly,weekly,daily,hourly|
|state|-|-|-|确认该任务计划是创建还是删除|
|user|-|-|-|以哪个用户的身份执行|

示例：

```sh
ansible test -m cron -a 'name="a job for reboot" special_time=reboot job="/some/job.sh"'

ansible test -m cron -a 'name="yum autoupdate" weekday="2" minute=0 hour=12 user="root

ansible test -m cron  -a 'backup="True" name="test" minute="0" hour="5,2" job="ls -alh > /dev/null"'

ansilbe test -m cron -a 'cron_file=ansible_yum-autoupdate state=absent'
```

### script 模块

script 模块将控制节点的脚本执行在被控节点上。

示例：

```sh
ansible host32 -m script -a /tmp/hello.sh host32 | SUCCESS => { "changed": true, "rc": 0, "stderr": "", "stdout": "this is test from host32\r\n", "stdout_lines": [ "this is test from host32" ->执行结果 ] }
```

### get_url 模块

该模块主要用于从 http、ftp、https 服务器上下载文件（类似于 wget）

|参数名|是否必须|默认值|选项|说明|
|----|-------|------|----|----|
|sha256sum|-|-|-|下载完成后进行sha256 check；|
|timeout|-|-|-|下载超时时间，默认10s|
|url|-|-|-|下载的URL|
|url_password、url_username|-|-|-|主要用于需要用户名密码进行验证的情况|
|use_proxy|-|-|-|是事使用代理，代理需事先在环境变更中定义|

示例：将 http://10.1.1.116/favicon.ico 文件下载到指定节点的 /tmp 目录下

```sh
ansible 10.1.1.113 -m get_url -a 'url=http://10.1.1.116/favicon.ico dest=/tmp'
```

### synchronize模块

使用 rsync 同步文件。

|参数名|是否必须|默认值|选项|说明|
|----|-------|------|----|----|
|archive|-|-|-|归档，相当于同时开启recursive(递归)、links、perms、times、|owner、group、-D选项都为yes ，默认该项为开启|
|checksum|-|-|-|跳过检测sum值，默认关闭|
|compress|-|-|-|是否开启压缩|
|copy_links|-|-|-|复制链接文件，默认为no ，注意后面还有一个links参数|
|delete|-|-|-|删除不存在的文件，默认no|
|dest|-|-|-|目录路径|
|dest_port|-|-|-|dest_port：默认目录主机上的端口 ，默认是22，走的ssh协议
|dirs|-|-|-|传速目录不进行递归，默认为no，即进行目录递归|
|rsync_opts|-|-|-|rsync参数部分|
|set_remote_user|-|-|-|主要用于/etc/ansible/hosts中定义或默认使用的用户与rsync使用的用户不同的情况|
|mode|-|-|-|push或pull 模块，push模的话，一般用于从本机向远程主机上传文件，pull 模式用于从远程主机上取文件|

示例1：将主控方 /root/a 目录推送到指定节点的 /tmp 目录下

```sh
ansible 10.1.1.113 -m synchronize -a 'src=/root/a dest=/tmp/ compress=yes'
```

- delete=yes   使两边的内容一样（即以推送方为主）
- compress=yes  开启压缩，默认为开启
- --exclude=.Git  忽略同步 .git 结尾的文件

示例2：将 10.1.1.113 节点的 /tmp/a 目录拉取到主控节点的 /root 目录下

```sh
ansible 10.1.1.113 -m synchronize -a 'mode=pull src=/tmp/a dest=/root/'
```

## 核心模块 playbook

playbook 说白了就是一个个的 yaml 文件。yaml 格式作为 json 的一种用于数据传输的替代品，它完美兼容 json 的同时，又用结构化的方式排列数据。不熟悉语法会经常犯错，使用编辑器插件来避免这个问题。

复杂的 playbook 可以分级，引入 role 等概念，我们先来一个最简单的 playbook，一个单纯的 yaml 文件。