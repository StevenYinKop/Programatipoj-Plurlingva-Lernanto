---
title: shell编程6-for...in, for(()),while
url: https://www.yuque.com/stevenyin/liv/lgub0v
---

<a name="a15e8f64"></a>

# for循环

<a name="c4dd9766"></a>

## 基本语法

1. `for ... in`

```sh
for 变量 in 值1 值2 值3
  do
    逻辑语句
  done
```

2. `for(())`

```sh
  for(( 初始值;循环控制条件;变量变化 ))
    do
      逻辑语句
    done
```

<a name="Example"></a>

## Example

1. 打印命令行输入的参数信息(使用*和@)

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell10_for.sh
```

```sh
#!/bin/bash

for i in "$*"
  do
    echo "$i"
  done

echo "======split======"

for i in "$@"
  do
    echo "$i"
  done
```

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# chmod +x shell10_for.sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell10_for.sh 1 2 3 45
1 2 3 45
======split======
1
2
3
45
```

之前看起来`$*`和`$@`好像没有区别, 现在就能很明显的发现
`_$*_`*会将参数看做是一个整体, 而*`_$@_`*则是分开处理*

2. 从1加到100, 并显示结果

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell10_for.sh
```

```sh
#!/bin/bash
for((i=1;i<=100;i++))
  do
    SUM=$[$SUM+$i]
  done
echo "sum=$SUM"
```

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell10_for.sh 1 2 3 45
sum=5050
```

3. 输入两个参数`$1`, `$2`, 且前`$1<$2`, 计算`$1+...+$2`的值是多少?

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell10_for.sh
```

```sh
#!/bin/bash
for((i=$1;i<=$2;i++))
  do
   SUM=$[$SUM+$i]
  done
echo "$1+...+$2=$SUM"
```

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell10_for.sh 1 50
1+...+50=1275
```

<a name="9861eb98"></a>

# while循环

<a name="c4dd9766-1"></a>

## 基本语法

```sh
while [ 条件判断式 ]
  do
    逻辑语句
  done
```

<a name="ffef48cb"></a>

## Example(使用`while`循环实现上面的三个Demo)

1. 打印命令行输入的参数信息(使用*和@)

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell11_while.sh
```

```sh
#!/bin/bash
while [ 0 -ne $# ]
  do
    echo "$1"
    shift
  done
```

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# chmod +x shell11_while.sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell11_while.sh 1 2 512 231
1
2
512
231
```

2. 从1加到100, 并显示结果

```sh
#!/bin/bash
i=1
while [ $i -le 100 ]
  do
    SUM=$(( $SUM + $i ))
    i=$(($i+1))
  done
echo "1+2+...+100=$SUM"
```

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell11_while.sh
1+2+...+100=5050
```

3. 输入两个参数`$1`, `$2`, 且前`$1<$2`, 计算`$1+...+$2`的值是多少?

```sh
#!/bin/bash
i=$1
SUM=0
while [ $i -le $2 ]
  do
    SUM=$[$SUM+$i]
    i=`expr $i + 1`
  done
echo "$1+...+$2=$SUM"
```

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell11_while.sh 1 200
1+...+200=20100
```
