# api doc的使用和部署

做web应用，总绕不开前后端数据接口的对接。如何才能写出一份简单、易于维护的api文档？

这时候api doc就出现了。

apidoc 是一个简单的 RESTful API 文档生成工具，它从代码注释中提取特定格式的内容，生成文档。 目前支持支持以下语言：C#、C/C++、D、Erlang、Go、Groovy、Java、JavaScript、Pascal/Delphi、 Perl、PHP、Python、Ruby、Rust、Scala 和 Swift。

以下的使用示例以python语言为主。

以下是官网[APIDOC](http://apidocjs.com/)。

## 安装

`npm install apidoc -g`

## 设置apidoc配置

在项目文件夹根目录创建文件apidoc.json文件。

里面的内容是对当前项目的描述。

其中header或者footer可以指向md文件，可以记录头信息和尾部信息。

```
{
  "name": "example",
  "version": "0.1.0",
  "description": "apiDoc basic example",
  "title": "Custom apiDoc browser title",
  "url" : "https://api.github.com/v1"，
  "header": {
    "title": "Overview",
    "filename": "header.md"
  },
  "footer": {
    "title": "Copyright",
    "filename": "footer.md"
  }
}
```

## 创建header.md和footer.md(非必须)

## 生成api doc

```
apidoc -i myapp/ -o apidoc/ 
-i 项目文件夹
-o apidoc文件夹
```

生成好了，就可以打开apidoc/文件夹下的index.html就可以了。

## 开始写注释