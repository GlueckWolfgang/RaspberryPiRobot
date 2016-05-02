# -*- coding: utf-8 -*-
###############################################################################
# Class of command list
# Version:  2016.04.29
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

    def sendCommandByNumber(self, coNumber, coValue):
        if int(coNumber) < len(self.list):        # list must not be empty
            CommandO = self.getCommandByNumber(coNumber)
            Command = CommandO.coDescription + ": " + coValue + "\n"
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
            if self.list[i].coDescription.startswith(coName):
                return self.list[i]
            else:
                continue
        return None

    def generateCommandList(self):
        CommandO = Command(0, "Stop")                    # Main process
        self.putCommand(CommandO)
        CommandO = Command(1, "Forward slow")            # Main process
        self.putCommand(CommandO)
        CommandO = Command(2, "Forward half")
        self.putCommand(CommandO)
        CommandO = Command(3, "Forward full")
        self.putCommand(CommandO)
        CommandO = Command(4, "Steering left")
        self.putCommand(CommandO)
        CommandO = Command(5, "Steering right")
        self.putCommand(CommandO)
        CommandO = Command(6, "Steering ahead")
        self.putCommand(CommandO)
        CommandO = Command(7, "Turn slow 45 left")
        self.putCommand(CommandO)
        CommandO = Command(8, "Turn slow 45 right")
        self.putCommand(CommandO)
        CommandO = Command(9, "Turn slow 90 left")
        self.putCommand(CommandO)
        CommandO = Command(10, "Turn slow 90 right")
        self.putCommand(CommandO)
        CommandO = Command(11, "Wlan ready")             # Main?
        self.putCommand(CommandO)
        CommandO = Command(12, "Encoder reset")          # Process Main
        self.putCommand(CommandO)
        CommandO = Command(13, "Amplifier")              # Process Audio
        self.putCommand(CommandO)
        CommandO = Command(14, "Align")                  # Process StatusAndMeasuredValue
        self.putCommand(CommandO)
        CommandO = Command(15, "Turn slow to")           # Main process
        self.putCommand(CommandO)
        return