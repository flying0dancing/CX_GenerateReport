#!/usr/bin/python
# -*- coding: UTF-8 -*-
import chardet
from utils import FileUtil


def getEncodingStr(filename):
    encodingStr = 'utf-8'
    if FileUtil.fileExist(filename):
        with open(filename, "rb") as f:
            encoding_message = chardet.detect(f.read())
            encodingStr = encoding_message['encoding']
            #print(encodingStr)
        f.close()
        #f = open(filename, "rb")
        #encoding_message = chardet.detect(f.read())
        #encodingStr = encoding_message['encoding']
        #f.close()
    return encodingStr
