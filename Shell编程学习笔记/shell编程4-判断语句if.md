---
title: shell编程4-判断语句if
url: https://www.yuque.com/stevenyin/liv/dihu7g
---

<a name="b5d04490"></a>

# 判断语句

<a name="c4dd9766"></a>

## 基本语法

`[ condition ]`: 非空返回`true`, 可使用`$?`验证(`0`为`true`, >1位`false`)

例如:

1. `[ abc ]`: 返回`true`
2. `[]`: 返回`false`
3. `[ condition ] && echo OK || echo notOK`: 条件满足则往下面走

<a name="45b540e9"></a>

## 常用判断条件

| 符号 | 含义 |
| --- | --- |
| `=` | 字符串比较 |
| `-lt` | 小于 |
| `-le` | 小于等于 |
| `-eq` | 等于 |
| `-gt` | 大于 |
| `-ge` | 大于等于 |
| `-ne` | 不等于 |
|  |  |
| `-r` | 对文件有读权限 |
| `-w` | 对文件有写权限 |
| `-x` | 对文件有执行权限 |
|  |  |
| `-f` | 文件存在并且是一个常规的文件 |
| `-e` | 文件存在 |
| `-d` | 文件存在且是目录 |

<a name="Example"></a>

## Example

1. 判断`"ok"`是否等于`"ok"`

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell07_condition.sh
```

```sh
  #!/bin/bash
  [ "ok" = "ok" ] && echo "ok" || echo "not ok"
  [ "ok" = "not ok" ] && echo "ok" || echo "not ok"
```

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# sh shell07_condition.sh
  ok
  not ok
```

2. 判断`23`是否大于`22`

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell07_condition.sh
```

```sh
  #!/bin/bash
  if [ 23 -gt 22 ]
  then
      echo "23 > 22"
  fi
```

      [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# sh shell07_condition.sh
      23 > 22

3. 判断`/root/shell07_condition.sh`目录中的文件是否存在

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell07_condition.sh
```

```sh
  #!/bin/bash
  FILE_NAME=/root/condition.txt
  if [ -e $FILE_NAME ]
  then
      echo "$FILE_NAME is exist"
  fi
```

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# sh shell07_condition.sh
  /root/condition.txt is not exist
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# touch condition.txt
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# sh shell07_condition.sh
  /root/condition.txt is exist
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]#
```
