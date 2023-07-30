---
title: 对ThreadLocal的理解(一)--使用
url: https://www.yuque.com/stevenyin/liv/mgq8x2
---

<a name="61a3ec66"></a>

## 介绍

> ThreadLocal是一个线程级别的变量池, 能够完成针对每一个线程, 分别维护一个变量值, 不会出现一个线程读取或修改另一个线程变量的现象.

<a name="d19f2c10"></a>

## 基本使用

<a name="5aa68c52"></a>

### ThreadLocal的成员方法

| 方法名 | 作用 |
| --- | --- |
| void set(T value) | 设置当前线程在ThreadLocal中的本地值 |
| T get() | 获取当前线程在ThreadLocal中的本地值 |
| void remove() | 移除当前线程在ThreadLocal中的本地值 |

<a name="34577a27"></a>

### 示例代码

使用5个线程, 使用ThreadLocal对每一个线程的变量进行保存并且读取:

```java
package cc.stevenyin.multithread.basic.threadlocal;

import lombok.Data;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadLocalTest {
    @Data
    static class Foo {
        static final AtomicInteger AMOUNT = new AtomicInteger(0);
        int index = 0;
        int bar = 0;

        public Foo() {
            index = AMOUNT.incrementAndGet();
        }
        @Override
        public String toString() {
            return index + "Foo{" +
                    "@bar=" + bar +
                    '}';
        }
    }
    private static final ThreadLocal<Foo> LOCAL_FOO = new ThreadLocal<>();

    public static void main(String[] args) {
        // 调度器对象
        // ExecutorService用于管理线程池
//        ExecutorService executorService = Executors.newCachedThreadPool();
        // 可缓存线程池的特点是: 无限大,如果线程池没有可用的线程则创建,有空闲的则使用
//        ExecutorService executorService = Executors.newFixedThreadPool(10);
        // 定长线程池的特点是: 固定线程总数, 空闲线程用于执行任务, 如果线程都在使用,后续任务处于等待状态, 在线程池中的线程执行完任务后,再执行后续的任务
//        ExecutorService executorService = Executors.newSingleThreadExecutor();
        ExecutorService executorService = Executors.newScheduledThreadPool(5);
        // 可调度线程池
        for (int i = 1; i <= 5; i ++) {
            executorService.execute(() -> {
                if (LOCAL_FOO.get() == null) {
                    LOCAL_FOO.set(new Foo());
                }
                System.out.println("初始本地值: " + LOCAL_FOO.get());
                for (int j = 0; j < 10; j ++) {
                    Foo foo = LOCAL_FOO.get();
                    foo.setBar(foo.getBar() + 1);
                    try {
                        TimeUnit.MILLISECONDS.sleep(10);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                System.out.println("累加10次后的值: " + LOCAL_FOO.get());
                LOCAL_FOO.remove();
            });
        }
        executorService.shutdown();
    }
}
```

    初始本地值: 2Foo{@bar=0}
    初始本地值: 3Foo{@bar=0}
    初始本地值: 4Foo{@bar=0}
    初始本地值: 1Foo{@bar=0}
    初始本地值: 5Foo{@bar=0}
    累加10次后的值: 1Foo{@bar=10}
    累加10次后的值: 4Foo{@bar=10}
    累加10次后的值: 5Foo{@bar=10}
    累加10次后的值: 2Foo{@bar=10}
    累加10次后的值: 3Foo{@bar=10}

根据输出结果可以看出: 在LOCAL\_FOO中, 每一个线程都绑定了一个独立的值(Foo对象), 这些值对象是线程的私有财产. 可以理解为线程的本地值. 线程的每一次操作都是在本线程对应的值上进行的.

<a name="7efcb0ce"></a>

## 使用场景

ThreadLocal是解决线程安全问题的一个较好的方案, 它通过为每一个线程提供一个独立的本地值, 去解决并发访问的冲突问题. 在很多情况下, 使用ThreadLocal比直接使用同步机制(如synchronized)解决线程安全问题更简单方便, 并且结果程序拥有更高的并发性.

<a name="74a707f2"></a>

### 线程隔离

ThreadLocal中的数据只属于当前线程, 其本地值对别的线程是不可见的.在多线程环境下, 可以用来防止自己的变量被其他线程篡改. 另外, 由于各个线程之间的数据相互隔离, 避免了同步加锁带来的性能问题, 大大提升了并发性能.

ThreadLocal在**线程隔离**中的常用场景有:

1. 可以为每一个线程绑定一个用户会话信息
2. 为每一个线程绑定一个数据库连接, 使得这个数据库连接为线程独享, 从而避免数据库连接被混用而导致操作异常问题.
3. HTTP请求

<a name="93d9170f"></a>

#### `Hibernate`中对ThreadLocal的应用

```java
private static final ThreadLocal threadSession = new ThreadLocal();

public static Session getSession() throws InfrastructureException {
    Session s = (Session) threadSession.get();
    try {
        if (s == null) {
            s = getSessionFactory().openSession();
            threadSession.set(s);
        }
    } catch (HibernateException ex) {
        throw new InfrastructureException(ex);
    }
    return s;
}
```

`Hibernate`对数据库连接进行了封装, 一个`Session`代表一个数据库连接, 通过以上代码可以看到,在`Hibernate`的`getSession()`方法中, 首先判断当前线程中有没有放进去`Session`, 如果还没有, 那么通过`sessionFactory().openSession()`来创建一个`Session`, 再将`Session`设置到`ThreadLocal`变量中, 这个`Session`相当于线程的私有变量, 而不是线程共有的, 显然其他的线程是获取不到这个`Session`的.
一般来说, 完成数据库操作之后程序会将`Session`关闭, 从而节省数据库连接资源. 如果`Session`的使用方式是共享而不是独占的, 在这种情况下, `Session`是多线程共享使用的, 如果某个线程使用完成直接将`Session`关闭, 那么其他线程在操作`Session`时就会报错, 所以`Hibernate`通过`ThreadLocal`非常简单地实现了数据库连接的安全使用.

<a name="03d799f9"></a>

### 跨函数的参数传递

在同一个线程内, 跨类,跨方法传递数据时, 如果不用ThreadLocal, 那么相互之间的数据传递势必要靠返回值和参数. 这样无形之中增加了这些类或者方法之间的耦合度.
由于ThreadLocal的特性, 同一线程在某些地方进行设置, 在随后的任意地方都可以获取到.

<a name="d7dd1d61"></a>

#### `Spring Security`中使用ThreadLocal传递用户信息

`org.springframework.security.core.context.ThreadLocalSecurityContextHolderStrategy`的源码中,使用ThreadLocal保存用户上下文信息:

```java
package org.springframework.security.core.context;

import org.springframework.util.Assert;

final class ThreadLocalSecurityContextHolderStrategy implements SecurityContextHolderStrategy {
    private static final ThreadLocal<SecurityContext> contextHolder = new ThreadLocal();

    ThreadLocalSecurityContextHolderStrategy() {
    }

    public void clearContext() {
        contextHolder.remove();
    }

    public SecurityContext getContext() {
        SecurityContext ctx = (SecurityContext)contextHolder.get();
        if (ctx == null) {
            ctx = this.createEmptyContext();
            contextHolder.set(ctx);
        }

        return ctx;
    }

    public void setContext(SecurityContext context) {
        Assert.notNull(context, "Only non-null SecurityContext instances are permitted");
        contextHolder.set(context);
    }

    public SecurityContext createEmptyContext() {
        return new SecurityContextImpl();
    }
}
```

在我们的代码的任意位置, 如果想要获取用户信息, 通过`SecurityContextHolder.getContext().getAuthentication()` 就可以获得.
