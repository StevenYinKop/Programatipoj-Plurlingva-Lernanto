---
title: "IAM: Users & Groups & Roles & Policies"
url: https://www.yuque.com/stevenyin/liv/vvextqycl6qkmkcq
---

> IAM is a Global service.

<a name="J0Jr4"></a>





|   | **Root ** | ** User ** | ** Role ** |
| --- | --- | --- | --- |
| 密码登录 | 总是 | 是 | 否 |
| Access Key | 是（不推荐） | 是 | 否 |
| 可以属于一个组 | 否 | 是 | 否 |
| 可以关联EC2实例 | 否 | 否 | 是 |

<a name="TiPH7"></a>

## Users & Groups

<a name="gRHGA"></a>

## Best Practices

- Don’t use the root account except for AWS account setup • One physical user = One AWS user
- Assign users to groups and assign permissions to groups
- Create a strong password policy
- Use and enforce the use of Multi Factor Authentication (MFA)
- Create and use Roles for giving permissions to AWS services
- Use Access Keys for Programmatic Access (CLI / SDK)
- Audit permissions of your account with the IAM Credentials Report • Never share IAM users & Access Keys

        <br /> 	 
