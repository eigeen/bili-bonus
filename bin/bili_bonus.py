#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---------------==========---------------
# Author: Eigeen
# Homepage: https://github.com/eigeen/bili-bonus
# ---------------==========---------------

import os
import re
import sys

from . import bili_reposts
from . import luckydraw
from .globals import tmp_path_, db_path_, data_path_


def init():
    # 建立data文件夹
    if not os.path.exists(data_path_):
        os.mkdir(data_path_)

    # 建立tmp文件夹
    if not os.path.exists(tmp_path_):
        os.mkdir(tmp_path_)

    # 清除旧数据库
    if os.path.exists(db_path_):
        try:
            os.remove(db_path_)
        except:
            print("Error: 清除旧数据库文件失败")
            input("按回车键退出...")
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


# def arg_parser():
#     parser = argparse.ArgumentParser(description="获取B站动态转发和评论信息，用于动态抽奖等功能。")
#     parser.add_argument("type", help="获取动态转发或评论 [repost/comment/both]")
#     parser.add_argument("address", help="B站动态的链接或id")
#     parser.add_argument("-o", "--output", help="导出到文件 <路径+文件名>.[json/xls]", default="")
#     parser.add_argument("--debug", help="输出调试信息", default=None)
#     args = parser.parse_args()
#     return args


# # 快速执行入口
# def get_reposts():
#     init()
#     address = input("请输入动态ID或完整的动态链接：")
#     dyn_id = parse_url(address)
#     scraper = bili_reposts.Scraper(dyn_id)
#     scraper.start()
#     print("*数据获取完毕")
#     exporter = bili_reposts.Exporter()
#
#     while True:
#         is_save = input("是否导出数据？(Y/n):")
#         if is_save in ['', 'y', 'Y']:
#             exporter.to_excel(r".\data\export.xls")
#             exporter.to_json(r".\data\export.json")
#             print("*数据已导出到data目录下")
#             break
#         elif is_save in ['n', 'N']:
#             break
#         else:
#             continue
#     exit_()


def build_data(winner_list):
    tmp = []
    for n in range(len(winner_list)):
        winner_dict = {
            'id': winner_list[n][0][0],
            'uid': winner_list[n][0][1],
            'uname': winner_list[n][0][2],
            'content': winner_list[n][0][3],
            'timestamp': winner_list[n][0][4],
            'raw': winner_list[n][0][5],
            'hash': winner_list[n][1][1],
            'hash_delta': winner_list[n][1][3],
        }
        tmp.append(winner_dict)
    return tmp


def print_winner(winner_data):
    for n in range(len(winner_data)):
        print("*" * 40)
        print("")
        print("No." + str(n + 1))
        print("-编号:", winner_data[n]['id'])
        print("-UID:", winner_data[n]['uid'])
        print("-用户名:", winner_data[n]['uname'])
        print("-内容:", winner_data[n]['content'])
        print("-发送时间:", winner_data[n]['timestamp'])
        print("-MD5:", winner_data[n]['hash'])
        print("-MD5差异值(是否中奖的评判标准，越小越好):\n", winner_data[n]['hash_delta'])
        print("")


def repost(dyn_id):
    scraper = bili_reposts.Scraper(dyn_id)
    print("*正在获取数据...")
    scraper.start()
    print("*数据获取完毕，处理中...")
    winner_list = luckydraw.roll()
    winner_data = build_data(winner_list)
    print_winner(winner_data)


def main():
    init()
    dyn_id = parse_url(input("请输入动态ID或完整的动态链接："))
    while True:
        mode = input("1. 转发\n2. 评论（不包括评论下的回复）\n3. 同时转发和评论筛选\n请选择要获取的内容序号：")
        os.system("cls")
        if mode == "1":
            repost(dyn_id)
            break
        # TODO: 待开发
        # elif mode == "2":
        #     scraper = bili_comments.Scraper(dyn_id)
        #     print("*正在获取数据...")
        #     scraper.start()
        #     print("*数据获取完毕，处理中...")
        #     luckydraw()
        #
        # elif mode == "3":
        #     scraper_r = bili_reposts.Scraper(dyn_id)
        #     scraper_c = bili_comments.Scraper(dyn_id)
        #     print("*正在获取数据...")
        #     scraper_r.start()
        #     scraper_c.start()
        #     print("*数据获取完毕，处理中...")
        #     luckydraw()
        #
        # else:
        #     os.system("cls")
        #     continue


if __name__ == "__main__":
    init()
    args = arg_parser()
    if args.type == "repost":
        scraper = bili_reposts.Scraper(args.address)
        scraper.start()
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
