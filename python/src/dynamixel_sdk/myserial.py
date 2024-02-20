import serial
import serial.serialutil
import fcntl
import termios
import os
import struct
import time 

import RPi.GPIO as GPIO


#CTSRTS_PIN=17
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(CTSRTS_PIN,GPIO.OUT)
#GPIO.output(CTSRTS_PIN,False)

import serial
import serial.serialutil
import fcntl
import termios
import os
import struct
 
class RS485Ext(serial.Serial):
    def __init__(self, *args, **kwargs):
        super(RS485Ext, self).__init__(*args, **kwargs)
 
    def write(self, b):
        # set RTS pin high
        fd = self.fileno()
        buf = struct.pack('<1i', termios.TIOCM_RTS)
        fcntl.ioctl(fd, termios.TIOCMBIC, buf) # clear
 
        # write data
        d = serial.serialutil.to_bytes(b)
        length = os.write(self.fileno(), d)
 
        # wait for TX
        lsr = struct.pack('<1i', 0)
        while(True):
            # check line status register
            unpacked_lsr = struct.unpack('<1i',
                fcntl.ioctl(fd, termios.TIOCSERGETLSR, lsr))
            if (unpacked_lsr[0] & termios.TIOCSER_TEMT):
                break
 
        # set RTS pin low
        fcntl.ioctl(fd, termios.TIOCMBIS, buf) # set
 
        return length