# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess status and measured value
# Version:  2016.02.14
#
# PQueue             = queue to listen
# AQueue.............= process Audio queue
# LQueue.............= process Alarm list queue
# MQueue             = process Main queue
# WPQueue            = process webserver queue
# StatusList         = image for stati
# MeasuredValueList  = image for measured values
###############################################################################
import json


class ProcessStatusAndMeasuredValue:

    def __str__(self):
        nachricht = "Process Status and measured value"
        return nachricht

    def Run(self, PQueue, AQueue, LQueue, MQueue, WPQueue, StatusList, MeasuredValueList):

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

            elif Message.find("R@") == 0:
                # request for data (Panel.html)

                # get measured values
                dictionary1 = dict()
                dictionary1 = MeasuredValueList.getData(MQueue)
                # MQueue.put("I@ MVdic:" + json.dumps(dictionary1))

                # get status values
                dictionary2 = dict()
                dictionary2 = StatusList.getData(MQueue)
                # MQueue.put("I@ STdic:" + json.dumps(dictionary2))

                # mixup both dicts
                dictionary = dict()
                dictionary.update(dictionary1)
                dictionary.update(dictionary2)
                # send to webserver
                output = json.dumps(dictionary)
                WPQueue.put(output)
            else:
                MQueue.put("I@Process status and measured value: Unknown message at PQueue: " + Message)
