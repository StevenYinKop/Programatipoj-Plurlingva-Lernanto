---
title: Spring bean 的生命周期
url: https://www.yuque.com/stevenyin/liv/ixh2wl
---


转自： <https://blog.csdn.net/Butterfly_resting/article/details/89735792>

1. Spring 容器根据配置中的 bean 定义中实例化 bean。
2. Spring 使用依赖注入填充所有属性，如 bean 中所定义的配置。
3. 如果 bean 实现 BeanNameAware 接口，则工厂通过传递 bean 的 ID 来调用 setBeanName()。
4. 如果 bean 实现 BeanFactoryAware 接口，工厂通过传递自身的实例来调用 setBeanFactory()。
5. 如果存在与 bean 关联的任何 BeanPostProcessors，则调用 postProcessBeforeInitialization() 方法。
6. 如果为 bean 指定了 init 方法（ 的 init-method 属性），那么将调用它。
7. 最后，如果存在与 bean 关联的任何 BeanPostProcessors，则将调用 postProcessAfterInitialization() 方法。
8. 如果 bean 实现 DisposableBean 接口，当 spring 容器关闭时，会调用 destory()。
9. 如果为 bean 指定了 destroy 方法（ 的 destroy-method 属性），那么将调用它。
