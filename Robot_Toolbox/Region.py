# -*- coding: utf-8 -*-
###############################################################################
# Class of Region
# Version:  2016.02.24
#
# dtype       the type of region ("I" has inner structure,
#                                 "M" is inner main structure)
# angle       the deviation from north direction
# color       class for display control
# xM, yM      the coordinates of the middle point of the region
# wm          width of the rectangle M
# hm          height of the rectangle M
#
###############################################################################


class Region:
    def __init__(self, dtype, anglem, p1=None, p2=None, p3=None, p4=None):
        self.dType = dtype
        self.angleM = anglem
        self.color = "#AAAAAA"
        # M
        self.xM = p1
        self.yM = p2
        self.widthM = p3
        self.heightM = p4

    def __str__(self):
        nachricht = "Class region"
        return nachricht
