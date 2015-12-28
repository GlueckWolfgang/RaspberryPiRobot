# -*- coding: utf-8 -*-
###############################################################################
# Class of status list
# Version:  2015.12.28
###############################################################################
from Robot_Toolbox.Status import *


class StatusL:

    def __init__(self):
        self.list = []                      # List of status objects

    def __str__(self):
        nachricht = " List of stati"
        return nachricht

    def putStatus(self, Status):
        self.list.append(Status)            # index = stNumber
        return

    def putValue(self, string):
        separatedString = string.split(":")   # Status name, value
        Status = self.getStatusByName(separatedString[0])
        if Status is not None:
            separatedString[1] = separatedString[1].strip(" ")
            Status.stStatus = int(separatedString[1])
        else:
            print("Status not found: ", separatedString[0], "\n")
        return

    def getStatusByNumber(self, stNumber):
        if stNumber < len(self.list):       # list must not be empty
            return self.list[stNumber]
        else:
            return None

    def getStatusByName(self, stName):
        for i in range(0, len(self.list)):  # list must not be empty
            if self.list[i].stDescription == stName:
                return self.list[i]
            else:
                continue
        return None

    def generateStatusList(self):
        StatusO = Status(0, "Turn finished", False)
        self.putStatus(StatusO)
        StatusO = Status(1, "W-LAN disturbance", True)
        self.putStatus(StatusO)
        StatusO = Status(2, "USB disturbance", True)
        self.putStatus(StatusO)
        StatusO = Status(3, "Emergency stop", True)
        self.putStatus(StatusO)
        StatusO = Status(4, "Forward slow", False)
        self.putStatus(StatusO)
        StatusO = Status(5, "Forward half", False)
        self.putStatus(StatusO)
        StatusO = Status(6, "Forward full", False)
        self.putStatus(StatusO)
        StatusO = Status(7, "Steering left", False)
        self.putStatus(StatusO)
        StatusO = Status(8, "Steering right", False)
        self.putStatus(StatusO)
        StatusO = Status(9, "Emergency stop", True)
        self.putStatus(StatusO)
        StatusO = Status(10, "Turn slow 45 left", False)
        self.putStatus(StatusO)
        StatusO = Status(11, "Turn slow 45 right", False)
        self.putStatus(StatusO)
        StatusO = Status(12, "Turn slow 90 left", False)
        self.putStatus(StatusO)
        StatusO = Status(13, "Turn slow 90 right", False)
        self.putStatus(StatusO)

        return