# -'- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *

import mode_calibration_loading
import mode_calibration_notice
import mode_calibration


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main")
        self.setGeometry(300, 300, 400, 300)

        btn_start = QPushButton("시작", self)
        btn_start.setGeometry(10, 10, 185, 280)
        btn_start.clicked.connect(self.tracking_clicked)

        btn_calibration = QPushButton("교정", self)
        btn_calibration.setGeometry(210, 10, 185, 280)
        btn_calibration.clicked.connect(self.calibration_clicked)

    def calibration_clicked(self):
        self.hide()
        self.w = mode_calibration_loading.MyWindow()
        self.w.showFullScreen()
        self.w.load_next()

    def tracking_clicked(self):
        self.hide()
        app2 = QApplication(sys.argv)
        myWindow2 = MyWindow()
        myWindow2.show()
        app2.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
