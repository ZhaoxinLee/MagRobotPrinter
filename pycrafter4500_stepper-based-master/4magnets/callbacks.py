from PyQt5 import uic
from PyQt5.QtCore import QFile, QRegExp, QTimer
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu, QMessageBox
from stepper import Stepper

qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

st = Stepper()

class GUI(QMainWindow,Ui_MainWindow):
    def __init__(self):#,sensor):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.setupMotors()
        
#         self.setupTimer()
#         self.sensor = sensor

    def setupTimer(self):
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.update)
        self.my_timer.start(300) # msec
    
    def setupMotors(self):
        self.pbt_run.clicked.connect(self.on_btn_run)
        self.pbt_reset.clicked.connect(self.on_btn_reset)
        
    def update(self):
        s = self.sensor
        self.lbl_x.setNum(s.field[0])
        self.lbl_y.setNum(s.field[1])
        self.lbl_z.setNum(s.field[2])
        self.lbl_mag.setNum(s.mag)
        self.lbl_phi.setNum(s.phi)
        self.lbl_theta.setNum(s.theta)

    def on_btn_run(self):
        val_phi = self.spb_phi.value()
        val_alpha_21 = self.spb_alpha_21.value()
        val_alpha_22 = self.spb_alpha_22.value()
        val_alpha_31 = self.spb_alpha_31.value()
        val_alpha_32 = self.spb_alpha_32.value()
        st.motorgo(val_phi,val_alpha_21,val_alpha_22,val_alpha_31,val_alpha_32)
        
    def on_btn_reset(self):
        st.resetval()
