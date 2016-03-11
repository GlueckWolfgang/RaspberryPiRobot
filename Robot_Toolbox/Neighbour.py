# -*- coding: utf-8 -*-
###############################################################################
# Class of Neighbour
# Version:  2016.02.29
#
# A region or Part of a region ("M") can have up to 4 neighbours
# a neighbour is docked either on north, south, west or east of the region
# hierachical dependencies will be put into inRegion
#
###############################################################################


class Neighbour:
    def __init__(self, region, innerRegion, north=None, south=None, west=None, east=None):
        self.region = region
        self.innerRegion = innerRegion
        self.northN = north
        self.southN = south
        self.westN = west
        self.eastN = east

    def __str__(self):
        nachricht = "Class neighbour"
        return nachricht