# -*- coding: utf-8 -*-
###############################################################################
# Class of Door
# Version:  2016.02.22
#
#
# color       class for display control
#
###############################################################################
from Robot_Toolbox.Region import *


class Door (Region):
    def __init__(self, dtype, anglem, p1=None, p2=None, p3=None, p4=None):
        self.color = "yellow"

    def __str__(self):
        nachricht = "Class door"
        return nachricht
