---
title: shell编程1-Shell变量的定义与使用
url: https://www.yuque.com/stevenyin/liv/hkhrgx
---

<a name="HelloWorld"></a>

# HelloWorld

打开Linux终端,我们使用vi编辑器编写第一个Shell脚本

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim helloworld.sh
```

编写HelloWorld脚本程序:

```sh
#!/bin/bash
echo "hello world!"
```

在`vim`下使用`:wq`保存, 查看文件后发现, `helloworld.sh`并没有执行权限`x`, 所以我们要赋予这个文件`x`权限

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ll
  total 4
  -rw-r--r-- 1 root root 32 Jul  7 15:13 helloworld.sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# chmod 755 helloworld.sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ll
  total 4
  -rwxr-xr-x 1 root root 32 Jul  7 15:13 helloworld.sh
```

此时`helloworld.sh`权限中含有了`x`权限, 下一步就是执行这个脚本, 通常执行脚本的方式有以下三种

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# sh helloworld.sh
  hello world!
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# /root/helloworld.sh
  hello world!
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./helloworld.sh
  hello world!
```

1. 使用命令: `sh 文件名`
2. 文件的绝对路径
3. 文件的相对路径

我们通常会使用后面两种

<a name="ff3f484b"></a>

# Shell的变量

Linux Shell中的变量分为: 系统变量和用户自定义变量

<a name="979a5068"></a>

## 系统变量

如: `$HOME`, `$PWD`, `$SHELL`, `$USER`

这些变量不是我们定义的, 是系统自带或者我们之前定义在环境中的变量, 比如`JAVA_HOME`是我们在安装`JDK`时配置的环境变量.

显示当前shell中所有变量: `set`

<a name="b273953b"></a>

## 自定义变量

<a name="c4dd9766"></a>

### 基本语法

1. 定义变量

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell01_variables.sh
```

编写以下命令

```sh
  #!/bin/bash
  A=100
  echo "$A"
  unset A
  echo "$A"
```

这段脚本的意思是: 定义一个变量`A`, 值为`100`, 并且打印这个变量, 然后将变量移除, 再重新打印结果.
我们执行上述脚本(需要赋予执行权限):

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell01_variables.sh
  100

  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]#
```

我们看到执行完成后, 只输出了一个`100`, 并且紧接着输出了一个空行, 说明第二次打印`$A`的时候这个变量已经被移除了

2. 定义readonly变量

当使用readonly来定义变量时, 此时该变量即为常量, 不可以被修改和unset

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell02_readonly.sh
```

```sh
  #!/bin/bash
  readonly A=99
  echo "A=$A"
  unset A
  echo "A=$A"
  A=100
  echo "A=$A"
```

执行:

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell02_readonly.sh
  A=99
  ./shell02_readonly.sh: line 4: unset: A: cannot unset: readonly variable
  A=99
  ./shell02_readonly.sh: line 6: A: readonly variable
  A=99
```

3. 将变量提升为系统变量, 供其他shell使用
   - 设置环境变量 `export 变量名=变量值(export JAVA_HOME=/usr/local/java)`
   - 使定义的环境变量生效 `source 定义环境变量的文件`
   - 打印设置的环境变量 `echo $环境变量名`

```sh
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# vim shell03_upgrade_to_env.sh
```

下面一段脚本将家目录下的文件打印出来, 存在`ENV_TEST`中, 同时打印出来, 又输出了之前设置的`JDK`的目录.

```sh
#!/bin/bash
export ENV_TEST=`ls -l ~/`
echo "$ENV_TEST"
echo "JAVA_HOME=$JAVA_HOME"
```

执行

```sh
  [root@iZuf6ik7jd0vx7lwr5lyvpZ ~]# ./shell03_upgrade_to_env.sh
  total 16
  -rwxr-xr-x 1 root root 32 Jul  7 15:13 helloworld.sh
  -rwxr--r-- 1 root root 46 Jul  7 15:35 shell01_variables.sh
  -rwxr--r-- 1 root root 76 Jul  7 17:17 shell02_readonly.sh
  -rwxr--r-- 1 root root 73 Jul  7 17:28 shell03_upgrade_to_env.sh
  JAVA_HOME=/software/jdk1.8.0_201
[root@iZuf6ik7jd0vx7lwr5lyvpZ ~]#
```

<a name="77c24679"></a>

### 变量定义的规则

- 变量名称可以由字母, 数字, 下划线组成, 但是不能以数字开头
- 等号两侧不能有空格
- 变量名称一般习惯大写

<a name="c75b7e48"></a>

### 将命令的返回值赋给变量

1. `A=`ls -la\`\` 使用反引号, 运行反引号中的命令, 将结果返回并且赋值给变量A
2. `A=$(ls -la)` 使用`$(命令)`, 效果和上述语法相同
