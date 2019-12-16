---
layout: wiki
title: Homebrew
categories: Homebrew
description: Homebrew 的常规使用
keywords: Homebrew， 软件管理
---

# Homebrew

## 说明

Mac 的软件包管理工具，类似于 linux 的 apt-get，能在 mac 中方便地安装软件或者卸载软件。

## 安装及卸载

1. Homebrew 依赖 xcode 和其 Command Line Tools。

    - 在 App Store 中安装最新版本的 xcode；
    - 执行 xcode-select --install 安装 Command Line Tools。

2. 安装

```shell
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

3. 卸载

```shell
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"
```

## 使用

|指令|说明|示例|
|---|----|---|
|brew update|更新 Homebrew|brew update|
|brew list|显示已安装的软件|brew list|
|brew info|显示安装了包的数量、文件数量和总占用空间|brew info|
|brew info 软件名|显示某个包的信息，包括版本、git 仓库、最近的安装情况分析|brew info git|
|brew deps 软件名|显示某个包的依赖关系|brew deps git|
|brew deps --installed --tree|查看已安装的包的依赖，树形显示|brew deps --installed --tree|
|brew install 软件名|安装软件|brew install git|
|brew uninstall 软件名|卸载软件|brew uninstall git|
|brew search 查询内容|查找软件|brew search git|
|brew outdated|查看所有可更新的包|brew outdated|
|brew upgrade 软件名|升级指定软件|brew upgrade git|
|brew upgrade|升级所有软件|brew upgrade|
|brew cleanup -n|查看哪些软件包将被清除|brew cleanup -n|
|brew cleanup 软件名|清除指定软件包的所有老版本|brew cleanup|
|brew cleanup|清除所有软件包的所有老版本|brew cleanup|
|brew pin 软件名|锁定指定的软件包|brew pin git|
|brew unpin 软件名|解锁指定的软件包|brew unpin git|
|brew prune|清理无用的 symlink，且清理与之相关的位于 /Applications 和 ~/Applications 中的无用 App 链接|brew prune|
|brew link 软件名|将指定软件的安装文件 symlink 到 Homebrew 上，默认通过 brew install 安装的包这步自动执行|brew link git|
