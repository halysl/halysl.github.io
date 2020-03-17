---
layout: post
title: 修复丢失的 GPG 密钥 Apt 存储库错误（NO_PUBKEY）
categories: [Linux, Ubuntu]
description:
keywords: 
---

# 修复丢失的 GPG 密钥 Apt 存储库错误（NO_PUBKEY）

apt遇到gpg error：pub key not found问题。

报错一般出现在 apt/apt-get update/upgrade 相关操作时。大致报错内容为：

```sh
W: GPG error: https://packages.grafana.com/oss/deb stable InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 8C8C34C524098CB6
```

注意这个 `8C8C34C524098CB6` 这个就是 pub key。

- 这个问题出现的原因是：当您添加存储库，而忘记添加其公共密钥时，或者在尝试导入 GPG 密钥时可能出现临时密钥服务器错误
- 它造成的影响是：无法更新软件索引，从而无法更新软件
- 解决方案：导入公共GPG密钥

## 修复单个存储库的丢失 GPG 密钥问题

```sh
sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys THE_MISSING_KEY_HERE
```

THE_MISSING_KEY_HERE 在这里指代上面的 `8C8C34C524098CB6`。

完整指令是：

```sh
sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys 8C8C34C524098CB6
```

## 批量修复存储库的丢失 GPG 密钥问题

```sh
sudo apt update 2>&1 1>/dev/null | sed -ne 's/.*NO_PUBKEY //p' | while read key; do if ! [[ ${keys[*]} =~ "$key" ]]; then sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys "$key"; keys+=("$key"); fi; done
```

## 参考

- [Fix Missing GPG Key Apt Repository Errors (NO_PUBKEY)](https://www.linuxuprising.com/2019/06/fix-missing-gpg-key-apt-repository.html)
