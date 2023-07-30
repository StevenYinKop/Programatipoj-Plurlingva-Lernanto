---
title: shell编程3-expr, $(()), $[]
url: https://www.yuque.com/stevenyin/liv/yb42d5
---

<a name="9cdd4a78"></a>

# 运算符

<a name="c4dd9766"></a>

## 基本语法

1. `$((算式))`或`$[算式]`
2. `expr m + n`
3. `expr m - n`
4. `expr *,/,%` **乘除取余**

<a name="Example"></a>

## Example

<a name="79af7240"></a>

### 计算 (2 + 3) * 4

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell06_expr.sh
```

```sh
  #!/bin/bash

  # Example01
  echo "use \$(())"
  RESULT1=$(((2+3)*4))
  echo "\$(((2+3)*4))=$RESULT1"

  #Example02
  echo "use \$[]"
  RESULT2=$[(2+3)*4]
  echo "\$[(2+3)*4]=$RESULT2"

  #Example03
  echo "use expr"

  TEMP=`expr 2 + 3`
  RESULT3=`expr $TEMP * 4`
  echo "expr ...= $RESULT3"
```

执行

```sh
  use $(())
  $(((2+3)*4))=20
  use $[]
  $[(2+3)*4]=20
  use expr
  expr ...= 20
```

三种方式计算的结果是一样的, 毕竟都是简单的运算操作

<a name="8ea87680"></a>

### 传入两个参数, 计算两个数字的和

继续在刚刚的脚本文件中编写:

```sh
  #Example04
  echo "caculate $1+$2"
  echo "SUM=$[$1+$2]"
```

再次执行

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# sh shell06_expr.sh 3 4
  caculate 3+4
  SUM=7
```
