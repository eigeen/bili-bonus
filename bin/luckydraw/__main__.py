#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .calc_hash import calc_hash
from .standard import get_standard
from .compare import compare


def roll():
    standard = get_standard()
    hash_list = calc_hash()
    sorted_data = compare(hash_list, standard)
    return sorted_data
