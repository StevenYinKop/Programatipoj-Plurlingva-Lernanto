---
title: What's difference between "NotAction" and "Effect:Deny"
url: https://www.yuque.com/stevenyin/liv/py7oh5fl521urdql
---

<a name="wlWzK"></a>

## I'm using IAM policies to configure some permission stuffs, what will happen if I do like this:

```json
{
    "Statement": [
        {
            "Effect": "Allow",
            "NotAction": [
                "iam:*",
                "organizations:*",
                "account:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateServiceLinkedRole",
                "iam:DeleteServiceLinkedRole",
                "iam:ListRoles",
                "organizations:DescribeOrganization",
                "account:ListRegions"
            ],
            "Resource": "*"
        }
    ]
}
```

The policy you have provided allows the following actions:

- Any action except for iam:*, organizations:*, and account:* is allowed on any resource (Effect: Allow, NotAction, Resource: *).
- iam:CreateServiceLinkedRole, iam:DeleteServiceLinkedRole, iam:ListRoles, organizations:DescribeOrganization, and account:ListRegions actions are allowed on any resource (Effect: Allow, Action, Resource: *).

This policy grants broad access to any action except for those related to IAM, Organizations, and Account management. It also explicitly allows certain IAM, Organizations, and Account management actions.
It's important to note that the NotAction condition only applies to the first statement. This means that the second statement would not be affected by the NotAction condition in the first statement. Therefore, the second statement would allow the specified actions on any resource, regardless of whether they are related to IAM, Organizations, or Account management.
In general, it is recommended to follow the principle of least privilege when configuring IAM policies. This means granting only the minimum permissions required for a user or resource to perform their intended actions. A more restrictive policy may be preferable in some cases, depending on the specific use case and the level of risk involved. <a name="z4GKa"></a>

## If I only use second Statement, it that same thing?

If you only use the second statement, it would allow the same actions as the second statement in your original policy:

- iam:CreateServiceLinkedRole
- iam:DeleteServiceLinkedRole
- iam:ListRoles
- organizations:DescribeOrganization
- account:ListRegions

However, it would also deny access to any other action, even if it is related to the allowed services. This means that if a user needs to perform any other action related to IAM, Organizations, or Account management, they would not be able to do so.
So while the second statement alone would provide a more restrictive policy compared to the original policy, it may not be sufficient depending on the specific use case and the level of access required. It is important to carefully consider the access needs of your users and resources when configuring IAM policies. <a name="R9XLN"></a>

## So in first case, can I use S3? what about in second case?

In the first case, you can use S3 as long as you do not perform any IAM, Organizations, or Account management actions, since those actions are not allowed by the policy. Any other actions on S3 or any other AWS service would be allowed.
In the second case, you can only use the specific IAM, Organizations, and Account management actions that are allowed by the policy, and any other actions on any other AWS service would be denied. This means that you would not be able to use S3 or any other AWS service unless you need to perform one of the allowed actions.
It's important to note that the Resource element in the policy statements can further restrict the access to specific resources within a service, so even if an action is allowed by the policy, it may not be allowed on all resources within that service. It's recommended to carefully review and test IAM policies before deploying them to ensure that they provide the necessary access to your users and resources while also maintaining security and compliance. <a name="f9XVC"></a>

## So when I use "NotAction", it means I can use anything which not declare in "NotAction" blocks

Yes, that is correct. When you use the NotAction element in an IAM policy statement, it means that any action that is not explicitly listed in the NotAction block is allowed. In other words, the policy statement denies only the actions that are specified in the NotAction block, and allows all other actions on the specified resources.
For example, in your original policy statement, the first statement denies all actions related to IAM, Organizations, and Account management, except for the actions related to creating, deleting, and listing service-linked roles, describing organizations, and listing regions. All other actions are allowed on any resource.
It's important to carefully consider the impact of using NotAction in an IAM policy statement, as it can grant broad access to resources and services that may not be necessary for the intended use case. You should always follow the principle of least privilege and grant only the permissions that are necessary for your users and resources to perform their intended actions. <a name="WLBvE"></a>

## What's difference between "NotAction" and "Effect:Deny"

Both NotAction and Effect: Deny are used to restrict access to AWS resources in IAM policies, but they work in different ways.
The NotAction element is used in an IAM policy statement to explicitly deny a list of actions while allowing all other actions. The NotAction element is used in combination with Effect: Allow to allow all actions except for the explicitly denied actions listed in NotAction. For example, in your original policy statement, the first statement denies all actions related to IAM, Organizations, and Account management, except for a few explicitly allowed actions, while allowing all other actions on any resource.
On the other hand, Effect: Deny is used to deny a specific action or a set of actions for a specific resource or set of resources. When Effect: Deny is used in a policy statement, it overrides any Effect: Allow statements for the same action on the same resource. For example, if you have an Effect: Allow statement that allows a certain action on a specific resource, and a Effect: Deny statement that denies the same action on the same resource, the Effect: Deny statement takes precedence and denies the action.
In general, it's recommended to use Effect: Deny sparingly and only when you need to explicitly deny access to specific actions or resources. Using NotAction or a more restrictive Effect: Allow statement is often a better approach to restricting access to AWS resources, as it is more clear and explicit in specifying the allowed actions and resources.
