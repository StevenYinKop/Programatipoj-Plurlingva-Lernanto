---
title: ELB(Elastic Load Balancer)
url: https://www.yuque.com/stevenyin/liv/abhaxc533q238qa4
---

<a name="QwlTS"></a>

## Application Load Balancer

- EC2 instances (can be managed by an Auto Scaling Group) – HTTP
- ECS tasks (managed by ECS itself) – HTTP
- Lambda functions – HTTP request is translated into a JSON event
- IP Addresses – must be private IPs

ALB can route to multiple target groups&#x20;
Health checks are at the target group level

1. Security Group
2. Target Group
3. EC2 Instances <a name="iwfzg"></a>

## Network Load Balancer

- Network load balancers (Layer 4) allow to:
  - Forward TCP & UDP traffic to your instances
  - Handle millions of request per seconds
  - Less latency ~ 100ms (vs 400ms for ALB) <a name="p7Ery"></a>

## Gateway Load Balancer

<a name="ObnH8"></a>

## Sticky Session

<a name="MS41B"></a>

## Cross Zone Load Balancer

<a name="CFPjy"></a>

## SSL Certificates

<a name="IviFH"></a>

## Connection Draining
