import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import *

from Ui_Loading import Ui_Loading

class MainWindow(Ui_Loading):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dragPos = QtCore.QPoint()
        

if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv) 

    w = MainWindow()
    w.show()

    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())