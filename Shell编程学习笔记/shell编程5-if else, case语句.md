---
title: shell编程5-if else, case语句
url: https://www.yuque.com/stevenyin/liv/dugw9c
---

<a name="dab26103"></a>

# if语句

<a name="c4dd9766"></a>

## 基本语法

```sh
  if [ 条件判断式 ];then
    逻辑代码
  fi
```

或者

```sh
  if[ 条件判断式 ]
    then
      逻辑代码
  elif
    then
      逻辑代码
fi
```

<a name="1bbbb204"></a>

## 注意事项

- `[ 条件判断式 ]`的左右两侧的括号与条件式之间必须要有空格, 这是`condition`条件的语法
- 一般情况下很少有编程语言在`if`后面还要加上分号`;`, 所以更推荐使用第二种语法

<a name="Example"></a>

## Example

1. 编写一个shell程序, 输入一个参数, 如果大于等于`60`, 则输出`"passed"`, 否则输出`"not passed"`

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell08_if.sh
```

```sh
  #!/bin/bash
  #编写一个shell程序, 如果大于等于60, 则输出"passed", 否则输出"not passed"
  if [ $1 -ge 60 ]
    then
      echo "passed"
  elif [ $1 -lt 60 ]
    then
      echo "not passed"
  fi
```

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 1
  not passed
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 60
  passed
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 80
  passed
```

2. 编写一个shell程序, 输入一个参数, 如果大于等于`90`, 则输出`"A"`, 如果大于等于`80`小于`90`, 输出`"B"`, 如果大于等于`70`小于`80`, 输出`"C"`, 如果大于等于`60`小于`70`, 输出`"D"`, 如果小于`60`, 输出`"E"`

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell08_if.sh
```

```sh
  #!/bin/bash
  if [ $1 -ge 90 ]
    then
      echo "A"
  elif [ $1 -ge 80 ] && [ $1 -lt 90 ]
    then echo "B"
  elif [ $1 -ge 70 ] && [ $1 -lt 80 ]
    then echo "C"
  elif [ $1 -ge 60 ] && [ $1 -lt 70 ]
    then echo "D"
  else
    echo "E"
  fi
```

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 1
  not passed
  E
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 60
  passed
  D
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 70
  passed
  C
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 71
  passed
  C
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 80
  passed
  B
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell08_if.sh 90
  passed
  A
```

<a name="2ae24b8a"></a>

# case 语句

<a name="c4dd9766-1"></a>

## 基本语法

```sh
  case $变量名 in
  "值1")
    逻辑语句
    ;; #使用两个分号, 代表结束, 类似于Java的break
  "值2")
    逻辑语句
    ;;
  *)
    # 如果上述的值都没有命中, 进入这个代码中
    ;;
  esac
```

<a name="Example-1"></a>

## Example

<a name="d712ee82"></a>

### 假设我们要编写一个自动执行`java jar`的脚本, 并且可以通过`start`, `stop`, `restart`, `status`来监控这个`jar`程序的执行状态, 我们就可以使用一下类似的条件判断(只有条件判断, 没有真正启动`jar`包的代码)

- 编写一个shell程序, 输入一个参数
  1. 如果是`start`, 则打印`blog is starting...`, 两秒后打印, `started! blog is running at pid 123456`;
  2. 如果是`stop`, 则打印`blog is stopping...`, 两秒后打印, `blog is not running now`;
  3. 如果是`restart`, 则打印 `blog is stopping...`, 两秒后打印, `blog is not running now`. 再打印`blog is starting...`, 两秒后打印, `started! blog is running at pid 123456`;
  4. 如果是`status`, 则打印`blog is running at pid 123456`;

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell09_case.sh
```

```sh
  #!/bin/bash
  case $1 in
    "start")
      echo "blog is starting..."
      sleep 2
      echo "blog is running at 123456"
      ;;
    "stop")
      echo "blog is stopping..."
      sleep 2
      echo "blog is not running now"
      ;;
    "restart")
      echo "blog is stopping..."
      sleep 2
      echo "blog is not running now"
      echo "blog is starting..."
      sleep 2
      echo "blog is running at 123456"
      ;;
    "status")
      echo "blog is running at 123456"
      ;;
    *)
      echo "usage: $0 start stop restart status"
      ;;
  esac
```

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell09_case.sh 1
  usage: ./shell09_case.sh start stop restart status
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell09_case.sh start
  blog is starting...
  blog is running at 123456
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell09_case.sh stop
  blog is stopping...
  blog is not running now
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell09_case.sh restart
  blog is stopping...
  blog is not running now
  blog is starting...
  blog is running at 123456
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell09_case.sh status
  blog is running at 123456
```
