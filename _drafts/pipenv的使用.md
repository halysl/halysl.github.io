https://docs.pipenv.org/en/latest/

# Pipenv 指令解释

pipenv 用起来挺方便的，但总是会遇到各种奇怪的问题。有些时候不如 pip，但是pip本身也会有很多坑。

从名字来看，pipenv 解决了以下问题：

- 不用再单独使用pip和virtualenv, 现在它们合并在一起了
- 不用再维护requirements.txt, 使用Pipfile和Pipfile.lock来代替
- 可以使用多个python版本(python2和python3)
- 在安装了pyenv的条件下，可以自动安装需要的Python版本

# 安装 pipenv

- MacOSX: `brew install pipenv`
- Linux: `pip install pipenv`
- Fedora: `sudo dnf install pipenv`

# 用户证明

> David Gang—
>> This package manager is really awesome. For the first time I know exactly what my dependencies are which I installed and what the transitive dependencies are. Combined with the fact that installs are deterministic, makes this package manager first class, like cargo.

> Justin Myles Holmes—
>> Pipenv is finally an abstraction meant to engage the mind instead of merely the filesystem.

# 基础概念

- 从0开始，自动创建一个虚拟环境
- 如果没有指定参数，那么创建环境时会自动安装文件 `Pipfile` 里的 `[packages]` 里提到的包
- 初始化一个 Python3 虚拟环境，执行 `$ pipenv --three`
- 初始化一个 Python2 虚拟环境，执行 `$ pipenv --two`
- 否则的话，会根据系统里的 Python 环境创建一个一样的环境

# 其他指令

- `graph` 将显示已安装项的依赖关系
- `shell` 将生成虚拟环境激活的shell，可以通过 `exit` 退出虚拟环境
- `run` 将会通过虚拟环境的程序执行命令，并且转发参数，例如：`$ pipenv run python or` `$ pipenv run pip freeze`
- `check` 检查安全漏洞并声明当前环境是否满足PEP 508要求

# Pipenv 使用

## pipenv

```shell
pipenv [OPTIONS] COMMAND [ARGS]...
```

### Options

--where 展示项目目录信息

--venv 展示虚拟环境目录

--py 展示 python 程序位置

--envs 展示环境变量

--rm 移除当前虚拟环境

--bare 最小化输出信息

--completion 命令自动补全

--man 展示帮助信息

--support 输出用于 GitHub 问题的诊断信息

--site-packages, --no-site-packages 创建环境时是否添加系统已有的包

--python <python> 指定特定版本的 python 的路径来创建虚拟环境

--three, --two 使用 python2/python3 来创建虚拟环境

--clear 清空缓存(pipenv, pip, and pip-tools).

-v, --verbose 完整输出模式

--pypi-mirror <pypi_mirror> 指定pypi镜像源

--version 展示 pipenv 版本

## check

检查安全漏洞并声明当前环境是否满足PEP 508要求

`pipenv check [OPTIONS] [ARGS]...`

### Options

--unused <unused> 给定代码路径，显示可能未使用的依赖项

-i, --ignore <ignore> 在安全检查期间忽略指定的漏洞

--python <python> 指定使用特定版本的 python

--three, --two 使用 python2/python3 来创建虚拟环境

--clear 清理缓存(pipenv, pip, and pip-tools).

-v, --verbose 详细输出模式

--pypi-mirror <pypi_mirror> 指定pypi镜像源

--system 使用系统pip进行管理

### Arguments

ARGS 可选参数

## clean

卸载所有不在 Pipfile.lock 中的包。

`pipenv clean [OPTIONS]`

### Options

--bare

--dry-run 只输出不必要的包

-v, --verbose

--three, --two

--python <python>

## graph

展示当前安装包的依赖关系。

`pipenv graph [OPTIONS]`

### Options

--bare

--json 输出json格式依赖信息

--json-tree 输出json树格式依赖信息

--reverse 反转依赖图

## install

安装三方包，并记录到Pipfile，或者从Pipifile中安装包。

`pipenv install [OPTIONS] [PACKAGES]...`

### Options

--system 使用系统的pip安装

-c, --code \<code\> 通过import语句发现包并安装包（不要用引号）

--deploy 如果Pipfile.lock已过期，或者Python版本错误，则中止安装

--site-packages, --no-site-packages

--skip-lock 安装包后不进行锁定

-e, --editable <editable> 可编辑的python包URL或路径，通常用于VCS存储库

--ignore-pipfile 安装包时忽略Pipfile，使用Pipfile.lock

--selective-upgrade 更新指定的包

-r, --requirements <requirements> 从requirements.txt发现包，并安装

--extra-index-url <extra_index_url> 从额外的Pypi库里找到需要的包（例如公司内部的Pypi源）

-i, --index <index>

--sequential 一次一个地安装依赖项，而不是同时安装

--keep-outdated 保持在Pipfile.lock中更新过时的依赖项

--pre 允许预发布的包

-d, --dev 将包安装在开发环境中

--python <python>

--three, --two

--clear 清理缓存 (pipenv, pip, and pip-tools).

-v, --verbose

--pypi-mirror <pypi_mirror> 指定pypi镜像

### Arguments

PACKAGES 包名

### Environment variables

- PIPENV_SKIP_LOCK 默认提供 --skip-lock 选项
- PIP_EXTRA_INDEX_URL 默认提供 --extra-index-url 选项
- PIP_INDEX_URL 默认提供 -i 选项
