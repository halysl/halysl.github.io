---
layout: post
title: WTF，一款个人终端仪表板
categories: [Linux]
description: WTF，一款个人终端仪表板
keywords: Linux
---

# WTF，一款个人终端仪表板

主要使用方法，看下面两个链接就好了。

- [WTF - the terminal dashboard](https://wtfutil.com/)
- [开始使用 WTF 吧，一款终端仪表板](https://zhuanlan.zhihu.com/p/55873451)

目前个人使用，还是遇到了一点坑。

## 坑一：配置文件

`wtfutil` 指令可以通过 `-c/--config` 指定特定的配置文件加载，但是实际在自己的机器上（macOS High Sierra）上无论怎么指定，都会指向 `~/.config/wtf/config.yml`，如果将该文件删除，那么就会生成一份默认的。对此我的解决方案是，直接修改 `~/.config/wtf/config.yml`，玩坏了，就重新生成默认配置。

## 坑二：部分模块设定 boarder：true，会导致左侧一列字符被吃掉

- 通过 CMDRUNNER 模块设置 `istats all` 会出现左侧一列字符消失，设置 boarder：false，问题解决，但缺少了 title 和边界区分
- 设置 DOCKER 模块，问题如上所述

由于官方目前提供的很多模块也是借助于一些接口的，例如：GitHub，GitLab，TRAVISCI 等，这些模块就没做测试，也暂时没用上。

## 坑三：DIGITAL CLOCK 模块显示错误

DIGITAL CLOCK 模块在我这边的显示效果，可以理解为第 3-5 个像素集体向左移动 1 像素，无论如何设置 height 和 width。

## 我想做的：增加一个课程表板块

## 我的配置

下面是我个人的配置，在 MacBook Pro 15‘ 2015 中，iTerm 完整屏幕显示效果还可以。(需要主动配置 git 仓库位置以及 markdown 文件位置)。

```shell
# 终端参数
➜  wtf echo $COLUMNS
204
➜  wtf echo $LINES
51
```

```yml
# ~/.config/wtf/config.yml

wtf:
  colors:
    border:
      focusable: darkslateblue
      focused: orange
      normal: gray
  grid:
    columns: [40, 40, 40, 40, 40]
    rows: [13, 13, 13, 5, 5]
  refreshInterval: 1
  mods:
    clocks:
      colors:
        rows:
          even: "lightblue"
          odd: "lightgreen"
      enabled: true
      locations:
        Shanghai: "Asia/Shanghai"
        Tokyo: "Asia/Tokyo"
        Toronto: "America/Toronto"
        New York: "America/New York"
        London: "Europe/London"
        Moscow: "Europe/Moscow"
        Hong Kong: "Asia/Hong Kong"
        Taipei: "Asia/Taipei"
      position:
        top: 0
        left: 0
        height: 1
        width: 2
      refreshInterval: 15
      timeFormat: "15:04:05 -0700 MST * 2006 January 2 * Monday"
      dateFormat: ""
      sort: "chronological"
      title: "Clocks"
      type: "clocks"
    ipinfo:
      border: true
      colors:
        name: "lightblue"
        value: "white"
      enabled: true
      position:
        top: 1
        left: 0
        height: 1
        width: 1
      refreshInterval: 150
    power:
      enabled: true
      position:
        top: 1
        left: 1
        height: 1
        width: 1
      refreshInterval: 15
      title: "⚡️"
    nbascore:
      enabled: true
      position:
        top: 2
        left: 2
        height: 1
        width: 2
      refreshInterval: 600
    uptime:
      args: [""]
      cmd: "uptime"
      enabled: true
      position:
        top: 3
        left: 2
        height: 1
        width: 2
      refreshInterval: 30
      type: cmdrunner
    security:
      enabled: true
      position:
        top: 2
        left: 1
        height: 1
        width: 1
      refreshInterval: 3600
    resourceusage:
      enabled: true
      position:
        top: 2
        left: 0
        height: 1
        width: 1
      refreshInterval: 1
    todo:
      checkedIcon: "X"
      colors:
        checked: gray
        highlight:
          fore: "black"
          back: "orange"
      enabled: true
      filename: "todo.yml"
      position:
        top: 3
        left: 0
        height: 2
        width: 1
      refreshInterval: 3600
    prettyweather:
      enabled: true
      city: "Hangzhou, China"
      position:
        top: 3
        left: 1
        height: 2
        width: 1
      refreshInterval: 300
      unit: "m"
      view: 0
      language: "en"
    git:
      commitCount: 5
      commitFormat: "[forestgreen]%h [grey]%cd [white]%s [grey]%an[white]"
      dateFormat: "%H:%M %d %b %y"
      enabled: true
      position:
        top: 0
        left: 2
        height: 2
        width: 3
      refreshInterval: 8
      repositories:
      - "/path/to/git/repository/1"
      - "/path/to/git/repository/2"
    textfile:
      enabled: true
      filePaths:
      - "/path/to/markdown/file1"
      - "/path/to/markdown/file2"
      format: true
      formatStyle: "dracula"
      position:
        top: 2
        left: 4
        height: 3
        width: 1
      refreshInterval: 15
      wrapText: true
```
