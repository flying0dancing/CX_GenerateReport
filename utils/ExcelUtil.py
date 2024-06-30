#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import os.path
import sys
import xlwings as xw
from xlwings import constants

logger = logging.getLogger('ExcelUtil')
def writeAndSaveAsExcel_YYT1818(fileFullName,sheet_index,identifier_column_index,precisionDataList,precisionErrData_list):
    app=xw.App(visible=False, add_book=False)
    app.display_alerts=False #设置提醒信息是否显示
    app.screen_updating=False #关闭屏幕更新
    wb=app.books.open(fileFullName)
    sheet3=wb.sheets[sheet_index]
    info=sheet3.used_range
    nrows=info.last_cell.row #get rows count
    ncolumns=info.last_cell.column #get columns count
    #print(nrows)
    #print(ncolumns)
    for row in range(1,nrows+1):
        #for col in range(1,ncolumns+1):
        col=identifier_column_index
        value=sheet3.range(row,col).value
        #print(value)
        filename=None
        for precisionData in precisionDataList:
            if value==precisionData.get_countID():
                sheet3.range(row,col+1).value=precisionData.get_measured_value()
                filename=precisionData.get_filename()
                if filename:
                    sheet3.range(row, 11).value = filename
        if filename:
            logger.info("imported precision data from %s" % (filename))
    if len(precisionErrData_list)>0:
        sheet4 = wb.sheets.add(after=wb.sheets[-1])
        sheet4.name='Bad Data'
        sheet4.range(1,1).value="Bad Data Check List:"
        for i in range(0,len(precisionErrData_list)):
            sheet4.range(i+2,1).value=precisionErrData_list[i]
    #cel.value='xlwings'
    app.calculate() #重新计算一遍所有工作簿里的公式
    wb.save(fileFullName)
    wb.close()
    app.screen_updating=True #返回屏幕更新状态
    app.quit()

def writeAndSaveAsExcel_YYT1818_6Sigma(fileFullName,sheet_index,precisionGroupList,precisionErrData_list):
    head_name = 1  # get_ColumnIndex(info, r'指标', 1)
    head_notional = 2  # get_ColumnIndex(info,r'接受参照值',2)
    head_count = 3  # get_ColumnIndex(info,r'测量计次',3)
    head_measured = 4  # get_ColumnIndex(info, r'测量值', 4)
    head_tipId = 5  # get_ColumnIndex(info, r'扫描头编号', 5)
    head_testData = 6  # get_ColumnIndex(info, r'测试数据', 6)
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False  # 设置提醒信息是否显示
    app.screen_updating = False  # 关闭屏幕更新
    if os.path.isfile(fileFullName):
        wb = app.books.open(fileFullName)
        sheet3 = wb.sheets[sheet_index]
    else:
        wb=app.books.add()
        sheet3 = wb.sheets[sheet_index]
        sheet3.name = r'YYT1818-2022精度数据'
        row=1
        sheet3.range(row, head_name).value = r'指标'
        sheet3.range(row, head_notional).value = r'接受参照值'
        sheet3.range(row, head_count).value = r'测量计次'
        sheet3.range(row, head_measured).value = r'测量值'
        sheet3.range(row, head_tipId).value = r'扫描头编号'
        sheet3.range(row, head_testData).value = r'测试数据'

    # print(nrows)
    # print(ncolumns)
    arr=['d1','d2','d3','d4','d5','d6','h1','h2','h3','h4','h5','h6','l1','l2','l3','l4']
    fileCount=len(precisionGroupList)
    for precisionGroup in precisionGroupList:
        precisionDataList = precisionGroup.get_precisionDataList()
        order = precisionGroup.get_tip_runtime_order()+1
        #dataCount=0
        for precisionData in precisionDataList:
            #row = dataCount * fileCount + order
            name = precisionData.get_name()
            try:
                position = arr.index(name)
                row = position * fileCount + order
                sheet3.range(row, head_name).value = name
                sheet3.range(row, head_notional).value = precisionData.get_notional_value()
                sheet3.range(row, head_count).value = precisionData.get_name() + ',' + str(precisionGroup.get_run_time())
                sheet3.range(row, head_measured).value = precisionData.get_measured_value()
                sheet3.range(row, head_tipId).value = precisionGroup.get_tip_Id()
                sheet3.range(row, head_testData).value = precisionGroup.get_filename()

            except ValueError:
                logger.error(f"Error: cannot find name/group: {name}。")
            logger.info("imported precision data of %s from %s"%(name,precisionData.get_filename()))
            #dataCount=dataCount+1
    if len(precisionErrData_list)>0:
        sheet4 = wb.sheets.add(after=wb.sheets[-1])
        sheet4.name='Bad Data'
        sheet4.range(1,1).value="Bad Data Check List:"
        for i in range(0,len(precisionErrData_list)):
            sheet4.range(i+2,1).value=precisionErrData_list[i]

    # cel.value='xlwings'
    app.calculate()  # 重新计算一遍所有工作簿里的公式
    wb.save(fileFullName)
    wb.close()
    app.screen_updating = True  # 返回屏幕更新状态
    app.quit()

'''Contains error'''
def get_ColumnIndex(search_range,searchStr,default_index):
    #search_range = sheet.range('1:1')
    #search_range = sheet.range('A1').expand('table')
    values=search_range.value
    found_index=-1
    try:
        found_index = values.index(searchStr)
        # 如果找到了值，获取它的位置
        if found_index:
            found_index=found_index+1
            print(f'值找到在: {found_index}')
    except:
        pass
    if found_index==-1:
        found_index=default_index
    return found_index
if __name__=='__main__':
    pass