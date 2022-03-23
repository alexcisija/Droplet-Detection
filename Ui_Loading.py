import math

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import *

from Ui_VideoAnalysis import Ui_VideoAnalysis

class Droplet():
    def __init__(self, offset=0, size=30):
        self.offset = offset
        self.size = size
        self.sized = size
    
    def next(self):
        self.offset = (self.offset + 1)
        self.size = round((0.5*(math.cos(self.offset * math.pi / 20)) + 0.5) * self.sized)

        return self.size


class Ui_Loading(QMainWindow):
    def setupUi(self, Frame):
        self.translate = QtCore.QCoreApplication.translate
        self.CreateWindow(Frame)

        self.droplet_1 = Droplet()
        self.droplet_2 = Droplet(15)

        QtCore.QMetaObject.connectSlotsByName(Frame)

    def CreateWindow(self, Frame):
        objName = "Frame"
        (width, height) = (420, 180+50)

        self.Frame = Frame
        self.Frame.resize(width, height)
        self.Frame.setObjectName(objName)
        self.Frame.setWindowTitle( self.translate(objName, "PS") )

        self.Frame.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.Frame.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)


        self.background = QtWidgets.QLabel(Frame)
        self.background.setGeometry(QtCore.QRect(0, 0, width, height-50))
        self.background.setStyleSheet(
            """
            border: 5px solid rgba(94, 221, 203, 255);
            background-color: rgba(94, 221, 203, 255);
            border-radius: 4px;
            """
        )

        # Logo Image
        self.logo = QtWidgets.QLabel(Frame)
        self.logo.setGeometry(QtCore.QRect(80, 40, 295, 130))
        self.logo.setPixmap(QtGui.QPixmap("./1x/logo.png"))
        self.logo.setObjectName("logo")
        self.logo.setStyleSheet(
            """
            border-radius: 2px;
            """
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDroplets)
        self.timer.start(18)

        self.timeout = 0

    def updateDroplets(self):
        self.timeout += 1
        if self.timeout > 100: 
            self.OpenAnalysisWindow()
            self.timer.stop()
            return
        self.droplet_1.next()
        self.droplet_2.next()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(94, 221, 203), Qt.SolidPattern))
        painter.drawEllipse(self.Frame.width()//2-(5 + self.droplet_1.size//2), self.Frame.height()-50+10, self.droplet_1.size, self.droplet_1.size)
        painter.drawEllipse(self.Frame.width()//2+(5 + self.droplet_1.size//2), self.Frame.height()-50+10, self.droplet_2.size, self.droplet_2.size)
        painter.end()

    def OpenAnalysisWindow(self):
        self.Analysis = QtWidgets.QMainWindow() #Make a new window
        self.ui = Ui_VideoAnalysis() #Which window we're opening
        self.ui.setupUi(self.Analysis) #Call the setup for that window
        self.hide() #Hides the OG
        self.Analysis.show() #Show it