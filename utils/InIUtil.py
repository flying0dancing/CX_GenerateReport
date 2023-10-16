#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configparser,os
from docs.Conf import BASE_DIR
from utils import ChardetUtil
import logging
from utils import Logger
logger = logging.getLogger('generator.IniUtil')

def getConfig():
    # defined config file full path
    path=BASE_DIR+r'\templates\TTY1818-2022_preplan_sample.ini'
    config=configparser.ConfigParser()
    config.read(path)
    return config

def updatePreplan(preplan_fullname, cxproject_fullname, input_fullname, outputFolder_fullname):
    preplan_fullname = preplan_fullname.replace("\\", "/")
    #cxproject_fullname = "\"" + cxproject_fullname.replace("\\", "/") + "\""
    #input_fullname="\""+input_fullname.replace("\\","/")+"\""
    #outputFolder_fullname = "\"" + outputFolder_fullname.replace("\\", "/") + "\""
    cxproject_fullname = "\"" + cxproject_fullname + "\""
    input_fullname = "\"" + input_fullname + "\""
    outputFolder_fullname = "\"" + outputFolder_fullname + "\""
    if os.path.isfile(preplan_fullname):
        config = configparser.RawConfigParser()
        config.optionxform=lambda optionstr:optionstr #reserve options' lower/upper cases
        encodingStr=ChardetUtil.getEncodingStr(preplan_fullname)
        config.read(preplan_fullname, encoding=encodingStr)
        general_sec='Option'
        if config.has_section(general_sec):
            for key, value in config[general_sec].items():
                if key.lower() == 'input':
                    logger.info("key %s, old value %s"%(key,value))
                    config.set(general_sec,key,input_fullname)
                    logger.info("key %s, new value %s" % (key, input_fullname))
                if key.lower() == 'outputfolder':
                    logger.info("key %s, old value %s"%(key,value))
                    config.set(general_sec,key,outputFolder_fullname)
                    logger.info("key %s, new value %s" % (key, outputFolder_fullname))
                if key.lower() == 'project':
                    logger.info("key %s, old value %s"%(key,value))
                    config.set(general_sec,key,cxproject_fullname)
                    logger.info("key %s, new value %s" % (key, cxproject_fullname))

        else:
            config.add_section(general_sec)
            config.set(general_sec,'Input',input_fullname)
            config.set(general_sec, 'OutputFolder', outputFolder_fullname)
        config.write(open(preplan_fullname, 'w',encoding=encodingStr))