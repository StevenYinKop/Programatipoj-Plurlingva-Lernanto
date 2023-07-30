---
title: shell编程8-函数定义
url: https://www.yuque.com/stevenyin/liv/qc3k94
---

<a name="870a51ba"></a>

# 函数

<a name="c4dd9766"></a>

## 基本语法

```sh
function foo()
{
  $1...
  逻辑代码
  [return int;]
}
```

```sh
  # 调用的时候直接写函数名就可以了
  foo
  # 如果需要传参数, 就直接在函数名后面加上参数

  foo param1 param2 ...
```

> **注意** 调用的时候如果需要传参, 则按照上面的方式去传递就可以了, 而函数接收参数的时候, 并不需要想`java`那样, `public static void main(String [] args)`, 而是不需要写形参, 需要使用参数的时候则使用`$1`, `$2`这样去引用就好了, 下面有例子详细说明

<a name="Example"></a>

## Example

> 这个案例在[case](/blog/21)部分练习过, 在这里可以把冗余的代码提取成函数

<a name="d140e4f6"></a>

### 1. 假设我们要编写一个自动执行`java jar`的脚本, 并且可以通过`start`, `stop`, `restart`, `status`来监控这个`jar`程序的执行状态, 我们就可以使用一下类似的条件判断(只有条件判断, 没有真正启动`jar`包的代码)

- 编写一个shell程序, 输入一个参数
  1. 如果是`start`, 则打印`blog is starting...`, 两秒后打印, `started! blog is running at pid 123456`;
  2. 如果是`stop`, 则打印`blog is stopping...`, 两秒后打印, `blog is not running now`;
  3. 如果是`restart`, 则打印 `blog is stopping...`, 两秒后打印, `blog is not running now`. 再打印`blog is starting...`, 两秒后打印, `started! blog is running at pid 123456`;
  4. 如果是`status`, 则打印`blog is running at pid 123456`;

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell13_function.sh
```

```sh
  #!/bin/bash
  function start()
  {
    echo "blog is starting..."
    sleep 2
    status
  }
  function stop
  {
      echo "blog is stopping..."
      sleep 2
      echo "blog is not running now"
  }
  function status
  {
    echo "blog is running at 123456"
  }

  case $1 in
  "start")
    start
    ;;
  "stop")
    stop
    ;;
  "restart")
    stop
    sleep 2
    start
    ;;
  "status")
    status
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

<a name="7c6b66fb"></a>

### 2. 编写一个函数, 计算传入的参数累加的值

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell14_sum.sh
```

```sh
  #!/bin/bash
  function getSum()
  {
    SUM=0
    for i in $@
      do
        SUM=$[$SUM+$i]
      done
    echo "$SUM"
  }

  echo "$(getSum $@)"
```

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# chmod shell14_sum.sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell14_sum.sh 1 23 4
28
```
