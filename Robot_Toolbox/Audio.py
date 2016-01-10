# -*- coding: utf-8 -*-
###############################################################################
# Class of Audio
# Version: 2016.01.10
#
# aType               = "ST", "MV"
# aNumber.............= str(Number according to aType)
# aCG.................= True, False
# aValue..............= str(0 or 1)
# aCAudioNo...........= str(1 or 2)

###############################################################################


class Audio:
    def __init__(self, aType, aNumber, aCG, aValue, aCAudioNo):

        self.aType = aType
        self.aNumber = aNumber
        self.aCG = aCG
        self.aValue = aValue
        self.aCAudioNo = aCAudioNo

    def __str__(self):
        nachricht = "Parameters for an audio message"
        return nachricht