#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script_version: 1.0.0

import requests
import json
import re
import xlwt
import time


class BiliPrize(object):
    def __init__(self):
        self.genId = BiliPrize.GenId(self)

    def run(self, dynamicAddress):
        BiliPrize.GetDynamicid(self, dynamicAddress)
        BiliPrize.GetContents(self)

    def GetContents(self):
        offset = 0
        totalNum = -1
        tmpNum = 0
        tmpUserInfo = {}
        self.usersInfo = []

        dynamicAPI = "https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost"

        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'd': '1',
            'origin': 'https://t.bilibili.com',
            'referer': 'https://t.bilibili.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        }

        while offset < totalNum or totalNum == -1:  #数据获取
            try:
                param = {'dynamic_id': self.dynamicId, 'offset': offset}
                response = requests.get(dynamicAPI, headers=header, params=param, timeout=10)
                self.resp_text = response.text
                self.resp_json = json.loads(response.text)
                if totalNum == -1:
                    totalNum = self.resp_json['data']['total_count']
                    print("总转发人数：" + str(totalNum))
                    self.upName = self.resp_json['data']['comments'][0]['detail']['desc']['origin']\
                        ['user_profile']['info']['uname']
            except Exception:
                print("出现错误，程序中断")
                break

            for tmpNum in range(0, 20):
                try:
                    uid = self.resp_json['data']['comments'][tmpNum]['uid']
                    uname = self.resp_json['data']['comments'][tmpNum]['uname']
                    ucomment = self.resp_json['data']['comments'][tmpNum]['comment']
                    tmpUserInfo["scrapeId"] = next(self.genId)
                    tmpUserInfo["uid"] = uid
                    tmpUserInfo["uname"] = uname
                    tmpUserInfo["comment"] = ucomment
                    self.usersInfo.append(tmpUserInfo.copy())
                except Exception:
                    return
            offset += 20
        print("数据获取完毕！")

    def GetLuckyDog(self):
        pass

    def GetDynamicid(self, dynamicAddress):
        id = re.findall(r"(\d+)", dynamicAddress)
        if id == None:
            print("错误，未获取到id。\n\
            输入可能有误，请确认输入的是正确的链接或正确格式的动态id。")
        else:
            print("获取到动态id：" + id[0])
            self.dynamicId = id[0]

    def SaveAsJson(self):
        fileName = self.upName + "_" + self.dynamicId[-6:] + ".json"
        try:
            with open(fileName, 'w', encoding="utf-8") as f:
                f.write(json.dumps(self.usersInfo, ensure_ascii=False))
            print("成功导出json文件。")
        except Exception:
            print("输出文件失败！")

    def SaveAsExcel(self):
        tmpUserInfo = {}
        fileName = self.upName + "_" + self.dynamicId[-6:] + ".xls"
        workbook = xlwt.Workbook(encoding="utf-8")
        sheet = workbook.add_sheet(self.upName)
        style1 = xlwt.XFStyle()
        style1.num_format_str = '0'
        sheet.write(0, 0, "编号")
        sheet.write(0, 1, "UID")
        sheet.write(0, 2, "用户名")
        sheet.write(0, 3, "转发内容")

        for i in range(len(self.usersInfo)):
            tmpUserInfo['scrapeId'] = self.usersInfo[i]['scrapeId']
            tmpUserInfo["uid"] = self.usersInfo[i]['uid']
            tmpUserInfo["uname"] = self.usersInfo[i]['uname']
            tmpUserInfo["comment"] = self.usersInfo[i]['comment']
            sheet.write(i + 1, 0, tmpUserInfo['scrapeId'])
            sheet.write(i + 1, 1, tmpUserInfo['uid'], style=style1)
            sheet.write(i + 1, 2, tmpUserInfo['uname'])
            sheet.write(i + 1, 3, tmpUserInfo['comment'])
        workbook.save(fileName)

    def GenId(self):
        i = 1
        yield i
        while True:
            i += 1
            yield i

    def NowTime(self):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return t


if __name__ == "__main__":
    dynamicAddress = input("输入动态id或动态链接：")
