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

from src.cnap.CommonTools import *


def generate_route_info(data):
    """
    根据数据集生成BUPPS_MSG_TYPE_SYS_STATUS表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_ROUTE_INFO.sql"
    with open(out_file, "w", encoding="UTF-8") as f:
        for index, row in data.iterrows():
            sql = "INSERT INTO BUPPS_ROUTE_INFO (\"ROUTE_CODE\", \"ROUTE_NAME\", \"PAY_CHANNEL\", \"PAY_CHANNEL_NAME\", \"CHANNEL_TRANSCODE\", \"MSG_TYPE\", \"BUSI_MODE\", \"ROUTE_CHECK_FLAG\", \"ROUTE_PKG_FLAG\", \"SWITCH_FLAG\", \"EFFECTIVE_TIME1\", \"EFFECTIVE_TIME2\", \"EFFECTIVE_TIME3\", \"MAX_AMT\", \"MIN_AMT\", \"TIME_EFFECT_FLAG\", \"FEE_RULE\", \"CUSTOMER_FLAG\", \"CASH_FLAG\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\", \"PRODUCT_RESERVE1\", \"PRODUCT_RESERVE2\", \"PRODUCT_RESERVE3\", \"RUNNING_STATUS\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '000', '1', '0', '0', '000001-092122', '092123-140000', '140001-235959', '0', '0', '2', '1', '1', '1', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'), NULL, NULL, NULL, NULL);".format(
                row['汇路编号'], row['报文名称'], row['通道编码'], row['通道编码'], "", row['报文编号'])
            f.writelines(sql)
            f.writelines("\n")


def generate_route_service_rel(data):
    """
    根据数据集生成BUPPS_ROUTE_SERVICE_REL表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_ROUTE_SERVICE_REL.sql"
    with open(out_file, "w", encoding="UTF-8") as f:
        for index, row in data.iterrows():
            data_id = row['汇路编号'] + row['服务类型']
            sql = "INSERT INTO BUPPS_ROUTE_SERVICE_REL (\"DATA_ID\", \"ROUTE_CODE\", \"ROUTE_NAME\", \"PAY_CHANNEL\", \"SERVICE_TYPE_CODE\", \"SERVICE_TYPE_NAME\", \"PRIORITY\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '1', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'));".format(
                data_id, row['汇路编号'], row['报文名称'].rstrip(), row['通道编码'].upper(), row['服务类型'], row['报文名称'])
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
            sql = "INSERT INTO BUPPS_SERVICE_BUSI_TYPE_REL(\"DATA_ID\", \"BUSI_TYPE_CODE\", \"BUSI_KIND_CODE\", \"BUSI_TYPE_NAME\", \"BUSI_KIND_NAME\", \"SERVICE_TYPE_CODE\", \"SERVICE_TYPE_NAME\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', to_char(sysdate,'yyyymmddhh24miss'), to_char(sysdate,'yyyymmddhh24miss');".format(
                row['服务类型'], row['服务类型名称'])
            f.writelines(sql)
            f.writelines("\n")


def merge_busi_type(type1, type2):
    if pd.isna(type1):
        return type2
    else:
        return type1


if __name__ == '__main__':
    rel = get_all_cnap_msg_type(is_only_req=True)
    rel['汇路编号'] = rel.apply(lambda row: msg_type_to_route_code(row['报文编号'], row['通道编码']), axis=1)
    rel['服务类型'] = rel['报文编号'].apply(lambda x: msg_type_to_service_type(x))
    rel['服务类型名称'] = rel['报文名称'].apply(lambda x: x.replace('报文', ''))
    generate_route_info(rel)
    print("生成BUPPS_ROUTE_INFO表")
    generate_route_service_rel(rel)
    print("生成BUPPS_ROUTE_SERVICE_REL表")
    rel.to_excel("../../resource/cnap/BUPPS_ROUTE_SERVICE_REL.xls", sheet_name="BUPPS_ROUTE_SERVICE_REL")

    service_type = rel.drop_duplicates('服务类型', keep="first", inplace=False)
    generate_service_type(service_type)
    print("生成BUPPS_SERVICE_TYPE_INFO表")
