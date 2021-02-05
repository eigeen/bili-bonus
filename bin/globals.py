#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

homepage_ = "https://github.com/eigeen/bili-bonus"
version_ = "0.0.5-210205-release"
bin_path_ = os.path.split(os.path.realpath(__file__))[0]
data_path_ = bin_path_ + r"\..\data"

tmp_path_ = data_path_ + r"\temp"

db_path_ = tmp_path_ + r"\bili_bonus_tmp.db"
