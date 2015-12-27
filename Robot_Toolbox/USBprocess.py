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
            self.device = "/dev/ttyUSB0"  # Linux
        else:
            self.device = "COM3"          # Windows
        self.baud = 38400
        self.ser = serial.Serial(self.device, self.baud)
        # clear buffer
        self.ser.close()
        self.ser.open()

        while True:
            try:
                # get messages from USB interface and append to MQueue
                MQueue.put(self.ser.readline())
            except serial.SerialException:
                MQueue.put(b'USB disturbance! \r\n')
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
                        # clear buffer
                        self.ser.close()
                        self.ser.open()
                        break
            else:
                # get command from CQueue
                if not MQueue.empty():
                    try:
                        command = bytes(CQueue.get(), encoding="UTF-8")
                        # Send command to USB interface
                        self.ser.write(command)
                    except serial.SerialException:
                        MQueue.put(b'USB disturbance! \r\n')
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
                                # clear buffer
                                self.ser.close()
                                self.ser.open()
                                break
                    else:
                        continue
                else:
                    continue
        # never executed
        return