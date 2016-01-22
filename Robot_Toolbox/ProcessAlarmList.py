# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess Alarm list
# Version:  2016.01.21
#
# LQueue             = queue to listen
# MQueue             = process Main queue
# WLQueue            = process webserver queue
# AlarmList          = Alarm list
###############################################################################


class ProcessAlarmList:

    def __str__(self):
        nachricht = "Process Alarm list"
        return nachricht

    def Run(self, LQueue, MQueue, WLQueue, AlarmList):
        while True:
            Message = LQueue.get()

            if Message[0] == "L@":
                # Put Alarm
                AlarmList.putAlarm(Message[1], MQueue)

            elif Message[0] == "Q@":
                # Acknowledge alarm list
                AlarmList.acknowledgeAlarmList(MQueue)

            elif Message[0] == "R@":
                # Request from webserver
                WLQueue.put(AlarmList.getActualPage())

            else:
                MQueue.put("I@Process Alarm list: Unknown message at LQueue " + Message[0])
