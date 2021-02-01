#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
from bin.globals import version_ as local_ver


def check_ver(local, remote):
    local = re.split("[.-]", local)
    remote = re.split("[.-]", remote)
    for l, r in zip(local, remote):
        if l > r:
            return True
        elif l < r:
            return False
    return None


if __name__ == "__main__":
    print("当前版本:", local_ver)
    readme_url = "https://cdn.jsdelivr.net/gh/eigeen/bili-bonus/README.md"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/89.0.4386.0 Safari/537.36 Edg/89.0.767.0'
               }
    readme_text = requests.get(readme_url, headers=headers, timeout=5).text
    remote_ver = re.findall(r"程序版本：(.*)", readme_text)[0]
    is_new_ver = check_ver(local_ver, remote_ver)
    if is_new_ver is True:
        print("最新版本:", remote_ver)
        print("您当前版本已经是最新版本。")
    elif is_new_ver is False:
        print("检测到新版本:", remote_ver)
    else:
        print("最新版本:", remote_ver)
        print("您当前版本已经是最新版本。")
    input("按回车键退出...")
