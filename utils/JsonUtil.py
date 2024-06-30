import json
from utils import ChardetUtil,FileUtil
import os.path

def getJson(fname):
    obj=None
    if FileUtil.fileExist(fname):
        with open(fname,'r',encoding=ChardetUtil.getEncodingStr(fname)) as fileHd:#for reading chinese charactors
            obj=json.load(fileHd)
    return obj

def setJson(fname,obj):
    with open(fname,'w',encoding=ChardetUtil.getEncodingStr(fname)) as fileHd:
        json.dump(obj,fileHd,ensure_ascii=False,sort_keys=True,indent=4)#for writing chinese charactors


