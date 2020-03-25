from __future__ import division
import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration
import threading

# 얼굴의 각 구역 구분
JAWLINE_POINTS = list(range(0, 17))
RIGHT_EYEBROW_POINTS = list(range(17, 22))
LEFT_EYEBROW_POINTS = list(range(22, 27))
NOSE_POINTS = list(range(27, 36))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
MOUTH_OUTLINE_POINTS = list(range(48, 61))
MOUTH_INNER_POINTS = list(range(61, 68))


class GazeTracking(object):
    """
    This class tracks the user's gaze.
    It provides useful information like the position of the eyes
    and pupils and allows to know if the eyes are open or closed
    """

    def __init__(self):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()

        # _face_detector is used to detect faces
        # 아래의 변수는 클래스에 포함된 변수로써 얼굴을 탐지할때 사용한다.
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor is used to get facial landmarks of a given face
        # 아래의 변수는 주어진 얼굴의 특징점을 얻기위해 사용한다.
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(
            os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))  # 특징점을 찾기위한 데이터
        self._predictor = dlib.shape_predictor(model_path)  # _predictor에게 특징점 모델을 갖게한다.

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detects the face and initialize Eye objects"""
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)
        try:
            landmarks = self._predictor(frame, faces[0])
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)

        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, frame):
        """
        Refreshes the frame and analyzes it.
        프레임을 업데이트 시키고 새로운 프레임을 분석한다.
        Arguments:
            frame (numpy.ndarray): The frame to analyze
            분석하기위한 프레임
        """
        self.frame = frame
        self._analyze()

    def pupil_right_coords(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.origin[0] + self.eye_left.pupil.x
            y = self.eye_left.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def pupil_left_coords(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_right.pupil.x
            y = self.eye_right.origin[1] + self.eye_right.pupil.y
            return (x, y)

    def horizontal_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        horizontal direction of the gaze. The extreme right is 0.0,
        the center is 0.5 and the extreme left is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def vertical_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        vertical direction of the gaze. The extreme top is 0.0,
        the center is 0.5 and the extreme bottom is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def is_1(self):
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.35 and self.vertical_ratio() <= 0.45

    def is_2(self):
        if self.pupils_located:
            return 0.35 < self.horizontal_ratio() < 0.65 and self.vertical_ratio() <= 0.45

    def is_3(self):
        if self.pupils_located:
            return 0.65 <= self.horizontal_ratio() and self.vertical_ratio() <= 0.45

    def is_4(self):
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.35 and 0.45 < self.vertical_ratio() < 0.75

    def is_5(self):
        if self.pupils_located:
            return 0.35 < self.horizontal_ratio() < 0.65 and 0.45 < self.vertical_ratio() < 0.75

    def is_6(self):
        if self.pupils_located:
            return 0.65 <= self.horizontal_ratio() and 0.45 < self.vertical_ratio() < 0.75

    def is_7(self):
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.35 and 0.75 <= self.vertical_ratio()

    def is_8(self):
        if self.pupils_located:
            return 0.35 < self.horizontal_ratio() < 0.65 and 0.75 <= self.vertical_ratio()

    def is_9(self):
        if self.pupils_located:
            return 0.65 <= self.horizontal_ratio() and 0.75 <= self.vertical_ratio()

    '''def is_left(self):
        """
        Returns true if the user is looking to the right
        오른쪽을 보면 True를 반환합니다.
        """
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.35

    def is_right(self):
        """
        Returns true if the user is looking to the left
        왼쪽을 보면 True를 반환합니다.
        """
        if self.pupils_located:
            return self.horizontal_ratio() >= 0.65

    def is_center(self):
        """
        Returns true if the user is looking to the center
        중앙을 보면 True를 반환합니다.
        """
        if self.pupils_located:
            return self.is_right() is not True and self.is_left() is not True

    def is_up(self):
        """위를 보면 True를 반환합니다."""
        if self.pupils_located:
            return self.vertical_ratio() <= 0.45

    def is_down(self):
        """아래를 보면 True를 반환합니다."""
        if self.pupils_located:
            return self.vertical_ratio() >= 0.75'''

    def is_blinking(self):
        """
        Returns true if the user closes his eyes
        눈을 감으면 Return True
        """
        if self.pupils_located:
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            return blinking_ratio > 4.8

    def annotated_frame(self):
        """
        Returns the main frame with pupils highlighted
        동공 부분을 색칠하여 Return 합니다.
        """
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            x_right, y_right = self.pupil_right_coords()
            # cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            # cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            # cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            # cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)

            # 홍채 중앙에 빨간색 원을 표시한다.
            # cv2.circle(이미지, 좌표, 반지름, 색상, 두께)
            # [tip. thickness = -1, 안쪽이 채워진 원]
            red_color = (0, 0, 255)
            cv2.circle(frame, (x_left, y_left), 3, red_color, thickness=1)
            cv2.circle(frame, (x_right, y_right), 3, red_color, thickness=1)

        return frame
