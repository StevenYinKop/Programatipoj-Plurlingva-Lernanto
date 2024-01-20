## 1. 面试的本质是寻找同类
### 错误案例
Q: 你学过计算机基础课程吗?
A: 没有学过
### 与面试官寻找共鸣
Q: 你学过计算机基础课程吗?
A: 我每天都有自学和了解计算机基础的只是

## 2. 问题之间是可以相互转化的
Q: 你有没有高并发编程的经验?
A: 高并发这种事情我整天都在想,请出题!

将"**有没有**"类型的问题转换为"**知识点**"考察

面试官可能会就高并发编程问你一写类似于: "_如何分库分表?_", "_缓冲区如何使用_", "_高并发网络IO如何处理?_"这类具体的问题

## 3. 问题是可以被拆解的
Q: 有没有大型项目的经验?
A: 什么样的大项目呢? 是需求多? 排期特别长? 沟通复杂? 团队沟通成本高? 技术特别难?

这样的话, 能够将这种虚的问题转换为实实在在的问题.

## 4. 不要被面试官牵着鼻子走, 引导面试官
Q: 流是不是缓冲区?

如果没有学习过流和缓冲区,这个问题无从下手.

## 5. 给面试官有思想深度的回答, 避免背诵
使用非官方,简介而本质的回答

> LinkedHashMap 是一个元素间用链表相连的HashTable

> HashMap就是用HashTable实现的Map, TreeMap使用树实现的Map, Map是一种映射关系

> B+ 树是一棵支持区间查找的树


## 容器, 集合, 映射
### 容器
> 存储一组对象并能够进行增删改
> 
#### 随机序列产生器
```java
public class RandomStringGenerator<T> implements Iterable<T> {
    private final List<T> list;
    public RandomStringGenerator(List<T> list) {
        this.list = list;
    }
    
    @Override
    public Iterator<T> Iterator() {
        return new Iterator<T>() {
            @Override
            public boolean hashNext() {
                return true;
            }
            public T next() {
                return list.get((int) list.size() * Math.random());
            }
        };
    }
}

```
#### Java Lambda -> Lazy evaluation
### 集合(Set)

#### 1. 内容不重复的容器
#### 实现
1. ConcurrentSkipListSet - 跳表
2. CopyOnWriteArraySet - 数组
3. EnumSet - 位运算
4. HashSet - 哈希表
5. ImmutableCollections.SetN - 哈希表
6. LinkedHashSet - 哈希表
7. TreeSet - 树

#### 顺序问题
- HashSet是无序的,稀疏的
- TreeSet是红黑树实现的,本质是一种二叉搜索树,可以保证顺序
- TreeSet的Super Interface是NavigableSet<T>
lower/higher
floor/ceiling

函数式编程 ->
immutable/pure
lazy
safety - monad 架构


Recursion / Backtracking
39, 40, 78, 90, 46, 47
Graph Travel - DFS, BFS, Topological Sorting
133, 127, 490, 210, 269
Binary Tree / Binary Search Tree(BST)
94, 236, 297, 102, 314, 98
Binary Search
34, 162, 69, 81
Linked List Manipulation
206, 237, 92, 21, 876, 143
Data Structure
242, 133, 127, 155, 225, 215, 23
Pointer Manipulation
239, 3, 76
Greedy
122, 605
Sorting
Time—O(N log N), Merge Sort—Space O(N), Quick sort, 148
Convert Real Life Problem to Code
146, 1066, 490

simultaneously

Responsiveness in User Interface

Responsiveness achieved by concurrency
Responsiveness achieved by Parallelism


illusion
caveat 


Context Switch

- Context switch is not cheap, and is the price of multitasking(concurrency)
- Same as we humans when we multitask - Takes time to focus
- Each thread consumes resources in the CPU and Memory
- When we switch to a different thread:
  - Store data for one thread
  - Restore data for another thread

Key Takeaways
- Too many threads - Thrashing, spending more ime in management than real productive work.
- Threads consume less resources than processes.
- Context switching between threads from the same process is cheaper than context switch between different processes.

Threads scheduling - First Come First Serve
- Problem - Long thread can cause starvation
- May cause User Interface threads being unresponsive - Bad User Experience
  
Threads scheduling - Shortest Job First

Threads scheduling - Dynamic Priority
- Using Dynamic Priority, the OS will give preference for Interactive threads

## When to prefer Multithreaded Architecture?
- Prefer if the tasks share a lot of data
- Threads are much faster to to create and destroy
- Switching between threads of the same process is faster(shorter context switches)

## When to prefer Multi-Process Architecture?
- Security and stability are of higher importance
- Tasks are unrelated to each other
