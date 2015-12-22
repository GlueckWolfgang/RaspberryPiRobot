# -*- coding: utf-8 -*-
###############################################################################
# Class of Command
# Version: 2015.12.21
#
# coNumber      = 1..n
# coDescription = ("Stop!"..)
#                 must be the same text as sent to Arduino!
###############################################################################


class Command:
    def __init__(self, coNumber, coDescription):
        self.coNumber = coNumber
        self.coDescription = coDescription

    def __str__(self):
        nachricht = "Parameters for a command"
        return nachricht