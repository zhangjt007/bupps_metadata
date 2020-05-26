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


def generate_bank_info(data):
    """
    根据数据集生成BUPPS_BANKS_INFO表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_BANKS_INFO.sql"
    count = 0
    with open(out_file, "w", encoding="UTF-8") as f:
        for row in data:
            sql = "INSERT INTO \"BUPPS_BANKS_INFO\"(\"INNER_BANK\", \"INNER_BANK_NAME\", \"BANK_SHORT_NAME\", \"INNER_SETTLE_BANK\", \"PARTICIPATE_ORG_TYPE\", \"BANK_CATEGORY_CODE\", \"SYS_LEGAL_PERSON\", \"SUPERVISE_BANK\", \"CCPC_CODE\", \"CITY_CODE\", \"ADDR\", \"POSTAL_CODE\", \"TELEPHONE\", \"EMAIL\", \"LOGOUT_DATE\", \"CREATE_DATETIME\",\"UPDATE_DATETIME\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'));".format(
                row['BANKCODE'], row['BANKNAME'], row['BANKNAME'], row['DRECCODE'], row['BANKCATALOG'], row['BANKTYPE'],
                row['AGENTSETTBANK'], row['SUPRLIST'],
                row['CCPC'], row['DEBTORCITY'], row['ADDR'], row['POSTCODE'], row['TEL'], row['EMAIL'], row['EXPDATE'])
            f.writelines(sql)
            f.writelines("\n")
            count += 1
            print(count)


def generate_pay_channel_bank_rel(data):
    """
    根据数据集生成BUPPS_BANKS_INFO表SQL文件
    :param data:
    :return:
    """
    out_file = "../../resource/cnap/BUPPS_PAY_CHANNEL_BANKS_REL.sql"
    payChannel = ['HVPS', 'BEPS', 'IBPS']
    count = 0
    with open(out_file, "w", encoding="UTF-8") as f:
        for row in data:
            count += 1
            print(count)
            for channel in payChannel:
                sql = "INSERT INTO \"BUPPS_PAY_CHANNEL_BANKS_REL\"(\"DATA_ID\", \"PAY_CHANNEL\", \"INNER_BANK\", \"INNER_BANK_NAME\", \"INNER_SETTLE_BANK\", \"OUT_BANK\", \"OUT_BANK_NAME\", \"OUT_SETTLE_BANK\", \"EFFECTIVE_FLAG\", \"LOGOUT_DATE\", \"LOGIN_STATUS\", \"VERSION_DATE\", \"VERSION_TIME\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '1', '{}', '1', '{}', '{}', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'));".format(
                    channel + row['BANKCODE'], channel, row['BANKCODE'], row['BANKNAME'], row['DRECCODE'],
                    row['BANKCODE'], row['BANKNAME'], row['DRECCODE'],
                    row['EXPDATE'], row['EXPDATE'], "000000")
                f.writelines(sql)
                print(sql)
                f.writelines("\n")


if __name__ == '__main__':
    source = "../../resource/CCMSZDT0401.XML"
    xtree = ET.parse(source)
    ccmsDataNode = xtree.getroot()
    ccmsBankDataNode = ccmsDataNode.find("CCMS_BANK_DATA")
    rowNode = ccmsBankDataNode.findall("ROW")
    df_cols = ['BANKCODE', 'BANKNAME', 'BANKCATALOG', 'BANKTYPE', 'PBCCODE', 'CCPC', 'DRECCODE', 'AGENTSETTBANK',
               'SUPRLIST', 'SBSTITNBK', 'DEBTORCITY', 'SYSCODE', 'TEL', 'EFFECTDATE', 'EXPDATE', 'ADDR', 'POSTCODE',
               'EMAIL']
    rows = []
    for node in rowNode:
        bankcode = node.findtext("BANKCODE") if node.findtext("BANKCODE") is not None else ""
        bankname = node.findtext("BANKNAME") if node.findtext("BANKNAME") is not None else ""
        bankcatalog = node.findtext("BANKCATALOG") if node.findtext("BANKCATALOG") is not None else ""
        banktype = node.findtext("BANKTYPE") if node.findtext("BANKTYPE") is not None else ""
        pbccode = node.findtext("PBCCODE") if node.findtext("PBCCODE") is not None else ""
        ccpc = node.findtext("CCPC") if node.findtext("CCPC") is not None else ""
        dreccode = node.findtext("DRECCODE") if node.findtext("DRECCODE") is not None else ""
        agentsettbank = node.findtext("AGENTSETTBANK") if node.findtext("AGENTSETTBANK") is not None else ""
        suprlist = node.findtext("SUPRLIST") if node.findtext("SUPRLIST") is not None else ""
        sbstitnbk = node.findtext("SBSTITNBK") if node.findtext("SBSTITNBK") is not None else ""
        debtorcity = node.findtext("DEBTORCITY") if node.findtext("DEBTORCITY") is not None else ""
        syscode = node.findtext("SYSCODE") if node.findtext("SYSCODE") is not None else ""
        tel = node.findtext("TEL") if node.findtext("TEL") is not None else ""
        postcode = node.findtext("POSTCODE") if node.findtext("POSTCODE") is not None else ""
        addr = node.findtext("ADDR") if node.findtext("ADDR") is not None else ""
        email = node.findtext("EMAIL") if node.findtext("EMAIL") is not None else ""
        effectdate = node.findtext("EFFECTDATE") if node.findtext("EFFECTDATE") is not None else ""
        expdate = node.findtext("EXPDATE") if node.findtext("EXPDATE") is not None else ""
        rows.append({"BANKCODE": bankcode,
                     "BANKNAME": bankname,
                     "BANKCATALOG": bankcatalog,
                     "BANKTYPE": banktype,
                     "PBCCODE": pbccode,
                     "CCPC": ccpc,
                     "DRECCODE": dreccode,
                     "AGENTSETTBANK": agentsettbank,
                     "SUPRLIST": suprlist,
                     "SBSTITNBK": sbstitnbk,
                     "DEBTORCITY": debtorcity,
                     "SYSCODE": syscode,
                     "TEL": tel,
                     "ADDR": addr,
                     "EMAIL": email,
                     "POSTCODE": postcode,
                     "EFFECTDATE": effectdate,
                     "EXPDATE": expdate})
    # generate_bank_info(rows)
    generate_pay_channel_bank_rel(rows)
