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


def msg_type_to_route_code(msg_type):
    payChannel = {
        "hvps": "00",
        "beps": "01",
        "ccms": "02",
        "saps": "03",
        "nets": "04",
        "pbcs": "05",
        "ibps": "06"
    }
    return payChannel[msg_type[0:4]] + msg_type[4:].replace(".", "").replace("0", "")


def get_hvps_msg_type(is_only_req=False, is_only_resp=False):
    """
    解析HVPS报文清单作为基准数据。
    :return:
    """
    hvps_msg_type = pd.read_excel(cnap_excel_file, sheet_name="HVPS报文清单", usecols=['报文编号', '报文名称', '报文方向'])
    hvps_msg_type['通道编码'] = "HVPS"
    if is_only_req:
        print("只获取往账报文")
        return hvps_msg_type[['报文编号', '报文名称', '通道编码']][
            hvps_msg_type['报文方向'].str.contains('参与者->|参与者<->|参与机构<->|参与机构->')]
    if is_only_resp:
        print("只获取来账报文")
        return hvps_msg_type[['报文编号', '报文名称', '通道编码']][hvps_msg_type['报文方向'].str.contains('参与者<|参与机构<|>参与者|>参与机构')]
    print("获取全量报文")
    return hvps_msg_type[['报文编号', '报文名称', '通道编码']]


def get_beps_msg_type(is_only_req=False, is_only_resp=False):
    """
    解析BEPS报文清单作为基准数据。
    :return:
    """
    beps_msg_type = pd.read_excel(cnap_excel_file, sheet_name="BEPS报文清单", usecols=['报文编号', '报文名称', '报文方向'])
    beps_msg_type['通道编码'] = "BEPS"
    if is_only_req:
        print("只获取往账报文")
        return beps_msg_type[['报文编号', '报文名称', '通道编码']][
            beps_msg_type['报文方向'].str.contains('参与者->|参与者<->|参与机构<->|参与机构->')]
    if is_only_resp:
        print("只获取来账报文")
        return beps_msg_type[['报文编号', '报文名称', '通道编码']][beps_msg_type['报文方向'].str.contains('参与者<|参与机构<|>参与者|>参与机构')]
    print("获取全量报文")
    return beps_msg_type[['报文编号', '报文名称', '通道编码']]


def get_saps_msg_type(is_only_req=False, is_only_resp=False):
    """
    解析SAPS报文清单作为基准数据。
    :return:
    """
    saps_msg_type = pd.read_excel(cnap_excel_file, sheet_name="SAPS报文清单", usecols=['报文编号', '报文名称', '报文方向'])
    saps_msg_type['通道编码'] = "SAPS"
    if is_only_req:
        print("只获取往账报文")
        return saps_msg_type[['报文编号', '报文名称', '通道编码']][
            saps_msg_type['报文方向'].str.contains('参与者->|参与者<->|参与机构<->|参与机构->')]
    if is_only_resp:
        print("只获取来账报文")
        return saps_msg_type[['报文编号', '报文名称', '通道编码']][saps_msg_type['报文方向'].str.contains('参与者<|参与机构<|>参与者|>参与机构')]
    print("获取全量报文")
    return saps_msg_type[['报文编号', '报文名称', '通道编码']]


def get_ccms_msg_type(is_only_req=False, is_only_resp=False):
    """
    解析CCMS报文清单作为基准数据。
    :return:
    """
    ccms_msg_type = pd.read_excel(cnap_excel_file, sheet_name="CCMS报文清单", usecols=['报文编号', '报文名称', '报文方向'])
    ccms_msg_type['通道编码'] = "CCMS"
    if is_only_req:
        print("只获取往账报文")
        return ccms_msg_type[['报文编号', '报文名称', '通道编码']][
            ccms_msg_type['报文方向'].str.contains('参与者->|参与者<->|参与机构<->|参与机构->')]
    if is_only_resp:
        print("只获取来账报文")
        return ccms_msg_type[['报文编号', '报文名称', '通道编码']][ccms_msg_type['报文方向'].str.contains('参与者<|参与机构<|>参与者|>参与机构')]
    print("获取全量报文")
    return ccms_msg_type[['报文编号', '报文名称', '通道编码']]


def get_all_cnap_msg_type(is_only_req=False, is_only_resp=False):
    """
    解析HVPS报文清单、BEPS报文清单、SAPS报文清单、CCMS报文清单作为基准数据。
    :return:
    """
    hvps_msg_type = get_hvps_msg_type(is_only_req, is_only_resp)
    beps_msg_type = get_beps_msg_type(is_only_req, is_only_resp)
    saps_msg_type = get_saps_msg_type(is_only_req, is_only_resp)
    ccms_msg_type = get_ccms_msg_type(is_only_req, is_only_resp)
    concat_result = pd.concat([hvps_msg_type, beps_msg_type, saps_msg_type, ccms_msg_type])
    return concat_result
