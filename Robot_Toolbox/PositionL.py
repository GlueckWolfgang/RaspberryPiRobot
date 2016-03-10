# -*- coding: utf-8 -*-
###############################################################################
# Class of PositionL
# Version:  2016.03.10
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
                        position.localWestSideOf = Relation.eastN
                        self.list.append(position)

                    x = R.xM + R.widthM / 2 + self.dw
                    position = Position(round(x), y)
                    # west
                    if Relation.westN is not None:
                        position.inRegion = Relation.westN
                        position.localEastSideOf = Relation.westN
                        self.list.append(position)
                else:
                    # door direction is W/E
                    x = R.xM

                    y = R.yM - R.heightM / 2 - self.dw
                    position = Position(x, round(y))
                    # north
                    if Relation.northN is not None:
                        position.inRegion = Relation.northN
                        position.localSouthSideOf = Relation.northN
                        self.list.append(position)

                    y = R.yM + R.heightM / 2 + self.dw
                    position = Position(x, round(y))
                    # south
                    if Relation.southN is not None:
                        position.inRegion = Relation.southN
                        position.localNorthSideOf = Relation.southN
                        self.list.append(position)

            elif isinstance(R, Room):
                # R = result[i]
                # get positions from self.list
                positions = []
                for j in range(0, len(self.list)):
                    if self.list[j].inRegion == R:
                        # position for R found
                        positions.append(self.list[j])

                if len(positions) == 1:
                    # R = result[i]
                    # Relation = Relations.getRelation(R)
                    # search for a neighbour region with class Room
                    neighbourR = None
                    if isinstance(Relation.northN, Room):
                        neighbourR = Relation.northN
                    elif isinstance(Relation.southN, Room):
                        neighbourR = Relation.southN
                    elif isinstance(Relation.westN, Room):
                        neighbourR = Relation.westN
                    elif isinstance(Relation.eastN, Room):
                        neighbourR = Relation.eastN
                    if neighbourR is not None:
                        # neighbour room found
                        # search for positions in neighbour room
                        for k in range(0, len(self.list)):
                            if self.list[k].inRegion == neighbourR:
                                # position for neighbour found
                                positions.append(self.list[k])

                if len(positions) == 2:
                    pos = None
                    # 2 positions for R or R and neighbour found
                    if positions[0].localNorthSideOf is not None\
                    and positions[1].localWestSideOf is not None:
                        # N/W
                        x = positions[0].x
                        y = positions[1].y
                        pos = Position(x, y)

                    elif positions[0].localWestSideOf is not None\
                    and positions[1].localNorthSideOf is not None:
                        # W/N
                        x = positions[1].x
                        y = positions[0].y
                        pos = Position(x, y)

                    elif positions[0].localNorthSideOf is not None\
                    and positions[1].localEastSideOf is not None:
                        # N/E
                        x = positions[0].x
                        y = positions[1].y
                        pos = Position(x, y)

                    elif positions[0].localEastSideOf is not None\
                    and positions[1].localNorthSideOf is not None:
                        # E/N
                        x = positions[1].x
                        y = positions[0].y
                        pos = Position(x, y)

                    elif positions[0].localSouthSideOf is not None\
                    and positions[1].localWestSideOf is not None:
                        # S/W
                        x = positions[0].x
                        y = positions[1].y
                        pos = Position(x, y)

                    elif positions[0].localWestSideOf is not None\
                    and positions[1].localSouthSideOf is not None:
                        # W/S
                        x = positions[1].x
                        y = positions[0].y
                        pos = Position(x, y)

                    elif positions[0].localSouthSideOf is not None\
                    and positions[1].localEastSideOf is not None:
                        # S/E
                        x = positions[0].x
                        y = positions[1].y
                        pos = Position(x, y)

                    elif positions[0].localEastSideOf is not None\
                    and positions[1].localSouthSideOf is not None:
                        # E/S
                        x = positions[1].x
                        y = positions[0].y
                        pos = Position(x, y)

                    if pos is not None:
                        # select pos.inRegion *******************************
                        if  (x >= R.xM - round(R.widthM / 2))\
                        and (x <= R.xM + round(R.widthM / 2))\
                        and (y >= R.yM - round(R.heightM / 2))\
                        and (y <= R.yM + round(R.heightM / 2)):
                            pos.inRegion = R
                        else:
                            pos.inRegion = neighbourR
                        self.list.append(pos)

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
