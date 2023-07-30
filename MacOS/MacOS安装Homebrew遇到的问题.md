---
title: MacOS安装Homebrew遇到的问题
url: https://www.yuque.com/stevenyin/liv/klrou8
---

官方/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

1.


<a name="l39pj"></a>

## Permission denied @ rb\_file\_s\_symlink - (../../../Homebrew/completions/zsh/\_brew, /usr/local/share/zsh/site-functions/\_brew)

执行下述命令后重新执行安装命令：

```shell
sudo chown -R $(whoami): /usr/local/share/zsh
```
