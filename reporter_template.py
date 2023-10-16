#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from generator import Main
#if len(sys.argv)>=3:
config_json = sys.argv[1]
selected_template = sys.argv[2]
if os.path.isfile(config_json):
    if 'YYT1818_SingleRun' in selected_template:
        Main.main(config_json, selected_template)
    '''
        jsonDict = JsonUtil.getJson(config_json)
        if selected_template in jsonDict.keys():
            selected = jsonDict[selected_template]
            Main.main(selected['monitor_folder'],selected['cx_project'],selected['pre_plan_ini_template'],selected['export_excel_template'],False,False)
        '''

