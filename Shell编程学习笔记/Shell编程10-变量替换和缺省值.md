---
title: Shell编程10-变量替换和缺省值
url: https://www.yuque.com/stevenyin/liv/ggl9zx
---

<a name="bSPXF"></a>

## 替换规则

| 语法 | 解释 |
| --- | --- |
| ${变量名#匹配规则} | 从变量开头进行规则匹配，将符合条件的最短数据删除 |
| ${变量名##匹配规则} | 从变量开头进行规则匹配，将符合条件的最长数据删除 |
| ${变量名%匹配规则} | 从变量尾部进行规则匹配，将符合条件的最短数据删除 |
| ${变量名%%匹配规则} | 从变量尾部进行规则匹配，将符合条件的最长数据删除 |
| ${变量名/旧字符串/新字符串} | 变量内容符合旧字符串的规则，则第一个匹配的旧字符串会被新字符串取代 |
| ${变量名//旧字符串/新字符串} | 变量内容符合旧字符串的规则，则所有匹配的旧字符串会被新字符串取代 |

```shell
➜  ~ ACTIVE_PROFILE=prod,dev,local,common
➜  ~ echo $ACTIVE_PROFILE
prod,dev,local,common
➜  ~ echo ${ACTIVE_PROFILE#*dev,} # 只要匹配到含有"dev,"这个字符，就会删除包括这个字符在内的前面所有内容
local,common
➜  ~ echo ${ACTIVE_PROFILE#*,} # 从头开始寻找","字符，删除满足条件的最短字符串
dev,local,common
➜  ~ echo ${ACTIVE_PROFILE##*,} # 从头开始寻找","字符，删除满足条件的最长字符串
common
➜  ~ echo ${ACTIVE_PROFILE%%,*} # 只要匹配到含有","这个字符，就会删除包括这个字符在内的所有内容
prod
➜  ~ echo ${ACTIVE_PROFILE%,*} # 只要匹配到含有","这个字符，就会删除包括这个字符在内的所有内容
prod,dev,local
```

| 变量配置方式 | str没有配置 | str为空字符串 | str已配置且非空 |
| --- | --- | --- | --- |
| `var=${str-expr}` | `var=expr` | `var=` | `var=$str` |
| `var=${str:-expr}` | `var=expr` | `var=expr` | `var=$str` |
| `var=${str+expr}` | `var=` | `var=expr` | `var=expr` |
| `var=${str:+expr}` | `var=` | `var=` | `var=expr` |
| `var=${str=expr}` | `var=expr` | `var=` | `var=$str` |
| `var=${str:=expr}` | `var=expr` | `var=expr` | `var=$str` |
