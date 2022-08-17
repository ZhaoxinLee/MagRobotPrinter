from TLV493D import TLV493D
from stepper import Stepper
from server import Server
from callbacks import GUI
from PyQt5 import QtWidgets
import sys

#sensor = TLV493D()
st = Stepper()
svr = Server(st)
#mm.svr = svr

if __name__ == "__main__":
    svr.start()
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
 
