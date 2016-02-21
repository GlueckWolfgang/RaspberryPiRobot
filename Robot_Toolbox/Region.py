# -*- coding: utf-8 -*-
###############################################################################
# Class of Region
# Version:  2016.02.21
#
# A region is a room or a door
#
# For ypur comfort:
# Use the parameter sequence of Region according to type part sequence
#
# dtype       the type of region ("M", "LM", "LMR")
# xm, ym      the coordinates of the middle point of the rectangle M
# wm          width of the rectangle M
# hm          height of the rectangle M
# anglem      deviation from north direction
#
# wl          width of the rectangle L
# hl          hight of the rectangle L
# yl          +- deviation from ym
#
# wr          width of the ectangle R
# hr          hight of the rectangle R
# yr          +- deviation from ym
#
###############################################################################


class Region:
    def __init__(self, dtype, anglem, p1=None, p2=None, p3=None, p4=None,
                        p5= None, p6=None, p7=None,p8=None,p9=None, p10=None):
        self.dtype = dtype
        self.angleM = anglem
        # M
        if dtype == "M":
            self.xM = p1
            self.yM = p2
            self.widthM = p3
            self.heightM = p4

            self.widthL = p5
            self.heightL = p6
            self.yL = p7
        else:
            # LM or LMR
            self.widthL = p1
            self.heightL = p2
            self.yL = p3

            self.xM = p4
            self.yM = p5
            self.widthM = p6
            self.heightM = p7

        # M, LM, LMR
        self.widthR = p8
        self.heightR = p9
        self.yR = p10


    def __str__(self):
        nachricht = "Class region"
        return nachricht



