# -*- coding: utf-8 -*-
###############################################################################
# Class of MeasuredValue
# Version: 2015.12.22
#
# mvNumber      = 1..n
# mvType        = ("Actual value", "Smoothed value")
# mvDimension   = ("V", "A", "Degrees", cm, m)
# mvDescription = ("Battery 7.2V:", "Arduino 5V:", "Motor 1 current:"...)
# mvUlAlert     = (True, False) True if Message is an alert for alert list
# mvLlAlert     = (True, False) True if Message is an alert for alert list
#                 must be the same text as received from Arduino!
###############################################################################


class MeasuredValue:

    def __init__(self, mvNumber, mvType, mvDimension, mvDescription, mvUlAlert, mvLlAlert):
        self.mvNumber = mvNumber
        self.mvDescription = mvDescription
        self.mvType = mvType
        self.mvDimension = mvDimension
        self.value = 0
        self.Ul = 0
        self.Ll = 0
        self.UlAbove = False
        self.UlAboveDescription = "Upper limit exceeded"
        self.UlAboveAlert = mvUlAlert
        self.LlBelow = False
        self.LlBelowDescription = "Lower limit exceeded"
        self.LlBelowAlert = mvLlAlert

    def __str__(self):
        nachricht = "Parameters for a measured value"
        return nachricht