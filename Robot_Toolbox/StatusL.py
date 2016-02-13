# -*- coding: utf-8 -*-
###############################################################################
# Class of status list
# Version:  2016.01.28
###############################################################################
from Robot_Toolbox.Status import *
from Robot_Toolbox.Alarm import *
from Robot_Toolbox.Audio import *
import datetime
import json
import re
import codecs
from bs4 import BeautifulSoup as Soup



class StatusL:

    def __init__(self):
        self.list = []                      # List of status objects
        template_S = dict()

        def get_ids(html_file, regular_expression):
             ids = dict()
             with codecs.open(html_file, 'r', encoding='utf-8', errors='ignore') as fh:
               soup = Soup(fh, 'html.parser')
               for element in soup.find_all('td', id=re.compile(regular_expression)):
                   id = element.get('id')
                   if id:
                       ids[id] = ""
                       if id.endswith("_V"):
                       # add Cv
                           id = id.replace("_V", "_Cv")
                           ids[id] = ""
             return ids

        # create dictionary
        template_S = get_ids("Robbi/Panel.html", r'["id=S_]+"')

    def __str__(self):
        nachricht = "List of stati"
        return nachricht

    def putStatus(self, Status):
        self.list.append(Status)            # index = stNumber
        return

    def putValue(self, string, AQueue, LQueue, MQueue):
        audioMessage = None
        separatedString = string.split(":")                # Status name, value
        value = int(separatedString[1].strip(" "))         # value
        Status = self.getStatusByName(separatedString[0])

        if Status is not None:
            if (Status.stStatus != value                   # comming / going
            and Status.stAlert is True):
                # edge 0 to 1 or edge 1 to 0
                # generate alarm for alarm list
                AlarmO = Alarm(str(datetime.datetime.now()),
                               Status.stDescription,
                               "ST",
                               str(Status.stNumber),  # int 0..n
                               "",                    # Subtype for measured value
                               str(value),            # int 0/1
                               "",                    # DType for measured value
                               "",                    # Limit of measured value
                               "",                    # Value for measured value
                               "")                    # Dimension for measured value

                LQueue.put(["L@", AlarmO])

            if (Status.stStatus != value                   # comming / going
            and Status.stCg is True
            and Status.stAlert is True)\
            or(Status.stStatus != value and value == 1     # comming only
            and Status.stCg is False
            and Status.stAlert is True):
                # edge 0 to 1 or edge 1 to 0
                # generate audio message
                if Status.stAlert is True:
                    audioMessage = Audio("ST",
                                          str(Status.stNumber),
                                          Status.stCg,
                                          str(value),
                                          "0")        # for measured value only
            Status.stStatus = value

        else:
            MQueue.put("I@Process status and measured value: Status not found: " + separatedString[0])
        if audioMessage is not None:
            AQueue.put(audioMessage)
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
        # structure = number, description text, stAlert, stCg
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
        StatusO = Status(14, "Compass", False, True)
        self.putStatus(StatusO)
        StatusO = Status(15, "Amplifier", False, True)
        self.putStatus(StatusO)
        StatusO = Status(16, "TestPoint1", True, False)
        self.putStatus(StatusO)
        StatusO = Status(17, "TestPoint2", True, False)
        self.putStatus(StatusO)
        StatusO = Status(18, "TestPoint3", True, False)
        self.putStatus(StatusO)

        return