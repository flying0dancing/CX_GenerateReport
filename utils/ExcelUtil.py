#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path
import sys
import xlwings as xw

def writeAndSaveAsExcel_YYT1818(fileFullName,SaveAsFileFullName,sheet_index,identifier_column_index,precisionDataList):
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
        for precisionData in precisionDataList:
            if value==precisionData.get_countID():
                sheet3.range(row,col+1).value=precisionData.get_measured_value()
                if precisionData.get_filename():
                    sheet3.range(row, 11).value = precisionData.get_filename()

    #cel.value='xlwings'
    app.calculate() #重新计算一遍所有工作簿里的公式
    wb.save(SaveAsFileFullName)
    wb.close()
    app.screen_updating=True #返回屏幕更新状态
    app.quit()

if __name__=='__main__':
    pass