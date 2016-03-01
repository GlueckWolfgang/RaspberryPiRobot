# -*- coding: utf-8 -*-
###############################################################################
# Class of PositionL
# Version:  2016.02.29
#
#
###############################################################################
import math
from Robot_Toolbox.Position import *
from Robot_Toolbox.Door import *
from Robot_Toolbox.Room import *
from Robot_Toolbox.Corridor import *


class PositionL:
    def __init__(self):
        self.list = []
        self.dw = 38.0    # wall distance

    def generatePositions(self, Relations, Region, Class):
        result = []
        Relations.getRegionsByClass(Region, Class, result)
        for i in range(0, len(result)):
            R = result[i]
            if isinstance(R, Door):
                if R.widthM < R.heightM:
                    # door direction is N/S
                    y = R.yM
                    x = R.xM - R.widthM / 2 - self.dw
                    position = Position(round(x), y)
                    self.list.append(position)

                    x = R.xM + R.widthM / 2 + self.dw
                    position = Position(round(x), y)
                    self.list.append(position)
                else:
                    # door direction is W/E
                    x = R.xM

                    y = R.yM - R.heightM / 2 - self.dw
                    position = Position(x, round(y))
                    self.list.append(position)

                    y = R.yM + R.heightM / 2 + self.dw
                    position = Position(x, round(y))
                    self.list.append(position)

            elif isinstance(R, Room):
                pass
            elif isinstance(R, Corridor):
                pass
        return

    def transformPositionsToCanvasCircle(self, scale, positions):
        result = []
        for i in range(0, len(positions.list)):
            region = positions.list[i]
            result.append([region.color,
                           round(region.x / scale),
                           round(region.y / scale),
                           round(region.r / scale), 0, 2 * math.pi])
        return result
