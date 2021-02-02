#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def hash_delta(hash_list, standard):
    delta_list = []
    for h in hash_list:
        id = h[0]
        hash = h[1]
        delta = abs(hash - standard)
        delta_list.append((id, delta))
    return delta_list


def compare(hash_list, standard):
    delta_list = hash_delta(hash_list, standard)
    delta_list.sort(key=lambda x: x[1])
    return delta_list
