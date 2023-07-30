---
title: Route 53
url: https://www.yuque.com/stevenyin/liv/who43538y15dd25q
---

<a name="HwLWn"></a>

## CNAME vs Alias

<a name="cHKg0"></a>

### CNAME:

- Points a hostname to any other hostname. (app.mydomain.com => blabla.anything.com)
- ONLY FOR NON ROOT DOMAIN <a name="U3Di5"></a>

### Alias:

- Points a hostname to an AWS Resource (app.mydomain.com => blabla.amazonaws.com)

<a name="HS6Gq"></a>

## Routing Policies

<a name="CGXB1"></a>

### Simple

<a name="YnGit"></a>

### Weighted

<a name="WPkmP"></a>

### Latency-based

<a name="BNDYy"></a>

## Routing Policies - Failover (Active-Passive)

<a name="VOsJ8"></a>

## Health Checks

<a name="h73UY"></a>

### Monitor an Endpoint

<a name="fq50d"></a>

### Calculated Health Checks

Combine the results of multiple Health Checks into a single Health Check <a name="YjqKv"></a>

### Private Hosted Zones

- Route 53 health checkers are outside the VPC
- They can't access private endpoints (private VPC or on-premises resource)
- You can create a CloudWatch Metric and associate a CloudWatch Alarm, then create a Health Check that checks the alarm itself.
