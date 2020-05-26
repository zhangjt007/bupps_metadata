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
import xml.etree.ElementTree as ET
from src.IdWorker import IdWorker


def generate_ccms_auth(data):
    """
    根据数据集生成BUPPS_BANKS_INFO表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_CCMS_AUTH.sql"
    count = 0
    with open(out_file, "w", encoding="UTF-8") as f:
        for row in data:
            sql = "INSERT INTO \"BUPPS_CCMS_AUTH\"(\"PAY_CHANNEL\", \"SEND_BRANCH\", \"RECV_BRANCH\", \"MSG_TYPE\", \"BUSI_TYPE_CODE\", \"AUTH_FLAG\", \"AUTH_WEIGTH\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\", \"DATA_ID\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}' , to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'), '{}');".format(
                row['SYSCODE'], row['SENDBANK'], row['RECVBANK'], row['MSGNO'], row['MSGTYPE'], row['FLAG'],
                row['LEVELNUM'], IdWorker.generate())
            f.writelines(sql)
            f.writelines("\n")
            count += 1
            print(count)


if __name__ == '__main__':
    source = "../../resource/CCMSZDT0417.XML"
    xtree = ET.parse(source)
    ccmsDataNode = xtree.getroot()
    ccmsAuthDataNode = ccmsDataNode.find("CCMS_AUTH_DATA")
    rowNode = ccmsAuthDataNode.findall("ROW")
    df_cols = ['SYSCODE', 'SENDBANK', 'RECVBANK', 'MSGNO', 'MSGTYPE', 'FLAG', 'LEVELNUM', 'AUTH_COUNT']
    rows = []
    for node in rowNode:
        syscode = node.findtext("SYSCODE") if node.findtext("SYSCODE") is not None else ""
        sendbank = node.findtext("SENDBANK") if node.findtext("SENDBANK") is not None else ""
        recvbank = node.findtext("RECVBANK") if node.findtext("RECVBANK") is not None else ""
        msgno = node.findtext("MSGNO") if node.findtext("MSGNO") is not None else ""
        msgtype = node.findtext("MSGTYPE") if node.findtext("MSGTYPE") is not None else ""
        flag = node.findtext("FLAG") if node.findtext("FLAG") is not None else ""
        levelnum = node.findtext("LEVELNUM") if node.findtext("LEVELNUM") is not None else ""
        auth_count = node.findtext("AUTH_COUNT") if node.findtext("AUTH_COUNT") is not None else ""
        rows.append({"SYSCODE": syscode,
                     "SENDBANK": sendbank,
                     "RECVBANK": recvbank,
                     "MSGNO": msgno,
                     "MSGTYPE": msgtype,
                     "FLAG": flag,
                     "LEVELNUM": levelnum,
                     "AUTH_COUNT": auth_count})
    generate_ccms_auth(rows)
