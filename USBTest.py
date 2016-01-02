# -*- coding: utf-8 -*-
###############################################################################
# USB test
# Version: 2015_12_30
###############################################################################
import serial
import time
import platform

if platform.system() == "Linux":
    device = "dev/ttyUSB0"  # Linux
else:
    device = "COM3"         # Windows
baud = 38400
ser = serial.Serial(device, baud, timeout = 0.1)
# clear buffer
ser.close()
ser.open()

while True:
    try:
        result = ser.readline()

        # protect from broken strings
        print(result)
        result = result.decode("utf-8")
        if result is not None\
        and result.rfind("\n") != -1:
            MQueue = result
            #print(MQueue)
        else:
            print("Fehlerhafter datensatz: ", result)

    except serial.SerialException:
        MQueue = ("S@USB disturbance! \r\n")
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
            else:
                # clear buffer
                ser.close()
                ser.open()
                break

    except UnicodeDecodeError:
        pass
    else:
        continue
