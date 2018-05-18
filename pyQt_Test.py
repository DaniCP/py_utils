import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
from posCurrTorqArduComm import posCurrTorqArduComm

'''CONSTANTS'''
# (tiempo, par, tension)
CICLO = ((5, 255, 24),
         (5, 123, 24),
         (5, 0, 24))
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
        self.fps = 0.
        self.lastupdate = time.clock()
        self.xdata = []  # init time x data
        self.ydata = []  # init ydata
        self.y2data = []  # init ydata

        #### Init arduino  #####################
        self.ardu = posCurrTorqArduComm(port='COM4')

        #### Start  #####################
        self.timeout = time.clock()+10  # seconds
        self._update()

    def _update(self):

        # self.ydata = np.sin(self.x/3. + self.counter/9.)
        a = self.ardu.set_torq(self.counter)
        self.ydata = np.append(self.ydata, [a[0]])
        self.y2data = np.append(self.y2data, [a[1]])
        self.xdata = np.append(self.xdata, time.clock())

        self.h2.setData(self.xdata, self.ydata)
        self.h1.setData(self.xdata, self.y2data)

        now = time.clock()

        print now, a[0], a[1], self.counter

        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
#         tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps)
        tx = 'dt: {dt:.3f}, elapsed: {el:.3f} s'.format(dt=dt, el=now)
        self.label.setText(tx)
        if now < self.timeout:
            QtCore.QTimer.singleShot(1, self._update)

        #  counter to increase the torque
        self.counter += 1
        if self.counter > 255:
            self.counter = 0


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())
