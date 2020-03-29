"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import threading
import time
import sys
import cv2
import keyboard
import numpy as np
import pyautogui

import mode_calibration_2
import gaze_tracking
from gtts import gTTS
from playsound import playsound
import pandas as pd
import mode_tracking
import test
from gaze_tracking import GazeTracking

screen_width, screen_height = pyautogui.size()
gaze = GazeTracking()

nowOrder = 0
count = 0
timerRun = False
initializing = False

# 색깔
gray_color = (153, 153, 153)
green_color = (0, 255, 0)
# 민감도
sensitivity = 1
position = [[300, 500], [400, 500], [500, 500]]


width = 800
height = 600

play = False
init = True


def save_narrator(msg, file_name):
    engine = gTTS(text=msg, lang='en')
    engine.save("./audio./" + file_name + "_audio.mp3")
    print(msg + '의 음성이 [' + file_name + '_audio.mp3] 파일로 저장 되었습니다.')


# 음성 출력 함수
def play_narrator(msg, file_name):
    playsound("./audio./" + file_name + "_audio.mp3")
    print(msg + '가 출력됩니다. - 파일명 : [' + file_name + '_audio.mp3]')

# normalization 함수
def normalization(x, max_p, min_p):
    calc = (x - float(min_p)) / (float(max_p) - float(min_p))
    # print(calc)
    return calc



# 타이머 함수
def start_timer():
    global count
    global nowOrder

    print(count)
    timer = threading.Timer(1, start_timer)
    count += 1
    idx = 0
    col = 0
    if nowOrder is 9:
        print('initialize completed')
        timer.cancel()
        return


    if count % 3 is 0:
        play_narrator("효과음", "ding")
        nowOrder += 1
        print('stop')
        timer.cancel()
        time.sleep(1)
        start_timer()


    timer.start()



def calibration():

    global sensitivity
    global position

    webCam = cv2.VideoCapture(0, cv2.CAP_DSHOW)


    global h_ratio, h_count, v_ratio, v_count

    while True:
        # _, frame = webCam.read()


        _, camFrame = webCam.read()
        camFrame = cv2.flip(camFrame, 1)
        camFrame = cv2.resize(camFrame, dsize=(800, 600), interpolation=cv2.INTER_AREA)
        camFrame = camFrame[150:450, 200:600]
        camFrame = cv2.resize(camFrame, dsize=(800, 600), interpolation=cv2.INTER_AREA)

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(camFrame)


        camFrame = gaze.annotated_frame()

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


        look_play = True

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()


        cv2.putText(camFrame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        cv2.putText(camFrame, text1, (90, 100), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)


        ##~ 민감도 조절 ~##
        # 기본 회색 틀 (숫자, 원, 라인, 화살표라인)
        cv2.putText(camFrame, "1", (295, 550), cv2.FONT_HERSHEY_DUPLEX, 0.5, gray_color, 2)
        cv2.putText(camFrame, "2", (395, 550), cv2.FONT_HERSHEY_DUPLEX, 0.5, gray_color, 2)
        cv2.putText(camFrame, "3", (495, 550), cv2.FONT_HERSHEY_DUPLEX, 0.5, gray_color, 2)
        camFrame = cv2.circle(camFrame, (300, 500), 10, gray_color, -1)
        camFrame = cv2.circle(camFrame, (400, 500), 10, gray_color, -1)
        camFrame = cv2.circle(camFrame, (500, 500), 10, gray_color, -1)
        camFrame = cv2.line(camFrame, (300,500), (500,500), gray_color, 2)
        camFrame = cv2.arrowedLine(camFrame, (250,500), (200,500), gray_color, 2, tipLength= 0.5)
        camFrame = cv2.arrowedLine(camFrame, (550,500), (600,500), gray_color, 2, tipLength= 0.5)

        # 선택된 민감도(초록원)
        camFrame = cv2.circle(camFrame, (position[sensitivity][0], position[sensitivity][1]), 15, green_color, -1)

        # 키보드 입력 및 이벤트
        if keyboard.is_pressed('left arrow'):
            if sensitivity > 0:
                sensitivity -= 1
        elif keyboard.is_pressed('right arrow'):
            if sensitivity < 2:
                sensitivity += 1
        else:
            pass

        # 민감도 실제 조절
        if sensitivity is 0:
            gaze.change_limit(0)
        elif sensitivity is 1:
            gaze.change_limit(1)
        elif sensitivity is 2:
            gaze.change_limit(2)




        garo = screen_width/2 - 400


        # 전체 화면
        # cv2.moveWindow("calibration", int(garo), 0)
        cv2.namedWindow("calibration", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("calibration", camFrame)




        if cv2.waitKey(1) == 27:
            break

if __name__ == '__main__':
    calibration()