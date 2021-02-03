#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import sqlite3

from bin.luckydraw.standard import get_standard
from bin.globals import db_path_


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
    """
    :return: hash_list [((rawdata), hash_hex, hash_int)]
    """
    rawdata, basic_info = fetch_db()
    salt = basic_info[1]  # dyn_id
    hash_list = []
    for data in rawdata:
        tmp = str(data) + str(salt)
        hash = hashlib.md5(tmp.encode("utf-8"))
        hash_int = int(hash.hexdigest(), 16)
        hash_list.append((data, hash.hexdigest(), hash_int))
    return hash_list


def delta(hash_list, standard):
    delta_list = []
    for h in hash_list:
        id = h[0][0]
        hash_int = h[2]
        delta = abs(hash_int - standard)
        delta_list.append((id, delta))
    return delta_list


def hash_delta(hash_list, standard):
    delta_list = delta(hash_list, standard)
    return delta_list


def winners(sorted_list, count):
    winners_list = []
    for n in range(count):
        winners_list.append(sorted_list[n])
    return winners_list


def roll():
    """
    :return: [(((id, uid, uname, comment, timestamp), hash_hex, hash_int), (id, hash_delta))]
    """
    standard = get_standard()
    print("标准值:", standard[0], "\nMD5:", standard[1])
    hash_list = calc_hash()
    delta_list = hash_delta(hash_list, int(standard[1], 16))

    sorted_list = []  # [(((id, uid, uname, comment, timestamp), hash_hex, hash_int), (id, hash_delta))]
    for n in range(len(delta_list)):
        sorted_list.append((hash_list[n], delta_list[n]))
    sorted_list.sort(key=lambda x: x[1][1])

    count = int(input("请输入获奖用户数量："))
    winners_list = winners(sorted_list, count)
    return winners_list


# Debug
if __name__ == "__main__":
    roll()
