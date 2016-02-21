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
    # Regions will be drawn after turning for the required angle

    Building = Region("M", 35.5, 618, 477, 1236, 954)

    GroundFloor = Region("M", 35.5, 618, 477, 1236, 954)
    FirstFloor = Region("M", 35.5, 618, 477, 1236, 954)

    Office = Region("M", 35.5, 148, 684, 295, 472)
    Parents = Region("LM", 35.5, 356, 376, 60, 417, 255, 65, 242)
    Bath = Region("LM", 125.5, 122, 200, 0, 52, 214, 194, 200)
    Shower = Region("M", 35.5, 61, 407, 92, 122)
    Living = Region("LM", 125.5, 571, 500, 149, 733, 1045, 324, 299)
    Kitchen = Region("M", 35.5, 694, 739, 330, 312)

    Corridor1 = Region("M", 35.5, 354, 470, 95, 198)
    Corridor2 = Region("LM", 125.5, 60, 90, -43, 462, 506, 148, 171)
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

    # Define relations between regions respectively their parts
    ###########################################################################
    Relations = Relation()
    Relations.putRelation(Neighbour(Office, "M", None, None, None, None, None, None, OfficeCdoor, "M"))
    Relations.putRelation(Neighbour(Parents, "L", None, None, ParentsCdoor, "M"))
    Relations.putRelation(Neighbour(Parents, "M", None, None, None, None, None, None, ParentsBdoor, "M"))
    Relations.putRelation(Neighbour(Bath, "L", None, None, BathSdoor, "M"))
    Relations.putRelation(Neighbour(Bath, "M", None, None, ParentsBdoor, "M", None, None, BathCdoor, "M"))
    Relations.putRelation(Neighbour(Shower, "M", None, None, None, None, None, None, BathSdoor, "M"))
    Relations.putRelation(Neighbour(Living, "L", None, None, LivingCdoor, "M"))
    Relations.putRelation(Neighbour(Living, "M", None, None, KitchenLdoor, "M"))
    Relations.putRelation(Neighbour(Kitchen, "M", Corridor3, "M", None, None, None, None, Living, "M"))
    Relations.putRelation(Neighbour(Corridor1, "M", ParentsCdoor, "M", None, None, OfficeCdoor, "M", Corridor2, "M"))
    Relations.putRelation(Neighbour(Corridor2, "L", None, None, None, None, BathCdoor, "M"))
    Relations.putRelation(Neighbour(Corridor2, "M", Corridor3, "M", CellerCdoor, "M"))
    Relations.putRelation(Neighbour(Corridor3, "M", None, None, KitchenCdoor, "M", Corridor2, "M", LivingCdoor, "L"))

    Relations.putRelation(Neighbour(OfficeCdoor, "M", None, None, None, None, Office, "M", Corridor1, "M"))
    Relations.putRelation(Neighbour(ParentsBdoor, "M", None, None, None, None, Parents, "M", Bath, "M"))
    Relations.putRelation(Neighbour(ParentsCdoor, "M", Parents, "L", Corridor1, "M"))
    Relations.putRelation(Neighbour(BathCdoor, "M", Bath, "M", Corridor2, "L"))
    Relations.putRelation(Neighbour(BathSdoor, "M", None, None, None, None, None, None, Bath, "L"))
    Relations.putRelation(Neighbour(CellerCdoor, "M", Corridor2, "M"))
    Relations.putRelation(Neighbour(KitchenCdoor, "M", Corridor3, "M", Kitchen, "M"))
    Relations.putRelation(Neighbour(KitchenLdoor, "M", None, None, None, None, Kitchen, "M", Living, "M"))
    Relations.putRelation(Neighbour(LivingCdoor, "M", None, None, None, None, Corridor3, "M", Living, "L"))

    Relations.putRelation(Neighbour(GroundFloor, "I", Office))
    Relations.putRelation(Neighbour(GroundFloor, "I", Parents))
    Relations.putRelation(Neighbour(GroundFloor, "I", Bath))
    Relations.putRelation(Neighbour(GroundFloor, "I", Shower))
    Relations.putRelation(Neighbour(GroundFloor, "I", Living))
    Relations.putRelation(Neighbour(GroundFloor, "I", Kitchen))

    Relations.putRelation(Neighbour(GroundFloor, "I", Corridor1))
    Relations.putRelation(Neighbour(GroundFloor, "I", Corridor2))
    Relations.putRelation(Neighbour(GroundFloor, "I", Corridor3))

    Relations.putRelation(Neighbour(GroundFloor, "I", OfficeCdoor))
    Relations.putRelation(Neighbour(GroundFloor, "I", ParentsBdoor))
    Relations.putRelation(Neighbour(GroundFloor, "I", ParentsCdoor))
    Relations.putRelation(Neighbour(GroundFloor, "I", BathSdoor))
    Relations.putRelation(Neighbour(GroundFloor, "I", BathCdoor))
    Relations.putRelation(Neighbour(GroundFloor, "I", CellerCdoor))
    Relations.putRelation(Neighbour(GroundFloor, "I", KitchenCdoor))
    Relations.putRelation(Neighbour(GroundFloor, "I", KitchenLdoor))
    Relations.putRelation(Neighbour(GroundFloor, "I", LivingCdoor))

    Relations.putRelation(Neighbour(Building, "I", GroundFloor))
    Relations.putRelation(Neighbour(Building, "I", FirstFloor))

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
