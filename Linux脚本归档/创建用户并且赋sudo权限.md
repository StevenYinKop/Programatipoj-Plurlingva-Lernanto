---
title: 创建用户并且赋sudo权限
url: https://www.yuque.com/stevenyin/liv/vpx8qd
---

```shell
adduser stevenyin
passwd stevenyin
# 输入密码
chmod -v u+w /etc/sudoers
vim /etc/sudoers
# 编辑/etc/sudoers文件。
# 找到这一 行："root ALL=(ALL) ALL"在起下面添加"stevenyin ALL=(ALL) ALL"
# 保存退出。
chmod -v u-w /etc/sudoers
```
