---
title: ASG(Auto Scaling Group)
url: https://www.yuque.com/stevenyin/liv/soo8c6gbz8mrmh4e
---

<a name="n8UDy"></a>

## Goal:

1. Scale out (add EC2 instances) to match an increased load
2. Scale in (remove EC2 instances) to match an decreased load
3. Ensure we have a minimum and a maximum number of EC2 instances running
4. Automatically register new instances to a load balancer
5. Re-create an EC2 instance in case a previous one is terminated (ex: if unhealthy)

Auto Scaling Group + Application Load Balancer + Target Group + EC2 Instance
