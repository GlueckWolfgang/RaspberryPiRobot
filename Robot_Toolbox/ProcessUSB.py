# -*- coding: utf-8 -*-
###############################################################################
# Class Process USB
# Version: 2016_02_16
#
# Please note, that the CQueue will only operate after a message has been
# received from MQueue or at least after timeout (100ms).
# If this is not what you expect, separate the whole command process!
###############################################################################
import serial
import time
import platform


class ProcessUSB:

    def __str__(self):
        nachricht = "Process USB"
        return nachricht

    def Run(self, MQueue, CQueue, PQueue):
        if platform.system() == "Linux":
            self.device = "/dev/ttyUSB0"  # Linux
        else:
            self.device = "COM3"          # Windows

        self.disturbance = 1
        while self.disturbance == 1:
            try:
                self.ser = serial.Serial(self.device, 38400, timeout=0.1)
                self.disturbance = 0
                PQueue.put("S@USB disturbance: 0")
            except serial.SerialException:
                # wait for the next trial
                # MQueue.put("I@USB open failed")
                PQueue.put("S@USB disturbance: 1")
                MQueue.put("I@USB open failed")
                time.sleep(1)
                continue
            else:
                break

        # continuous process
        while True:
            try:
                # get messages from USB interface and append to MQueue
                result = (self.ser.readline())
                result = result.decode("utf-8")  # see except UnicodeDecodeError
                if result is not None\
                and result.rfind("\n") != -1:
                    PQueue.put(result)

                # get command from CQueue
                if not CQueue.empty():
                    command = bytes(CQueue.get(), encoding="UTF-8")
                    # Send command to USB interface
                    self.ser.write(command)

            except serial.SerialException:
                PQueue.put("S@USB disturbance: 1")
                # initiation USB after connection  was lost
                while True:
                    try:
                        # clear buffer
                        self.ser.close()
                        self.ser.open()
                        PQueue.put("S@USB disturbance: 0")
                    except serial.SerialException:
                        # wait for the next trial
                        # MQueue.put("I@USB open failed")
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