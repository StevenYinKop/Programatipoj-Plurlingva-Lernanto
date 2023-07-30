---
title: MySQL事务与锁机制
url: https://www.yuque.com/stevenyin/liv/vmxrpu
---

<a name="Eq2Tt"></a>

## ![image.png](../assets/vmxrpu/1632920508311-3a6bbb9e-113a-41a8-8615-29c00ebfee15.png)

<a name="jbpnH"></a>

## 数据库事务的典型场景

1. 下单,资金,物流需要同时完成
2. 12306网站<接续换乘>功能, 需要买两张票作为中转站,所以两张票要同时购买成功. <a name="ABhU5"></a>

## 数据库事务

![image.png](../assets/vmxrpu/1632919313754-61258949-e6a7-462e-8bad-5f1db46813c8.png)

> 事务是数据库管理系统(DBMS)执行过程中的一个逻辑单位, 由一个有限的数据库操作序列构成.

<a name="KbCzM"></a>

## 数据库事务的四大特性

![image.png](../assets/vmxrpu/1632919451273-7d99296d-670f-43d0-b746-889ddc3fbe85.png)
undo log 实现原子性
redo log 实现持久性
隔离性

开启事务:

1. DML自动开启事务
2. begin关键字

结束事务:

1. 自动提交 commit
2. rollback
3. 连接断开, 事务自动回滚.

![image.png](../assets/vmxrpu/1632920236065-162bf612-12bb-48ef-9bcc-e7f2b4bb6350.png)
![image.png](../assets/vmxrpu/1632920214137-df0c5aad-1a2a-4692-8b2b-4334f7f81a77.png)	![image.png](../assets/vmxrpu/1632920282239-45bb7427-e0bc-445d-974e-ea6ae5709a46.png)

![image.png](../assets/vmxrpu/1632920306377-11631c47-8345-4822-952f-96d1c16100dd.png)
![image.png](../assets/vmxrpu/1632920372025-0b3d5210-d85d-4d32-8f5f-091a26f05292.png)
![image.png](../assets/vmxrpu/1632920590261-7897e4c2-2cdb-43bb-99fc-c6f50270ed84.png)

![image.png](../assets/vmxrpu/1632920718809-b5727052-b1cb-409f-9847-6cc9346097a2.png)

![image.png](../assets/vmxrpu/1632920753374-c18bf984-8aad-4ce6-b704-31a233b5b5f8.png)
![image.png](../assets/vmxrpu/1632927934264-fefe6ab5-aef0-40ea-b704-212f6c4662da.png)
![image.png](../assets/vmxrpu/1632928374816-4818cf5b-e9d8-4ae0-a232-43ef5d8a48cf.png)

<https://dev.mysql.com/doc/refman/5.7/en/innodb-locking-transaction-model.html>

![image.png](../assets/vmxrpu/1632928576347-2980c64f-fb9b-409d-8fe7-c08034b8ad0a.png)

![image.png](../assets/vmxrpu/1632928677484-c46bb59e-495c-43a8-a3ed-0a2b140c753a.png)

如果给一行数据加上共享锁, 那么存储引擎就会给**表**加上"意向共享锁"
如果给一行数据加上排他锁, 那么存储引擎就会给**表**加上"意向排他锁"

1. 为什么一张表没有索引, 加行锁会锁住整张表?

一张表可不可能没有索引? 不可能, 有隐藏的聚集索引
没有主键 -- 全表扫描  -- 把所有隐藏的聚集索引全部锁住

![image.png](../assets/vmxrpu/1632929484820-b529c2bc-2411-47a1-be6f-ecd4f9778cf3.png)
N 个 records
N+1 个 gaps
next-key: gap和右侧的record

![image.png](../assets/vmxrpu/1632929651667-de64317a-1cc2-4d7b-ac8b-cd883e6a2ba1.png)
![image.png](../assets/vmxrpu/1632929655238-8c8a0ded-bc14-4541-914c-55a4ded70e7b.png)
间隙锁最大的作用就是: 阻塞插入 -> 就是说可以解决幻读问题
![image.png](../assets/vmxrpu/1632929864157-3ae45b74-5ffc-4a4f-9ae3-2dd1b1256158.png)
![image.png](../assets/vmxrpu/1632930091385-dbf6a7ae-6333-4dbd-baf1-b59bc79ae034.png)

![image.png](../assets/vmxrpu/1632930137389-46b8d78e-0721-46ce-b4e3-fb5b79b1d70c.png)
![image.png](../assets/vmxrpu/1632930151517-e40a000c-2e5c-448d-9ed1-ad5ff8c3213e.png)
