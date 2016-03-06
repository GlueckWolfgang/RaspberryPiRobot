# -*- coding: utf-8 -*-
###############################################################################
# Class of PositionL
# Version:  2016.03.06
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
            # Region
            R = result[i]
            # Relation
            Relation = Relations.getRelation(R)
            if isinstance(R, Door):
                if R.widthM < R.heightM:
                    # door direction is N/S
                    y = R.yM
                    x = R.xM - R.widthM / 2 - self.dw
                    position = Position(round(x), y)
                    # east
                    if Relation.eastN is not None:
                        position.inRegion = Relation.eastN
                        self.list.append(position)

                    x = R.xM + R.widthM / 2 + self.dw
                    position = Position(round(x), y)
                    # west
                    if Relation.westN is not None:
                        position.inRegion = Relation.westN
                        self.list.append(position)
                else:
                    # door direction is W/E
                    x = R.xM

                    y = R.yM - R.heightM / 2 - self.dw
                    position = Position(x, round(y))
                    # north
                    if Relation.northN is not None:
                        position.inRegion = Relation.northN
                        self.list.append(position)

                    y = R.yM + R.heightM / 2 + self.dw
                    position = Position(x, round(y))
                    # south
                    if Relation.southN is not None:
                        position.inRegion = Relation.southN
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
