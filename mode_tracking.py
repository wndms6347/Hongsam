import cv2
import pyautogui
from Tracking import GazeTracking
import pandas as pd
import threading
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
import sys

# 사용자 해상도를 가져온다
screen_width, screen_height = pyautogui.size()

# csv 파일을 불러온다
output_eyeratio = pd.read_csv('./eye_ratio.csv', names = ['num','h_ratio','v_ratio'])

# normalization 함수
def normalization(x, max_p, min_p):
    calc = (x - float(min_p)) / (float(max_p) - float(min_p))
    return calc

# pyautogui 설정
pyautogui.FAILSAFE = False # 화면 밖을 나가거나 오류가 생겨도 계속 진행

# gaze, webcam 할당
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# 마우스 이동 함수
def move_mouse():
    global output

    # 만약 동공을 찾았다면..
    if gaze.pupils_located:
        print(output)
        pyautogui.moveTo(((screen_width* gaze.horizontal_ratio()) - 576) * 1.74, ((screen_height*gaze.vertical_ratio()) - 540) * 1.35,5)
        #pyautogui.moveTo(screen_width/2, screen_height * normalization(gaze.vertical_ratio(),output_eyeratio.loc[8,'v_ratio'],output_eyeratio.loc[4,'v_ratio']) )
    else:
        #pyautogui.moveTo(screen_width/2,screen_height/2)
        print("err")

class MainWindow(QWidget):
    # 윈도우 초기화
    def __init__(self):
        super().__init__()
        self.init_ui()

    # 윈도우 설정
    def init_ui(self):
        self.setGeometry(0,0,screen_width,screen_height) # x, y, width, height
        self.setWindowTitle('mode_tracking')

        # 좌, 우측 pupil coord를 표시하기 위한 라벨 생성
        self.label = QLabel(self)
        self.label.setGeometry(90, 60, 200, 20)

        self.label2 = QLabel(self)
        self.label2.setGeometry(90, 100, 200, 20)

        # 영상 가져오기
        _, cam_frame = webcam.read()
        cam_frame = cv2.flip(cam_frame, 1)  # 좌우반전

        # 해상도를 높힌다 -> 일반적으로 INTER_AREA는 shrimp할 때 사용하므로 INTER_CUBIC으로 바꿨다.
        # cam_frame = cv2.resize(cam_frame, dsize=(800, 600), interpolation=cv2.INTER_AREA)
        # 배수 Size지정
        # frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # 프레임 사이즈 측정
        rows, cols = cam_frame.shape[:2]

        # 변환 행렬, X축으로 10, Y축으로 20 이동
        # M = np.float32([[1, 0, 10], [0, 1, 20]])
        # cam_frame = cv2.warpAffine(cam_frame, M, (cols, rows))

        # GazeTracking에 분석하기 위해서 프레임을 토스함
        gaze.refresh(cam_frame)
        cam_frame = gaze.annotated_frame()

        # Text 관리
        text = ""
        text1 = ""
        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"
        if gaze.is_up():
            text1 = "Looking up"
        elif gaze.is_down():
            text1 = "Looking down"

        # 좌, 우측 좌표를 가져온다
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        # 좌, 우측 좌표를 라벨에 집어넣기
        self.label.setText("Left pupil: " + str(left_pupil))
        self.label2.setText("right pupil: " + str(right_pupil))

    # 트래킹을 실행한다.
    def tracking():
        while True:
            # frame에 텍스트를 붙힌다
            cv2.putText(cam_frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
            cv2.putText(cam_frame, text1, (90, 100), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
            cv2.putText(cam_frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(cam_frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            # 화면을 띄운다
            # cv2.imshow("tracking", cam_frame)



# 만약 MAIN console로 켜진다면 tracking() 함수를 실행한다
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    # tracking()