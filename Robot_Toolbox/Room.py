# -*- coding: utf-8 -*-
###############################################################################
# Class of Room
# Version:  2016.02.22
#
#
# color       class for display control
#
###############################################################################
from Robot_Toolbox.Region import *


class Room (Region):
    def __init__(self, dtype, anglem, p1=None, p2=None, p3=None, p4=None):
        self.color = "green"

    def __str__(self):
        nachricht = "Class room"
        return nachricht
