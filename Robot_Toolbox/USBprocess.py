# -*- coding: utf-8 -*-
###############################################################################
# Class USBprocess
# Version: 2015_12_27
# Creator: Wolfgang Glück
###############################################################################
import serial
import time
import platform


class USBprocess:

    def __str__(self):
        nachricht = "USBprocess"
        return nachricht

    def USBrun(self, MQueue, CQueue):
        # continuous process
        if platform.system() == "Linux":
            self.device = "dev/ttyUSB0"  # Linux
        else:
            self.device = "COM3"         # Windows
        #self.device = [/dev/ttyUSB0"  # Linux
        self.device = "COM3"           # Windows
        self.baud = 250000
        self.ser = serial.Serial(self.device, self.baud)
        time.sleep(4)

        while True:
            try:
                # get messages from USB interface and append to MQueue
                MQueue.put(self.ser.readline())
            except serial.SerialException:
                MQueue.put("USB disturbance! ")
                # initiation USB after connection  was lost
                while True:
                    try:
                        self.ser.close()
                        self.ser.open()
                    except serial.SerialException:
                        # wait for the next trial
                        time.sleep(1)
                        continue
                    else:
                        # wait for the Arduino reset
                        time.sleep(4)
                        break
            else:
                # get comman from CQueue
                command = CQueue.get()
                if command is not None:
                    try:
                        # Send command to USB interface
                        self.ser.write(b'command')
                    except serial.SerialException:
                        MQueue.put("USB disturbance! ")
                        # initiation USB after connection  was lost
                        while True:
                            try:
                                self.ser.close()
                                self.ser.open()
                            except serial.SerialException:
                                # wait for the next trial
                                time.sleep(1)
                                continue
                            else:
                                # wait for the Arduino reset
                                time.sleep(4)
                                break
                    else:
                        continue

        # never executed
        return