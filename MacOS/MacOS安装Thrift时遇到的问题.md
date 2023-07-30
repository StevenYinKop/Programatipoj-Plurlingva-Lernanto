---
title: MacOS安装Thrift时遇到的问题
url: https://www.yuque.com/stevenyin/liv/gcy0mu
---

> 官方文档的步骤: <https://thrift.apache.org/docs/install/os_x.html>

<a name="brh92"></a>

##

<a name="hod9n"></a>

## 安装`Boost`

下载`boost`的`tar`包，`untar & compile`

```shell
./bootstrap.sh
sudo ./b2 threading=multi address-model=64 variant=release stage install
```

<a name="UFUA2"></a>

## 安装`libevent`

下载`libevent`的`tar`包，`untar & compile`

```shell
./configure --prefix=/usr/local 
make
sudo make install
```

<a name="LQhD5"></a>

## 安装Apache Thrift

```shell
./configure --prefix=/usr/local/ --with-boost=/usr/local --with-libevent=/usr/local --without-ruby --without-swift --without-php
make
sudo make install
```

<a name="GJxlo"></a>

###

<a name="CWLN8"></a>

## 报错清单

<a name="vmjee"></a>

### 报错1：`configure: error: Bison version 2.5 or higher must be installed on the system!`

通过`brew`更新`bison`：

```shell
brew install bison
```

添加bison到PATH中：

```shell
export PATH="$(brew --prefix bison)/bin:$PATH"
```

验证：

```shell
(base) ➜  ~ bison --version
bison (GNU Bison) 3.8.2
Written by Robert Corbett and Richard Stallman.

Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
```

升级结束。 <a name="tOy61"></a>

### 报错2: `fatal error: 'openssl/opensslv.h' file not found`

执行如下脚本后重新安装：

```shell
brew install openssl
brew link openssl --force
ln -s /usr/local/opt/openssl/bin/openssl /usr/local/bin/openssl
ln -s /usr/local/opt/openssl/include/openssl /usr/local/include/openssl
ln -s /usr/local/opt/openssl/lib/libssl.a /usr/local/lib/libssl.a
ln -s /usr/local/opt/openssl/lib/libcrypto.a /usr/local/lib/libcrypto.a
```

<a name="juEEh"></a>

### 报错3: python环境相关

```shell
...
...
...
creating /usr/lib/python3.9
error: could not create '/usr/lib/python3.9': Operation not permitted
make[4]: *** [install-exec-hook] Error 1
make[3]: *** [install-exec-am] Error 2
make[2]: *** [install-am] Error 2
make[1]: *** [install-recursive] Error 1
make: *** [install-recursive] Error 1
```

查看`thrift`的`py`部分的`MakeFile`的源码，初步判断是`thrift`在安装的过程中，会在`PY_PREFIX`这个路径下拼接`/lib/python3.9/site-packages`，但是对于`MacOS`来说，有一个路径保护的策略，`thrift`默认生成的路径在`/usr/`下，但是这个目录即使是`root`权限也无法在下面创建任何目录。
所以手动修改了`Makefile`，又因为我没有使用默认的`python`安装方式而是安装了`Anaconda`，所以把路径改成现在已经存在的`PY_PREFIX = /Users/stevenyin/Applications/Anaconda3/anaconda3`
�，这也是我本地默认的`site-packages`路径。目的是为了这个路径能够不受权限的影响创建出来。 <a name="TLzfG"></a>

### �报错4: Go相关

```shell
...
...
...
/usr/local/go/bin/go build -mod=mod ./thrift
go: go.mod file not found in current directory or any parent directory; see 'go help modules'
make[4]: *** [all-local] Error 1
make[3]: *** [all-recursive] Error 1
make[2]: *** [all-recursive] Error 1
make[1]: *** [all-recursive] Error 1
make: *** [all] Error 2
```

这个错误是在使用`Go`语言是，需要开启`GO111MODULE`，并且开启完成之后需要执行`go mod init <项目名>`，对于`1.16`之后的`Go`来说，默认是开启`GO111MODULE`的，所以我们执行下面的代码，然后重新`make`就好：

```shell
go mod init cc.stevenyin.thrift
```

<a name="i4CRl"></a>

### 报错5: Swift相关

```shell
error: terminated(72): /usr/bin/xcrun --sdk macosx --find xctest output:
xcrun: error: unable to find utility "xctest", not a developer tool or in PATH
```

参考：<https://github.com/boycgit/swiftui-knowledge/issues/4>和<https://github.com/mxcl/homebrew-made/issues/1>解决。
执行下面的命令之后重新`make`：

```shell
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

<a name="cq3Hc"></a>

### 报错6: swift相关2

```shell
error: unable to invoke subcommand: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swift-install (No such file or directory)
```

*暂时没有找到解决办法*，为了解决这个问题先跳过了swift的加载。 <a name="jI94Z"></a>

### 报错7: 安装Thrift的前置依赖libevent时报错：OpenSSL相关

```shell
...
...
...
checking for pkg-config... no
checking for library containing SSL_new... no
checking for library containing SSL_new... no
checking openssl/ssl.h usability... no
checking openssl/ssl.h presence... no
checking for openssl/ssl.h... no
configure: error: openssl is a must but can not be found. You should add the directory containing `openssl.pc' to the `PKG_CONFIG_PATH' environment variable, or set `CFLAGS' and `LDFLAGS' directly for openssl, or use `--disable-openssl' to disable support for openssl encryption
```

这个报错信息大致是说找不到`openssl`的相关配置文件。解决办法的话我通过`brew install openssl`更新`openssl`，从安装日志中顺带寻找了一下安装路径在`/usr/local/opt/openssl@3/bin`。因为在brew安装`openssl`结束之后，最后日志会提示你将部分参数配置到`PATH`下，所以我将下面几句话加到了环境变量`~/.zshrc`中然后刷新环境变量:

```shell
export PATH="/usr/local/opt/openssl@3/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/openssl@3/lib"
export CPPFLAGS="-I/usr/local/opt/openssl@3/include"
export PKG_CONFIG_PATH="/usr/local/opt/openssl@3/lib/pkgconfig"
```

在重新`configure libevent`就不报错了
