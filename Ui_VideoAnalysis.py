import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import *

class Ui_VideoAnalysis(QMainWindow):
    def setupUi(self, Frame):
        self.translate = QtCore.QCoreApplication.translate
        self.CreateWindow(Frame)

        QtCore.QMetaObject.connectSlotsByName(Frame)



    def CreateWindow(self, Frame):
        objName = "Frame"
        (width, height) = (800, 500)

        self.Frame = Frame
        self.Frame.resize(width, height)
        self.Frame.setObjectName(objName)
        self.Frame.setWindowTitle( self.translate(objName, "Droplet Analysis") )
        self.Frame.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.Frame.setStyleSheet(
            """
            border: 5px solid rgba(94, 221, 203, 255);
            background-color: rgba(94, 221, 203, 255);
            """
        )


    def AddButton(self, name, pos):
        pushButton = QtWidgets.QPushButton(self.Frame)
        pushButton.setGeometry(pos)
        pushButton.setObjectName(name)
        pushButton.setText(name)
        
        return pushButton