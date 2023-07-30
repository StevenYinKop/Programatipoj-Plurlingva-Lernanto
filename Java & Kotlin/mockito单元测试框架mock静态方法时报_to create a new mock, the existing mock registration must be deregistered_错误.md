---
title: mockito单元测试框架mock静态方法时报"to create a new mock, the existing mock
  registration must be deregistered"错误
url: https://www.yuque.com/stevenyin/liv/ouux3d
---

最大的原因就是除了当前的单元测试类中，其他的地方可能也对这个静态方法进行了mock，

所以在每一次进行mock的时候， 对单个单元测试， 应该mock完再清除掉， 下次需要使用的时候再重新mock

      private MockedStatic<UserContext> mockStatic;

      @BeforeEach
      public void beforeEach() {
        mockStatic = Mockito.mockStatic(UserContext.class);
      }

      @AfterEach
      public void afterEach() {
        mockStatic.close();
      }
