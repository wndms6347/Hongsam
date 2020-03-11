import cv2
import pyautogui
from Tracking import GazeTracking
import pandas as pd
import threading

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

# 마우스 이동 함수
def move_mouse():
    global output
    if gaze.pupils_located:
        print(output)
        #pyautogui.moveTo(((screen_width* gaze.horizontal_ratio()) - 576) * 1.74, ((screen_height*gaze.vertical_ratio()) - 540) * 1.35,5)
        #pyautogui.moveTo(screen_width/2, screen_height * normalization(gaze.vertical_ratio(),output_eyeratio.loc[8,'v_ratio'],output_eyeratio.loc[4,'v_ratio']) )
    pyautogui.moveTo(screen_width/2,screen_height/2)
    print("err")


# 트래킹을 실행한다.
def tracking():
    while True:
        _, frame = gaze.frame


        if(frame is not None):
            cv2.imshow("tracking", frame)

        # ESC를 누르면 꺼진다.
        if cv2.waitKey(1) == 27:
            break


if __name__ == '__main__':
    tracking()