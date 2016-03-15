# -*- coding: utf-8 -*-
###############################################################################
# Class of PositionL
# Version:  2016.03.15
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
        self.dwr = 61.0    # wall distance room(42cm furniture + 19cm Robot)
        self.dwc = 30.0    # wall distance corridor (30 cm Robot)

    def generatePositions(self, Relations, Region, Class):
        result = []
        Relations.getRegionsByClass(Region, Class, result)

        if Class == Door:
            # *****************************************************************
            for i in range(0, len(result)):
                # Region
                R = result[i]
                if isinstance(R, Door):
                    # Relation
                    Relation = Relations.getRelation(R)

                    if R.widthM < R.heightM:

                        # door direction is N/S
                        y = R.yM
                        x = R.xM + round(R.widthM / 2) + self.dwr
                        position = Position(x, y)
                        # east
                        if Relation.eastN is not None:
                            position.inRegion = Relation.eastN
                            position.localWestSideOf = Relation.eastN
                            if isinstance(position.inRegion, Corridor):
                                position.x = R.xM + round(R.widthM / 2) + self.dwc
                            self.list.append(position)

                        x = R.xM - round(R.widthM / 2) - self.dwr
                        position = Position(x, y)
                        # west
                        if Relation.westN is not None:
                            position.inRegion = Relation.westN
                            position.localEastSideOf = Relation.westN
                            if isinstance(position.inRegion, Corridor):
                                position.x = R.xM - round(R.widthM / 2) - self.dwc
                            self.list.append(position)
                    else:
                        # door direction is W/E
                        x = R.xM

                        y = R.yM - round(R.heightM / 2) - self.dwr
                        position = Position(x, y)
                        # north
                        if Relation.northN is not None:
                            position.inRegion = Relation.northN
                            position.localSouthSideOf = Relation.northN
                            if isinstance(position.inRegion, Corridor):
                                position.y = R.yM - round(R.heightM / 2) - self.dwc
                            self.list.append(position)

                        y = R.yM + round(R.heightM / 2) + self.dwr
                        position = Position(x, y)
                        # south
                        if Relation.southN is not None:
                            position.inRegion = Relation.southN
                            position.localNorthSideOf = Relation.southN
                            if isinstance(position.inRegion, Corridor):
                                position.y = R.yM + round(R.heightM / 2) + self.dwc
                            self.list.append(position)

        elif Class == Room:
            for i in range(0, len(result)):
                # Region
                R = result[i]
                if isinstance(R, Room):
                    # Relation
                    Relation = Relations.getRelation(R)
                    # *************************************************************
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

                        if len(positions) > 2:
                            # Region with more than 1 point found
                            # break (will be part of other algorithms)
                            positions = []

                    if len(positions) == 2:
                        pos = None
                        # 2 positions for R or R and neighbour found
                        if(positions[0].localNorthSideOf is not None
                        and positions[1].localWestSideOf is not None)\
                        or(positions[0].localSouthSideOf is not None
                        and positions[1].localEastSideOf is not None)\
                        or(positions[0].localNorthSideOf is not None
                        and positions[1].localEastSideOf is not None)\
                        or(positions[0].localSouthSideOf is not None
                        and positions[1].localWestSideOf is not None):
                            # N/W, S/E, N/E, S/W
                            x = positions[0].x
                            y = positions[1].y
                            pos = Position(x, y)

                        elif (positions[0].localWestSideOf is not None
                        and positions[1].localNorthSideOf is not None)\
                        or(positions[0].localEastSideOf is not None
                        and positions[1].localSouthSideOf is not None)\
                        or(positions[0].localEastSideOf is not None
                        and positions[1].localNorthSideOf is not None)\
                        or(positions[0].localWestSideOf is not None
                        and positions[1].localSouthSideOf is not None):
                            # W/N, E/S, E/N, W/S
                            x = positions[1].x
                            y = positions[0].y
                            pos = Position(x, y)

                        if pos is not None:
                            # select pos.inRegion *****************************
                            if  (x >= R.xM - round(R.widthM / 2))\
                            and (x <= R.xM + round(R.widthM / 2))\
                            and (y >= R.yM - round(R.heightM / 2))\
                            and (y <= R.yM + round(R.heightM / 2)):
                                pos.inRegion = R
                            else:
                                pos.inRegion = neighbourR
                            self.list.append(pos)

            # generate navpoint relations "localDirectionOf"  neigbour regions
            # for room parts only
            #**********************************************************

            for j in range(0, len(result)):
                # Region
                R = result[j]
                if isinstance(R, Room):
                    # Relation
                    Relation = Relations.getRelation(R)

                    # selected region is a room
                    for k in range(0, len(self.list)):
                        if self.list[k].inRegion == R:
                            # for all own navpoints
                            # if neighbour is a room too only
                            if isinstance(Relation.northN, Room):
                                self.list[k].localSouthOf = Relation.northN

                            if isinstance(Relation.southN, Room):
                                self.list[k].localNorthOf = Relation.southN

                            if isinstance(Relation.westN, Room):
                                self.list[k].localEastOf = Relation.westN

                            if isinstance(Relation.eastN, Room):
                                self.list[k].localWestOf = Relation.eastN

            # generate additional navpoints between room parts (N/S, W/E)
            # *********************************************************
            for j in range(0, len(result)):
                # Region
                R = result[j]
                if isinstance(R, Room):
                    # Relation
                    Relation = Relations.getRelation(R)
                    positions = []
                    for k in range(0, len(self.list)):
                        if self.list[k].inRegion == R:
                            # position for R found
                            positions.append(self.list[k])
                    if len(positions) == 1:
                        # R = result[i]
                        # Relation = Relations.getRelation(R)
                        # search for a neighbour region with class Room
                        neighbourR = None
                        if isinstance(Relation.westN, Room):
                            neighbourR = Relation.westN
                        elif isinstance(Relation.eastN, Room):
                            neighbourR = Relation.eastN
                        elif isinstance(Relation.northN, Room):
                            neighbourR = Relation.northN
                        elif isinstance(Relation.southN, Room):
                            neighbourR = Relation.southN

                        if neighbourR is not None:
                            # neighbour room found
                            # search for positions in neighbour room
                            for l in range(0, len(self.list)):
                                if self.list[l].inRegion == neighbourR:
                                    # position for neighbour found
                                    positions.append(self.list[l])

                            if len(positions) > 1:
                                # find closest to the first point
                                k = 1
                                dx = positions[0].x - positions[1].x
                                if dx < 0:
                                    dx = dx * - 1
                                dy = positions[0].y - positions[1].y
                                if dy < 0:
                                    dy = dy * - 1
                                if (dx == 0) or (dy == 0):
                                    # point already on line for x or y
                                    positions = []
                                else:
                                    for n in range(2, len(positions)):
                                        dxl = positions[0].x - positions[n].x
                                        if dxl < 0:
                                            dxl = dxl * - 1
                                        dyl = positions[0].y - positions[n].y
                                        if dyl < 0:
                                            dyl = dyl * - 1

                                        if  (dxl < dx)\
                                        or (dyl < dy):
                                            # closer point found
                                            if (dx == 0) or (dy == 0):
                                                # point already on line for x or y
                                                positions = []
                                                break
                                            dx = dxl
                                            dy = dyl
                                            k = n
                                    if len(positions) > 0:
                                        positionl = []
                                        positionl.append(positions[0])
                                        positionl.append(positions[k])
                                        positions = positionl

                                        # create new navpoint
                                        pos = None
                                        pos1 = None
                                        pos2 = None
                                        if positions[0].localSouthOf is not None\
                                        and positions[1].localNorthOf is not None:
                                            # Variant a)
                                            y = positions[1].y
                                            x = positions[0].x
                                            # target point
                                            pos1 = Position(x, y)
                                            pos1.inRegion = neighbourR
                                            y = positions[0].y
                                            x = positions[1].x
                                            # alternative point
                                            pos2 = Position(x, y)
                                            pos2.inRegion = R
                                            # create reference area of target point
                                            rA = neighbourR
                                            rA.widthM = rA.widthM - 2 * self.dwr
                                            rA.heightM = rA.heightM - 2 * self.dwr

                                        elif positions[0].localNorthOf is not None\
                                        and positions[1].localSouthOf is not None:
                                            # variant b)
                                            x = positions[1].x
                                            y = positions[0].y
                                            # target point
                                            pos1 = Position(x, y)
                                            pos1.inRegion = R
                                            x = positions[0].x
                                            y = positions[1].y
                                            # alternative point
                                            pos2 = Position(x, y)
                                            pos2.inRegion = neighbourR
                                            # create reference area of target point
                                            rA = R
                                            rA.widthM = rA.widthM - 2 * self.dwr
                                            rA.heightM = rA.heightM - 2 * self.dwr

                                        elif (positions[0].localEastOf is not None\
                                        and positions[1].localWestOf is not None):
                                            # variant c)
                                            x = positions[1].x
                                            y = positions[0].y
                                            # target point
                                            pos1 = Position(x, y)
                                            pos1.inRegion = neighbourR
                                            x = positions[0].x
                                            y = positions[1].y
                                            # alternative point
                                            pos2 = Position(x, y)
                                            pos2.inRegion = R
                                            # create reference area for target point
                                            rA = neighbourR
                                            rA.widthM = rA.widthM - 2 * self.dwr
                                            rA.heightM = rA.heightM - 2 * self.dwr

                                        elif positions[0].localWestOf is not None\
                                        and positions[1].localEastOf is not None:
                                            # Variant d)
                                            y = positions[1].y
                                            x = positions[0].x
                                            # target point
                                            pos1 = Position(x, y)
                                            pos1.inRegion = R
                                            y = positions[0].y
                                            x = positions[1].x
                                            # alternative point
                                            pos2 = Position(x, y)
                                            pos2.inRegion = neighbourR
                                            # create reference area for target point
                                            rA = R
                                            rA.widthM = rA.widthM - 2 * self.dwr
                                            rA.heightM = rA.heightM - 2 * self.dwr


                                        if  (pos1.x >= (rA.xM - round(rA.widthM / 2)))\
                                        and (pos1.x <= (rA.xM + round(rA.widthM / 2)))\
                                        and (pos1.y >= (rA.yM - round(rA.heightM / 2)))\
                                        and (pos1.y <= (rA.yM + round(rA.heightM / 2))):
                                            # pos1 is the new navpoint
                                            pos = pos1
                                        else:
                                            # pos2 is the new navpoint
                                            pos = pos2
                                        # put new navpoint in position list
                                        self.list.append(pos)

        elif Class == Corridor:
        # *********************************************************************
            for i in range(0, len(result)):
                # Region
                R = result[i]
                if isinstance(R, Corridor):
                    # Relation
                    Relation = Relations.getRelation(R)
                    positions = []
                    for j in range(0, len(self.list)):
                        if self.list[j].inRegion == R:
                            # position for R found
                            positions.append(self.list[j])

                    if len(positions) == 1:
                        # R = result[i]
                        # Relation = Relations.getRelation(R)
                        # search for a neighbour region with class Corridor
                        neighbourR = None

                        if isinstance(Relation.westN, Corridor):
                            neighbourR = Relation.westN
                        elif isinstance(Relation.eastN, Corridor):
                            neighbourR = Relation.eastN
                        elif isinstance(Relation.northN, Corridor):
                            neighbourR = Relation.northN
                        elif isinstance(Relation.southN, Corridor):
                            neighbourR = Relation.southN
                        if neighbourR is not None:
                            # neighbour corridor found
                            # search for positions in neighbour corridor
                            for k in range(0, len(self.list)):
                                if self.list[k].inRegion == neighbourR:
                                    # position for neighbour found
                                    positions.append(self.list[k])

                        if len(positions) > 2:
                            # Region with more than 1 point found
                            # break (will be part of other algorithms)
                            positions = []

                    if len(positions) == 2:
                        pos = None
                        # 2 positions for R or R and neighbour found
                        if(positions[0].localNorthSideOf is not None
                        and positions[1].localWestSideOf is not None)\
                        or(positions[0].localSouthSideOf is not None
                        and positions[1].localEastSideOf is not None)\
                        or(positions[0].localNorthSideOf is not None
                        and positions[1].localEastSideOf is not None)\
                        or(positions[0].localSouthSideOf is not None
                        and positions[1].localWestSideOf is not None):
                            # N/W, S/E, N/E, S/W
                            x = positions[0].x
                            y = positions[1].y
                            pos = Position(x, y)

                        elif (positions[0].localWestSideOf is not None
                        and positions[1].localNorthSideOf is not None)\
                        or(positions[0].localEastSideOf is not None
                        and positions[1].localSouthSideOf is not None)\
                        or(positions[0].localEastSideOf is not None
                        and positions[1].localNorthSideOf is not None)\
                        or(positions[0].localWestSideOf is not None
                        and positions[1].localSouthSideOf is not None):
                            # W/N, E/S, E/N, W/S
                            x = positions[1].x
                            y = positions[0].y
                            pos = Position(x, y)


                        if pos is not None:
                            # select pos.inRegion *****************************
                            if  (x >= R.xM - round(R.widthM / 2))\
                            and (x <= R.xM + round(R.widthM / 2))\
                            and (y >= R.yM - round(R.heightM / 2))\
                            and (y <= R.yM + round(R.heightM / 2)):
                                pos.inRegion = R
                            else:
                                pos.inRegion = neighbourR
                            self.list.append(pos)

            # generate navpoint relations "localDirectionOf"  neigbour regions
            # for corrdidor parts only
            # *****************************************************************
            for i in range(0, len(result)):
                # Region
                R = result[i]
                if isinstance(R, Corridor):
                    # Relation
                    Relation = Relations.getRelation(R)
                    # selected region is a corridor
                    for j in range(0, len(self.list)):
                        if self.list[j].inRegion == R:
                            # for all own navpoints
                            # if neighbour is a corridor too only
                            if isinstance(Relation.northN, Corridor):
                                self.list[j].localSouthOf = Relation.northN

                            if isinstance(Relation.southN, Corridor):
                                self.list[j].localNorthOf = Relation.southN

                            if isinstance(Relation.westN, Corridor):
                                self.list[j].localEastOf = Relation.westN

                            if isinstance(Relation.eastN, Corridor):
                                self.list[j].localWestOf = Relation.eastN


            # generate additional navpoints between corridor parts (N/S, W/E)
            # *****************************************************************
            for j in range(0, len(result)):
                # Region
                R = result[j]
                if isinstance(R, Corridor):
                    # Relation
                    Relation = Relations.getRelation(R)
                    positions = []
                    for k in range(0, len(self.list)):
                        if self.list[k].inRegion == R:
                            # position for R found
                            positions.append(self.list[k])
                    if len(positions) == 1:
                        # R = result[j]
                        # Relation = Relations.getRelation(R)
                        # search for a neighbour region with class Room
                        neighbourR = None

                        if isinstance(Relation.westN, Corridor):
                            neighbourR = Relation.westN
                        elif isinstance(Relation.eastN, Corridor):
                            neighbourR = Relation.eastN
                        elif isinstance(Relation.northN, Corridor):
                            neighbourR = Relation.northN
                        elif isinstance(Relation.southN, Corridor):
                            neighbourR = Relation.southN
                        if neighbourR is not None:
                            # neighbour corridor found
                            # search for positions in neighbour corridor
                            for l in range(0, len(self.list)):
                                if self.list[l].inRegion == neighbourR:
                                    # position for neighbour found
                                    positions.append(self.list[l])

                            if len(positions) > 1:
                                # find closest to the first point
                                k = 1
                                dx = positions[0].x - positions[1].x
                                if dx < 0:
                                    dx = dx * - 1
                                dy = positions[0].y - positions[1].y
                                if dy < 0:
                                    dy = dy * - 1
                                if (dx == 0) or (dy == 0):
                                    # point already on line for x or y
                                    positions = []
                                else:
                                    for n in range(2, len(positions)):
                                        dxl = positions[0].x - positions[n].x
                                        if dxl < 0:
                                            dxl = dxl * - 1
                                        dyl = positions[0].y - positions[n].y
                                        if dyl < 0:
                                            dyl = dyl * - 1

                                        if  (dxl < dx)\
                                        or (dyl < dy):
                                            # closer point found
                                            if (dx == 0) or (dy == 0):
                                                # point already on line for x or y
                                                positions = []
                                                break
                                            dx = dxl
                                            dy = dyl
                                            k = n

                                    if len(positions) > 0:
                                        positionl = []
                                        positionl.append(positions[0])
                                        positionl.append(positions[k])
                                        positions = positionl

                                        # create new navpoint
                                        pos = None
                                        pos1 = None
                                        pos2 = None
                                        if positions[0].localSouthOf is not None\
                                        and positions[1].localNorthOf is not None:
                                            # Variant a)
                                            y = positions[1].y
                                            x = positions[0].x
                                            # target point
                                            pos1 = Position(x, y)
                                            pos1.inRegion = neighbourR
                                            y = positions[0].y
                                            x = positions[1].x
                                            # alternative point
                                            pos2 = Position(x, y)
                                            pos2.inRegion = R
                                            # create reference area of target point
                                            rA = neighbourR
                                            rA.widthM = rA.widthM - 2 * self.dwc
                                            rA.heightM = rA.heightM - 2 * self.dwc

                                        elif positions[0].localNorthOf is not None\
                                        and positions[1].localSouthOf is not None:
                                            # variant b)
                                            x = positions[1].x
                                            y = positions[0].y
                                            # target point
                                            pos1 = Position(x, y)
                                            pos1.inRegion = R
                                            x = positions[0].x
                                            y = positions[1].y
                                            # alternative point
                                            pos2 = Position(x, y)
                                            pos2.inRegion = neighbourR
                                            # create reference area of target point
                                            rA = R
                                            rA.widthM = rA.widthM - 2 * self.dwc
                                            rA.heightM = rA.heightM - 2 * self.dwc

                                        elif (positions[0].localEastOf is not None\
                                        and positions[1].localWestOf is not None):
                                            # variant c)
                                            x = positions[1].x
                                            y = positions[0].y
                                            # target point
                                            pos1 = Position(x, y)
                                            pos1.inRegion = neighbourR
                                            x = positions[0].x
                                            y = positions[1].y
                                            # alternative point
                                            pos2 = Position(x, y)
                                            pos2.inRegion = R
                                            # create reference area for target point
                                            rA = neighbourR
                                            rA.widthM = rA.widthM - 2 * self.dwc
                                            rA.heightM = rA.heightM - 2 * self.dwc

                                        elif positions[0].localWestOf is not None\
                                        and positions[1].localEastOf is not None:
                                            # Variant d)
                                            y = positions[1].y
                                            x = positions[0].x
                                            # target point
                                            pos1 = Position(x, y)
                                            pos1.inRegion = R
                                            y = positions[0].y
                                            x = positions[1].x
                                            # alternative point
                                            pos2 = Position(x, y)
                                            pos2.inRegion = neighbourR
                                            # create reference area for target point
                                            rA = R
                                            rA.widthM = rA.widthM - 2 * self.dwc
                                            rA.heightM = rA.heightM - 2 * self.dwc

                                        # select right position from pos1, pos2
                                        if pos1 is not None and pos2 is not None:


                                            if  (pos1.x >= (rA.xM - round(rA.widthM / 2)))\
                                            and (pos1.x <= (rA.xM + round(rA.widthM / 2)))\
                                            and (pos1.y >= (rA.yM - round(rA.heightM / 2)))\
                                            and (pos1.y <= (rA.yM + round(rA.heightM / 2))):
                                                # pos1 is the new navpoint
                                                pos = pos1
                                            else:
                                                # pos2 is the new navpoint
                                                pos = pos2
                                            # put new navpoint in position list
                                            self.list.append(pos)
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
