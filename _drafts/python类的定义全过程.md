# python 类的实例化的全过程
https://juejin.im/post/5add4446f265da0b8d4186af

https://www.cnblogs.com/ifantastic/p/3175735.html

一直以来使用 Python 里的类，都是先写类名，然后 `__init__`， 并且 Python 变量不需要声明类型的，就理所应当的觉得 Python 里没有 new，不像是 Java 或者 C# 那样使用一个对象前要先 new 一个出来，然后再实例化。

结果是 Python 里有 `__new__` 这个概念，但是大部分情况下会被隐藏，我们可以先定义一个类，然后 dir(cls) 看下有哪些方法。



