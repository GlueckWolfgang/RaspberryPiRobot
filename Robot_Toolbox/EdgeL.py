# -*- coding: utf-8 -*-
###############################################################################
# Class of EdgeL
# Version:  2016.04.08
#
#
###############################################################################
import copy
from Robot_Toolbox.Edge import *

class EdgeL:
    def __init__(self):
        self.list = []                # list of position edges
        self.stack = []
        self.buffer = []
        self.path = []
        self.startPosition = None
        self.targetPosition = None
        self.robotPositionX = 0
        self.robotPositionY = 0
        self.robotSquareWidth = 30
        self.robotSquareHeight = 30
        self.robotSquareColor = "#0000FF"

    def putStack(self, element):
        self.stack.append(element)
        return

    def getNextfromStack(self):
        if len(self.stack) > 0:
            return self.stack.pop(0)
        else:
            return None

    def emptyPath(self):
        self.path = []
        return

    def getEdge(self, fromP, toP):
        for i in range(0, len(self.list)):
            if self.list[i].fromP == fromP\
            and self.list[i].toP == toP:
                return self.list[i]
                break
        return None

    def generateEdges(self, Positions, Relations):
        Positions.reset()                 # clear done tag
        self.putStack(Positions.list[0])  # Base as Start Position

        while len(self.stack) > 0:
            position = self.getNextfromStack()
            position.done = True          # done!
            westList = []
            eastList = []
            northList = []
            southList = []
            self.buffer = []
            # search for closest in x direction W/E y = y'
            for i in range(0, len(Positions.list)):
                position2 = Positions.list[i]
                if position2 is not position\
                and position2.y == position.y\
                and position2.x - position.x < 0:
                    # position found in west direction
                    westList.append(position2)

                if position2 is not position\
                and position2.y == position.y\
                and position2.x - position.x > 0:
                    # position found in east direction
                    eastList.append(position2)

            # search for closest in y direction N/S x = x'
            for i in range(0, len(Positions.list)):
                position2 = Positions.list[i]
                if position2 is not position\
                and position2.x == position.x\
                and position2.y - position.y < 0:
                    # position found in north direction
                    northList.append(position2)

                if position2 is not position\
                and position2.x == position.x\
                and position2.y - position.y > 0:
                    # position found in south direction
                    southList.append(position2)

            if len(westList) > 0:
                position2 = westList[0]
                for j in range(0, len(westList)):
                    if (position2.x - position.x) < (westList[j].x - position.x):
                        position2 = westList[j]
                # closest position west
                position2.angle = 270  # angle from position to position2
                self.buffer.append(position2)

            if len(eastList) > 0:
                position2 = eastList[0]
                for j in range(0, len(eastList)):
                    if (position2.x - position.x) > (eastList[j].x - position.x):
                        position2 = eastList[j]
                # closest position east
                position2.angle = 90  # angle from position to position2
                self.buffer.append(position2)

            if len(northList) > 0:
                position2 = northList[0]
                for j in range(0, len(northList)):
                    if (position2.y - position.y) < (northList[j].y - position.y):
                        position2 = northList[j]
                # closest position north
                position2.angle = 0  # angle from position to position2
                self.buffer.append(position2)

            if len(southList) > 0:
                for j in range(0, len(southList)):
                    position2 = southList[0]
                    if (position2.y - position.y) > (southList[j].y - position.y):
                        position2 = southList[j]
                # closest position south
                position2.angle = 180  # angle from position to position2
                self.buffer.append(position2)

            # process Buffer
            for j in range (0, len(self.buffer)):
                # put buffer[j] to stack if not done and not in stack
                if (not self.buffer[j].done) and (self.buffer[j] not in self.stack):
                    self.putStack(self.buffer[j])

                # generate edge from position to buffer[j]
                if position.x == self.buffer[j].x:
                    weight = abs(position.y - self.buffer[j].y)
                else:
                    weight = abs(position.x - self.buffer[j].x)
                # check if points are in the same region
                #       or in a neighbour region
                #       or buffer[j] has same neighbour door as position
                positionRel = Relations.getRelation(position.inRegion)
                bufferRel = Relations.getRelation(self.buffer[j].inRegion)
                bufferRelList =[]
                if bufferRel.northN is not None:
                    bufferRelList.append(bufferRel.northN)
                if bufferRel.southN is not None:
                    bufferRelList.append(bufferRel.southN)
                if bufferRel.westN is not None:
                    bufferRelList.append(bufferRel.westN)
                if bufferRel.eastN is not None:
                    bufferRelList.append(bufferRel.eastN)

                if position.inRegion == self.buffer[j].inRegion\
                or position.inRegion in bufferRelList\
                or positionRel.northN in bufferRelList\
                or positionRel.southN in bufferRelList\
                or positionRel.westN in bufferRelList\
                or positionRel.eastN in bufferRelList:

                    # check if forward or backward edge
                    if self.buffer[j].done is False:
                        # Forward edge
                        self.list.append(Edge(position, self.buffer[j], weight, self.buffer[j].angle, True))
                    else:
                        # Backward edge
                        self.list.append(Edge(position, self.buffer[j], weight, self.buffer[j].angle, False))
        return

    def transformEdgesToCanvasLine(self, modus, scale):
        result = []
        if modus == "All":
            source = self.list
        else:
            source = self.path
        for i in range(0, len(source)):
            edge = source[i]
            if edge.forward is True\
            or modus == "Path":
                Buffer = []
                if modus == "Path":
                    Buffer.append(edge.pathColor)
                else:
                    Buffer.append(edge.roadColor)
                Buffer.append(round(edge.fromP.x / scale))
                Buffer.append(round(edge.fromP.y / scale))
                Buffer.append(round(edge.toP.x / scale))
                Buffer.append(round(edge.toP.y / scale))
                result.append(Buffer)
        return result

    def transformRobotPositionToCanvasRect(self, scale):
        Buffer = []
        if self.robotPositionX != 0\
        and self.robotPositionY != 0:
            Buffer.append([[self.robotSquareColor],
                          [round((self.robotPositionX - self.robotSquareWidth / 2) / scale),
                           round((self.robotPositionY - self.robotSquareHeight / 2) / scale),
                           round(self.robotSquareWidth / scale),
                           round(self.robotSquareHeight / scale)]])
        return Buffer

    def setStartPosition(self, position):
        if position is not None:
            self.startPosition = position
        return

    def setTargetPosition(self, position):
        if position is not None:
            self.targetPosition = position
        return

    def calculateNewPath(self, Positions, PQueue):
        self.putStack(self.startPosition)  # Start Position to stack
        Positions.reset()                  # clear done tag
        Buffer = []
        Buffer.append([self.startPosition])

        while len(self.stack) > 0:
            position = self.getNextfromStack()
            # print ("Stack: x ",position.x, " y ", position.y)
            for i in range(0, len(self.list)):
                if self.list[i].fromP == position:
                    # edge with from position == position found
                    position.done = True   # done!
                    # if toP not done, and not disabled and not target
                    if self.list[i].toP.done is False\
                    and self.list[i].toP.disabled is False\
                    and self.list[i].toP != self.targetPosition:
                        # put toP to stack
                        self.putStack(self.list[i].toP)


                    # search for  lines in buffer with position at the end
                    lineFound = False
                    for j in range(0, len(Buffer)):
                        line = Buffer[j]
                        if line[len(line) - 1] == position:
                            # found stack position at the end
                            lineFound = True
                            Buffer[j].append(self.list[i].toP)
                            #print("Buffer existing lines after append:")
                            #for k in range(0, len(Buffer)):
                                #print("\n")
                                #for l in range (0, len(Buffer[k])):
                                    #print("x ", Buffer[k][l].x, " y ", Buffer[k][l].y)

                    # create new line
                    if lineFound is False:
                        for j in range(0, len(Buffer)):
                            line = Buffer[j]
                            if line[len(line) - 2] == position:
                                # found stack position at end -1
                                newline = copy.copy(Buffer[j])
                                newline.pop(len(newline) - 1)
                                newline.append(self.list[i].toP)
                                Buffer.append(newline)
                                #print("Buffer new line after append:")
                                #for k in range(0, len(Buffer)):
                                    #print("\n")
                                    #for l in range (0, len(Buffer[k])):
                                        #print("x ", Buffer[k][l].x, " y ", Buffer[k][l].y)
                                break
        # store status "No path found" G
        PQueue.put("S@Target not reachable: " + str(0))
        # delete path
        self.emptyPath()

        # delete path length
        PQueue.put("MV@Path lenght: V " + str(0))

        # check if a solution exists and note sum of edge length
        solution = False
        Buffer2 = []
        for i in range(0, len(Buffer)):
            if Buffer[i][len(Buffer[i]) - 1] == self.targetPosition:
                solution = True
                length = 0
                edge = []
                for j in range(0, len(Buffer[i]) - 1):
                    edge.append(self.getEdge(Buffer[i][j], Buffer[i][j + 1]))
                    length = length + edge[len(edge) - 1].weight
                edge.append(length)
                Buffer2.append(edge)

        if solution is False:
            # no solution
            # store status "No path found" C
            PQueue.put("S@Target not reachable: " + str(1))
        else:
            # find solution with shortest path length
            shortest = Buffer2[0]
            for j in range(0, len(Buffer2)):
                if Buffer2[j][len(Buffer2[j]) - 1] < shortest[len(shortest) - 1]:
                    shortest = Buffer2[j]
            pathLength = shortest.pop(len(shortest) - 1)
            # store path length as a measured value
            PQueue.put("MV@Path lenght: V " + str(int(pathLength)))

            # store path
            self.path = shortest

        return
