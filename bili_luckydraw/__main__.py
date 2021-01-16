#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from bili_luckydraw import bili_reposts


def arg_parser():
    parser = argparse.ArgumentParser(description="获取B站动态转发和评论信息，用于动态抽奖等功能。")
    parser.add_argument("type", help="获取动态转发或评论 [repost/comment/both]")
    parser.add_argument("address", help="B站动态的链接或id")
    parser.add_argument("-o", "--output", help="导出到文件 <路径+文件名>.[json/xls]", default="")
    parser.add_argument("--debug", help="输出调试信息", default=None)
    args = parser.parse_args()
    return args


def main():  # 功能：传参，其他模块入口
    args = arg_parser()
    if args.type == "repost":
        scraper = bili_reposts.Scraper(args.address)
        scraper.scrape()
        bili_reposts.exporter.export(args.output, scraper.users_info, scraper.up_name,
                                     scraper.dynamic_id, scraper.time)
    elif args.type == "comment":
        pass
    elif args.type == "both":
        pass
    else:
        print(args.type+" 参数错误，应当为repost/comment/both")


if __name__ == "__main__":
    scraper = bili_reposts.Scraper("477862261840413245")
    scraper.scrape()
    print(scraper.dynamic_id)
    print(scraper.up_name)
    print(scraper.users_info)
