---
layout: post
title: Python-super 没那么简单
categories: [Python, 转载]
description: Python-super 没那么简单
keywords: Python, 转载
---

# 【转】Python: super 没那么简单

## 转载信息

关于 python super 相关的东西，这篇博客的解释非常易懂，作者思路清晰，对于文中部分不精确的地方，我会适当的加上注释。链接是：[Python: super 没那么简单](https://mozillazg.com/2016/12/python-super-is-not-as-simple-as-you-thought.html)。

## 目录

- [前言¶](#qianyan)
- [约定¶](#yueding)
- [单继承¶](#danjichen)
- [多继承¶](#duojichen)
- [super 是个类¶](#superclass)
- [多继承中 super 的工作方式¶](#duojichensuper)
- [实现一个 Super 类¶](#achievesuper)
- [总结¶](#comment)
- [参考资料¶](#refer)

<span id="qianyan"></span>
## 前言

说到 `super`， 大家可能觉得很简单呀，不就是用来调用父类方法的嘛。如果真的这么简单的话也就不会有这篇文章了，且听我细细道来。😄

<span id="yueding"></span>
## 约定

在开始之前我们来约定一下本文所使用的 Python 版本。默认用的是 Python 3，也就是说：本文所定义的类都是新式类。如果你用到是 Python 2 的话，记得继承 `object`:

```python
# 默认， Python 3
class A:
    pass

# Python 2
class A(object):
    pass
```

Python 3 和 Python 2 的另一个区别是: Python 3 可以使用直接使用 ```super().xxx``` 代替 ```super(Class, self).xxx``` :

```python
# 默认，Python 3
class B(A):
    def add(self, x):
        super().add(x)

# Python 2
class B(A):
    def add(self, x):
        super(B, self).add(x)
```

所以，你如果用的是 Python 2 的话，记得将本文的 `super()` 替换为 `suepr(Class, self)`。

如果还有其他不兼容 Python 2 的情况，我会在文中注明的。

<span id="danjichen"></span>
## 单继承

在单继承中 `super` 就像大家所想的那样，主要是用来调用父类的方法的。

```python
class A:
    def __init__(self):
        self.n = 2

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        self.n += m


class B(A):
    def __init__(self):
        self.n = 3

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        super().add(m)
        self.n += 3
```

你觉得执行下面代码后， `b.n` 的值是多少呢？

```python
b = B()
b.add(2)
print(b.n)
```

执行结果如下:

```python
self is <__main__.B object at 0x106c49b38> @B.add
self is <__main__.B object at 0x106c49b38> @A.add
8
```

这个结果说明了两个问题:

1. `super().add(m)` 确实调用了父类 A 的 `add` 方法。
2. `super().add(m)` 调用父类方法 `def add(self, m)` 时, 此时父类中 `self` 并不是父类的实例而是子类的实例, 所以 `super().add(m)` 之后 `self.n` 的结果是 `5` 而不是 `4` 。

不知道这个结果是否和你想到一样呢？下面我们来看一个多继承的例子。

<span id="duojichen"></span>
## 多继承

这次我们再定义一个 `class C`，一个 `class D`:

```python
class C(A):
    def __init__(self):
        self.n = 4

    def add(self, m):
        print('self is {0} @C.add'.format(self))
        super().add(m)
        self.n += 4


class D(B, C):
    def __init__(self):
        self.n = 5

    def add(self, m):
        print('self is {0} @D.add'.format(self))
        super().add(m)
        self.n += 5
```

下面的代码又输出啥呢？

```python
d = D()
d.add(2)
print(d.n)
```

这次的输出如下:

```python
self is <__main__.D object at 0x10ce10e48> @D.add
self is <__main__.D object at 0x10ce10e48> @B.add
self is <__main__.D object at 0x10ce10e48> @C.add
self is <__main__.D object at 0x10ce10e48> @A.add
19
```

你说对了吗？你可能会认为上面代码的输出类似:

```python
self is <__main__.D object at 0x10ce10e48> @D.add
self is <__main__.D object at 0x10ce10e48> @B.add
self is <__main__.D object at 0x10ce10e48> @A.add
15
```

为什么会跟预期的不一样呢？下面我们将一起来看看 `super` 的奥秘。

<span id="superclass"></span>
## super 是个类

当我们调用 `super()` 的时候，实际上是实例化了一个 `super` 类。你没看错， `super` 是个类，既不是关键字也不是函数等其他数据结构:

```python
>>> class A: pass
...
>>> s = super(A)
>>> type(s)
<class 'super'>
>>>
```

在大多数情况下， `super` 包含了两个非常重要的信息: 一个 MRO(Method Resolution Order) 列表以及 MRO 中的一个类。当以如下方式调用 `super` 时:

```python
# 注意这里的obj指的是instance，在python2中就像是super(Classname, self)，python3中隐藏
super(a_type, obj)
```

MRO 列表指的是 `type(obj)` 的 MRO 列表, MRO 中的那个类就是 `a_type` , 同时 `isinstance(obj, a_type) == True` 。

当这样调用时:

```
super(type1, type2)
```

MRO 指的是 `type2` 的 MRO 列表, MRO 中的那个类就是 `type1` ，同时 `issubclass(type2, type1) == True` 。

那么， `super()` 实际上做了啥呢？简单来说就是：提供一个 MRO 列表以及一个 MRO 中的类 `C` ， `super()` 将返回一个从 MRO 列表中 `C` 之后的类中查找方法的对象。

也就是说，查找方式时不是像常规方法一样从所有的 MRO 类中查找，而是从 MRO 列表的 tail 中查找。

举个栗子, 有个 MRO 列表:

```python
[A, B, C, D, E, object]
```

下面的调用:

```python
super(C, A).foo()
```

`super` 只会从 `C` 之后查找，即: 只会在 `D` 或 `E` 或 `object` 中查找 `foo` 方法。

<span id="duojichensuper"></span>
## 多继承中 super 的工作方式

再回到前面的

```python
d = D()
d.add(2)
print(d.n)
```

现在你可能已经有点眉目，为什么输出会是

```python
self is <__main__.D object at 0x10ce10e48> @D.add
self is <__main__.D object at 0x10ce10e48> @B.add
self is <__main__.D object at 0x10ce10e48> @C.add
self is <__main__.D object at 0x10ce10e48> @A.add
19
```

了吧 ;)

下面我们来具体分析一下:

- `D` 的 MRO 是: `[D, B, C, A, object]` 。 备注: 可以通过 `D.mro()` (Python 2 使用 `D.__mro__` ) 来查看 `D` 的 MRO 信息）
- 详细的代码分析如下:

```python
class A:
    def __init__(self):
        self.n = 2

    def add(self, m):
        # 第四步
        # 来自 D.add 中的 super
        # self == d, self.n == d.n == 5
        print('self is {0} @A.add'.format(self))
        self.n += m
        # d.n == 7


class B(A):
    def __init__(self):
        self.n = 3

    def add(self, m):
        # 第二步
        # 来自 D.add 中的 super
        # self == d, self.n == d.n == 5
        print('self is {0} @B.add'.format(self))
        # 等价于 suepr(B, self).add(m)
        # self 的 MRO 是 [D, B, C, A, object]
        # 从 B 之后的 [C, A, object] 中查找 add 方法
        super().add(m)

        # 第六步
        # d.n = 11
        self.n += 3
        # d.n = 14

class C(A):
    def __init__(self):
        self.n = 4

    def add(self, m):
        # 第三步
        # 来自 B.add 中的 super
        # self == d, self.n == d.n == 5
        print('self is {0} @C.add'.format(self))
        # 等价于 suepr(C, self).add(m)
        # self 的 MRO 是 [D, B, C, A, object]
        # 从 C 之后的 [A, object] 中查找 add 方法
        super().add(m)

        # 第五步
        # d.n = 7
        self.n += 4
        # d.n = 11


class D(B, C):
    def __init__(self):
        self.n = 5

    def add(self, m):
        # 第一步
        print('self is {0} @D.add'.format(self))
        # 等价于 super(D, self).add(m)
        # self 的 MRO 是 [D, B, C, A, object]
        # 从 D 之后的 [B, C, A, object] 中查找 add 方法
        super().add(m)

        # 第七步
        # d.n = 14
        self.n += 5
        # self.n = 19

d = D()
d.add(2)
print(d.n)
```

调用过程图如下:

```python
D.mro() == [D, B, C, A, object]
d = D()
d.n == 5
d.add(2)

class D(B, C):          class B(A):            class C(A):             class A:
    def add(self, m):       def add(self, m):      def add(self, m):       def add(self, m):
        super().add(m)  1.--->  super().add(m) 2.--->  super().add(m)  3.--->  self.n += m
        self.n += 5   <------6. self.n += 3    <----5. self.n += 4     <----4. <--|
        (14+5=19)               (11+3=14)              (7+4=11)                (5+2=7)
```

![super](/images/blog/super.png)

现在你知道为什么 `d.add(2)` 后 `d.n` 的值是 19 了吧 ;)

如果感觉上面的解释还不是很清楚的话，下面我们一起来根据 super 的功能实现一个我们自己的 Super 类，相信这样会更直观一点。

<span id="achievesuper"></span>
## 实现一个 Super 类

在实现这个 Super 类之前，我们先来复习一下前面说的 super 的信息：

> super() 实际上做了啥呢？简单来说就是：提供一个 MRO 列表以及一个 MRO 中的类 C ， super() 将返回一个从 MRO 列表中 C 之后的类中查找方法的对象。

根据这个信息我们可以写一个简陋版本的 Super 类:

```python
from functools import partial


class Super:
    def __init__(self, sub_cls, instance):
        # 假设 sub_cls = B, instance = D()
        # Super(B, self).add(233)
        mro = instance.__class__.mro()
        # mro == [D, B, C, A, object]
        # sub_cls is B
        # 从 mro 中 sub_cls 后面的类中进行查找
        # __mro_tail == [C, A, object]
        self.__mro_tail = mro[mro.index(sub_cls)+1:]
        self.__sub_cls = sub_cls
        self.__instance = instance

    def __getattr__(self, name):
        # 从 mro tail 列表的各个类中查找方法
        for cls in self.__mro_tail:
            if not hasattr(cls, name):
                continue

            print('call {}.{}'.format(cls, name))
            # 获取类中定义的方法
            attr = getattr(cls, name)
            # 因为 d = D(); d.add(233)  等价于 D.add(d, 233)
            # 所以返回的函数需要自动填充第一个 self 参数
            return partial(attr, self.__instance)

        raise AttributeError(name)
```

然后我们把上面的那个例子中的 super 替换为这个简陋版本的 Super 类，看看效果:

```python
class A:
    def __init__(self):
        self.n = 2

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        self.n += m


class B(A):
    def __init__(self):
        self.n = 3

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        Super(B, self).add(m)
        self.n += 3


class C(A):
    def __init__(self):
        self.n = 4

    def add(self, m):
        print('self is {0} @C.add'.format(self))
        Super(C, self).add(m)
        self.n += 4


class D(B, C):
    def __init__(self):
        self.n = 5

    def add(self, m):
        print('self is {0} @D.add'.format(self))
        Super(D, self).add(m)
        self.n += 5


d = D()
d.add(2)
print(d.n)
```

修改后的例子运行结果如下:

```python
self is <__main__.D object at 0x10d02cf98> @D.add
call <class '__main__.B'>.add
self is <__main__.D object at 0x10d02cf98> @B.add
call <class '__main__.C'>.add
self is <__main__.D object at 0x10d02cf98> @C.add
call <class '__main__.A'>.add
self is <__main__.D object at 0x10d02cf98> @A.add
19
```

可以看到使用简陋版 `Super` 和内置的 `super` 的效果是一样的。希望这个简陋的 Super 类可以帮助大家初步理解 super 的工作方式。

<span id="comment"></span>
## 总结

希望这篇文章能让你对 super 多一点了解，如果文中有啥没讲清楚或讲的不对的地方欢迎指正。

<span id="refer"></span>
## 参考资料

- [Python's super() Explained](http://sixty-north.com/blog/series/pythons-super-explained)
- [2. Built-in Functions — Python 3.5.2 documentation](https://docs.python.org/3/library/functions.html#super)
- [3. Data model — Python 3.7.1 documentation](https://docs.python.org/3/reference/datamodel.html#object.__getattr__)
- [functools — Higher-order functions and operations on callable objects — Python 3.7.1 documentation](https://docs.python.org/3/library/functools.html#functools.partial)
- [Python's Super Considered Harmful](https://fuhm.net/super-harmful/)
- [Python: 多继承模式下 MRO(Method Resolution Order) 的计算方式 - Huang Huang 的博客](https://mozillazg.github.io/2016/11/python-mro-compute.html)
