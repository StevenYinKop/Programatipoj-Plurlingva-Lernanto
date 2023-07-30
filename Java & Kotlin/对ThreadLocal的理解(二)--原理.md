---
title: 对ThreadLocal的理解(二)--原理
url: https://www.yuque.com/stevenyin/liv/yvtbmg
---

<a name="MR4MD"></a>

## `ThreadLocal`的内部结构演进

早期版本的JDK中，`ThreadLocal`的内部结构是一个`Map`，其中每一个线程实例作为Key，线程在`ThreadLocal`中绑定的值为`Value`，早期版本的`Map`结构，拥有这是`ThreadLocal`，每一个`ThreadLocal`实例拥有一个`Map`实例。

在`JDK8`中，`ThreadLocal`的内部结构发生演进。虽然还是使用了`Map`结构，但是`Map`结构的拥有者，从`ThreadLocal`实例变为了`Thread`实例。每一个`Thread`实例拥有一个`Map`实例。另外，`Map`结构的`Key`值也发生了变化：新的`Key`值为`ThreadLocal`实例。
如果给一个Thread创建了多个ThreadLocal实例，那么当前的ThreadLocalMap中就会有多个Key-Value对，其中ThreadLocal为Key，数据为Value。

<a name="ZLJOf"></a>

### 总结：

与早期的`ThreadLocalMap`相比，新版本主要变化为：

1. 拥有者发生了变化，`ThreadLocalMap`的拥有者，从早期版本的`ThreadLocal`变为新版本的`Thread`。
2. `Key`值发生了变化：新版本的`Key`为`ThreadLocal`实例，早期版本的`Key`为`Thread`实例

与早期版本的`ThreadLocalMap`相比，新版本的主要优势为：

1. 每一个`ThreadLocalMap`存储的“`Key-Value`”数量变少。早期版本的“`Key-Value`对”数量与线程个数强关联，如果线程数量多，那么`ThreadLocalMap`存储的“`Key-Value`”数量也多，新版本的`ThreadLocalMap`的`Key`是`ThreadLocal`实例，多线程情况下`ThreadLocal`实例比线程数量少。
2. 早期版本的`ThreadLocalMap`的拥有者为`ThreadLocal`，在`Thread`实例销毁后，`ThreadLocalMap`还是存在的；新版本的`ThreadLocalMap`的拥有者为`Thread`，所以当线程销毁后，`ThreadLocalMap`也会随之销毁。

<a name="RFj2m"></a>

## `Thread`，`ThreadLocal`，`ThreadLocalMap`的关系

<a name="sMlwq"></a>

## `ThreadLocal`源码

<a name="raYsm"></a>

### 1. set(T value)方法

用于设置当前线程的变量值。

```java
public void set(T value) {
    // 获取当前线程对象
    Thread t = Thread.currentThread();
    // 获取当前线程的ThreadLocalMap成员
    ThreadLocalMap map = getMap(t);
    // 判断map是否存在
    if (map != null) {
        // 将value绑定到threadLocal实例上
        map.set(this, value);
    } else {
        // 如果当前线程没有ThreadLocalMap，则创建一个新的
        // 并且将变量绑定到新创建的实例上
        createMap(t, value);
    }
}
// 获取线程t的ThreadLocalMap成员
ThreadLocalMap getMap(Thread t) {
    return t.threadLocals;
}
// 线程t创建一个ThreadLocalMap成员
// 为新的Map成员设置第一个Key-Value对，Key为当前的ThreadLocal实例
void createMap(Thread t, T firstValue) {
    t.threadLocals = new ThreadLocalMap(this, firstValue);
}
```

<a name="CUrvQ"></a>

#### set的执行流程总结：

1. 获得当前线程，然后获得当前线程的ThreadLocalMap成员，暂存于map局部变量中
2. 如果map不为空，就将Value设置到map中，当前的ThreadLocal作为Key
3. 如果map为空，那么为当前线程创建map，然后设置第一个“Key-Value”，Key为当前的ThreadLocal实例，Value为set()方法的参数value值。 <a name="Oun4e"></a>

### 2. get()方法

get()方法用于获取当前线程对应的ThreadLocalMap中的值。

```java
public T get() {
    // 获得当前线程对象
    Thread t = Thread.currentThread();
    // 获得线程对象的ThreadLocalMap成员
    ThreadLocalMap map = getMap(t);
    // 如果当前线程内部的map成员存在
    if (map != null) {
        // 以当前ThreadLocal为Key，尝试获得对应的Entry
        ThreadLocalMap.Entry e = map.getEntry(this);
        if (e != null) {
            // 如果Entry存在就返回对应值
            @SuppressWarnings("unchecked")
            T result = (T)e.value;
            return result;
        }
    }
    // map不存在，返回初值
    return setInitialValue();
}

// 设置ThreadLocal关联的初始值并返回
private T setInitialValue() {
    // 调用初始化钩子函数，获取初值
    T value = initialValue();
    Thread t = Thread.currentThread();
    ThreadLocalMap map = getMap(t);
    // 如果map存在，则赋初值
    if (map != null) {
        map.set(this, value);
    } else {
        // 不存在就先创建
        createMap(t, value);
    }
    if (this instanceof TerminatingThreadLocal) {
        TerminatingThreadLocal.register((TerminatingThreadLocal<?>) this);
    }
    return value;
}
```

<a name="PUYo0"></a>

#### get的执行流程

1. 先尝试获得当前线程，然后获得当前线程的ThreadLocalMap成员，暂存于map变量。
2. 如果获得的map不为空，那么以当前ThreadLocal实例为Key，获得对应的Entry
3. 如果Entry存在，就返回对应的Value
4. 如果Entry不存在，就先initialValue计算出ThreadLocal的初始值，并设置在map中。如果map不存在，就会给当前线程创建一个新的ThreadLocalMap变量，并且赋第一个Key-Value <a name="KaNC5"></a>

### 3. remove()方法

移除当前Thread的ThreadLocalMap中对应的值。

```java
public void remove() {
    ThreadLocalMap m = getMap(Thread.currentThread());
    if (m != null) {
        m.remove(this);
    }
}
```

<a name="L6Tq9"></a>

### 4. initialValue()方法

如果在没有set()的情况下直接调用了get()方法，此时肯定只能拿到null值。所以如果不想得到null值想要给它赋一个初始值，可以重写initialValue()方法。

```java
protected T initialValue() {
    return null;
}
```

但是重写方法写起来太麻烦了，JDK提供了ThreadLocal的内部静态子类SuppliedThreadLocal。并且提供了ThreadLocal.withInitial(...)静态工厂方法。
实例代码：í

```java
ThreadLocal<Foo> LOCAL_FOO = ThreadLocal.withInitial(() -> new Foo());
```

<a name="ruVjc"></a>

### 5. withInitial()和SuppliedThreadLocal类的源码

```java
public static <S> ThreadLocal<S> withInitial(Supplier<? extends S> supplier) {
    return new SuppliedThreadLocal<>(supplier);
}
```

```java
// 静态内部类
// 继承了ThreadLocal，重写initialValue()方法，返回钩子函数的值作为初始值
static final class SuppliedThreadLocal<T> extends ThreadLocal<T> {

    private final Supplier<? extends T> supplier;

    SuppliedThreadLocal(Supplier<? extends T> supplier) {
        this.supplier = Objects.requireNonNull(supplier);
    }

    @Override
    protected T initialValue() {
        return supplier.get();
    }
}

```

<a name="tvJNg"></a>

## `ThreadLocalMap`源码

<a name="NwwEc"></a>

### 1. ThreadLocalMap的主要成员变量

ThreadLocalMap的成员变量与HashMap非常类似：

```java
public class ThreadLocal<T> {
    // 省略其他
static class ThreadLocalMap {
    // Map的条目数组，作为哈希表使用
	private Entry[] table;
    // Map的初始容量16
    private static final int INITIAL_CAPACITY = 16;
    // Map的条目数量
    private int size = 0;
    // 扩容因子
    private int threshold;
    // Map的条目类型，一个静态的内部类
    // Entry继承于WeakReference，Key为ThreadLocal实例
    static class Entry extends WeakReference<ThreadLocal<?>> {
        Object value;
        Entry(ThreadLocal<?> k, Object v) {
            super(k);
            value = v;
        }
    }    
}
```

`ThreadLocal`中的`get()`，`set()`，`remove()`方法都设计到`ThreadLocalMap`中的方法调用，主要调用了如下几个方法：

- `set(ThreadLocal<?> key，Object value)`：向`Map`中设置`Key-Value Pair`
- `getEntry(ThreadLocal<?> key)`：从`Map`实例获取`Key`(`ThreadLocal`) 所属的`Entry`
- `remove(ThreadLocal<?> key)`：根据`Key`(`ThreadLocal`)从`Map`中移除对应`Entry` <a name="YrtoG"></a>

### 2. set(ThreadLocal\<?> key，Object value)方法

```java
private void set(ThreadLocal<?> key, Object value) {

    Entry[] tab = table;
    int len = tab.length;
    // 根据key的hashCode，找到key在数组上的槽。
    int i = key.threadLocalHashCode & (len-1);
	// 从槽点i开始for循环，寻找“已存在的槽点”或者“空白槽点”。
    // 这两个寻找的目标肯定有一个存在，因为如果没有“空白槽点”，那么肯定会在之前就触发了扩容操作。
    for (Entry e = tab[i];
         e != null;
         e = tab[i = nextIndex(i, len)]) {
        ThreadLocal<?> k = e.get();
		// 找到了现有的槽点。对值进行替换
        if (k == key) {
            e.value = value;
            return;
        }
		// 找到异常槽点，说明被GC掉了，重设Key值和Value值
        if (k == null) {
            replaceStaleEntry(key, value, i);
            return;
        }
    }

    // 啥也没找到，则在空白位置新增Entry
    tab[i] = new Entry(key, value);
    // 维护Map的size
    int sz = ++size;
    // 清理Key为null的无效Entry。
    // 没有可清理的Entry，并且现有条目数量大于扩容因子，则触发扩容操作。
    if (!cleanSomeSlots(i, sz) && sz >= threshold)
        rehash();
}
```

<a name="rF2tg"></a>

### 3. Entry的Key为什么使用弱引用

<a name="gbQhn"></a>

#### 什么是弱引用

弱引用`(Weak Reference)`指向的对象只能生存到下一次垃圾回收之前，也就是说，当GC发生时，无论内存够不够，仅被弱引用所指向的对象都会被GC回收掉，而拥有强引用指向的对象则不会被直接回收掉。

`Entry`用于保存`ThreadLocalMap`的`Key-Value Pair`，但是`Entry` 使用了`ThreadLocal`实例包装后的弱引用对象作为`Key`，其源码如下：

```java
// Entry继承了WeakReference，并且使用WeakReference对Key进行包装
static class Entry extends WeakReference<ThreadLocal<?>> {
    /** The value associated with this ThreadLocal. */
    Object value;
    Entry(ThreadLocal<?> k, Object v) {
        super(k);
        value = v;
    }
}
```

<a name="QkAwZ"></a>

#### 为什么使用弱引用

```java
public void funcA() {
    // 创建一个线程的本地变量
	ThreadLocal local = new ThreadLocal<Integer>();
    // 设置值
    local.set(100);
    // 使用值
    local.get();
    // 方法结束, 局部变量销毁
}
```

我们使用线程`thread-1`调用`funcA()`方法，此时新建了一个`ThreadLocal`变量，所以在对应的`ThreadLocalMap`中存在以`local`为`Key`，`100` 为`value`的`Key-Value Entry`，这时候`funcA()`调用完毕，该栈帧销毁，局部变量`local`已经没了，但是线程`thread-1`对应的`ThreadLocalMap`中的`Key-Value Entry`还存在，这个时候如果使用的是`WeakReference`，这个可能导致内存泄漏的值就会被回收掉。 <a name="ME97D"></a>

### 4. 总结

由于`ThreadLocalMap`中`Entry`的`Key`使用了弱引用，在下次`GC`发生时，就可以是那些没有被其他强引用指向，仅被`Entry`的`Key`指向的`ThreadLocal`实例能够被顺利回收。并且在`Entry`的`Key`引用被回收之后，其`Entry`的`Key`变成`null`，后续当`ThreadLocal`在做`get()`，`set()`，`remove()`的时候，都会触发`ThreadLocalMap`的内部检查逻辑。清除`Key`为`null`的`Entry`。
使用`ThreadLocal`会发生内存泄漏的前提总结如下:

1. 线程长时间运行而没有被销毁。线程池中的`Thread`实例很容易满足此条件。
2. `ThreadLocal`引用被设置为`null`，且后续在同一个`Thread`实例执行期间，没有发生对其他`ThreadLocal`实例的`get()`, `set()`, `remove()`操作。只要存在一个针对任何`ThreadLocal`的`get()`, `set()`, remove()，就会触发Thread实例拥有的`ThreadLocalMap`的`Key`为`null`的Entry清理工作，释放掉ThreadLocal中弱引用为null的Entry。 <a name="yv6IT"></a>

## 参考资料

- [ThreadLocal与WeakReference](https://www.jianshu.com/p/c0ca0db80299)
