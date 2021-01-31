---
version: 0.0.3-210131-release
---

# B站动态抽奖程序

## 介绍

Python版本：基于Python3.9开发，建议版本>=3.6

程序版本：0.0.3

作者：我自己（@Eigeen）

调用的外部模块：

- requests

- xlwt

## 功能

> 当前为早期测试版，抽奖部分还未完成，目前仅能保存数据。
>
> 数据保存后可以使用第三方工具抽奖，保证无黑箱（



当前可用功能：

- 获取普通动态的转发数据，包括转发用户UID，用户名，转发内容

- 数据导出为json

- 数据导出为xls表格

计划实现的功能：

- [x] 获取评论数据
- [x] 重构项目，优化调用
- [x] 数据导出到SQL
- [ ] 同时转发和评论的筛选
- [ ] 基于Hash的可溯源高级抽奖方法



## 使用方法

### 安装外部模块

执行`pip install -r requirements.txt`

或运行Install_requirements.bat

### 使用

直接运行主目录下的`get_reposts.py`或`get_comments.py`，根据命令行提示输入参数

文件默认导出至data文件夹内

