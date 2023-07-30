---
title: shell编程2-$0,$1,$$,$!,$?,$*,$@,$#
url: https://www.yuque.com/stevenyin/liv/ho2a9e
---

<a name="c37c6119"></a>

# 位置参数变量

我们在执行一个脚本的时候, 可能会传入一些变量, 比如我的脚本`filenameGenerator.sh`是生成一组文件名, 但是文件的版本号是动态的, 此时我会这样执行我的脚本`./filenameGenerator.sh V1.0`, 将版本号以参数的形式传入到脚本中, 从而动态的变化.

如果想要完成这样的操作, 就需要在脚本中使用一下方式:

<a name="c4dd9766"></a>

## 基本语法

1. `$n`n位数字, `$0`代表当前执行的命令, $1-$9代表传入的第一到第九个参数, 十个以上的参数要写成`{10}`这样的形式.
2. `$*` 代表命令行中所有的参数, `$*`把所有的参数看成一个整体
3. `$@` 也代表命令行中所有的参数, 不过`$@`把每个参数区分对待
4. `$#` 代表这个命令行中所有参数的个数

<a name="Example"></a>

## Example

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell04_positionParams.sh
```

```sh
  #!/bin/bash
  # 获取各个参数
  # 分别输出执行的命令, 和随后输出的两个参数
  echo "$0 $1 $2"
  # 把后面的参数当做整体输出
  echo "$*"
  # 把参数区分对待(这个例子中看不出效果, 和上面的输出从形式上是一样的)
  echo "$@"
  # 输出参数的个数
  echo "$#"
```

执行该脚本时输入两个参数

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell04_positionParams.sh value1 value2
  ./shell04_positionParams.sh value1 value2
  value1 value2
  value1 value2
  2
```

<a name="8c19b91a"></a>

# 预定义变量

shell的设计者预先定义好的一些变量, 可以直接在shell脚本中使用

<a name="c4dd9766-1"></a>

## 基本语法

1. `$$` : 表示当前进程的进程号
2. `$!` : 表示后台运行的最后一个进程的进程号
3. `$?` : 最后一次执行命令的返回状态, 如果这个变量的值为0, 证明上一个命令正确执行; 如果这个变量的值非0,(具体是那一个数字由命令决定), 则证明上一个命令执行不正确.

<a name="Example-1"></a>

## Example

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell05_preset_variable.sh
```

```sh
#!/bin/bash
# 输出当前进程号
echo "current pid=$$"
# 后台执行shell04_positionParams.sh脚本
./shell04_positionParams.sh &
# 输出最后一个后台进程号
echo "last pid=$!"
# 输出最后一次执行的命令的返回值
echo "result = $?"
```

执行`shell05_preset_variable.sh`后结果为:

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# sh shell05_preset_variable.sh
current pid=27249
last pid=27250
result = 0
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell04_positionParams.sh


0
```

我只执行了`shell05_preset_variable.sh`, 命令行中打印出了三个值并且自动执行了`shell04_positionParams.sh`, 并且输出了`shell04_positionParams.sh`的结果.
