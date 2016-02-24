# -*- coding: utf-8 -*-
###############################################################################
# Class of Room
# Version:  2016.02.23
#
#
# color       class for display control
#
###############################################################################
from Robot_Toolbox.Region import *


class Room (Region):
    def __init__(self, dtype, anglem, p1=None, p2=None, p3=None, p4=None):
        Region.__init__(self, dtype, anglem, p1, p2, p3, p4)
        self.color = "#00FF00"

    def __str__(self):
        nachricht = "Class room"
        return nachricht
