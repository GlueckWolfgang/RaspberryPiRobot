# -*- coding: utf-8 -*-
###############################################################################
# Class of Alarm
# Version: 2016.01.26
#
# alDateTime        = str(Time stamp) created in putValue
# all other parameters according to MeasuredValueL respectively StatusL
# alDescription     = Description text
# alType            = "ST", "MV"
# alNumber          = str(0..n mvNumber or stNumber)
# alSubtype         = "UL", "LL", ""  for measured values only
# alStatus          = str (0, 1)
# alDtype           = "Integer", "Float"
# alValue...........= measured value according to alDtype
# alDimension       = "V", "A", "cm"
###############################################################################


class Alarm:
    def __init__(self, alDateTime, alDescription, alType, alNumber, alSubType,
                       alStatus, alDtype, alValue, alDimension):

        self.alDateTime = alDateTime
        self.alDescription = alDescription
        self.alStatusTextC = "C"
        self.alStatusTextG = "G"
        self.alAcknowledgeTextFalse = "A"
        self.alAcknowledgeTextTrue = ""
        self.alType = alType
        self.alNumber = alNumber
        self.alSubType = alSubType
        self.alStatus = alStatus
        self.alDtype = alDtype
        self.alValue = alValue
        self.alDimension = alDimension
        self.alAcknowledged = False
        self.alDelete = False

    def __str__(self):
        nachricht = "Parameters for an alarm"
        return nachricht