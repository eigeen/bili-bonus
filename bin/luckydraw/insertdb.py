#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

from bin.globals import db_path_


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
