#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bin.globals import data_path_, version_
from .fetchdb import fetch_std


def export_csv(sorted_data, std):
    time = std[0][:10]
    header = "开奖时间：{} ~ 程序版本：{},,,,,,,\n".format(time, version_)
    form_head = "序号, 编号, UID, 用户名, 内容, 发送时间, MD5(16进制), MD5差异值\n"
    line = "{number}, {id}, {uid}, {uname}, {content}, {timestamp}, {hash}, {hash_delta}\n"
    fp = open(data_path_ + r"\full_export.csv", "w", encoding="utf-8-sig")
    for n in range(len(sorted_data)):
        data_dict = {
            'number': n + 1,
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


def export_txt(sorted_data, std):
    line = "No.{number}\n-编号: {id}\n-UID: {uid}\n-用户名: {uname}""\n-内容: {content}\n-发送时间: {timestamp}" \
           "\n-MD5: {hash}\n-MD5差异值(是否中奖的评判标准，越小越好): {hash_delta}\n\n"
    fp = open(data_path_ + r"\full_export.txt", "w", encoding="utf-8")

    time = std[0][:10]
    fp.write("开奖时间：{} ~ 程序版本：{}\n".format(time, version_))
    for n in range(len(sorted_data)):
        data_dict = {
            'number': n + 1,
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


def export_all(sorted_data):
    std = fetch_std()
    export_txt(sorted_data, std)
    export_csv(sorted_data, std)
