__dir__

__eq__
__ge__
__gt__
__le__
__lt__

__init__
__new__

__str__
__repr__

__format__
__doc__

__get__
__set__

__getattribute__
__getattr__
__setattr__
__delattr__


# Python 的对象协议

传闻中，掌握了 Python 的魔术方法，就掌握了 Python 面向对象的一切。可以说，面向对象的很多接口的实现靠的就是「对象协议」。说起来有点玄乎，实际操作起来就好了。

Python 是一门动态语言，Duck Typing 概念遍布其中，所以其中的 Concept 并不是以类型的约束为载体，而是使用称作为协议的概念。那什么是 Duck Typing 呢？

Duck Typing 是鸭子类型，在动态语言中用的较多，是动态类型语言设计的一种风格。在这种风格中，一个对象有效的语义，不是由继承自特定的类或实现特定的接口决定，而是由当前方法和属性的集合决定。说白了就是并不关心对象是什么类型，只关心行为。

> “当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。”

现在来看看什么是协议吧，所谓协议，类似你讲中文，我也讲中文，我们就能交流，你讲英文，我学过英文（即实现了“听得懂英语协议”）；简单的说，在python中我需要调用你的某个方法，你正好有这个方法，这就是协议，比如在加法运算中，当出现加号（+）时，那么按照数值类型相关的协议，python会自动去调用相应对象的__add__()方法，这就是协议。

## 构造和初始化协议


## 类型转换协议

将对象类型进行转换的协议。

```python
In [13]: a = 1

In [14]: type(a)
Out[14]: int

In [15]: b = float(a)

In [16]: c = a.__float__()

In [17]: type(b)
Out[17]: float

In [18]: type(c)
Out[18]: float
```

可以看到，通过 \_\_float__ 协议将 int 类型转成了 float 类型。

Python也有很多的魔术方法来实现类似 float() 的内置类型转换特性。 __int__(self) 实现整形的强制转换 __long__(self) 实现长整形的强制转换 __float__(self) 实现浮点型的强制转换 __complex__(self) 实现复数的强制转换 __oct__(self) 实现八进制的强制转换 __hex__(self) 实现二进制的强制转换 __index__(self) 当对象是被应用在切片表达式中时，实现整形强制转换，如果你定义了一个可能在切片时用到的定制的数值型,你应该定义 __index__ (详见PEP357) __trunc__(self) 当使用 math.trunc(self) 的时候被调用。 __trunc__ 应该返回数值被截取成整形(通常为长整形)的值 __coerce__(self, other) 实现混合模式算数。如果类型转换不可能的话，那么 __coerce__ 将会返回 None ,否则他将对 self 和 other 返回一个长度为2的tuple，两个为相同的类型。

## 比较大小的协议

## 数值类型相关

<table>
<tr>
<th>分类</th>
<th>方法</th>
<th>操作符/函数</th>
<th>说明</th>
</tr>
<tr>
    <td rowspan="10"> 数值运算符</td>
</tr>
<tr>
    <td>__add__</td>
    <td>+</td>
    <td>加</td>
</tr>
<tr>
    <td>__sub__</td>
    <td>-</td>
    <td>减</td>
</tr>
<tr>
    <td>__mul__</td>
    <td>*</td>
    <td>乘</td>
</tr>
<tr>
    <td>__div__</td>
    <td>/</td>
    <td>除</td>
</tr>
<tr>
    <td>__floordiv__</td>
    <td>//</td>
    <td>整除</td>
</tr>
<tr>
    <td>__truediv__</td>
    <td>/</td>
    <td>真除，当__future__.division 起作用时调用，否则调用__div__</td>
</tr>
<tr>
    <td>__power__</td>
    <td>**</td>
    <td>幂运算</td>
</tr>
<tr>
    <td>__mod__</td>
    <td>%</td>
    <td>取余</td>
</tr>
<tr>
    <td>__divmod__</td>
    <td>divmod()</td>
    <td>余、除</td>
</tr>
<tr>
    <td rowspan="7"> 数值运算符</td>
</tr>
<tr>
    <td>__lshift__</td>
    <td><<</td>
    <td>向左移位</td>
</tr>
<tr>
    <td>__rshift__</td>
    <td>>></td>
    <td>向右移位</td>
</tr>
<tr>
    <td>__and__</td>
    <td>&</td>
    <td>与</td>
</tr>
<tr>
    <td>__or__</td>
    <td>|</td>
    <td>或</td>
</tr>
<tr>
    <td>__xor__</td>
    <td>^</td>
    <td>异或</td>
</tr>
<tr>
    <td>__invert__</td>
    <td>~</td>
    <td>非</td>
</tr>
<tr>
    <td rowspan="14"> 运算运算符</td>
</tr>
<tr>
    <td>__iadd__</td>
    <td>+=</td>
    <td></td>
</tr>
<tr>
    <td>__isub__</td>
    <td>-=</td>
    <td></td>
</tr>
<tr>
    <td>__imul__</td>
    <td>*=</td>
    <td></td>
</tr>
<tr>
    <td>__idiv__</td>
    <td>/=</td>
    <td></td>
</tr>
<tr>
    <td>__ifloordiv__</td>
    <td>//=</td>
    <td></td>
</tr>
<tr>
    <td>__itruediv__</td>
    <td>/=</td>
    <td></td>
</tr>
<tr>
    <td>__ipower__</td>
    <td>**=</td>
    <td></td>
</tr>
<tr>
    <td>__imod__</td>
    <td>%=</td>
    <td></td>
</tr>
<tr>
    <td>__ilshift__</td>
    <td><<=</td>
    <td></td>
</tr>
<tr>
    <td>__irshift__</td>
    <td>>>=</td>
    <td></td>
</tr>
<tr>
    <td>__iand__</td>
    <td>&=</td>
    <td></td>
</tr>
<tr>
    <td>__ior__</td>
    <td>|=</td>
    <td></td>
</tr>
<tr>
    <td>__ixor__</td>
    <td>^=</td>
    <td></td>
</tr>
<tr>
    <td rowspan="4"> 其他</td>
</tr>
<tr>
    <td>__pos__</td>
    <td>+</td>
    <td>正</td>
</tr>
<tr>
    <td>__neg__</td>
    <td>-</td>
    <td>负</td>
</tr>
<tr>
    <td>__abs__</td>
    <td>abs()</td>
    <td>绝对值</td>
</tr>

</table>

## 容器类型协议

## 可调用对象协议

## 可哈希协议

## 描述符协议

## 属性交互协议

## 上下文管理协议

