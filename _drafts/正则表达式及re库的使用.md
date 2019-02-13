#正则表达式及re库的使用
##一、正则表达式
正则表达式要做的事简单地说就是字符串匹配，它由普通字符、非打印字符、特殊字符、限定符和定位符构成。理论上可以匹配一切字符串。
##二、字符分类
1、普通字符
##三、re库的使用
re.match(pattern, string, flags=0)
re.search(pattern, string, flags=0)
re.sub(pattern, repl, string, count=0, flags=0)

re.compile(pattern[, flags])

re.findall(string[, pos[, endpos]])
re.finditer(pattern, string, flags=0)
re.split(pattern, string[, maxsplit=0, flags=0])


[Python 正则表达式](http://www.runoob.com/python/python-reg-expressions.html)
[在线正则表达式测试](http://tool.oschina.net/regex)
[正则表达式手册](http://tool.oschina.net/uploads/apidocs/jquery/regexp.html)
[正则表达式30分钟入门教程](https://deerchao.net/tutorials/regex/regex.htm)