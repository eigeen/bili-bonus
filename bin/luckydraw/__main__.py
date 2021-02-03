#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import sqlite3

from bin.globals import db_path_, data_path_
from bin.luckydraw.standard import get_standard


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


def db_data(rawdata, salt):
    """
    :param rawdata:
    :param salt:
    """
    conn = sqlite3.connect(db_path_)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE DrawOrigin (
        id INTEGER NOT NULL,
        uid INTEGER NOT NULL,
        uname TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        raw TEXT
    )''')

    for n in range(len(rawdata)):
        cursor.execute('''INSERT INTO DrawOrigin VALUES 
        ("{}", "{}", "{}", "{}", "{}", "{}")'''.format(
            rawdata[n][0], rawdata[n][1], rawdata[n][2], rawdata[n][3], rawdata[n][4], str(rawdata[n]) + str(salt))
        )
    conn.commit()
    conn.close()


def db_hash(hash_list, delta_list):
    """
    :param hash_list: [(id, hash_hex, hash_int)]
    :param delta_list: [(id, delta_int)]
    """
    conn = sqlite3.connect(db_path_)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE DrawHash (
        id INTEGER,
        hash TEXT,
        hash_int TEXT,
        hash_delta TEXT
    )''')
    for n in range(len(hash_list)):
        cursor.execute('''INSERT INTO DrawHash VALUES 
        ("{}", "{}", "{}", "{}")'''.format(
            hash_list[n][0], hash_list[n][1], hash_list[n][2], delta_list[n][1]
        ))
    conn.commit()
    conn.close()


def calc_hash():
    """
    :return: [(id, hash_hex, hash_int)]
    """
    rawdata, basic_info = fetch_db()
    salt = basic_info[1]  # dyn_id
    db_data(rawdata, salt)
    hash_list = []
    for data in rawdata:
        tmp = str(data) + str(salt)
        hash = hashlib.md5(tmp.encode("utf-8"))
        hash_int = int(hash.hexdigest(), 16)
        hash_list.append((data[0], hash.hexdigest(), hash_int))
    return hash_list


def calc_delta(hash_list, standard):
    """
    :param hash_list: [(id, hash_hex, hash_int)]
    :param standard: -> int
    :return: [(id, delta_int)]
    """
    delta_list = []
    for h in hash_list:
        id = h[0]
        hash_int = h[2]
        delta = abs(hash_int - standard)
        delta_list.append((id, delta))
    return delta_list


def db_std(std):
    """
    :param std: (std, std_hash, std_hash_int)
    """
    conn = sqlite3.connect(db_path_)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE DrawStd (
        origin TEXT,
        std_hash TEXT,
        std_hash_int INTEGER
    )''')

    cursor.execute('''INSERT INTO DrawStd VALUES (
    "{}", "{}", "{}")'''.format(std[0], std[1], std[2]))
    conn.commit()
    conn.close()


def db_insert():
    standard = get_standard()
    db_std(standard)
    print("标准值:", standard[0], "\nMD5:", standard[1])
    hash_list = calc_hash()
    delta_list = calc_delta(hash_list, standard[2])
    db_hash(hash_list, delta_list)


def fetch_data():
    """
    :return: TABLE: DrawOrigin, DrawHash
    """
    conn = sqlite3.connect(db_path_)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM DrawOrigin''')
    origin = cursor.fetchall()
    cursor.execute('''SELECT * FROM DrawHash''')
    hash = cursor.fetchall()
    conn.close()
    return origin, hash


def combine_data(origin_data, hash_data):
    """
    :param origin_data: TABLE DrawOrigin
    :param hash_data: TABLE DrawHash
    :return: [((origin), (hash))]
    """
    data = []
    for n in range(len(origin_data)):
        data.append((origin_data[n], hash_data[n]))
    return data


def sort_data(data):
    """
    :param data: [((origin), (hash))]
    :return: sorted_data
    """
    data.sort(key=lambda x: int(x[1][3]))
    return data


def winners(sorted_data, count):
    """
    :param sorted_data:
    :param count: -> int
    :return: winners_list
    """
    winners_list = []
    for n in range(count):
        winners_list.append(sorted_data[n])
    return winners_list


def export_all(sorted_data):
    line = "No.{number}\n-编号: {id}\n-UID: {uid}\n-用户名: {uname}""\n-内容: {content}\n-发送时间: {timestamp}"\
           "\n-MD5: {hash}\n-MD5差异值(是否中奖的评判标准，越小越好): {hash_delta}\n\n"
    fp = open(data_path_ + r"\lucky_draw_export.txt", "w", encoding="utf-8")
    for n in range(len(sorted_data)):
        data_dict = {
            'number': n+1,
            'id': sorted_data[n][0][0],
            'uid': sorted_data[n][0][1],
            'uname': sorted_data[n][0][2],
            'content': sorted_data[n][0][3],
            'timestamp': sorted_data[n][0][4],
            'raw': sorted_data[n][0][5],
            'hash': sorted_data[n][1][1],
            'hash_delta': sorted_data[n][1][3],
        }
        fp.write(line.format(**data_dict))
    fp.close()


def roll():
    db_insert()
    origin_data, hash_data = fetch_data()
    data = combine_data(origin_data, hash_data)
    sorted_data = sort_data(data)
    export_all(sorted_data)

    count = int(input("\n请输入获奖用户数量："))
    winners_list = winners(sorted_data, count)
    return winners_list


# Debug
if __name__ == "__main__":
    print(roll())
