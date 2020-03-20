# -'- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mode_calibration
import mode_tracking

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main")
        self.setGeometry(300, 300, 400, 300)

        btn_start = QPushButton("시작", self)
        btn_start.setGeometry(10,10,185,280)
        btn_start.clicked.connect(self.tracking_clicked)

        btn_calibration = QPushButton("교정", self)
        btn_calibration.setGeometry(210, 10, 185, 280)
        btn_calibration.clicked.connect(self.calibration_clicked)
        btn_calibration.clicked.connect(QCoreApplication.instance().quit)

    def calibration_clicked(self):
        self.hide()
        return mode_calibration.calibration()

    def tracking_clicked(self):
        self.hide()
        return mode_tracking.tracking()
 #      self.hide()

def main():
    w = myWindow()
    w.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())