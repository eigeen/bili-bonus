# -*- coding: utf-8 -*-
import os

__homepage__ = "https://github.com/eigeen/bili-bonus"
__version__ = "0.1.0-210222-a1"

__bin_path__ = os.path.split(os.path.realpath(__file__))[0]
__data_path__ = __bin_path__ + r"\..\data"
__temp_path__ = __data_path__ + r"\temp"
__db_path__ = __temp_path__ + r"\bili_bonus_tmp.db"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4386.0 Safari/537.36 Edg/89.0.767.0'
}
