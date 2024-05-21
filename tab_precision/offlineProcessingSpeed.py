#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os.path
import time,datetime
import subprocess
import sys
def refineSpeed(inputfile):
    csd_mesh_grandparent = os.path.dirname(os.path.abspath(inputfile)) + "\\"
    #print(csd_mesh_grandparent)
    input_base_name_prefix,input_base_name_suffix=getname_prefix_suffix(os.path.basename(os.path.abspath(inputfile)))
    # delete existed result file
    csd_mesh_log = csd_mesh_grandparent + "result_OfflineProcessingSpeed["+input_base_name_prefix+"].log"
    while os.path.exists(csd_mesh_log):
        os.remove(csd_mesh_log)
    data=getFileContent(inputfile)
    logger(csd_mesh_log, "analyze log for offline speed: "+inputfile)
    timeData = []
    for i in range(len(data)):
        logger(csd_mesh_log,data[i])
        if data[i].find('AcquisitionToCheck, refine resolution is 0') > -1:
            if data[i + 1].find('ToothMeshRefineProc end') > -1:
                diff = "low solution(0):" + str(calcTimeDiff(data[i][0:19], data[i + 1][0:19]))
                timeData.append(diff)
        if data[i].find('AcquisitionToCheck, refine resolution is 1') > -1:
            if data[i + 1].find('ToothMeshRefineProc end') > -1:
                diff = "standard solution(1):" + str(calcTimeDiff(data[i][0:19], data[i + 1][0:19]))
                timeData.append(diff)
        if data[i].find('AcquisitionToCheck, refine resolution is 2') > -1:
            if data[i + 1].find('ToothMeshRefineProc end') > -1:
                diff = "high solution(2):" + str(calcTimeDiff(data[i][0:19], data[i + 1][0:19]))
                timeData.append(diff)
    for i in timeData:
        logger(csd_mesh_log,i)
    logger(csd_mesh_log, "result is at " + csd_mesh_log)
    return timeData

def calcTimeDiff(begin, end):
    #print(begin)
    #print(end)
    diffSeconds = round(time.mktime(time.strptime(end, "%Y-%m-%dT%H:%M:%S")) - time.mktime(time.strptime(begin, "%Y-%m-%dT%H:%M:%S")))
    #print(str(diffSeconds))
    m, s = divmod(diffSeconds, 60)
    h, m = divmod(m, 60)
    if(diffSeconds<60):
        diff="%d''" % (s)
    else:
        diff="%d'%d''" % (m, s)
    return diff

def getFileContent(input):
    cached=[]
    with open(input,'r', encoding='utf-8', errors='ignore') as fileHd:#for reading chinese charactors
        for line in fileHd.readlines():
            line=line.strip()
            if line=='':
                continue
            if line.find('AcquisitionToCheck, refine resolution is')>-1:
                cached.append(line)
                #print(line)
            if line.find('ToothMeshRefineProc end')>-1:
                cached.append(line)
                #print(line)
    return cached
def logger(logfullname,msg):
    with open(logfullname,'a+', encoding='utf-8', errors='ignore') as fileHd:#for reading chinese charactors
        fileHd.write(msg+"\n")
        print(msg)

def inputFile():
    str=input("input log's full name:")
    while not os.path.isfile(str) :
        str = input("input log's full name:")

    return str

def getname_prefix_suffix(fileName):
    splitArr=os.path.splitext(fileName)
    file_prefix=splitArr[-2]
    file_suffix=splitArr[-1]
    return file_prefix,file_suffix

if __name__=='__main__':
    print(str(sys.argv))
    #inputfile=r'C:\ProgramData\TW\AcqAltair\log\acqaltair_20220712.csv'
    inputfile=r'\\10.196.98.73\test\Quality\Test_Obj_ScanFlow\Precision\Precision_Result_Ver1.0.9.662.d251_kun\3700_Offline_Speed\ScanFlow_20230712.csv'
    #refineSpeed(inputFile())
    refineSpeed(inputfile)
    #calcTimeDiff('2021-05-21T15:25:30', '2021-05-21T15:27:21')