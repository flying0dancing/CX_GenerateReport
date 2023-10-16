#!/usr/bin/python
# -*- coding: UTF-8 -*-
from docs import Conf
import os,sys,time,re,logging
from utils import CsvUtil
from utils import ExcelUtil,DateTimeUtil,FileUtil
from utils import Logger
logger = logging.getLogger('generator.Main')

def main(monitorFolder, inputCSV, reporterTemplate):
    flag=0
    precisionData_List = CsvUtil.readCSV4Full(inputCSV)
    logger.info("====================================================")
    logger.info("group,order [notional, measured, offset, tolerance]")
    for precisionData in precisionData_List:
        precisionData.toString()
    logger.info("====================================================")

    reporterNameSet = FileUtil.getFileName(reporterTemplate)
    reporter_full_name = monitorFolder + "\\" + reporterNameSet[0].replace('yyyymmdd',DateTimeUtil.get_dateYYYYMMDDHHMMSS()) + reporterNameSet[1]
    FileUtil.copyAndRenameFile(reporterTemplate, reporter_full_name)
    ExcelUtil.writeAndSaveAsExcel_YYT1818(reporter_full_name,reporter_full_name, 0, 4, precisionData_List)

    return flag

def get_dateYYYMMDD():
    now = time.localtime()
    now_time = time.strftime("%Y%m%d",now)
    return now_time


if __name__=='__main__':
    print(get_dateYYYMMDD())
    print(Conf.BASE_DIR+r'\templates\YYT1818-2022_report_yyyymmdd.xlsx')
    monitorFolder=r'\\10.196.98.73\test\Quality\CX_projects\YYT1818\result\800'
    flag=main(monitorFolder,Conf.BASE_DIR + r"\默认.csv", Conf.BASE_DIR + r'\templates\YYT1818-2022_report_yyyymmdd.xlsx')
    print(flag)