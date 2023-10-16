#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess
import psutil
import time

def execAndWaitFinish(cmdline_str):
    process=subprocess.Popen(cmdline_str)
    while process.poll() is None:
        pass
    #time.sleep(10)
    print('=' * 15)
    while True:
        #if psutil.pid_exists(process.pid) and psutil.pid_exists(process.pid) in psutil.pids():
            #print('running')
            #time.sleep(5)

        if isRunning('RFXOVMain.exe'):
            print('invoke process is still running')
            time.sleep(5)
        else:
            break

    #output=process.stdout.read()
    exit_code=process.returncode
    #print(output)
    return exit_code

def isRunning(process_name):
    result=False #not running
    pl=psutil.pids()
    for pid in pl:
        try:
            process_name_running=psutil.Process(pid).name()
            #if pid not in [0,1,2,3,4,260]:
                #try:
                    #print(process_name_running+' '+psutil.Process(pid).cwd())
                #except:
                    #pass
        except:
            continue
        if( process_name_running== process_name):
            if isinstance(pid, int):
                result=True #is running
    return result
