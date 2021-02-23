# -*- coding: utf-8 -*-
import hashlib
import json

from src.globalvar import __temp_path__

# def _attrs(user):
#     attrs_full = dir(user)
#     attrs = filter(lambda x: x[:2] != "__", attrs_full)
#     return list(attrs)
from src.luckydraw.export import exportall
from src.luckydraw.getstd import getstd


def _fetch_data(user):
    data = user.__dict__
    return str(data)


def _calchash(user):
    with open(__temp_path__ + r"\basic.json", "r", encoding="utf-8") as f:
        info = json.loads(f.read())
    salt = str(info['dyn_id'])
    string = _fetch_data(user) + salt
    uhash = hashlib.md5(string.encode("utf-8"))
    uhash_hex = uhash.hexdigest()
    return uhash_hex


def gethash(users):
    for u in users:
        u.hashhex = _calchash(u)


def editdistance(str1, str2):
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)
    return matrix[len(str1)][len(str2)]


def integerdiff(hashhex, stdhash):
    return abs(int(hashhex, 16) - int(stdhash, 16))


def compare(users, stdhash, mode):
    if mode == "editdistance":
        for u in users:
            u.hashdelta = editdistance(u.hashhex, stdhash)
    elif mode == "integerdiff":
        for u in users:
            u.hashdelta = integerdiff(u.hashhex, stdhash)


def sortbydelta(users):
    sorted_users = sorted(users, key=lambda x: x.hashdelta)
    return sorted_users


def selectusers(sorted_users):
    pass
    # TODO:


def start(users, mode="integerdiff"):
    gethash(users)
    stdtxt, stdhash = getstd()
    compare(users, stdhash, mode)
    sorted_users = sortbydelta(users)
    exportall(sorted_users)
    selectusers(sorted_users)
