# -*- coding: utf-8 -*-
###############################################################################
# Class of Relations
# Version:  2016.02.23
#
# relations between regions respectively their parts
#
###############################################################################


class Relation:
    def __init__(self):
        self.list = []                    # list of relations

    def __str__(self):
        nachricht = "Class relation"
        return nachricht

    def putRelation(self, relation):
        self.list.append(relation)
        return

    def getRegions(self, region, result):
        for i in range(0, len(self.list)):
            if self.list[i].region == region:
                if self.list[i].region.dType == "M":
                    result.append(self.list[i].region)
                else:
                    self.getRegions(self.list[i].northN, result)
        return

