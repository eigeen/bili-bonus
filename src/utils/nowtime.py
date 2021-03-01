# -*- coding: utf-8 -*-

# 获取时间
import time


def nowtime():
    t = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return t

