# -*- coding: utf-8 -*-
###############################################################################
# Class of alarm list
# Version:  2016.02.07
#
###############################################################################
import copy
from Robot_Toolbox.Alarm import *
import json


class AlarmL:

    def __init__(self):
        self.list = []           # List of alarm objects in temporal sequence
        self.actualPage = []     # alarms of actual visible page
        self.actualPageNo = 1    # actual visible page number
        self.maxPageNo = 1       # maximum pagenumber depends on number of alarms
        self.numberOfLines = 25  # Number of lines per page

        # generate an empty dictionary as template
        self.template = {"actual": "&nbsp;", "last": "&nbsp;"}
        for i in range(0, self.numberOfLines):
            for j in range(0, 7):
                element = {str(i + 1) + "." + str(j + 1): "&nbsp;"}
                self.template.update(element)

    def __str__(self):
        nachricht = "List of alarms"
        return nachricht

    def getActualPage(self, MQueue):
        # first line contains some head information
        alarmList = [[str(self.actualPageNo), str(self.maxPageNo),str(self.numberOfLines)]]

        # the following lines containing alarm rows of actual page
        for i in range(0, len(self.actualPage)):
            AlarmO = self.actualPage[i]
            Alarmtext = [AlarmO.alDateTime[0:23],
                         AlarmO.alDescription]
            if AlarmO.alType == "ST":
                Alarmtext.append("")
                Alarmtext.append("")
                Alarmtext.append("")
            else:
                Alarmtext.append(AlarmO.alLimit)
                Alarmtext.append(AlarmO.alValue)
                Alarmtext.append(AlarmO.alDimension)

            if AlarmO.alStatus == "0":
                Alarmtext.append(AlarmO.alStatusTextG)
            else:
                Alarmtext.append(AlarmO.alStatusTextC)

            if AlarmO.alAcknowledged is True:
                Alarmtext.append(AlarmO.alAcknowledgeTextTrue)
            else:
                Alarmtext.append(AlarmO.alAcknowledgeTextFalse)

            alarmList.append(Alarmtext)

        # generate dictionary from empty template
        dictionary = copy.copy(self.template)
        dictionary.update({"actual": alarmList[0][0], "last": alarmList[0][1]})

        # fill in existing alarmlist values except headline [0][1..7]
        for i in range(1, len(alarmList)):
            for j in range(0, 7):
                element = {str(i) + "." + str(j + 1): alarmList[i][j]}
                dictionary.update(element)

        output = json.dumps(dictionary)

        return output

    def putAlarm(self, AlarmO, MQueue):
        self.list.append(AlarmO)
        self.maxPageNo = int(len(self.list) / self.numberOfLines)
        if len(self.list) % self.numberOfLines > 0:
            self.maxPageNo += 1
        self.fillActualPage()
        return

    def fillActualPage(self):
        # internal use
        self.actualPage = []
        for i in range(0, len(self.list)):
            if i >= (self.actualPageNo - 1) * self.numberOfLines\
            and i < self.actualPageNo * self.numberOfLines:
                self.actualPage.append(self.list[i])
        return self.actualPageNo

    def firstPage(self):
        self.actualPageNo = 1
        self.fillActualPage()
        return self.actualPageNo

    def lastPage(self):
        self.actualPageNo = self.maxPageNo
        self.fillActualPage()
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
        self.maxPageNo = int(len(self.list) / self.numberOfLines)
        if len(self.list) % self.numberOfLines > 0\
        or self.maxPageNo == 0:
            self.maxPageNo += 1

        # check if actualPageNo is out of range after acknowledge execution
        if self.actualPageNo > self.maxPageNo:
            self.actualPageNo = self.maxPageNo

        # actualize actual page
        self.fillActualPage()

        return self.actualPageNo
