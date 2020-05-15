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


def generate_msg_type_sys_status(data):
    """
    根据数据集生成BUPPS_MSG_TYPE_SYS_STATUS表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_ROUTE_INFO.sql"
    with open(out_file, "w", encoding="UTF-8") as f:
        for index, row in data.iterrows():
            print(row)
            route_code = msg_type_to_route_code(str(row['报文编号']))
            sql = "INSERT INTO BUPPS_ROUTE_INFO (\"ROUTE_CODE\", \"ROUTE_NAME\", \"PAY_CHANNEL\", \"PAY_CHANNEL_NAME\", \"CHANNEL_TRANSCODE\", \"MSG_TYPE\", \"BUSI_MODE\", \"ROUTE_CHECK_FLAG\", \"ROUTE_PKG_FLAG\", \"SWITCH_FLAG\", \"EFFECTIVE_TIME1\", \"EFFECTIVE_TIME2\", \"EFFECTIVE_TIME3\", \"MAX_AMT\", \"MIN_AMT\", \"TIME_EFFECT_FLAG\", \"FEE_RULE\", \"CUSTOMER_FLAG\", \"CASH_FLAG\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\", \"PRODUCT_RESERVE1\", \"PRODUCT_RESERVE2\", \"PRODUCT_RESERVE3\", \"RUNNING_STATUS\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '000', '1', '0', '0', '000001-092122', '092123-140000', '140001-235959', '0', '0', '2', '1', '1', '1', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'), NULL, NULL, NULL, NULL);".format(
                route_code, row['报文名称'], row['通道编码'], row['通道编码'], "", row['报文编号'])
            f.writelines(sql)
            f.writelines("\n")


if __name__ == '__main__':
    generate_msg_type_sys_status(get_all_cnap_msg_type())
