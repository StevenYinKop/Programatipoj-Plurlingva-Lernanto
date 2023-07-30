---
title: SpringBoot 生命周期钩子方法
url: https://www.yuque.com/stevenyin/liv/zi3wvl
---

<a name="8040a6e9"></a>

# Spring Bean实例化完成后进行初始化操作的方法

<a name="df368884"></a>

## 前言

本文将介绍,当`Bean`加载完成后, 自动执行初始化逻辑的方法.

<a name="227e47a4"></a>

## 程序启动后进行初始化操作

由于`Spring`的控制反转特性(IoC),我们不应该简单地在`Bean`的构造方法中写这些逻辑,`Bean`是由`Spring`容器创建的,在这个过程中不受控

请看下面这个例子:

```java
@Component
public class InvalidInitExampleBean {
 
    @Autowired
    private Environment env;
 
    public InvalidInitExampleBean() {
        env.getActiveProfiles();
    }
}
```

在这个例子中, 我们想要通过`@Autowired`的方式把`Environment`的对象注入进来, 然后在构造方法中使用它, 但是实际上, 这个时候`Bean`还没有完全实例化结束, 也就是说此时还没有对应的`env`对象, 那么结果就是在这里抛出空指针异常`NullPointerExceptions`

为了解决这个问题,Spring给我们提供了几种方法

<a name="747de5ca"></a>

### 使用注解 `@PostConstruct`

被这个注解修饰的方法, 在当前`Bean`实例化完成后会立即执行.

所以刚刚的例子可以写成这样:

```java
@Component
public class PostConstructExampleBean {
 
    private static final Logger LOG 
      = Logger.getLogger(PostConstructExampleBean.class);
 
    @Autowired
    private Environment environment;
 
    @PostConstruct
    public void init() {
        LOG.info(Arrays.asList(environment.getDefaultProfiles()));
    }
}
```

这样的话, `Environment`的实例可以正常初始化, 也不会抛错了

<a name="7410d630"></a>

### 实现`InitializingBean`接口

`InitializingBean`接口比`@PostConstruct`使用起来更加简单, 你只需要在对应的类上实现这个接口, 并且重写它对应的`afterPropertiesSet()`就可以了, 效果和刚刚一样

```java
@Component
public class InitializingBeanExampleBean implements InitializingBean {
 
    private static final Logger LOG 
      = Logger.getLogger(InitializingBeanExampleBean.class);
 
    @Autowired
    private Environment environment;
 
    @Override
    public void afterPropertiesSet() throws Exception {
        LOG.info(Arrays.asList(environment.getDefaultProfiles()));
    }
}
```

<a name="8e33fb63"></a>

### `ApplicationListener`

`ApplicationListener`是一个基于观察者模式的事件机制,具体过于复杂, 在这里为了实现我们的需求(容器启动后进行相关逻辑操作), 不会对`ApplicationListener`进行过多解释, 我们只需要在相应的类上实现`ApplicationListener<ContextRefreshedEvent>`接口, 并且重写`onApplicationEvent`方法即可.

```java
@Component
public class StartupApplicationListenerExample implements
  ApplicationListener<ContextRefreshedEvent> {
 
    private static final Logger LOG 
      = Logger.getLogger(StartupApplicationListenerExample.class);
 
    public static int counter;
 
    @Override public void onApplicationEvent(ContextRefreshedEvent event) {
        LOG.info("Increment counter");
        counter++;
    }
}
```

值得一提的是, 自从Spring 4.2以后，可以使用@EventListener注解来实现相同的效果:

```java
@Component
public class EventListenerExampleBean {
 
    private static final Logger LOG 
      = Logger.getLogger(EventListenerExampleBean.class);
 
    public static int counter;
 
    @EventListener
    public void onApplicationEvent(ContextRefreshedEvent event) {
        LOG.info("Increment counter");
        counter++;
    }
}
```

<a name="c40a189f"></a>

### 在`@Bean`的`initMethod`属性

在`@Bean`注解中, 有一个`initMethod`属性, 这个属性的值接受`String`类型, 我们要做的是:

1. 在`Bean`中编写需要在初始化后执行的方法(假设方法名为`init`)
2. 在注入这个`Bean`的时候(`@Configuration`或`XML`形式), 通过`initMethod`属性填写对应的方法名即`@Bean(initMethod="init")`

如下:

```java
public class InitMethodExampleBean {
 
    private static final Logger LOG = Logger.getLogger(InitMethodExampleBean.class);
 
    @Autowired
    private Environment environment;
 
    public void init() {
        LOG.info(Arrays.asList(environment.getDefaultProfiles()));
    }
}
```

1. 使用注解的方式注册[@Bean ](/Bean)

```java
@Bean(initMethod="init")
public InitMethodExampleBean exBean() {
    return new InitMethodExampleBean();
}
```

2. 使用`XML`文件

```xml
<bean id="initMethodExampleBean"
  class="org.baeldung.startup.InitMethodExampleBean"
  init-method="init">
</bean>
```

<a name="43fd9fdf"></a>

### Constructor Injection

对于`Spring`来说, 当我们使用一个`Bean`的时候, 可以在成员变量声明时, 进行`@Autowired`, 同样也可以在这个`Bean`初始化的时候在它的构造方法上进行`@Autowired`(注意, 这种做法是在**构造方法**上进行注入, 而不是在成员变量上, 所以和最开头说的\_不能在构造方法中写逻辑\_并不矛盾)

具体实现如下:

```java
@Component
public class LogicInConstructorExampleBean {
 
    private static final Logger LOG 
      = Logger.getLogger(LogicInConstructorExampleBean.class);
 
    private final Environment environment;
 
    @Autowired
    public LogicInConstructorExampleBean(Environment environment) {
        this.environment = environment;
        LOG.info(Arrays.asList(environment.getDefaultProfiles()));
    }
}
```

这样实现并不会抛出`NullPointerException`, `environment`可以正常地注入进构造方法中

<a name="3d9fb526"></a>

### Spring Boot `CommandLineRunner`

`Spring Boot` 提供了`CommanLineRunner`接口来实现我们的需求. **当然要实现接口的`run()`方法**

```java
@Component
public class CommandLineAppStartupRunner implements CommandLineRunner {
    private static final Logger LOG =
      LoggerFactory.getLogger(CommandLineAppStartupRunner.class);
 
    public static int counter;
 
    @Override
    public void run(String...args) throws Exception {
        LOG.info("Increment counter");
        counter++;
    }
}
```

**注意**: 当我们实现了多个`CommandLineRunner`的时候, 可以在定义`@Component`的同时, 再加上`@Order`对`Bean`进行排序

<a name="88757741"></a>

### Spring Boot的`ApplicationRunner`接口

与`CommandLineRunner`接口,SpringBoot提供了`ApplicationRunner`接口并且也要实现`run()`方法.而区别在于, 这个`run()`方法的入参并不是一个`String`数组`args`而是一个封装类`ApplicationArguments`.

```java
@Component
public class AppStartupRunner implements ApplicationRunner {
    private static final Logger LOG =
      LoggerFactory.getLogger(AppStartupRunner.class);
 
    public static int counter;
 
    @Override
    public void run(ApplicationArguments args) throws Exception {
        LOG.info("Application started with option names : {}", 
          args.getOptionNames());
        LOG.info("Increment counter");
        counter++;
    }
}
```

<a name="534206ff"></a>

## 混合使用时的优先级问题

面对不同的业务场景, 我们可能会混用上述的各种骚操作.那么需要了解他们的执行顺序:

1. `Bean`的构造方法
2. `@PostConstruct`注解
3. `InitializingBean`接口的`afterPropertiesSet()`方法
4. 在`@Bean`或`XML`中声明的`initMethod`属性

下面这个例子可以很清晰地看出先后顺序:

```java
@Component
@Scope(value = "prototype")
public class AllStrategiesExampleBean implements InitializingBean {
 
    private static final Logger LOG 
      = Logger.getLogger(AllStrategiesExampleBean.class);
 
    public AllStrategiesExampleBean() {
        LOG.info("Constructor");
    }
 
    @Override
    public void afterPropertiesSet() throws Exception {
        LOG.info("InitializingBean");
    }
 
    @PostConstruct
    public void postConstruct() {
        LOG.info("PostConstruct");
    }
    // 配置部分没有贴出, 大概就是在@Configuration中声明AllStrategiesExampleBean这个Bean的时候写成这样:@Bean(initMethod="init")
    public void init() {
        LOG.info("init-method");
    }
}
```

当你实例化这个对象的时候, 就会打印出如下log

```log
[main] INFO o.b.startup.AllStrategiesExampleBean - Constructor
[main] INFO o.b.startup.AllStrategiesExampleBean - PostConstruct
[main] INFO o.b.startup.AllStrategiesExampleBean - InitializingBean
[main] INFO o.b.startup.AllStrategiesExampleBean - init-method
```
