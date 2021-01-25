#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---------------==========---------------
# Release_Version: 0.0.3a  *Early Version*
# Author: Eigeen
# Homepage: https://github.com/eigeen/bili-bonus
# ---------------==========---------------

import argparse
import re
import sys

from . import bili_reposts
from .globals import *


def init():
    # 建立data文件夹
    if os.path.exists(data_path_):
        pass
    else:
        os.mkdir(data_path_)

    # 清除旧数据库
    if os.path.exists(db_path_):
        try:
            os.remove(db_path_)
        except:
            print("Error: 清除旧数据库文件失败")
            sys.exit()


def exit_():
    print("\n*程序运行结束\n")
    sys.exit(os.system("pause"))


# URL中取ID
def parse_url(address):
    dyn_id = re.findall(r"(\d+)", address)
    if dyn_id == "":
        print("错误，未获取到id。\n\
        输入可能有误，请确认输入的是正确的链接或正确格式的动态id。")
        return ""
    else:
        return dyn_id[0]


def arg_parser():
    parser = argparse.ArgumentParser(description="获取B站动态转发和评论信息，用于动态抽奖等功能。")
    parser.add_argument("type", help="获取动态转发或评论 [repost/comment/both]")
    parser.add_argument("address", help="B站动态的链接或id")
    parser.add_argument("-o", "--output", help="导出到文件 <路径+文件名>.[json/xls]", default="")
    parser.add_argument("--debug", help="输出调试信息", default=None)
    args = parser.parse_args()
    return args


def main():
    init()
    address = input("请输入动态ID或完整的动态链接：")
    dyn_id = parse_url(address)
    scraper = bili_reposts.Scraper(dyn_id)
    scraper.scrape()
    print("*数据获取完毕")
    exporter = bili_reposts.Exporter()

    while True:
        is_save = input("是否导出数据？(Y/n):")
        if is_save in ['', 'y', 'Y']:
            exporter.to_excel(r".\data\export.xls")
            exporter.to_json(r".\data\export.json")
            print("*数据已导出到data目录下")
            break
        elif is_save in ['n', 'N']:
            break
        else:
            continue
    exit_()


if __name__ == "__main__":
    init()
    args = arg_parser()
    if args.type == "repost":
        scraper = bili_reposts.Scraper(args.address)
        scraper.scrape()
        exporter = bili_reposts.Exporter()

        splitted = args.output.split(".")
        suffix = splitted[-1]
        if suffix == "json":
            exporter.to_json(args.output)
        elif suffix == "xls":
            exporter.to_excel(args.output)
        else:
            print("Error: 文件保存路径格式错误！")
            print("-->" + args.output)
            sys.exit()
    elif args.type == "comment":
        pass
    elif args.type == "both":
        pass
    else:
        print(args.type, " 参数错误，应当为repost/comment/both")
