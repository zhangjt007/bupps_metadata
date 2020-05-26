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


def msg_type_to_route_code(msg_type, pay_channel):
    """
    根据报文类型转换为汇路标识
    :param msg_type:
    :return:
    """
    payChannel = {
        "hvps": "0",
        "beps": "1",
        "ccms": "2",
        "saps": "3",
        "nets": "4",
        "pbcs": "5",
        "ibps": "6",
        "maps": "7"
    }
    return msg_type[0:4] + msg_type[5:8] + msg_type[13:].replace(".", "").replace("0", "")


msg_type_service_type_rel = {
    "hvps.111.001": "961001",
    "hvps.112.001": "961001",
    "hvps.141.001": "963001",
    "hvps.141.002": "963001",
    "beps.121.001": "961001",
    "beps.122.001": "961001",
    "beps.123.001": "961001",
    "beps.125.001": "961003",
    "beps.127.001": "962001",
    "beps.131.001": "962001",
    "beps.133.001": "962003",
    "ibps.101.001": "961001",
    "ibps.103.001": "962001",
}


def msg_type_to_service_type(msg_type):
    start_index = 963010
    if msg_type[:12] in msg_type_service_type_rel:
        service_type = msg_type_service_type_rel[msg_type[:12]]
    else:
        service_type = str(start_index + len(msg_type_service_type_rel))
        msg_type_service_type_rel[msg_type[:12]] = service_type
    return service_type


def get_ibps_msg_type(is_only_req=False, is_only_resp=False):
    """
    解析HVPS报文清单作为基准数据。
    :return:
    """
    ibps_msg_type = pd.read_excel(cnap_excel_file, sheet_name="IBPS报文清单", usecols=['报文编号', '报文名称', '报文方向'])
    ibps_msg_type['通道编码'] = "IBPS"
    if is_only_req:
        print("只获取往账报文")
        return ibps_msg_type[['报文编号', '报文名称', '通道编码']][
            ibps_msg_type['报文方向'].str.contains('参与者->|参与者<->|参与机构<->|参与机构->')]
    if is_only_resp:
        print("只获取来账报文")
        return ibps_msg_type[['报文编号', '报文名称', '通道编码']][ibps_msg_type['报文方向'].str.contains('参与者<|参与机构<|>参与者|>参与机构')]
    print("获取全量报文")
    ibps_msg_type['报文名称'] = ibps_msg_type['报文名称'].apply(lambda x: x.strip())
    return ibps_msg_type[['报文编号', '报文名称', '通道编码']]


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
    hvps_msg_type['报文名称'] = hvps_msg_type['报文名称'].apply(lambda x: x.strip())
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
    beps_msg_type['报文名称'] = beps_msg_type['报文名称'].apply(lambda x: x.lstrip())
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
    saps_msg_type['报文名称'] = saps_msg_type['报文名称'].apply(lambda x: x.strip())
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
    ccms_msg_type['报文名称'] = ccms_msg_type['报文名称'].apply(lambda x: x.strip())
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
    ibps_msg_type = get_ibps_msg_type(is_only_req, is_only_resp)
    concat_result = pd.concat([hvps_msg_type, beps_msg_type, saps_msg_type, ccms_msg_type, ibps_msg_type])
    return concat_result
