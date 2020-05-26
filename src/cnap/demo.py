import xml.etree.ElementTree as ET

source = "../../resource/CCMSZDT0307.XML"
xtree = ET.parse(source)
ccmsDataNode = xtree.getroot()
ccmsMsgtypeDataNode = ccmsDataNode.find("CCMS_MSGTYPE_DATA")
rowNode = ccmsMsgtypeDataNode.findall("ROW")
for row in rowNode:
    print(row.findtext("SYSCODsE"))
