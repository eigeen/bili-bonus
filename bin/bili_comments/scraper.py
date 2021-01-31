#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sqlite3
import time

import requests

from globals import *


# 获取时间
def now_time():
    t = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    return t


class Scraper(object):
    def __init__(self, dyn_id):
        self.dyn_id = dyn_id
        self.time = now_time()
        pass

    def start(self):
        basic_info = {}
        comment_info = {}
        comment_root = ""
        now_count = 1
        page = 1
        dyn_comment_api = "https://api.bilibili.com/x/v2/reply"
        # comment_reply_api = "https://api.bilibili.com/x/v2/reply/reply"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4386.0 Safari/537.36 Edg/89.0.767.0'
        }
        params_main = {
            'jsonp': 'jsonp',
            'pn': page,
            'type': 17,
            'oid': self.dyn_id,
            'sort': 0
        }
        # params_reply = {
        #     'jsonp': 'jsonp',
        #     'pn': 1,  #
        #     'type': 17,
        #     'oid': self.dyn_id,
        #     'ps': 10,
        #     'root': comment_root
        # }

        # 获取基础信息
        data_text = requests.get(dyn_comment_api, headers=headers, params=params_main, timeout=10).text
        data_json = json.loads(data_text)
        basic_info['count'] = data_json['data']['page']['count']
        basic_info['acount'] = data_json['data']['page']['acount']

        # 数据库初始化
        conn = sqlite3.connect(db_path_)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE Comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            type INT NOT NULL,
            uid INT NOT NULL,
            user_name TEXT NOT NULL,
            comment TEXT NOT NULL,
            timestamp INT NOT NULL
        )''')
        cursor.execute('''CREATE TABLE CommentHeaders (
            time INT NOT NULL,
            dynamic_id INT NOT NULL,
            comment_count INT NOT NULL,
            total_count INT NOT NULL
        )''')
        cursor.execute('''INSERT INTO CommentHeaders 
            VALUES ('{}', '{}', '{}', '{}')'''.format(
            self.time, self.dyn_id, basic_info['count'], basic_info['acount']))

        # 评论获取
        while now_count < basic_info['count']:
            data_text = requests.get(dyn_comment_api, headers=headers, params=params_main, timeout=10).text
            data_json = json.loads(data_text)
            page += 1
            if basic_info['count'] - now_count >= 20:
                count_in_page = 20
            else:
                count_in_page = basic_info['count'] - now_count + 1

            for now_count_tmp in range(count_in_page):
                comment_info['mid'] = data_json['data']['replies'][now_count_tmp]['member']['mid']
                comment_info['uname'] = data_json['data']['replies'][now_count_tmp]['member']['uname']
                comment_info['message'] = data_json['data']['replies'][now_count_tmp]['content']['message']
                comment_info['ctime'] = data_json['data']['replies'][now_count_tmp]['ctime']
                cursor.execute('''INSERT INTO Comments
                    VALUES (NULL, '0', '{mid}', '{uname}', '{message}', '{ctime}')'''.format(**comment_info))

                # 回复的获取功能由于与项目本身功能关系不大，故该项目暂不处理，未来可能置于独立项目中
                # # 获取评论下的回复
                # if data_json['data']['replies'][now_count_tmp]['replies'] is not None:
                #     reply_info['ctype'] = 1
                #     ...
                now_count += 1
        conn.commit()
        conn.close()


# Debug
if __name__ == "__main__":
    import os
    import sys

    if os.path.exists(db_path_):
        try:
            os.remove(db_path_)
        except:
            print("Error: 清除旧数据库文件失败")
            sys.exit()
    scraper = Scraper("483065202402169510")
    scraper.start()
