# -*- coding: utf-8 -*-
###############################################################################
# Raspberry Robot Program
# Version: 2015_12_29
# Creator: Wolfgang Glück
###############################################################################
import multiprocessing as mp

from Robot_Toolbox.MeasuredValueL import *
from Robot_Toolbox.StatusL import *
from Robot_Toolbox.CommandL import *
from Robot_Toolbox.USBprocess import *
from Robot_Toolbox.Audioprocess import *


###############################################################################
# Main process
if __name__ == '__main__':
    ###########################################################################
    # Create instance of queues and processes
    AQueue = mp.Queue()
    MQueue = mp.Queue()
    CQueue = mp.Queue()
    USBProcess = USBprocess()
    AudioProcess = Audioprocess()
    processList = [mp.Process(target=USBProcess.USBrun, args=(MQueue, CQueue))]
    processList = processlist.append[mp.Process(target=AudioProcess.Audiorun, args=(AQueue))]
    ###########################################################################
    # starting child processes
    for p in processList:
        p.start()
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

    ###########################################################################
    # Endless loop of main program
    while True:
        if not MQueue.empty():
            result = MQueue.get().strip()
            result = result.decode("utf-8")
            # Check if line is a status or a measured value
            if result.find("S@") == 0:
                result = result.replace("S@", "")
                StatusList.putValue(result)

            elif result.find("MV@") == 0:
                result = result.replace("MV@", "")
                MeasuredValueList.putValue(result)
            #print(result)
    ###########################################################################
