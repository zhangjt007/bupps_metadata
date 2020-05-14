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

import pandas as pd
from src.cnap.CommonTools import get_all_cnap_msg_type, cnap_excel_file
import src.IdWorker as idWorker


def generate_msg_type_sys_status(data):
    """
    根据数据集生成BUPPS_MSG_TYPE_SYS_STATUS表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_MSG_TYPE_SYS_STATUS.sql"
    with open(out_file, "w", encoding="UTF-8") as f:
        for index, row in data.iterrows():
            route_code = row['报文编号'].replace('.', '').replace('0', '')
            route_code = route_code[:8]
            sql = "INSERT INTO BUPPS_ROUTE_SERVICE_REL (\"DATA_ID\", \"ROUTE_CODE\", \"ROUTE_NAME\", \"PAY_CHANNEL\", \"SERVICE_TYPE_CODE\", \"SERVICE_TYPE_NAME\", \"PRIORITY\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '1', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'));".format(
                idWorker.generate(), route_code, row['报文名称'].rstrip(), row['通道'].upper(), row['服务代码'],
                row['报文名称'])
            f.writelines(sql)
            f.writelines("\n")


if __name__ == '__main__':
