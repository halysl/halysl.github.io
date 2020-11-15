---
layout: post
title: ansible tower 的搭建
categories: [Linux, ansible]
description:
keywords: 
---

# ansible tower 的搭建

## 下载

```
axel https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-3.7.3-1.tar.gz -n 10
```

可能会出现：`重定向过多` 的问题，手动编译 axel 或者使用 wget 即可。

```
# 下载源码包
wget -O axel-2.16.1.tar.gz https://file.idait.cn/axel-2.16.1.tar.gz
# 解压
tar xzvf axel-2.16.1.tar.gz
# 进入目录
cd axel-2.16.1/

# 检查编译
./configure --prefix=/usr/local/axel
# 报错 No package 'openssl' found，则 yum install openssl-devel

make && make install
#报错请安装 gcc 工具 不报错请忽略

yum groupinstall "Development tools"
#axel 执行路径
echo 'PATH=/usr/local/axel/bin:$PATH' > /etc/profile.d/axel.sh
#使文件生效
. /etc/profile
```

## 配置并安装

```
cd /opt/
tar xf ansible-tower-setup-bundle-3.7.3-1.tar.gz
cd ansible-tower-setup-bundle-3.7.3-1/
```

```
# 配置密码
vim inventory

[tower]
localhost ansible_connection=local
[database]
[all:vars]
admin_password='abcdefg'
pg_host=''
pg_port=''
pg_database='awx'
pg_username='awx'
pg_password='abcdefg'
```

```
# 安装
./setup.sh
```

## 破解

```
# 安装 pip
cd /tmp
axel https://bootstrap.pypa.io/get-pip.py -n 10
python get-pip.py

# 安装 uncompyle6
pip install uncompyle6
```

```
cd /var/lib/awx/venv/awx/lib/python3.6/site-packages/tower_license
ls -al
总用量 12
-rw-r--r-- 1 root root 8348 9月  28 16:00 __init__.pyc
drwxr-xr-x 2 root root   37 11月 15 04:02 __pycache__

# 反汇编 init.pyc
uncompyle6 __init__.pyc >__init__.py

# 修改 __init__.py 文件
    def _check_cloudforms_subscription(self):
        return True    #添加这一行
        if os.path.exists('/var/lib/awx/i18n.db'):
            return True
        else:
            if os.path.isdir('/opt/rh/cfme-appliance'):
                if os.path.isdir('/opt/rh/cfme-gemset'):
                    pass
            try:
                has_rpms = subprocess.call(['rpm', '--quiet', '-q', 'cfme', 'cfme-appliance', 'cfme-gemset'])
                if has_rpms == 0:
                    return True
            except OSError:
                pass
 
            return False
....
 
# 修改 "license_date=253370764800L" 为 "license_date=253370764800"
    def _generate_cloudforms_subscription(self):
        self._attrs.update(dict(company_name='Red Hat CloudForms License', instance_count=MAX_INSTANCES,
          license_date=253370764800,  #修改
          license_key='xxxx',
          license_type='enterprise',
          subscription_name='Red Hat CloudForms License'))
...
 
#------------------------------------------------------------------
 
#修改完重新编译一下
[root@tower tower_license]# python3 -m py_compile __init__.py
[root@tower tower_license]# python3 -O -m py_compile __init__.py
 
#重启服务
[root@tower tower_license]# ansible-tower-service restart
```
