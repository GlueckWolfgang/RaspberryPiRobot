# -*- coding: utf-8 -*-
###############################################################################
# Class of Relations
# Version:  2016.02.22
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
