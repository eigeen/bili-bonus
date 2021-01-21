#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---------------==========---------------
# Release_Version: 0.0.2  *Early Version*
# Author: Eigeen
# Homepage: https://github.com/eigeen/bili-bonus
# ---------------==========---------------

import argparse
import sys
import bili_reposts


def arg_parser():
    parser = argparse.ArgumentParser(description="获取B站动态转发和评论信息，用于动态抽奖等功能。")
    parser.add_argument("type", help="获取动态转发或评论 [repost/comment/both]")
    parser.add_argument("address", help="B站动态的链接或id")
    parser.add_argument("-o", "--output", help="导出到文件 <路径+文件名>.[json/xls]", default="")
    parser.add_argument("--debug", help="输出调试信息", default=None)
    args = parser.parse_args()
    return args


def main():
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
        print(args.type + " 参数错误，应当为repost/comment/both")


if __name__ == "__main__":
    address = input("请输入动态ID或完整的动态链接：")
    scraper = bili_reposts.Scraper(address)
    scraper.scrape()
    print("*数据获取完毕")
    exporter = bili_reposts.Exporter()

    while True:
        isSave = input("是否导出数据？(Y/n):")
        if isSave in ['', 'y', 'Y']:
            exporter.to_excel(r".\data\export.xls")
            exporter.to_json(r".\data\export.json")
            print("*数据已导出到data目录下")
            sys.exit()
        elif isSave in ['n', 'N']:
            sys.exit()
        else:
            continue
