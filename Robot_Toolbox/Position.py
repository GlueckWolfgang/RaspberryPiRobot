# -*- coding: utf-8 -*-
###############################################################################
# Class of Position
# Version:  2016.02.29
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

    def __str__(self):
        nachricht = "Class position"
        return nachricht
