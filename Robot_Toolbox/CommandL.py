# -*- coding: utf-8 -*-
###############################################################################
# Class of command list
# Version:  2016.01.05
###############################################################################
from Robot_Toolbox.Command import *


class CommandL:

    def __init__(self):
        self.list = []                       # List of command objects

    def __str__(self):
        nachricht = " List of commands"
        return nachricht

    def putCommand(self, Command):
        self.list.append(Command)            # index = coNumber
        return

    def sendCommandByNumber(self,coNumber, coValue):
        if int(coNumber) < len(self.list):        # list must not be empty
            CommandO = self.getCommandByNumber(coNumber)
            Command = CommandO.coDescription + coValue
            return Command
        else:
            return None

    def getCommandByNumber(self, coNumber):
        if int(coNumber) < len(self.list):        # list must not be empty
            return self.list[int(coNumber)]
        else:
            return None

    def getCommandByName(self, coName):
        for i in range(0, len(self.list)):  # list must not be empty
            if self.list[i].coDescription == coName:
                return self.list[i]
            else:
                continue
        return None

    def generateCommandList(self):
        CommandO = Command(0, "Stop")
        self.putCommand(CommandO)
        CommandO = Command(1, "ForwardSlow")
        self.putCommand(CommandO)
        CommandO = Command(2, "ForwardHalf")
        self.putCommand(CommandO)
        CommandO = Command(3, "ForwardFull")
        self.putCommand(CommandO)
        CommandO = Command(4, "SteeringLeft")
        self.putCommand(CommandO)
        CommandO = Command(5, "SteeringRight")
        self.putCommand(CommandO)
        CommandO = Command(6, "SteeringAhead")
        self.putCommand(CommandO)
        CommandO = Command(7, "TurnSLow45Left")
        self.putCommand(CommandO)
        CommandO = Command(8, "TurnSlow45Right")
        self.putCommand(CommandO)
        CommandO = Command(9, "TurnSlow90Left")
        self.putCommand(CommandO)
        CommandO = Command(10, "TurnSlow90Right")
        self.putCommand(CommandO)
        CommandO = Command(11, "WlanReady")
        self.putCommand(CommandO)
        CommandO = Command(12, "EncoderReset")
        self.putCommand(CommandO)
        CommandO = Command(13, "Amplifier: ")
        self.putCommand(CommandO)


        return