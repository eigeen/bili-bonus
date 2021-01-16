# B站动态抽奖程序



## 介绍

Python版本：基于Python3.9开发，建议版本>=3.6

作者：我自己（@Eigeen）

调用的外部模块：

- requests

- xlwt

  

## 安装

`pip install bili-bonus`



## 功能

> 当前为v0.0.1版，抽奖部分还未完成，目前仅能保存数据。
>
> 数据保存后可以使用第三方工具抽奖，保证无黑箱（



当前可用功能：

- 获取普通动态的转发数据，包括转发用户UID，用户名，转发内容

- 数据导出为json

- 数据导出为xls表格

  

计划实现的功能：

- [ ] 获取评论数据
- [x] 重构项目，优化调用
- [ ] 数据导出到SQL
- [ ] 同时转发和评论的筛选
- [ ] 基于Hash的可溯源高级抽奖方法
- [ ] *断点续传

~~*断点续传功能由于本人能力限制，不一定实现~~



## 使用方法

### 安装：

`pip install bili-bonus`

### 使用：

`bili-bonus [可选参数] <获取转发/评论 repost/comment> <链接或ID>`

### 快速上手

获取动态[https://t.bilibili.com/477862261840413245?tab=1](https://t.bilibili.com/477862261840413245?tab=1)的所有转发数据，并导出为表格：

`bili-bonus repost https://t.bilibili.com/477862261840413245?tab=1 -o 20210106.xls`



### 参数

| 参数    | 用途和用法                | 是否必须                       |
| ------- | ------------------------- | ------------------------------ |
| type    | repost/comment/both       | 是                             |
| address | 链接或动态ID（纯数字）    | 是                             |
| -o      | -o [完整路径或完整文件名] | 非必须，缺少此参数无法导出文件 |



## 附录

PyPi页面：[bili-bonus · PyPI](https://pypi.org/project/bili-bonus/)

代码重构参考了项目[nICEnnnnnnnLee/LiveRecorder: you-live - A live recorder focus on China mainland livestream sites(A站/B站/斗鱼/快手) (github.com)](https://github.com/nICEnnnnnnnLee/LiveRecorder)