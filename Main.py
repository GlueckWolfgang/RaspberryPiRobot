# -*- coding: utf-8 -*-
###############################################################################
# Raspberry Robot Program
# Version: 2016_03_06
# Creator: Wolfgang Glück
###############################################################################
import multiprocessing as mp

from Robot_Toolbox.MeasuredValueL import *
from Robot_Toolbox.StatusL import *
from Robot_Toolbox.CommandL import *
from Robot_Toolbox.AlarmL import *
from Robot_Toolbox.ProcessUSB import *
from Robot_Toolbox.ProcessAudio import *
from Robot_Toolbox.ProcessStatusAndMeasuredValue import *
from Robot_Toolbox.ProcessAlarmList import *
from Robot_Toolbox.ProcessWebserver import *
from Robot_Toolbox.Region import *
from Robot_Toolbox.Room import *
from Robot_Toolbox.Door import *
from Robot_Toolbox.Corridor import *
from Robot_Toolbox.Neighbour import *
from Robot_Toolbox.Relation import *
from Robot_Toolbox.PositionL import *

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

    # Create instance of queues and processes
    ###########################################################################
    AQueue = mp.Queue()
    CQueue = mp.Queue()
    LQueue = mp.Queue()
    MQueue = mp.Queue()
    PQueue = mp.Queue()
    WLQueue = mp.Queue()
    WPQueue = mp.Queue()
    WMQueue = mp.Queue()

    USBProcess = ProcessUSB()
    AudioProcess = ProcessAudio()
    STAndMVProcess = ProcessStatusAndMeasuredValue()
    AlarmProcess = ProcessAlarmList()
    WebserverProcess = ProcessWebserver()

    processList = [mp.Process(target=USBProcess.Run, args=(MQueue, CQueue, PQueue)),
                   mp.Process(target=AudioProcess.Run, args=(MQueue, AQueue, CQueue, CommandList)),
                   mp.Process(target=STAndMVProcess.Run, args=(PQueue, AQueue, LQueue, MQueue, WPQueue, CQueue, StatusList, MeasuredValueList)),
                   mp.Process(target=AlarmProcess.Run, args=(LQueue, MQueue, WLQueue, AlarmList)),
                   mp.Process(target=WebserverProcess.Run, args=(WLQueue, WPQueue, WMQueue,MQueue, LQueue, PQueue))]

    # starting child processes
    for i in range(0, len(processList)):
        processList[i].start()

    # set default manual operation and stop
    PQueue.put("S@Manual Operation: 1")
    PQueue.put("S@Stop: 1")

    # Define regions
    ###########################################################################
    # All values in cm , degrees
    # x/y = 35/0 is located at the inner left top corner of the building
    # deviation from north direction is 35.5 degrees

    Building = Region("I", 35.5, 0, 0, 1236, 920)
    GroundFloor = Region("I", 35.5, 0, 0)
    # First floor is empty
    FirstFloor = Region("I", 35.5, 0, 0)
    FirstFloor = Region("M", 35.5, 0, 0, 1236, 920)

    Office = Room("M", 35.5, 148, 684, 295, 472)
    Parents = Room("I", 35.5, 35, 0)
    Parents1 = Room("M", 35.5, 210, 186, 349, 372)
    Parents2 = Room("M", 35.5, 417, 253, 65, 237)
    Bath = Room("I", 35.5, 500, 70)
    Bath1 = Room("M", 35.5, 580, 64, 178, 127)
    Bath2 = Room("M", 35.5, 566, 220, 206, 186)
    Shower = Room("M", 35.5, 442, 61, 92, 122)
    Living = Room("I", 35.5, 685, 70)
    Living1 = Room("M", 35.5, 932, 286, 502, 501)
    Living2 = Room("M", 35.5, 1034, 698, 299, 324)
    Kitchen = Room("M", 35.5, 694, 704, 352, 310)
    Hall = Corridor("I", 35.5, 309, 376)
    Corridor1 = Corridor("M", 35.5, 355, 492, 96, 210)
    Corridor2 = Corridor("M", 35.5, 497, 461, 189, 148)
    Corridor3 = Corridor("M", 35.5, 513, 358, 101, 60)
    Corridor4 = Corridor("M", 35.5, 630, 461, 77, 148)

    OfficeCdoor = Door("M", 35.5, 301, 549, 12, 82)
    ParentsBdoor = Door("M", 35.5, 455, 184, 12, 77)
    ParentsCdoor = Door("M", 35.5, 350, 382, 82, 12)
    BathSdoor = Door("M", 35.5, 490, 96, 3, 52)
    BathCdoor = Door("M", 35.5, 512, 322, 77, 12)
    CellerCdoor = Door("M", 35.5, 461, 542, 82, 12)
    KitchenCdoor = Door("M", 35.5, 627, 542, 77, 12)
    KitchenLdoor = Door("M", 35.5, 877, 751, 12, 77)
    LivingCdoor = Door("M", 35.5, 674, 461, 12, 120)
    LivingTdoor = Door("M", 33.5, 841, 29, 110, 12)

    # Define relations between regions respectively their parts
    ###########################################################################
    Relations = Relation()
    Relations.putRelation(Neighbour(Office, None, None, None, None, OfficeCdoor))
    Relations.putRelation(Neighbour(Parents1, None, None, ParentsCdoor, None, Parents2))
    Relations.putRelation(Neighbour(Parents2, None, None, None, Parents1, ParentsBdoor))
    Relations.putRelation(Neighbour(Bath1, None, None, Bath2, BathSdoor))
    Relations.putRelation(Neighbour(Bath2, None, Bath1, BathCdoor, ParentsBdoor))
    Relations.putRelation(Neighbour(Shower, None, None, None, None, BathSdoor))
    Relations.putRelation(Neighbour(Living1, None, LivingTdoor, Living2, LivingCdoor))
    Relations.putRelation(Neighbour(Living2, None, Living1, None, KitchenLdoor))
    Relations.putRelation(Neighbour(Kitchen, None, KitchenCdoor, None, None, KitchenLdoor))
    Relations.putRelation(Neighbour(Corridor1, None, ParentsCdoor, None, OfficeCdoor, Corridor2))
    Relations.putRelation(Neighbour(Corridor2, None, Corridor3, CellerCdoor, Corridor1, Corridor4))
    Relations.putRelation(Neighbour(Corridor3, None, BathCdoor, Corridor2))
    Relations.putRelation(Neighbour(Corridor4, None, None, KitchenCdoor, Corridor2, LivingCdoor))

    Relations.putRelation(Neighbour(OfficeCdoor, None, None, None, Office, Corridor1))
    Relations.putRelation(Neighbour(ParentsBdoor, None, None, None, Parents2, Bath2))
    Relations.putRelation(Neighbour(ParentsCdoor, None, Parents1, Corridor1))
    Relations.putRelation(Neighbour(BathCdoor, None, Bath2, Corridor3))
    Relations.putRelation(Neighbour(BathSdoor, None, None, None, Shower, Bath1))
    Relations.putRelation(Neighbour(CellerCdoor, None, Corridor2))
    Relations.putRelation(Neighbour(KitchenCdoor, None, Corridor4, Kitchen))
    Relations.putRelation(Neighbour(KitchenLdoor, None, None, None, Kitchen, Living2))
    Relations.putRelation(Neighbour(LivingCdoor, None, None, None, Corridor4, Living1))
    Relations.putRelation(Neighbour(LivingTdoor, None, None, Living1, None, None))

    # Define hierarchical dependencies
    ###########################################################################

    Relations.putRelation(Neighbour(Parents, Parents1))
    Relations.putRelation(Neighbour(Parents, Parents2))
    Relations.putRelation(Neighbour(Bath, Bath1))
    Relations.putRelation(Neighbour(Bath, Bath2))
    Relations.putRelation(Neighbour(Living, Living1))
    Relations.putRelation(Neighbour(Living, Living2))
    Relations.putRelation(Neighbour(Hall, Corridor1))
    Relations.putRelation(Neighbour(Hall, Corridor2))
    Relations.putRelation(Neighbour(Hall, Corridor3))
    Relations.putRelation(Neighbour(Hall, Corridor4))

    Relations.putRelation(Neighbour(GroundFloor, Office))
    Relations.putRelation(Neighbour(GroundFloor, Parents))
    Relations.putRelation(Neighbour(GroundFloor, Bath))
    Relations.putRelation(Neighbour(GroundFloor, Shower))
    Relations.putRelation(Neighbour(GroundFloor, Living))
    Relations.putRelation(Neighbour(GroundFloor, Kitchen))
    Relations.putRelation(Neighbour(GroundFloor, Hall))

    Relations.putRelation(Neighbour(GroundFloor, OfficeCdoor))
    Relations.putRelation(Neighbour(GroundFloor, ParentsBdoor))
    Relations.putRelation(Neighbour(GroundFloor, ParentsCdoor))
    Relations.putRelation(Neighbour(GroundFloor, BathSdoor))
    Relations.putRelation(Neighbour(GroundFloor, BathCdoor))
    Relations.putRelation(Neighbour(GroundFloor, CellerCdoor))
    Relations.putRelation(Neighbour(GroundFloor, KitchenCdoor))
    Relations.putRelation(Neighbour(GroundFloor, KitchenLdoor))
    Relations.putRelation(Neighbour(GroundFloor, LivingCdoor))
    Relations.putRelation(Neighbour(GroundFloor, LivingTdoor))


    Relations.putRelation(Neighbour(Building, GroundFloor))
    Relations.putRelation(Neighbour(Building, FirstFloor))

    Scale = 2.5    # Scale 1/x between real cm and canvas px

    R = []
    Relations.getRegions(GroundFloor, R)
    canvasRect = Relations.transformRegionsToCanvasRect(Scale, R)

    # Define positions
    ###########################################################################

    Positions = PositionL()
    Positions.generatePositions(Relations, GroundFloor, Door)
    Positions.generatePositions(Relations, GroundFloor, Room)
    Positions.generatePositions(Relations, GroundFloor, Corridor)
    canvasCircle = Positions.transformPositionsToCanvasCircle(Scale, Positions)

    # Endless loop of main program
    while True:
            result = MQueue.get()

            if result.find("I@") == 0:
                # internal message
                result = result.replace("I@", "")
                print (result)

            elif result.find("R@") == 0:
                # map data required
                WMQueue.put(canvasRect)

            elif result.find("C@") == 0:
                # position data reqired
                WMQueue.put(canvasCircle)

            else:
                print("Process main: Unknown message at MQueue: " + result)
    ###########################################################################
