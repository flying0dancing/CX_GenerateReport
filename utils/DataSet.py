#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import logging
import re
import traceback
from utils import ChardetUtil, CsvUtil, FileUtil
from utils import Logger
logger = logging.getLogger('DataSet')
class PrecisionGroup:
    def __init__(self,tip_Id, tip_groupId, tip_briefId, runtime, tip_runtime_order, filename):
        self.__file_name = filename
        self.__tip_Id = tip_Id
        self.__tip_groupId = tip_groupId
        self.__tip_briefId=tip_briefId
        self.__run_time = runtime
        self.__tip_runtime_order=tip_runtime_order # used for write file by this order
    def set_filename(self,str):
        self.__file_name=str
    def get_filename(self):
        return self.__file_name
    def set_tip_Id(self,str):
        self.__tip_Id=str
    def get_tip_Id(self):
        return self.__tip_Id
    def set_tip_groupId(self,str):
        self.__tip_groupId=str
    def get_tip_groupId(self):
        return self.__tip_groupId
    def set_tip_briefId(self,str):
        self.__tip_briefId=str
    def get_tip_briefId(self):
        return self.__tip_briefId
    def set_run_time(self,str):
        self.__run_time=str
    def get_run_time(self):
        return self.__run_time
    def set_tip_runtime_order(self,str):
        self.__tip_runtime_order=str
    def get_tip_runtime_order(self):
        return self.__tip_runtime_order
    def set_precisionDataList(self,lst):
        self.__precisionDataList=lst
    def get_precisionDataList(self):
        return self.__precisionDataList
    def toString(self):
        logger.info("=========="*10)
        logger.info("[tip Id:%s, runtime:%s, order:%s], %s" % (self.__tip_Id, self.__run_time, self.__tip_runtime_order, self.__file_name))
        logger.info("name/group, order,(measured count) [name/group, notional, measured, offset, tolerance] filename")
        for item in self.get_precisionDataList():
            item.toString()

class PrecisionData:
    def __init__(self, groupID, orderID, row, fileType, filename):
        self.__groupID = groupID
        self.__orderID = orderID
        self.__countID=groupID[0]+orderID+','+groupID[1:]
        self.__countID_reverse=groupID+','+orderID
        try:
            if fileType=='1Group':
                self.__name = row[0]
                self.__notional_value = float(row[4])
                self.__measured_value = float(row[5])
                self.__offset = float(row[3])
                self.__tolerance = float(row[2].replace('±', ''))
                self.__file_name=filename
            else: #full (10Groups)
                self.__name = row[0]
                self.__notional_value = float(row[1])
                self.__measured_value = float(row[2])
                self.__offset = float(row[3])
                self.__tolerance = float(row[4].replace('±',''))
                self.__file_name = filename
        except ValueError as e:
            logger.error(traceback.format_exc())
    def set_name(self,str):
        self.__name=str
    def get_name(self):
        return self.__name
    def set_groupID(self, str):
        self.__groupID = str

    def get_groupID(self):
        return self.__groupID

    def set_orderID(self, str):
        self.__orderID = str

    def get_orderID(self):
        return self.__orderID

    def set_countID(self, str):
        self.__countID=str

    def get_countID_reverse(self):
        return self.__countID_reverse
    def set_countID_reverse(self, str):
        self.__countID_reverse=str

    def get_countID(self):
        return self.__countID

    def set_notional_value(self, val):
        self.__notional_value = val

    def get_notional_value(self):
        return self.__notional_value

    def set_measured_value(self, val):
        self.__measured_value = val

    def get_measured_value(self):
        return self.__measured_value

    def set_offset(self, val):
        self.__offset = val

    def get_offset(self):
        return self.__offset

    def set_tolerance(self, val):
        self.__tolerance = val

    def get_tolerance(self):
        return self.__tolerance

    def set_filename(self,str):
        self.__file_name=str
    def get_filename(self):
        return self.__file_name
    def toString(self):
        logger.info("%s,%s,(%s) [%s, %s, %s, %s, ±%s] %s"%(self.__groupID, self.__orderID,self.__countID, self.__name, self.__notional_value, self.__measured_value, self.__offset, self.__tolerance, self.__file_name))
        #print("%s"%(self.__countID))

def get_PrecisionGroupList(exportedReports,files_pattern):
    tipId_runtime_arr = []
    PrecisionGroupList = []
    precisionErrData_list = []
    for csvname in exportedReports:
        # calculate tipGroup's start tip, tip's start time
        get_tipId_runtime_Orders(csvname,files_pattern, tipId_runtime_arr)
    for csvname in exportedReports:
        if csvname.lower().endswith('.csv'):
            setPrecisonGroupList(csvname,files_pattern,tipId_runtime_arr,PrecisionGroupList,precisionErrData_list)
    return (PrecisionGroupList,precisionErrData_list)
def setPrecisonGroupList(filename,files_pattern, arr, precisionGroupList,precisionErrData_list):
    patternX = re.compile(files_pattern,
                          re.IGNORECASE | re.UNICODE)
    #patternX = re.compile(r'.*[\\/]?tip\[((\w+\-)(\d+))\]_time\[(.*)\]',
                          #re.IGNORECASE | re.UNICODE)  # can match r'D:\Kun\CX_projects\YYT1818-2022\autoTest/tip[tip1-2]_time[3].stl','tip[tip1-2]_time[3].stl'
    matchX = patternX.match(filename)
    if matchX:
        tip_Id,tip_groupId,tip_briefId,run_time,tip_Id_runtime=__set_matchedX(matchX)

        tip_runtime_order=searchArr_by_tipId_runtime(arr,tip_Id_runtime)
        precisionData_List=[]

        dataflag=CsvUtil.readCSV4OneGroup(filename, tip_runtime_order, precisionData_List,precisionErrData_list)
        if dataflag:
            oPrecisionGroup = PrecisionGroup(tip_Id, tip_groupId, tip_briefId, run_time, tip_runtime_order, filename)
            oPrecisionGroup.set_precisionDataList(precisionData_List)
            oPrecisionGroup.toString()
            precisionGroupList.append(oPrecisionGroup)

        #logger.info("========================= Next ===========================")

def __set_matchedX(matchX):
    tip_Id = matchX.group(1)
    tip_groupId = matchX.group(2)
    tip_briefId = matchX.group(3)
    run_time = matchX.group(4)
    tip_Id_runtime = tip_Id + "," + run_time
    # print(tip_Id)
    # print(tip_groupId)
    # print(tip_briefId)
    # print(run_time)
    # print("=======next=======")
    return (tip_Id,tip_groupId,tip_briefId,run_time,tip_Id_runtime)
def get_tipId_runtime_Orders(filename,files_pattern, arr):
    #patternX = re.compile(r'.*[\\/]?tip\[((\w+\-)(\d+))\]_time\[(.*)\]', re.IGNORECASE | re.UNICODE)# can match r'D:\Kun\CX_projects\YYT1818-2022\autoTest/tip[tip1-2]_time[3].stl','tip[tip1-2]_time[3].stl'
    patternX = re.compile(files_pattern,
                          re.IGNORECASE | re.UNICODE)
    matchX = patternX.match(filename)
    if matchX:
        #tip_Id = matchX.group(1)
        #tip_groupId = matchX.group(2)
        #tip_briefId = matchX.group(3)
        #run_time = matchX.group(4)
        #tip_Id_runtime = tip_Id + "," + run_time
        tip_Id,tip_groupId,tip_briefId,run_time,tip_Id_runtime=__set_matchedX(matchX)
        tip_groupBriefId = tip_groupId.replace("-", "").replace("tip", "")
        arr.append([tip_Id_runtime,int(tip_groupBriefId),int(tip_briefId),int(run_time)])

    if arr == []:
        pass
    else:
        #print("========sorted=============")
        arr.sort(key=lambda x: (x[1], x[2], x[3]))
    return matchX

def searchArr_by_tipId_runtime(arr,key):
    order=-1
    for i in range(0,len(arr)):
        if arr[i][0]==key:
            order=i+1
            #print(order)
            break
    return order