---
layout: wiki
title: XML语法
categories: [XML, Sytanx]
description: XML的语法
keywords: XML, Sytanx
---

# XML

XML 指可扩展标记语言（eXtensible Markup Language）。

XML 被设计用来传输和存储数据。

## XML 和 HTML 之间的差异

XML 不是 HTML 的替代。

XML 和 HTML 为不同的目的而设计：

- XML 被设计用来传输和存储数据，其焦点是数据的内容。
- HTML 被设计用来显示数据，其焦点是数据的外观。

HTML 旨在显示信息，而 XML 旨在传输信息。

## XML 不是对 HTML 的替代

XML 是对 HTML 的补充。

XML 不会替代 HTML，理解这一点很重要。在大多数 Web 应用程序中，XML 用于传输数据，而 HTML 用于格式化并显示数据。

对 XML 最好的描述是：

*XML* 是独立于软件和硬件的信息传输工具。

```xml
<!-- 简单的例子 -->
<bookstore>
    <book category="COOKING">
        <title lang="en">Everyday Italian</title>
        <author>Giada De Laurentiis</author>
        <year>2005</year>
        <price>30.00</price>
    </book>
    <book category="CHILDREN">
        <title lang="en">Harry Potter</title>
        <author>J K. Rowling</author>
        <year>2005</year>
        <price>29.99</price>
    </book>
        <book category="WEB">
        <title lang="en">Learning XML</title>
        <author>Erik T. Ray</author>
        <year>2003</year>
        <price>39.95</price>
    </book>
</bookstore>
```

## XML 语法

XML 的语法规则很简单，且很有逻辑。

### 必须有根元素

它是所有其他元素的父元素。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>
```

### XML 声明

XML 声明文件的可选部分，如果存在需要放在文档的第一行。

```xml
<?xml version="1.0" encoding="utf-8"?>
```

### XML 元素都必须有一个关闭标签

在 HTML 中，某些元素不必有一个关闭标签;

但是，在 XML 中，省略关闭标签是非法的。所有元素都必须有关闭标签。

### XML 标签对大小写敏感

XML 标签对大小写敏感。标签 <Letter> 与标签 <letter> 是不同的。

必须使用相同的大小写来编写打开标签和关闭标签。

### XML 标签必须正确嵌套

```xml
<!-- error -->
<b><i>This text is bold and italic</b></i>

<!-- right -->
<b><i>This text is bold and italic</i></b>
```

### XML 属性值必须加引号

与 HTML 类似，XML 元素也可拥有属性（名称/值的对）。

在 XML 中，XML 的属性值必须加引号。

请研究下面的两个 XML 文档。 第一个是错误的，第二个是正确的：

```xml
<note date=12/11/2007>
<to>Tove</to>
<from>Jani</from>
</note>
```

```xml
<note date="12/11/2007">
<to>Tove</to>
<from>Jani</from>
</note>
```

### 实体引用

如果您把字符 "<" 放在 XML 元素中，会发生错误，这是因为解析器会把它当作新元素的开始。

这样会产生 XML 错误：

```xml
<message>if salary < 1000 then</message>
```

为了避免这个错误，请用实体引用来代替 "<" 字符：

```xml
<message>if salary &lt; 1000 then</message>
```

&lt;&nbsp;	<&nbsp;	less than
&gt;&nbsp;	>&nbsp;	greater than
&amp;&nbsp;	&&nbsp;	ampersand
&apos;&nbsp;	'&nbsp;	apostrophe
&quot;&nbsp;	"&nbsp;	quotation mark

## XML 元素

XML 元素指的是从（且包括）开始标签直到（且包括）结束标签的部分。

一个元素可以包含：

- 其他元素
- 文本
- 属性
- 或混合以上所有...

```xml
<bookstore>
    <book category="CHILDREN">
        <title>Harry Potter</title>
        <author>J K. Rowling</author>
        <year>2005</year>
        <price>29.99</price>
    </book>
    <book category="WEB">
        <title>Learning XML</title>
        <author>Erik T. Ray</author>
        <year>2003</year>
        <price>39.95</price>
    </book>
</bookstore>
```

在上面的实例中，<bookstore> 和 <book> 都有 元素内容，因为他们包含其他元素。<book> 元素也有属性（category="CHILDREN"）。<title>、<author>、<year> 和 <price> 有文本内容，因为他们包含文本。

### 命名规则

- 名称可以包含字母、数字以及其他的字符
- 名称不能以数字或者标点符号开始
- 名称不能以字母 xml（或者 XML、Xml 等等）开始
- 名称不能包含空格

### 命名习惯

- 使名称具有描述性。使用下划线的名称也很不错：<first_name>、<last_name>。

- 名称应简短和简单，比如：<book_title>，而不是：<the_title_of_the_book>。

- 避免 "-" 字符。如果您按照这样的方式进行命名："first-name"，一些软件会认为您想要从 first 里边减去 name。

- 避免 "." 字符。如果您按照这样的方式进行命名："first.name"，一些软件会认为 "name" 是对象 "first" 的属性。

- 避免 ":" 字符。冒号会被转换为命名空间来使用（稍后介绍）。

- XML 文档经常有一个对应的数据库，其中的字段会对应 XML 文档中的元素。有一个实用的经验，即使用数据库的命名规则来命名 XML 文档中的元素。

## XML 属性

属性（Attribute）提供有关元素的额外信息。

### XML 属性值必须加引号

属性值必须被引号包围，不过单引号和双引号均可使用。比如一个人的性别，person 元素可以这样写：

```xml
<person sex="female">
<person sex='female'>
```

如果属性值本身包含双引号，您可以使用单引号，就像这个实例：

```xml
<gangster name='George "Shotgun" Ziegler'>
<gangster name="George &quot;Shotgun&quot; Ziegler">
```

### XML 元素和属性

```xml
<person sex="female">
<firstname>Anna</firstname>
<lastname>Smith</lastname>
</person>
```

```xml
<person>
<sex>female</sex>
<firstname>Anna</firstname>
<lastname>Smith</lastname>
</person>
```

在第一个实例中，sex 是一个属性。在第二个实例中，sex 是一个元素。这两个实例都提供相同的信息。

没有什么规矩可以告诉我们什么时候该使用属性，而什么时候该使用元素。我的经验是在 HTML 中，属性用起来很便利，但是在 XML 中，您应该尽量避免使用属性。如果信息感觉起来很像数据，那么请使用元素吧。

> 元数据（有关数据的数据）应当存储为属性，而数据本身应当存储为元素.

### 属性的劣势

- 属性不能包含多个值（元素可以）
- 属性不能包含树结构（元素可以）
- 属性不容易扩展（为未来的变化）

属性难以阅读和维护。请尽量使用元素来描述数据。而仅仅使用属性来提供与数据无关的信息。


### 注

XML 现在的很多使用场景已经被 JSON 替代，但在一些特殊领域，XML 的设计思想很适合存储特定数据，例如 XPATH 在爬虫的应用。