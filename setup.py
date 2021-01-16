#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from bili_bonus import info

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bili-bonus",
    version=info.version_,
    keywords=["bilibili", "spider", "requests"],
    description=info.description_,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",

    url="https://github.com/eigeen/bili-bonus",
    author="Eigeen",
    author_email="dengyk2002@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    python_requires='>=3.6',
    requires=info.requires_,
    install_requires=info.requires_,

    entry_points={
        "console_scripts": ["bili-bonus=bili_bonus.__main__:main"]
    },
)
