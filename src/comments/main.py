# -*- coding: utf-8 -*-
import json
import time

import requests

from src.globalvar import __temp_path__, headers
from src.reposts.user import User
from src.utils import nowtime


def start(dyn_id):
    basic_info = {}
    detail_api = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={}"
    comment_api = "https://api.bilibili.com/x/v2/reply"
    # comment_reply_api = "https://api.bilibili.com/x/v2/reply/reply"

    # params_reply = {
    #     'jsonp': 'jsonp',
    #     'pn': 1,  #
    #     'type': 17,
    #     'oid': self.dyn_id,
    #     'ps': 10,
    #     'root': comment_root
    # }

    # 获取动态oid
    detail_text = requests.get(detail_api.format(dyn_id), headers=headers, timeout=10).text
    detail_json = json.loads(detail_text)
    oid = detail_json['data']['card']['desc']['rid']  # data►card►desc►rid

    # 获取基础信息
    page = 1
    params_main = {
        'jsonp': 'jsonp',
        'pn': page,
        'type': 11,
        'oid': oid,
        'sort': 0  # 0按时间排序 2按热度排序
    }
    data_text = requests.get(comment_api, headers=headers, params=params_main, timeout=10).text
    data_json = json.loads(data_text)
    basic_info['count'] = data_json['data']['page']['count']
    basic_info['acount'] = data_json['data']['page']['acount']
    info = {
        'count': basic_info['count'],
        'acount': basic_info['acount'],
        'dyn_id': dyn_id,
        'time': nowtime()
    }

    # 评论获取
    users = []
    uidls = []
    now_count = 1
    while now_count < basic_info['count']:
        params_main['pn'] = page
        page += 1
        data_text = requests.get(comment_api, headers=headers, params=params_main, timeout=10).text
        data_json = json.loads(data_text)
        for now_count_tmp in range(len(data_json['data']['replies'])):
            uid = data_json['data']['replies'][now_count_tmp]['member']['mid']
            uname = data_json['data']['replies'][now_count_tmp]['member']['uname']
            content = data_json['data']['replies'][now_count_tmp]['content']['message']
            timestamp = data_json['data']['replies'][now_count_tmp]['ctime']

            # 包含重复用户剔除
            if uid in uidls:
                continue
            else:
                uidls.append(uid)
            exec("user_{:0>4d} = User(uid, uname, content, timestamp)".format(User.cid))
            exec("users.append(user_{:0>4d})".format(User.cid - 1))
            # users = [user_0001<CLass>, user_0002<Class>, ...]

            # 回复的获取功能由于与项目本身功能关系不大，故该项目暂不处理，未来可能置于独立项目中
            # # 获取评论下的回复
            # if data_json['data']['replies'][now_count_tmp]['replies'] is not None:
            #     reply_info['ctype'] = 1
            #     ...
            now_count += 1
            time.sleep(0.2)

    with open(__temp_path__ + r"\basic.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=4))

    for i in range(len(users)):  # 逆序id，使越早转发的用户的id越小
        users[i].id = len(users) - i
    users.sort(key=lambda x: x.id)
    return users
