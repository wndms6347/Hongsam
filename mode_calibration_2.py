# -'- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QPalette, QBrush
import mode_calibration
import pyautogui
import cv2

screen_width, screen_height = pyautogui.size()


class widget1(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        # 다음 버튼
        btn_next = QPushButton("다음", self)
        btn_next.setGeometry(900, 890, 200, 100)  # x, y, 버튼 가로, 버튼 세로
        btn_next.clicked.connect(self.next_clicked)

        global screen_height
        global screen_width

        oImage = QImage("./image.jpg")
        sImage = oImage.scaled(QSize(screen_width, screen_height))

        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))

        self.setPalette(palette)

        # 설명
        textLabel = QLabel("[조정 전 알림]", self)
        textLabel.resize(1800, 80)
        textLabel.move(400, 100)
        textLabel.setStyleSheet("font: 35pt Comic Sans MS")

        textLabel = QLabel("얼굴은 그대로 고정해주십시오.", self)
        textLabel.resize(1800, 80)
        textLabel.move(400, 200)
        textLabel.setStyleSheet("font: 30pt Comic Sans MS")

        textLabel1 = QLabel("붉은 원이 줄어들어 초록 원이 될 때까지 원을 응시해주세요.", self)
        textLabel1.resize(1800, 80)
        textLabel1.move(400, 300)
        textLabel1.setStyleSheet("font: 30pt Comic Sans MS")

        textLabel2 = QLabel("원은 총 9개가 나타납니다.", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(400, 400)
        textLabel2.setStyleSheet("font: 30pt Comic Sans MS")

        textLabel2 = QLabel("다음 버튼을 누르면 시점 조정을 시작합니다.", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(400, 500)
        textLabel2.setStyleSheet("font: 30pt Comic Sans MS")

    def next_clicked(self):
        self.close()
        return mode_calibration.calibration()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = widget1()
    form.showMaximized()
    sys.exit(app.exec_())