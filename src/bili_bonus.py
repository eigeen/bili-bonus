# -*- coding: utf-8 -*-
import os
import re
import sys

from src import reposts, luckydraw
from src.globalvar import __data_path__, __temp_path__, __db_path__


def exit_():
    print("\n*程序运行结束\n")
    sys.exit(os.system("pause"))


def mkdir():
    # 建立data文件夹
    if not os.path.exists(__data_path__):
        os.mkdir(__data_path__)

    # 建立tmp文件夹
    if not os.path.exists(__temp_path__):
        os.mkdir(__temp_path__)

    # 清除旧数据库
    if os.path.exists(__db_path__):
        try:
            os.remove(__db_path__)
        except:
            print("Error: 清除旧数据库文件失败")
            input("按回车键退出...")
            exit_()


# URL中取ID
def parse_url(address):
    dyn_id = re.findall(r"(\d+)", address)
    if dyn_id == "":
        print("错误，未获取到id。\n\
        输入可能有误，请确认输入的是正确的链接或正确格式的动态id。")
        return ""
    else:
        return dyn_id[0]


# 入口
def main():
    mkdir()
    dyn_id = parse_url(input("请输入动态ID或完整的动态链接："))
    while True:
        # mode = input("1. 转发\n2. 评论（不包括评论下的回复）\n3. 同时转发和评论筛选\n请选择要获取的内容序号：")
        mode = "1"
        os.system("cls")
        if mode == "1":
            users = reposts.start(dyn_id)
            break

    luckydraw.start(users)
    print("数据已全部导出至data目录下，请查收~")
