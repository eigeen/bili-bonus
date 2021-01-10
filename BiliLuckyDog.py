#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script_version: 1.0.0

import requests
import json
import re


class BiliPrize(object):
    def __init__(self):
        self.genId = BiliPrize.gen_scrapeid(self)

    def run(self, dynamicAddress):
        BiliPrize.get_dynamicid(self, dynamicAddress)
        BiliPrize.get_contents(self)

    def get_contents(self):
        offset = 0
        totalNum = -1
        tmpNum = 0
        userInfo = {}
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
                    print("总人数：" + str(totalNum))
            except Exception:
                print("出现错误:")
                break

            while tmpNum < 20:
                try:
                    uid = self.resp_json['data']['comments'][tmpNum]['uid']
                    uname = self.resp_json['data']['comments'][tmpNum]['uname']
                    ucomment = self.resp_json['data']['comments'][tmpNum]['comment']
                    userInfo['uid'] = uid
                    userInfo['uname'] = uname
                    userInfo['comment'] = ucomment
                    userInfo['scrapeId'] = next(self.genId)
                    self.usersInfo.append(str(userInfo))
                    tmpNum += 1
                except IndexError:
                    break
            offset += 20
            tmpNum = 0
        print("获取完毕！")

    def get_dynamicid(self, dynamicAddress):
        id = re.findall(r"(\d+)", dynamicAddress)
        if id == None:
            print("错误，未获取到id。\n\
            输入可能有误，请确认输入的是正确的链接或正确格式的动态id。")
        else:
            print("获取到动态id：" + id[0])
            self.dynamicId = id

    def save_file(self, asJson=True):
        if asJson == True:
            fileName = str(self.dynamicId) + "_" + ".json"
            with open(fileName, 'w', encoding="utf-8") as f:
                f.write(str(self.usersInfo))

    def gen_scrapeid(self):
        i = 1
        yield i
        while True:
            i += 1
            yield i


if __name__ == "__main__":
    # dynamicAddress = input("输入动态id或动态链接：")
    dynamicAddress = "477862261840413245"
    main = BiliPrize()
    main.run(dynamicAddress)
    main.save_file()
