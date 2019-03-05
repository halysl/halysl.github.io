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

## 保护你的 python 代码工作流

- 在 `your_script.py` 首行 `import pyconcrete`
- pyconcrete 将会自动和其他模块挂钩
- 当 `your_script.py` 开始倒入其他模块，pyconcrete 首先会尝试寻找 `MODULE.pye`，然后通过 \_pyconcrete.pyd 对`MODULE.pye` 进行解密

执行加密后的文件。

and execute decrypted data (as .pyc content)
encrypt & decrypt secret key record in _pyconcrete.pyd (like DLL or SO) the secret key would be hide in binary code, can't see it directly in HEX view
pyconcrete-admin.py compile --source=[] --pye


## 加密

- 只支持 AES 128 位加密
- 通过 OpenAES 加解密

Installation
need to input your passphrase create secret key for encrypt python script.
same passphrase will generate the same secret key
installation will add pyconcrete.pth into your site-packages for execute sitecustomize.py under pyconcrete which will automatic import pyconcrete
pip
$ pip install pyconcrete
If you only execute pip install will not display any prompt(via stdout) from pyconcrete. Installation will be blocked and waiting for user input passphrase twice. You must input passphrase for installation continuously.

$ pip install pyconcrete --egg --install-option="--passphrase=<your passphrase>"
pyconcrete installed as egg, if you want to uninstall pyconcrete will need to manually delete pyconcrete.pth.

source
get the pyconcrete source code
$ git clone <pyconcrete repo> <pyconcre dir>
install pyconcrete
$ python setup.py install
Usage
Full encrypted
convert all of your .py to *.pye
$ pyconcrete-admin.py compile --source=<your py script>  --pye
$ pyconcrete-admin.py compile --source=<your py module dir> --pye
remove *.py *.pyc or copy *.pye to other folder
main.py encrypted as main.pye, it can't be executed by normal python. You must use pyconcrete to process the main.pye script. pyconcrete(exe) will be installed in your system path (ex: /usr/local/bin)
pyconcrete main.pye
src/*.pye  # your libs
Partial encrypted (pyconcrete as lib)
download pyconcrete source and install by setup.py
$ python setup.py install \
  --install-lib=<your project path> \
  --install-scripts=<where you want to execute pyconcrete-admin.py and pyconcrete(exe)>
import pyconcrete in your main script
recommendation project layout
main.py       # import pyconcrete and your lib
pyconcrete/*  # put pyconcrete lib in project root, keep it as original files
src/*.pye     # your libs
Test
test all case
$ ./pyconcrete-admin.py test
test all case, setup TEST_PYE_PERFORMANCE_COUNT env to reduce testing time
$ TEST_PYE_PERFORMANCE_COUNT=1 ./pyconcrete-admin.py test
Example
Django with pyconcrete

Building on Linux
Python 3.7 - fix Ubuntu 14.04 build error
x86_64-linux-gnu-gcc: error: unrecognized command line option `-fstack-protector-strong`
Reference by Stackoverflow solution

you should install gcc-4.9 first
symlink /usr/bin/x86_64-linux-gnu-gcc to gcc-4.9
build pycocnrete again
rollback symlink
Building on Windows
Python 2.7 - Visual Studio 2008
https://www.microsoft.com/en-us/download/details.aspx?id=44266

Open VS2008 Command Prompt
set DISTUTILS_USE_SDK=1
set SET MSSdk=1
create distutils.cfg and put inside
[build]
compiler=msvc
Python 3.5, 3.6, 3.7 - Visual Studio 2015
MSVC 2015 Build Tools

Document

make sure setuptools >= 24.0

python -c 'import setuptools; print(setuptools.__version__)'
Open VS2015 Build Tools Command Prompt

set DISTUTILS_USE_SDK=1

setenv /x64 /release or setenv /x86 /release

Reference
https://matthew-brett.github.io/pydagogue/python_msvc.html https://github.com/cython/cython/wiki/CythonExtensionsOnWindows

Announcement
pyconcrete is an experimental project, there is always a way to decrypt .pye files, but pyconcrete just make it harder.