# B站动态抽奖程序
[TOC]

## 介绍

版本：Python3

作者：我自己（@Eigeen）

调用的外部模块：

- requests

- xlwt

  

## 功能

> 当前为v1.0.0版，抽奖部分还未完成，目前仅能保存数据。
>
> 数据保存后可以使用第三方工具抽奖，保证无黑箱（



当前可用功能：

- 获取普通动态的转发数据，包括转发用户UID，用户名，转发内容

- 数据导出为json

- 数据导出为xls表格

  

计划实现的功能：

- 获取评论数据
- 数据导出到SQL
- 完善模块，优化调用
- *断点续传

~~*断点续传功能由于本人能力限制，不一定实现~~

## 调用

主程序封装于BiliPrize.py内

```python
from BiliPrize import BiliPrize

dynamicAddress = ""             # 输入动态ID或动态链接
choujiang = BiliPrize()
choujiang.run(dynamicAddress)
main.SaveAsJson()               # 保存为.json到程序同一目录下
main.SaveAsExcel()              # 保存为.xls到程序同一目录下
```

