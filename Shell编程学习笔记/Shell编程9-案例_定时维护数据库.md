---
title: Shell编程9-案例:定时维护数据库
url: https://www.yuque.com/stevenyin/liv/okc4e9
---

<a name="9286e940"></a>

# Shell编程案例之---定时维护数据库

<a name="6bffd61d"></a>

## 需求:

1. 每天夜间**3:20**备份数据库到`/app/bakup/blog_db`
2. 备份操作开始和结束能够给出相应的提示信息
3. 备份后的文件要求以备份时间为文件名, 并打包成`.tar.gz`格式, 如: `2019-08-08_032000.tar.gz`
4. 备份的同时, 检查是否有**10天前**备份的数据库文件, 如果有则删除

<a name="1da25b1b"></a>

## 涉及到的知识点:

1. `crontab`任务调度器语法
2. `gzip`, `tar`压缩打包命令
3. `find`命令进行复杂条件查询
4. `mysqldump`备份`mysql`数据库脚本

```bash
  vim /app/bakup/bak.sh
```

```bash
#!/bin/bash

# 完成数据库定时备份
# 定义备份的路径
BACKUP=/app/bakup/blog_db
# 保存当前日期为变量
DATE=$(date +%Y-%m-%d_%H%M%S)

echo "=============start back up==============="
echo "the target file is $BACKUP/$DATE.tar.gz"

HOST=#数据库所在服务器
DB_USER=#用户名
# 由于密码比较敏感, 最好不要直接写在脚本中.
# 当然, 无论写在服务器的什么位置, 都会被获取到, 所以可以严格控制该文件的权限, 只有执行这个脚本的用户, 有权限查看, 也就是700
DB_PWD=#数据库密码
DB_NAME=#数据库名称
# 创建备份路径
# 如果备份的路径存在,就使用,否则就创建
[ ! -d "$BACKUP/$DATE" ] && mkdir -p
# 执行备份操作 
mysqldump -u${DB_USER} -p${DB_PWD} --host=${HOST} $DB_NAME | gzip > $BACKUP/$DATE/${DATE}.sql.gz

cd $BACKUP
# 对备份完成的sql文件再执行tar压缩命令
tar -zcvf $DATE.sql.gz $DATE
#删除临时文件
rm -rf $BACKUP/$DATE

# 删除十天前的文件
find $BACKUP -mtime +10 -name "*.tar.gz" -exec rm -rf {} \;
```

脚本写完后, 首先赋权, 然后将脚本加入到crontab的执行序列中:

```bash
chmod 700 /app/bakup/bak.sh
crontab -e
20 3 * * * /app/bakup/bak.sh
```
