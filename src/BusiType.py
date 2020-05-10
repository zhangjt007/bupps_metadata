#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : BusiType.py
@Time    : 2020/5/10 16:29
@Author  : Zhang JinTao
@Version : 1.0.0
@Contact : zhangjt007@gmail.com
@License : (C)Copyright 2020-2021, SOLO
@Des     : None
"""

import pandas as pd

sourceFile = '../resource/人行二代基础数据.xls'
busiType = pd.read_excel(sourceFile, sheet_name="业务类型编码")
busiKind = pd.read_excel(sourceFile, sheet_name="业务种类编码")
busiTypeAndKindRel = pd.read_excel(sourceFile, sheet_name="业务类型与业务种类对照表")
msgTypeAndBusiTypeRel = pd.read_excel(sourceFile, sheet_name="报文与业务类型对照表")
# 根据条件业务类型号不为4位,获取业务类型好和业务类型名称
busiType = busiType[['业务类型号', '业务类型名称']][busiType['业务类型号'].map(len) == 4]
# 删除业务类型号重复的数据
# keep="first"表示保留第一次出现的数据
# inplace=True表示直接在原来的DataFrame上删除重复项，而默认值False表示生成一个副本
busiType.drop_duplicates('业务类型号', keep="first", inplace=True)
# 对编码列不足5位的补零
busiKind['编码'] = busiKind['编码'].apply(lambda x: str(x).zfill(5))
