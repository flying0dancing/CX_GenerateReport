#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess
import psutil
import time

def execAndWaitFinish(cmdline_str):
    exit_code=-1
    try:
        process = subprocess.Popen(cmdline_str)
        while process.poll() is None:
            pass
        time.sleep(15)
        print('=' * 15)
        count=0

        while True:
            # if psutil.pid_exists(process.pid) and psutil.pid_exists(process.pid) in psutil.pids():
            # print('running')
            # time.sleep(5)
            count =count + 1

            if isRunning('RFXOVMain.exe'):
                if count==1:
                    print('invoke process is still running', end=' ')
                else:
                    print('.', end=' ')
                time.sleep(5)
            else:
                break

        # output=process.stdout.read()
        exit_code = process.returncode
        # print(output)
    except Exception as e:
        print(str(e))
    return exit_code

def isRunning(process_name):
    result=False #not running
    pl=psutil.pids()
    for pid in pl:
        try:
            process_name_running=psutil.Process(pid).name()
            #print(f"PID: {pid} - Status: {process_name_running.status()}")
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
