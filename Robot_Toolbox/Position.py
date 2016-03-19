# -*- coding: utf-8 -*-
###############################################################################
# Class of Position
# Version:  2016.03.19
#
# x, y      The coordinates of the position
# disabled  Position is temporarily not available
# done      Tag for search algorithm to memorize "already done"
#
###############################################################################


class Position:
    def __init__(self, x, y):
        self.color = "#000000"
        self.disabledColor = "#FF0000"
        self.r = 2.5
        self.disabledR = 7.5
        self.x = x
        self.y = y
        self.disabled = False
        self.done = None
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
