# -*- coding: utf-8 -*-
###############################################################################
# Class USBprocess
# Version: 2015_12_28
# Creator: Wolfgang Glück
###############################################################################
import serial
import time
import platform

if platform.system() == "Linux":
    device = "dev/ttyUSB0"  # Linux
else:
    device = "COM3"         # Windows
baud = 38400
ser = serial.Serial(device, baud)
# clear buffer
ser.close()
ser.open()

while True:
    try:
        result = ser.readline()
        if result is not None and result is not "b'\r\n'":
            MQueue = result
            print(MQueue)
            continue
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
                # clear buffer
                ser.close()
                ser.open()
                break
    else:
        continue