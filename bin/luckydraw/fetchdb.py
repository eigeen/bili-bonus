#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

from bin.globals import db_path_


def fetch_dynid():
    """
    :return: str: dyn_id
    """
    conn = sqlite3.connect(db_path_)
    cursor = conn.cursor()
    cursor.execute('''SELECT dynamic_id FROM RepostHeaders''')
    dyn_id = cursor.fetchone()
    conn.close()
    return dyn_id[0]


def fetch_std():
    """
    :return: tuple: std
    """
    conn = sqlite3.connect(db_path_)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM DrawStd''')
    std = cursor.fetchone()
    conn.close()
    return std


def fetch_draw():
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


def fetch_raw():
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
