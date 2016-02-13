# -*- coding: utf-8 -*-
###############################################################################
# Class of Measured Value List
# Version:  2016.02.13
###############################################################################
from Robot_Toolbox.MeasuredValue import *
from Robot_Toolbox.Alarm import *
from Robot_Toolbox.Audio import *
import datetime
import re
import codecs
from bs4 import BeautifulSoup as Soup


class MeasuredValueL:

    def __init__(self):
        self.list = []                      # List of measured value objects
        self.template_M = dict()            # template for dictionary of Panel.html with all id= "M_...)

        def get_ids(html_file, regular_expression):
            ids = dict()
            with codecs.open(html_file, 'r', encoding='utf-8', errors='ignore') as fh:
                soup = Soup(fh, 'html.parser')
                for element in soup.find_all('td', id=re.compile(regular_expression)):
                    idi = element.get('id')
                    if idi:
                        ids[idi] = "?"
                        if idi.endswith("_V"):
                            # add Cv
                            idi = idi.replace("_V", "_Cv")
                            ids[idi] = "?"
            return ids

        # create dictionary
        self.template_M = get_ids("Robbi/Panel.html", r'[id="M_+"]')



    def __str__(self):
        nachricht = " List of measured values"
        return nachricht


    def getData(self, MQueue):
        for key in self.template_M:
            mvid = key.split("_")  # M, mvNo, code
            MV = self.getMeasuredValueByNumber(int(mvid[1]))
            if mvid[2] == "D":
                self.template_M[key] = MV.mvDescription
            elif mvid[2] == "Dim":
                self.template_M[key] = MV.mvDimension
            elif mvid[2] == "V":
                self.template_M[key] = str(MV.value)
            elif mvid[2] == "Cv":
                if MV.UlAbove == False\
                and MV.LlBelow == False:
                    self.template_M[key] = "black"
                elif MV.UlAbove == True:
                    self.template_M[key] = "red"
                elif MV.LlBelow == True:
                    self.template_M[key] = "yellow"
            elif mvid[2] == "Ul":
                self.template_M[key] = str(MV.Ul)
            elif mvid[2] == "Ll":
                self.template_M[key] = str(MV.Ll)
        return self.template_M


    def putMeasuredValue(self, measuredValue):
        self.list.append(measuredValue)     # index = mvNumber
        return

    def putValue(self, string, AQueue, LQueue, MQueue):
        audioMessage = None
        separatedString = string.split(":")   # MV name, value
        MV = self.getMeasuredValueByName(separatedString[0])
        if MV is not None:
            separatedStringP = separatedString[1].split(" ")  # "", keyword, value
            separatedStringP[2] = separatedStringP[2].strip(" ")
            # print(separatedString, separatedStringP)
            if separatedStringP[1] == "V":
                if MV.mvDtype == "Integer":
                    MV.value = int(separatedStringP[2])
                elif MV.mvDtype == "Float":
                    MV.value = float(separatedStringP[2])

            elif separatedStringP[1] == "LL":
                if MV.mvDtype == "Integer":
                    MV.Ll = int(separatedStringP[2])
                elif MV.mvDtype == "Float":
                    MV.Ll = float(separatedStringP[2])

            elif separatedStringP[1] == "UL":
                if MV.mvDtype == "Integer":
                    MV.Ul = int(separatedStringP[2])
                elif MV.mvDtype == "Float":
                    MV.Ul = float(separatedStringP[2])

            elif separatedStringP[1] == "LL_Exceeded":
                if MV.LlBelow != int(separatedStringP[2]):
                    # print(separatedString[0], MV.LlBelow, separatedStringP[2])
                    # edge 0 to 1 or edge 1 to 0
                    MV.LlBelow = int(separatedStringP[2])
                    if MV.LlBelowAlert is True:
                        # generate audio message
                        audioMessage = Audio("MV",
                                              str(MV.mvNumber),
                                              True,
                                              str(MV.LlBelow),
                                              "2")
                        # generate alarm for alarm list
                        AlarmO = Alarm(str(datetime.datetime.now()),
                        MV.mvDescription + " " + MV.LlBelowDescription,
                        "MV",
                        str(MV.mvNumber),      # int 0..n
                        "LL",                  # Subtype
                        str(MV.LlBelow),       # int 0/1
                        MV.mvDtype,            # "Integer", "Float"
                        str(MV.Ll),            # Limit
                        str(MV.value),         # Value
                        MV.mvDimension)        # Dimension

                        LQueue.put(["L@", AlarmO])

            elif separatedStringP[1] == "UL_Exceeded":
                if MV.UlAbove != int(separatedStringP[2]):
                    # print(separatedString[0], MV.UlAbove, separatedStringP[2])
                    # edge 0 to 1 or edge 1 to 0
                    MV.UlAbove = int(separatedStringP[2])
                    if MV.UlAboveAlert is True:
                        # generate audio message
                        audioMessage = Audio("MV",
                                              str(MV.mvNumber),
                                              True,
                                              str(MV.UlAbove),
                                              "1")

                        # generate alarm for alarm list
                        AlarmO = Alarm(str(datetime.datetime.now()),
                        MV.mvDescription + " " + MV.UlAboveDescription,
                        "MV",
                        str(MV.mvNumber),      # int 0..n
                        "UL",                  # Subtype
                        str(MV.UlAbove),       # int 0/1
                        MV.mvDtype,            # "Integer", "Float"
                        str(MV.Ul),            # Limit
                        str(MV.value),         # Value
                        MV.mvDimension)        # Dimension

                        LQueue.put(["L@", AlarmO])
                        # AlarmList.putAlarm(AlarmO, MQueue)

        else:
            MQueue.put("I@Process status and measured value: Measured value not found: " + separatedString[0])

        if audioMessage is not None:
            AQueue.put(audioMessage)
        return

    def getMeasuredValueByNumber(self, mvNumber):
        if mvNumber < len(self.list):       # list must not be empty
            return self.list[mvNumber]
        else:
            return None

    def getMeasuredValueByName(self, mvName):
        for i in range(0, len(self.list)):  # list must not be empty
            if self.list[i].mvDescription == mvName:
                return self.list[i]
            else:
                continue
        return None

    def generateMeasuredValueList(self):
        # structure = Number, type, datatype, dimension, description text, ULAlert, LLAlert
        MValue = MeasuredValue(0, "Actual value", "Integer", "", "Version", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(1, "Actual value", "Integer", "cm", "EncLt", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(2, "Actual value", "Integer", "cm", "EncRt", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(3, "Actual value", "Float", "V", "Battery 9V", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(4, "Actual value", "Float", "V", "Battery 7V", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(5, "Actual value", "Float", "V", "Battery 5V", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(6, "Actual value", "Float", "V", "Arduino 5V", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(7, "Actual value", "Float", "A", "Motor1 current", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(8, "Actual value", "Float", "A", "Motor2 current", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(9, "Actual value", "Float", "A", "Motor3 current", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(10, "Actual value", "Float", "A", "Motor4 current", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(11, "Actual value", "Integer", "&#176;", "Roll", True,True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(12, "Actual value", "Integer", "&#176;", "Pitch", True, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(13, "Actual value", "Float", "&#176;", "Actual angle", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(14, "Actual value", "Float", "&#176;", "Turned angle", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(15, "Smoothed value", "Float", "&#176;", "Smoothed angle", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(16, "Actual value", "Integer", "cm", "Distance fleft", True, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(17, "Actual value", "Integer", "cm", "Distance fright", True, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(18, "Actual value", "Integer", "cm", "Distance bleft", True, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(19, "Actual value", "Integer", "cm", "Distance bright", True, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(20, "Actual value", "Integer", "cm", "Distance front", True, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(21, "Actual value", "Integer", "cm", "Distance up", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(22, "Actual value", "Integer", "cm", "Distance down", True, False)
        self.putMeasuredValue(MValue)

        return