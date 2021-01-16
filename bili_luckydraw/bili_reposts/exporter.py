#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import xlwt


def parse_path(file_path, users_info, up_name, dynamic_id, time):
    splitted = file_path.split(".")
    suffix = splitted[-1]
    if suffix == "json":
        to_json(file_path, users_info, up_name, dynamic_id, time)
    elif suffix == "xls":
        to_excel(file_path, users_info, up_name, dynamic_id, time)
    else:
        print("Error: 文件保存路径格式错误！")
        print("-->"+file_path)


def to_json(file_path, users_info, up_name, dynamic_id, time):
    # file_name = up_name + "_" + dynamic_id[-6:] + "_" + time + ".json"
    file_name = file_path
    try:
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(json.dumps(users_info, ensure_ascii=False))
        print("成功导出json文件。")
    except Exception:
        print("输出文件失败！")


def to_excel(file_path, users_info, up_name, dynamic_id, time):
    tmp_user_info = {}
    # file_name = up_name + "_" + dynamic_id[-6:] + "_" + time + ".xls"
    file_name = file_path
    workbook = xlwt.Workbook(encoding="utf-8")
    sheet = workbook.add_sheet(up_name)
    style1 = xlwt.XFStyle()
    style1.num_format_str = '0'
    sheet.write(0, 0, "编号")
    sheet.write(0, 1, "UID")
    sheet.write(0, 2, "用户名")
    sheet.write(0, 3, "转发内容")

    for i in range(len(users_info)):
        tmp_user_info['scrapeId'] = users_info[i]['scrapeId']
        tmp_user_info["uid"] = users_info[i]['uid']
        tmp_user_info["uname"] = users_info[i]['uname']
        tmp_user_info["comment"] = users_info[i]['comment']
        sheet.write(i + 1, 0, tmp_user_info['scrapeId'])
        sheet.write(i + 1, 1, tmp_user_info['uid'], style=style1)
        sheet.write(i + 1, 2, tmp_user_info['uname'])
        sheet.write(i + 1, 3, tmp_user_info['comment'])
    workbook.save(file_name)


# 入口
def export(file_path, users_info, up_name, dynamic_id, time):
    parse_path(file_path, users_info, up_name, dynamic_id, time)
