---
layout: wiki
title: SQLite 的学习
categories: [SQLite, Sytanx]
description: SQLite 的学习
keywords: SQLite, Sytanx
---

# SQLITE 的学习

sqlite 是一个非常轻量化的数据库，用于存储个人少量的数据，简单够用。同时它对 python 的支持相当好。

## 点命令

第一次使用 sqlite 的时候连退出都不会，想起了被 vi 支配的恐惧，后来才知道 sqlite 有一系列点命令，通过这些命令可以简化一些 SQL 语句。这些命令不属于 SQL 的定义，仅仅为了更好用。

```shell
$ sqlite3
SQLite version 3.3.6
Enter ".help" for instructions
sqlite>
```



常用点命令：

| 命令               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| .backup ?DB? FILE  | 备份 DB 数据库（默认是 "main"）到 FILE 文件。                |
| .bail ON\|OFF      | 发生错误后停止。默认为 OFF。                                 |
| .databases         | 列出数据库的名称及其所依附的文件。                           |
| .dump ?TABLE?      | 以 SQL 文本格式转储数据库。如果指定了 TABLE 表，则只转储匹配 LIKE 模式的 TABLE 表。 |
| .echo ON\|OFF      | 开启或关闭 echo 命令。                                       |
| .exit              | 退出 SQLite 提示符。                                         |
| .explain ON\|OFF   | 开启或关闭适合于 EXPLAIN 的输出模式。如果没有带参数，则为 EXPLAIN on，及开启 EXPLAIN。 |
| .header(s) ON\|OFF | 开启或关闭头部显示。                                         |
| .help              | 显示消息。                                                   |
| .import FILE TABLE | 导入来自 FILE 文件的数据到 TABLE 表中。                      |
| .indices ?TABLE?   | 显示所有索引的名称。如果指定了 TABLE 表，则只显示匹配 LIKE 模式的 TABLE 表的索引。 |
| .load FILE ?ENTRY? | 加载一个扩展库。                                             |
| .log FILE\|off     | 开启或关闭日志。FILE 文件可以是 stderr（标准错误）/stdout（标准输出）。 |
| .mode MODE         | 设置输出模式，MODE 可以是下列之一：<br>-**csv** 逗号分隔的值 <br>-**column** 左对齐的列 <br>-**html** HTML 的代码 <br>-**insert** TABLE 表的 SQL 插入（insert）语句<br>-**line** 每行一个值 <br>-**list** 由 .separator 字符串分隔的值 <br>-**tabs** 由 Tab 分隔的值 <br>-**tcl** TCL 列表元素 |
| .nullvalue STRING | 在 NULL 值的地方输出 STRING 字符串。 |
| .output FILENAME | 发送输出到 FILENAME 文件。 |
| .output stdout | 发送输出到屏幕。 |
| .print STRING... | 逐字地输出 STRING 字符串。 |
| .prompt MAIN CONTINUE | 替换标准提示符。 |
| .quit | 退出 SQLite 提示符。 |
| .read FILENAME | 执行 FILENAME 文件中的 SQL。 |
| .schema ?TABLE? | 显示 CREATE 语句。如果指定了 TABLE 表，则只显示匹配 LIKE 模式的 TABLE 表。 |
| .separator STRING | 改变输出模式和 .import 所使用的分隔符。 |
| .show | 显示各种设置的当前值。 |
| .stats ON\|OFF | 开启或关闭统计。 |
| .tables ?PATTERN? | 列出匹配 LIKE 模式的表的名称。 |
| .timeout MS | 尝试打开锁定的表 MS 毫秒。 |
| .width NUM NUM | 为 "column" 模式设置列宽度。 |
| .timer ON\|OFF | 开启或关闭 CPU 定时器。 |

有了上面这张表，就可以用 .exit 或者 .quit 退出 SQLite Shell 了。

### 格式化输出

```shell
sqlite>.header on
sqlite>.mode column
sqlite>.timer on
sqlite>
```

```shell
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0
CPU Time: user 0.000000 sys 0.000000
```

### sqlite_master 表格

主表中保存数据库表的关键信息，并把它命名为 sqlite_master。

```shell
sqlite>.schema sqlite_master
CREATE TABLE sqlite_master (
  type text,
  name text,
  tbl_name text,
  rootpage integer,
  sql text
);
```

## 语法

### 注释

SQLite 注释是附加的注释，可以在 SQLite 代码中添加注释以增加其可读性，他们可以出现在任何空白处，包括在表达式内和其他 SQL 语句的中间，但它们不能嵌套。

SQL 注释以两个连续的 "-" 字符（ASCII 0x2d）开始，并扩展至下一个换行符（ASCII 0x0a）或直到输入结束，以先到者为准。

您也可以使用 C 风格的注释，以 "/\*" 开始，并扩展至下一个 "*/" 字符对或直到输入结束，以先到者为准。SQLite的注释可以跨越多行。

```shell
sqlite>.help -- 这是一个简单的注释
```

### 语句

所有的 SQLite 语句可以以任何关键字开始，如 SELECT、INSERT、UPDATE、DELETE、ALTER、DROP 等，所有的语句以分号（;）结束。其使用方法类似标准 SQL 语法。

## 数据类型

SQLite 数据类型是一个用来指定任何对象的数据类型的属性。SQLite 中的每一列，每个变量和表达式都有相关的数据类型。

您可以在创建表的同时使用这些数据类型。SQLite 使用一个更普遍的动态类型系统。在 SQLite 中，值的数据类型与值本身是相关的，而不是与它的容器相关。

### SQLite 存储类

| 存储类   | 描述                                                         |
| ------- | ----------------------------------------------------------- |
| NULL    | 值是一个 NULL 值。                                            |
| INTEGER	| 值是一个带符号的整数，根据值的大小存储在 1、2、3、4、6 或 8 字节中。  |
| REAL	  | 值是一个浮点值，存储为 8 字节的 IEEE 浮点数字。                   |
| TEXT	  | 值是一个文本字符串，使用数据库编码（UTF-8、UTF-16BE 或 UTF-16LE）存储。|
| BLOB	  | 值是一个 blob 数据，完全根据它的输入存储。|

## 数据库相关操作

### 创建数据库
```shell
$sqlite3 DatabaseName.db
```

如果创建成功，会直接进入 sqlite shell，同时也可以查询 `.databases`来检查它是否在数据库列表中。

### 导出数据库

```shell
sqlite3 testDB.db .dump > testDB.sql
```

### 附加数据库 

当在同一时间有多个数据库可用，您想使用其中的任何一个。SQLite 的 ATTACH DATABASE 语句是用来选择一个特定的数据库，使用该命令后，所有的 SQLite 语句将在附加的数据库下执行。

```shell
sqlite> ATTACH DATABASE 'testDB.db' as 'TEST';
```

```shell
sqlite>.database
seq  name             file
---  ---------------  ----------------------
0    main             /home/sqlite/testDB.db
2    test             /home/sqlite/testDB.db
```

数据库名称 main 和 temp 被保留用于主数据库和存储临时表及其他临时数据对象的数据库。这两个数据库名称可用于每个数据库连接，且不应该被用于附加，否则将得到一个警告消息，如下所示：

```shell
sqlite>  ATTACH DATABASE 'testDB.db' as 'TEMP';
Error: database TEMP is already in use
sqlite>  ATTACH DATABASE 'testDB.db' as 'main';
Error: database main is already in use；
```

### 分离数据库

SQLite的 DETACH DTABASE 语句是用来把命名数据库从一个数据库连接分离和游离出来，连接是之前使用 ATTACH 语句附加的。如果同一个数据库文件已经被附加上多个别名，DETACH 命令将只断开给定名称的连接，而其余的仍然有效。您无法分离 main 或 temp 数据库。

```shell
sqlite>DETACH DATABASE 'Alias-Name';
```

假设在前面的章节中已经创建了一个数据库，并给它附加了 'test' 和 'currentDB'，使用 .database 命令，我们可以看到：

```shell
sqlite>.databases
seq  name             file
---  ---------------  ----------------------
0    main             /home/sqlite/testDB.db
2    test             /home/sqlite/testDB.db
3    currentDB        /home/sqlite/testDB.db
```

现在，让我们尝试把 'currentDB' 从 testDB.db 中分离出来，如下所示：

```shell
sqlite> DETACH DATABASE 'currentDB';
```

现在，如果检查当前附加的数据库，您会发现，testDB.db 仍与 'test' 和 'main' 保持连接。

```shell
sqlite>.databases
seq  name             file
---  ---------------  ----------------------
0    main             /home/sqlite/testDB.db
2    test             /home/sqlite/testDB.db
```
### 运算符

#### 算术运算符

|运算符	|描述       |实例       |
|-------|----------|----------|
|+	      |加法 - 把运算符两边的值相加|	a + b 将得到 30|
|-	      |减法 - 左操作数减去右操作数|	a - b 将得到 -10|
|*	      |乘法 - 把运算符两边的值相乘|	a * b 将得到 200|
|/       |除法 - 左操作数除以右操作数|	b / a 将得到 2|
|%	      |取模 - 左操作数除以右操作数后得到的余数|	b % a will give 0|

#### 比较运算符

|运算符|	描述|	实例|
|-----|-----|----|
|==   |检查两个操作数的值是否相等，如果相等则条件为真。|(a == b) 不为真。 |
|=	   |检查两个操作数的值是否相等，如果相等则条件为真。|(a = b) 不为真。  |
|!=   |检查两个操作数的值是否相等，如果不相等则条件为真。|(a != b) 为真。  |
|<>	|检查两个操作数的值是否相等，如果不相等则条件为真。|(a <> b) 为真。  |
|>	   |检查左操作数的值是否大于右操作数的值，如果是则条件为真。|(a > b) 不为真。|
|<    |检查左操作数的值是否小于右操作数的值，如果是则条件为真。|(a < b) 为真。  |
|>=	|检查左操作数的值是否大于等于右操作数的值，如果是则条件为真。|(a >= b) 不为真。|
|<=	|检查左操作数的值是否小于等于右操作数的值，如果是则条件为真。|(a <= b) 为真。|
|!<	|检查左操作数的值是否不小于右操作数的值，如果是则条件为真。|(a !< b) 为假。|
|!>	|检查左操作数的值是否不大于右操作数的值，如果是则条件为真。|(a !> b) 为真。|

#### 逻辑运算符

|运算符     |描述         |
|----------|------------|
|AND        |AND 运算符允许在一个 SQL 语句的 WHERE 子句中的多个条件的存在。|
|BETWEEN	   |BETWEEN 运算符用于在给定最小值和最大值范围内的一系列值中搜索值。|
|EXISTS	   |EXISTS 运算符用于在满足一定条件的指定表中搜索行的存在。|
|IN         |IN 运算符用于把某个值与一系列指定列表的值进行比较。|
|NOT IN	   |IN 运算符的对立面，用于把某个值与不在一系列指定列表的值进行比较。|
|LIKE       |LIKE 运算符用于把某个值与使用通配符运算符的相似值进行比较。|
|GLOB       |GLOB 运算符用于把某个值与使用通配符运算符的相似值进行比较。GLOB 与 LIKE 不同之处在于，它是大小写敏感的。|
|NOT        |NOT 运算符是所用的逻辑运算符的对立面。比如 NOT EXISTS、NOT BETWEEN、NOT IN，等等。它是否定运算符。|
|OR         |OR 运算符用于结合一个 SQL 语句的 WHERE 子句中的多个条件。|
|IS NULL    |NULL 运算符用于把某个值与 NULL 值进行比较。|
|IS         |IS 运算符与 = 相似。|
|IS NOT	   |IS NOT 运算符与 != 相似。|
|\|\|	      |连接两个不同的字符串，得到一个新的字符串。|
|UNIQUE	   |UNIQUE 运算符搜索指定表中的每一行，确保唯一性（无重复）。|

#### 位运算符

|运算符|描述                                                   |实例                            |
|-----|------------------------------------------------------|-------------------------------|
|&    |如果同时存在于两个操作数中，二进制 AND 运算符复制一位到结果中。  |(A & B) 将得到 12，即为 0000 1100|
|\|	|如果存在于任一操作数中，二进制 OR 运算符复制一位到结果中。       |(A | B) 将得到 61，即为 0011 1101|
|~    |二进制补码运算符是一元运算符，具有"翻转"位效应，即0变成1，1变成0。|	(~A ) 将得到 -61，即为 1100 0011，一个有符号二进制数的补码形式。|
|<<   |二进制左移运算符。左操作数的值向左移动右操作数指定的位数。	      |A << 2 将得到 240，即为 1111 0000|
|>>   |二进制右移运算符。左操作数的值向右移动右操作数指定的位数。	      |A >> 2 将得到 15，即为 0000 1111|

## 表的操作

### 创建表

```shell
CREATE TABLE database_name.table_name(
   column1 datatype  PRIMARY KEY(one or more columns),
   column2 datatype,
   column3 datatype,
   .....
   columnN datatype,
);
```

```shell
sqlite> CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);
```

创建表之后，可以使用 SQLIte 命令中的 .tables 命令来验证表是否已成功创建
```shell
sqlite>.tables
COMPANY     DEPARTMENT
```

可以使用 SQLite .schema 命令得到表的完整信息，如下所示：

```shell
sqlite>.schema COMPANY
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);
```

### 删除表

 DROP TABLE 语句用来删除表定义及其所有相关数据、索引、触发器、约束和该表的权限规范。

 ```shell
 DROP TABLE database_name.table_name;
 ```

 ```shell
sqlite>.tables
COMPANY       test.COMPANY
sqlite>DROP TABLE COMPANY;
sqlite>.tables
sqlite>
```

## 数据操作

### insert

```shell
INSERT INTO TABLE_NAME (column1, column2, column3,...columnN)
VALUES (value1, value2, value3,...valueN);

INSERT INTO TABLE_NAME VALUES (value1, value2, value3,...valueN);
```

### select

```shell
SELECT column1, column2, columnN FROM table_name;

SELECT * FROM table_name;
```

```shell
sqlite>.header on
sqlite>.mode column
sqlite> SELECT * FROM COMPANY;
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0
```

```shell
sqlite> SELECT ID, NAME, SALARY FROM COMPANY;
ID          NAME        SALARY
----------  ----------  ----------
1           Paul        20000.0
2           Allen       15000.0
3           Teddy       20000.0
4           Mark        65000.0
5           David       85000.0
6           Kim         45000.0
7           James       10000.0
```

#### 设置输出列的宽度

```shell
sqlite>.width 10, 20, 10
```

### update

```shell
UPDATE table_name
SET column1 = value1, column2 = value2...., columnN = valueN
WHERE [condition];
```

如果没有 where 子句，那么表格的某一列的值全部更新。

### delete

```shell
DELETE FROM table_name
WHERE [condition];
```

如果没有 where 子句，那么将删除表格的所有记录。

### where 子句

WHERE 子句用于指定从一个表或多个表中获取数据的条件。

如果满足给定的条件，即为真（true）时，则从表中返回特定的值。您可以使用 WHERE 子句来过滤记录，只获取需要的记录。

WHERE 子句不仅可用在 SELECT 语句中，它也可用在 UPDATE、DELETE 语句中。

WHERE 可以完美配合 `运算符` 里提到的符号进行逻辑判断。

### like 子句

SQLite 的 LIKE 运算符是用来匹配通配符指定模式的文本值。如果搜索表达式与模式表达式匹配，LIKE 运算符将返回真（true），也就是 1。这里有两个通配符与 LIKE 运算符一起使用：

- 百分号 （%）
- 下划线 （_）

百分号（%）代表零个、一个或多个数字或字符。下划线（_）代表一个单一的数字或字符。这些符号可以被组合使用。

#### 实例

|语句                      |描述                |
|--------------------------|-------------------|
|WHERE SALARY LIKE '200%'  |查找以 200 开头的任意值|
|WHERE SALARY LIKE '%200%'	|查找任意位置包含 200 的任意值|
|WHERE SALARY LIKE '_00%'	|查找第二位和第三位为 00 的任意值|
|WHERE SALARY LIKE '2_%_%'	|查找以 2 开头，且长度至少为 3 个字符的任意值|
|WHERE SALARY LIKE '%2'	   |查找以 2 结尾的任意值|
|WHERE SALARY LIKE '_2%3'	|查找第二位为 2，且以 3 结尾的任意值|
|WHERE SALARY LIKE '2___3'	|查找长度为 5 位数，且以 2 开头以 3 结尾的任意值|


### glob 子句

SQLite 的 GLOB 运算符是用来匹配通配符指定模式的文本值。如果搜索表达式与模式表达式匹配，GLOB 运算符将返回真（true），也就是 1。与 LIKE 运算符不同的是，GLOB 是大小写敏感的，对于下面的通配符，它遵循 UNIX 的语法。

- 星号 （*）
- 问号 （?）

星号（*）代表零个、一个或多个数字或字符。问号（?）代表一个单一的数字或字符。这些符号可以被组合使用。

#### 实例

|语句                      |描述|
|--------------------------|----|
|WHERE SALARY GLOB '200*'  |查找以 200 开头的任意值|
|WHERE SALARY GLOB '*200*'	|查找任意位置包含 200 的任意值|
|WHERE SALARY GLOB '?00*'	|查找第二位和第三位为 00 的任意值|
|WHERE SALARY GLOB '2??'	|查找以 2 开头，且长度至少为 3 个字符的任意值|
|WHERE SALARY GLOB '*2'	   |查找以 2 结尾的任意值|
|WHERE SALARY GLOB '?2*3'	|查找第二位为 2，且以 3 结尾的任意值|
|WHERE SALARY GLOB '2???3'	|查找长度为 5 位数，且以 2 开头以 3 结尾的任意值|

### limit 子句

SQLite 的 LIMIT 子句用于限制由 SELECT 语句返回的数据数量。

```shell
SELECT column1, column2, columnN 
FROM table_name
LIMIT [no of rows]
```

```shell
SELECT column1, column2, columnN 
FROM table_name
LIMIT [no of rows] OFFSET [row num]
```

SQLite 引擎将返回从下一行开始直到给定的 OFFSET 为止的所有行。

#### 实例

```shell
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0

sqlite> SELECT * FROM COMPANY LIMIT 6;

ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0

sqlite> SELECT * FROM COMPANY LIMIT 3 OFFSET 2;

ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
```

### order by 子句

SQLite 的 ORDER BY 子句是用来基于一个或多个列按升序或降序顺序排列数据。

```shell
SELECT column-list 
FROM table_name 
[WHERE condition] 
[ORDER BY column1, column2, .. columnN] [ASC | DESC];
```


### group by 子句

SQLite 的 GROUP BY 子句用于与 SELECT 语句一起使用，来对相同的数据进行分组。

在 SELECT 语句中，GROUP BY 子句放在 WHERE 子句之后，放在 ORDER BY 子句之前。

```shell
SELECT column-list
FROM table_name
WHERE [ conditions ]
GROUP BY column1, column2....columnN
ORDER BY column1, column2....columnN
```

这里的 select 想要查处的列基本都有聚合函数的影子。

### having 子句

HAVING 子句允许指定条件来过滤将出现在最终结果中的分组结果。

WHERE 子句在所选列上设置条件，而 HAVING 子句则在由 GROUP BY 子句创建的分组上设置条件。

```shell
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
```

在一个查询中，HAVING 子句必须放在 GROUP BY 子句之后，必须放在 ORDER BY 子句之前。下面是包含 HAVING 子句的 SELECT 语句的语法：

```shell
SELECT column1, column2
FROM table1, table2
WHERE [ conditions ]
GROUP BY column1, column2
HAVING [ conditions ]
ORDER BY column1, column2
```
