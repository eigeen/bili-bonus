#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import sqlite3

from bin.globals import db_path_


def hex2int(hash):
    return int(hash, 16)


def _calc(rawdata, basic_info):
    salt = str(basic_info[0])  # 动态发布时间
    hash_list = []
    for data in rawdata:
        tmp = str(data) + salt
        hash = hashlib.md5(tmp.encode("utf-8"))
        hash_int = hex2int(hash.hexdigest())
        hash_list.append((data[0], hash_int))
    return hash_list


def fetch_db():
    conn = sqlite3.connect(db_path_)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Reposts GROUP BY user_name HAVING count(uid) < 2''')
    group1 = cursor.fetchall()
    cursor.execute('''SELECT * FROM Reposts GROUP BY user_name HAVING count(uid) >= 2''')
    group2 = cursor.fetchall()
    rawdata = group1 + group2
    rawdata.sort(key=lambda x: x[0])
    cursor.execute('''SELECT * FROM RepostHeaders''')
    basic_info = cursor.fetchone()
    conn.close()
    return rawdata, basic_info


def calc_hash():
    rawdata, basic_info = fetch_db()
    hash_list = _calc(rawdata, basic_info)
    return hash_list
