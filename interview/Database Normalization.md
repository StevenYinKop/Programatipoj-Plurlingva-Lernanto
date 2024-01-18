# Database Normalization



## Normalized Table are:

1. Easier to Understand
2. Easier to enhance and extend
3. Protected from:
    1. insertion anomalies
    2. update anomalies
    3. deletion anomalies

## First Normal Form

1. Using row order to convey information is not permitted
2. Mixing data types within the same column is not permitted
3. Having a table without a primary key is not permitted
4. Repeating groups are not permitted

## Second Normal Form

> Each non-key attribute must depend on the entire primary key.

| Player_ID | Item_Type    | Item_Quantity |
|-----------|--------------|---------------|
| steven    | amulets      | 1             |
| steven    | rings        | 2             |
| jason     | copper coins | 20            |
| tom       | shields      | 2             |
| tom       | arrows       | 5             |
| tom       | cooper coins | 10            |
| tom       | rings        | 7             |

| Player_ID | Player_Rating |
|-----------|---------------|
| steven    | Intermediate  |
| jason     | Beginner      |
| tom       | Advanced      |
| tina      | Beginner      |

Primary key: {Player_ID, Item_Type}
Non-key attribute: {Item_Quantity}

## Third Normal Form

> Every non-key attribute in a table should depend on the key, the whole key, and nothing but the key.

Player
| Player_ID | Player_Rating | Player_Skill_Level |
|-----------|---------------|--------------------|
| steven | Intermediate | 4 |
| jason | Beginner | 4 |
| tom | Advanced | 8 |
| tina | Beginner | 1 |

Player_Skill_Levels
| Player_ID | Player_Rating | Player_Skill_Level |
|-----------|---------------|--------------------|
| steven | Intermediate | 4 |
| jason | Beginner | 4 |
| tom | Advanced | 8 |
| tina | Beginner | 1 |

## Boyce-Codd Normal Form:

> Every attribute in a table should depend on the key, the whole key, and nothing but the key.

## Fourth Normal Form

> Multivalued dependencies in a table must be multivalued dependencies on the keys.

## Fifth Normal Form

> The table(which must be in 4NF) cannot be describable as the logical result of joining some other tables together.


不满足任何范式的表结构如下：

| 学生信息                 |
|----------------------|
| 张三,23,180,2019-04-01 |
| 李四,24,167,2019-04-01 |
| 王五,23,177,2019-04-01 |


## 第一范式:

1. 数据库所有字段都只有单一属性
2. 单一属性是由基本数据类型构成的
3. 数据库的表都是二维的(行与列)
4. 字段中的数据不能在被拆分，已经是最小的粒度了

### 第一范式样表

| 学号        | 姓名      | 系名   | 班主任  | 课名     | 得分  |
|-----------|---------|------|------|--------|-----|
| 201311035 | Steven  | 计算机系 | Tom  | 数据库设计  | 90  |
| 201311035 | Steven  | 计算机系 | Tom  | 高等数学   | 55  |
| 201311035 | Steven  | 计算机系 | Tom  | Java编程 | 88  |
| 201309001 | Jason   | 汉语系  | Wang | 汉语语言文学 | 70  |
| 201309001 | Jason   | 汉语系  | Wang | 现代汉语   | 100 |
| 201430201 | Michael | 生物系  | Lee  | 高等数学   | 90  |
| 201430201 | Michael | 生物系  | Lee  | 大学英语   | 90  |
| 201430201 | Michael | 生物系  | Lee  | 生物基础   | 90  |

### 问题：

#### 1. 出现了大量的重复数据

`姓名`、`系名`、`班主任`等，都出现了大量的重复数据

#### 2. 出现了新增异常，修改异常和删除异常

##### 新增异常

如果学校新增了一个系，名为表演系。但是并没有进行招生。在这种情况下，这张表中无法体现表演系的任何信息。也就是`新增异常`

##### 修改异常

如果班主任或任一其他重复数据发生变更，但是由于一些不可抗力或者代码bug，导致数据没有完全更新成功，这个时候就会出现数据不统一的情况，如同一个系对应两名不同的班主任。

##### 删除异常

如果我们删除Jason用户，删除完成后，连`汉语系`的数据也消失了。

## 第二范式

1. 必须符合第一范式
2. 表必须要有主键（一列或者多列）
3. 其他字段必须和主键有着明确的依赖关系

### 问题：

1. 只能解决第一范式中，数据冗余的问题，无法解决新增异常，修改异常和删除异常
2. 从第一范式样表中可以看到，以`学号`作为主键的情况下，`学号`和`姓名`,`系名`,`班主任`都有着依赖关系,但是`课名`和`分数`

### 第二范式样表

