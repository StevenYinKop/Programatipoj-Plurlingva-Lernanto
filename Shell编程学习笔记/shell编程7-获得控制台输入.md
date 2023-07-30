---
title: shell编程7-获得控制台输入
url: https://www.yuque.com/stevenyin/liv/ozuky6
---

<a name="6cc42b1e"></a>

# 获得控制台输入

当脚本执行的过程中, 可能会有一些需要交互的参数, 比如填写用户, 邮箱之类的信息, 如果在执行shell脚本的时候通过`./xxx.sh params1 params2 ...`的方式进行传参的话, 参数多起来会很难阅读, 所以我们可以使用`Linux`中`read`命令来获取控制台输入.

<a name="c4dd9766"></a>

## 基本语法

`read -p "xx" -t 123 VAR1`

<a name="ea15ae2b"></a>

### 选项

- `-p`: 用户输入值的时候提供的提示文字
- `-t`: 等待输入的时间(s), 如果超过这个时间还没有输入, 则程序自动停止
- `-s`: 输入的字符不显示在控制台中, 大多数用于输入密码的场景
- 后面的`VAR1`是这个变量的变量名

<a name="Example"></a>

## Example

1. 提示用户输入姓名, 用户输入完后打印"Hello {输入的值}"

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell12_read.sh
```

```sh
#!/bin/bash
read -p "Plz input your name: " NAME
echo "Hello $NAME!"
```

    [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# chmod +x shell12_read.sh
    [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell12_read.sh
    Plz input your name: CinCommon
    Hello CinCommon!

2. 先后提示用户输入Id, 密码. 如果10s都没有输入密码, 则打印`"default password is: 123456"`, 否则打印`{Id}/{密码}`

```sh
#!/bin/bash

read -p "Plz input your name: " NAME
echo "Hello $NAME!"
read -s -p "plz input a password: " -t 5  PASSWD
if [ -z $PASSWD ]
    then echo "the password is empty, set default password: 123456"
else
    echo "check your input: $NAME/$PASSWD"
fi
```

当5s内没有输入密码时

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell12_read.sh
Plz input your name: CinCommon
Hello CinCommon!
plz input a password: the password is empty, set default password: 123456
```

正常输入密码时

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell12_read.sh
Plz input your name: CinCommon
Hello CinCommon!
plz input a password: check your input: CinCommon/impassword
```
