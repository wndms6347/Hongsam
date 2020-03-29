# -'- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QPalette, QBrush
import mode_calibration_start
import pyautogui
import cv2


screen_width, screen_height = pyautogui.size()


class widget_1(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Calibration_ready")
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
        textLabel.move(350, 100)
        textLabel.setStyleSheet("font: 30pt Comic Sans MS")

        textLabel = QLabel("1. 눈동자에 십자가가 뜨도록 얼굴 위치를 맞추고 고정하세요.", self)
        textLabel.resize(1800, 80)
        textLabel.move(350, 200)
        textLabel.setStyleSheet("font: 25pt Comic Sans MS")

        textLabel1 = QLabel("2. 음성이 재생됩니다.", self)
        textLabel1.resize(1800, 80)
        textLabel1.move(350, 300)
        textLabel1.setStyleSheet("font: 25pt Comic Sans MS")

        textLabel1 = QLabel("각각 left, right, up, down 이 맞게 뜨는지 확인하시고", self)
        textLabel1.resize(1800, 80)
        textLabel1.move(350, 350)
        textLabel1.setStyleSheet("font: 25pt Comic Sans MS")

        textLabel2 = QLabel("아래의 민감도 조절 버튼으로 맞게 조정해주세요.", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(350, 400)
        textLabel2.setStyleSheet("font: 25pt Comic Sans MS")

        textLabel2 = QLabel("(민감도는 키보드 <-, -> 버튼으로 조정합니다)", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(350, 450)
        textLabel2.setStyleSheet("font: 25pt Comic Sans MS")

        textLabel2 = QLabel("3. 스페이스바를 누르면 음성이 다시 재생됩니다.", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(350, 550)
        textLabel2.setStyleSheet("font: 25pt Comic Sans MS")

        textLabel2 = QLabel("4. 모두 읽으셨다면, 다음 버튼을 눌러 진행해주십시오.", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(350, 650)
        textLabel2.setStyleSheet("font: 25pt Comic Sans MS")

        self.w = None

    def next_clicked(self):
        self.close()
        return mode_calibration_start.calibration()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = widget_1()
    form.showFullScreen()
    sys.exit(app.exec_())