# -*- coding: utf-8 -*-
###############################################################################
# Class USBprocess
# Version: 2015_12_28
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
        if platform.system() == "Linux":
            self.device = "/dev/ttyUSB0"  # Linux
        else:
            self.device = "COM3"          # Windows
        self.baud = 38400
        self.ser = serial.Serial(self.device, self.baud)
        # clear buffer
        self.ser.close()
        self.ser.open()
        MQueue.put(b'S-USB disturbance: 0\r\n')

        # continuous process
        while True:
            try:
                # get messages from USB interface and append to MQueue
                result = (self.ser.readline())
                if result is not None and result is not "":
                    MQueue.put(result)

                # get command from CQueue
                if not CQueue.empty():
                    command = bytes(CQueue.get(), encoding="UTF-8")
                    # Send command to USB interface
                    self.ser.write(command)

            except serial.SerialException:
                MQueue.put(b'S-USB disturbance: 1\r\n')
                # initiation USB after connection  was lost
                while True:
                    try:
                        self.ser.close()
                        self.ser.open()
                        MQueue.put(b'USB open! \r\n')
                        MQueue.put(b'S-USB disturbance: 0\r\n')
                    except serial.SerialException:
                        # wait for the next trial
                        MQueue.put(b'USB Open failed! \r\n')
                        time.sleep(1)
                        continue
                    else:
                        # clear buffer
                        self.ser.close()
                        self.ser.open()
                        break

            else:
                continue
        # never executed
        return