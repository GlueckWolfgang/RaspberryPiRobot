# -*- coding: utf-8 -*-
###############################################################################
# Raspberry Robot Program
# Version: 2015_12_27
# Creator: Wolfgang Glück
###############################################################################
import time
import multiprocessing as mp

from Robot_Toolbox.MeasuredValueL import *
from Robot_Toolbox.StatusL import *
from Robot_Toolbox.CommandL import *
from Robot_Toolbox.USBprocess import *

# Create instance of measured value list
MeasuredValueList = MeasuredValueL()
MeasuredValueList.generateMeasuredValueList()

# Create instance of status list
StatusList = StatusL()
StatusList.generateStatusList()

# Create instance of command list
CommandList = CommandL()
CommandList.generateCommandList()

###############################################################################
# Create instance of USB process and start it
MQueue = mp.Queue
CQueue = mp.Queue

USBProcess = USBprocess()
process = mp.Process(target=USBProcess.USBrun, args=(MQueue, CQueue))

if __name__ == '__main__':
    process.start()

    process.join()

    ###########################################################################
    # Endles loop of main program
    while True:

        result = MQueue.get()
        if result is not None:
            print(result)

        time.sleep(0.01)
    ###########################################################################
