---
layout: wiki
title: Docker
categories: Docker
description: Docker 常用操作记录。
keywords: Docker, 虚拟化, 容器化
---

## 常用指令

| 功能                      | 命令                                  |
|:--------------------------|:--------------------------------------|
| 获取镜像                   | docker pull image_name               |
| 获取特定版本的镜像           | docker pull image_name:version       |
| 查看本地已有的镜像           | docker images                        |
| 对本地镜像添加标签           | docker tag tag_name:version image_name:version|
| 查看镜像详细信息            | docker inspect image_id               |
| 在仓库搜索镜像              | docker search key_word<br>&nbsp; &nbsp;  --automated=false 仅显示自动创建的镜像<br>&nbsp; &nbsp;  --no-trunc=false 输出信息不截断<br>&nbsp; &nbsp;  -s, --stars=0指定仅显示评价为指定星级以上的镜像|
| 删除镜像                   | docker rmi image_tag/image_id         |
| 基于已有镜像的容器创建        | docker commit [options] container image_name<br>&nbsp; &nbsp; -a, --Author=作者信息<br>&nbsp; &nbsp; -m, --message=提交信息<br>&nbsp; &nbsp; -p, --pause=true提交时暂停容器运行 | 
| 基于本地模板导入             | cat model.tar.gz \| docker import - image_name |
| 保存镜像                   | docker save -o save_name image_name      |
| 载入镜像                   | docker load < save_name                  |
| 上传镜像                   | docker push image_name                   | 