"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import threading
import time
import sys
import cv2
import numpy as np
import pyautogui

import mode_calibration_2
from gaze_tracking import GazeTracking
from gtts import gTTS
from playsound import playsound
import pandas as pd
import mode_tracking
import test

screen_width, screen_height = pyautogui.size()
gaze = GazeTracking()

nowOrder = 0
count = 0
timerRun = False
initializing = False

circle_radius = 40

#circle 크기 변화를 위한 변수
circle_radius_change = circle_radius
circle_is_change = True
circle_count = 3
red_color = (0,0,255)
green_color = (0,255,0)
circle_color = red_color

width = 800
height = 600

position = position = [[circle_radius, circle_radius], [int(width/2), circle_radius], [int(width - circle_radius), circle_radius],
            [circle_radius, int(height/2)], [int(width/2), int(height/2)], [int(width - circle_radius), int(height/2)],
            [circle_radius, int(height-circle_radius)], [int(width/2), int(height-circle_radius)], [int(width - circle_radius), int(height-circle_radius)]]
red_color = (0, 0, 255)

look_play = False
play = False
init = True

output_file = "eye_ratio.csv"

global h_ratio, h_count, v_ratio, v_count
h_ratio = 0
h_count = 0
v_ratio = 0
v_count = 0

global eye_ratio
eye_ratio = []

def isdigit(str):
    try:
        tmp = float(str)
        return True
    except ValueError:
        return False

# 음성 저장 함수
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

def mean_ratio(h_ratio, h_count, v_ratio, v_count):
    h = h_ratio/h_count
    v = v_ratio/v_count

    eye_ratio.append([h,v])
    print(eye_ratio)


def save_text(f_name):
    df = pd.DataFrame(eye_ratio, index=np.arange(1,10,1), columns=['h_ratio', 'v_ratio'])

    df.to_csv(output_file)

'''def read_text(text_name, num):
    f = open(text_name, 'r')
    string = f.read()
    string_list = string.split(" ")
    return string_list[num]'''

# 타이머 함수
def start_timer():
    global count
    global nowOrder
    global circle_radius
    global circle_radius_change
    global circle_color

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
        circle_radius_change = circle_radius
        circle_color = red_color
        mean_ratio(h_ratio, h_count, v_ratio, v_count)
        print('stop')
        timer.cancel()
        time.sleep(1)
        start_timer()


    timer.start()

#원 줄어드는 함수
def circle_decrease():
    global circle_radius_change
    global circle_is_change
    global circle_count
    global circle_color
    if circle_radius_change < 18:
        circle_color = green_color
    elif circle_radius_change > 0 :
        circle_radius_change -= 1

# 원 줄어드는 속도 조정을 위한 함수 1
def circle_change_flip():
    global circle_is_change
    if circle_is_change is True:
        circle_is_change = False
    else:
        circle_is_change = True


# 원 줄어드는 속도 조절을 위한 함수 2
def circle_count_decrease():
    global circle_count
    if circle_count > 0:
        circle_count -= 1


def calibration():


    play = False
    look_play = False
    webCam = cv2.VideoCapture(0, cv2.CAP_DSHOW)


    global h_ratio, h_count, v_ratio, v_count

    while True:
        # _, frame = webCam.read()

        frame = np.zeros((512, 512, 3), np.uint8)
        frame = cv2.resize(frame, dsize=(800, 600), interpolation=cv2.INTER_AREA)

        _, camFrame = webCam.read()
        camFrame = cv2.flip(camFrame, 1)
        camFrame = cv2.resize(camFrame, dsize=(800, 600), interpolation=cv2.INTER_AREA)
        camFrame = camFrame[150:450, 200:600]
        camFrame = cv2.resize(camFrame, dsize=(800, 600), interpolation=cv2.INTER_AREA)


        # 원 줄어들게 하기 위한 함수
        # circle_change_flip()
        #circle_count_decrease()

        if look_play == False:
            # 하늘색 배경 + 글자
            cv2.rectangle(frame, (0,0), (800,600), (250,244,192), -1)
            text2 = "Look at the red point"
            cv2.putText(frame,text2,(90,300),cv2.FONT_HERSHEY_DUPLEX, 1.8, (147,58,31), 2)
        else:
            if nowOrder < 9:
                circle_decrease()
                frame = cv2.circle(frame, (position[nowOrder][0], position[nowOrder][1]), circle_radius_change, circle_color, -1)

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)
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

        if nowOrder is 9:
            cv2.putText(camFrame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
            cv2.putText(camFrame, text1, (90, 100), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
            cv2.putText(camFrame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                        (147, 58, 31), 1)
            cv2.putText(camFrame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                        (147, 58, 31), 1)
            save_text(output_file)
            cv2.destroyAllWindows()
            test.main()
            break;



        garo = screen_width/2 - 400

        '''save eye ratio per frame'''
        if isdigit(str(gaze.horizontal_ratio())) == True:
            h_ratio += gaze.horizontal_ratio()
            h_count += 1
        if isdigit(str(gaze.vertical_ratio())) == True:
            v_ratio += gaze.vertical_ratio()
            v_count += 1
        '''###############################'''

        # 전체 화면
        # cv2.moveWindow("calibration", int(garo), 0)
        cv2.namedWindow("calibration", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("calibration", frame)

        # cv2.imshow("webcam", camFrame)




        if cv2.waitKey(1) == 27:
            break

        # 음성 출력
        if play is False:
            play_narrator("응시 나레이터", "look")
            start_timer()
            #save_text(output_file, cal_col, cal_row, gaze.horizontal_ratio())
            play = True;

if __name__ == '__main__':
    calibration()