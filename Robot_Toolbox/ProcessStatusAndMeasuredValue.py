# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess status and measured value
# Version:  2016.05.03
#
# PQueue             = queue to listen
# AQueue.............= process Audio queue
# LQueue.............= process Alarm list queue
# MQueue             = process Main queue
# WPQueue            = process webserver queue
# CQueue             = process USB queue
# StatusList         = image for stati
# MeasuredValueList  = image for measured values
# CommandList        = image for commands
###############################################################################
import json


class ProcessStatusAndMeasuredValue:

    def __str__(self):
        nachricht = "Process Status and measured value"
        return nachricht

    def Run(self, PQueue, AQueue, LQueue, MQueue, WPQueue, CQueue, SMQueue, StatusList, MeasuredValueList, CommandList):

        while True:
            Message = PQueue.get()
            if Message.find("S@") == 0:
                Message = Message.replace("S@", "")
                # Put status
                StatusList.putValue(Message, AQueue, LQueue, MQueue)

            elif Message.find("MV@") == 0:
                Message = Message.replace("MV@", "")
                # Put measured value
                MeasuredValueList.putValue(Message, AQueue, LQueue, MQueue)

            elif Message.find("I@") == 0:
                # mirrored command
                MQueue.put(Message)

            elif Message.find("R@Panel") == 0:
                # request for data (Panel.html)

                # get measured values
                dictionary1 = dict()
                dictionary1 = MeasuredValueList.getPanelData(MQueue)
                # MQueue.put("I@ MVdic:" + json.dumps(dictionary1))

                # get status values
                dictionary2 = dict()
                dictionary2 = StatusList.getPanelData(MQueue)
                # MQueue.put("I@ STdic:" + json.dumps(dictionary2))

                # mixup both dicts
                dictionary = dict()
                dictionary.update(dictionary1)
                dictionary.update(dictionary2)

                # send to webserver
                output = json.dumps(dictionary)
                WPQueue.put(output)

            elif Message.find("R@Map") == 0:
                # request for data (Map.html)
                # get status values
                dictionary = dict()
                dictionary = StatusList.getMapData(MQueue)

                # send to webserver
                output = json.dumps(dictionary)
                WPQueue.put(output)

            elif Message.find("MS@") == 0:
                # get stStatus by number
                Message = Message.replace("MS@", "")
                statusNo = int(Message)
                status = StatusList.getStatusByNumber(statusNo)
                SMQueue.put(str(status.stStatus))

            elif Message.find("MM@") == 0:
                # get value from measured value by number
                Message = Message.replace("MM@", "")
                mvNo = int(Message)
                measuredValue = MeasuredValueList.getMeasuredValueByNumber(mvNo)
                SMQueue.put(str(measuredValue.value))

            elif Message.find("C@") == 0:
                # Manual command to be sent with interlocking conditions
                Message = Message.replace("C@", "")
                status = Message.split("_")
                operationModeManual = StatusList.getStatusByNumber(19)
                operationModeTargetMove = StatusList.getStatusByNumber(21)
                operationModeSetBearing = StatusList.getStatusByNumber(30)
                setN = StatusList.getStatusByNumber(32)
                setS = StatusList.getStatusByNumber(33)
                setW = StatusList.getStatusByNumber(34)
                setE = StatusList.getStatusByNumber(35)
                startEndposition = StatusList.getStatusByNumber(24)
                tag = StatusList.getStatusByNumber(25)
                run = StatusList.getStatusByNumber(26)
                usbDisturbance = StatusList.getStatusByNumber(2)
                emergencyStop = StatusList.getStatusByNumber(4)

                forwardSlow = StatusList.getStatusByNumber(5)
                forwardHalf = StatusList.getStatusByNumber(6)
                forwardFull = StatusList.getStatusByNumber(7)

                if status[0] == "mouse":
                    if operationModeTargetMove.stStatus == 1\
                    and run != 1:
                        # mouse click allowed for start end position and tag
                        if startEndposition.stStatus == 1:
                            MQueue.put("M@startEndposition_" + status[1] +"_" + status[2] + "_" + status[3])
                        elif tag.stStatus == 1:
                            MQueue.put("M@tag_" + status[1] +"_" + status[2] + "_" + status[3])

                    elif operationModeSetBearing.stStatus == 1:
                        # mouse click allowed for robot position
                        MQueue.put("M@robotPosition_" + status[1] + "_" +status[2] + "_" + status [3])

                # status[0] == "S"
                # stop is always allowed
                elif status[1] == "3":
                    run.stStatus = 0
                    # send stop command
                    CQueue.put(CommandList.sendCommandByNumber(0, "1"))

                # change operation mode
                # manual is allowed always
                elif status[1] == "19":
                    operationModeTargetMove.stStatus = 0
                    operationModeSetBearing.stStatus = 0
                    startEndposition.stStatus = 0
                    tag.stStatus = 0
                    run.stStatus = 0
                    setN.stStatus = 0
                    setS.stStatus = 0
                    setW.stStatus = 0
                    setE.stStatus = 0
                    operationModeManual.stStatus = 1
                    # Stop command
                    CQueue.put(CommandList.sendCommandByNumber(0, "1"))
                    # delete robot position
                    MQueue.put("M@robotPosition_delete")

                    # save bearing values to csv file
                    MQueue.put("BF@")

                # transition from manual or set bearing to target move is allowed
                elif status[1] == "21"\
                and (operationModeManual.stStatus == 1
                or operationModeSetBearing.stStatus == 1):
                    operationModeManual.stStatus = 0
                    operationModeSetBearing.stStatus = 0
                    setN.stStatus = 0
                    setS.stStatus = 0
                    setW.stStatus = 0
                    setE.stStatus = 0
                    operationModeTargetMove.stStatus = 1
                    # Stop command
                    CQueue.put(CommandList.sendCommandByNumber(0, "1"))
                    # delete robot position
                    MQueue.put("M@robotPosition_delete")

                    # save bearing values to csv file
                    MQueue.put("BF@")

                # transition from target move or manual to setBearing is allowed
                elif (operationModeTargetMove.stStatus == 1
                or operationModeManual.stStatus == 1)\
                and status[1] == "30":
                    # Set Bearing
                    operationModeManual.stStatus = 0
                    operationModeTargetMove.stStatus = 0
                    operationModeSetBearing.stStatus = 1
                    # Stop command
                    CQueue.put(CommandList.sendCommandByNumber(0, "1"))
                    # delete robot position
                    MQueue.put("M@robotPosition_delete")

                # Robot align, Steering left steering right and steering ahead
                # only allowed if Forward slow or Forward half or Forward full
                # is true
                elif (status[1] == "8"
                or status[1] == "9"
                or status[1] == "22"
                or status[1] == "23")\
                and (forwardSlow.stStatus == 1
                or forwardHalf.stStatus == 1
                or forwardFull.stStatus == 1):
                    CQueue.put(CommandList.sendCommandByNumber(int(status[1]), "1"))

                # Start end position allowed if operation mode is target move
                elif operationModeTargetMove.stStatus == 1\
                and(status[1] == "24"):
                    # toggle status
                    startEndposition.stStatus = startEndposition.stStatus ^ 1
                    tag.stStatus = 0

                elif operationModeTargetMove.stStatus == 1\
                and(status[1] == "25"):
                    # toggle status
                    tag.stStatus = tag.stStatus ^ 1
                    startEndposition.stStatus = 0

                elif operationModeTargetMove.stStatus == 1\
                and usbDisturbance.stStatus == 0\
                and emergencyStop.stStatus == 0\
                and(status[1] == "26"):
                    # run
                    tag.stStatus = 0
                    startEndposition.stStatus = 0
                    run.stStatus = 1
                    # start run sequence
                    MQueue.put("SR@")

                elif operationModeTargetMove.stStatus == 1\
                and(status[1] == "15"):
                    # turn slow to
                    CQueue.put(CommandList.sendCommandByNumber(int(status[1]), status[2]))

                elif operationModeTargetMove.stStatus == 1\
                and(status[1] == "29"):
                    # Encounter reset
                    CQueue.put(CommandList.sendCommandByNumber(int(status[1]), "1"))

                elif operationModeTargetMove.stStatus == 1\
                and(status[1] == "5"):
                    # Forward slow
                    CQueue.put(CommandList.sendCommandByNumber(int(status[1]), "1"))

                elif operationModeSetBearing.stStatus == 1\
                and(status[1] == "32"):
                    # Set N
                    MQueue.put("SB@0")
                    PQueue.put("S@Set N: 0")

                elif operationModeSetBearing.stStatus == 1\
                and(status[1] == "33"):
                    # Set S
                    MQueue.put("SB@1800")
                    PQueue.put("S@Set S: 0")

                elif operationModeSetBearing.stStatus == 1\
                and(status[1] == "34"):
                    # Set W
                    MQueue.put("SB@2700")
                    PQueue.put("S@Set W: 0")

                elif operationModeSetBearing.stStatus == 1\
                and(status[1] == "35"):
                    # Set E
                    MQueue.put("SB@900")
                    PQueue.put("S@Set E: 0")

                # other driving commands allowed if operation mode is manual
                elif operationModeManual.stStatus == 1\
                    and(status[1] != "19"
                    or status[1] != "21"
                    or status[1] != "22"
                    or status[1] != "23"
                    or status[1] != "8"
                    or status[1] != "9"
                    or status[1] != "24"
                    or status[1] != "25"
                    or status[1] != "26"):
                        CQueue.put(CommandList.sendCommandByNumber(int(status[1]), "1"))

            else:
                MQueue.put("I@Process status and measured value: Unknown message at PQueue: " + Message)
