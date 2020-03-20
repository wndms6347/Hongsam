import math
import numpy as np
import cv2
from .pupil import Pupil


class Eye(object):
    """
    This class creates a new frame to isolate the eye and
    initiates the pupil detection.
    이 클래스는 얼굴에서 눈 부분을 분리하여 새로운 프레임으로 만들고
    동공 감지를 하는 부분입니다.
    """
    
    # 얼굴에서 좌, 우측 눈 좌표 지점
    LEFT_EYE_POINTS =  [42, 43, 44, 45, 46, 47]
    RIGHT_EYE_POINTS = [36, 37, 38, 39, 40, 41]    #eye landmarks
    
    # 초기화
    def __init__(self, original_frame, landmarks, side, calibration):
        self.frame = None
        self.origin = None
        self.center = None
        self.pupil = None

        # 원래 프레임(orginal_frame)과 랜드마크, 사이드, 캘리브레이션
        self._analyze(original_frame, landmarks, side, calibration)

    @staticmethod
    def _middle_point(p1, p2):
        """Returns the middle point (x,y) between two points
            두 좌표간의 중간지점(x,y) 을 반환합니다.
        Arguments:
            p1 (dlib.point): First point
            p2 (dlib.point): Second point
        """
        x = int((p1.x + p2.x) / 2)
        y = int((p1.y + p2.y) / 2)
        return (x, y)

    def _isolate(self, frame, landmarks, points):
        """Isolate an eye, to have a frame without other part of the face.
            얼굴의 다른 부분 없이 눈을 분리시켜 새로운 프레임으로 만듭니다.

        Arguments:
            frame (numpy.ndarray): Frame containing the face
            프레임은 웹캠에서 받아오는 프레임 입니다.
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            랜드마크는 얼굴부분으로부터 얼굴 특징점을 의미합니다.
            points (list): Points of an eye (from the 68 Multi-PIE landmarks)
            눈의 좌표를 의미합니다.
        """

        # 얼굴에서 landmark 부분을 배열에 담습니다. (int32 형태)
        region = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in points])
        region = region.astype(np.int32)

        # Applying a mask to get only the eye
        # 눈 부분만 얻기위해 마스크(커널)를 적용합니다.
        height, width = frame.shape[:2]
        black_frame = np.zeros((height, width), np.uint8)
        mask = np.full((height, width), 255, np.uint8)
        cv2.fillPoly(mask, [region], (0, 0, 0))
        eye = cv2.bitwise_not(black_frame, frame.copy(), mask=mask)

        # Cropping on the eye
        margin = 5
        min_x = np.min(region[:, 0]) - margin
        max_x = np.max(region[:, 0]) + margin
        min_y = np.min(region[:, 1]) - margin
        max_y = np.max(region[:, 1]) + margin

        self.frame = eye[min_y:max_y, min_x:max_x]
        self.origin = (min_x, min_y)

        height, width = self.frame.shape[:2]
        self.center = (width / 2, height / 2)

    def _blinking_ratio(self, landmarks, points):
        """Calculates a ratio that can indicate whether an eye is closed or not.
        It's the division of the width of the eye, by its height.

        Arguments:
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            points (list): Points of an eye (from the 68 Multi-PIE landmarks)

        Returns:
            The computed ratio
        """
        right = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
        left = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
        top = self._middle_point(landmarks.part(points[1]), landmarks.part(points[2]))
        bottom = self._middle_point(landmarks.part(points[5]), landmarks.part(points[4]))

        eye_width = math.hypot((right[0] - left[0]), (right[1] - left[1]))
        eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))

        try:
            ratio = eye_width / eye_height
        except ZeroDivisionError:
            ratio = None

        return ratio

    def _analyze(self, original_frame, landmarks, side, calibration):
        """Detects and isolates the eye in a new frame, sends data to the calibration
        and initializes Pupil object.

        Arguments:
            original_frame (numpy.ndarray): Frame passed by the user
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            side: Indicates whether it's the left eye (0) or the right eye (1)
            calibration (calibration.Calibration): Manages the binarization threshold value
        """
        if side == 0:
            points = self.LEFT_EYE_POINTS####
        elif side == 1:
            points = self.RIGHT_EYE_POINTS####
        else:
            return

        self.blinking = self._blinking_ratio(landmarks, points)
        self._isolate(original_frame, landmarks, points)

        if not calibration.is_complete():
            calibration.evaluate(self.frame, side)

        threshold = calibration.threshold(side)
        self.pupil = Pupil(self.frame, threshold)
