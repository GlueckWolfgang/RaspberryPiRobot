# -*- coding: utf-8 -*-
###############################################################################
# Class USBprocess
# Version: 2016_01_02
#
# Please note, that the CQueue will only operate after a message has been
# received from MQueue. (Arduino sends every 250 ms a message block)
# If this is not what you expect, separate the whole command process!
###############################################################################
import serial
import time
import platform


class USBprocess:

    def __str__(self):
        nachricht = "USB process"
        return nachricht

    def USBrun(self, MQueue, CQueue):
        if platform.system() == "Linux":
            self.device = "/dev/ttyUSB0"  # Linux
        else:
            self.device = "COM3"          # Windows
        self.baud = 38400
        self.ser = serial.Serial(self.device, self.baud)
        # clear buffer
        self.ser.close()
        self.ser.open()
        MQueue.put("S@USB disturbance: 0\n")

        # continuous process
        while True:
            try:
                # get messages from USB interface and append to MQueue
                result = (self.ser.readline())
                result = result.decode("utf-8")  # see except UnicodeDecodeError
                if result is not None\
                and result.rfind("\n") != -1:
                    MQueue.put(result)

                # get command from CQueue
                if not CQueue.empty():
                    command = bytes(CQueue.get(), encoding="UTF-8")
                    # Send command to USB interface
                    self.ser.write(command)

            except serial.SerialException:
                MQueue.put("S@USB disturbance: 1\n")
                # initiation USB after connection  was lost
                while True:
                    try:
                        self.ser.close()
                        self.ser.open()
                        MQueue.put("S@USB disturbance: 0\n")
                    except serial.SerialException:
                        # wait for the next trial
                        MQueue.put("I@USB open failed")
                        time.sleep(1)
                        continue
                    else:
                        # clear buffer
                        self.ser.close()
                        self.ser.open()
                        break
            except UnicodeDecodeError:
                # put the rubbish (corrupted data) to the bin
                pass
            else:
                continue
        # never executed
        return