# -*- coding: utf-8 -*-
###############################################################################
# Class of Region
# Version:  2016.02.20
#
# A region is a room or a door
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
    def __init__(self, dtype, xm, ym, wm, hm, anglem, wl= None, hl=None, yl=None, wr=None, hr=None, yr=None):
        self.dtype = dtype
        self.xM = xm
        self.yM = ym
        self.widthM = wm
        self.heightM = hm
        self.angleM = anglem
        self.widthL = wl
        self.heightL = hl
        self.yL = yl
        self.widthR = wr
        self.heightR = hr
        self.yR = yr


    def __str__(self):
        nachricht = "Class region"
        return nachricht



