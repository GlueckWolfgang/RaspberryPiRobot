# -*- coding: utf-8 -*-
###############################################################################
# Class of alarm list
# Version:  2016.01.07
# not yet tested!
###############################################################################
import copy
from Robot_Toolbox.Alarm import *


class AlarmL:

    def __init__(self):
        self.list = []                      # List of alarm objects
                                            # in temporal sequence
        self.actualPage = []                # alarms of actual visible page
        self.actualPageNo = 1               # actual visible page number
        self.maxPageNo = 1                  # maximum pagenumber depends on
                                            # number of alarms in list
        self.numberOfLines = 45             # Number of lines per page
        self.fillActualPage()

    def __str__(self):
        nachricht = " List of alarms"
        return nachricht

    def putAlarm(self, AlarmO):
        self.list.append(AlarmO)
        self.maxPageNo = len(self.list) / self.numberOfLines
        if len(self.list) % self.numberOfLines > 0:
            self.maxPageNo += 1
        self.fillActualPage()
        return

    def fillActualPage(self):
        self.actualPage = []
        for i in range(0, len(self.list)):
            if i >= (self.actualPageNo - 1) * self.numberOfLines\
            and i < self.actualPageno * self.numberOfLines:
                self.actualPage.append(self.list[i])
        return self.actualPageNo

    def pageForward(self):
        if actualPageNo < maxPageNo:
            actualPageNo += 1
            self.fillActualPage()
        return self.actualPageNo

    def pageBackward(self):
        if actualPageNo > 1:
            actualPageNo -= 1
            self.fillActualPage()
        return self.actualPageNo

    def firstPage(self):
        self.actualPageNo = 1
        return self.actualPageNo

    def lastPage(self):
        self.actualPageNo = maxPageNo
        return self.actualPageNo

    def getActualPageNo(self):
        return self.actualPageNo

    def getMaxPageNo(self):
        return self.maxPageNo

    def acknowledgeAlarmList(self):
        # start at the end of list and read alarms and set alAcknowledge
        for i in range(len(self.list - 1), -1):
            self.AlarmO = self.list[i]
            self.AlarmO.alAcknowledge = True

            # if the alarm was going
            if self.list[i].alStatus == 0:
                for j in range(i, -1):
                    if self.alarmO.alNumber == self.list[i].alNumber\
                    and self.alarmO.alType == self.list[i].alType\
                    and self.alarmO.alSubtype == self.list[i].alsubType:
                        # set alDelete for all elder alarms of the same number,type and subtype
                        # even the last alarm of this number, type and subtype
                        self.AlarmO.alDelete = True
            else:
            # the alarm was comming,
                for j in range(i - 1, -1):
                    if self.alarmO.alNumber == self.list[i].alNumber\
                    and self.alarmO.alType == self.list[i].alType\
                    and self.alarmO.alSubtype == self.list[i].alsubType:
                        # set alDelete for all elder alarms of the same number,type and subtype
                        # except the last alarm of this number, type and subtype
                        self.AlarmO.alDelete = True

        # delete all alarms with alDelete is set
        self.listCopy = copy.copy(self.list)
        for i in range(0, len(self.listCopy)):
            if self.listCopy[i].alDelete is True:
                del self.list[i]
        self.listCopy = []

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
