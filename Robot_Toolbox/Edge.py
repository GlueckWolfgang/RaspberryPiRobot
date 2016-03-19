# -*- coding: utf-8 -*-
###############################################################################
# Class of Edge
# Version:  2016.03.16
#
# fromP          from position
# toP            to position
# weight         distance in cm of |x-x'| or |y-y'| for x <> x' or y <> y'
# relativeAngle  Realtive angle of fromP to toP (north = 0 degrees)
#
###############################################################################


class Edge:
    def __init__(self, fromP, toP, weight):

        self.fromP = fromP
        self.toP = toP
        self.weight = weight
        self.relativeAngle = 0.0

    def __str__(self):
        nachricht = "Class edge"
        return nachricht