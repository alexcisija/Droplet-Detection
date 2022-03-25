import sys, cv2

import DropletDetection
import numpy as np
from PyQt5.QtWidgets import QSlider, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtGui import QPixmap, QImage

from decord import VideoReader, cpu, gpu

class FrameView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

    def addWidget(self, widget, x, y, r, c):
        self.layout.addWidget(widget, x, y, r, c)
        self.setLayout(self.layout)



class Ui_VideoAnalysis(QMainWindow):
    def setupUi(self, Frame):
        self.translate = QtCore.QCoreApplication.translate
        self.startTime = 0
        self.endTime = 0

        self.CreateWindow(Frame)

        self.frameView = FrameView()
        self.openVideoButton = self.AddButton("Open Video")
        self.openVideoButton.clicked.connect(self.OpenVideo)
        self.frameView.addWidget(self.openVideoButton, 2, 0, 1, 1)


        self.setCentralWidget(self.frameView)



    def CreateWindow(self, Frame):
        objName = "Frame"
        (width, height) = (800, 500)

        self.Frame = Frame
        self.Frame.resize(width, height)
        self.Frame.setObjectName(objName)
        self.Frame.setWindowTitle( self.translate(objName, "Droplet Analysis") )

    def AddButton(self, name):
        pushButton = QtWidgets.QPushButton(name, self)
        pushButton.setObjectName(name)
        pushButton.setFixedSize(100, 40)
        pushButton.setStyleSheet(
            """
            background-color: black;
            color: white;
            border-radius: 10px;
            """
        )
        
        return pushButton

    def AddFrameView(self):
        duration = len(VideoReader(f"{self.filename}", ctx=cpu(0))) - 1

        self.frameWindow = QLabel()
        self.frameWindow.setStyleSheet("background-color: red; border: 5px solid black; border-radius: 8px;")    

        self.nextFrameButton = self.AddButton("Next Frame")
        self.nextFrameButton.clicked.connect(self.NextFrame)

        self.setStartButton = self.AddButton(f"Set Start: {self.startTime}")
        self.setStartButton.clicked.connect(self.SetStartTime)
        self.frameView.addWidget(self.setStartButton, 2, 2, 1, 1)

        self.analyzeButton = self.AddButton(f"Start Analysis")
        self.analyzeButton.clicked.connect(lambda: DropletDetection.Analyze(self.filename))
        self.frameView.addWidget(self.analyzeButton, 2, 4, 1, 1)

        self.setEndButton = self.AddButton(f"Set End: {self.endTime}")
        self.setEndButton.clicked.connect(self.SetEndTime)
        self.frameView.addWidget(self.setEndButton, 2, 3, 1, 1)

        self.frameView.addWidget(self.frameWindow, 0, 0, 1, -1)
        self.frameView.addWidget(self.nextFrameButton, 2, 1, 1, 1)

        self.frameNumber = QLabel(f"{self.fno}")

        self.frameSlider = QSlider(QtCore.Qt.Horizontal, self)
        self.frameSlider.sliderReleased.connect(lambda: self.GoToFrame(self.frameSlider.value()))
        self.frameSlider.setRange(0, duration)

        self.frameView.addWidget(self.frameSlider, 1, 0, 1, -1)
        # self.frameView.addWidget(self.frameNumber, 2, 2, 1, 1)

        self.ShowVideoFrame()

    def OpenVideo(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open Video", filter="Videos (*.mp4)")[0]
        self.fno = 0
        self.AddFrameView()

    def ShowVideoFrame(self):        
        self.pixmap = QPixmap(self.FetchVideoFrame())
        self.pixmap = self.pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.frameWindow.setPixmap(self.pixmap)
        self.frameWindow.setScaledContents(True)

    def FetchVideoFrame(self):
        v = VideoReader(f"{self.filename}", ctx=cpu(0))
        image = v[self.fno].asnumpy()      
        # image = DropletDetection.DrawContours( DropletDetection.DetectEdgesInfo(image), image)
        
        return QImage(image, image.shape[0], image.shape[1], image.shape[0] * 3, QImage.Format_RGB888)

    def NextFrame(self):
        self.GoToFrame(self.fno + 1)

    def GoToFrame(self, fno):
        self.fno = fno
        self.frameNumber.setText(f"{fno}")
        self.ShowVideoFrame()

    def SetStartTime(self):
        self.startTime = self.fno
        self.setStartButton.setText(f"Set Start: {self.fno}")

    def SetEndTime(self):
        self.endTime = self.fno
        self.setEndButton.setText(f"Set End: {self.fno}")