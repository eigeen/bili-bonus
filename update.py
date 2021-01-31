#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

readme_url = "https://cdn.jsdelivr.net/gh/eigeen/bili-bonus/README.md"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/89.0.4386.0 Safari/537.36 Edg/89.0.767.0'
           }
readme_text = requests.get(readme_url, headers=headers, timeout=5).text
remote_version = re.findall(r"version: (.*?)", readme_text)[0]
print(remote_version)