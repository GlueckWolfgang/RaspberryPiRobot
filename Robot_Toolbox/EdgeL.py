# -*- coding: utf-8 -*-
###############################################################################
# Class of EdgeL
# Version:  2016.03.19
#
#
###############################################################################
from Robot_Toolbox.Edge import *


class EdgeL:
    def __init__(self):
        self.list = []                # list of position edges
        self.stack = []
        self.buffer = []
        self.roadMap = []

    def putStack(self, element):
        self.stack.append(element)
        return

    def getNextfromStack(self):
        if len(self.stack) > 0:
            return self.stack.pop(0)
        else:
            return None

    def emptyRoadmap(self):
        self.roadMap = []
        return

    def generateEdges(self, Positions):
        Positions.reset()                 # clear done tag
        self.putStack(Positions.list[0])  # Base as Start Position

        while len(self.stack) > 0:
            position = self.getNextfromStack()
            position.done = True
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
                if len(westList) > 0:
                    position2 = westList[0]
                    for j in range(0, len(westList)):
                        if (position2.x - position.x) < (westList[j].x - position.x):
                            position2 = westList[j]
                    self.buffer.append(position2)

                if position2 is not position\
                and position2.y == position.y\
                and position2.x - position.x > 0:
                    # position found in east direction
                    eastList.append(position2)
                if len(eastList) > 0:
                    position2 = eastList[0]
                    for j in range(0, len(eastList)):
                        if (position2.x - position.x) > (eastList[j].x - position.x):
                            position2 = eastList[j]
                    self.buffer.append(position2)

            # search for closest in y direction N/S x = x'
            for i in range(0, len(Positions.list)):
                position2 = Positions.list[i]
                if position2 is not position\
                and position2.x == position.x\
                and position2.y - position.y < 0:
                    # position found in north direction
                    northList.append(position2)
                if len(northList) > 0:
                    for j in range(0, len(northList)):
                        if (position2.y - position.y) < (northList[j].y - position.y):
                            position2 = northList[j]
                    self.buffer.append(position2)


                if position2 is not position\
                and position2.x == position.x\
                and position2.y - position.y > 0:
                    # position found in south direction
                    southList.append(position2)
                if len(southList) > 0:
                    for j in range(0, len(southList)):
                        if (position2.y - position.y) < (southList[j].y - position.y):
                            position2 = southList[j]
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
                self.list.append(Edge(position, self.buffer[j], weight))
        return
