#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : MsgTypeSysStatus.py
@Time    : 2020/5/10 16:29
@Author  : Zhang JinTao
@Version : 1.0.0
@Contact : zhangjt007@gmail.com
@License : (C)Copyright 2020-2021, SOLO
@Des     : None
"""
import pandas as pd
from src.cnap.CommonTools import get_all_cnap_msg_type, cnap_excel_file


def concat_status_str(row):
    str = ''
    if row['日终处理'] == '√':
        str = str + ',8'
    if row['营业准备'] == '√':
        str = str + ',4'
    if row['日间'] == '√':
        str = str + ',5'
    if row['业务截止'] == '√':
        str = str + ',6'
    if row['清算窗口'] == '√':
        str = str + ',7'
    if row['停运/维护'] == '√':
        str = str + ',1,2'
    if str:
        return str[1:]
    return str


def generate_sql_file(sql_file, data):
    """
    根据数据集生成SQL文件
    :param sql_file:
    :param data:
    :return:
    """
    with open(sql_file, "w", encoding="UTF-8") as f:
        for index, row in data.iterrows():
            sys_status = str(row['运行支持状态'])
            if sys_status:
                sql = "INSERT INTO BUPPS_MSG_TYPE_SYS_STATUS(\"MSG_TYPE\", \"PAY_CHANNEL\", \"PARTY_STATUS_SET\") VALUES ('{}', '{}', '{}');".format(
                    row['报文编号'], row['通道编码'], sys_status)
                f.writelines(sql)
                f.writelines("\n")
            else:
                print("生成SQL时忽略该条记录：【%s】" % (row['报文编号']))


if __name__ == '__main__':
    out_file = "../../resource/cnap/BUPPS_MSG_TYPE_SYS_STATUS.sql"
    # 解析参与者发起报文与系统状态对照表
    msgTypeAndSysStatusRel = pd.read_excel(cnap_excel_file, sheet_name="参与者发起报文与系统状态对照表")
    msgTypeAndSysStatusRel['运行支持状态'] = msgTypeAndSysStatusRel.apply(lambda x: concat_status_str(x), axis=1)
    # 去掉"beps.401.001.01"和“beps.402.001.01”，因为在报文列表中不存在
    msgTypeAndSysStatusRel = msgTypeAndSysStatusRel[
        True ^ msgTypeAndSysStatusRel['报文编号'].isin(["beps.401.001.01", "beps.402.001.01"])]
    # 左连接拼接
    result = pd.merge(msgTypeAndSysStatusRel, get_all_cnap_msg_type(), on='报文编号', how='left')
    generate_sql_file(out_file, result)
