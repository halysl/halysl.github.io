# Cli 模块的学习

望文生义，cli 模块是一种简单、快速且有趣的通过 go 构建命令行工具的包。它的[源码地址](https://github.com/urfave/cli)。它的 [v2 帮助文件](https://github.com/urfave/cli/blob/master/docs/v2/manual.md)。

## 获取和导入

```sh
$ GO111MODULE=on go get github.com/urfave/cli/v2
```

```go
import (
  "github.com/urfave/cli/v2" // imports as package "cli"
)
```

