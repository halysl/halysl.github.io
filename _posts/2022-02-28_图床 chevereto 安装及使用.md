# 图床 chevereto 安装及使用

图床服务就是一个图片存储服务，图片直接存放到图床上，需要使用时直接通过一个链接进行调用。这意味着自制图床需要两个先决条件：

- 一台有存储空间的服务器
- 一个可以访问的 ip 地址

至于公有云上的图床，可能存在以下一些问题：

- 图片资源违规直接丢失
- 收费（容易超出预算）

一台 NAS 即可满足上述两个条件，在下面两篇文章中也提到了如何在 NAS 上配置图床：

- [群晖搭建 chevereto 图床](https://post.smzdm.com/p/a3gvxnon/)
- [在群晖中使用Chevereto搭建图床](https://lisenlinsirb.github.io/2020/11/21/20.11.21-chevereto_synology/)

但是出于对 NAS 的隐私性，公网访问不稳定性，性能三方面的考虑，决定不使用 NAS，而直接用服务器搭建，它本质上就是一个网络服务。

正好在良心云上有台低配的服务器，话不多少，直接折腾 [chevereto-free](https://github.com/rodber/chevereto-free)。

它的安装还是比较麻烦的，需要配置数据库、http 服务、PHP 服务，这些配置都可以查看 [Server Installation](https://chevereto-free.github.io/setup/server/installation.html)。

我直接使用容器的方式进行安装，按照 [chevereto container compose](https://chevereto-free.github.io/setup/container/compose.html) 描述的进行操作。

安装完成后，默认使用的是宿主机的 8810 端口，这需要去良心云的后台的主机防火墙配置中增加一个 allow 的选项，否则公网页无法访问，配置完成后，打开 public-ip:8810，填入基本信息就可以使用。

最简单的使用方法就是点击 Upload，然后上传本地图片或者通过 url 获取图片资源，理论上会有 api 上传的方案，这里暂且不表。

下面这张图就是该图床存的第一张图。

![2022-02-28-3.50.52.png](http://121.5.131.212:8810/images/2022/02/28/2022-02-28-3.50.52.png)

需要使用图片时，就点开图片详情页，在 `Embed codes` 会给出不同场合下该如何使用该图片的代码，例如:

![c6e1e43882e7fbc41082d40813cfeef8.png](http://121.5.131.212:8810/images/2022/02/28/c6e1e43882e7fbc41082d40813cfeef8.png)
