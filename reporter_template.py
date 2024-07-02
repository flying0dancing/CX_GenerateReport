#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from generator import Main,Main_6Sigma
#if len(sys.argv)>=3:
config_json = sys.argv[1]
selected_template = sys.argv[2]
if os.path.isfile(config_json):
    if 'YYT1818_SingleRun'.lower()==selected_template.lower():
        Main.main(config_json, selected_template)
    elif 'YYT1818_6Sigma'.lower()==selected_template.lower():
        if __name__ == '__main__':
            Main_6Sigma.main(config_json, selected_template)
    '''
        jsonDict = JsonUtil.getJson(config_json)
        if selected_template in jsonDict.keys():
            selected = jsonDict[selected_template]
            Main.main(selected['monitor_folder'],selected['cx_project'],selected['pre_plan_ini_template'],selected['export_excel_template'],False,False)
        '''

