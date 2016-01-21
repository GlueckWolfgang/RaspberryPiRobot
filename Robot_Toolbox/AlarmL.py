# -*- coding: utf-8 -*-
###############################################################################
# Class of alarm list
# Version:  2016.01.21
# not yet fully tested!
###############################################################################
import copy
from Robot_Toolbox.Alarm import *


class AlarmL:

    def __init__(self):
        self.list = []           # List of alarm objects in temporal sequence
        self.actualPage = []     # alarms of actual visible page
        self.actualPageNo = 1    # actual visible page number
        self.maxPageNo = 1       # maximum pagenumber depends on number of alarms
        self.numberOfLines = 45  # Number of lines per page

    def __str__(self):
        nachricht = "List of alarms"
        return nachricht

    def getActualPage(self):
        alarmList = []
        for i in range(0, len(aelf.actualPage)):
            AlarmO = self.actualPage[i]
            Alarmtext = [AlarmO.alDateTime,
                         AlarmO.alDescription]
            if AlarmO.alType == "ST":
                Alarmtext.append("")
            else:
                Alarmtext.append(AlarmO.alValue)
            if AlarmO.alStatus == "0":
                Alarmtext.appen(AlarmO.alStatusTextG)
            else:
                Alarmtext.append(AlarmO.alStatusTextC)
            if AlarmO.alAcknowledged is True:
                Alarmtext.append(AlarmO.alAcknowledgeTextTrue)
            else:
                Alarmtext.append(AlarmO.alAcknowledgeTextFalse)
            alarmList.appen(Alarmtext)
        return alarmList

    def putAlarm(self, AlarmO, MQueue):
        self.list.append(AlarmO)
        self.maxPageNo = len(self.list) / self.numberOfLines
        if len(self.list) % self.numberOfLines > 0:
            self.maxPageNo += 1
        self.fillActualPage()
        # for test reasons only, until the web client works
        #######################################################################
        MQueue.put("I@\nAlarmlist:")
        for i in range(0, len(self.list)):
            AlarmO = self.list[i]
            Alarmtext = AlarmO.alDateTime + " " + AlarmO.alDescription + " "
            if AlarmO.alType == "ST":
                Alarmtext = Alarmtext + "                       "
            else:
                Alarmtext = Alarmtext + AlarmO.alValue + " "
            if AlarmO.alStatus == "0":
                Alarmtext = Alarmtext + AlarmO.alStatusTextG + " "
            else:
                Alarmtext = Alarmtext + AlarmO.alStatusTextC + " "
            if AlarmO.alAcknowledged is True:
                Alarmtext = Alarmtext + AlarmO.alAcknowledgeTextTrue + " "
            else:
                Alarmtext = Alarmtext + AlarmO.alAcknowledgeTextFalse + " "
            if AlarmO.alDelete is True:
                Alarmtext = Alarmtext + "D"
            Alarmtext = Alarmtext + "\n"

            MQueue.put("I@" + Alarmtext)

        #######################################################################
        return

    def fillActualPage(self):
        # internal use
        self.actualPage = []
        for i in range(0, len(self.list)):
            if i >= (self.actualPageNo - 1) * self.numberOfLines\
            and i < self.actualPageNo * self.numberOfLines:
                self.actualPage.append(self.list[i])
        return self.actualPageNo

    def pageForward(self):
        if self.actualPageNo < self.maxPageNo:
            self.actualPageNo += 1
            self.fillActualPage()
        return self.actualPageNo

    def pageBackward(self):
        if self.actualPageNo > 1:
            self.actualPageNo -= 1
            self.fillActualPage()
        return self.actualPageNo

    def acknowledgeAlarmList(self, MQueue):
        # start at the end of list and read alarms and set alAcknowledged
        for i in range(len(self.list) - 1, -1, -1):
            AlarmO = self.list[i]
            AlarmO.alAcknowledged = True
            # if the alarm was going
            if AlarmO.alStatus == "0":
                for j in range(i, -1, -1):
                    if AlarmO.alNumber == self.list[j].alNumber\
                    and AlarmO.alType == self.list[j].alType\
                    and AlarmO.alSubType == self.list[j].alSubType:
                        # set alDelete for all elder alarms of the same number,type and subtype
                        # even the last alarm of this number, type and subtype
                        self.list[j].alDelete = True

            else:
            # the alarm was comming
                for j in range(i - 1, -1, -1):
                    if AlarmO.alNumber == self.list[j].alNumber\
                    and AlarmO.alType == self.list[j].alType\
                    and AlarmO.alSubType == self.list[j].alSubType:
                        # set alDelete for all elder alarms of the same number,type and subtype
                        # except the last alarm of this number, type and subtype
                        self.list[j].alDelete = True

        # delete all alarms with alDelete is set
        listCopy = copy.copy(self.list)
        for i in range(0, len(listCopy)):
            if listCopy[i].alDelete is True:
                self.list.remove(listCopy[i])
        listCopy = []

        # adapt maxPageNo after acknowledge execution
        self.maxPageNo = len(self.list) / self.numberOfLines
        if len(self.list) % self.numberOfLines > 0:
            self.maxPageNo += 1

        # check if actualPageNo is out of range after acknowledge execution
        if self.actualPageNo > self.maxPageNo:
            self.actualPageNo = self.maxPageNo

        # actualize actual page
        self.fillActualPage()

        return self.actualPageNo
