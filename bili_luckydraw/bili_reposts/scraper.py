#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import re
import requests
import json


# 获取时间，建议爬虫开始时获取
def now_time(type=0):  # Type0 FullTime  Type1 InFileName
    if type == 0:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    elif type == 1:
        t = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    else:
        t = None
    return t


# 生成顺序ID
def gen_id():
    i = 1
    yield i
    while True:
        i += 1
        yield i


# URL中取ID
def parse_url(dynamic_address):
    id = re.findall(r"(\d+)", dynamic_address)
    if id == "":
        print("错误，未获取到id。\n\
        输入可能有误，请确认输入的是正确的链接或正确格式的动态id。")
    else:
        return id[0]


# 爬虫核心
class Scraper(object):
    def __init__(self, address):
        self.time = now_time(type=1)
        self.dynamic_id = parse_url(address)
        self.up_name = ""
        self.users_info = []
        self.time = time
        self.gen_id = gen_id()

    def scrape(self):
        count = 0
        offset = 0
        total_num = -1
        tmp_user_info = {}
        users_info = []
        dynamic_api = "https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost"
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'd': '1',
            'origin': 'https://t.bilibili.com',
            'referer': 'https://t.bilibili.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        }

        self.time = now_time(type=1)

        while offset < total_num or total_num == -1:  # 数据获取
            try:
                param = {'dynamic_id': self.dynamic_id, 'offset': offset}
                response = requests.get(dynamic_api, headers=header, params=param, timeout=10)
                resp_json = json.loads(response.text)
                if total_num == -1:
                    total_num = resp_json['data']['total_count']
                    print("总转发人数：" + str(total_num))
                    self.up_name = resp_json['data']['comments'][0]['detail']['desc']['origin'][
                        'user_profile']['info']['uname']
            except Exception:
                print("出现错误，程序中断")
                print(response.text)
                return

            for tmp_num in range(0, 20):
                try:
                    if count < total_num:
                        count += 1
                        uid = resp_json['data']['comments'][tmp_num]['uid']
                        uname = resp_json['data']['comments'][tmp_num]['uname']
                        ucomment = resp_json['data']['comments'][tmp_num]['comment']
                        tmp_user_info["scrapeId"] = next(self.gen_id)
                        tmp_user_info["uid"] = uid
                        tmp_user_info["uname"] = uname
                        tmp_user_info["comment"] = ucomment
                        users_info.append(tmp_user_info.copy())
                    else:
                        break
                except Exception:
                    print("Error when collecting data.")
                    return
            offset += 20
        self.users_info = users_info
        print("数据获取完毕！")


# Debug
if __name__ == "__main__":
    dynamicAddress = "477862261840413245"
    biliprize = Scraper(dynamicAddress)
    biliprize.scrape()
