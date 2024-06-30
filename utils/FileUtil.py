#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path
from utils import DateTimeUtil, ChardetUtil
import re
import shutil, sys
import logging
logger = logging.getLogger('FileUtil')

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
    if fileExist(fname):
        basename = os.path.basename(fname)
        splits=os.path.splitext(basename)
    else:
        splits = os.path.splitext(fname)
    return splits


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
    flag = False
    try:
        for srcfile in files:
            logger.debug("delete file %s" % (srcfile))
            os.remove(srcfile)
        flag = True
    except Exception as e:
        print(e)
    return flag





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
                else:
                    cleanedSearchStr = re.sub(r'[`~!@#\$\^&\(\)\-+=\{\}\[\];,]', ".", fnameSplits[0])  # filter special character
                    if fileMatches(r'^' + cleanedSearchStr + '.*\.csv$', filenames) == False:
                        archiveFiles.append(os.path.join(folderName, filename))

def revFiles_by_keywords(path, keywordsList, fileTypes=['.stl', '.ply'], archiveFiles=[]):
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

'''
retrieve folders for keywords and file types,
if not set keywords and file types, retrieve all files in folder and subfolders.
'''
def revFiles1(path, keywordList, fileTypes, archiveFiles):
    for folderName, subfolders, filenames in os.walk(path):
        for filename in filenames:
            full_filename = os.path.join(folderName, filename)
            suffix = os.path.splitext(filename)[1]
            suffix_lower =suffix.lower()
            if isEmptyList(fileTypes):
                if isEmptyList(keywordList):
                    archiveFiles.append(full_filename)
                    #print(full_filename)
                else:
                    for keyword in keywordList:
                        if keyword in full_filename and full_filename not in archiveFiles:
                            archiveFiles.append(full_filename)
                            #print(full_filename)
            else:
                if suffix_lower in fileTypes:
                    if isEmptyList(keywordList):
                        archiveFiles.append(full_filename)
                        #print(full_filename)
                    else:
                        for keyword in keywordList:
                            if keyword in full_filename and full_filename not in archiveFiles:
                                archiveFiles.append(full_filename)
                                #print(full_filename)



def revFiles_old(path, archivedWhichSubfolderHasKeywords, ignoreFolderWhichContainsFiles, fileTypes=['.stl', '.ply'], archiveFiles=[]):

    for folderName, subfolders, filenames in os.walk(path):
        flag = True
        if isEmptyList(ignoreFolderWhichContainsFiles):
            pass
        else:
            for ignoredFile in ignoreFolderWhichContainsFiles:
                if ignoredFile in filenames:
                    flag=False
                    break
        if flag==True:
            flag_keyword=False
            if isEmptyList(archivedWhichSubfolderHasKeywords):
                flag_keyword = True
            else:
                for keyword in archivedWhichSubfolderHasKeywords:
                    if keyword in folderName:
                        flag_keyword = True
                        break
            if flag_keyword==True:
                for filename in filenames:
                    appendFileInList(folderName,filename,fileTypes,archiveFiles)

def appendFileInList(folderName,filename,fileTypes,archiveFiles):
    suffix = os.path.splitext(filename)[1]
    suffix=suffix.lower()
    if suffix in fileTypes:
        archiveFiles.append(os.path.join(folderName, filename))
def fileMatches(regStr,filenames):
    flag=False
    for filename in filenames:
        matchX=re.match(regStr,filename,re.IGNORECASE) #exlude already calculated file
        if matchX:
            flag=True
            break
    return flag

def get_threshold(regStr, searchedStr):
    str='-1'
    patternX = re.compile(regStr,re.IGNORECASE|re.UNICODE)
    matchX = patternX.match(searchedStr)
    if matchX:
        str=matchX.group(1)
        #print(matchX.group(1))
    return str

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
def copyAndRenameFile_AddSuffix(src,dst):
    if fileExist(src):
        split_names=os.path.splitext(dst)
        count=0
        while fileExist(dst):
            count = count + 1
            dst=split_names[0]+'_'+str(count)+split_names[1]

        logger.info("copy file %s to %s" % (src,dst))
        try:
            shutil.copyfile(src, dst)
            return dst
        except IOError as e:
            logger.error("Unable to copy file. %s" % e )
        except:
            logger.error("Unexpected error", sys.exc_info())
    return None
def renameFile_AddSuffix(dst):
    split_names = os.path.splitext(dst)
    count = 0
    while fileExist(dst):
        count = count + 1
        dst = split_names[0] + '_' + str(count) + split_names[1]
    logger.info("new file's name is: %s" % (dst))

    return dst
def updateFileSeperator(filePath):
    if not isEmptyStr(filePath):
        if filePath.find("\\")!=-1:
            filePath.replace("\\","/")
        if filePath.endswith("/"):
            pass
        else:
            filePath=filePath+"/"
    return filePath


def getFileContent(filepath):
    cached = []
    encodingStr = ChardetUtil.getEncodingStr(filepath)
    with open(filepath, 'r', encoding=encodingStr, errors='ignore') as fileHd:  # for reading chinese charactors
        for line in fileHd.readlines():
            line = line.strip()
            if line == '':
                continue
            else:
                cached.append(line)
    return cached

def isEmptyList(li):
    flag = False
    if li == None or li == []:
        logger.debug("String is empty.")
        flag = True
    return flag

def is_tuple(obj):
    return isinstance(obj, tuple)

def appendValueToDict(dict, key,value):
    v=dict.get(key)
    if v is None:
        dict[key] = value
    else:
        if (int(value) < int(v)):  # 取最小值
            dict[key] = value

def appendDictToDict(dict, key,values):
    sub_exist_dict=dict.get(key)
    if sub_exist_dict is None:
        dict[key] = values
    else:
        for k,v in values.items():
            if k not in sub_exist_dict.keys():
                sub_exist_dict[k]=v
                #dict[key] = sub_exist_dict
            else:
                if(int(v)<int(sub_exist_dict[k])):#取最小值
                    sub_exist_dict[k] = v



if __name__=='__main__':
    archiveFiles = []
    revFolders(r'D:\Kun\CX_projects\YYT1818-2022\autoTest', False,True, ['.stl', '.ply'], archiveFiles)
    for i in archiveFiles:
        print(i)
    #filenames=[r'D:\Kun\CX_projects\YYT1818-2022\autoTest\tip[tip1-2]_time[4].stl',r'D:\Kun\CX_projects\YYT1818-2022\autoTest\tip[tip1-2]_time[3](报告 1).csv',r'D:\Kun\CX_projects\YYT1818-2022\autoTest\tip[tip1-3]_time[2].stl',r'D:\Kun\CX_projects\YYT1818-2022\autoTest\tip[tip1-3]_time[10].stl',r'D:\Kun\CX_projects\YYT1818-2022\autoTest\tip[tip2-1]_time[7].stl',r'D:\Kun\CX_projects\YYT1818-2022\autoTest\tip[tip2-10]_time[6].stl']




