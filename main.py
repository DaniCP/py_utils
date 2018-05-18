from posCurrTorqArduComm import posCurrTorqArduComm
import time
import numpy as np
import matplotlib.pyplot as plt

'''CONSTANTES'''
# (tiempo, par, tension)
CICLO = ((5, 255, 24),
         (5, 123, 24),
         (5, 0, 24))
SAMPLING = 100.0  # ms el set torque ya espera 8ms

'''PROGRAMA'''
ardu = posCurrTorqArduComm(port='COM4')

plt.axis([0, 16, 0, 1050])
print 'TIME\tA0\tA1'

for i in range(0, len(CICLO)):
    timeout = time.clock() + CICLO[i][0]  # 5s from now
    while(time.clock() < timeout):
        a = ardu.set_torq(CICLO[i][1])
        print str(time.clock())+'\t'+str(a[0])+'\t'+str(a[1])
        plt.scatter(time.clock(), a[0])
        plt.pause(0.000000001)
        # time.sleep((SAMPLING-8)/1000)
plt.show()
