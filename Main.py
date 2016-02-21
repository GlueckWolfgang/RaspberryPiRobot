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
    # deviation from north is 35.5 degrees

    Building = Region("M", 35.5, 618, 477, 1236, 954)

    GroundFloor = Region("M", 35.5, 618, 477, 1236, 954)
    FirstFloor = Region("M", 35.5, 618, 477, 1236, 954)

    Office = Region("M", 35.5, 148, 684, 295, 472)
    Parents = Region("LM", 35.5, 356, 376, 60, 417, 255, 65, 242)
    Bath = Region("LM", -54.5, 122, 200, 0, 52, 214, 194, 200)
    Shower = Region("M", 35.5, 61, 407, 92, 122)
    Living = Region("LM", -54.5, 571, 500, 149, 733, 1045, 324, 299)
    Kitchen = Region("M", 35.5, 694,739 , 330, 312)

    Corridor1 = Region("M", 35.5, 354, 470, 95, 198)
    Corridor2 = Region("LM", -54.5, 60, 90, -43, 462, 506, 148, 171)
    Corridor3 = Region("M", 35.5, 113, 198, 111, 148)

    OfficeCdoor = Region("M", 35.5, 301, 549, 12, 82)
    ParentsBdoor = Region("M", 35.5, 445, 184, 12, 77)
    ParentsCdoor = Region("M", 35.5, 315, 382, 82, 12)
    BathSdoor = Region("M", 35.5, 453, 90, 1, 61)
    BathCdoor = Region("M", 35.5, 459, 322, 77, 12)
    CellerCdoor = Region("M", 35.5, 461, 507, 82, 12)
    KitchenCdoor = Region("M", 35.5, 663, 507, 77, 12)
    KitchenLdoor = Region("M", 35.5, 877, 786, 12, 77)
    LivingCdoor = Region("M", 35.5, 662, 496, 12, 120)

    # Define relations between regions
    ###########################################################################
    Relations = Relation()
    Relations.putRelation(Neighbour("M", Office, None, None, None, OfficeCdoor))
    Relations.putRelation(Neighbour("L", Parents, None, ParentsCdoor))
    Relations.putRelation(Neighbour("M", Parents, None, None, None, ParentsBdoor))
    Relations.putRelation(Neighbour("L", Bath, None, BathSdoor))
    Relations.putRelation(Neighbour("M", Bath, None, ParentsBdoor, None, BathCdoor))
    Relations.putRelation(Neighbour("M", Shower, None, None, None, BathSdoor))
    Relations.putRelation(Neighbour("L", Living, None, LivingCdoor))
    Relations.putRelation(Neighbour("M", Living, None, KitchenLdoor))
    Relations.putRelation(Neighbour("M", Kitchen, Corridor3, None, None, Living))
    Relations.putRelation(Neighbour("M", Corridor1, ParentsCdoor, None, OfficeCdoor, Corridor2))
    Relations.putRelation(Neighbour("L", Corridor2, None, None, BathCdoor))
    Relations.putRelation(Neighbour("M", Corridor2, Corridor3, CellerCdoor))
    Relations.putRelation(Neighbour("M", Corridor3, None, KitchenCdoor, Corridor2, LivingCdoor))

    Relations.putRelation(Neighbour("M", OfficeCdoor, None, None, Office, Corridor1))
    Relations.putRelation(Neighbour("M", ParentsBdoor, None, None, Parents, Bath))
    Relations.putRelation(Neighbour("M", ParentsCdoor, Parents, Corridor1))
    Relations.putRelation(Neighbour("M", BathCdoor, Bath, Corridor2))
    Relations.putRelation(Neighbour("M", BathSdoor, None, None, None, Bath))
    Relations.putRelation(Neighbour("M", CellerCdoor, Corridor2))
    Relations.putRelation(Neighbour("M", KitchenCdoor, Corridor3, Kitchen))
    Relations.putRelation(Neighbour("M", KitchenLdoor, None, None, Kitchen, Living))
    Relations.putRelation(Neighbour("M", LivingCdoor, None, None, Corridor3, Living))

    Relations.putRelation(Neighbour("I", GroundFloor, Office))
    Relations.putRelation(Neighbour("I", GroundFloor, Parents))
    Relations.putRelation(Neighbour("I", GroundFloor, Bath))
    Relations.putRelation(Neighbour("I", GroundFloor, Shower))
    Relations.putRelation(Neighbour("I", GroundFloor, Living))
    Relations.putRelation(Neighbour("I", GroundFloor, Kitchen))

    Relations.putRelation(Neighbour("I", GroundFloor, Corridor1))
    Relations.putRelation(Neighbour("I", GroundFloor, Corridor2))
    Relations.putRelation(Neighbour("I", GroundFloor, Corridor3))

    Relations.putRelation(Neighbour("I", GroundFloor, OfficeCdoor))
    Relations.putRelation(Neighbour("I", GroundFloor, ParentsBdoor))
    Relations.putRelation(Neighbour("I", GroundFloor, ParentsCdoor))
    Relations.putRelation(Neighbour("I", GroundFloor, BathSdoor))
    Relations.putRelation(Neighbour("I", GroundFloor, BathCdoor))
    Relations.putRelation(Neighbour("I", GroundFloor, CellerCdoor))
    Relations.putRelation(Neighbour("I", GroundFloor, KitchenCdoor))
    Relations.putRelation(Neighbour("I", GroundFloor, KitchenLdoor))
    Relations.putRelation(Neighbour("I", GroundFloor, LivingCdoor))

    Relations.putRelation(Neighbour("I", Building, GroundFloor))
    Relations.putRelation(Neighbour("I", Building, FirstFloor))

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
