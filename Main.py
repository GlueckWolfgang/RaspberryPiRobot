###############################################################################
# Raspberry Robot Program
# Version: 2015_12_21
# Creator: Wolfgang Glück
###############################################################################
from Robot_Toolbox.MeasuredValueL import *
from Robot_Toolbox.StatusL import *
from Robot_Toolbox.CommandL import *

# Create instance of measured value list
MeasuredValueList = MeasuredValueL()
MeasuredValueList.generateMeasuredValueList()

# Create instance of status list
StatusList = StatusL()
StatusList.generateStatusList()

# Create instance of command list
CommandList = CommandL()
CommandList.generateCommandList()