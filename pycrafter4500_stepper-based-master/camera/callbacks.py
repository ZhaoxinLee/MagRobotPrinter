import math
import time
from vision import Vision
from PyQt5 import uic
from PyQt5.QtCore import QFile, QRegExp, QTimer
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu, QMessageBox,QTableWidgetItem
#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================
# UI config
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

vision = Vision(mode='Video')
# vision = Vision(mode='Camera')
#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================

class GUI(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        # self.updateRate = int(round(1000/vision.getFrameRate()))
        self.updateRate = 15 #ms, considering delay due to program running,
        # the frame rate of camera is measured to be around 30fps when updateRate is 15ms
        self.setupUi(self)

        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupObjectDetection()
        self.setupTimer()

    def setupTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.updateRate) # msec

    def update(self):
        vision.updateFrame()

    def setupObjectDetection(self):     ##
        self.btn_original.clicked.connect(self.on_btn_runOriginal)
        self.btn_grayscale.clicked.connect(self.on_btn_runGrayscale)
        self.btn_binary.clicked.connect(self.on_btn_runBinary)
        self.btn_detectContour.clicked.connect(self.on_btn_runObjectDetection)
        self.btn_susContour.clicked.connect(self.on_btn_susObjectDetection)
        self.btn_clearContour.clicked.connect(self.on_btn_clearObjectDetection)
        self.btn_snapshot.clicked.connect(self.on_btn_snapshot)
        self.btn_startRecording.clicked.connect(self.on_btn_startRecording)
        self.btn_stopRecording.clicked.connect(self.on_btn_stopRecording)

    def about(self):
        QMessageBox.about(self, "About Vision",
                "<p>For the model of <b>Camera</b>, please refer to OV2710 Webcam on Amazon. <br>" \
                "The <b>snapshot</b> will be stored under path <i>/snapshot</i>, the <b>video</b> recorded will be stored under path <i>/video</i>."
                "<p align='right'>Jason</p>")

    def setupFileMenu(self):
        fileMenu = QMenu("&File", self)
        self.menuBar().addMenu(fileMenu)
        fileMenu.addAction("E&xit", QApplication.instance().quit, "Ctrl+Q")

    def setupHelpMenu(self):
        helpMenu = QMenu("&Help", self)
        self.menuBar().addMenu(helpMenu)
        helpMenu.addAction("&About", self.about)

    def on_btn_runOriginal(self):
        vision.setOriginal()

    def on_btn_runGrayscale(self):
        vision.setGrayscale()

    def on_btn_runBinary(self):
        vision.setThreshold(self.spb_threshval.value(),self.spb_maxval.value())

    def on_btn_runObjectDetection(self):
        vision.setObjectDetection(self.spb_threshval.value(),self.spb_maxval.value())

    def on_btn_susObjectDetection(self):
        vision.susObjectDetection()

    def on_btn_clearObjectDetection(self):
        vision.setOriginal()

    def on_btn_snapshot(self):
        vision.setSnapshot()

    def on_btn_startRecording(self):
        vision.startRecording(self.pte_filename.toPlainText())

    def on_btn_stopRecording(self):
        vision.stopRecording()
