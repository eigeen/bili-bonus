#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib

from bin.luckydraw.standard import get_standard
from .export import export_all
from .fetchdb import fetch_draw, fetch_raw
from .insertdb import db_data, db_std, db_hash


def calc_hash():
    """
    :return: [(id, hash_hex, hash_int)]
    """
    rawdata, basic_info = fetch_raw()
    salt = basic_info[1]  # dyn_id
    db_data(rawdata, salt)
    hash_list = []
    for data in rawdata:
        tmp = str(data) + str(salt)
        hash = hashlib.md5(tmp.encode("utf-8"))
        hash_int = int(hash.hexdigest(), 16)
        hash_list.append((data[0], hash.hexdigest(), hash_int))
    return hash_list


def calc_delta(hash_list, standard):
    """
    :param hash_list: [(id, hash_hex, hash_int)]
    :param standard: -> int
    :return: [(id, delta_int)]
    """
    delta_list = []
    for h in hash_list:
        id = h[0]
        hash_int = h[2]
        delta = abs(hash_int - standard)
        delta_list.append((id, delta))
    return delta_list


def db_insert():
    standard = get_standard()
    db_std(standard)
    print("标准值:", standard[0], "\nMD5:", standard[1])
    hash_list = calc_hash()
    delta_list = calc_delta(hash_list, standard[2])
    db_hash(hash_list, delta_list)


def combine_data(origin_data, hash_data):
    """
    :param origin_data: TABLE DrawOrigin
    :param hash_data: TABLE DrawHash
    :return: [((origin), (hash))]
    """
    data = []
    for n in range(len(origin_data)):
        data.append((origin_data[n], hash_data[n]))
    return data


def sort_data(data):
    """
    :param data: [((origin), (hash))]
    :return: sorted_data
    """
    data.sort(key=lambda x: int(x[1][3]))
    return data


def winners(sorted_data, count):
    """
    :param sorted_data:
    :param count: -> int
    :return: winners_list
    """
    winners_list = []
    for n in range(count):
        winners_list.append(sorted_data[n])
    return winners_list


def roll():
    db_insert()
    origin_data, hash_data = fetch_draw()
    data = combine_data(origin_data, hash_data)
    sorted_data = sort_data(data)
    export_all(sorted_data)

    count = int(input("\n请输入获奖用户数量："))
    winners_list = winners(sorted_data, count)
    return winners_list


# Debug
if __name__ == "__main__":
    print(roll())
