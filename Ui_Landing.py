from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import *

from Ui_VideoAnalysis import Ui_VideoAnalysis

class LandingOptions(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.setLayout(self.layout)

    def addWidget(self, widget):
        self.layout.addWidget(widget, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)


class Ui_Landing(QMainWindow):
    def setupUi(self, Frame):
        self.translate = QtCore.QCoreApplication.translate
        self.LandingOptions = LandingOptions()

        self.CreateWindow(Frame)
        self.DisplayLogo()
        self.openButton = self.AddButton("Open")
        self.openButton.clicked.connect(self.OpenVideo)
        self.LandingOptions.addWidget(self.openButton)

        self.setCentralWidget(self.LandingOptions)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.DrawCircle(painter, -200, self.Frame.height()-300, 500)
        self.DrawCircle(painter, 550, self.Frame.height()-300, 200)
        self.DrawCircle(painter, 100, 100, 100)

    def DisplayLogo(self):
        self.logo = QLabel()
        self.logoPixmap = QPixmap("./1x/blogo.png")
        self.logo.setStyleSheet("background-color: transparent;")
        self.logo.setPixmap(self.logoPixmap)
        self.LandingOptions.addWidget(self.logo)
    
    def OpenVideo(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open Video", filter="Videos (*.mp4)")[0]
        self.OpenVideoAnalysis()

    def OpenVideoAnalysis(self):
        self.VideoAnalysis = Ui_VideoAnalysis(self.filename)
        self.hide()
        self.VideoAnalysis.show()

    def DrawCircle(self, painter, x, y, r):

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(204, 255, 250), Qt.SolidPattern))
        painter.drawEllipse(x, y, r, r)

        pen = QPen(QColor(142, 244, 232))
        pen.setWidth(r//10)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(254, 254, 254), Qt.SolidPattern))
        painter.drawEllipse(x + (r//4), y + (r//4), r//2, r//2)


    def CreateWindow(self, Frame):
        objName = "Frame"
        (width, height) = (800, 600)

        self.Frame = Frame
        self.Frame.resize(width, height)
        self.Frame.setObjectName(objName)
        self.Frame.setWindowTitle( self.translate(objName, "Project Symphony") )
        self.Frame.setStyleSheet("background-color: white;")

    def AddButton(self, name):
        pushButton = QtWidgets.QPushButton(name, self.Frame)
        pushButton.setObjectName(name)
        pushButton.setFixedSize(130, 50)
        pushButton.setStyleSheet(
            """
            background-color: #333333;
            color: #eeeeee;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            """
        )
        
        return pushButton