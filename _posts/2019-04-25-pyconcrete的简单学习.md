---
layout: post
title: pyconcrete的简单学习
categories: [Python, Python模块]
description: pyconcrete的简单学习
keywords: python, 代码加密
---

# pyconcrete 的简单学习
 
 [pypi-pyconcrete 0.12.1](https://pypi.org/project/pyconcrete/#description)

(个人感觉用这个库加密 python 程序的人不多。。。)

（我在 MacOS python3.7.3 下又无法安装了）

pyconcrete 是一个 python 文件加密库，它可以将常规的 .py 文件或 .pyc 文件加密为 .pye 文件，这样就无法直接打开源代码，避免了源代码的泄漏，也为 python 项目商用提供了解决方案。

该库在国内用的人不多，中文教程也少得可怜，Google 首页就两篇中文相关内容，一篇还是认识的人写的，一篇是对 GitHub 上对应项目的自述文件进行机翻，这里参考的是[Falldog/pyconcrete](https://github.com/Falldog/pyconcrete)。

## 安装

尽量不要使用 pip 安装！！！

我的几次安装经历，通过 pip 安装总是会出现各种各样的问题，可以试着通过

```shell
$ pip install pyconcrete --egg --install-option="--passphrase=<your passphrase>"
```

进行安装，或者下载[源代码](https://pypi.org/project/pyconcrete/)，进行安装，这可能是最快的安装方式。

## 保护你的 python 代码工作流

- 在 `your_script.py` 首行 `import pyconcrete`
- pyconcrete 将会自动和其他模块挂钩
- 当 `your_script.py` 开始导入其他模块，pyconcrete 首先会尝试寻找 `MODULE.pye`，然后通过 \_pyconcrete.pyd 对`MODULE.pye` 进行解密

执行加密后的文件。

## 加密

- 只支持 AES 128 位加密
- 通过 OpenAES 加解密

## 用法

### 完整加密

- 将所有以 `.py` 结尾的文件转为 `.pye`。

```shell
$ pyconcrete-admin.py compile --source=<your py script>  --pye
$ pyconcrete-admin.py compile --source=<your py module dir> --pye
```

- 移除所有的 `*.py` 和 `*.pyc` 文件，或者将所有的 `*.pye` 文件移动到其他的文件夹
- `main.py` 文件也会被加密为 `main.pye`，它无法被普通的 python 直接调用。必须使用 pyconcrete 来启动 `main.pye`。

```shell
pyconcrete main.pye
src/*.pye  # your libs
```

### 部分加密

将库文件被部分加密。

- 下载 将被加密的库，然后通过 setup.py 进行安装。

```shell
$ python setup.py install \
  --install-lib=<your project path> \
  --install-scripts=<where you want to execute pyconcrete-admin.py and pyconcrete(exe)>
```

- 将 pyconcrete 在主程序中导入
  - 推荐项目依赖

```python
main.py       # import pyconcrete and your lib
pyconcrete/*  # put pyconcrete lib in project root, keep it as original files
src/*.pye     # your libs
```
