import sys, cv2

import DropletDetection
import numpy as np
from PyQt5.QtWidgets import QSlider, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtGui import QPixmap, QImage, QIcon

from decord import VideoReader, cpu, gpu

class FrameView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
        self.setLayout(self.layout)

class QVComponent(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
        self.setLayout(self.layout)



class Ui_VideoAnalysis(QMainWindow):
    def __init__(self, filename=None):
        super().__init__()
        self.setupUi(self, filename)
        self.setWindowIcon(QIcon('./1x/favicon.ico'))


    def setupUi(self, Frame, filename):
        self.translate = QtCore.QCoreApplication.translate
        self.startTime = 0
        self.endTime = 0
        self.fno = 0
        self.filename = filename

        self.CreateWindow(Frame)
        self.CreateFrameView()


    def CreateWindow(self, Frame):
        objName = "Frame"
        (width, height) = (700, 500)

        self.Frame = Frame
        self.Frame.resize(width, height)
        self.Frame.setObjectName(objName)
        self.Frame.setWindowTitle( self.translate(objName, "Project Symphony | Droplet Analysis") )

    def CreateFrameView(self):
        self.frameView = FrameView()
        self.setCentralWidget(self.frameView)

        videoScreen = QVComponent()
        optionButtons = QVComponent()
        optionButtons.setFixedSize(200, 500)

        self.frameWindow = QLabel()
        self.frameWindow.setStyleSheet("background-color: red; border: 5px solid black; border-radius: 8px;")
        videoScreen.addWidget(self.frameWindow)

        self.CreateFrameSlider()
        videoScreen.addWidget(self.frameSlider)

        self.setStartButton = self.AddButton(f"Set Start")
        self.setStartButton.clicked.connect(self.SetStartTime)
        optionButtons.addWidget(self.setStartButton)

        self.setEndButton = self.AddButton(f"Set End")
        self.setEndButton.clicked.connect(self.SetEndTime)
        optionButtons.addWidget(self.setEndButton)

        self.analyzeButton = self.AddButton(f"Analyze")
        self.analyzeButton.clicked.connect(lambda: DropletDetection.Analyze(self.filename, self.startTime, self.endTime))
        self.analyzeButton.setStyleSheet(
            """
            background-color: #6edbcc;
            color: #eeeeee;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            margin: 8px 0;
            """
        )
        optionButtons.addWidget(self.analyzeButton)

        self.cancelButton = self.AddButton(f"Cancel")
        self.cancelButton.clicked.connect(self.CloseWindow)
        self.cancelButton.setStyleSheet(
            """
            background-color: #ff8f8f;
            color: #eeeeee;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            margin: 8px 0;
            """
        )
        optionButtons.addWidget(self.cancelButton)

        self.frameView.addWidget(videoScreen)
        self.frameView.addWidget(optionButtons)

        self.ShowVideoFrame()

    def AddButton(self, name):
        pushButton = QtWidgets.QPushButton(name, self)
        pushButton.setObjectName(name)
        pushButton.setFixedSize(130, 50+16)
        pushButton.setStyleSheet(
            """
            background-color: #333333;
            color: #eeeeee;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            margin: 8px 0;
            """
        )
        
        return pushButton

    def CreateFrameSlider(self):
        videoDuration = len(VideoReader(f"{self.filename}", ctx=cpu(0))) - 1
        self.frameSlider = QSlider(QtCore.Qt.Horizontal, self)
        self.frameSlider.sliderReleased.connect(lambda: self.GoToFrame(self.frameSlider.value()))
        self.frameSlider.setRange(0, videoDuration)
        self.frameSlider.setStyleSheet(
            """
            QSlider::groove:horizontal{
                height: 20px;
                margin: 0 0;
            }
            QSlider::handle:horizontal{
                background-color: #6edbcc; 
                border-radius: 2px; 
                height: 80px; 
                width: 40px; 
                margin: 0 0;
            }
            """
        )

    def CloseWindow(self):
        self.close()

    def ShowVideoFrame(self):        
        self.pixmap = QPixmap(self.FetchVideoFrame())
        self.pixmap = self.pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.frameWindow.setPixmap(self.pixmap)
        self.frameWindow.setMinimumSize(500, 500)
        self.frameWindow.setScaledContents(True)

    def FetchVideoFrame(self):
        v = VideoReader(f"{self.filename}", ctx=cpu(0))
        image = v[self.fno].asnumpy()      
        image = DropletDetection.DrawContours( DropletDetection.DetectEdgesInfo(image), image)
        
        return QImage(image, image.shape[0], image.shape[1], image.shape[0] * 3, QImage.Format_RGB888)

    def GoToFrame(self, fno):
        self.fno = fno
        self.ShowVideoFrame()

    def SetStartTime(self):
        self.startTime = self.fno
        self.setStartButton.setText(f"Frame: {self.fno}")

    def SetEndTime(self):
        self.endTime = self.fno
        self.setEndButton.setText(f"Frame: {self.fno}")