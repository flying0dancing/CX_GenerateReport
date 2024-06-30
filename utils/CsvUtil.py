#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import logging
import traceback
from utils import ChardetUtil
from utils import DataSet
from utils import Logger
logger = logging.getLogger('CsvUtil')

'''
##h
实测值,h1,h2,h3,h4,h5,h6
MaxillaryAnatomy(报告 2),6.0003,5.8744,5.9448,5.9732,5.9652,5.9996
MandibularAnatomy(报告 2),5.9837,5.9068,5.9662,6.0003,5.9583,5.9919
...
计算,10,10,10,10,10,10
合计,60.0133,58.8692,59.6071,59.6745,59.6069,60.006
最小,5.9787,5.8488,5.9448,5.9520,5.9513,5.9825
最大,6.0200,5.9359,5.9750,6.0003,5.9753,6.0139
...
##h1
名称,名义值,实测值,偏差,公差
MaxillaryAnatomy(报告 2),6,6.0003,0.0003,±0.05
MandibularAnatomy(报告 2),6,5.9837,-0.0163,±0.05
'''
def readCSV4Full(fileFullName):
    identifierList = getIdentifiers()
    precisionData_List=[]
    rowNum = 0
    with open(fileFullName, "r", encoding=ChardetUtil.getEncodingStr(fileFullName)) as f:
        reader = csv.reader(f)
        for row in reader:
            rowNum=rowNum+1
            for identifier in identifierList:
                if row[0] == identifier:
                    #print(identifier)
                    next(reader)
                    rowNum = rowNum + 1
                    for i in range(1, 11, 1):
                        line=next(reader)
                        rowNum = rowNum + 1
                        flag=notContainsEmptyCol(line)
                        if flag:  # exclude bad data
                            precisionData_List.append(DataSet.PrecisionData(identifier.replace('##',''),str(i),line,'full',fileFullName))
                            #print(next(reader))
                        else:
                            logger.error("bad data in row[%s], file[%s]" % (rowNum, fileFullName))

    f.close()
    return precisionData_List


'''
##h
名称,结果名称,公差,偏差,名义值,实测值
h1,结果数据 - 1,±0.15,0.0006,6,6.0006
h2,结果数据 - 1,±0.05,0.0378,6,6.0378
h3,结果数据 - 1,±0.05,0.0007,6,6.0007
h4,结果数据 - 1,±0.05,0.0038,6,6.0038
h5,结果数据 - 1,±0.05,0.0279,6,6.0279
h6,结果数据 - 1,±0.05,0.0088,6,6.0088
##l
名称,结果名称,公差,偏差,名义值,实测值
'''
def readCSV4OneGroup(fileFullName, fileOrder,precisionData_List,precisionErrData_list):
    #identifierList = ['##h', '##d', '##l']
    tempList=[]
    flag_result=True
    with open(fileFullName, "r", encoding=ChardetUtil.getEncodingStr(fileFullName)) as f:
        reader = csv.reader(f)
        rowNum=0
        for row in reader:
            rowNum = rowNum+1
            if row[0].startswith('##') or row[0].startswith('名称') or row[0].startswith('Name'):
                continue
            else:
                flag=notContainsEmptyCol(row)
                if flag:#exclude bad data
                    tempList.append(DataSet.PrecisionData(row[0],str(fileOrder),row,'1Group',fileFullName))
                else:
                    logger.error("bad data in row[%s], file[%s]"%(rowNum, fileFullName))
                    precisionErrData_list.append("bad data in row[%s], file[%s],row details: %s"%(rowNum, fileFullName,row))
                    flag_result=False
    f.close()
    if flag_result:
        precisionData_List.extend(tempList)
    return flag_result

def notContainsEmptyCol(row):#exclude bad data
    flag=True
    for tmp in row:
        if tmp:
            pass
        else:
            flag=False
            break
    return flag


def getIdentifiers():
    identifierBriefList = ['##h', '##d', '##l']
    identifierList = []
    for i in identifierBriefList:
        for k in range(1, 7, 1):
            identifierList.append(i + str(k))
    identifierList.remove('##l5')
    identifierList.remove('##l6')

    return identifierList




if '__main__' == __name__:
    pass
    #precisionData_List=readCSV("默认.csv")
    #print("group,order [notional, measured, offset, tolerance]")
    #for precisionData in precisionData_List:
        #precisionData.toString()
