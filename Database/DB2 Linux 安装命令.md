# DB2Linux安装

1. 创建用户组
```sh
groupadd -g 2000 dlkiadmg
groupadd -g 2000 dlkfadmg
groupadd -g 2000 dlkadmg
```

2. 创建数据库用户
```sh
useradd -u 3001 -g dlkiadmg -m -d /home/datalake datalake
useradd -u 3001 -g dlkfadmg -m -d /home/dlkfenc dlkfenc
useradd -u 3001 -g dlkadmg -m -d /home/dlkuser dlkuser
```

3. 设置密码
```sh
passwd datalake datalake@jtyh1
passwd dlkfenc datalake@jtyh1
passwd dlkuser datalake@jtyh1
```

4. 创建DB2实例(instance)
```sh
cd /opt/ibm/db2/V11.1/instance/
./db2icrt -a server -p 50002 -u dlkfenc datalake
```


5. 切换用户
```sh
su datalake
```

6. 配置实例参数
```sh
db2set DB2COMM=tcpip
```

7. 创建sample数据库
```sh
db2sampl
```

8. 启动database manager
```sh
db2start
```

9. 连接到sample库
```sh
db2 connect to sample
```

10. 测试功能
```sh
db2 "select * from staff"
```

11. 创建数据库
```sh
db2 create database DLK
```

12. set remote NODE catalog 设置远程节点编目
```sh
db2 catalog tcpip node <NODENAME> remote <Host Name/IP> server <port>
db2 catalog tcpip node DLKDEV remote 182.47.21.137 server 50002
```
- 删除数据库编目
```sh
db2 uncatalog node <NODENAME>
```

13. 刷新
    db2 terminate

14. 检查directory
    db2 list node directory

15. 设置远程数据库编目
    db2 catalog db <server local DB name> as <remote DB name/alias> at node <NODENAME> authentication server
    db2 catalog db DLKDEV as DLKTEST at node DLKDEV authentication server
    db2 catalog db SAMPLE as DLKTMP at node DLKDEV authentication server

16. 刷新
    db2 terminate

17. 检查db
    db2 list db directory

18. catalog remote dbs to local
    db2 catalog db <remote db name> at node <NODENAME>
    db2 catalog db DLKDEV at node DLKDEV
    db2 catalog db DLKTMP at node DLKDEV

19. 刷新
    db2 terminate

20. 在本地连接远程数据库
    db2 connect to <local DB name> user <db2user> using <password>
    db2 connect to DLKDEV user datalake using datalake@jtyh1
    db2 connect to DLKTMP user datalake using datalake@jtyh1
