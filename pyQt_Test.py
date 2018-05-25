import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
from posCurrTorqArduComm import posCurrTorqArduComm

'''CONSTANTS'''
# (tiempo, par, tension)
CICLO = ((2*5, 255, 24),
         (3, 123, 24),
         (3, 0, 24))
SAMPLING = 100.0  # ms
ARD_COM = 'COM4'


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)

        #  line plot
        self.otherplot = self.canvas.addPlot()
        self.h2 = self.otherplot.plot(pen='y')
        self.h1 = self.otherplot.plot(pen='y')


        #### Set Data  #####################
        self.x = np.linspace(0, 50., num=100)
        self.X, self.Y = np.meshgrid(self.x, self.x)
        self.counter = 0
        self.lastupdate = time.clock()
        self.xdata = []  # init time x data
        self.ydata = []  # init ydata
        self.y2data = []  # init ydata

        #### Init arduino  #####################
        self.ardu = posCurrTorqArduComm(port='COM4')

        #### Start  #####################
        self.timeout = time.clock() + CICLO[0][0]  # seconds
        self._update()

    def _update(self):

        a = self.ardu.set_torq(CICLO[self.counter][1])  # get data from ardu
        now = time.clock()

        self.ydata = np.append(self.ydata, [a[0]])
        self.y2data = np.append(self.y2data, [a[1]])
        self.xdata = np.append(self.xdata, now)

        self.h2.setData(self.xdata, self.ydata)
        self.h1.setData(self.xdata, self.y2data)

        print now, a[0], a[1], self.counter

        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001

        tx = 'dt: {dt:.3f}, elapsed: {el:.3f} s'.format(dt=dt, el=now)
        self.label.setText(tx)

        if now > self.timeout:
            self.counter += 1
            if self.counter < len(CICLO):
                self.timeout = time.clock() + CICLO[self.counter][0]

        if self.counter < len(CICLO):
            QtCore.QTimer.singleShot(SAMPLING, self._update)

        self.lastupdate = now


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())
