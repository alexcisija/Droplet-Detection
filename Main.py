import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import *

from Ui_Loading import Ui_Loading
from Ui_VideoAnalysis import Ui_VideoAnalysis

class MainWindow(Ui_VideoAnalysis):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv) 

    w = MainWindow()
    w.show()

    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())