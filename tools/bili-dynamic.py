#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---------------==========---------------
# Release_Version: 0.0.1  *Early Version*
# Author: Eigeen
# Homepage: https://github.com/eigeen/bili-dynamic
# ---------------==========---------------

import json
import os
import sqlite3
import sys

import requests

sqlite_db_path = r".\data\bili_dynamic_tmp.db"


def del_db():
    global sqlite_db_path
    if os.path.exists(sqlite_db_path):
        try:
            os.remove(sqlite_db_path)
        except:
            print("Error: 清除旧数据库文件失败")
            sys.exit()


def mkdir_data():
    if os.path.exists(r".\data"):
        pass
    else:
        os.mkdir(r".\data")


def print_data(data):
    for t_dyn in data:
        print("")
        print("=" * 40)
        print("ID: " + str(t_dyn[0]))
        print("动态ID: " + str(t_dyn[1]))
        print("时间戳: " + str(t_dyn[2]))
        print("阅读: " + str(t_dyn[3]))
        print("转发: " + str(t_dyn[4]))
        print("评论: " + str(t_dyn[5]))
        print("点赞: " + str(t_dyn[6]))
        if t_dyn[7] == 1:
            print("*这是一条置顶动态")


def scrape(up_uid):
    global sqlite_db_path
    dynamic_info = {}
    dynamic_api = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/89.0.4386.0 Safari/537.36 Edg/89.0.767.0',
        'dnt': '1',
        'origin': 'https://space.bilibili.com',
        'referer': 'https://space.bilibili.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    basic_param = {'host_uid': up_uid, 'offset_dynamic_id': '0', 'need_top': '1'}

    data_raw = requests.get(dynamic_api, headers=header, params=basic_param, timeout=10)
    data_json = json.loads(data_raw.text)

    # 数据库初始化
    mkdir_data()
    del_db()
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE Dynamic (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        dynamic_id INT NOT NULL,
        timestamp INT NOT NULL,
        view INT NOT NULL,
        repost INT NOT NULL,
        comment TEXT NOT NULL,
        like INT NOT NULL,
        is_space_top INT NOT NULL)''')

    # 保存raw.json
    with open(r".\data\raw.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_json, ensure_ascii=False, sort_keys=True, indent=4))

    # 写入数据库
    for n in range(len(data_json['data']['cards'])):
        dynamic_info['dynamic_id'] = data_json['data']['cards'][n]['desc']['dynamic_id']
        dynamic_info['timestamp'] = data_json['data']['cards'][n]['desc']['timestamp']
        dynamic_info['view'] = data_json['data']['cards'][n]['desc']['view']
        dynamic_info['repost'] = data_json['data']['cards'][n]['desc']['repost']
        dynamic_info['like'] = data_json['data']['cards'][n]['desc']['like']
        dynamic_info['is_space_top'] = data_json['data']['cards'][n]['extra']['is_space_top']
        card_str = data_json['data']['cards'][n]['card']
        card_json = json.loads(card_str)
        if 'comment' in data_json['data']['cards'][n]['desc']:
            dynamic_info['comment'] = data_json['data']['cards'][n]['desc']['comment']
        else:
            dynamic_info['comment'] = -1

        cursor.execute('''INSERT INTO Dynamic VALUES 
            (NULL, '{dynamic_id}', '{timestamp}', '{view}', '{repost}', 
            '{comment}', '{like}', '{is_space_top}')'''.format(**dynamic_info))
    conn.commit()
    conn.close()


def export():
    global sqlite_db_path

    # 读数据库
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Dynamic''')
    data = cursor.fetchall()

    print_data(data)


if __name__ == "__main__":
    up_uid = input("请输入up主的UID：")
    scrape(str(up_uid))
    export()
    print("\n按Enter键退出...", end="")
    input()
