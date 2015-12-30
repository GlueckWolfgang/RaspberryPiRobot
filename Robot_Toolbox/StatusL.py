# -*- coding: utf-8 -*-
###############################################################################
# Class of status list
# Version:  2015.12.29
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
        audioMessage = None
        separatedString = string.split(":")                # Status name, value
        value = int(separatedString[1].strip(" "))         # value
        Status = self.getStatusByName(separatedString[0])

        if Status is not None:
            if (Status.stStatus == 0 and value == 1)\
            or (Status.stStatus == 1 and value == 0):
                # edge 0 to 1 or edge 1 to 0
                Status.stStatus = value
                if Status.stAlert is True:
                    audioMessage = ["ST", str(Status.stNumber), str(Status.stAlert), str(Status.stCg), str(value), ""]

        else:
            print("Status not found: ", separatedString[0], "\n")
        return audioMessage

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
        StatusO = Status(0, "Turn finished", False, True)
        self.putStatus(StatusO)
        StatusO = Status(1, "W-LAN disturbance", True, True)
        self.putStatus(StatusO)
        StatusO = Status(2, "USB disturbance", True, True)
        self.putStatus(StatusO)
        StatusO = Status(3, "Stop", False, True)
        self.putStatus(StatusO)
        StatusO = Status(4, "Emergency stop", True, False)
        self.putStatus(StatusO)
        StatusO = Status(5, "Forward slow", False, True)
        self.putStatus(StatusO)
        StatusO = Status(6, "Forward half", False, True)
        self.putStatus(StatusO)
        StatusO = Status(7, "Forward full", False, True)
        self.putStatus(StatusO)
        StatusO = Status(8, "Steering left", False, True)
        self.putStatus(StatusO)
        StatusO = Status(9, "Steering right", False, True)
        self.putStatus(StatusO)
        StatusO = Status(10, "Turn slow 45 left", False, True)
        self.putStatus(StatusO)
        StatusO = Status(11, "Turn slow 45 right", False, True)
        self.putStatus(StatusO)
        StatusO = Status(12, "Turn slow 90 left", False, True)
        self.putStatus(StatusO)
        StatusO = Status(13, "Turn slow 90 right", False, True)
        self.putStatus(StatusO)

        return