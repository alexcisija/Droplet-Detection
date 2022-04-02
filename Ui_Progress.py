import cv2
import threading
import math
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5 import QtCore, QtWidgets, QtGui

import DropletDetection

class QVComponent(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignVCenter)
        self.setLayout(self.layout)

    def addWidget(self, widget, alignment=QtCore.Qt.AlignCenter):
        self.layout.addWidget(widget, alignment=alignment)
        self.setLayout(self.layout)

class ProgressWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int, int)

    def __init__(self, filename, start, end):
        super().__init__()
        self.filename = filename
        self.start = start
        self.end = end

    def run(self):
        video = cv2.VideoCapture(self.filename)

        with open("./output.csv", 'w+') as f:
            for i in range(self.start, self.end): #Make sure to seek to user selected start of video.
                success, image = video.read()
                circles = DropletDetection.DetectEdgesInfo(image) # Should implement radius calculation in the future.
                self.progress.emit(i+1, self.end-self.start) #self.SetProgressBar(i, end-start)
                
                for circle in circles: f.write(f"{circle[2]}, ")
                f.write("\n")

        video.release()
        self.finished.emit()      

class Ui_Progress(QMainWindow):
    def __init__(self, filename, startTime, endTime):
        super().__init__()
        self.setWindowIcon(QIcon('./1x/favicon.ico'))

        self.filename = filename
        self.startTime = startTime
        self.endTime = endTime

        self.setupUi(self)
        self.Analyze()

    def setupUi(self, Frame):
        self.translate = QtCore.QCoreApplication.translate

        self.CreateWindow(Frame)
        self.progressView = QVComponent()

        self.progressText = QLabel(f"Analyzing 0 / {self.endTime - self.startTime}")
        self.progressText.setStyleSheet(
            """
            font-size: 16px;
            color: #aaaaaa;
            font-weight: bold;
            """
        )
        self.progressView.addWidget(self.progressText)
        
        self.progressBar = QLabel()
        self.progressBar.setFixedSize(1, 20)
        self.progressBar.setStyleSheet(
            """
            border: 1px solid #dddddd;
            border-radius: 5px;
            background-color: #6edbcc;
            """
        )
        self.progressView.addWidget(self.progressBar)
        

        self.cancelButton = self.AddButton(f"Cancel")
        self.cancelButton.clicked.connect(self.CloseWindow)
        self.progressView.addWidget(self.cancelButton)

        self.setCentralWidget(self.progressView)

    def CreateWindow(self, Frame):
        objName = "Frame"
        (width, height) = (700, 500)

        self.Frame = Frame
        self.Frame.resize(width, height)
        self.Frame.setObjectName(objName)
        self.Frame.setWindowTitle( self.translate(objName, "Project Symphony | Analyzing") )

    def AddButton(self, name):
        pushButton = QPushButton(name, self)
        pushButton.setObjectName(name)
        pushButton.setFixedSize(130, 50+16)
        pushButton.setStyleSheet(
            """
            background-color: #ff8f8f;
            color: #eeeeee;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            margin: 8px 0;
            """
        )
        
        return pushButton

    def CloseWindow(self):
        self.close()

    def SetProgressBar(self, frame, totalFrames, maxWidth=600):
        print(frame, totalFrames, maxWidth)
        self.progressBar.setFixedSize(math.floor(frame/totalFrames * maxWidth), 20)
        self.progressText.setText(f"Analyzing {frame} / {totalFrames}")
        if frame == totalFrames: self.ShowDoneButton()

    def ShowDoneButton(self):
        self.cancelButton.setText("Done")
        self.cancelButton.setStyleSheet(
            """
            background-color: #6edbcc;
            color: #ffffff;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            margin: 8px 0;
            """
        )

    def Analyze(self):
        self.analyzeThread = QtCore.QThread()
        self.worker = ProgressWorker(self.filename, self.startTime, self.endTime)

        self.worker.moveToThread(self.analyzeThread)

        self.analyzeThread.started.connect(self.worker.run)
        self.worker.finished.connect(self.analyzeThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.analyzeThread.finished.connect(self.analyzeThread.deleteLater)
        self.worker.progress.connect(self.SetProgressBar)

        self.analyzeThread.start()
