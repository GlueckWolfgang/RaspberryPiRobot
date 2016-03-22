# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess status and measured value
# Version:  2016.02.16
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

    def Run(self, PQueue, AQueue, LQueue, MQueue, WPQueue, CQueue, StatusList, MeasuredValueList):

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

            elif Message.find("C@") == 0:
                # Manual command to be sent with interlocking conditions
                Message = Message.replace("C@", "")
                status = Message.split("_")
                operationModeManual = StatusList.getStatusByNumber(19)
                operationModeTargetMove = StatusList.getStatusByNumber(21)
                forwardSlow = StatusList.getStatusByNumber(5)
                forwardHalf = StatusList.getStatusByNumber(6)
                forwardFull = StatusList.getStatusByNumber(7)

                # stop is always allowed
                if status[1] == "3":
                        statusO = StatusList.getStatusByNumber(int(status[1]))
                        CQueue.put(statusO.stDescription + ": " + "1")

                # change operation mode
                # transition from target move to manual is allowed
                elif status[1] == "19"\
                and operationModeTargetMove.stStatus == 1:
                    operationModeTargetMove.stStatus = 0
                    operationModeManual.stStatus = 1

                # transition from manual to target move is allowed
                elif status[1] == "21"\
                and operationModeManual.stStatus == 1:
                    operationModeManual.stStatus = 0
                    operationModeTargetMove.stStatus = 1

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
                    statusO = StatusList.getStatusByNumber(int(status[1]))
                    CQueue.put(statusO.stDescription + ": " + "1")

                # other driving commands allowed if operation mode is manual
                elif operationModeManual.stStatus == 1\
                    and(status[1] != "19"
                    or status[1] != "21"
                    or status[1] != "22"
                    or status[1] != "23"
                    or status[1] != "8"
                    or status[1] != "9"):
                        statusO = StatusList.getStatusByNumber(int(status[1]))
                        CQueue.put(statusO.stDescription + ": " + "1")

            else:
                MQueue.put("I@Process status and measured value: Unknown message at PQueue: " + Message)
