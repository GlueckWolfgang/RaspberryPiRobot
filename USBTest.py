# -*- coding: utf-8 -*-
###############################################################################
# Class USBprocess
# Version: 2015_12_27
# Creator: Wolfgang Glück
###############################################################################
import serial
import time
import platform

if platform.system() == "Linux":
    device = "dev/ttyUSB0"  # Linux
else:
    device = "COM3"         # Windows
baud = 250000
ser = serial.Serial(device, baud)
# wait for the Arduino reset
time.sleep(4)

while True:
    try:
        MQueue = ser.readline()
        if MQueue is not None:
            print(MQueue)
    except serial.SerialException:
        MQueue = ("USB disturbance! \r\n")
        print(MQueue)
        # initiation USB after connection  was lost
        while True:
            try:
                ser.close()
                ser.open()
                print("USB open! \r\n")
            except serial.SerialException:
                print("USB Open failed! \r\n")
                # wait for the next trial
                time.sleep(1)
                continue
            else:
                # wait for the Arduino reset
                time.sleep(4)
                break
    else:
        continue