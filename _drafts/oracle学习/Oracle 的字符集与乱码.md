# Oracle 的字符集与乱码

最近有个需求，通过 python 处理数据，然后将数据存入到 oracle 11g 库中，中间遇到了一些编码相关的问题。由于可以直接登录上 oracle 所在的服务器，所以在本机上的 sqlplus 属于客户端，只是直接连接了本机，既然这样的话，就需要配置 NLS_LANG。

很多文章只会提到，将 NLS_LANG 配置改成 `SIMPLIFIED CHINESE_CHINA.AL32UTF8`，或者通过 os.environ 进行设置，这确实可以解决问题，但真正的原因并不是改个这个就完事了。

其实 oracle 数据库已经做了很多的字符转换工作，只要配置得当，那么数据就能正常存入，查询，转码的过程中也不会出问题，所以就必须知道，字符具体会在那些地方变更。

下面的这篇文章解决了我的问题，也让编码问题更为清晰。

## 字符集的作用

字符集问题一直叫人头疼，究其原因还是不能完全明白其运作原理。

在整个运行环节中，字符集在 3 个环节中发挥作用：

- 软件在操作系统上运作时的对用户的显示，此时采用操作系统定义的字符集进行显示。我们在系统 I/O 编程的时候经常要指定字符集，C# 中的 `Text.Encoding=Encoding.Default` 实际上就是告诉编译器，文本使用系统定义的默认字符集进行编码。sqlplus 也是运行在操作系统上的软件，当然要使用系统所指定的字符集对外显示内容。

- 数据向 Oracle 服务端传送前的通告。也就是 sqlplus 告诉服务器现在使用的字符集是什么。

- 数据流到达服务器后，按照服务器所使用的字符集自动翻译客户端的数据，然后存储进系统。

在客户端 sqlplus 和服务端传送数据，数据会按照服务端字符集进行翻译，这个过程是自动完成的不需要人工干预。任何时候，oracle 服务端总是按照自己的字符集设置来存取数据，`客户端要想正确显示从服务端读取到的数据，也需要按照本地的字符集设置进行翻译，这个过程也是自动的。`（重点是 `按照本地的字符集设置`）

服务器端需要采用合适的字符集进行数据存储，这个很容易理解，ASCII 字符集没办法用来存储中文汉字，因为它根本没有描述汉字所需要的编码空间。

问题常常存在于客户端与服务端通讯的过程中，sqlplus 作为运行在操作系统上的软件，无论是显示还是通讯，`必然使用操作系统所使用的字符集设置`。无论 sqlplus 设置的字符集，作用只有一个，那就是通告服务器端，为相互之间的字符集翻译做准备。

客户端的字符集设置是在NLS_LANG环境变量中设置的，客户读端的字符集可以和oracle客户端设置得不一样（本来人家就是自动翻译的），但是`客户端字符集一定要和操作系统设置的字符集相匹配`！（后面会有匹配表）

## 出现编码错误的原因

考虑一下，sqlplus 使用的是操作系统的字符集定义在显示和发送数据（假设是 TYPE_A），却告诉 oracle 服务器自己使用的字符集是 TYPE_B，oracle 服务器会怎么办？它会将客户端发送过来的 TYPE_A 数据当作 TYPE_B 字符集格式用自身的 TYPE_C 字符集进行翻译，然后再存储进系统，这就形成了乱码。反向的过程类似，Oracle服务器发出的数据格式没有疑问是 TYPE_C，但是客户端软件认为自己使用的编码是 TYPE_B 并进行了翻译，交给操作系统用 TYPE_A 字符集总的字符/编码映射关系进行翻译显示，最终导致了无法正确显示。

一个现实的例子：RHEL5.8 操作系统安装了中文支持包以后，所有的语言环境都被设置成了 zh_CN.UTF-8（通过 LANG 环境变量可知，也可通过 locale 命令查到）,数据库服务器所使用的字符集为 ZHS16GBK,很明显，这两者不一致，sqlplus 在没有设置 NLS_LANG 环境变量时，与数据库保持一致，此时，从服务端取得的数据不需要翻译，被 sqlplus 读取并用 zh_CN.UTF-8 的字符/编码映射关系进行翻译显示，所有的汉字变成了“？”。

根据上面的分析，要解决这一问题，要把 sqlplus 的字符集设置成和操作系统一致即可，操作系统设置的是 zh_CN.UTF-8，但在 .bash_profile 里面还不能直接将 NLS_LANG 设置为 zh_CN.UTF-8，因为这个 zh_CN.UTF8 是字符集的 localeID 而不是字符集的名称，真正的名称叫 SIMPLIFIED CHINESE_CHINA.AL32UTF8，如果设置成 zh_CN.UTF8，oracle 会报`ORA-12705: Cannotaccess NLS data files or invalid environmentspecified` 错误。在 .bash_profile 里面加入 `export NLS_LANG="SIMPLIFIEDCHINESE_CHINA.AL32UTF8";` 问题就解决了。

## locale ID 与字符集名称的对应关系

| Language               | Locale ID         | NLS_LANG                                 |
| ---------------------- | ----------------- | ---------------------------------------- |
| English (American)     | en_US.UTF-8       | AMERICAN_AMERICA.AL32UTF8                |
| English (American)     | en_US.ISO-8859-1  | AMERICAN_AMERICA.WE8ISO8859P1            |
| English (American)     | en_US.ISO-8859-15 | AMERICAN_AMERICA.WE8ISO8859P15           |
| English (Australian)   | en_AU.UTF-8       | ENGLISH_AUSTRALIA.AL32UTF8               |
| English (Australian)   | en_AU.ISO-8859-1  | ENGLISH_AUSTRALIA.WE8ISO8859P1           |
| English (Australian)   | en_AU.ISO-8859-15 | ENGLISH_AUSTRALIA.WE8ISO8859P15          |
| English (British)      | en_GB.UTF-8       | ENGLISH_UNITED KINGDOM.AL32UTF8          |
| English (British)      | en_GB.ISO-8859-1  | ENGLISH_UNITED KINGDOM.WE8ISO8859P1      |
| English (British)      | en_GB.ISO-8859-15 | ENGLISH_UNITEDKINGDOM.WE8ISO8859P15      |
| English (Ireland)      | en_IE.UTF-8       | ENGLISH_IRELAND.AL32UTF8                 |
| English (Ireland)      | en_IE.ISO-8859-1  | ENGLISH_IRELAND.WE8ISO8859P1             |
| English (Ireland)      | en_IE.ISO-8859-15 | ENGLISH_IRELAND.WE8ISO8859P15            |
| German                 | de_DE.UTF-8       | GERMAN_GERMANY.AL32UTF8                  |
| German                 | de_DE.ISO-8859-1  | GERMAN_GERMANY.WE8ISO8859P1              |
| German                 | de_DE.ISO-8859-15 | GERMAN_GERMANY.WE8ISO8859P15             |
| French                 | fr_FR.UTF-8       | FRENCH_FRANCE.AL32UTF8                   |
| French                 | fr_FR.ISO-8859-1  | FRENCH_FRANCE.WE8ISO8859P1               |
| French                 | fr_FR.ISO-8859-15 | FRENCH_FRANCE.WE8ISO8859P15              |
| Italian                | it_IT.UTF-8       | ITALIAN_ITALY.AL32UTF8                   |
| Italian                | it_IT.ISO-8859-1  | ITALIAN_ITALY.WE8ISO8859P1               |
| Italian                | it_IT.ISO-8859-15 | ITALIAN_ITALY.WE8ISO8859P15              |
| Spanish                | es_ES.UTF-8       | SPANISH_SPAIN.AL32UTF8                   |
| Spanish                | es_ES.ISO-8859-1  | SPANISH_SPAIN.WE8ISO8859P1               |
| Spanish                | es_ES.ISO-8859-15 | SPANISH_SPAIN.WE8ISO8859P15              |
| Spanish (Mexico)       | es_MX.UTF-8       | MEXICAN SPANISH_MEXICO.AL32UTF8          |
| Spanish (Mexico)       | es_MX.ISO-8859-1  | MEXICAN SPANISH_MEXICO.WE8ISO8859P1      |
| Spanish (Mexico)       | es_MX.ISO-8859-15 | MEXICANSPANISH_MEXICO.WE8ISO8859P15      |
| Portuguese (Brazilian) | pt_BR.UTF-8       | BRAZILIANPORTUGUESE_BRAZIL.AL32UTF8      |
| Portuguese (Brazilian) | pt_BR.ISO-8859-1  | BRAZILIANPORTUGUESE_BRAZIL.WE8ISO8859P1  |
| Portuguese (Brazilian) | pt_BR.ISO-8859-15 | BRAZILIANPORTUGUESE_BRAZIL.WE8ISO8859P15 |
| Japanese               | ja_JP.EUC-JP      | JAPANESE_JAPAN.JA16EUC                   |
| Japanese               | ja_JP.UTF-8       | JAPANESE_JAPAN.AL32UTF8                  |
| Korean                 | ko_KR.EUC-KR      | KOREAN_KOREA.KO16KSC5601                 |
| Korean                 | ko_KR.UTF-8       | KOREAN_KOREA.AL32UTF8                    |
| Chinese (simplified)   | zh_CN.GB18030     | SIMPLIFIEDCHINESE_CHINA.ZHS32GB18030     |
| Chinese (simplified)   | zh_CN.UTF-8       | SIMPLIFIED CHINESE_CHINA.AL32UTF8        |
| Chinese (traditional)  | zh_TW.BIG5        | TRADITIONALCHINESE_TAIWAN.ZHT16BIG5      |
| Chinese (traditional)  | zh_TW.UTF-8       | TRADITIONAL CHINESE_TAIWAN               |


步骤可以归纳为：

1. 找到操作系统使用的字符集，并按上表找到对应的字符集名称。
2. 修改客户端软件的字符集 NLS_LANG 环境变量设置。

其中第二步可以通过 os.environ 改变，原理一致，这样数据传到服务端就会自动处理。

## 不同平台的一些细节

### Windows（ 如简体系统为：ZHS16GBK，繁体系统为：MSWIN950 ）

1、设置session变量

- 常用中文字符集：`set NLS_LANG=SIMPLIFIED CHINESE_CHINA.ZHS16GBK`
- 常用unicode字符集: `set NLS_LANG=american_america.AL32UTF8`

2、可以通过修改注册表键值永久设置

- HKEY_LOCAL_MACHINE/SOFTWARE/ORACLE/HOMExx/NLS_LANG

3、设置环境变量

- NLS_LANG=SIMPLIFIED CHINESE_CHINA.ZHS16GBK
- NLS_LANG=american_america.AL32UTF8

### Unix/Linus:

1、设置session变量

- 常用unicode字符集: `export NLS_LANG=american_america.AL32UTF8`
- 常用中文字符集: `export NLS_LANG="Simplified Chinese_china".ZHS16GBK`

2、设置环境变量

可以编辑 .bash_profile 文件进行永久设置

```shell
vi .bash_profile
NLS_LANG="Simplified Chinese_china".ZHS16GBK
export NLS_LANG
```

使 bash_profile 设置生效

```shell
source .bash_profile
```

### 其他

1、查看sqlplus客户编码：

```echo $NLS_LANG```

2、查看系统编码：

```locale```

3、查看数据库字符集，执行如下查询:

```select userenv('language') from dual;```

## 转载信息

- 作者：hcling97 
- 地址：http://blog.sina.com.cn/hcling97
