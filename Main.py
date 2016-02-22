# -*- coding: utf-8 -*-
###############################################################################
# Raspberry Robot Program
# Version: 2016_02_21
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
from Robot_Toolbox.Region import *
from Robot_Toolbox.Room import *
from Robot_Toolbox.Door import *
from Robot_Toolbox.Neighbour import *
from Robot_Toolbox.Relation import *

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

    # Define regions
    ###########################################################################
    # x/y = 35/0 is located at the inner left top corner of the building
    # deviation from north direction is 35.5 degrees

    Building = Region("I", 35.5, 0, 0, 1236, 920)
    GroundFloor = Region("I", 35.5, 0, 0, 1236, 920)
    FirstFloor = Region("I", 35.5, 0, 0, 1236, 920)

    Office = Room("M", 35.5, 148, 684, 295, 472)
    Parents = Room("I", 35.5, 35, 0)
    Parents1 = Room("M", 35.5, 35, 0, 349, 376)
    Parents2 = Room("M", 35.5, 428, 122, 65, 242)
    Bath = Room("I", 35.5, 500, 70)
    Bath1 = Room("M", 35.5, 500, 70, 180, 122)
    Bath2 = Room("M", 35.5, 461, 122, 194, 200)
    Shower = Room("M", 35.5, 396, 0, 92, 122)
    Living = Room("I", 35.5, 685, 70)
    Living1 = Room("M", 35.5, 685, 70, 500, 501)
    Living2 = Room("M", 35.5, 900, 571, 299, 324)
    Kitchen = Room("M", 35.5, 694, 739, 330, 312)
    Corridor = Room("I", 35.5, 309, 376)
    Corridor1 = Room("M", 35.5, 309, 376, 95, 198)
    Corridor2 = Room("M", 35.5, 404, 376, 189, 148)
    Corridor3 = Room("M", 35.5, 473, 328, 89, 60)
    Corridor4 = Room("M", 35.5, 562, 368, 111, 148)

    OfficeCdoor = Door("M", 35.5, 301, 549, 12, 82)
    ParentsBdoor = Door("M", 35.5, 455, 184, 12, 77)
    ParentsCdoor = Door("M", 35.5, 350, 382, 82, 12)
    BathSdoor = Door("M", 35.5, 453, 96, 1, 52)
    BathCdoor = Door("M", 35.5, 518, 322, 77, 12)
    CellerCdoor = Door("M", 35.5, 461, 542, 82, 12)
    KitchenCdoor = Door("M", 35.5, 627, 542, 77, 12)
    KitchenLdoor = Door("M", 35.5, 877, 751, 12, 77)
    LivingCdoor = Door("M", 35.5, 674, 461, 12, 120)

    # Define relations between regions respectively their parts
    ###########################################################################
    Relations = Relation()
    Relations.putRelation(Neighbour(Office, None, None, None, OfficeCdoor))
    Relations.putRelation(Neighbour(Parents1, None, ParentsCdoor))
    Relations.putRelation(Neighbour(Parents2, None, None, None, ParentsBdoor))
    Relations.putRelation(Neighbour(Bath1, None, None, BathSdoor))
    Relations.putRelation(Neighbour(Bath2, None, BathCdoor, ParentsBdoor))
    Relations.putRelation(Neighbour(Shower, None, None, None, BathSdoor))
    Relations.putRelation(Neighbour(Living1, None, None, LivingCdoor))
    Relations.putRelation(Neighbour(Living2, None, None, KitchenLdoor))
    Relations.putRelation(Neighbour(Kitchen, KitchenCdoor, None, None, KitchenLdoor))
    Relations.putRelation(Neighbour(Corridor1, ParentsCdoor, None, OfficeCdoor, Corridor2))
    Relations.putRelation(Neighbour(Corridor2, Corridor3, CellerCdoor, Corridor1, Corridor4))
    Relations.putRelation(Neighbour(Corridor3, BathCdoor, Corridor2))
    Relations.putRelation(Neighbour(Corridor4, None, KitchenCdoor, Corridor2, LivingCdoor))

    Relations.putRelation(Neighbour(OfficeCdoor, None, None, Office, Corridor1))
    Relations.putRelation(Neighbour(ParentsBdoor, None, None, Parents2, Bath2))
    Relations.putRelation(Neighbour(ParentsCdoor, Parents1, Corridor1))
    Relations.putRelation(Neighbour(BathCdoor, Bath2, Corridor3))
    Relations.putRelation(Neighbour(BathSdoor, None, None, Shower, Bath1))
    Relations.putRelation(Neighbour(CellerCdoor, Corridor2))
    Relations.putRelation(Neighbour(KitchenCdoor, Corridor4, Kitchen))
    Relations.putRelation(Neighbour(KitchenLdoor, None, None, Kitchen, Living2))
    Relations.putRelation(Neighbour(LivingCdoor, None, None, Corridor4, Living1))

    # Define hierarchical dependencies
    ###########################################################################

    Relations.putRelation(Neighbour(GroundFloor, Office))
    Relations.putRelation(Neighbour(GroundFloor, Parents))
    Relations.putRelation(Neighbour(GroundFloor, Bath))
    Relations.putRelation(Neighbour(GroundFloor, Shower))
    Relations.putRelation(Neighbour(GroundFloor, Living))
    Relations.putRelation(Neighbour(GroundFloor, Kitchen))
    Relations.putRelation(Neighbour(GroundFloor, Corridor))

    Relations.putRelation(Neighbour(GroundFloor, OfficeCdoor))
    Relations.putRelation(Neighbour(GroundFloor, ParentsBdoor))
    Relations.putRelation(Neighbour(GroundFloor, ParentsCdoor))
    Relations.putRelation(Neighbour(GroundFloor, BathSdoor))
    Relations.putRelation(Neighbour(GroundFloor, BathCdoor))
    Relations.putRelation(Neighbour(GroundFloor, CellerCdoor))
    Relations.putRelation(Neighbour(GroundFloor, KitchenCdoor))
    Relations.putRelation(Neighbour(GroundFloor, KitchenLdoor))
    Relations.putRelation(Neighbour(GroundFloor, LivingCdoor))

    Relations.putRelation(Neighbour(Building, GroundFloor))
    Relations.putRelation(Neighbour(Building, FirstFloor))

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
