---
layout: post
title: pip安装mysql-python出现的问题
categories: [python, pip]
description: pip安装mysql-python出现的问题
keywords: python, pip, linux
---

# pip安装mysql-python出现的问题

使用 pip 安装 mysql-python 这个包，总是会遇到各种问题，以我个人为例，就在 deepin linux，MacOSX，rhel6.7 上遇到过三次，这里主要针对的是 `EnvironmentError: mysql_config not found` 问题，解决方案来自于stackoverflow。

## 问题描述

```
(mysite)zjm1126@zjm1126-G41MT-S2:~/zjm_test/mysite$ pip install mysql-python
Downloading/unpacking mysql-python
  Downloading MySQL-python-1.2.3.tar.gz (70Kb): 70Kb downloaded
  Running setup.py egg_info for package mysql-python
    sh: mysql_config: not found
    Traceback (most recent call last):
      File "<string>", line 14, in <module>
      File "/home/zjm1126/zjm_test/mysite/build/mysql-python/setup.py", line 15, in <module>
        metadata, options = get_config()
      File "setup_posix.py", line 43, in get_config
        libs = mysql_config("libs_r")
      File "setup_posix.py", line 24, in mysql_config
        raise EnvironmentError("%s not found" % (mysql_config.path,))
    EnvironmentError: mysql_config not found
    Complete output from command python setup.py egg_info:
    sh: mysql_config: not found

Traceback (most recent call last):

  File "<string>", line 14, in <module>

  File "/home/zjm1126/zjm_test/mysite/build/mysql-python/setup.py", line 15, in <module>

    metadata, options = get_config()

  File "setup_posix.py", line 43, in get_config

    libs = mysql_config("libs_r")

  File "setup_posix.py", line 24, in mysql_config

    raise EnvironmentError("%s not found" % (mysql_config.path,))

EnvironmentError: mysql_config not found

----------------------------------------
Command python setup.py egg_info failed with error code 1
Storing complete log in /home/zjm1126/.pip/pip.log
(mysite)zjm1126@zjm1126-G41MT-S2:~/zjm_test/mysite$ pip install mysql-python
Downloading/unpacking mysql-python
  Running setup.py egg_info for package mysql-python
    sh: mysql_config: not found
    Traceback (most recent call last):
      File "<string>", line 14, in <module>
      File "/home/zjm1126/zjm_test/mysite/build/mysql-python/setup.py", line 15, in <module>
        metadata, options = get_config()
      File "setup_posix.py", line 43, in get_config
        libs = mysql_config("libs_r")
      File "setup_posix.py", line 24, in mysql_config
        raise EnvironmentError("%s not found" % (mysql_config.path,))
    EnvironmentError: mysql_config not found
    Complete output from command python setup.py egg_info:
    sh: mysql_config: not found

Traceback (most recent call last):

  File "<string>", line 14, in <module>

  File "/home/zjm1126/zjm_test/mysite/build/mysql-python/setup.py", line 15, in <module>

    metadata, options = get_config()

  File "setup_posix.py", line 43, in get_config

    libs = mysql_config("libs_r")

  File "setup_posix.py", line 24, in mysql_config

    raise EnvironmentError("%s not found" % (mysql_config.path,))

EnvironmentError: mysql_config not found

----------------------------------------
Command python setup.py egg_info failed with error code 1
Storing complete log in /home/zjm1126/.pip/pip.log
```

## 解决方案

### Debian/Ubuntu

```
sudo apt-get install libmysqlclient-dev
```

新版本（比如2018）的 Debian/Ubuntu

```
sudo apt install default-libmysqlclient-dev
```

### Mac OSX

```
export PATH=$PATH:/usr/local/mysql/bin
```

前提是已经安装 mysql

```
brew install mysql
```

### Centos/RHEL

```
yum install -y mysql-devel python-devel python-setuptools
```

## 解决方案来源

[pip install mysql-python fails with EnvironmentError: mysql_config not found
](https://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found)