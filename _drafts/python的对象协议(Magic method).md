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

## 构造协议、初始化协议和删除协议

每个人都知道一个最基本的魔术方法， `__init__`。通过此方法我们可以定义一个对象的初始操作。然而，当我调用 x = SomeClass() 的时候， `__init__` 并不是第一个被调用的方法。实际上，还有一个叫做 `__new__` 的方法，来构造这个实例。然后给在开始创建时候的初始化函数来传递参数。在对象生命周期的另一端，也有一个 `__del__` 方法。我们现在来近距离的看一看这三个方法:

- `__new__(cls, [...)` `__new__` 是在一个对象实例化的时候所调用的第一个方法。它的第一个参数是这个类，其他的参数是用来直接传递给 `__init__` 方法。 `__new__` 方法相当不常用,但是它有自己的特性，特别是当继承一个不可变的类型比如一个 tuple 或者 string。
- `__init__(self, […)` 此方法为类的初始化方法。当构造函数被调用的时候的任何参数都将会传给它。(比如如果我们调用 x = SomeClass(10, 'foo'))，那么 `__init__` 将会得到两个参数 10 和 foo。 `__init__` 在 Python 的类定义中被广泛用到。
- `__del__(self)` 如果 `__new__` 和 `__init__` 是对象的构造器的话，那么 `__del__` 就是析构器。它不实现语句 del x (以上代码将不会翻译为 x.__del__() )。它定义的是当一个**对象**进行垃圾回收时候的行为。当一个对象在删除的时需要更多的清洁工作的时候此方法会很有用，比如套接字对象或者是文件对象。注意，如果解释器退出的时候对象还存存在，就不能保证 `__del__` 能够被执行。

放在一起的话，这里是一个 `__init__` 和 `__del__` 实际使用的例子。

```python
from os.path import join

class FileObject:
    '''给文件对象进行包装从而确认在删除时文件流关闭'''

    def __init__(self, filepath='~', filename='sample.txt'):
        #读写模式打开一个文件
        self.file = open(join(filepath, filename), 'r+')

    def __del__(self):
        self.file.close()
        del self.file
```

关于 `__del__` 方法，想要理解的透彻，需要知道，python 使用的是引用机制，使用 GC机制 进行数据清除，这意味着什么呢，这意味着：

- `del xxx` 语法上不等于 `xxx.__del__()`
- `xxx.__del__()` 会在特殊时间被调用（一个时间段或者程序退出时）

- `del xxx` 指的是删除某个对象对数据的引用，此时那个数据还存在，只不过引用数降低，甚至为0
- `xxx.__del__()` 可以被手动调用执行，也会在程序退出时自动调用

我么可以用下面的交互式界面验证这个问题：

```python
>>> class Hero(object):
...     def __init__(self, name):
...         self.name = name
...     def __del__(self):
...         print '{} will del...'.format(self.name)
# 可以看到每次直接声明 Hero，它的前一次定义就会被删除，因为 Hero() 本身没有被任何引用过
>>> Hero('Ash')
<__main__.Hero object at 0x10fc19e90>
>>> Hero('Bob')
Ash will del...
<__main__.Hero object at 0x10fc19fd0>
>>> Hero('Cat')
Bob will del...
<__main__.Hero object at 0x10fc19e90>
# 这里可能有点绕，首先我们可以看出__del__可以被调用，而对象并没有没删除
>>> h1 = Hero('Diabo')
>>> h2 = Hero('Eight')
>>> h1.__del__()
Diabo will del...
>>> h2.__del__()
Eight will del...
# 这里只是 repr(h1)，为什么会调用上个 Cat 对象的 __del__ 暂时还没搞清楚 T^T，猜测程序先调用了一次内存回收
>>> h1
Cat will del...
<__main__.Hero object at 0x10fc19fd0>
>>> h2
<__main__.Hero object at 0x10fc27050>
>>> del h1
Diabo will del...
# 这里可以看出 h2 对象引用已经被删除，但是本身的 __del__ 还没调用
>>> del h2
>>> exit
Eight will del...
Use exit() or Ctrl-D (i.e. EOF) to exit
```
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

## 序列化协议

