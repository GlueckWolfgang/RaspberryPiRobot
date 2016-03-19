# -*- coding: utf-8 -*-
###############################################################################
# Class of EdgeL
# Version:  2016.03.16
#
#
###############################################################################


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

    def notInStack(self, Navpoint):
        for i in range(0, len(self.stack)):
            if self.stack[i] == Navpoint:
                return False
        return True

    def emptyRoadmap(self):
        self.roadMap = []
        return

    def generateEdges(self, Positions):
        Positions.reset()            # clear done tag
        self.putStack(Positions[0])  # Base as Start Position

        while len(self.stack) > 0:
            position = self.getNextfromStack()
            position.done = True
            # search for closest in x direction W/E y = y'

            # put in Buffer

            # search for closest in y direction N/S x = x'

            # put in Buffer

            # process Buffer and put buffer content in to stack if not in stack
            if len(self.buffer) > 0:
                pass

        return
