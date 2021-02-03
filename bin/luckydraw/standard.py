#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import hashlib
import traceback

import requests
from lxml import etree


def _getdate():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    one_week_before_yesterday = yesterday - datetime.timedelta(days=6)
    return today, yesterday, one_week_before_yesterday


def get_standard():
    """
    :return: [(std_raw, std_hash_hex, std_hash_int)]
    """
    keyword = "python"
    today, startday, endday = _getdate()
    url = "https://index.chinaz.com/{}/{}~{}".format(keyword, startday, endday)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4386.0 Safari/537.36 Edg/89.0.767.0'
    }
    try:
        page = requests.get(url, headers=headers, timeout=10)
        tree = etree.HTML(page.text)
        index = tree.xpath('//ul[@class="zs-nodule bor-b1s tin6 clearfix"]'
                           '/li[@class="nod-li col-blue02 w12-1"]/text()')[0]
        std_txt = str(today) + "_" + keyword + "_" + index
        hash = hashlib.md5(std_txt.encode("utf-8"))
        std_hash = hash.hexdigest()
        standard = (std_txt, std_hash, int(std_hash, 16))
        return standard
    except Exception:
        traceback.print_exc()
        input("按回车键退出...")

