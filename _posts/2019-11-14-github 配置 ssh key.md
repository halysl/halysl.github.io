---
layout: post
title: GitHub 配置 ssh key
categories: [Git, Skill]
description: GitHub 配置 ssh key
keywords: 
---

# GitHub 配置 ssh key

## 生成 key

```
ssh-keygen -t rsa -C "your_email@example.com"
```

代码参数含义：

- -t 指定密钥类型，默认是 rsa ，可以省略。
- -C 设置注释文字，比如邮箱。
- -f 指定密钥文件存储文件名。

然后在交互式页面，指定文件位置，推荐设置为 `~/.ssh/id_rsa_github`。

然后回车，回车，等待命令结束后，通过 `ls -al ~/.ssh` 观察是否多了两个文件 `id_rsa_github` 和 `id_rsa_github.pub`。

## 将 key.pub 添加到 GitHub 账户

a. 首先你需要拷贝 `id_rsa_github.pub` 文件的内容，你可以用编辑器打开文件复制，也可以用命令复制该文件的内容，如：

```sh
$ clip < ~/.ssh/id_rsa_github.pub
```

b、登录你的github账号，从右上角的设置（ [Account Settings](https://github.com/settings) ）进入，然后点击菜单栏的 SSH key 进入页面添加 SSH key。

c、点击 Add SSH key 按钮添加一个 SSH key 。把你复制的 SSH key 代码粘贴到 key 所对应的输入框中，记得 SSH key 代码的前后不要留有空格或者回车。当然，上面的 Title 所对应的输入框你也可以输入一个该 SSH key 显示在 github 上的一个别名。默认的会使用你的邮件名称。

## 配置 config

首先观察 `~/.ssh` 路径下是否有 `config` 文件，如果没有，创建一个 `touch ~/.ssh/config`，如果有直接编辑。

将以下配置项复制到 config 文件中。

```
Host github.com
HostName github.com
IdentityFile ~/.ssh/id_rsa_github
```

它的意思是，如果 ssh 连接的 hostname 是 github.com，那么就直接使用 `id_rsa_github` 文件。

## 测试

```
ssh -T git@github.com
```

当你输入以上代码时，会有一段警告代码，如：

```
The authenticity of host 'github.com (207.97.227.239)' can't be established.
# RSA key fingerprint is 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48.
# Are you sure you want to continue connecting (yes/no)?
```

这是正常的，你输入 yes 回车既可。

```
Hi username! You've successfully authenticated, but GitHub does not
# provide shell access.
```

如果用户名是正确的,你已经成功设置SSH密钥。

## 