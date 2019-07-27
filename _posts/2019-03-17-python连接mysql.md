---
layout: post
title: Python 连接 MySQL
categories: [Python, 逃离CSDN]
description: 两种方式连接 MySQL 库，以及基本操作
keywords: Python, 逃离CSDN
---

# Python 连接 MySQL

使用接口 Python DB API，两种情况：

- python2.7，使用 Python-MySQL connector，载入语句 `import MySQLdb`
- python3.4，安装 pymysql 模块，载入语句 `import pymysql`

## Connection对象：


创建方法：`pymysql.Connect(host,port,user,passwd,db)`

支持方法： 

- 1、cursor()，使用该连接创建并返回游标 
- 2、commit()，提交当前事务 
- 3、rollback()，回滚当前事务 
- 4、close()，关闭连接 

## cursor游标对象：用于执行查询和获取结果 

支持方法： 

- 1、execute(op,[args])，执行一个数据库查询和命令 
- 2、fetchone()，取得结果集的下一行 
- 3、fetchmany(size)，取得结果集的下几行 
- 4、fetchall()，取得结果集的剩下的所有行 
- 5、rowcount，最近一次execute返回数据的行数或影响行数 
- 6、close()，关闭游标对象

## select查询数据操作过程

- 开始 
- 创建connection 
- 创建cursor 
- 使用cursor.excute()执行select语句 
- 使用cursor.fetch*()获取并处理数据 
- 关闭cursor 
- 关闭connection 
-结束

## insert/update/delete更新数据库操作过程

- 开始
- 创建connection 
- 创建cursor 
- 使用cursor.excute()执行insert/update/delete语句 
  -出现异常：使用connection.rollback()回滚事务 
  - 未出现异常：使用connection.commit()提交事务 
- 关闭cursor 
- 关闭connection 
- 结束
