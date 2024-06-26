#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path
import sys
import shutil
import time
def main(inputFolder,outputFolder,fileTypes=['.stl','.ply']):
    path_parent = os.path.dirname(os.path.abspath(inputFolder)) + "\\"
    input_base_name_prefix, input_base_name_suffix = getname_prefix_suffix(os.path.basename(os.path.abspath(inputFolder)))
    print(input_base_name_prefix)
    print(input_base_name_suffix)
    csd_mesh_log = path_parent + "result_combineFileTo1Folder[" + input_base_name_prefix + "].log"
    while os.path.exists(csd_mesh_log):
        os.remove(csd_mesh_log)

    logger(csd_mesh_log, "export files to output folder")
    logger(csd_mesh_log, "inputFolder: "+inputFolder)
    logger(csd_mesh_log,"outputFolder: "+outputFolder)

    files=[]
    revFiles(inputFolder,fileTypes,files) #get export files by keywords(date, first and last name)
    #print(files)
    makedirs(outputFolder) # create export folder
    if os.path.isdir(outputFolder) and files:
        copy2OutputFolder(files,outputFolder,csd_mesh_log)


def copy2OutputFolder(files,outputFolder,loggerFile):
    index=len(os.listdir(outputFolder))+1
    for srcfile in files:
        splitNames=getFileName(srcfile)
        outputName=str(index)+'_'+splitNames[0]+splitNames[1]#renamed file, like 1_original name
        outputName=os.path.join(outputFolder,outputName)
        logger(loggerFile, "copy file %s to %s" % (srcfile,outputName))
        shutil.copy(srcfile,outputName)
        index=index+1

def getFileName(fname):
    basename=''
    if fileExist(fname):
        basename=os.path.basename(fname)
        os.path.splitext(basename)
    return os.path.splitext(basename)
"""
:return the position if (str1 in str), others -3(not run),-2(empty str),-1(not found)
"""
def containsStr(str,str1):
    flag=-3
    if( isEmptyStr(str) or isEmptyStr(str1)):
        flag=-2
    else:
        flag=str.find(str1)
    return flag
"""
:return true or false, string is None or '' or '  ' return true
"""
def isEmptyStr(str):
    flag=False
    if(str==None or str=='' or str.strip()==''):
        print("Input string is empty.")
        flag=True
    return flag
def makedirs(fpath):
    if not isEmptyStr(fpath):
        if not fileExist(fpath):
            os.makedirs(fpath)
def deleteFile(path):
    if fileExist(path):
        print("delete %s" % path)
        os.remove(path)
"""
:return true or false
"""
def fileExist(fname):
    flag=False
    if not isEmptyStr(fname):
        if containsStr(fname,'*')>0:
            pass
        else:
            flag=os.path.exists(fname)
    return flag

def getname_prefix_suffix(fileName):
    splitArr=os.path.splitext(fileName)
    file_prefix=splitArr[-2]
    file_suffix=splitArr[-1]
    return file_prefix,file_suffix



def revFiles(path,fileTypes=['.stl','.ply'],archiveFiles=[]):
    for folderName, subfolders, filenames in os.walk(path):
        print("folderName: "+folderName)

        for filename in filenames:
            fnameSplits=os.path.splitext(filename)
            if len(fnameSplits)>1 and fnameSplits[1] in fileTypes:
                archiveFiles.append(os.path.join(folderName, filename))


def logger(logfullname,msg):
    with open(logfullname,'a+', encoding='utf-8', errors='ignore') as fileHd: #for reading chinese charactors
        fileHd.write(msg+"\n")
        print(msg)

if __name__=='__main__':
    print(str(sys.argv))
    inputFolder=r'C:\D\0605\ScanFlow'
    outputFolder=r'C:\D\0605\2023060505'
    main(inputFolder,outputFolder)