# -*- coding: utf-8 -*-
###############################################################################
# Class of Status
# Version: 2015.12.22
#
# stNumber      = 1..n
# stDescription = ("Turn slow 45 right!",..)
#                 must be the same text as received from Arduino!
# stAlert       = (True, False) True if status is an alert for alert list
###############################################################################


class Status:
    def __init__(self, stNumber, stDescription, stAlert):
        self.stNumber = stNumber
        self.stDescription = stDescription
        self.stStatus = False
        self.stAlert = stAlert

    def __str__(self):
        nachricht = "Parameters for a status"
        return nachricht