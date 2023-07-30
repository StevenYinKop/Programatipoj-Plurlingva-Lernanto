---
title: Java-Write to File
url: https://www.yuque.com/stevenyin/liv/dsho5m
---

<a name="8b9c3a81"></a>

# Java 数据写入文件的方法

> 本文将向大家分享使用Java的`BufferedWriter`, `PrintWriter`, `FileOutputStream`, `DataOutputStream`, `RandomAccessFile`, `FileChannel`, 和一些Java7的实用类写文件的操作

<a name="d4dfa987"></a>

## `BufferedWriter`

直接上Demo:

```java
@Test
public void whenWriteStringUsingBufferedWritter_thenCorrect() 
  throws IOException {
    String str = "Hello";
    BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
    writer.write(str);
    
    writer.close();
}
```

这样我们就可以将`Hello`字符串输出到文件(`fileName`)中:

我们也可以使用`new FileWriter(fileName, true)`将第二个参数设置为`true`来追加内容, 并不覆盖

```java
@Test
public void whenAppendStringUsingBufferedWritter_thenOldContentShouldExistToo() 
  throws IOException {
    String str = "World";
    BufferedWriter writer = new BufferedWriter(new FileWriter(fileName, true));
    writer.append(' ');
    writer.append(str);
    writer.close();
}
```

这样的执行结果:

Hello World

`writer.append(String str)`和`writer.write(String str)`本质上是相同的, `append`方法实际上就是调用了`write`方法, 然后`return this`方便后续链式调用

<a name="cf5004ad"></a>

## `PrintWriter`

```java
@Test
public void givenWritingStringToFile_whenUsingPrintWriter_thenCorrect() 
  throws IOException {
    FileWriter fileWriter = new FileWriter(fileName);
    PrintWriter printWriter = new PrintWriter(fileWriter);
    printWriter.print("Some String");
    printWriter.printf("Product name is %s and its price is %d $", "iPhone", 1000);
    printWriter.close();
}
```

打印的结果为:

    Some StringProduct name is iPhone and its price is 1000$

上述我们还使用了C语言中特别经典的printf来格式化我们的打印内容.

<a name="bd8fc6cb"></a>

## `FileOutputStream`

使用`FileOutputStream`将bytes数组写入文件中

```java
@Test
public void givenWritingStringToFile_whenUsingFileOutputStream_thenCorrect() 
  throws IOException {
    String str = "Hello";
    FileOutputStream outputStream = new FileOutputStream(fileName);
    byte[] strToBytes = str.getBytes();
    outputStream.write(strToBytes);
    outputStream.close();
}
```

结果:

    Hello

<a name="588675a8"></a>

## `DataOutputStream`

```java
@Test
public void givenWritingToFile_whenUsingDataOutputStream_thenCorrect() 
  throws IOException {
    String value = "Hello";
    FileOutputStream fos = new FileOutputStream(fileName);
    DataOutputStream outStream = new DataOutputStream(new BufferedOutputStream(fos));
    outStream.writeUTF(value);
    outStream.close();

    // verify the results
    String result;
    FileInputStream fis = new FileInputStream(fileName);
    DataInputStream reader = new DataInputStream(fis);
    result = reader.readUTF();
    reader.close();

    assertEquals(value, result);
}
```

<a name="18a8b077"></a>

## `RandomAccessFile`

使用RandomAccessFile能够在文件的特定位置进行写操作，给定从文件开头开始的偏移量（以bytes为单位）。

这段代码写一个整数值，其偏移量从文件开头开始：

```java
private void writeToPosition(String filename, int data, long position) 
  throws IOException {
    RandomAccessFile writer = new RandomAccessFile(filename, "rw");
    writer.seek(position);
    writer.writeInt(data);
    writer.close();
}
```

从特定位置读取一个整数值

```java
private int readFromPosition(String filename, long position) 
  throws IOException {
    int result = 0;
    RandomAccessFile reader = new RandomAccessFile(filename, "r");
    reader.seek(position);
    result = reader.readInt();
    reader.close();
    return result;
}
```

测试: 在特定位置写入整数值, 然后进行测试

```java
@Test
public void whenWritingToSpecificPositionInFile_thenCorrect() 
  throws IOException {
    int data1 = 2014;
    int data2 = 1500;
    
    writeToPosition(fileName, data1, 4);
    assertEquals(data1, readFromPosition(fileName, 4));
    
    writeToPosition(fileName, data2, 4);
    assertEquals(data2, readFromPosition(fileName, 4));
}
```

7. `FileChannel`

   如果要处理大文件，则FileChannel可以比标准IO更快。 以下代码使用FileChannel将String写入文件：

```java
@Test
public void givenWritingToFile_whenUsingFileChannel_thenCorrect() 
  throws IOException {
    RandomAccessFile stream = new RandomAccessFile(fileName, "rw");
    FileChannel channel = stream.getChannel();
    String value = "Hello";
    byte[] strBytes = value.getBytes();
    ByteBuffer buffer = ByteBuffer.allocate(strBytes.length);
    buffer.put(strBytes);
    buffer.flip();
    channel.write(buffer);
    stream.close();
    channel.close();

    // verify
    RandomAccessFile reader = new RandomAccessFile(fileName, "r");
    assertEquals(value, reader.readLine());
    reader.close();
}
```

<a name="201e4fff"></a>

## `Java7`提供的`Files`类

Java 7引入了使用文件系统的新方法，以及新的工具类：`Files`。

使用Files类，我们可以创建，移动，复制和删除文件和目录。 也可以用于读取和写入文件：

```java
@Test
public void givenUsingJava7_whenWritingToFile_thenCorrect() 
  throws IOException {
    String str = "Hello";

    Path path = Paths.get(fileName);
    byte[] strToBytes = str.getBytes();

    Files.write(path, strToBytes);

    String read = Files.readAllLines(path).get(0);
    assertEquals(str, read);
}
```

<a name="b30db159"></a>

## 临时文件

现在让我们尝试写入一个临时文件, 在操作完成之后, 这个文件就会被删除掉。 以下代码创建一个临时文件并向其中写入一个String：

```java
@Test
public void whenWriteToTmpFile_thenCorrect() throws IOException {
    String toWrite = "Hello";
    File tmpFile = File.createTempFile("test", ".tmp");
    FileWriter writer = new FileWriter(tmpFile);
    writer.write(toWrite);
    writer.close();

    BufferedReader reader = new BufferedReader(new FileReader(tmpFile));
    assertEquals(toWrite, reader.readLine());
    reader.close();
}
```

<a name="0cb20665"></a>

## 在写文件之前将文件锁定

最后，在写入文件时，有时我们需要确保没有其他人在同一时间写入该文件。 基本上，我们需要能够在写入时锁定该文件。

```java
@Test
public void whenTryToLockFile_thenItShouldBeLocked() 
  throws IOException {
    RandomAccessFile stream = new RandomAccessFile(fileName, "rw");
    FileChannel channel = stream.getChannel();

    FileLock lock = null;
    try {
        lock = channel.tryLock();
    } catch (final OverlappingFileLockException e) {
        stream.close();
        channel.close();
    }
    stream.writeChars("test lock");
    lock.release();

    stream.close();
    channel.close();
}
```

这是当我们想要获取这个文件但是文件被别人锁定的时候, 则会抛出OverlappingFileLockException异常。

<a name="2250ab9c"></a>

## 一些注意事项

1. 如果我们从不存在的文件中读取文件，则会抛出`FileNotFoundException`。
2. 如果我们将数据写入不存在的文件，则将首先创建该文件，并且不会抛异常。
3. 使用完资源之后close()不要忘记, 否则会导致这个资源一直被占用。
4. 在输出流中，`close()`方法在释放资源之前调用`flush()`，这将强制将所有缓冲的字节写入流中。
5. `PrintWriter`常用于写入格式文本，`FileOutputStream`常用于写入二进制数据，`DataOutputStream`常用于写入原始数据类型，`RandomAccessFile`常用于写入特定位置，`FileChannel`常用于更快地写入较大的文件。
