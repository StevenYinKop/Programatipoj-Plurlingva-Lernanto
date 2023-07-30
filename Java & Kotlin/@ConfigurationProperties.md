---
title: "@ConfigurationProperties"
url: https://www.yuque.com/stevenyin/liv/wafa6w
---

<a name="4e0452ee"></a>

# 使用@ConfigurationProperties配置Spring Boot模块

> 很多上了一定规模的应用程序在启动时都需要指定一些参数。 例如，最典型的比如定义要连接的数据库，服务的端口号, 应用的日志记录级别等。

这些参数应该从外部提供, 不能在代码里面写死, 所以我们可以在启动我们的程序的时候通过命令行或者配置文件的形式进行配置

使用`@ConfigurationProperties`这个注解, Springboot可以非常轻松的绑定上面说的参数信息:

现在我们有一个场景, 我们要在应用中发送email, 但是我们不想在任何情况下都发送邮件, 也就是说我们要提供一个开关, 来控制是否发送邮件, 另外，我们希望能够为这些邮件配置默认的标题(subject)，这样我们可以知道这些邮件来自我们的测试环境

<a name="db2c46f5"></a>

## 不用`@ConfigurationProperties`

`Spring Boot`提供了许多不同的选项来将类似这样的参数传递到应用程序中。在本文我们使用的是通过`application.properties`文件来指定我们的配置,这个也是比较常用的形式, 我们可以根据不同的环境指定不同的配置文件：

```properties
myapp.mail.enabled=true
myapp.mail.default-subject=This is a Test
```

有了上面的配置, 我们就可以使用`@Value`来注入配置文件的值

<a name="a620031a"></a>

## 使用`@ConfigurationProperties`

`@Value`可以获得配置文件中的值, 但是，创建一个配置类并且使用`@ConfigurationProperties`注解修饰，这种方式更为方便和安全：

```java
@ConfigurationProperties(prefix = "myapp.mail")
class MailModuleProperties {
  // 如果这个值在配置文件中没有指定, 则可以指定默认值
  private Boolean enabled = Boolean.TRUE;
  private String defaultSubject;
  // getters / setters  
}
```

`@ConfigurationProperties`的基本用法非常简单粗暴, 使用`prefix`属性来指定属性的前缀, 比如上面的例子中, 代表我们的属性全部都要以`myapp.mail`开头, 而接受的属性有`myapp.mail.enabled`和`myapp.mail.default-subject`, 有以下几点请注意:

1. 类本身可以是`private`
2. 字段的`setter`方法必须是`public`的

如果我们将`MailModuleProperties`注入另一个`bean`，则该`bean`现在可以以类型安全的方式访问那些外部配置参数的值。如:

```java
@Service
class UserService {
  @Autowired
  private MailModuleProperties mailModuleProperties;
  public Boolean sendmail() {
    if (!mailModuleProperties.isEnabled()) return;
    MailSender sender = new MailSender();
    sender.setSubject(mailModuleProperties.getDefaultSubject());
    ...
  }
}
```

我们必须要让Spring能够识别到我们自己配置的`@ConfigurationProperties`, 这样才会纳入Spring上下文的管理中

<a name="680385b7"></a>

### 激活`@ConfigurationProperties`

我们可以使用以下几种方式, 将我们自己写的`MailModuleProperties`纳入Spring的管理中:

1. 首先, 我们可以使用`@Component`注解, 这样Spring在进行`ComponentScan`时会新建这个Class的实例

```java
@Component
@ConfigurationProperties(prefix = "myapp.mail")
class MailModuleProperties {
  // ...  
}
```

<a name="cf52413f"></a>

### 使用`@Bean`手动新建

```java
@Configuration
class MailModuleConfiguration {

  @Bean
  public MailModuleProperties mailModuleProperties(){
    return new MailModuleProperties();
  }
}
```

3. 用`@EnableConfigurationProperties`指定激活的`Properties`配置类

```java
@Configuration
@EnableConfigurationProperties(MailModuleProperties.class)
class MailModuleConfiguration {

}
```

以上的4种方式都可以使用, 但是我们更推荐模块化, 在各自的模块中提供对应的`@ConfigurationProperties`类, 这样的话我们在重构的时候不会对其他的模块产生影响.

所以, 我们应该在各自模块的@Configuration文件中激活各自模块的配置文件, 而不是在主应用程序中使用去指定配置.

<a name="2b93bbe4"></a>

## `ignoreInvalidFields`

> 处理属性类型转换失败的情况: 如果我们定义了某一个属性, 但是实际传入的值没办法转换成我们定义的类型该怎么办呢.

我们在配置文件中, 将`enabled`的值改成`abcd`字符串

```properties
myapp.mail.enabled=abcd
```

默认情况下, SpringBoot在启动时读取配置文件的时候, 就会报错, 然后整个应用启动失败:`java.lang.IllegalArgumentException: Invalid boolean value 'abcd'`

但是这是默认情况, 万一我们想要的是, 解析不出来就算, 但是应用不能报错, 那么我们要在配置上面增加一个属性, 如下:

```java
@ConfigurationProperties(prefix = "myapp.mail", ignoreInvalidFields = true)
class MailModuleProperties {
  
  private Boolean enabled = Boolean.TRUE;
  
  // getters / setters
}
```

这样的话, SpringBoot就会把转换失败的值跳过, 继续使用我们指定的默认值(上面的`Boolean.TRUE`或者`null`(如果没有指定默认值)

<a name="ignoreUnknownFields"></a>

## ignoreUnknownFields

如果我们传入的配置文件中, 包含一个我们没有定义的值. 如`myapp.mail.sender=stevenyin`, 这个时候SpringBoot默认会忽略掉这个没有见过的属性.

如:

```properties
myapp.mail.enabled=true
myapp.mail.default-subject=This is a Test
myapp.mail.sender=stevenyin
```

但是这也是默认情况, 我们现在存在这样的场景: 开发时使用的一个变量, 在开发过程中移除了. 如果项目结束, 后人接手看到一个属性, 没见过也不敢删, 就很傻逼. 所以我们在定义这个配置类的时候就指定好, 如果出现了没见过的属性, 报错.

我们可以加入如下配置:

```java
@ConfigurationProperties(prefix = "myapp.mail", ignoreUnknownFields = false)
class MailModuleProperties {
  
  private Boolean enabled = Boolean.TRUE;
  private String defaultSubject;
  
  // getters / setters
}
```

这种情况下, 一旦指定了一些没用的属性, SpringBoot就会启动失败.并且抛错.

`org.springframework.boot.context.properties.bind.UnboundConfigurationPropertiesException:\nThe elements [myapp.mail.sender] were left unbound.`

<a name="a7f6b9e6"></a>

### `ignoreUnknownFields`未来版本会废弃

但是这个属性仍然会存在问题, 如果我们出现两个被`@ConfigurationProperties`修饰的类, 使用了相同的前缀.这样就有可能导致报错

<a name="851ee494"></a>

## 在应用启动时校验`@ConfigurationProperties`

如果我们想要验证传入的参数是否符合我们的语气, 我们可以在这个类上添加`@Validated`属性来校验传入的值, 这种方式更为灵活和强大

```java
@ConfigurationProperties(prefix = "myapp.mail")
@Validated
class MailModuleProperties {

  @NotNull private Boolean enabled = Boolean.TRUE;
  @NotEmpty private String defaultSubject;

  // getters / setters
}
```

这时如果我们没有设置defaultSubject的值, 那么我们在启动应用的时候, 会抛出`BindValidationException`的错误:

```properties
myapp.mail.default-subject=
```

```java
org.springframework.boot.context.properties.bind.validation.BindValidationException: 
   Binding validation errors on myapp.mail
   - Field error in object 'myapp.mail' on field 'enabled': rejected value [null]; ...
   - Field error in object 'myapp.mail' on field 'defaultSubject': rejected value []; ...
```

如果我们想要自定义校验逻辑,那么我们也可以创建一个自定义校验的`annotation`来完成这个功能

当然, 也可以自定义一些校验方法, 如果不满足校验预期就抛出异常, 然后在这些方法上面添加`@PostConstruct`注解, 让他们在项目启动后自动被Spring调用.

<a name="064b799e"></a>

## 复杂的属性类型

其实大部分的情况下, 我们使用的属性应该都是基本的`String`或者`Number`或者`Boolean`, 但是有一些场景我们可能需要一些复杂的数据类型来支撑完成我们的需求.

<a name="3b6de852"></a>

### Lists,Sets

现在有一个需求, 我们有一个邮件服务器的列表需要维护, 这时我们需要配置多个邮件服务器IP, 那我们在配置类里面可以这样写, (对于Set类型来说, 配置的方法是一样的):

```java
@ConfigurationProperties(prefix = "myapp.mail")
class MailModuleProperties {

  private List<String> smtpServers;
  
  // getters / setters
  
}
```

在我们的配置文件中这样写:

```properties
myapp.mail.smtpServers[0]=server1
myapp.mail.smtpServers[1]=server2
```

而如果我们使用的是`yaml`文件来进行配置, 那么整个配置文件的格式看起来会更加直观一些:

```yml
myapp:
  mail:
    smtp-servers:
      - server1
      - server2
```

<a name="d735fdc4"></a>

### 时间类型(`Durations`)

SpringBoot内建支持`Durations`类型来支持解析时间值

```java
@ConfigurationProperties(prefix = "myapp.mail")
class MailModuleProperties {

  private Duration pauseBetweenMails;
  
  // getters / setters
  
}
```

支持的值:

1. 传入毫秒值(milliseconds)
2. 传入带单位的值(接受`ns`, `us`, `ms`, `s`, `m`, `h`, `d`)

```properties
myapp.mail.pause-between-mails=5s
```

<a name="56662d7c"></a>

### 文件大小(`DataSize`)

```java
@ConfigurationProperties(prefix = "myapp.mail")
class MailModuleProperties {

  private DataSize maxAttachmentSize;
  
  // getters / setters
  
}
```

支持的值:

1. 字节数(`bytes`)
2. 传入带单位的值(接受`B`, `KB`, `MB`, `GB`, `TB`)

```properties
myapp.mail.max-attachment-size=1MB
```

<a name="5d63fea5"></a>

### 自定义类型

在某一些奇葩场景中, 我们可能还需要一些特定的数据类型(可能是我们自定义的类型)来完成配置.假设我们接下来需要一个叫做`Weight`的自定义类型来进行配置, 它配置了一个重量信息并且用`5kg`这样的文字来描述重量

```java
@ConfigurationProperties(prefix = "myapp.mail")
class MailModuleProperties {

  private Weight maxAttachmentWeight;
  
  // getters / setters
}
```

```properties
myapp.mail.max-attachment-weight=5kg
```

这种情况下, 我们有两种简单的方式来对传入的值进行解析:

1. `Weight`有一个`public Weight(String weight) {...}`的构造方法, 或者
2. `Weight`有一个`public static Weight valueOf(String weight) {...}`的静态方法, 并且返回`Weight`对象.

   如果我们确实没办法提供这样的构造或者`valueOf`方法, 那么就要稍微费点事, 实现一个`Converter`接口来解析这个Weight类型, 这个接口需要实现`public Weight convert(String source) {...}`方法, 能够实现和上面`valueOf`一样的功能.

```java
class WeightConverter implements Converter<String, Weight> {

  @Override
  public Weight convert(String source) {
    // create and return a Weight object from the String
  }

}
```

当我们创建完converter之后, 需要让SpringBoot知道我们创建了这个Converter, 也就是要在`@Configuration`修饰的配置类种, 声明一个`WeightConverter`的`Bean`, 并且一定要写上`@ConfigurationPropertiesBinding`注解!一定要写上`@ConfigurationPropertiesBinding`注解!一定要写上`@ConfigurationPropertiesBinding`注解!

```java
@Configuration
class MailModuleConfiguration {

  @Bean
  @ConfigurationPropertiesBinding
  public WeightConverter weightConverter() {
    return new WeightConverter();
  }

}
```

当然这只是一个例子, 并没有email需要提供`5kg`这样的属性, 这种场景实在比较少, 一般情况下没必要为了一个配置信息搞这么多东西(自定义类型, 自定义Converter, 声明@ConfigurationPropertiesBinding等)

<a name="54bbba80"></a>

# 结论

Spring Boot的@ConfigurationProperties非常强大, 它能够将配置信息绑定到Java Bean上, 并且能够提供类型安全的访问

这样我们不仅可以为我们的应用程序简单地创建一个配置Bean，还可以利用此功能为每个模块创建一个单独的配置Bean，我们可以灵活地将不同的模块分离, 并且在需要使用的时候提供对应的参数
