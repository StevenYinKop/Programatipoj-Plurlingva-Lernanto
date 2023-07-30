---
title: 在阿里云上安装docker的shell脚本
url: https://www.yuque.com/stevenyin/liv/ein6d4
---

```shell
yum -y install gcc
yum -y install gcc-c++.x86_64
yum remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine
yum install -y yum-utils
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum makecache
yum -y install docker-ce docker-ce-cli containerd.io
systemctl start docker
docker version

mkdir -p /etc/docker
tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://<!!!!这里要替换成自己的容器镜像服务!!!!!>.mirror.aliyuncs.com"]
}
EOF
systemctl daemon-reload
systemctl restart docker

```

<a name="uKAwj"></a>

## 容器镜像服务

1. 登录阿里云, 找到**容器镜像服务**这个选项

![image.png](../assets/ein6d4/1630415826597-66410281-eb62-431a-b0bd-0a27fa1830ea.png)

2. 找到镜像加速器复制URL, 替换当前脚本的url

![image.png](../assets/ein6d4/1630415974404-51559a71-39f6-43ce-8a33-a95a5e419f68.png)
