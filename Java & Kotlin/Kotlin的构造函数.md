---
title: Kotlin的构造函数
url: https://www.yuque.com/stevenyin/liv/dfffzr
---

Kotlin的构造函数在一开始学习的阶段, 有点摸不清头脑, 因为既可以放在类声明上, 又可以用`constructor`修饰, 还可以在`init`代码块中编写一些初始化逻辑

<a name="GMazC"></a>

## 主构造函数

<a name="ip4m3"></a>

### 使用示例

紧跟在类名后面的构造函数是**主构造函数**具体语法为:

```kotlin
class Person constructor(firstName: String) { /*...*/ }
```

如果主构造函数没有任何注解或者可见性修饰符，可以省略这个 `_constructor_`关键字。即:

```kotlin
class Person(firstName: String) { /* ... */ }
```

如果你想要私有构造方法, 那么这个`_constructor_`就不能省略, 即:

```kotlin
class Person private constructor(firstName: String) { /* ... */ }
```

<a name="BsnzA"></a>

### `init`代码块

当使用这种构造的方式声明一个类的时候, 等于是没有构造方法的方法体了, 所以想要在构造的时候添加一些逻辑, 就需要使用`init`代码块, 即:

```kotlin
class Person(name: String) {
	init {
		println("class Person initialized! name=$name")
        println("class Person initialized! name=${this.name}")
	}
}

fun main() {
	Person("stevenyin")
}
```

代码执行结果为:

    class Person initialized! name=stevenyin

从上例中可以看出, `init`块中可以使用主构造中的参数.

如果存在多个`init`初始化块, 执行的顺序如下代码所示:

```kotlin
class InitOrderDemo(name: String) {
    val firstProperty = "First property: $name".also(::println)
    
    init {
        println("First initializer block that prints ${name}")
    }
    
    val secondProperty = "Second property: ${name.length}".also(::println)
    
    init {
        println("Second initializer block that prints ${name.length}")
    }
}


fun main() {
	Person("stevenyin")
}
```

结果为:

    First property: stevenyin
    First initializer block that prints stevenyin
    Second property: 9
    Second initializer block that prints 9

<a name="NzkAh"></a>

### 在构造函数中使用`var`/`val`修饰符

我们在Java中经常需要实现类似于下面这样的操作:

```java
class Person {
	private String name;
    public Person(String name) {
    	this.name = name;
    }
}
```

也就是在构造的时候传入成员变量的初始值, 对它进行赋值, 在kotlin中, 我们完全可以使用`var`或者`val`关键字来对成员变量进行复制, 上面的例子就可以改写为:

```kotlin
class Person(var name: String)
```

我们用一个main函数来测试一波:

```kotlin
fun main() {
	val person = Person("stevenyin")
	println(person.name)
}
```

控制台输出:

    stevenyin

但是如果我们不加`var`/`val`的话, 对于那么这个变量`name`就可以理解成是构造函数的一个普普通通的参数而已, 与成员变量没有任何关系.

```kotlin
class Person(name: String)

fun main() {
	val person = Person("stevenyin")
	println(person.name)
}
```

这个时候代码直接就报错了, 告诉我们`person`对象中根本就不存在`name`这个属性.
使用`val`修饰符也是同理, 只不过只用了`val`修饰符就代表这个变量赋值后就无法更改了, 因为它变成了一个只读的属性. <a name="Wfe1A"></a>

## 从构造函数

<a name="pW1AA"></a>

### 介绍

在很多情况下, 一个构造函数往往无法满足业务需求, 我们需要多个构造函数, 这个时候可以使用`constructor`来声明其余的构造函数:

```kotlin
class Person(val name: String) {
    var children: List<Person> = mutableListOf()
    constructor(name: String, parent: Person) : this(name) {
        parent.children.add(this)
    }
}
```

但是这里有一个需要注意的地方, 就是所有的从构造函数, 最终都需要直接或者间接调用主构造函数, 类似于上面代码的第三行末尾`: this(name)`
当然, 如果这个类没有主构造函数只有从构造函数, 那就不用进行委托了. <a name="mzoUa"></a>

### 完整示例

```kotlin

class Student (name: String, age: Int) {
	init {
		println("主构造函数传入的参数: name: $name, age: $age;")
	}
	var name: String =  "${name}L"
	var age: Int = age + 1
	init {
		println("主构造函数的成员变量: name: ${this.name}, age: ${this.age};")
	}
	var height: Int = 0
	constructor(name: String, age: Int, height: Int): this(name, age) {
		println("从构造函数传入的参数为: name: $name, age: $age, height: $height")
		this.height = height
	}

	override fun toString() = "Student(name=$name, age=$age, height=$height)"
}

fun main() {
	Student("Steven", 26, 178)
}

```

最终执行的结果是:

    主构造函数传入的参数: name: Steven, age: 26;
    主构造函数的成员变量: name: StevenL, age: 27;
    从构造函数传入的参数为: name: Steven, age: 26, height: 178
