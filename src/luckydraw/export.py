# -*- coding: utf-8 -*-
import json
import os

from src.globalvar import __data_path__, __homepage__, __version__, __temp_path__


def _fetchinfo():
    with open(__temp_path__ + r"\basic.json", "r", encoding="utf-8") as f:
        info = json.loads(f.read())
    return info['dyn_id'], info['time'], info['stdtxt'], info['stdhash']


def export_csv(sorted_users):
    try:
        dyn_id, time, stdtxt, stdhash = _fetchinfo()
        header = "开奖时间：{} ~ 动态ID: {},,,,,,,\n" \
                 "抽奖程序: {} ~ version: {},,,,,,,\n".format(time, dyn_id, __homepage__, __version__)
        standard = "\"标准值: {} ~ MD5: {}\",,,,,,,\n".format(stdtxt, stdhash)
        form_head = "序号, 编号, UID, 用户名, 内容, 发送时间, MD5(16进制), MD5差异值\n"
        line = "{number}, {id}, {uid}, {uname}, {content}, {timestamp}, {hash}, {hash_delta}\n"

        fp = open(__data_path__ + r"\full_export.csv", "w", encoding="utf-8-sig")
        fp.write(header + standard + form_head)
        for n in range(len(sorted_users)):
            data_dict = {
                'number': n + 1,
                'id': sorted_users[n].id,
                'uid': sorted_users[n].uid,
                'uname': sorted_users[n].uname,
                'content': sorted_users[n].content,
                'timestamp': sorted_users[n].timestamp,
                'hash': sorted_users[n].hashhex,
                'hash_delta': sorted_users[n].hashdelta,
            }
            fp.write(line.format(**data_dict))
    except PermissionError:
        print("!访问被拒绝!：写入csv文件失败，请关闭打开的文件后重试")
        os.system("pause")
    finally:
        fp.close()


def export_txt(sorted_users):
    try:
        dyn_id, time, stdtxt, stdhash = _fetchinfo()
        line = "No.{number}\n-编号: {id}\n-UID: {uid}\n-用户名: {uname}""\n-内容: {content}\n-发送时间: {timestamp}" \
               "\n-MD5: {hash}\n-MD5差异值(越小越好): {hash_delta}\n\n"
        fp = open(__data_path__ + r"\full_export.txt", "w", encoding="utf-8")

        fp.write("开奖时间：{}  ~ 动态ID: {}\n"
                 "抽奖程序: {} ~ version: {}\n"
                 "标准值: {} ~ MD5: {}".format(time, dyn_id, __homepage__, __version__, stdtxt, stdhash))
        # TODO: 补充标准值
        for n in range(len(sorted_users)):
            data_dict = {
                'number': n + 1,
                'id': sorted_users[n].id,
                'uid': sorted_users[n].uid,
                'uname': sorted_users[n].uname,
                'content': sorted_users[n].content,
                'timestamp': sorted_users[n].timestamp,
                'hash': sorted_users[n].hashhex,
                'hash_delta': sorted_users[n].hashdelta,
            }
            fp.write(line.format(**data_dict))
    except PermissionError:
        print("访问被拒绝：写入txt文件失败，请关闭打开的文件后重试")
    finally:
        fp.close()


def exportall(sorted_users):
    export_txt(sorted_users)
    export_csv(sorted_users)
