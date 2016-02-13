# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess status and measured value
# Version:  2016.01.21
#
# PQueue             = queue to listen
# AQueue.............= process Audio queue
# LQueue.............= process Alarm list queue
# MQueue             = process Main queue
# WPQueue            = process webserver queue
# StatusList         = image for stati
# MeasuredValueList  = image for measured values
###############################################################################
import copy


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
                # request for data
                WPQueue.put(["S@", copy.copy(StatusList.list)])
                WPQueue.put(["MV@", copy.copy(MeasuredValueList.list)])

            else:
                MQueue.put("I@Process status and measured value: Unknown message at PQueue: " + Message)