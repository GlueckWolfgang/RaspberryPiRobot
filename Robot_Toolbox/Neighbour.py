# -*- coding: utf-8 -*-
###############################################################################
# Class of Neighbour
# Version:  2016.02.20
#
# one or more parts of a region ("M", "L", "R") can have up to 4 neighbours
# a neighbour is docked either on north, south, west or east of the part
# Variant for dimension I, containing region is stored in north
#
###############################################################################


class Neighbour:
    def __init__(self, region, dPart=None, north=None, south=None, west=None, east=None):
        self.dPart = dPart
        self.region = region
        self.northN = north
        self.southN = south
        self.westN = west
        self.eastN = east

    def __str__(self):
        nachricht = "Class neighbour"
        return nachricht