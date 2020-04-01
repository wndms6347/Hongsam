import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QPalette, QBrush
import mode_calibration
import pyautogui
import cv2

import mode_calibration_notice

screen_width, screen_height = pyautogui.size()


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calibration_loading")
        # 다음 버튼

        global screen_height
        global screen_width

        oImage = QImage("./image.jpg")
        sImage = oImage.scaled(QSize(screen_width, screen_height))

        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))

        self.setPalette(palette)

        textLabel2 = QLabel("Loading...", self)
        textLabel2.resize(1800, 250)
        textLabel2.move(600, 350)
        textLabel2.setStyleSheet("font: 100pt Comic Sans MS")

        self.w = None

    def load_next(self):
        self.w = mode_calibration_notice.widget_1()
        self.w.showFullScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MyWindow()
    form.showFullScreen()
    form.load_next()
    sys.exit(app.exec_())