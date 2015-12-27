# -*- coding: utf-8 -*-
###############################################################################
# Raspberry Robot Program
# Version: 2015_12_27
# Creator: Wolfgang Glück
###############################################################################
import multiprocessing as mp

from Robot_Toolbox.MeasuredValueL import *
from Robot_Toolbox.StatusL import *
from Robot_Toolbox.CommandL import *
from Robot_Toolbox.USBprocess import *


###############################################################################
# Main process
if __name__ == '__main__':
    ###########################################################################
    # Create instance of USB process
    MQueue = mp.Queue()
    CQueue = mp.Queue()
    USBProcess = USBprocess()
    process = mp.Process(target=USBProcess.USBrun, args=(MQueue, CQueue))
    ###########################################################################
    # starting child processes
    process.start()
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
            result = MQueue.get()
            result = result.decode("utf-8")
            print(result)


    ###########################################################################
