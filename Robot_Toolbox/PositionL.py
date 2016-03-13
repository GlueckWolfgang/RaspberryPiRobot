# -*- coding: utf-8 -*-
###############################################################################
# Class of PositionL
# Version:  2016.03.13
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
        self.dwc = 30.0    # wall distance corridor (34 cm Robot)

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

                    if len(positions) > 2:
                        # Region with more than 1 point found
                        # break (will be part of other algorithms)
                        positions = []

                        ## find closest to the first point
                        #k = 1
                        #dx = positions[0].x - positions[1].x
                        #if dx < 0:
                            #dx = dx * - 1
                        #dy = positions[0].y - positions[1].y
                        #if dy < 0:
                            #dy = dy * - 1
                        #for j in range(2, len(positions)):
                            #dxl = positions[0].x - positions[j].x
                            #if dxl < 0:
                                #dxl = dxl * - 1
                            #dyl = positions[0].y - positions[j].y
                            #if dyl < 0:
                                #dyl = dyl * - 1

                            #if  (dxl < dx)\
                            #or (dyl < dy):
                                ## closer point found
                                #if dx == 0 or dy == 0:
                                    ## point already on line for x or y
                                    #positions = []
                                    #break
                                #dx = dxl
                                #dy = dyl
                                #k = j
                        #if len(positions) >0:
                            #positionl = []
                            #positionl.append(positions[0])
                            #positionl.append(positions[k])
                            #positions = positionl

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
                    # search for a neighbour region with class Corridor
                    neighbourR = None
                    if isinstance(Relation.northN, Corridor):
                        neighbourR = Relation.northN
                    elif isinstance(Relation.southN, Corridor):
                        neighbourR = Relation.southN
                    elif isinstance(Relation.westN, Corridor):
                        neighbourR = Relation.westN
                    elif isinstance(Relation.eastN, Corridor):
                        neighbourR = Relation.eastN
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



        # generate navpoint relations "localDirectionOf"  neigbour regions
        # for room parts only
        result = []
        Relations.getRegionsByClass(Region, Room, result)
        for i in range(0, len(result)):
            # Region
            R = result[i]
            # Relation
            Relation = Relations.getRelation(R)

            # selected region is a room
            for j in range(0, len(self.list)):
                if self.list[j].inRegion == R:
                    # for all own navpoints
                    # if neighbour is a room too only
                    if isinstance(Relation.northN, Room):
                        self.list[j].localSouthOf = Relation.northN

                    elif isinstance(Relation.southN, Room):
                        self.list[j].localNorthOf = Relation.southN

                    elif isinstance(Relation.westN, Room):
                        self.list[j].localEastOf = Relation.westN

                    elif isinstance(Relation.eastN, Room):
                        self.list[j].localWestOf = Relation.eastN

        # generate navpoint relations "localDirectionOf"  neigbour regions
        # for cordidor parts only
        result = []
        Relations.getRegionsByClass(Region, Corridor, result)
        for i in range(0, len(result)):
            # Region
            R = result[i]
            # Relation
            Relation = Relations.getRelation(R)

            # selected region is a corridor
            for j in range(0, len(self.list)):
                if self.list[j].inRegion == R:
                    # for all own navpoints
                    # if neighbour is a corridor too only
                    if isinstance(Relation.northN, Corridor):
                        self.list[j].localSouthOf = Relation.northN

                    elif isinstance(Relation.southN, Corridor):
                        self.list[j].localNorthOf = Relation.southN

                    elif isinstance(Relation.westN, Corridor):
                        self.list[j].localEastOf = Relation.westN

                    elif isinstance(Relation.eastN, Corridor):
                        self.list[j].localWestOf = Relation.eastN




        # generate additional navpoints between room parts (N/S, W/E)


        # generate additional navpoints between corridor parts (N/S, W/E)



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
