#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from bili_luckydraw import info

with open("README.md", "r",encoding="utf-8") as fh:
     long_description = fh.read()

setup(
    name = "bili-luckydraw",
    version = info._version_,
    keywords = ["bilibili", "spider", "requests"],
    description = info._description_,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "GPL-3.0 License",

    url = "https://github.com/eigeen/bili-dynamic-luckydraw",
    author = "Eigeen",
    author_email = "dengyk2002@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    python_requires='>=3.6',
    requires = info._requires_,
    install_requires = info._requires_,

    entry_points = {
        "console_scripts": ["bili-luckydraw=bili_luckydraw.__main__:main"]
    },
)
