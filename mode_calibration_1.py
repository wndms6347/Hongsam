"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import sys
import cv2
import pyautogui
from PyQt5.QtGui import QImage, QPixmap, QPalette, QBrush, QPainter

from gaze_tracking import GazeTracking
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mode_calibration_2


screen_width, screen_height = pyautogui.size()
gaze = GazeTracking()



class widget_0(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Calibration_Start")

        # 다음 버튼
        btn_next = QPushButton("다음", self)
        btn_next.setGeometry(900, 890, 200, 100)  # x, y, 버튼 가로, 버튼 세로
        btn_next.clicked.connect(self.next_clicked)

        global screen_height
        global screen_width

        # 배경
        oImage = QImage("./image.jpg")
        sImage = oImage.scaled(QSize(screen_width,screen_height))

        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))

        self.setPalette(palette)
        self.w = None


        # 설명
        textLabel = QLabel("초록 십자가가 눈에 맞도록 얼굴 위치를 조정해주세요.", self)
        textLabel.resize(1800, 80)
        textLabel.move(400, 0)
        textLabel.setStyleSheet("font: 30pt Comic Sans MS")

        self.initUI()

    def initUI(self):
        self.cpt = cv2.VideoCapture(0)
        self.fps = 24
        #self.sens = 300
        _, self.img_o = self.cpt.read()
        self.img_o = cv2.cvtColor(self.img_o, cv2.COLOR_RGB2GRAY)
        cv2.imwrite('img_o.jpg', self.img_o)

        self.frame = QLabel(self)
        global screen_width, screen_height
        self.frame.setGeometry(200,100, screen_width-400, screen_height-300)
        self.frame.setScaledContents(True)

        self.start()

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 / self.fps)

    def nextFrameSlot(self):
        _, cam = self.cpt.read()
        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
        cam = cv2.flip(cam,1)

        gaze.refresh(cam)
        cam = gaze.annotated_frame()

        self.img_p = cv2.cvtColor(cam, cv2.COLOR_RGB2GRAY)
        cv2.imwrite('img_p.jpg', self.img_p)
        self.img_o = self.img_p.copy()
        img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix)

    def next_clicked(self):
        self.close()
        self.timer.stop()
        self.cpt.release()
        self.w = mode_calibration_2.widget_1()
        self.w.showFullScreen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = widget_0()
    myWindow.showFullScreen()
    sys.exit(app.exec_())



