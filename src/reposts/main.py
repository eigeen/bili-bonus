# -*- coding: utf-8 -*-
import json
import re
import time

import requests

from src.reposts.user import RepostUser
from src.globalvar import __temp_path__, headers


# 获取时间
def now_time():
    t = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return t


def _get_offset(data_json):
    if 'offset' in data_json['data']:
        return data_json['data']['offset']
    else:
        return None


def start(dyn_id):
    dynamic_api = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail"
    info = {
        "time": now_time(),
        "dyn_id": dyn_id
    }

    # 首次数据获取
    offset = "1:0"
    param = {'dynamic_id': dyn_id, 'offset': offset}
    data = requests.get(dynamic_api, headers=headers, params=param, timeout=10)
    data_json = json.loads(data.text)
    total_num = data_json['data']['total']
    info['total'] = total_num
    print("总转发人数：" + str(total_num))

    # 获取全部数据
    now_num = 0
    count = 0
    users = []
    while now_num < total_num:  # 循环获取页面
        param = {'dynamic_id': dyn_id, 'offset': offset}
        data = requests.get(dynamic_api, headers=headers, params=param, timeout=10)
        data_json = json.loads(data.text)
        for i in range(0, 20):  # 获取单页的所有用户（最多20条）
            if count < total_num:
                count += 1
                uid = data_json['data']['items'][i]['desc']['uid']
                uname = data_json['data']['items'][i]['desc']['user_profile']['info']['uname']
                card = data_json['data']['items'][i]['card']
                re_card = re.compile("\"content\\\": \\\"(.*?)\\\"")
                content = re_card.findall(card)[0]  # "content\": \"内容\"
                timestamp = data_json['data']['items'][i]['desc']['timestamp']

                exec("user_{:0>4d} = RepostUser(uid, uname, content, timestamp)".format(RepostUser.cid))
                exec("users.append(user_{:0>4d})".format(RepostUser.cid - 1))
            else:  # 最后一页数量少于20时
                break
        offset = _get_offset(data_json)
        if offset is None:
            break
        now_num += 20
        time.sleep(0.2)

    with open(__temp_path__ + r"\basic.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=4))

    for i in range(len(users)):  # 逆序id，使越早转发的用户的id越小
        users[i].id = len(users) - i
    users.sort(key=lambda x: x.id)
    return users
