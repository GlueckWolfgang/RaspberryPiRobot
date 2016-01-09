# -*- coding: utf-8 -*-
###############################################################################
# Raspberry Robot Program
# Version: 2016_01_09
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
    MQueue = mp.Queue()
    CQueue = mp.Queue()
    PQueue = mp.Queue()
    LQueue = mp.Queue()

    USBProcess = ProcessUSB()
    AudioProcess = ProcessAudio()
    STAndMVProcess = ProcessStatusAndMeasuredValue()
    AlarmProcess = ProcessAlarmList()

    processList = [mp.Process(target=USBProcess.Run, args=(MQueue, CQueue, PQueue)),
                   mp.Process(target=AudioProcess.Run, args=(MQueue, AQueue, CQueue, CommandList)),
                   mp.Process(target=STAndMVProcess.Run, args=(PQueue, AQueue, LQueue, MQueue, StatusList, MeasuredValueList)),
                   mp.Process(target=AlarmProcess.Run, args=(LQueue, MQueue, AlarmList))]

    # starting child processes
    for i in range(0, len(processList)):
        processList[i].start()

    # Endless loop of main program
    while True:
        if not MQueue.empty():
            result = MQueue.get().strip()

            if result.find("I@") == 0:
                # internal message
                result = result.replace("I@", "")
                print (result)
            time.sleep(1)

    ###########################################################################
