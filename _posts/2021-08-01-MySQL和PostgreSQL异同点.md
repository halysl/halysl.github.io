# MySQL 和 PostgreSQL 异同点

MySQL 是一个非常常见的 RDBMS，同时在国内的市场占有率也非常的高。PostgreSQL 近些年来才在国内有了些起色。先不论这种现象是如何形成的，只谈两者间的差异。

由于数据库版本的更新，以下部分内容可能不太准确。仅从一些大的方面进行比较。

|功能|MySQL|PostgreSQL|
|---|----|-------|
|OLTP|yes|yes|
|OLAP|no|yes|
|性能|弱|强|
|数据类型|少|多|
|时序数据|no|yes|
|图数据|no|yes|
|集群|yes,主从|yes,强一致|
|其他数据接入|弱|强|
|SQL特性支持|36|94|
|GPU加速|no|yes|
|发版速度|慢|快|
|数据库命名|好点|差点|

以上比较仅参考一些回答梳理而出，相比于 MySQL 我更乐意学习 PostgreSQL。

从技术层面来看，PostgreSQL 比 MySQL 更好用，性能更好，同时做了很多其他事，增加了学习成本；从工程实践来看，MySQL 足够流行，易于学习，只做自己份内的事。

## 参考

- [PostgreSQL 与 MySQL 相比，优势何在？](https://www.zhihu.com/question/20010554)
- [MySQL已经可以干大部分事情了，还有必要使用商业数据库或者PostgreSQL吗？](https://www.zhihu.com/question/21793412)
- [PostgreSQL具有更多的企业级数据库的特性，为什么国内开源数据库用MySQL的更加广泛？](https://www.zhihu.com/question/22487614)
