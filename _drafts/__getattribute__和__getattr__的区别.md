# __getattribute__ 和 __getattr__ 的区别

这两个方法在外形上有点相似，但是差距不小，后面的 getattr() 和 setattr()、delattr()类似于Java里的 setter，getter。

## __getattribute__ 是啥子

\_\_getattribute__ 是新式类才出现的。

|Python Version|必要条件|类类型|
|--------------|-------|-----|
|<2.2|无|经典类|
|(2.2, 2.7)|无|经典类
|(2.2, 2.7)|继承object|新式类|
|3.x|无|新式类|

`__getattribute__` 是属性访问拦截器，就是当这个类的属性被访问时，会自动调用类的 `__getattribute__` 方法。

Python中只要是新式类，就默认存在属性拦截器，只不过是拦截后没有进行任何操作，而是直接返回。所以我们可以自己改写 `__getattribute__` 方法来实现相关功能，比如查看权限、打印 log 日志等。如下代码，简单理解即可：

```python
class Student(object):
    def __init__(self, name, num):
        self.name = name
        self.num = num

    def __getattribute__(self, *args, **kwargs):
        if args[0] == "name":
            print("you want get attr({}),but will return {{value+1}}".format(args[0]))
            return str(object.__getattribute__(self,*args,**kwargs)) + "1"
        else:
            print("you don't want get attr name")
            return object.__getattribute__(self,*args,**kwargs)

s1 = Student("Ash", 1)
s2 = Student("Light", 2)
print(s1.name)
print(s2.name)
print(s1.num)
print(s2.num)
```

上述过程中如果访问的是 name 字段，就会打印日志，并且将返回值变为字符串并且后缀加上字符“1”。

初学者用__getattribute__方法时，容易栽进这个坑，什么坑呢，直接看代码：

```python
class Student(object):
    def __init__(self, name, num):
        self.name = name
        self.num = num

    def __getattribute__(self, *args, **kwargs):
        if args[0] == "name":
            print("you want get attr({}),but will return {{value+1}}".format(args[0]))
            return str(object.__getattribute__(self,*args,**kwargs)) + "1"
        else:
            print("you don't want get attr name")
            return self.special_call()
    
    def special_call(self):
        return "special call"

s1 = Student("Ash", 1)
print(s1.name)
print(s1.num)
```

上面执行的结果就会进入到错误的无限递归，这是因为，当调用 `s1.num` 的时候，会去调用 `self.special_call`， 但是调用 `self.special_call` 的时候又会从 `__getattribute__` 走，无限递归。

如果 `__getattribute__` 没有定义好，这个问题会出现在很多地方，包括对象的内建方法或属性，比如  `__dict__`，所以这时候就推荐使用 `__getattr__`。

## __getattr__ 是啥子

当访问某个实例属性时， `__getattribute__` 会被无条件调用。

如果没有实现自己的 `__getattr__` 方法，就会抛出 `AttributeError` 提示找不到这个属性。

如果自定义了自身的 `__getattr__` 方法的话，方法会在这种找不到属性的情况下被调用。

所以在找不到属性的情况下通过实现自定义的 `__getattr__` 方法来实现一些功能是一个不错的方式。

```python
class Test(object):
    def __init__(self, p):
        self.p = p

    def __getattr__(self, item):
        return 'default'

t = Test('p1')
print(t.p)
print(t.p2)
```

和 `__getattr__` 同一级别的还有 `__setattr__` 和 `__delattr__` 方法。
