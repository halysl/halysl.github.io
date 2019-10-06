---
layout: post
title: Python 的对象协议
categories: [Python, 转载]
description: Python 的对象协议
keywords: Python, 转载
---

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

可以看到，通过 `__float__` 协议将 int 类型转成了 float 类型。

Python也有很多的魔术方法来实现类似 float() 的内置类型转换特性。 

- `__int__(self)` 实现整形的强制转换
- `__long__(self)` 实现长整形的强制转换
- `__float__(self)` 实现浮点型的强制转换
- `__complex__(self)` 实现复数的强制转换
- `__oct__(self)` 实现八进制的强制转换
- `__hex__(self)` 实现二进制的强制转换
- `__index__(self)` 当对象是被应用在切片表达式中时，实现整形强制转换，如果你定义了一个可能在切片时用到的定制的数值型，你应该定义 `__index__` (详见PEP357) 
- `__trunc__(self)` 当使用 math.trunc(self) 的时候被调用。 `__trunc__` 应该返回数值被截取成整形(通常为长整形)的值
- `__coerce__(self, other)` 实现混合模式算数。如果类型转换不可能的话，那么`__coerce__` 将会返回 None ,否则他将对 self 和 other 返回一个长度为2的tuple，两个为相同的类型。

## 比较大小的协议

这个协议依赖于 `__cmp__()` 方法，当两者相等时返回 0，`self<other` 时返回负值，反之返回正值。但是这种返回有点复杂，Python 又定义了以下方法进行判定：

- `__eq__(self, other)` 定义了等号的行为, == 。
- `__ne__(self, other)` 定义了不等号的行为, != 。
- `__lt__(self, other)` 定义了小于号的行为， < 。
- `__gt__(self, other)` 定义了大于等于号的行为， >= 。

## 数值类型相关协议

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

作为一个容器，具备这么几个行为：查询、取值、删除、赋值、求长度，由此可以推断出有哪些协议被实现。

- `__len__(self)` 给出容器长度。对于可变，不可变容器都需要有的协议的一部分。 
- `__getitem__(self, key)` 定义当一个条目被访问时，使用符号 `self[key]` 。这也是不可变容器和可变容器都要有的协议的一部分。如果键的类型错误和 KeyError 或者没有合适的值。那么应该抛出适当的 TypeError 异常。
- `__setitem__(self, key, value)` 定义当一个条目被赋值时的行为,使用 `self[key] = value` 。这也是可变容器和不可变容器协议中都要有的一部分。
- `__delitem__(self, key)` 定义当一个条目被删除时的行为(比如 `del self[key]`)。这只是可变容器协议中的一部分。当使用一个无效的键时应该抛出适当的异常。 
- `__iter__(self)` 返回一个容器的迭代器。很多情况下会返回迭代器，尤其是当内置的 iter() 方法被调用的时候，或者当使用 `for x in container` 方式循环的时候。迭代器是他们本身的对象，他们必须定义返回 self 的 `__iter__` 方法。
- `__reversed__(self)` 实现当 `reversed()` 被调用时的行为。应该返回列表的反转版本。
- `__contains__(self, item)` 当调用 in 和 not in 来测试成员是否存在时候 `__contains__` 被定义。你问为什么这个不是序列协议的一部分？那是因为当 `__contains__` 没有被定义的时候，Python会迭代这个序列并且当找到需要的值时会返回 True 。
- `__concat__(self, other)` 最终，你可以通过 `__concat__` 来定义当用其他的来连接两个序列时候的行为。当 + 操作符被调用时候会返回一个 `self` 和 `other.__concat__` 被调用后的结果产生的新序列。

## 可调用对象协议

可调用对象，也就是类似函数对象，能够让类实例表现的像函数一样，这样可以让每一个函数调用都有所不同。怎么理解这句话呢？

允许一个类的实例像函数一样被调用。实质上说，这意味着 `x()` 与 `x.__call__()` 是相同的。注意 `__call__` 参数可变。这意味着你可以定义 `__call__` 为其他你想要的函数，无论有多少个参数。

`__call__` 在那些类的实例经常改变状态的时候会非常有效。调用这个实例是一种改变这个对象状态的直接和优雅的做法。

还是看例子吧。

```python
#coding=utf-8
class A(object):
    def __init__(self,name):
        self.name = name
    def __call__(self):
        print "dongn something with %s"%(self.name)

a = A('li lei')
b = A('han ×××')
print a()
print b()
```

- [Python 内部：可调用对象是如何工作的](https://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/python-internals-how-callables-work.html)

## 可哈希协议

如果对象有 `__hash__()` 方法，表示是一个可哈希对象。`__hash__()` 方法支持这 hash() 这个内置函数。按照文档里面的解释“如果一个对象是可哈希的，那么在它的生存期内必须不可变(需要一个哈希函数)，而且可以和其他对象比较(需要比较方法).比较值相同的对象一定有相同的哈希值”。

这也就是说所有不可变的内置类型 t 都是可哈希的，比如 `string`，`tuple`。所有可变的内置类型都是不可哈希的，比如 `list`，`dict`（即没有 `__hash__()` 方法）。字典的 `key` 必须是可哈希的，所以 `tuple`，`string` 可以做 key，而 `list` 不能做key。

## 描述符协议

描述器相关的概念，这个概念相当的复杂，内部的实现以及外部的使用能水两篇文章，这里只提到一些协议。

为了构建一个描述器，一个类必须有至少 `__get__` 或者 `__set__` 其中一个，并且 `__delete__` 被实现。

让我们看看这些魔术方法。 

- `__get__(self, instance, owner)` 定义当描述器的值被取得的时候的行为，instance 是拥有者对象的一个实例。 owner 是拥有者类本身。 
- `__set__(self, instance, value)` 定义当描述器值被改变时候的行为。instance 是拥有者类的一个实例 value 是要设置的值。 
- `__delete__(self, instance)` 定义当描述器的值被删除的行为。instance 是拥有者对象的实例。

```python
class Meter(object):
    def __init__(self, value=0.0):
        self.value = float(value)
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = float(value)

class Foot(object):
    def __get__(self, instance, owner):
        return instance.meter * 3.2808
    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808

class Distance(object):
    '''Class to represent distance holding two descriptors for feet and
    meters.'''
    meter = Meter()
    foot = Foot()

d = Distance()
print(d.meter)
print(d.foot)
d.meter = 2
print(d.meter)
print(d.foot)
```

## 属性交互协议

也就是 控制属性访问 相关的协议。

- `__getattr__(self, name)` 你可以定义当用户试图获取一个不存在的属性时的行为。这适用于对普通拼写错误的获取和重定向，对获取一些不建议的属性时候给出警告(如果你愿意你也可以计算并且给出一个值)或者处理一个 AttributeError 。只有当调用不存在的属性的时候会被返回。然而，这不是一个封装的解决方案。 
- `__setattr__(self, name, value)` 与 `__getattr__` 不同， `__setattr__` 是一个封装的解决方案。无论属性是否存在，它都允许你定义对对属性的赋值行为，以为这你可以对属性的值进行个性定制。但是你必须对使用 `__setattr__` 特别小心。之后我们会详细阐述。 - 
- `__delattr__` 与 `__setattr__` 相同，但是功能是删除一个属性而不是设置他们。注意与 `__setattr__` 相同，防止无限递归现象发生。(在实现 `__delattr__` 的时候调用 `del self.name` 即会发生)
- `__getattribute__(self, name)` `__getattribute__` 与它的同伴 `__setattr__` 和 `__delattr__` 配合非常好。但是我不建议使用它。只有在新类型类定义中才能使用 `__getattribute__` (这样你可以定义一个属性值的访问规则。有时也会产生一些递归现象。(这时候你可以调用基类的 `__getattribute__` 方法来防止此现象的发生。)它可以消除对 `__getattr__` 的使用，如果它被明确调用或者一个 AttributeError 被抛出，那么当实现 `__getattribute__` 之后才能被调用。此方法是否被使用其实最终取决于你的选择。)我不建议使用它因为它的使用几率较小(我们在取得一个值而不是设置一个值的时候有特殊的行为是非常罕见的。)而且它不能避免会出现bug。

更多的区别可以看：[getattribute 和 getattr 的区别](https://halysl.github.io/2019/03/03/__getattribute__%E5%92%8C__getattr__%E7%9A%84%E5%8C%BA%E5%88%AB/)

## 上下文管理协议

这个板块的协议作用比较大。

上下文管理也称为会话管理，通过 `with` 语句块快速实现环境设置和环境清除，这依赖于 `__enter__` 和 `__exit__` 方法。

- `__enter__(self)` 定义当使用 with 语句的时候会话管理器应该初始块被创建的时候的行为。注意 `__enter__` 的返回值被 with 语句的目标或者 as 后的名字绑定。 
- `__exit__(self, exception_type, exception_value, traceback)` 定义当一个代码块被执行或者终止后会话管理器应该做什么。它可以被用来处理异常，清除工作或者做一些代码块执行完毕之后的日常工作。如果代码块执行成功， exception_type , exception_value , 和 traceback 将会是 None 。否则的话你可以选择处理这个异常或者是直接交给用户处理。如果你想处理这个异常的话，确认 `__exit__` 在所有结束之后会返回 True 。如果你想让异常被会话管理器处理的话，那么就这样处理。

```python
class Closer:
'''通过with语句和一个close方法来关闭一个对象的会话管理器'''

def __init__(self, obj):
    self.obj = obj

def __enter__(self):
    return self.obj # bound to target

def __exit__(self, exception_type, exception_val, trace):
    try:
        self.obj.close()
    except AttributeError: # obj isn't closable
        print 'Not closable.'
        return True # exception handled successfully
```

```python
>>> from magicmethods import Closer
>>> from ftplib import FTP
>>> with Closer(FTP('ftp.somesite.com')) as conn:
...     conn.dir()
...
>>> conn.dir()
>>> with Closer(int(5)) as i:
...     i += 1
...
Not closable.
>>> i
6
```

上下文管理器属于比较重要的模块，也非常容易实现，最简单的实现方案莫过于 `contextmanager + yield`，更多的内容可以参考[谈一谈Python的上下文管理器](http://www.bjhee.com/python-context.html)。

## 序列化协议

比较少用到，主要是搭配 Pickle 使用。

Pickle 并不是只支持内建数据结果，任何遵循 Pickle 协议的类都可以，Pickle 协议为 Python 对象规定了4个可选方法来自定义 Pickle 行为（对于 C 扩展的 cPickle 模块会有一些不同，但是这并不在我们的讨论范围内）：

- `__getinitargs__(self)`：如果你希望在逆序列化的同时调用 `__init__` ，你可以定义 `__getinitargs__` 方法，这个方法应该返回一系列你想被 `__init__` 调用的参数，注意这个方法只对经典类起作用。
- `__getnewargs__(self)`：对于新式的类，你可以定义任何在重建对象时候传递到 `__new__` 方法中的参数。这个方法也应该返回一系列的被 `__new__` 调用的参数。
- `__getstate__(self)`：你可以自定义当对象被序列化时返回的状态，而不是使用 `__dict` 方法，当逆序列化对象的时候，返回的状态将会被 `__setstate__` 方法调用。
- `__setstate__(self, state)`：在对象逆序列化的时候，如果 `__setstate__` 定义过的话，对象的状态将被传给它而不是传给 `__dict__` 。这个方法是和 `__getstate__` 配对的，当这两个方法都被定义的时候，你就可以完全控制整个序列化与逆序列化的过程了。

## 类的表现协议

如果有一个字符串来表示一个类将会非常有用。在 Python 中，有很多方法可以实现类定义内置的一些函数的返回值。 

- `__str__(self)` 定义当 str() 调用的时候的返回值
- `__repr__(self)` 定义 repr() 被调用的时候的返回值

str() 和 repr() 的主要区别在于 repr() 返回的是机器可读的输出，而 str() 返回的是人类可读的。 

- `__unicode__(self)` 定义当 unicode() 调用的时候的返回值。 unicode() 和 str() 很相似，但是返回的是unicode字符串。注意，如a果对你的类调用 str() 然而你只定义了 `__unicode__()` ，那么将不会工作。你应该定义 `__str__()` 来确保调用时能返回正确的值
- `__hash__(self)` 定义当 hash() 调用的时候的返回值，它返回一个整形，用来在字典中进行快速比较

# 参考资料

- [Python 魔术方法指南](https://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/a-guide-to-pythons-magic-methods.html#id18)
- [Python的对象协议](https://blog.51cto.com/11026142/1858863)
- [python中的del用法](https://blog.csdn.net/windscloud/article/details/79732014)
- [Python 内部：可调用对象是如何工作的](https://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/python-internals-how-callables-work.html)
