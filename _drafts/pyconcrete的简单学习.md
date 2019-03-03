# pyconcrete的简单学习

pyconcrete 是一个 python 文件加密库，它可以将常规的 .py 文件或 .pyc 文件加密为 .pye 文件，这样就无法直接打开源代码，避免了源代码的泄漏，也为 python 项目商用提供了解决方案。

该库在国内用的人不多，中文教程也少得可怜，Google首页就两篇中文相关内容，一篇还是认识的人写的，一篇是对 GitHub 上对应项目的自述文件进行机翻，这里参考的是[Falldog/pyconcrete](https://github.com/Falldog/pyconcrete)。

## 安装

尽量不要使用 pip 安装！！！

我的几次安装经历，通过 pip 安装总是会出现各种各样的问题，可以试着通过

```shell
$ pip install pyconcrete --egg --install-option="--passphrase=<your passphrase>"
```

进行安装，或者下载[源代码](https://pypi.org/project/pyconcrete/)，进行安装，这可能是最快的安装方式。

## 使用

pyconcrete-admin.py compile --source=[] --pye