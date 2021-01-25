#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3

import xlwt

from ..globals import *


class Exporter(object):
    def __init__(self):
        self.conn = sqlite3.connect(db_path_)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT * FROM RepostHeaders''')
        self.users_data = []
        self.user_data_tmp = {}

        header = self.cursor.fetchone()
        self.time = header[0]
        self.up_name = header[1]
        self.dynamic_id = header[2]
        self.total_num = header[3]

    def get_content(self):
        self.users_data = []
        self.user_data_tmp = {}
        self.cursor.execute('''SELECT * FROM Reposts''')
        for row in self.cursor.fetchall():
            self.user_data_tmp['id'] = row[0]
            self.user_data_tmp['uid'] = row[1]
            self.user_data_tmp['user_name'] = row[2]
            self.user_data_tmp['comment'] = row[3]
            self.users_data.append(self.user_data_tmp.copy())

    def to_json(self, file_path):
        # file_name = up_name + "_" + dynamic_id[-6:] + "_" + time + ".json"]
        Exporter.get_content(self)
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(self.users_data, ensure_ascii=False, sort_keys=True, indent=4))

    def to_excel(self, file_path):
        # file_name = up_name + "_" + dynamic_id[-6:] + "_" + time + ".xls"
        workbook = xlwt.Workbook(encoding="utf-8")
        sheet = workbook.add_sheet(self.up_name)
        style1 = xlwt.XFStyle()
        style1.num_format_str = '0'
        sheet.write(0, 0, "编号")
        sheet.write(0, 1, "UID")
        sheet.write(0, 2, "用户名")
        sheet.write(0, 3, "转发内容")
        for n in range(self.total_num):
            self.cursor.execute('''SELECT * FROM Reposts WHERE id = "{}"'''.format(n + 1))
            user_data = self.cursor.fetchone()
            sheet.write(n + 1, 0, user_data[0])
            sheet.write(n + 1, 1, user_data[1], style=style1)
            sheet.write(n + 1, 2, user_data[2])
            sheet.write(n + 1, 3, user_data[3])
        workbook.save(file_path)
