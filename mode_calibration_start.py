"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import sys
import threading
import time
import cv2
import keyboard
import pyautogui
from PyQt5.QtWidgets import QWidget, QApplication

import mode_calibration_check
from playsound import playsound
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
darkGray_color = (51, 51, 51)
white_color = (255, 255, 255)
red_color = (153, 153, 204)
# 민감도
sensitivity = 1  # (0~2)
position_s = [[300, 500], [400, 500], [500, 500]]
# 설정된 민감도
set_sen_u = 1
set_sen_d = 1
set_sen_l = 1
set_sen_r = 1
is_set_u = False
is_set_d = False
is_set_l = False
is_set_r = False
# 방향
direction = 0  # (0~4, 위, 아래, 왼쪽, 오른쪽)
position_d = [[700, 185, 750, 235], [700, 245, 750, 295], [700, 305, 750, 355], [700, 365, 750, 415]]


# 이전 폼
parent_form = 1

width = 800
height = 600

play = False
init = True

# 음성 출력 함수
def play_narrator(msg, file_name):
    playsound("./audio./" + file_name + "_audio.mp3")
    print(msg + '가 출력됩니다. - 파일명 : [' + file_name + '_audio.mp3]')


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
    global position_s
    global direction
    global position_d
    global is_set_u
    global is_set_d
    global is_set_l
    global is_set_r
    global set_sen_d
    global set_sen_l
    global set_sen_r
    global set_sen_u

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


        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()


        cv2.putText(camFrame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        cv2.putText(camFrame, text1, (90, 100), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)


        ##~ 민감도 조절 ~##
        # 기본 회색 틀 (숫자, 원, 텍스트, 네모, 라인, 화살표라인)
        cv2.putText(camFrame, "0", (295, 540), cv2.FONT_HERSHEY_DUPLEX, 0.6, gray_color, 1)
        cv2.putText(camFrame, "1", (395, 540), cv2.FONT_HERSHEY_DUPLEX, 0.6, gray_color, 1)
        cv2.putText(camFrame, "2", (495, 540), cv2.FONT_HERSHEY_DUPLEX, 0.6, gray_color, 1)
        camFrame = cv2.circle(camFrame, (300, 500), 10, gray_color, -1)
        camFrame = cv2.circle(camFrame, (400, 500), 10, gray_color, -1)
        camFrame = cv2.circle(camFrame, (500, 500), 10, gray_color, -1)
        camFrame = cv2.line(camFrame, (300,500), (500,500), gray_color, 2)
        camFrame = cv2.arrowedLine(camFrame, (250,500), (200,500), gray_color, 2, tipLength= 0.5)
        camFrame = cv2.arrowedLine(camFrame, (550,500), (600,500), gray_color, 2, tipLength= 0.5)
        # 800 600 네모
        camFrame = cv2.rectangle(camFrame, (700, 185), (750, 235), gray_color, -1)
        camFrame = cv2.rectangle(camFrame, (700, 245), (750, 295), gray_color, -1)
        camFrame = cv2.rectangle(camFrame, (700, 305), (750, 355), gray_color, -1)
        camFrame = cv2.rectangle(camFrame, (700, 365), (750, 415), gray_color, -1)
        camFrame = cv2.line(camFrame, (725, 190), (725, 400), gray_color, 2)
        camFrame = cv2.arrowedLine(camFrame, (725, 155), (725, 105), gray_color, 2, tipLength= 0.5)
        camFrame = cv2.arrowedLine(camFrame, (725, 445), (725, 495), gray_color, 2, tipLength= 0.5)
        cv2.putText(camFrame, "up", (710, 215), cv2.FONT_HERSHEY_DUPLEX, 0.7, darkGray_color, 1)
        cv2.putText(camFrame, "down", (700, 275), cv2.FONT_HERSHEY_DUPLEX, 0.6, darkGray_color, 1)
        cv2.putText(camFrame, "left", (706, 335), cv2.FONT_HERSHEY_DUPLEX, 0.7, darkGray_color, 1)
        cv2.putText(camFrame, "right", (703, 395), cv2.FONT_HERSHEY_DUPLEX, 0.6, darkGray_color, 1)

        # 키보드 입력 및 이벤트
        if keyboard.is_pressed('left arrow'):
            if sensitivity > 0:
                sensitivity -= 1

        elif keyboard.is_pressed('right arrow'):
            if sensitivity < 2:
                sensitivity += 1

        elif keyboard.is_pressed('up arrow'):
            if direction > 0:
                direction -= 1

        elif keyboard.is_pressed('down arrow'):
            if direction < 3:
                direction += 1

        elif keyboard.is_pressed('enter'):
            if direction is 0:
                set_sen_u = sensitivity
                is_set_u = True
            elif direction is 1:
                set_sen_d = sensitivity
                is_set_d = True
            elif direction is 2:
                set_sen_l = sensitivity
                is_set_l = True
            elif direction is 3:
                set_sen_r = sensitivity
                is_set_r = True
            thread_sound = threading.Thread(target=play_narrator, args=("효과음", "ding",))
            thread_sound.start()


        elif keyboard.is_pressed('backspace'):
            if direction is 0 and is_set_u is True:
                is_set_u = False
                sensitivity = 1
                set_sen_u = 1
            elif direction is 1 and is_set_d is True:
                is_set_d = False
                sensitivity = 1
                set_sen_d = 1
            elif direction is 2 and is_set_l is True:
                is_set_l = False
                sensitivity = 1
                set_sen_l = 1
            elif direction is 3 and is_set_r is True:
                is_set_r = False
                sensitivity = 1
                set_sen_r = 1

        elif keyboard.is_pressed('n'):
            parent_form.w.open()
        else:
            pass

        # 선택된 민감도(초록원, 초록네모)
        camFrame = cv2.circle(camFrame, (position_s[sensitivity][0], position_s[sensitivity][1]), 15, green_color,
                              -1)
        camFrame = cv2.rectangle(camFrame, (position_d[direction][0], position_d[direction][1]),
                                 (position_d[direction][2], position_d[direction][3]), green_color, -1)
        if direction is 0:
            if is_set_u is True:
                camFrame = cv2.rectangle(camFrame, (700, 185), (750, 235), red_color, -1)
                sensitivity = set_sen_u
            cv2.putText(camFrame, "up", (710, 215), cv2.FONT_HERSHEY_DUPLEX, 0.7, white_color, 1)
        elif direction is 1:
            if is_set_d is True:
                camFrame = cv2.rectangle(camFrame, (700, 245), (750, 295), red_color, -1)
                sensitivity = set_sen_d
            cv2.putText(camFrame, "down", (700, 275), cv2.FONT_HERSHEY_DUPLEX, 0.6, white_color, 1)
        elif direction is 2:
            if is_set_l is True:
                camFrame = cv2.rectangle(camFrame, (700, 305), (750, 355), red_color, -1)
                sensitivity = set_sen_l
            cv2.putText(camFrame, "left", (706, 335), cv2.FONT_HERSHEY_DUPLEX, 0.7, white_color, 1)
        elif direction is 3:
            if is_set_r is True:
                camFrame = cv2.rectangle(camFrame, (700, 365), (750, 415), red_color, -1)
                sensitivity = set_sen_r
            cv2.putText(camFrame, "right", (703, 395), cv2.FONT_HERSHEY_DUPLEX, 0.6, white_color, 1)

        # 민감도 임시 조절과 실제 조절
        if direction is 0 and is_set_u is False:
            gaze.change_limit(0, sensitivity)
        elif direction is 1 and is_set_d is False:
            gaze.change_limit(1, sensitivity)
        elif direction is 2 and is_set_l is False:
            gaze.change_limit(2, sensitivity)
        elif direction is 3 and is_set_r is False:
            gaze.change_limit(3, sensitivity)

        garo = screen_width/2 - 400


        # 전체 화면
        # cv2.moveWindow("calibration", int(garo), 0)
        cv2.namedWindow("calibration", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("calibration", camFrame)




        if cv2.waitKey(1) == 27:
            break
def pass_form(form):
    global parent_form

    parent_form = form

class widget_3(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Calibration_start")
        self.setGeometry(0, 0, 300, 300)

        self.w = None

    def open(self):
        self.w = mode_calibration_check.widget_2()
        self.w.pass_value([set_sen_u, set_sen_d, set_sen_l, set_sen_r])
        self.w.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form2 = widget_3()
    form2.hide()
    calibration()
    sys.exit(app.exec_())