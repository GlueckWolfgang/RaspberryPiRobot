# -*- coding: utf-8 -*-
###############################################################################
# Raspberry Robot Program
# Version: 2016_02_16
# Creator: Wolfgang Glück
###############################################################################
import multiprocessing as mp
import time

from Robot_Toolbox.MeasuredValueL import *
from Robot_Toolbox.StatusL import *
from Robot_Toolbox.CommandL import *
from Robot_Toolbox.AlarmL import *
from Robot_Toolbox.ProcessUSB import *
from Robot_Toolbox.ProcessAudio import *
from Robot_Toolbox.ProcessStatusAndMeasuredValue import *
from Robot_Toolbox.ProcessAlarmList import *
from Robot_Toolbox.ProcessWebserver import *


###############################################################################
# Main process
if __name__ == '__main__':
    ###########################################################################
    # Create instance of measured value list
    MeasuredValueList = MeasuredValueL()
    MeasuredValueList.generateMeasuredValueList()

    # Create instance of status list
    StatusList = StatusL()
    StatusList.generateStatusList()

    # Create instance of command list
    CommandList = CommandL()
    CommandList.generateCommandList()

    # Create instance of alarm list
    AlarmList = AlarmL()

    ###########################################################################
    # Create instance of queues and processes
    AQueue = mp.Queue()
    CQueue = mp.Queue()
    LQueue = mp.Queue()
    MQueue = mp.Queue()
    PQueue = mp.Queue()
    WLQueue = mp.Queue()
    WPQueue = mp.Queue()

    USBProcess = ProcessUSB()
    AudioProcess = ProcessAudio()
    STAndMVProcess = ProcessStatusAndMeasuredValue()
    AlarmProcess = ProcessAlarmList()
    WebserverProcess = ProcessWebserver()

    processList = [mp.Process(target=USBProcess.Run, args=(MQueue, CQueue, PQueue)),
                   mp.Process(target=AudioProcess.Run, args=(MQueue, AQueue, CQueue, CommandList)),
                   mp.Process(target=STAndMVProcess.Run, args=(PQueue, AQueue, LQueue, MQueue, WPQueue, CQueue, StatusList, MeasuredValueList)),
                   mp.Process(target=AlarmProcess.Run, args=(LQueue, MQueue, WLQueue, AlarmList)),
                   mp.Process(target=WebserverProcess.Run, args=(WLQueue, WPQueue, MQueue, LQueue, PQueue))]



    # starting child processes
    for i in range(0, len(processList)):
        processList[i].start()

    # set default manual operation and stop
    PQueue.put("S@Manual Operation: 1")
    PQueue.put("S@Stop: 1")

    count = 1

    # Endless loop of main program
    while True:
        while not MQueue.empty():
            result = MQueue.get()

            if result.find("I@") == 0:
                # internal message
                result = result.replace("I@", "")
                print (result)

        time.sleep(1)

    ###########################################################################
