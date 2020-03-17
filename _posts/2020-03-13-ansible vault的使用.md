---
layout: post
title: ansible vault 的使用
categories: [Linux, 运维, ansible]
description:
keywords: 
---

# ansible vault 的使用

ansible 在某些特殊的操作，例如 become 提取操作，再或者有些配置文件有机密信息，不想明文保存，那么就需要用到 vault 这个工具。它随着 ansible 发行，调用方式为 ansible-vault。

在不是非常保密严格的场合，可以只配置 2-3 个 vault 密码，去加密 ansible 用到的所有文件。

现在假设当前目录下有以下文件：

```sh
ansible.cfg
hosts
hello.yml
```

那么除了 ansible.cfg 不能被加密，其他数据都可以加密。相当于用一个密码隐藏另一堆机密数据。

## 模块说明

create: 创建一个新文件，并直接对其进行加密
decrypt: 解密文件
edit: 用于编辑 ansible-vault 加密过的文件
encrypy: 加密文件
encrypt_strin: 加密字符串，字符串从命令行获取
view: 查看经过加密的文件
rekey: 重新设置密码

每个模块都很容易理解。

每个模块的作用可以参考：

- [ansible笔记（43）：使用 ansible-vault 加密数据](https://www.zsythink.net/archives/3250)
- [Ansible 加密模块 Vault](https://blog.51cto.com/steed/2432427)

## 使用方式

这里提供两种加密明文密码的使用姿势。

首先，我们需要创造一个 vault 的密码，这个密码可以人工创造，或者交给 openssl 自动生成，存储在特定文件里。

```sh
$ openssl rand -base64 100 > vault.pass
```

接着编辑 ansible.cfg 文件（该文件绝不能被 vault 加密）。

```sh
# echo 'vault_password_file = ./vault.pass' >> ansible.cfg
```

### 加密完整文件

可以利用 ansible 的 vars 分层方式，将机密变量和非机密变量分开。

```ini
# hosts
[test]
test1 ansible_host=10.1.1.1
test2 ansible_host=10.1.1.2
```

接着创建 group_vars 和 host_vars 文件夹。接着在 group_vars 文件夹内创建 test 目录，在 group_vars/test/ 下创建 secret 和 common 文件。在 secret 中写入机密信息。最后通过 ansible-vault 进行加密。由于在 ansible.cfg 中已经配置了 vault 文件位置，所以一切都是免密操作。

```sh
$ mkdir -p group_vars/test
$ mkdir -p host_vars/test{1,2}
$ touch group_vars/test/secret group_vars/test/common
$ echo 'pass: 123456' >>  group_vars/test/secret
$ ansible-vault encrypt group_vars/test/secret
$ cat group_vars/test/secret
$ANSIBLE_VAULT;1.1;AES256
64326239346537383433366361333964633536643730343962386463666266383663663661326238
6433353232373961616466383136613935333361386264610a616165386533623435323261363437
38653263323134623136366264633565656565646437363764383165356262633163323332306365
6666366233323333330a643962373964656334666662623164306634393130323734383531303664
65363937636433636335353235633638303335393335373839363438626134363465
```

好了，一切大功告成，保护好 vault.pass 文件就好了。

更多的变量分组分层的资料可以参考：[ansible 笔记（44）](https://www.zsythink.net/archives/3270)。

### 加密字符串

除了对完整的文件进行加密，也可以对 字符串 进行加密。

```yml
# hello.yml
- hosts: test1
  vars:
    pass: 123456
  tasks:
    - debug:
        msg: "{{ pass }}"
```

```sh
$ ansible-vault encrypt_string 123456
!vault |
          $ANSIBLE_VAULT;1.1;AES256
          34653630613836316563313166623466633266323235626238653736396533346635653761656338
          6435353532633765623832373266333536646530663534640a383566313036666536383362633962
          65653635343830396666386563313036623134633438373131353030383534316665623166663366
          6365626432313632380a663566343366393130366439613463653765383237656430386233306539
          3566
Encryption successful
$ vi hello.yml  # 替换 123456
```

```yml
# hello.yml
- hosts: test1
  vars:
    pass: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          34653630613836316563313166623466633266323235626238653736396533346635653761656338
          6435353532633765623832373266333536646530663534640a383566313036666536383362633962
          65653635343830396666386563313036623134633438373131353030383534316665623166663366
          6365626432313632380a663566343366393130366439613463653765383237656430386233306539
          3566
  tasks:
    - debug:
        msg: "{{ pass }}"
```

这样就可以了，但是 ansible_become_pass 这个变量无法通过该方式加密。

## 参考

- [ansible笔记（43）：使用 ansible-vault 加密数据](https://www.zsythink.net/archives/3250)
- [Ansible 加密模块 Vault](https://blog.51cto.com/steed/2432427)
- [ansible 笔记（44）](https://www.zsythink.net/archives/3270)
- [Using Vault in playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html)
