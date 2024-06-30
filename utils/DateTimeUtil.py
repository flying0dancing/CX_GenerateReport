import time,datetime
import os.path
from time import strftime
import logging
logger = logging.getLogger('DateTimeUtil')

def get_time():
    now = time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S",now)
    return now_time

def get_dateYYYYMMDD():
    now = time.localtime()
    now_time = time.strftime("%Y%m%d",now)
    return now_time

def get_dateYYYYMMDDHHMMSS():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

'''
return None if the fname doesn't match export folder's name rule, ex. fname='20230605 - 163537 - 3800 YYT' result: 20230605163537
'''
def getDateByFolderName(fname):
    pics_fname = fname.split(' - ')
    #print(pics_fname[0])
    if len(pics_fname)>1:
        format="%Y%m%d%H%M%S"
        datetime_result=pics_fname[0]+pics_fname[1]
    else:
        datetime_result=None
    return datetime_result

def getDiffDays(datetime1Str,datetime2Str):
    date1=datetime.datetime.strptime(datetime1Str,"%Y%m%d%H%M%S")
    date2=datetime.datetime.strptime(datetime2Str, "%Y-%m-%d %H:%M:%S")
    duration=date2-date1
    return duration.days

def getDateTimeOfFile(fname):
    ctime=os.path.getmtime(fname)
    return timeStampToTime(ctime)

def timeStampToTime(timestamp):
    timeStruct=time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)

if __name__ == '__main__':
    #now_time = get_dateYYYMMDD()
    #print(now_time)
    date1str = getDateByFolderName('20230614 - 123537 - 3800 YYT')
    date2str = get_time()
    if date1str is not None:
        print(getDiffDays(date1str, date2str))

    
