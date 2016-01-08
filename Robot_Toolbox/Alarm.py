# -*- coding: utf-8 -*-
###############################################################################
# Class of Alarm
# Version: 2016.01.08
#
# alDateTime        = Time stamp created in putValue
# all other parameters according to MeasuredValueL respectively StatusL
# alDescription     = Description text
# alType            = "ST", "MV"
# alNumber          = 0..n mvNumber or stNumber
# alSubtype         = "UL", "LL", ""  for measured values only
# alStatus          = 0, 1
# alDtype           = "Integer", "Float"
# alValue...........= measured value according to alDtype
###############################################################################


class Alarm:
    def __init__(self, alDateTime, alDescription, alType, alNumber, alSubtype,
                       alStatus, alDtype, alValue):

        self.alDateTime = alDateTime
        self.alDescription = alDescription
        self.alStatusTextC = "C"
        self.alStatusTextG = "G"
        self.alAcknowledgeTextFalse = "A"
        self.alAcknowledgeTextTrue = ""
        self.alType = alType
        self.alNumber = alNumber
        self.stSubType = alSubtype
        self.alStatus = alStatus
        self.alDtype = alDtype
        self.alValue = alValue
        self.alAcknowledged = False
        self.alDelete = False

    def __str__(self):
        nachricht = "Parameters for an alarm"
        return nachricht