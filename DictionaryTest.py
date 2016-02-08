# -*- coding: utf-8 -*-
###############################################################################
# Test dictionary
# Version:  2016.02.06
#
###############################################################################
import json

alarmList = [["1", "4", "25"],
             ["Date / Time", "Message", "Limit", "Value", "Dimension", "C/G", "A"],
             ["2016-02-06 20:05:36.422", "USB Schnittstelle gestört", "", "", "", "C", "A"]]

# generate header and a empty dictionary for alarm list
dictionary = {"actual": alarmList[0][0], "last": alarmList[0][1]}
for i in range(0, 25):
    for j in range(0, 7):
        element = {str(i + 1) + "." + str(j + 1): ""}
        dictionary.update(element)

# fill in existing alarmlist values except headline [0][1..7]
for i in range(1, len(alarmList)):
    for j in range(0, 7):
        element = {str(i) + "." + str(j + 1): alarmList[i][j]}
        dictionary.update(element)

output = json.dumps(dictionary)
print("Dictionary: \n" + output)
