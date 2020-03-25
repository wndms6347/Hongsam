"""
    [목표]
    1. frame 에서 얼굴 인식
    2. 얼굴에서 눈 인식하기
    3. 인식된 눈에서 동공 찾기
    4. 동공의 움직임 인식하기
"""

import numpy as np
import dlib
import cv2
from gaze_tracking import GazeTracking
from gaze_tracking.eye import Eye
import pyautogui  # 마우스 제어용

# GazeTracking, dlib.face_detector 객체 불러오기
gaze = GazeTracking()
gaze2 = GazeTracking()  # 실험용
face_detector = dlib.get_frontal_face_detector()

# 모니터의 사이즈
screenWidth, screenHeight = pyautogui.size()

# 웹캠 실시간 받아오기
video_capture = cv2.VideoCapture(0)

# 데이터 등록
predictor = dlib.shape_predictor('./data/shape_predictor_68_face_landmarks.dat')  # 얼굴 랜드마크
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# 얼굴의 각 구역 구분
JAWLINE_POINTS = list(range(0, 17))
RIGHT_EYEBROW_POINTS = list(range(17, 22))
LEFT_EYEBROW_POINTS = list(range(22, 27))
NOSE_POINTS = list(range(27, 36))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
MOUTH_OUTLINE_POINTS = list(range(48, 61))
MOUTH_INNER_POINTS = list(range(61, 68))


def detect(gray, frame):
    """
        [설명]
        def = eyeCascade와 dlib를 이용하여 얼굴을 찾고 눈을 찾는 함수
        input = 웹캠에서 받아온 그레이스케일 이미지와 default 이미지
        output = 얼굴과 눈에 사각형이 그려진 이미지 프레임과 얼굴의 68개 점
    """

    try:
        # gray_scale 에서 dlib 를 통하여 얼굴을 찾는다.
        faces = face_detector(gray)
        # 얼굴 영역을 사각형으로 마킹..
        f = faces[0]
        cv2.rectangle(frame, (f.left(), f.top()), (f.right(), f.bottom()), (255, 0, 0), 1)
        cv2.putText(frame, "Detected Face", (f.left() + 3, f.top() + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)

        # 얼굴 부분을 자른다.
        face_color = frame[f.top():f.bottom(), f.left():f.right()]  # 컬러

        # face_color 영상을 두배로 늘린다.
        color_image = cv2.resize(face_color, None, fx=3, fy=3, interpolation=cv2.INTER_AREA)
        gaze2.refresh(color_image)
        color_image = gaze2.annotated_frame()
        cv2.imshow("color_image", color_image)
        cv2.moveWindow("color_image", 0, 0)
        mouseCnt(gaze2)
    except:
        cv2.destroyWindow("color_image")
        pass

    # # 등록한 Cascade classifier 를 이용 얼굴을 찾음
    #
    # faces = faceCascade.detectMultiScale(gray, scaleFactor=1.05,
    # minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    #
    # # 웹캠에서 얼굴을 하나도 찾을 수 없다면 sub_image 를 없앤다.
    # if len(faces) < 1:
    #     cv2.destroyWindow("sub_image")
    #
    # for(x, y, w, h) in faces:
    #     # 얼굴 영역을 사각형으로 마킹..
    #     cv2.rectangle(frame, (x+2, y+2), (x+w-2, y+h-2), (255,0,0), 2)
    #     cv2.putText(frame, "Detected Face", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,0,0), 2)
    #
    #     # 얼굴 부분을 자른다.
    #     face_gray = frame[y:y+h, x:x+w] # 그레이스케일
    #     face_color = frame[y:y+h, x:x+w] # 컬러
    #     face_for_dlib = dlib.rectangle(int(x), int(y), int(x+w), int(y+h)) # dlib용 이미지
    #     cv2.imshow("face_gray",face_gray)
    #
    #     # 랜드마크 포인트들 지정
    #     shape = predictor(face_gray, face_for_dlib)
    #     landmarks = np.matrix([[p.x,p.y] for p in shape.parts()])
    #
    #     # 얼굴을 찾을 수 있을때, 21번 포인트와 29번 포인트를 기준으로 자른 이미지를 보여준다. ( 눈탐지도 같이 함 )
    #     if face_gray is not None:
    #         p_21_y = int(shape.part(21).y)
    #         p_29_y = int(shape.part(29).y)
    #         sub_image = frame[p_21_y:p_21_y + p_29_y - p_21_y, x:x+w]
    #         sub_image = cv2.resize(sub_image, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    #
    #         # sub_image = cv2.bilateralFilter(sub_image, 9, 75, 75)
    #
    #         # # 자른 그레이스케일 얼굴 영역에서 눈을 감지
    #         # eyes = eyeCascade.detectMultiScale(sub_image, 1.1, 3)
    #         #
    #         # for (ex, ey, ew, eh) in eyes:
    #         #     # frame에서 눈 영역을 사각형으로 마킹한다.
    #         #     cv2.rectangle(sub_image, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    #         #     cv2.putText(sub_image, "Detected Eyes", (ex, ey), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)
    #
    #         # 모든 포인트들을 넣는다.
    #         landmarks_display = landmarks[0:68]
    #         # landmarks_display = landmarks[RIGHT_EYE_POINTS, LEFT_EYE_POINTS] # 인쪽 오른쪽 눈만 랜드마크 표시
    #
    #         # 랜드마크 포인트 출력
    #         for idx, point in enumerate(landmarks_display):
    #             pos = (point[0, 0], point[0, 1])
    #             cv2.circle(sub_image, pos, 1, color=(0, 0, 0), thickness=-1)
    #         cv2.imshow("sub_image", sub_image)
    #
    # # 찾은 프레임을 전달
    # return frame


def save_location(file_name, data):
    f = open(file_name, 'a')
    f.write(str(data) + " ")
    f.close()


def read_location(file_name):
    f = open(file_name, 'r')
    string = f.read()
    string_list = string.split(" ")
    print(string_list)
    return string_list


max_num = 0
min_num = screenWidth
sleep = 0


def mouseCnt(gaze):
    global max_num, min_num, sleep, screenWidth, screenHeight # 전역변수
    
    #####################################
    #      2020-03-25, 동공 크기비       #
    #####################################
    if gaze.pupils_located:  # 만약 동공 탐지가 되었으면..
        re_width = gaze.eye_right.width
        re_height = gaze.eye_right.height
        re_x, re_y = gaze.pupil_right_coords()

        """
        (screen_width or screen_height) : Y = (re_width or re_height) : X
        * 조건 : screen_width = 변하지 않는 cosnt_var
        """
        re_x -= gaze.eye_right.left[0]
        re_y -= gaze.eye_right.top[1]
        # re_eye = read_location("./data/right_eye_x.txt") # right_eye = arr
        # re_width = max(re_eye) - min(re_eye)
        m_x = screenWidth * re_x / re_width
        m_y = screenHeight * re_y / re_height

        if max_num < m_x:
            max_num = m_x

        if min_num > m_x:
            min_num = m_x

        print("(" + str(m_x) + "," + str(m_y) + ") ---- max : " + str(max_num) + ", min : " + str(min_num))
        pyautogui.moveTo(m_x, m_y)

        if cv2.waitKey(1) & 0xFF == ord('x'):   # 'x' 를 누르면 정지
            sleep = 1

        if cv2.waitKey(1) & 0xFF == ord('s'):   # 's' 를 누르면 세이브
            save_location("./data/right_eye_x.txt", re_x)
            read_location("./data/right_eye_x.txt")


while True:
    if sleep is 1:
        while True:
            if cv2.waitKey(1) & 0xFF == ord('x'):
                sleep = 0
                break

    # 웹캠 이미지를 프레임으로 자르고 좌우 반전을 한다.
    _, frame = video_capture.read()
    frame = cv2.flip(frame, 1)  # 이미지 좌우 반전

    # # gaze 객체의 프레임을 갱신한다.
    # gaze.refresh(frame)
    #
    # # 동공에 빨간 점 표시를 한다.
    # gaze_frame = gaze.annotated_frame()

    # 프레임을 그레이스케일로 변환..
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴과 눈을 찾기위한 판별
    detect(gray_frame, frame)

    # # 찾은 이미지를 보여준다.
    # cv2.imshow("gaze_frame", gaze_frame)
    # cv2.moveWindow("gaze_frame", 0, 0)

    # q를 누르면 종료한다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 된 후 처리
video_capture.release()  # 웹캠 중지
cv2.destroyAllWindows()  # 열려있는 윈도우 종료
