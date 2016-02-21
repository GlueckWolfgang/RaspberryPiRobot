# -*- coding: utf-8 -*-
###############################################################################
# Class of Neighbour
# Version:  2016.02.21
#
# one or more parts of a region ("M", "L", "R") can have up to 4 neighbours
# a neighbour is docked either on north, south, west or east of the part
# Variant for dimension I, containing region is stored in north
#
###############################################################################


class Neighbour:
    def __init__(self, region, dPart=None,
                north=None, dPartNorth=None,
                south=None, dPartSouth=None,
                west=None, dPartWest=None,
                east=None, dPartEast=None):
        self.dPart = dPart
        self.region = region
        self.northN = north
        self.dPartNorth = dPartNorth
        self.southN = south
        self.dPartSouth = dPartSouth
        self.westN = west
        self.dPartWest = dPartWest
        self.eastN = east
        self.dPartEast = dPartEast

    def __str__(self):
        nachricht = "Class neighbour"
        return nachricht