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

import pandas as pd

from src.cnap.CommonTools import cnap_excel_file


def generate_bupps_busi_type_info_file(data):
    """
    根据数据集生成BUPPS_BUSI_TYPE_INFO表SQL文件
    :param sql_file:
    :param data:
    :return:
    """
    sql_file = "../../resource/cnap/BUPPS_BUSI_TYPE_INFO.sql"
    with open(sql_file, "w", encoding="UTF-8") as f:
        for index, row in data.iterrows():
            dataId = row['业务类型号'] + str(row['业务种类编码'])
            sql = "INSERT INTO BUPPS_BUSI_TYPE_INFO(\"DATA_ID\", \"BUSI_TYPE_CODE\", \"BUSI_KIND_CODE\", \"BUSI_TYPE_NAME\", \"BUSI_KIND_NAME\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\") VALUES ('{}', '{}', '{}', '{}', '{}', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'));".format(
                dataId, row['业务类型号'], row['业务种类编码'], row['业务类型名称'], row['业务种类'])
            f.writelines(sql)
            f.writelines("\n")


def generate_bupps_channel_busi_type_rel_file(data, pay_channel):
    """
    根据数据集生成BUPPS_CHANNEL_BUSI_TYPE_REL表SQL文件
    :param data:
    :param pay_channel:
    :return:
    """
    sql_file = "../../resource/cnap/BUPPS_CHANNEL_BUSI_TYPE_REL.sql"
    with open(sql_file, "w", encoding="UTF-8") as f:
        for pay_channel_index in pay_channel:
            for index, row in data.iterrows():
                dataId = pay_channel_index[0] + row['业务类型号'] + str(row['业务种类编码'])
                sql = "INSERT INTO BUPPS_CHANNEL_BUSI_TYPE_REL(\"DATA_ID\", \"PAY_CHANNEL\", \"PAY_CHANNEL_NAME\", \"BUSI_TYPE_CODE\", \"BUSI_TYPE_NAME\", \"BUSI_KIND_CODE\", \"BUSI_KIND_NAME\", \"SUBSYS_BUSI_TYPE\", \"SUBSYS_BUSI_KIND\", \"CREATE_DATETIME\", \"UPDATE_DATETIME\") VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', to_char(sysdate, 'yyyymmddhh24miss'), to_char(sysdate, 'yyyymmddhh24miss'));".format(
                    dataId, pay_channel_index[0], pay_channel_index[1], row['业务类型号'], row['业务种类编码'], row['业务类型名称'],
                    row['业务种类'],
                    row['业务类型号'], row['业务种类编码'])
                f.writelines(sql)
                f.writelines("\n")


if __name__ == '__main__':
    busiType = pd.read_excel(cnap_excel_file, sheet_name="业务类型编码")
    # 根据条件业务类型号不为4位,获取业务类型好和业务类型名称
    busiType = busiType[['业务类型号', '业务类型名称']][busiType['业务类型号'].map(len) == 4]
    # 删除业务类型号重复的数据
    # keep="first"表示保留第一次出现的数据
    # inplace=True表示直接在原来的DataFrame上删除重复项，而默认值False表示生成一个副本
    busiType.drop_duplicates('业务类型号', keep="first", inplace=True)
    busiTypeAndBusiKindRel = pd.read_excel(cnap_excel_file, sheet_name="业务类型与业务种类对照表")
    busiTypeAndBusiKindRel['业务种类编码'] = busiTypeAndBusiKindRel['业务种类编码'].apply(lambda x: str(x).zfill(5))
    busiTypeAndBusiKindRel = busiTypeAndBusiKindRel[
        True ^ busiTypeAndBusiKindRel['序号'].str.contains('大额系统|小额系统|SAPS系统|CCMS系统|网银系统')]
    result = pd.merge(busiType[['业务类型号', '业务类型名称']], busiTypeAndBusiKindRel[['业务类型', '业务类型编码', '业务种类', '业务种类编码']],
                      left_on='业务类型号', right_on='业务类型编码', how='left')
    # 填充左连接后业务种类为NA的情况
    result.fillna("", inplace=True)
    generate_bupps_busi_type_info_file(result)
    generate_bupps_channel_busi_type_rel_file(result, [("HVPS", "大额系统"), ("BEPS", "小额系统"), ("IBPS", "超网系统")])
