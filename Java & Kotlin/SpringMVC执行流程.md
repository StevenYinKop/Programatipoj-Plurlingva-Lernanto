---
title: SpringMVC执行流程
url: https://www.yuque.com/stevenyin/liv/mnmgn2
---

- （1）用户发送请求至前端控制器DispatcherServlet；
- （2） DispatcherServlet收到请求后，调用HandlerMapping处理器映射器，请求获取Handle；
- （3）处理器映射器根据请求url找到具体的处理器，生成处理器对象及处理器拦截器(如果有则生成)一并返回给DispatcherServlet；
- （4）DispatcherServlet 调用 HandlerAdapter处理器适配器；
- （5）HandlerAdapter 经过适配调用 具体处理器(Handler，也叫后端控制器)；
- （6）Handler执行完成返回ModelAndView；
- （7）HandlerAdapter将Handler执行结果ModelAndView返回给DispatcherServlet；
- （8）DispatcherServlet将ModelAndView传给ViewResolver视图解析器进行解析；
- （9）ViewResolver解析后返回具体View；
- （10）DispatcherServlet对View进行渲染视图（即将模型数据填充至视图中）
- （11）DispatcherServlet响应用户。
