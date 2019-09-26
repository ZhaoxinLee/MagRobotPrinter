import syntax
import math
import time
import re
import pycrafter4500
import xlwt
import xlrd
import os
from textprocess import TextProcess
from client import Client
from motormanager import MotorManager
from gallery import Gallery
from PyQt5 import uic
from PyQt5.QtCore import QFile, QRegExp
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu, QMessageBox,QTableWidgetItem
#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================
# UI config
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

client = Client()
mm = MotorManager(client)
tp = TextProcess(client,mm)
#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================

class GUI(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupCallbacksLED()
        self.setupMotors()
        self.setupCallbacksEditor()
        self.setupGallery()

        self.time_ms = 0
        self.intensity = 0

    def setupCallbacksLED(self):
        self.btn_LED_set.clicked.connect(self.on_btn_LED_set)

    def setupMotors(self):
        self.btn_motor1_run.clicked.connect(self.on_btn_motor1_run)
        self.btn_motor2_run.clicked.connect(self.on_btn_motor2_run)
        self.btn_phi_theta_run.clicked.connect(self.on_btn_phi_theta_run)
        self.btn_phi_at_singularity.clicked.connect(self.on_btn_phi_at_singularity)
        self.btn_oscPitch.clicked.connect(self.on_btn_oscPitch)
        self.btn_oscYaw.clicked.connect(self.on_btn_oscYaw)
        self.btn_oscRandomize.clicked.connect(self.on_btn_oscRandomize)
    def setupCallbacksEditor(self):
        self.currentFilePath = ''
        self.btn_editor_update.clicked.connect(self.on_btn_editor_update)
        self.highlighter = syntax.Highlighter(self.editor.document())
    def setupGallery(self):
        self.btn_runGallery.clicked.connect(self.on_btn_runGallery)

    def about(self):
        QMessageBox.about(self, "About Pycrafter 4500",
                "<p>The <b>Pycrafter4500</b> is based on the DLPC350 USB API. " \
                "Please refer to <b>DLPC350 Programmer’s Guide</b> for a list of commands. " \
                "Many thanks to API Python wrapper <b>https://github.com/SivyerLab/pyCrafter4500</b>. " \
                "Tianqi</p>")

    def aboutFiles(self):
        QMessageBox.about(self, "About Files",
                "<p>"
                "<b>syntax</b> editor keyword highlighting <br>"
                "<b>Pixel</b> database class that handles pixel information <br>"
                "<b>callbacks</b> GUI class that handles callbacks <br>"
                "</p>")

    def newFile(self):
        self.editor.clear()
        self.currentFilePath = ''

    def openFile(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                    "txt Files (*.txt)")
        if path:
            self.currentFilePath = path
            self.setWindowTitle(path)
            inFile = QFile(path)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = inFile.readAll()
                text = str(text, encoding='ascii')
                self.editor.setPlainText(text)

    def saveFile(self):
        if self.currentFilePath == '':
            self.currentFilePath, _ = QFileDialog.getSaveFileName(self, "Save file", '',
                    "txt Files (*.txt)")
        else:
            msg = QMessageBox()
            msg.setText("Do you want to save your changes?")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            msg.setWindowTitle("Confirm Save")
            ret = msg.exec_()
            if ret == 2048:
                pass
            else:
                return
        path = self.currentFilePath
        saveFile = open(path, "w")
        text = str(self.editor.toPlainText())
        saveFile.write(text)
        saveFile.close()

    def newGallery(self):
        self.tbl_gallery.clearContents()
        self.pte_galleryTitle.clear()
        self.currentFilePath = ''

    def openGallery(self,path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                    ".xls(*.xls)")
        if path:
            self.currentFilePath = path
            self.setWindowTitle(path)
            book = xlrd.open_workbook(self.currentFilePath)
            sheet = book.sheets() [0]
            data = [[int(sheet.cell_value(r,c)) for c in range (sheet.ncols)]for r in range(sheet.nrows)]
            for i in range(len(data)):
                for j in range(len(data[i])):
                    self.tbl_gallery.setItem(i,j,QTableWidgetItem(str(data[i][j])))
            base = os.path.basename(path)
            self.pte_galleryTitle.setPlainText(os.path.splitext(base)[0])

    def saveGallery(self):
        if self.currentFilePath == '':
            self.currentFilePath, _ = QFileDialog.getSaveFileName(self, "Save file", '',
                    ".xls(*.xls)")
        else:
            msg = QMessageBox()
            msg.setText("Do you want to save your changes?")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            msg.setWindowTitle("Confirm Save")
            ret = msg.exec_()
            if ret == 2048:
                pass
            else:
                return
        path = self.currentFilePath
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("Sheet1", cell_overwrite_ok=True)
        for i in range(self.tbl_gallery.rowCount()):
            for j in range(self.tbl_gallery.columnCount()):
                if self.tbl_gallery.item(i, j) != None:
                    teext = int(self.tbl_gallery.item(i, j).text())
                    sheet.write(i, j, teext)
        wbk.save(self.currentFilePath)

    def setupFileMenu(self):
        fileMenu = QMenu("&File", self)
        self.menuBar().addMenu(fileMenu)
        fileMenu.addAction("&New Editor", self.newFile, "Ctrl+N")
        fileMenu.addAction("&New Gallery", self.newGallery, "Ctrl+Shift+N")
        fileMenu.addAction("&Open Editor...", self.openFile, "Ctrl+O")
        fileMenu.addAction("&Open Gallery", self.openGallery, "Ctrl+Shift+O")
        fileMenu.addAction("&Save Editor", self.saveFile, "Ctrl+S")
        fileMenu.addAction("&Save Gallery", self.saveGallery, "Ctrl+Shift+S")
        fileMenu.addAction("E&xit", QApplication.instance().quit, "Ctrl+Q")

    def setupHelpMenu(self):
        helpMenu = QMenu("&Help", self)
        self.menuBar().addMenu(helpMenu)
        helpMenu.addAction("&About", self.about)
        helpMenu.addAction("About &Files", self.aboutFiles)

    def on_btn_LED_set(self):
        self.time_ms = self.spb_LED_exposureTime.value()
        self.intensity = 0xFF - self.spb_LED_intensity.value()
        if self.time_ms == 0:
            pycrafter4500.set_LED_current(self.intensity)
        else:
            pycrafter4500.set_LED_current(self.intensity)
            time.sleep(self.time_ms/1000)
            pycrafter4500.set_LED_current(255)

    def on_btn_motor1_run(self):
        val = self.spb_motor1_step.value()
        mm.motorgo(0,val)

    def on_btn_motor2_run(self):
        val = self.spb_motor2_step.value()
        mm.motorgo(1,val)

    def on_btn_phi_run(self):
        val = self.spb_phi.value()
        mm.phiGo(val)

    def on_btn_theta_run(self):
        val = self.spb_theta.value()
        mm.thetaGo(val)
    def on_btn_phi_theta_run(self):
        phi = self.spb_phi.value()
        theta = self.spb_theta.value()
        mm.magneticFieldGo(phi,theta)
    def on_btn_phi_at_singularity(self):
        phi = self.spb_phi_at_singularity.value()
        mm.setPhiSingularity(phi)
    def on_btn_oscPitch(self):
        mm.oscPitch()
    def on_btn_oscYaw(self):
        mm.oscYaw()
    def on_btn_oscRandomize(self):
        mm.randomize()
    def on_btn_runGallery(self):
        title = self.pte_galleryTitle.toPlainText()
        list = []
        for i in range(self.tbl_gallery.rowCount()):
            new = []
            for j in range(4):
                if self.tbl_gallery.item(i, j) != None:
                    new.append(int(self.tbl_gallery.item(i, j).text()))
                else:
                    new.append('')
            list.append(new)
        print(list)
        gl = Gallery(title, list, self.time_ms, self.intensity, self.currentFilePath, mm)
        gl.run_field()
        #gl.show_slides()
        gl.run()


    def on_btn_editor_update(self):
        tp.clear()
        tp.set_exposureTime(self.spb_LED_exposureTime.value())
        tp.set_intensityUV(self.spb_LED_intensity.value())
        tp.process(self.editor.toPlainText().splitlines())
