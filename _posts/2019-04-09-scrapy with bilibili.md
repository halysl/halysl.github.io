---
layout: post
title: scrapy框架初使用及爬取LOL信息
categories: [Python, 爬虫, 逃离CSDN]
description: scrapy框架初使用及爬取LOL信息
keywords: Python, 爬虫, 逃离CSDN
---

# Scrapy with bilibili

## 一、前言

在一个月前，我写了一篇[scrapy 框架初使用及爬取 LOL 信息](https://halysl.github.io/2019/03/11/scrapy%E6%A1%86%E6%9E%B6%E5%88%9D%E4%BD%BF%E7%94%A8%E5%8F%8A%E7%88%AC%E5%8F%96LOL%E4%BF%A1%E6%81%AF/)记录了爬取 lol.qq.com 获取英雄联盟数据及英雄皮肤原画的过程。第一次使用 scrapy 后，了解了大致的爬取流程，但在细节上（例如防 ban 策略，奇怪数据处理）没太在意，处于编码第一阶段（能跑就行）。

中间学了半个月的 Qt5 和 pygame，（没学出个什么样子，了解了大致概念，翻指南能上手了），之后，看到 github 中早期 fork 了一个库，airingursb 写的[bilibili-user](https://github.com/airingursb/bilibili-user)，深有所悟，在此先感谢他的源码及他的开源精神。

但最近一段时间，BiliBili 的网站结构有了些许的变化，我就尝试着用 scrapy 重写这个功能，以只修改 item 的方式保证这个爬虫的生命（理论上，更换 item 对应的 xpath 位置就可以应对页面元素更改）。并在此基础上增加一些防 ban 策略，深化对爬虫的编写能力，以及应对可能过大的数据处理任务（单纯的构造 url，截止 5 月 3 日，b 站已经有了 323000449 账号详情界面，之前的 lol 爬虫上千条数据就把路由器撑爆了，这次可能要应付 3 亿条数据）。完整代码可见[bilibili-user-scrapy](https://github.com/halysl/bilibili-user-scrapy)

## 二、爬虫设计全思路

### 1、目标网站

[账户详情页](https://space.bilibili.com/id/#/)

### 2、爬取内容:

- 1. uid 用户id，int
- 2. mid 用户id，str
- 3. name 用户姓名，str
- 4. sex 用户性别，str
- 5. regtime 用户注册时间，str
- 6. birthday 用户生日，str
- 7. place 用户住址，str
- 8. fans 用户粉丝数，int
- 9. attention 用户关注数，int
- 10. level 用户等级，int

### 3、技术：scrapy，splash，docker，mysql

### 4、难点

- 1. 数据库设计及数据插入
- 2. js 页面数据的获取
- 3. 特殊数据的处理
- 4. 防 ban 策略

## 三、环境搭建

### 1、开发语言：python v3.6.5

### 2、开发语言环境：anaconda v1.6.9 （非必须，但这是一个好习惯）

### 3、docker 安装

[deepin 下安装 docker](https://wiki.deepin.org/index.php?title=Docker&oldid=1649)
[其他系统安装 docker](https://yeasy.gitbooks.io/docker_practice/content/install/)

### 4、splash

[安装方法](http://splash.readthedocs.io/en/stable/install.html)

### 5、一些第三方库：

```shell
# scrapy库
conda install Scrapy
# scrapy_splash库
conda install scrapy_splash
# pymysql库（conda无法安装，迷）
pip3 install pymysql
```

### 6、mysql

[MySQL 安装](http://www.runoob.com/mysql/mysql-install.html))

## 四、爬虫设计

只需要一个爬虫就 ok 了。

### 1、定义 item

打开 items.py，添加代码：

```python
import scrapy

class BilibiliUserScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # coins = scrapy.Field()
    # friend = scrapy.Field()
    # exp = scrapy.Field()
    uid = scrapy.Field() # int id
    mid = scrapy.Field() # str id
    name = scrapy.Field()
    sex = scrapy.Field()    
    regtime = scrapy.Field()
    birthday = scrapy.Field()
    place = scrapy.Field()
    fans = scrapy.Field()    
    attention = scrapy.Field()
    level = scrapy.Field()    
```

注释部分的内容，由于隐私不可见，暂时无法获取。

### 2、设计 mysql 数据库及表
这里不在赘述如果有 mysql 建表，更多 mysql 可见[MySQL教程](http://www.runoob.com/mysql/mysql-tutorial.html)。

这里只需要知道我的数据库配置即可。

```
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'bilibili'       #数据库名字，请修改
MYSQL_USER = 'light'            #数据库账号，请修改 
MYSQL_PASSWD = '123456'         #数据库密码，请修改

MYSQL_PORT = 3306 

tablename:bilibili_user_info
```

### 3、编写 pipeline

pipelines 是对 spider 爬取到的 item 进行处理的过程，在这个爬虫中，我们需要对获得的数据进行转码并储存在 mysql 数据库中。记得将 BilibiliUserScrapyPipeline 添加到配置文件 settings.py 中。

```python
import pymysql
from scrapy import log

from bilibili_user_scrapy import settings
from bilibili_user_scrapy.items import BilibiliUserScrapyItem

class BilibiliUserScrapyPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""select * from bilibili_user_info where uid=%s""", item['uid'])
            ret = self.cursor.fetchone()
            if ret:
                self.cursor.execute(
                    """update bilibili_user_info set 
                    mid=%s,name=%s,sex=%s,
                    regtime=%s,birthday=%s,place=%s,
                    fans=%s,attention=%s,level=%s 
                    where uid=%s""",
                    (item["mid"],
                     item["name"],
                     item["sex"],
                     item["regtime"],
                     item["birthday"],
                     item["place"],
                     item["fans"],
                     item["attention"],
                     item["level"],
                     item["uid"]))
            else:
                self.cursor.execute(
                    """insert into bilibili_user_info(uid,mid,name,sex,regtime,birthday,
                    place,fans,attention,level)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (item['uid'],
                     item["mid"],
                     item["name"],
                     item["sex"],
                     item["regtime"],
                     item["birthday"],
                     item["place"],
                     item["fans"],
                     item["attention"],
                     item["level"]))
            self.connect.commit()
        except Exception as error:
            log.msg(error)
            print("error",error)
        return item
```

简单粗暴，先连接数据库，然后查询数据库，若存在则更新，不存在则插入。

4、编写spider

```python
# -*-coding:utf-8 -*-
import pymysql
import re
import sys
import random
import time
from imp import reload
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from bilibili_user_scrapy.items import BilibiliUserScrapyItem

reload(sys)

# 获取随机 user_agent
def LoadUserAgents(uafile):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    # random 的序列随机混合方法
    random.shuffle(uas)
    return uas

ua_list = LoadUserAgents("user_agents.txt")
# 默认 header
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}


# 主爬虫类
class BILIBILIUserSpider(Spider): 

    name = "bilibili_user_scrapy"

    start_urls = []
    # 截止 2018/5/2 日，B站注册账号数量
    start = 1
    end = 323000449

    # 构造 url，根据机能分批爬取，未进行分布式爬虫    
    for i in range(2000, 100000):
        url = "https://space.bilibili.com/"+str(i)+"/#/"
        start_urls.append(url)


    def start_requests(self):
        for url in self.start_urls:
            time.sleep(1)
            # 随机 headers
            headers = {'User-Agent':random.choice(ua_list),
               'Referer':'http://space.bilibili.com/'+str(random.randint(9000,10000))+'/'}
            yield SplashRequest(url=url, callback=self.parse, args={'wait':0.5},
                endpoint='render.html',splash_headers=headers,
                )

    def parse(self, response):
        # 爬虫 item 类
        item = BilibiliUserScrapyItem()

        #一些常规的元素抓取
        attention = response.xpath("//*[@id=\"n-gz\"]/text()").extract_first()
        fans = response.xpath("//*[@id=\"n-fs\"]/text()").extract_first()
        level = response.xpath("//*[@id=\"app\"]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[1]/a[1]/@lvl").extract_first()
        # 由于未知的原因，部分页面无法正确加载某些元素
        # 当元素为 None 时，将其设置为 ‘null’
        # 但 uid 特殊，必须存在，所以从 response.url 中截取
        uid = response.url[27:-3]
        # uid = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[1]/span[2]/text()").extract_first()
        sex = response.xpath("//*[@id=\"h-gender\"]/@class").extract_first()

        # 小数值直接 int
        item['attention'] = int(attention)
        item['level'] = int(level)

        item['birthday'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[1]/span[2]/text()").extract_first()
        item['name'] = response.xpath("//*[@id=\"h-name\"]/text()").extract_first().strip()
        item['place'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[2]/a/text()").extract_first()
        item['regtime'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[2]/span[2]/text()").extract_first()

        item['uid'] = int(uid)
        item['mid'] = uid
        # 对性别进行处理
        if len(sex.split(" ")) == 3:
            item['sex'] = sex.split(" ")[2]
        else:
            item['sex'] = 'null'

        # 对地址进行处理
        if item['place'] is None:
            item['place'] = "null"        

        # 对 fans 进行处理
        if "万" in fans:
            item['fans'] = int(float(fans[:-3])*10000)
        else:
            item['fans'] = int(fans)

        # 对生日进行处理
        if item['birthday'] is None:
            item['birthday'] = "null"
        else:
            item['birthday'] = item['birthday'].strip()

        # 对注册时间进行处理
        if item['regtime'] is None:
            item['regtime'] = "null"
        else:
            item['regtime'] = item['regtime'].strip()

        # 这些项暂时无法直接从界面获取
        #item['coins'] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div[1]/a/span[2]/text()").extract_first()
        #item['friend'] = item["fans"]
        #item['exp'] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[3]/a/div/div[3]/div/text()").extract_first()

        yield item
```

这个爬虫的设计思路如下： 

- 1、设置 user_agents（放在第五节描述） 
- 2、设置 proxy（放在第五节描述） 
- 3、构造 url 
- 4、获取数据 
- 5、对特殊数据进行处理 
- 6、返回到 pipeline，再插入到数据库中

### 5、setting

```python
# ip 代理池
DOWNLOADER_MIDDLEWARES = {
    'bilibili_user_scrapy.middlewares.ProxyMiddleware': 543,
}

ITEM_PIPELINES = {
    'bilibili_user_scrapy.pipelines.BilibiliUserScrapyPipeline': 300,
}

# 配置 mysql
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'bilibili'         #数据库名字，请修改
MYSQL_USER = 'light'             #数据库账号，请修改 
MYSQL_PASSWD = '123456'         #数据库密码，请修改

MYSQL_PORT = 3306               #数据库端口

# splash 配置
SPLASH_URL = 'http://172.17.0.2:8050/'  # splash在docker下的url
# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
# 爬虫中间件
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'  # 去重过滤器（必须）
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage' # 使用 http 缓存
```

## 五、反爬虫策略

### 1、设置睡眠

虽然 scrapy 自带多线程异步处理，但是在代码中添加睡眠方法可能会有效。 

```python
# 在 spider 文件中添加 
import time 
time.sleep(2)
```

### 2、设置 user_agent

ua 是一个网站识别用户使用终端的手段，scrapy 的默认 ua 就是 scrapy，一般网站可以直接禁止 scrapy 的 header 进行访问，在这个爬虫中，我们先构造一个默认 header 头，然后从 ua 文件中随机获得新的 ua，和原先的 header 结合，形成新的 header 进行防 ban 访问。

### 3、设置 referer

这个 referer 是 header 的一个属性，它意味着访问来源是什么，但这只是个辅助，并不确定是否真实（可能由于网络重定向或者其他原因，导致 referer 不准确），但我们可以利用改变 referer 的值以使得后端服务器觉得是不同的用户在访问。利用 random 方法构造不同的 referer。

### 4、设置代理

这个方法可能是最有效的防 ban 策略，但却不容易实现。首先免费的代理不多，而且质量良莠不济，过度使用代理可能会无法正常访问（你能找到的代理早被人玩过多少次了……）。如果数据量小的话就不使用代理，前面三项做好就没什么问题，数据量大的话可以考虑购买代理（商业爬虫应该是有收费代理用的吧……）。

在scrapy中使用代理不麻烦，在 middlewares.py 中添加一个代理类，再将这个类添加到 settings.py 中就可以了。

middlewares.py文件中：

```python
# ip 代理
class ProxyMiddleware(object):
    proxies = {
        'http':'http://140.240.81.16:8888',
        'http':'http://185.107.80.44:3128',
        'http':'http://203.198.193.3:808',
        'http':'http://125.88.74.122:85',
        'http':'http://125.88.74.122:84',
        'http':'http://125.88.74.122:82',
        'http':'http://125.88.74.122:83',
        'http':'http://125.88.74.122:81',
        'http':'http://123.57.184.70:8081'
        }

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(proxies)
```

settings.py文件中：

```python
DOWNLOADER_MIDDLEWARES = {
    'bilibili_user_scrapy.middlewares.ProxyMiddleware': 543,
}
```

## 六、反思

- 1、实际开发时间两天，但是 commit 记录有七天，这是为什么呢？因为刚开头遇到了一个“非常低级”的错误，写代码时迷迷糊糊的，直接根据问题报告去查资料，找了很多，不得其解，觉得这可能是框架的 bug，只有看源码才能解决了，然后就去干其他事了。五天后，我读了《代码整洁之道：程序员的自我修养》后重新审视这个问题，发现其实是在 spider 文件中错误的定义了 item 类型，直接定义为了默认列表类，而不是自己设置的 item 类。事后想到这个错误都觉得难堪，反思一下：发困的时候不要写东西，心里有事的时候要先调整好在编码。

- 2、在处理特殊数据的时候有些随意了，再加上未知 bug，造成最后获得的数据真实有效的可能只有一半。按道理说，用户详情页面的元素应该都是一致的，但就是出现了无法获取的情况，单纯的以https://space.bilibili.com/1/#/ 和 https://space.bilibili.com/2/#/ 为例，粉丝数量的元素在 xpath 上位置一样，但就是无法获得正确数据，返回 None。怀疑可能是 splash 配置的问题（毕竟这些元素都是 js 载入的）。

- 3、虽然获取数据量少，但每次获取都是进行一次 http 连接，所以还是没能力跑 3 亿条数据，这需要太多的时间，如果可以的话，可以尝试分布式爬虫。

- 4、下一步就是用 numpy 等库对获得的数十万条数据进行统计处理。
