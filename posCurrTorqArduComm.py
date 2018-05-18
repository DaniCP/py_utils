'''
Created on 17 May 2018

@author: daniel.cano
@note: Arduino communication:
    - Send to arduino the Torque target
    - Read position and current
'''

import serial
from time import sleep

TORQUE = 255


class posCurrTorqArduComm():
    def __init__(self, port='COM4'):
        pass
        self.ser = serial.Serial(port=port, baudrate=9600, timeout=1)
        sleep(2)

    def set_torq(self, torque=0):
        ''' input:  torque 0-255 to send [integer]
            output: position and speed   [integer]'''
        a = bytearray(chr(torque))
        self.ser.write(a)
        sleep(0.001)
        a = self.ser.read(4)
        pos = hex(int(a[-2:].encode('hex'), 16))
        curr = hex(int(a[:2].encode('hex'), 16))
        return int(pos, 0), int(curr, 0)


if __name__ == '__main__':
    ardu = posCurrTorqArduComm(port='COM4')
    for i in range(123, 255):
        print ardu.set_torq(i)
