#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path
from utils import DateTimeUtil
import re
import shutil, sys
import logging
logger = logging.getLogger('generator.FileUtil')

"""
:return true or false
"""


def fileExist(fname):
    flag = False
    if not isEmptyStr(fname):
        if containsStr(fname, '*') > 0:
            pass
        else:
            flag = os.path.exists(fname)
    return flag


def deleteFile(path):
    if fileExist(path) and os.path.isfile(path):
        logger.info("delete %s" % path)
        os.remove(path)


def cleanFileContent(path):
    if fileExist(path) and os.path.isfile(path):
        logger.info("clean content %s" % path)
        with open(path, 'r+', encoding='utf-8', errors='ignore') as f:  # for reading chinese charactors
            f.seek(0)
            f.truncate()
            f.write('')


def makedirs(fpath):
    if not isEmptyStr(fpath):
        if not fileExist(fpath):
            os.makedirs(fpath)


def deldirs(fpath):
    if not isEmptyStr(fpath):
        if fileExist(fpath):
            os.removedirs(fpath)


def getFileName(fname):
    basename = ''
    if fileExist(fname):
        basename = os.path.basename(fname)
        os.path.splitext(basename)
    return os.path.splitext(basename)


def getFileContentByStr(input, findstr):
    cached = []
    with open(input, 'r', encoding='utf-8', errors='ignore') as fileHd:  # for reading chinese charactors
        for line in fileHd.readlines():
            line = line.strip()
            if line == '':
                continue
            if line.find(findstr) > -1:
                cached.append(line)
                print(line)
    return cached


'''
find some string in file content
@param filepath: a full file name
@param findstr: a str which need to find
@param lineCount: the line count means last lines of the file content
@return: return True or False, True means find the string, False means not find it
'''


def existInFileContentByStr(filepath, findstr, lineCount=10):
    flag = False
    strlist = getFileContentByStrList(filepath, [findstr], lineCount)
    if strlist:
        for astring in strlist:
            if astring.find(findstr) > -1:
                flag = True
                break

    return flag


'''
find some string in file content
@param filepath: a full file name
@param findlist: a str List which need to find
@param lineCount: the line count means last lines of the file content  
@return: last lines's file content 
'''


def getFileContentByStrList(filepath, findlist, linesCount=300):
    cached = []
    rawlines = tail(filepath, linesCount)
    if findlist:
        for line in rawlines:
            line = str(line.strip())
            if line == '':
                continue
            for findstr in findlist:
                if findstr != '' and line.find(findstr) > -1:
                    cached.append(line)
                    print(line)
                    break

    else:
        logger.warning("find string List is empty.")
    return cached


# read last lines of a file
def tail(filepath, n, block=-1024):
    with open(filepath, 'rb') as f:
        f.seek(0, 2)
        filesize = f.tell()
        while True:
            if filesize > abs(block):
                f.seek(block, 2)
                s = f.readlines()
                if len(s) > n:
                    return s[-n:]
                    # break
                else:
                    block *= 2
            else:
                if filesize == abs(block):
                    f.seek(0, 0)
                    s = f.readlines()
                    return s
                block = -filesize


"""
:return the position if (str1 in str), others -3(not run),-2(empty str),-1(not found)
"""


def containsStr(str, str1):
    flag = -3
    if (isEmptyStr(str) or isEmptyStr(str1)):
        flag = -2
    else:
        flag = str.find(str1)
    return flag


"""
:return true or false, string is None or '' or '  ' return true
"""


def isEmptyStr(str):
    flag = False
    if (str == None or str == '' or str.strip() == ''):
        logger.debug("String is empty.")
        flag = True
    return flag


"""
default empty str to ''
"""


def defaultEmpty(str):
    if isEmptyStr(str):
        logger.debug("set default empty string to ''.")
        str = ""
    return str


def getParentFolder(filePath):
    parentFolder = os.path.dirname(os.path.abspath(filePath))  # __file__
    basename = os.path.basename(parentFolder)
    return basename


def deleteFiles(files):
    for srcfile in files:
        logger.debug("delete file %s" % (srcfile))
        os.remove(srcfile)





def revFolders(path,within1DayFlag, overWriteCSVFlag, fileTypes=['.stl','.ply'],archiveFiles=[]):
    for folderName, subfolders, filenames in os.walk(path):
        for subfolder in subfolders:
            if within1DayFlag==True:
                #collect data within 1 day
                date1str = DateTimeUtil.getDateByFolderName(subfolder)
                date2str = DateTimeUtil.get_time()
                if date1str is None or DateTimeUtil.getDiffDays(date1str, date2str)>10: #exclude folder not match date format
                    continue
            '''
            filenames=os.listdir(os.path.join(folderName, subfolder))
            for filename in filenames: #only include files in sub folders, not in folder
                fnameSplits=os.path.splitext(filename)
                if len(fnameSplits)>1 and fnameSplits[1] in fileTypes:
                    if overWriteCSVFlag==True:
                        archiveFiles.append(os.path.join(folderName, subfolder,filename))
                    elif fileMatches(r'^'+fnameSplits[0]+'.*\.csv',filenames)==False:
                        archiveFiles.append(os.path.join(folderName, subfolder, filename))
            '''
        for filename in filenames: #include files in folder and sub folders
            fnameSplits = os.path.splitext(filename)
            if len(fnameSplits) > 1 and fnameSplits[1] in fileTypes:
                if overWriteCSVFlag == True:
                    archiveFiles.append(os.path.join(folderName, filename))
                elif fileMatches(r'^' + fnameSplits[0] + '.*\.csv', filenames) == False:
                    archiveFiles.append(os.path.join(folderName, filename))

def revFiles(path, keywordsList, fileTypes=['.stl', '.ply'], archiveFiles=[]):
    for folderName, subfolders, filenames in os.walk(path):
        for filename in filenames:
            flag=True
            if keywordsList:
                for keyword in keywordsList:
                    #print("keyword: "+keyword)
                    if keyword not in filename:
                        #print("keyword  %s not in subfolder %s" % (keyword, subfolder))
                        flag = False
                        break
            if flag==True:
                suffix=os.path.splitext(filename)[1]
                if suffix in fileTypes:
                    archiveFiles.append(os.path.join(folderName,filename)) 

def fileMatches(regStr,filenames):
    flag=False
    for filename in filenames:
        matchX=re.match(regStr,filename,re.IGNORECASE) #exlude already calculated file
        if matchX:
            flag=True
            break
    return flag


def copyAndRenameFile(src,dst):
    if fileExist(src):
        if fileExist(dst):
            deleteFile(dst)
        logger.info("copy file %s to %s" % (src,dst))
        try:
            shutil.copyfile(src, dst)
        except IOError as e:
            logger.error("Unable to copy file. %s" % e )
        except:
            logger.error("Unexpected error", sys.exc_info())

def updateFileSeperator(filePath):
    if not isEmptyStr(filePath):
        if filePath.find("\\")!=-1:
            filePath.replace("\\","/")
        if filePath.endswith("/"):
            pass
        else:
            filePath=filePath+"/"
    return filePath




if __name__=='__main__':
    archiveFiles = []
    revFolders(r'D:\Kun\CX_projects\YYT1818-2022\autoTest', False,True, ['.stl', '.ply'], archiveFiles)
    for i in archiveFiles:
        print(i)