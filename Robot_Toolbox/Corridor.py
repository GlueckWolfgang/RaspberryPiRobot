# -*- coding: utf-8 -*-
###############################################################################
# Class of Corridor
# Version:  2016.04.18
#
#
# color       class for display control
# name        name as clear text
#
###############################################################################
from Robot_Toolbox.Region import *


class Corridor (Region):
    def __init__(self, name, dtype, p1=None, p2=None, p3=None, p4=None):
        Region.__init__(self, name, dtype, p1, p2, p3, p4)
        self.color = "#FFD700"
        self.name = name

    def __str__(self):
        nachricht = "Class corridor"
        return nachricht