# -*- coding: utf-8 -*-
###############################################################################
# Class of Alarm
# Version: 2016.01.07
# not yet tested!
#
# alDateTime        = Time stamp created in putValue
# all other parameters according to MeasuredValueL respectively StatusL
# alDescription     = Description text
# alType            = "ST", "MV"
# alNumber          = 0..n according to StatusL and MeasuredValueL
# alSubtype         = "UL", "LL", ""  for measured values only
# alStatus          = 0, 1
###############################################################################


class Alarm:
    def __init__(self, alDateTime, alDescription, alType, alNumber, alSubtype,
                       alStatus):

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
        self.alAcknowledged = False
        self.alDelete = False

    def __str__(self):
        nachricht = "Parameters for an alarm"
        return nachricht