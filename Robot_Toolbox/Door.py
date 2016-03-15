# -*- coding: utf-8 -*-
###############################################################################
# Class of Door
# Version:  2016.03.15
#
#
# color       class for display control
# name        name as clear text
#
###############################################################################
from Robot_Toolbox.Region import *


class Door (Region):
    def __init__(self, name, dtype, anglem, p1=None, p2=None, p3=None, p4=None):
        Region.__init__(self, name, dtype, anglem, p1, p2, p3, p4)
        self.color = "#FFAA00"
        self.name = name

    def __str__(self):
        nachricht = "Class door"
        return nachricht
