#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3
import time

import xlsxwriter as xw

from bin.globals import db_path_


class Exporter(object):
    def __init__(self):
        self.conn = sqlite3.connect(db_path_)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT * FROM CommentHeaders''')
        self.users_data = []

    def get_content(self):
        self.cursor.execute('''SELECT * FROM Comments''')
        if not self.users_data:
            for row in self.cursor.fetchall():
                user_data_tmp = {'id': row[0], 'uid': row[1], 'user_name': row[2], 'comment': row[3]}
                self.users_data.append(user_data_tmp.copy())

    def to_json(self, file_path=""):
        if not file_path:
            file_path = time.strftime("%y%m%d%H%M%S", time.localtime()) + ".json"
        Exporter.get_content(self)
        with open(file_path, 'w', encoding="utf-8") as fp:
            fp.write(json.dumps(self.users_data, ensure_ascii=False, sort_keys=True, indent=4))

    def to_excel(self, file_path=""):
        if not file_path:
            file_path = time.strftime("%y%m%d%H%M%S", time.localtime()) + ".xlsx"
        workbook = xw.Workbook(file_path)
        sheet = workbook.add_worksheet("BiliBonusOutput")
        num_style = workbook.add_format({'num_format': '0'})

        sheet.write(0, 0, "编号")
        sheet.write(0, 1, "UID")
        sheet.write(0, 2, "用户名")
        sheet.write(0, 3, "转发内容")
        for n in range(len(self.users_data)):
            self.cursor.execute('''SELECT * FROM Reposts WHERE id = "{}"'''.format(n + 1))
            user_data = self.cursor.fetchone()
            sheet.write(n + 1, 0, user_data[0])
            sheet.write(n + 1, 1, user_data[1], num_style)
            sheet.write(n + 1, 2, user_data[2])
            sheet.write(n + 1, 3, user_data[3])
        workbook.close()
