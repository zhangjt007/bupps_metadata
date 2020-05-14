#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : CommonTools.py
@Time    : 2020/5/10 16:29
@Author  : Zhang JinTao
@Version : 1.0.0
@Contact : zhangjt007@gmail.com
@License : (C)Copyright 2020-2021, SOLO
@Des     : None
"""
import pandas as pd

cnap_excel_file = "../../resource/人行二代基础数据.xls"


def get_all_cnap_msg_type():
    """
    解析HVPS报文清单、BEPS报文清单、SAPS报文清单、CCMS报文清单作为基准数据。
    :return:
    """
    hvps_msg_type = pd.read_excel(cnap_excel_file, sheet_name="HVPS报文清单", usecols=['报文编号', '报文名称'])
    hvps_msg_type['通道编码'] = "HVPS"
    beps_msg_type = pd.read_excel(cnap_excel_file, sheet_name="BEPS报文清单", usecols=['报文编号', '报文名称'])
    beps_msg_type['通道编码'] = "BEPS"
    saps_msg_type = pd.read_excel(cnap_excel_file, sheet_name="SAPS报文清单", usecols=['报文编号', '报文名称'])
    saps_msg_type['通道编码'] = "SAPS"
    ccms_msg_type = pd.read_excel(cnap_excel_file, sheet_name="CCMS报文清单", usecols=['报文编号', '报文名称'])
    ccms_msg_type['通道编码'] = "CCMS"
    return pd.concat([hvps_msg_type, beps_msg_type, saps_msg_type, ccms_msg_type])
