# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess status and measured value
# Version:  2016.01.09
#
# PQueue             = queue to listen
# AQueue.............= process Audio queue
# LQueue.............= process Alarm list queue
# MQueue             = process Main queue
# StatusList         = image for stati
# MeasuredValueList  = image for measured values
###############################################################################


class ProcessStatusAndMeasuredValue:

    def __str__(self):
        nachricht = "Process Status and measured value"
        return nachricht

    def Run(self, PQueue, AQueue, LQueue, MQueue, StatusList, MeasuredValueList):

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
            else:
                MQueue.put("I@Process status and measured value: Unknown message at PQueue: " + Message)

