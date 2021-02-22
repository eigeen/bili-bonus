# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import traceback

import requests
from lxml import etree

from src.globalvar import headers, __temp_path__


def _getdate():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    one_week_before_yesterday = yesterday - datetime.timedelta(days=6)
    return today, yesterday, one_week_before_yesterday


def exportstd(stdtxt, stdhash):
    with open(__temp_path__ + r"\basic.json", "r", encoding="utf-8") as f:
        origin = json.loads(f.read())
    with open(__temp_path__ + r"\basic.json", "w", encoding="utf-8") as f:
        f.write(json.dumps({**origin, **{"stdtxt": stdtxt, "stdhash": stdhash}}))


def getstd():
    keyword = "python"
    today, endday, startday = _getdate()
    url = "https://index.chinaz.com/{}/{}~{}".format(keyword, startday, endday)
    try:
        page = requests.get(url, headers=headers, timeout=10)
        tree = etree.HTML(page.text)
        index = tree.xpath('//ul[@class="zs-nodule bor-b1s tin6 clearfix"]'
                           '/li[@class="nod-li col-blue02 w12-1"]/text()')[0]
        stdtxt = str(today) + "_" + keyword + "_" + index
        hash = hashlib.md5(stdtxt.encode("utf-8"))
        stdhash = hash.hexdigest()
        exportstd(stdtxt, stdhash)
        return stdtxt, stdhash
    except:
        traceback.print_exc()
        input("按回车键退出...")
