# -*- coding: utf-8 -*-
###############################################################################
# Class of Edge
# Version:  2016.04.18
#
# fromP          from position
# toP            to position
# weight         distance in cm of |x-x'| or |y-y'| for x <> x' or y <> y'
# relativeAngle  Realtive angle of fromP to toP (north = 0 degrees)
# bearing        absolute compass angle to go
#
###############################################################################


class Edge:
    def __init__(self, fromP, toP, weight, angle, forward):

        self.fromP = fromP
        self.toP = toP
        self.forward = forward
        self.weight = weight
        self.relativeAngle = angle
        self.bearing = 0
        self.roadColor = "#000000"
        self.pathColor = "#FFFFFF"

    def __str__(self):
        nachricht = "Class edge"
        return nachricht