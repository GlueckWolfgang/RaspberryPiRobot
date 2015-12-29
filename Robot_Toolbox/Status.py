# -*- coding: utf-8 -*-
###############################################################################
# Class of Status
# Version: 2015.12.29
#
# stNumber      = 1..n
# stDescription = ("Turn slow 45 right!",..)
#                 must be the same text as received from Arduino!
# stAlert       = (True, False) True if status is an alert for alert list
# stKg          = (True, False) True if status has komming/going character
###############################################################################


class Status:
    def __init__(self, stNumber, stDescription, stAlert, stKg):
        self.stNumber = stNumber
        self.stDescription = stDescription
        self.stStatus = False
        self.stAlert = stAlert
        self.stKg = stKg

    def __str__(self):
        nachricht = "Parameters for a status"
        return nachricht