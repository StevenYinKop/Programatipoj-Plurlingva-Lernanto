---
title: 在Java中使用SFTP传输文件
url: https://www.yuque.com/stevenyin/liv/nn0gro
---

<a name="uEysw"></a>

## 框架版本

| **groupId** | **artifactId** | **version** |
| --- | --- | --- |
| com.jcraft | jsch | 0.1.55 |
| com.hierynomus | sshj | 0.27.0 |
| org.apache.commons | commons-vfs2 | 2.4 |
|  |  |  |

<a name="YA0EO"></a>

使用`JSch`库




<a name="EPPPG"></a>

### Maven 配置

```xml
<dependency>
    <groupId>com.jcraft</groupId>
    <artifactId>jsch</artifactId>
    <version>0.1.55</version>
</dependency>
```

<a name="lfKd5"></a>

### 初始化

```java
private String remoteHost = "127.0.0.1"
private String knownHost = "/Users/stevenyin/.ssh/known_hosts";
private String username = "admin";
private String password = "123456";

private ChannelSftp setupJsch() throws JSchException {
    JSch jsch = new JSch();
    jsch.setKnownHosts(remoteHost);
    Session jschSession = jsch.getSession(username, remoteHost);
    jschSession.setPassword(password);
    jschSession.connect();
    return (ChannelSftp) jschSession.openChannel("sftp");
}
```

```shell
ssh-keyscan -H -t rsa REMOTE_HOSTNAME >> known_hosts
```

<a name="GJA19"></a>

### 上传文件

```java
@Test  
public void whenUploadFileUsingJsch_thenSuccess() throws JSchException, SftpException {
    ChannelSftp channelSftp = setupJsch();
    channelSftp.connect();
    String localFile = "src/main/resources/sample.txt";
    String remoteDir = "remote_sftp_test/";
    channelSftp.put(localFile, remoteDir + "jschFile.txt");
    channelSftp.exit();
}
```

<a name="VGKrY"></a>

### 下载文件

```java
@Test  
public void whenDownloadFileUsingJsch_thenSuccess() throws JSchException, SftpException {
    ChannelSftp channelSftp = setupJsch();
    channelSftp.connect();
    String remoteFile = "welcome.txt";
    String localDir = "src/main/resources/";
    channelSftp.get(remoteFile, localDir + "jschFile.txt");
    channelSftp.exit();
}
```

<a name="Ic7Na"></a>

## Using SSHJ

<a name="qIZWc"></a>

### Maven配置

```xml
<dependency>
    <groupId>com.hierynomus</groupId>
    <artifactId>sshj</artifactId>
    <version>0.27.0</version>
</dependency>
```

<a name="WinUe"></a>

### 初始化

```java
private SSHClient setupSshj() throws IOException {
    SSHClient client = new SSHClient();
    client.addHostKeyVerifier(new PromiscuousVerifier());
    client.connect(remoteHost);
    client.authPassword(username, password);
    return client;
}
```

<a name="k0hFA"></a>

### 上传文件

```java
@Test
public void whenUploadFileUsingSshj_thenSuccess() throws IOException {
    SSHClient sshClient = setupSshj();
    SFTPClient sftpClient = sshClient.newSFTPClient();
 	String localFile = "src/main/resources/input.txt";
	String remoteDir = "remote_sftp_test/";
    sftpClient.put(localFile, remoteDir + "sshjFile.txt");
 
    sftpClient.close();
    sshClient.disconnect();
}
```

<a name="uvzsB"></a>

Apache Commons VFS




<a name="AYqdT"></a>

### Maven配置

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-vfs2</artifactId>
    <version>2.4</version>
</dependency>
```

<a name="dCXsr"></a>

### Tips

远程文件的路径为: `sftp://username:password@remoteHost.` <a name="HlyrH"></a>

### 上传文件

```java
@Test
public void whenUploadFileUsingVfs_thenSuccess() throws IOException {
    FileSystemManager manager = VFS.getManager();
 
    FileObject local = manager.resolveFile(System.getProperty("user.dir") + "/" + localFile);
    FileObject remote = manager.resolveFile("sftp://" + username + ":" + password + "@" + remoteHost + "/" + remoteDir + "vfsFile.txt");
 
    remote.copyFrom(local, Selectors.SELECT_SELF);
 
    local.close();
    remote.close();
}
```

<a name="eRpRj"></a>

### 下载文件

```java
@Test
public void whenDownloadFileUsingVfs_thenSuccess() throws IOException {
    FileSystemManager manager = VFS.getManager();
 
    FileObject local = manager.resolveFile(System.getProperty("user.dir") + "/" + localDir + "vfsFile.txt");
    FileObject remote = manager.resolveFile("sftp://" + username + ":" + password + "@" + remoteHost + "/" + remoteFile);
 
    local.copyFrom(remote, Selectors.SELECT_SELF);
 
    local.close();
    remote.close();
}
```
