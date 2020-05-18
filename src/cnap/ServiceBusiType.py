#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : Route.py
@Time    : 2020/5/10 16:29
@Author  : Zhang JinTao
@Version : 1.0.0
@Contact : zhangjt007@gmail.com
@License : (C)Copyright 2020-2021, SOLO
@Des     : 获取汇路信息
"""
import xml.etree.ElementTree as et

from src.cnap.CommonTools import *


def generate_route_info(data):
    """
    根据数据集生成BUPPS_MSG_TYPE_SYS_STATUS表SQL文件
    :param data:
    :return:
    """
    data['PART_MSGTYPE'] = data['MSGTYPE'].apply(lambda x: x[:12])
    data.drop_duplicates(['SYSCODE', 'PART_MSGTYPE'], keep="first", inplace=True)
    all_cnap_msg_type = get_all_cnap_msg_type(is_only_req=True)
    all_cnap_msg_type['PART_MSGTYPE'] = all_cnap_msg_type['报文编号'].apply(lambda x: str(x)[:12])
    result = pd.merge(data, all_cnap_msg_type, on='PART_MSGTYPE', how='outer')
    result.to_excel("../../resource/cnap/BUPPS_ROUTE_INFO.xls")
    out_file = "../../resource/cnap/BUPPS_ROUTE_INFO.sql"
    with open(out_file, "w", encoding="UTF-8") as f:
        for index, row in result.iterrows():
            route_code = msg_type_to_route_code(str(row['报文编号']), str(row['SYSCODE']))
            sql = "INSERT INTO BUPPS_ROUTE_INFO (\"ROUTE_CODE\", \"ROUTE_NAME\", \"PAY_CHANNEL\", \"PAY_CHANNEL_NAME\", \"CHANNEL_TRANSCODE\", \"MSG_TYPE\", \"BUSI_MODE\", \"ROUTE_CHECK_FLAG\", \"ROUTE_PKG_FLAG\", \"SWITCH_FLAG\", \"EFFECTIVE_TIME1\", \"EFFECTIVE_TIME2\", \"EFFECTIVE_TIME3\", \"MAX_AMT\", \"MIN_AMT\", \"TIME_EFFECT_FLAG\", \"FEE_RULE\", \"CUSTOMER_FLAG\", \"CASH_FLAG\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\", \"PRODUCT_RESERVE1\", \"PRODUCT_RESERVE2\", \"PRODUCT_RESERVE3\", \"RUNNING_STATUS\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '000', '1', '0', '0', '000001-092122', '092123-140000', '140001-235959', '0', '0', '2', '1', '1', '1', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'), NULL, NULL, NULL, NULL);".format(
                route_code, row['报文名称'], row['SYSCODE'], row['SYSCODE'], "", row['报文编号'])
            f.writelines(sql)
            f.writelines("\n")


def generate_service_type(data):
    """
    根据数据集生成BUPPS_SERVICE_TYPE_INFO表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_SERVICE_TYPE_INFO.sql"
    with open(out_file, "w", encoding="UTF-8") as f:
        for index, row in data.iterrows():
            sql = "INSERT INTO BUPPS_SERVICE_TYPE_INFO (\"SERVICE_TYPE_CODE\", \"SERVICE_TYPE_NAME\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\", \"EFFECT_FLAG\") VALUES ('{}', '{}', to_char(sysdate,'yyyymmddhh24miss'), to_char(sysdate,'yyyymmddhh24miss'), '1');".format(
                row['服务类型'], row['服务类型名称'])
            f.writelines(sql)
            f.writelines("\n")


def generate_service_busi_rel(data):
    """
    根据数据集生成BUPPS_SERVICE_BUSI_TYPE_REL表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_SERVICE_BUSI_TYPE_REL.sql"
    with open(out_file, "w", encoding="UTF-8") as f:
        for index, row in data.iterrows():
            data_id = str(row['服务类型']) + str(row['BIZTYPE']) + str(row['BIZDTLTYPEPURPOSE'])
            sql = "INSERT INTO BUPPS_SERVICE_BUSI_TYPE_REL(\"DATA_ID\", \"BUSI_TYPE_CODE\", \"BUSI_KIND_CODE\", \"BUSI_TYPE_NAME\", \"BUSI_KIND_NAME\", \"SERVICE_TYPE_CODE\", \"SERVICE_TYPE_NAME\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\") VALUES ('{}', '{}', '{}', '', '', '{}', '{}', to_char(sysdate,'yyyymmddhh24miss'), to_char(sysdate,'yyyymmddhh24miss');".format(
                data_id, row['BIZTYPE'], row['BIZDTLTYPEPURPOSE'], row['服务类型'], row['服务类型名称'])
            f.writelines(sql)
            f.writelines("\n")


if __name__ == '__main__':
    source = "../../resource/CCMSZDT0307.XML"
    xtree = et.parse(source)
    xroot = xtree.getroot()
    df_cols = ['SYSCODE', 'MSGTYPE', 'BIZTYPE', 'BIZDTLTYPEPURPOSE']
    rows = []
    for node in xroot:
        syscode = node.find("SYSCODE").text if node is not None else None
        msgtype = node.find("MSGTYPE").text if node is not None else None
        biztype = node.find("BIZTYPE").text if node is not None else None
        bizdtltypepurpose = node.find("BIZDTLTYPEPURPOSE").text if node is not None else None
        rows.append({"SYSCODE": syscode,
                     "MSGTYPE": msgtype,
                     "BIZTYPE": biztype,
                     "BIZDTLTYPEPURPOSE": bizdtltypepurpose})
    out_df = pd.DataFrame(rows, columns=df_cols)
    generate_route_info(out_df.copy(deep=True))
