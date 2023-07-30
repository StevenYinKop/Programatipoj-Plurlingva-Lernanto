---
title: '@Scope("prototype")的正确用法——解决Bean的多例问题'
url: https://www.yuque.com/stevenyin/liv/hv0bu0
---

<a name="gKOih"></a>

## 问题，Spring管理的某个Bean需要使用多例

在使用了Spring的web工程中，除非特殊情况，我们都会选择使用Spring的IOC功能来管理Bean，而不是用到时去new一个。Spring管理的Bean默认是单例的（即Spring创建好Bean，需要时就拿来用，而不是每次用到时都去new，又快性能又好），但有时候单例并不满足要求（比如Bean中不全是方法，有成员，使用单例会有线程安全问题，可以搜索线程安全与线程不安全的相关文章），你上网可以很容易找到解决办法，即使用@Scope("prototype")注解，可以通知Spring把被注解的Bean变成多例，如下所示：

作者：猫尾草
链接：https://www.jianshu.com/p/54b0711a8ec8
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
