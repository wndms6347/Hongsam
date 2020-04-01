import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QPalette, QBrush
import mode_calibration
import pyautogui
import cv2
import mode_calibration_start

screen_width, screen_height = pyautogui.size()


class widget_2(QWidget):

    gaze = [0, 0, 0, 0]

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Calibration_check")
        # 다음 버튼

        global screen_height
        global screen_width

        oImage = QImage("./image.jpg")
        sImage = oImage.scaled(QSize(screen_width, screen_height))

        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))

        self.setPalette(palette)

        # 설명
        textLabel = QLabel("[민감도 확인]  (0,1,2)", self)
        textLabel.resize(1800, 80)
        textLabel.move(350, 100)
        textLabel.setStyleSheet("font: 35pt Comic Sans MS")

        textLabel = QLabel("위: ", self)
        textLabel.resize(1800, 80)
        textLabel.move(350, 250)
        textLabel.setStyleSheet("font: 30pt Comic Sans MS")


        textLabel1 = QLabel("아래: ", self)
        textLabel1.resize(1800, 80)
        textLabel1.move(350, 350)
        textLabel1.setStyleSheet("font: 30pt Comic Sans MS")

        textLabel1 = QLabel("왼쪽: ", self)
        textLabel1.resize(1800, 80)
        textLabel1.move(350, 450)
        textLabel1.setStyleSheet("font: 30pt Comic Sans MS")

        textLabel2 = QLabel("오른쪽: ", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(350, 550)
        textLabel2.setStyleSheet("font: 30pt Comic Sans MS")

        textLabel2 = QLabel("맞으시다면 'Play' 버튼을 누르세요.", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(350, 700)
        textLabel2.setStyleSheet("font: 25pt Comic Sans MS")

        textLabel2 = QLabel("다시 조정을 원하시면 'Back' 을 누르세요.", self)
        textLabel2.resize(1800, 80)
        textLabel2.move(350, 750)
        textLabel2.setStyleSheet("font: 25pt Comic Sans MS")

        # 이전 버튼
        btn_next = QPushButton("Back", self)
        btn_next.setGeometry(650, 890, 200, 100)  # x, y, 버튼 가로, 버튼 세로
        btn_next.clicked.connect(self.back_clicked)

        # 플레이 버튼
        btn_next = QPushButton("Play", self)
        btn_next.setGeometry(1150, 890, 200, 100)  # x, y, 버튼 가로, 버튼 세로
        btn_next.clicked.connect(self.play_clicked)

        self.w = None

    def back_clicked(self):
        self.close()

    def play_clicked(self):
        print('b')

    def pass_value(self, tmp):
        self.gaze = tmp

        # 위
        textLabel = QLabel(repr(self.gaze[0]), self)
        textLabel.resize(1800, 80)
        textLabel.move(450, 250)
        textLabel.setStyleSheet("font: 30pt Comic Sans MS")

        # 아래
        textLabel = QLabel(repr(self.gaze[1]), self)
        textLabel.resize(1800, 80)
        textLabel.move(500, 350)
        textLabel.setStyleSheet("font: 30pt Comic Sans MS")

        # 왼쪽
        textLabel = QLabel(repr(self.gaze[2]), self)
        textLabel.resize(1800, 80)
        textLabel.move(500, 450)
        textLabel.setStyleSheet("font: 30pt Comic Sans MS")

        # 오른쪽
        textLabel = QLabel(repr(self.gaze[3]), self)
        textLabel.resize(1800, 80)
        textLabel.move(550, 550)
        textLabel.setStyleSheet("font: 30pt Comic Sans MS")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = widget_2()
    form.showFullScreen()
    sys.exit(app.exec_())