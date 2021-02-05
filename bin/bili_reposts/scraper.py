#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import sqlite3
import time

import requests

from bin.globals import *


# 获取时间
def now_time():  # Type0 FullTime  Type1 InFileName
    t = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    return t


def get_offset(data_json):
    if 'offset' in data_json['data']:
        return data_json['data']['offset']
    else:
        return None


# 爬虫核心
class Scraper(object):
    def __init__(self, dyn_id):
        self.time = now_time()
        self.dynamic_id = dyn_id

    def start(self):
        count = 0
        offset = "1:0"
        conn = sqlite3.connect(db_path_)
        cursor = conn.cursor()
        dynamic_api = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail"
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4386.0 Safari/537.36 Edg/89.0.767.0',
            'd': '1',
            'origin': 'https://space.bilibili.com',
            'referer': 'https://space.bilibili.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        }

        # 首次数据获取
        param = {'dynamic_id': self.dynamic_id, 'offset': offset}
        data = requests.get(dynamic_api, headers=header, params=param, timeout=10)
        data_json = json.loads(data.text)
        total_num = data_json['data']['total']
        print("总转发人数：" + str(total_num))
        # up_name = data_json['data']['comments'][0]['detail']['desc']['origin'][
        #     'user_profile']['info']['uname']

        # 数据库初始化
        cursor.execute('''CREATE TABLE Reposts (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                uid INT NOT NULL,
                user_name TEXT NOT NULL,
                comment TEXT NOT NULL,
                timestamp INT NOT NULL
            )''')
        cursor.execute('''CREATE TABLE RepostHeaders (
                scrapytime TEXT NOT NULL,
                dynamic_id INT NOT NULL,
                total_count INT NOT NULL,
                raw TEXT NOT NULL
            )''')
        cursor.execute('''INSERT INTO RepostHeaders  
            VALUES ('{}', '{}', '{}', '{}')'''.format(
            self.time, int(self.dynamic_id), total_num, data.text))

        # 获取数据
        now_num = 0
        while now_num < total_num:
            param = {'dynamic_id': self.dynamic_id, 'offset': offset}
            data = requests.get(dynamic_api, headers=header, params=param, timeout=10)
            data_json = json.loads(data.text)

            for tmp_num in range(0, 20):  # 数据写入数据库
                if count < total_num:
                    count += 1
                    uid = data_json['data']['items'][tmp_num]['desc']['uid']
                    user_name = data_json['data']['items'][tmp_num]['desc']['user_profile']['info']['uname']
                    card = data_json['data']['items'][tmp_num]['card']
                    content = re.findall("\"content\\\": \\\"(.*?)\\\"", card)[0]  # "content\": \"内容\"
                    timestamp = data_json['data']['items'][tmp_num]['desc']['timestamp']
                    cursor.execute('''INSERT INTO Reposts 
                        VALUES(NULL, '{}', '{}', '{}', '{}')'''.format(uid, user_name, content, timestamp))
                else:
                    break
            offset = get_offset(data_json)
            if offset is None:
                break
            now_num += 20
            time.sleep(0.2)
        conn.commit()
        conn.close()
