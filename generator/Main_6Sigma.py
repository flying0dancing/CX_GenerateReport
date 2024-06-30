#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess
from docs import Conf
import os,logging
from utils import CsvUtil, ExcelUtil, FileUtil, DateTimeUtil, InIUtil, ProcessUtil, JsonUtil, DataSet
from utils import Logger

logger = logging.getLogger('generator.Main_6Sigma')
def main(config_json,selected_template):
    jsonDict = JsonUtil.getJson(config_json)
    if selected_template in jsonDict.keys():
        selected = jsonDict[selected_template]
        monitorFolder=selected['monitor_folder']
        cxproject = selected['cx_project']
        preplanFile = selected['pre_plan_ini_template']
        export_reporterTemplate = selected['export_excel_template']
        files_pattern=r'.*[\\/]?tip\[((\w+\-)(\d+))\]_time\[(.*)\]'
        main_inner(monitorFolder, cxproject, preplanFile, export_reporterTemplate,files_pattern, selected['within1DayFlag'], selected['overWriteCSVFlag'])

def main_inner(monitorFolder,cxprojectname, preplanFile, reporterTemplate,files_pattern,within1DayFlag, overWriteCSVFlag):
    #LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    #logging.FileHandler(os.sep.join([monitorFolder, LOG_FILE]))

    folder_template="\\templates\\"
    folder_log='\\logs\\'
    software_geomagicControlX="GeomagicControlX.exe" #D:\\Program Files\\Oqton\\Geomagic Control X 2023.1\\GeomagicControlX.exe
    flag=0
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
            FileUtil.revFiles_by_keywords(exportFolder,[keyword],['.csv'],exportedReports)
        fileOrder = fileOrder + 1

    if exportedReports==[]:
        FileUtil.revFiles_by_keywords(monitorFolder, None, ['.csv'], exportedReports)
    PrecisionGroupList,precisionErrData_list=DataSet.get_PrecisionGroupList(exportedReports,files_pattern)

    #logger.info("====================================================")
    #for precisionGroup in PrecisionGroupList:
        #precisionGroup.toString()
    #logger.info("====================================================")
    reporterNameSet=FileUtil.getFileName(reporterTemplate)
    reporter_full_name=monitorFolder+"\\"+reporterNameSet[0].replace('yyyymmdd', dateStr)+reporterNameSet[1]
    reporter_new=FileUtil.renameFile_AddSuffix(reporter_full_name)
    ExcelUtil.writeAndSaveAsExcel_YYT1818_6Sigma(reporter_new, 0, PrecisionGroupList,precisionErrData_list)

    return flag



if __name__=='__main__':
    print(Conf.BASE_DIR + r'\templates\YYT1818-2022_report(6Sigma)_yyyymmdd.xlsx')
    monitorFolder=r'C:\D\0629\802'
    #r'\\10.196.98.73\test\Quality\CX_projects\YYT1818\result\800'
    #r'\\10.196.98.73\test\Quality\CX_projects\YYT1818\result\226'  bad data:\\10.196.98.73\test\Quality\CX_projects\YYT1818\result\226\20230711 - 150312 - 1 卧 龙\MandibularAnatomy(报告 1).csv
    cxprojectname=Conf.BASE_DIR+r'\templates\111_0707.CXProj'
    preplanFile=Conf.BASE_DIR + r'\templates\YYT1818-2022_preplan_sample.ini'
    reporterTemplate=Conf.BASE_DIR + r'\templates\YYT1818-2022_report(6Sigma)_yyyymmdd.xlsx'
    flag = main_inner(monitorFolder, cxprojectname, preplanFile, reporterTemplate,False,False)
    print(flag)