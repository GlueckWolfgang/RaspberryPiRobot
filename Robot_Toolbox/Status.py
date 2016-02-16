# -*- coding: utf-8 -*-
###############################################################################
# Class of Status
# Version: 2015.02.16
#
# stNumber      = 1..n
# stDescription = ("Turn slow 45 right!",..)
#                 must be the same text as received from Arduino!
# stAlert       = (True, False) True if status is an alert for alert list
# stCg          = (True, False) True if status has komming/going character
###############################################################################


class Status:
    def __init__(self, stNumber, stDescription, stAlert, stCg):
        self.stNumber = stNumber
        self.stDescription = stDescription
        self.stStatus = 0
        self.stAlert = stAlert
        self.stCg = stCg

    def __str__(self):
        nachricht = "Parameters for a status"
        return nachricht