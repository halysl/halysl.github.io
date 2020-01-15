---
layout: post
title: MySQL 的 JSON 类型
categories: [MySQL]
description:
keywords: 
---

# MySQL 的 JSON 类型

之前的开发经验，让我了解到，在对表的设计时，可以预留一个 JSON 类型的字段，这样可以实现一定程度的扩展，我一开始有些反感，因为这可能滥用。例如说，建表的时候考虑不再那么周全，全部放在 attr 字段里，虽然后期实现没问题，但如果这样为什么不直接用 NoSQL，想怎么存就怎么存。

使用 JSON 类型存储，然后在代码里使用 ORM 的技术，也很容易读取。最近我遇到了一个需求，需要将监控数据以表格的形式展示，通用的 TSDB （使用 Grafana）很难渲染成表格，就决定使用 MySQL 实现。但是监控项那么多，可以考虑使用 JSON 类型存储。

## 设置 JSON 字段

```sh
mysql> CREATE TABLE user(id INT PRIMARY KEY, name VARCHAR(20) , lastlogininfo JSON);
Query OK, 0 rows affected (0.27 sec)
```

设置类型为 JSON 即可。

## 插入 JSON 数据

### 字符串法

```sql
mysql> INSERT INTO user VALUES(1 ,"lucy",'{"time":"2015-01-01 13:00:00","ip":"192.168.1.1","result":"fail"}');
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO user VALUES(1 ,"lucy",'{"time":"2015-01-01 13:00:00","ip":"192.168.1.1","result":"fail}');
ERROR 3140 (22032): Invalid JSON text: "Missing a closing quotation mark in string." at position 63 in value for column 'user.lastlogininfo'.
```

只要字符串符合 JSON 语法就可以直接插入，否则会报 `Invalid JSON text` 错误。

### JSON_OBJECT() 法

```sql
mysql> INSERT INTO user VALUES(1, "lucy",JSON_OBJECT("time",NOW(),"ip","192.168.1.1","result","fail"));
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO user VALUES(2, "andy",JSON_OBJECT("time",NOW(),"attr", JSON_OBJECT("ip","192.168.1.1","result","fail")));
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO user VALUES(3, "light",JSON_OBJECT("time",NOW(),"attr", JSON_ARRAY("ip","192.168.1.1", "result","fail")));
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM user;
+----+-------+-----------------------------------------------------------------------------------------+
| id | name  | lastlogininfo                                                                           |
+----+-------+-----------------------------------------------------------------------------------------+
|  1 | lucy  | {"ip": "\n192.168.1.1", "time": "2020-01-07 21:07:05.000000", "result": "fail"}         |
|  2 | andy  | {"attr": {"ip": "192.168.1.1", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
|  3 | light | {"attr": ["ip", "192.168.1.1", "result", "fail"], "time": "2020-01-07 21:16:50.000000"} |
+----+-------+-----------------------------------------------------------------------------------------+
3 rows in SET (0.00 sec)
```

通过 JSON_OBJECT() 方法序列化一个 JSON 对象，可以嵌套，也可以用 JSON_ARRAY 实现 JSON 列表。

### JSON_MERGE() 整合

```sql
mysql> INSERT INTO user VALUES(4, 'Ash',JSON_MERGE(
    JSON_OBJECT('time',NOW()),
    '{"attr": ["ip","192.168.1.1", "result","fail"]}')
    );
Query OK, 1 row affected, 1 warning (0.00 sec)
```

通过 JSON_MERGE() 可以拼接多个 JSON 对象，整合成一个对象，如果有重复的键出现，那么后者的值覆盖前者的值。

## 查询 JSON 字段数据

使用 -> 操作符，它和 JSON_EXTRACT 等效。

`json列->'$.键' == JSON_EXTRACT(json列 , '$.键')`

在做下面的操作前，先看下表里的数据。

```sql
mysql> SELECT * FROM user;                                                                                                          +----+-------+-----------------------------------------------------------------------------------------+
| id | name  | lastlogininfo                                                                           |
+----+-------+-----------------------------------------------------------------------------------------+
|  1 | lucy  | {"attr": {"ip": "192.168.1.1", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"} |
|  2 | andy  | {"attr": {"ip": "192.168.1.2", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
|  3 | light | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"} |
|  4 | Ash   | {"attr": {"ip": "192.168.1.4", "result": "fail"}, "time": "2020-01-08 10:10:48.000000"} |
+----+-------+-----------------------------------------------------------------------------------------+
4 rows in SET (0.00 sec)
```

开始使用 -> 或 JSON_EXTRACT 提取数据。

```sql
/* 在 WHERE 字句使用 -> 查找数据 */
mysql> SELECT * FROM user WHERE lastlogininfo -> '$.time' = "2020-01-07 21:07:43.000000";
+----+------+-----------------------------------------------------------------------------------------+
| id | name | lastlogininfo                                                                           |
+----+------+-----------------------------------------------------------------------------------------+
|  1 | lucy | {"attr": {"ip": "192.168.1.1", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"} |
+----+------+-----------------------------------------------------------------------------------------+
1 row in SET (0.00 sec)

/* 在 WHERE 字句使用 JSON_EXTRACT 查找数据 */
mysql> SELECT * FROM user WHERE JSON_EXTRACT(lastlogininfo, '$.time') = "2020-01-07 21:07:43.000000";
+----+------+-----------------------------------------------------------------------------------------+
| id | name | lastlogininfo                                                                           |
+----+------+-----------------------------------------------------------------------------------------+
|  1 | lucy | {"attr": {"ip": "192.168.1.1", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"} |
+----+------+-----------------------------------------------------------------------------------------+
1 row in SET (0.00 sec)

/* 在 WHERE 字句使用 JSON_EXTRACT 查找数据，并且查找 JSON 嵌套数据（$.attr.ip） */
mysql> SELECT * FROM user WHERE JSON_EXTRACT(lastlogininfo, '$.attr.ip') = "192.168.1.2";
+----+------+-----------------------------------------------------------------------------------------+
| id | name | lastlogininfo                                                                           |
+----+------+-----------------------------------------------------------------------------------------+
|  2 | andy | {"attr": {"ip": "192.168.1.2", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
+----+------+-----------------------------------------------------------------------------------------+
1 row in SET (0.00 sec)

/* 在 ORDER BY 字句使用 JSON_EXTRACT 排序数据 */
mysql> SELECT * FROM user ORDER BY JSON_EXTRACT(lastlogininfo, '$.attr.ip') DESC;
+----+-------+-----------------------------------------------------------------------------------------+
| id | name  | lastlogininfo                                                                           |
+----+-------+-----------------------------------------------------------------------------------------+
|  4 | Ash   | {"attr": {"ip": "192.168.1.4", "result": "fail"}, "time": "2020-01-08 10:10:48.000000"} |
|  3 | light | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"} |
|  2 | andy  | {"attr": {"ip": "192.168.1.2", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
|  1 | lucy  | {"attr": {"ip": "192.168.1.1", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"} |
+----+-------+-----------------------------------------------------------------------------------------+
4 rows in SET (0.00 sec)
```

该表达式可以用于 SELECT 查询列表 ，WHERE/HAVING , ORDER/GROUP BY 中，但它不能用于设置值，也就是说 `SELECT lastlogininfo->'$.attr' FROM user` 这种用法是错误的，不管是 `->` 还是 `JSON_EXTRACT` 都不可以。但是可以使用虚拟列的方式实现（曲线救国）。

```sql
mysql> ALTER TABLE user ADD lastloginIP VARCHAR(15) GENERATED ALWAYS AS (lastlogininfo->'$.attr.ip') VIRTUAL;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> SELECT name, lastloginIP FROM user;
+-------+---------------+
| name  | lastloginIP   |
+-------+---------------+
| lucy  | "192.168.1.1" |
| andy  | "192.168.1.2" |
| light | "192.168.1.3" |
| Ash   | "192.168.1.4" |
+-------+---------------+
4 rows in SET (0.00 sec)
```

## 更新 JSON 字段数据

更新字段数据指的是更新当前的 JSON 字段的值，也就是说无法 `指派一个全新的 JSON OBJECT` 去替换它。

常用的三个方法，各有不同：

- `JSON_INSERT` 函数只有当属性不存在的时候，它才会将这个属性添加到对象中。
- `JSON_REPLACE` 函数只有在对象中找到该属性才会替换该属性。
- `JSON_SET` 函数，如果在对象中没有找到这个属性，就会添加这个属性到对象中，如果对象中有这个属性了，就会替换掉原来的属性。

```sql
/* 使用 JSON_INSERT 插入一个新的 key，并定为 +8 */
mysql> UPDATE user SET lastlogininfo=JSON_INSERT(lastlogininfo, '$.attr.locate', '+8') WHERE id=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
/* 使用 JSON_INSERT 插入一个新的 key，并定为 +9，但由于这个 key 已经存在，所以无修改 */
mysql> UPDATE user SET lastlogininfo=JSON_INSERT(lastlogininfo, '$.attr.locate', '+9') WHERE id=1;
Query OK, 0 rows affected (0.00 sec)
Rows matched: 1  Changed: 0  Warnings: 0

mysql> SELECT id, lastlogininfo FROM user;
+----+---------------------------------------------------------------------------------------------------------+
| id | lastlogininfo                                                                                           |
+----+---------------------------------------------------------------------------------------------------------+
|  1 | {"attr": {"ip": "192.168.1.1", "locate": "+8", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"} |
|  2 | {"attr": {"ip": "192.168.1.2", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"}                 |
|  3 | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"}                 |
|  4 | {"attr": {"ip": "192.168.1.4", "result": "fail"}, "time": "2020-01-08 10:10:48.000000"}                 |
+----+---------------------------------------------------------------------------------------------------------+
4 rows in SET (0.00 sec)

/* 使用 JSON_REPLACE 修改一个存在 key，并定为 +9 */
mysql> UPDATE user SET lastlogininfo=JSON_REPLACE(lastlogininfo, '$.attr.locate', '+9') WHERE id=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT id, lastlogininfo FROM user;
+----+---------------------------------------------------------------------------------------------------------+
| id | lastlogininfo                                                                                           |
+----+---------------------------------------------------------------------------------------------------------+
|  1 | {"attr": {"ip": "192.168.1.1", "locate": "+9", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"} |
|  2 | {"attr": {"ip": "192.168.1.2", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"}                 |
|  3 | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"}                 |
|  4 | {"attr": {"ip": "192.168.1.4", "result": "fail"}, "time": "2020-01-08 10:10:48.000000"}                 |
+----+---------------------------------------------------------------------------------------------------------+
4 rows in SET (0.00 sec)

/* 使用 JSON_SET 处理，如果在对象中没有找到这个属性，就会添加这个属性到对象中，如果对象中有这个属性了，就会替换掉原来的属性 */
mysql> UPDATE user SET lastlogininfo=JSON_SET(lastlogininfo, '$.attr.locate', '+9') WHERE id=2;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT id, lastlogininfo FROM user;
+----+---------------------------------------------------------------------------------------------------------+
| id | lastlogininfo                                                                                           |
+----+---------------------------------------------------------------------------------------------------------+
|  1 | {"attr": {"ip": "192.168.1.1", "locate": "+9", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"} |
|  2 | {"attr": {"ip": "192.168.1.2", "locate": "+9", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
|  3 | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"}                 |
|  4 | {"attr": {"ip": "192.168.1.4", "result": "fail"}, "time": "2020-01-08 10:10:48.000000"}                 |
+----+---------------------------------------------------------------------------------------------------------+
4 rows in SET (0.00 sec)

mysql> UPDATE user SET lastlogininfo=JSON_SET(lastlogininfo, '$.attr.locate', '+7') WHERE id=2;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT id, lastlogininfo FROM user;
+----+---------------------------------------------------------------------------------------------------------+
| id | lastlogininfo                                                                                           |
+----+---------------------------------------------------------------------------------------------------------+
|  1 | {"attr": {"ip": "192.168.1.1", "locate": "+9", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"} |
|  2 | {"attr": {"ip": "192.168.1.2", "locate": "+7", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
|  3 | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"}                 |
|  4 | {"attr": {"ip": "192.168.1.4", "result": "fail"}, "time": "2020-01-08 10:10:48.000000"}                 |
+----+---------------------------------------------------------------------------------------------------------+
4 rows in SET (0.00 sec)
```

综上所述，简单粗暴就用 JSON_SET() 处理。

## 删除 JSON 字段数据

这里可以分为仅仅删除 JSON 对象内部的某些字段，还是根据 JSON 内容删除对应的行。

### 仅删除 JSON 对象的字段

```sql
mysql> UPDATE user SET lastlogininfo=JSON_REMOVE(lastlogininfo,'$.attr.locate') WHERE id=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT id, lastlogininfo FROM user;
+----+---------------------------------------------------------------------------------------------------------+
| id | lastlogininfo                                                                                           |
+----+---------------------------------------------------------------------------------------------------------+
|  1 | {"attr": {"ip": "192.168.1.1", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"}                 |
|  2 | {"attr": {"ip": "192.168.1.2", "locate": "+7", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
|  3 | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"}                 |
|  4 | {"attr": {"ip": "192.168.1.4", "result": "fail"}, "time": "2020-01-08 10:10:48.000000"}                 |
+----+---------------------------------------------------------------------------------------------------------+
4 rows in SET (0.00 sec)

mysql> UPDATE user SET lastlogininfo=JSON_REMOVE(lastlogininfo,'$.attr') WHERE id=4;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT id, lastlogininfo FROM user;
+----+---------------------------------------------------------------------------------------------------------+
| id | lastlogininfo                                                                                           |
+----+---------------------------------------------------------------------------------------------------------+
|  1 | {"attr": {"ip": "192.168.1.1", "result": "fail"}, "time": "2020-01-07 21:07:43.000000"}                 |
|  2 | {"attr": {"ip": "192.168.1.2", "locate": "+7", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
|  3 | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"}                 |
|  4 | {"time": "2020-01-08 10:10:48.000000"}                                                                  |
+----+---------------------------------------------------------------------------------------------------------+
4 rows in SET (0.00 sec)
```

### 删除对应的行

其实这里又回到了查询的概念，只要能提取到想要的数据就行，还是要用到 JSON_EXTRACT 或者 ->。

```sql
mysql> DELETE FROM user WHERE JSON_EXTRACT(lastlogininfo, '$.attr.ip') = '192.168.1.1';
Query OK, 1 row affected (0.00 sec)

mysql> SELECT id, lastlogininfo FROM user;
+----+---------------------------------------------------------------------------------------------------------+
| id | lastlogininfo                                                                                           |
+----+---------------------------------------------------------------------------------------------------------+
|  2 | {"attr": {"ip": "192.168.1.2", "locate": "+7", "result": "fail"}, "time": "2020-01-07 21:12:43.000000"} |
|  3 | {"attr": {"ip": "192.168.1.3", "result": "fail"}, "time": "2020-01-07 21:16:50.000000"}                 |
|  4 | {"time": "2020-01-08 10:10:48.000000"}                                                                  |
+----+---------------------------------------------------------------------------------------------------------+
3 rows in SET (0.00 sec)
```

## 参考资料

- [深入了解 MySQL 的 JSON 数据类型（关系型数据库里的 NoSQL 初探）](https://learnku.com/laravel/t/13185/in-depth-understanding-of-json-data-type-of-mysql-nosql-in-relational-database)
- [MySQL 5.7 使用原生JSON类型的例子](https://www.jianshu.com/p/455d3d4922e1)
