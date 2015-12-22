# -*- coding: utf-8 -*-
###############################################################################
# Class of Measured Value List
# Version:  2015.12.21
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
        MValue = MeasuredValue(0, "Actual value", "", "Version: ", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(1, "Actual value", "cm", "EncLt: ", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(2, "Actual value", "cm", "EncRt: ", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(3, "Actual value", "V", "Battery 9V: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(4, "Actual value", "V", "Battery 7V: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(5, "Actual value", "V", "Battery 5V: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(6, "Actual value", "V", "Arduino 5V: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(7, "Actual value", "A", "Motor1 current: ", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(8, "Actual value", "A", "Motor2 current: ", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(9, "Actual value", "A", "Motor3 current: ", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(10, "Actual value", "A", "Motor4 current: ", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(11, "Actual value", "Degrees", "Roll: ", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(12, "Actual value", "Degrees", "Pitch: ", True, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(13, "Actual value", "Degrees", "Actual angle: ", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(14, "Actual value", "Degrees", "Turned angle: ", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(15, "Smoothed value", "Degrees", "Smoothed angle: ", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(16, "Actual value", "cm", "Distance fleft: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(17, "Actual value", "cm", "Distance fright: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(18, "Actual value", "cm", "Distance bleft: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(19, "Actual value", "cm", "Distance bright: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(20, "Actual value", "cm", "Distance front: ", False, True)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(21, "Actual value", "cm", "Distance up: ", False, False)
        self.putMeasuredValue(MValue)
        MValue = MeasuredValue(22, "Actual value", "cm", "Distance down: ", False, True)
        self.putMeasuredValue(MValue)

        return
