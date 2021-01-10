#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from BiliLuckyDog import BiliPrize

dynamicAddress = "477862261840413245"
main = BiliPrize()
main.run(dynamicAddress)

doSaveFile = input("是否保存获取到的文件？(j=Json,e=Excel,n=不保存):")
if doSaveFile == "j":
    main.SaveAsJson()
elif doSaveFile == "e":
    main.SaveAsExcel()
elif doSaveFile == "n":
    pass
