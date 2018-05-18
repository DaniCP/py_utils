'''
Created on 04 de May de 2017

@author: daniel.cano
@note: Delta Elektronika power source controller
'''

from time import sleep
import serial


class Delta_elektronka_mng():
    def __init__(self, com_port='COM13'):
        self.com = serial.Serial(com_port, baudrate=9600)
        self.com.write('CH 1')
        sleep(0.1)

    def set_voltage(self, v):
        self.com.write('SOURCE:VOLTAGE '+str(v)+'\r\n')
        sleep(0.1)

    def set_current(self, c):
        self.com.write('SOURCE:CURRENT '+str(c)+'\r\n')
        sleep(.1)

    def power_on(self):
        self.com.write('OUTPUT 1\r\n')
        sleep(.1)

    def power_off(self):
        self.com.write('OUTPUT 0\r\n')
        sleep(.1)


if __name__ == '__main__':
    delta = Delta_elektronka_mng('COM13')
    delta.set_voltage(24)
    delta.set_current(2)
    delta.power_on()
    sleep(5)
    delta.power_off()
    print 'END'

'''
COMUNICACION CON ARDUINO
import serial
from time import sleep
ser = serial.Serial(port='COM4',baudrate=9600, timeout=1)
sleep(2)

x = bytearray(b'\xff')
#x.append(0xff)

b = ser.write(x)
sleep(0.1)
a = ser.read(4)
pos = hex(int(a[-2:].encode('hex'), 16))
curr = hex(int(a[:2].encode('hex'), 16))
print int(pos,0)
print int(curr,0)
'''
