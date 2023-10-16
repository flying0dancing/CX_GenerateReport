#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess
from docs import Conf
import os,logging
from utils import CsvUtil, ExcelUtil,FileUtil,DateTimeUtil,InIUtil,ProcessUtil,JsonUtil
from utils import Logger

logger = logging.getLogger('generator.Main')
def main(config_json,selected_template):
    jsonDict = JsonUtil.getJson(config_json)
    if selected_template in jsonDict.keys():
        selected = jsonDict[selected_template]
        monitorFolder=selected['monitor_folder']
        cxproject = selected['cx_project']
        preplanFile = selected['pre_plan_ini_template']
        export_reporterTemplate = selected['export_excel_template']
        main_inner(monitorFolder, cxproject, preplanFile, export_reporterTemplate, selected['within1DayFlag'], selected['overWriteCSVFlag'])

def main_inner(monitorFolder,cxprojectname, preplanFile, reporterTemplate,within1DayFlag, overWriteCSVFlag):
    #LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    #logging.FileHandler(os.sep.join([monitorFolder, LOG_FILE]))
    folder_template="\\templates\\"
    folder_log='\\logs\\'
    software_geomagicControlX="GeomagicControlX.exe" #D:\\Program Files\\Oqton\\Geomagic Control X 2023.1\\GeomagicControlX.exe
    flag=0
    precisionData_List = []
    archiveFiles = []
    exportedReports=[]
    dateStr=DateTimeUtil.get_dateYYYYMMDD()
    FileUtil.revFolders(monitorFolder,within1DayFlag, overWriteCSVFlag, ['.stl', '.ply'], archiveFiles) #search files within one day and not contains csv
    fileOrder=1
    for filename in archiveFiles:
        print(filename)
        exportFolder=os.path.dirname(filename)
        #TODO copy ini and update with filename
        preplan_with_dateorder=preplanFile.replace(folder_template,folder_log).replace('_sample.ini','_'+dateStr+'_'+str(fileOrder)+'.ini')
        FileUtil.copyAndRenameFile(preplanFile,preplan_with_dateorder)
        InIUtil.updatePreplan(preplan_with_dateorder,cxprojectname,filename,exportFolder)
        #os.system('"D:\\Program Files\\Oqton\\Geomagic Control X 2023.1\\GeomagicControlX.exe" '+preplan_with_dateorder)
        cmdlineStr=[software_geomagicControlX, preplan_with_dateorder]
        result_code=ProcessUtil.execAndWaitFinish(cmdlineStr)
        if result_code==0:
            keyword=FileUtil.getFileName(filename)[0]
            FileUtil.revFiles(exportFolder,[keyword],['.csv'],exportedReports)
        fileOrder = fileOrder + 1
    fileOrder = 1
    exportedReports=[]
    FileUtil.revFiles(monitorFolder, None, ['.csv'], exportedReports)
    for csvname in exportedReports:
        if csvname.lower().endswith('.csv'):
            CsvUtil.readCSV4OneGroup(csvname, fileOrder, precisionData_List)
            fileOrder = fileOrder + 1

    logger.info("====================================================")
    logger.info("group, order [notional, measured, offset, tolerance]")
    for precisionData in precisionData_List:
        precisionData.toString()
    logger.info("====================================================")
    reporterNameSet=FileUtil.getFileName(reporterTemplate)
    reporter_full_name=monitorFolder+"\\"+reporterNameSet[0].replace('yyyymmdd', dateStr)+reporterNameSet[1]
    FileUtil.copyAndRenameFile(reporterTemplate,reporter_full_name)
    ExcelUtil.writeAndSaveAsExcel_YYT1818(reporter_full_name, reporter_full_name, 0, 4, precisionData_List)

    return flag



if __name__=='__main__':
    print(Conf.BASE_DIR + r'\templates\YYT1818-2022_report_yyyymmdd.xlsx')
    monitorFolder=r'V:\Quality\CX_projects\YYT1818\result\800'
    #r'\\10.196.98.73\test\Quality\CX_projects\YYT1818\result\800'
    #r'\\10.196.98.73\test\Quality\CX_projects\YYT1818\result\226'  bad data:\\10.196.98.73\test\Quality\CX_projects\YYT1818\result\226\20230711 - 150312 - 1 卧 龙\MandibularAnatomy(报告 1).csv
    cxprojectname=Conf.BASE_DIR+r'\templates\111_0707.CXProj'
    preplanFile=Conf.BASE_DIR + r'\templates\YYT1818-2022_preplan_sample.ini'
    reporterTemplate=Conf.BASE_DIR + r'\templates\YYT1818-2022_report_yyyymmdd.xlsx'
    flag = main_inner(monitorFolder, cxprojectname, preplanFile, reporterTemplate,False,False)
    print(flag)