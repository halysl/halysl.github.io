# pyconcrete的简单学习

pyconcrete 是一个 python 文件加密库，它可以将常规的 .py 文件或 .pyc 文件加密为 .pye 文件，这样就无法直接打开源代码，避免了源代码的泄漏，也为 python 项目商用提供了解决方案。

该库在国内用的人不多，中文教程也少得可怜，Google首页就两篇中文相关内容，一篇还是认识的人写的，这里参考的是[pyconcrete, 保护 python 脚本，将它的加密为. pye 并在导入时解密](https://www.helplib.com/GitHub/article_133608)。

## 安装

尽量不要使用 pip 安装！！！

我的几次安装经历，通过 pip

pyconcrete-admin.py compile --source=[] --pye