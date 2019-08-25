---
layout: wiki
title: SQL基础语句
categories: SQL
description: SQL的基础语句，等待持续更新...
keywords: SQL
---

# SQL基础语句

## 常用

- select
- insert
- update
- delet

select：查找

```sql
    SELECT 列名称 FROM 表名称
    SELECT * FROM 表名称
```

insert：插入新行

```sql
    INSERT INTO 表名称 VALUES (值1, 值2,....)
    INSERT INTO 表名称 (列1, 列2,...) VALUES (值1, 值2,....)
```

update：修改表中数据

```sql
    UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
```

delete：删除某一行

```sql
    DELETE FROM 表名称 WHERE 列名称 = 值
    DELETE FROM table_name 删除所有行
```

## 判断条件

- distinct
- where
- and
- or
- order by

distinct：用于返回唯一不同的值

```sql
    SELECT DISTINCT 列名称 FROM 表名称
```

where：判断条件

```sql
    SELECT 列名称 FROM 表名称 WHERE 列 运算符 值    # 若值为文本值，需要加引号，数值不需要
```

and:条件且运算

```sql
    条件 = 列 运算符 值
    SELECT 列名称 FROM 表名称 WHERE 条件1 AND 条件2 [AND 条件3]
```

or:条件或运算

```sql
    条件 = 列 运算符 值
    SELECT 列名称 FROM 表名称 WHERE 条件1 OR 条件2 [OR 条件3]
```

order by：根据指定的列对结果集进行排序，默认是升序

```sql
    SELECT 列名称 FROM 表名称 ORDER BY 列 [ASC|DESC]
```
