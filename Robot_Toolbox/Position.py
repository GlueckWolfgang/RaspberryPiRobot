# -*- coding: utf-8 -*-
###############################################################################
# Class of Position
# Version:  2016.03.08
#
# x, y      the coordinates of the position
#
###############################################################################


class Position:
    def __init__(self, x, y):
        self.color = "#000000"
        self.r = 2.5
        self.x = x
        self.y = y
        self.inRegion = None
        self.localNorthOf = None
        self.localSouthOf = None
        self.localWestOf = None
        self.localEastOf = None

        self.localNorthSideOf = None
        self.localSouthSideOf = None
        self.localWestSideOf = None
        self.localEastSideOf = None

    def __str__(self):
        nachricht = "Class position"
        return nachricht
