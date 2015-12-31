# -*- coding: utf-8 -*-
###############################################################################
# Class of Measured Value List
# Version:  2015.12.29
###############################################################################
from Robot_Toolbox.MeasuredValue import *


class MeasuredValueL:

    def __init__(self):
        self.list = []                      # List of measured value objects

    def __str__(self):
        nachricht = " List of measured values"
        return nachricht

    def putMeasuredValue(self, measuredValue):
        self.list.append(measuredValue)     # index = mvNumber
        return

    def putValue(self, string):
        audioMessage = None
        separatedString = string.split(":")   # MV name, value
        MV = self.getMeasuredValueByName(separatedString[0])
        if MV is not None:
            separatedStringP = separatedString[1].split(" ")  # keyword, value
            separatedStringP[1] = separatedStringP[1].strip(" ")
            if separatedStringP[0] == "V":
                if MV.mvDtype == "Integer":
                    MV.value = int(separatedStringP[1])
                elif MV.mvDtype == "Float":
                    MV.value = float(separatedStringP[1])

                elif separatedStringP[0] == "LL":
                    if MV.mvDtype == "Integer":
                        MV.Ll = int(separatedStringP[1])
                    elif MV.mvDtype == "Float":
                        MV.Ll = float(separatedStringP[1])

                elif separatedStringP[0] == "UL":
                    if MV.mvDtype == "Integer":
                        MV.Ul = int(separatedStringP[1])
                    elif MV.mvDtype == "Float":
                        MV.Ul = float(separatedStringP[1])

                elif separatedStringP[0] == "LL_Exceeded":

                    if (MV.LlBelow == 0 and int(separatedStringP[1]) == 1)\
                    or (MV.LlBelow == 1 and int(separatedStringP[1]) == 0):
                        # edge 0 to 1 or edge 1 to 0
                        MV.LlBelow = int(separatedStringP[1])
                        if MV.mvAlert is True:
                            audioMessage = ["MV", str(MV.mvNumber),
                                                  MV.LlBelowAlert,
                                                  "",
                                                  str(MV.LlBelow),
                                                  "2"]

                elif separatedStringP[0] == "UL_Exceeded":
                    if (MV.UlAbove == 0 and int(separatedStringP[1]) == 1)\
                    or (MV.UlAbove == 1 and int(separatedStringP[1]) == 0):
                        # edge 0 to 1 or edge 1 to 0
                        MV.UlAbove = int(separatedStringP[1])
                        if MV.UlAboveAlert is True:
                            audioMessage = ["MV", str(MV.mvNumber),
                                                  MV.LlAboveAlert,
                                                  "",
                                                  str(MV.LlAbove),
                                                  "1"]

        else:
            print("Measured value not found: ", separatedString[0], "\n")
        return audioMessage

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
        MValue = MeasuredValue(11, "Actual value", "Integer", "Degrees", "Roll", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(12, "Actual value", "Integer", "Degrees", "Pitch", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(13, "Actual value", "Float", "Degrees", "Actual angle", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(14, "Actual value", "Float", "Degrees", "Turned angle", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(15, "Smoothed value", "Float", "Degrees", "Smoothed angle", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(16, "Actual value", "Integer", "cm", "Distance fleft", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(17, "Actual value", "Integer", "cm", "Distance fright", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(18, "Actual value", "Integer", "cm", "Distance bleft", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(19, "Actual value", "Integer", "cm", "Distance bright", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(20, "Actual value", "Integer", "cm", "Distance front", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(21, "Actual value", "Integer", "cm", "Distance up", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(22, "Actual value", "Integer", "cm", "Distance down", False, True)
        self.putMeasuredValue(MValue)

        return
