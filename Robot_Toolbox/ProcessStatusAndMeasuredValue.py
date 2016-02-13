# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess status and measured value
# Version:  2016.01.21
#
# PQueue             = queue to listen
# AQueue.............= process Audio queue
# LQueue.............= process Alarm list queue
# MQueue             = process Main queue
# WPQueue            = process webserver queue
# StatusList         = image for stati
# MeasuredValueList  = image for measured values
###############################################################################
import copy
import json
import re
import codecs
from bs4 import BeautifulSoup as Soup


class ProcessStatusAndMeasuredValue:

    def __init__(self):
        template = dict()


        def get_ids(html_file, regular_expression):
           ids = dict()
           with codecs.open(html_file, 'r', encoding='utf-8', errors='ignore') as fh:
              soup = Soup(fh, 'html.parser')
              for element in soup.find_all('td', id=re.compile(regular_expression)):
                  id = element.get('id')
                  if id:
                      ids[id] = ""
                      if id.endswith("_V"):
                      # add Cv
                          id = id.replace("_V", "_Cv")
                          ids[id] = ""
           return ids

        # create dictionary
        template = get_ids("Robbi/Panel.html", r'["id=M_]|["id=S_]+"')
        ouput = json.dumps(template)


    def __str__(self):
        nachricht = "Process Status and measured value"
        return nachricht


    def Run(self, PQueue, AQueue, LQueue, MQueue, WPQueue, StatusList, MeasuredValueList):

        while True:
            Message = PQueue.get()
            if Message.find("S@") == 0:
                Message = Message.replace("S@", "")
                # Put status
                StatusList.putValue(Message, AQueue, LQueue, MQueue)

            elif Message.find("MV@") == 0:
                Message = Message.replace("MV@", "")
                # Put measured value
                MeasuredValueList.putValue(Message, AQueue, LQueue, MQueue)

            elif Message.find("R@") == 0:
                # request for data
                WPQueue.put(["S@", copy.copy(StatusList.list)])
                WPQueue.put(["MV@", copy.copy(MeasuredValueList.list)])

            else:
                MQueue.put("I@Process status and measured value: Unknown message at PQueue: " + Message)