import numpy as np
import cv2

class Pupil(object):
    """
    This class detects the iris of an eye and estimates
    the position of the pupil
    이 클래스는 눈동자에서 홍채를 찾고, 동공의 위치를 예측하는 기능을 합니다.
    """

    def __init__(self, eye_frame, threshold):
        self.iris_frame = None
        self.threshold = threshold
        self.x = None
        self.y = None

        self.detect_iris(eye_frame)

    @staticmethod
    def image_processing(eye_frame, threshold):
        """
        Performs operations on the eye frame to isolate the iris
        눈 영상에서 홍채 영상을 분리하기 위해서 작동하는 함수입니다.
        Arguments:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else
            눈 프레임
            threshold (int): Threshold value used to binarize the eye frame
            임계값

        Returns:
            A frame with a single element representing the iris
            하나의 홍채가 존재하는 프레임이 반환된다.
        """
        kernel = np.ones((3, 3), np.uint8) # 3,3 커널 사용
        new_frame = cv2.bilateralFilter(eye_frame, 10, 15, 15) # 영상을 좀 더 선명하게 필터링을 거친다.
        new_frame = cv2.erode(new_frame, kernel, iterations=3) # 영상을 침식시킨다. erosion을 의미 (팽창, 침식)
        new_frame = cv2.threshold(new_frame, threshold, 255, cv2.THRESH_BINARY)[1] # 임계값을 통하여 홍채 프레임 반환

        cv2.imshow("pupil",new_frame)
        return new_frame

    def detect_iris(self, eye_frame):
        """
        Detects the iris and estimates the position of the iris by
        calculating the centroid.
        홍체를 찾고, 중앙점을 계산하므로써 홍채 위치를 찾습니다.

        Arguments:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else
            한쪽의 눈동자만 있으면 된다.
        """
        self.iris_frame = self.image_processing(eye_frame, self.threshold) # 홍채 프레임을 받아온다.

        contours, _ = cv2.findContours(self.iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:] # 홍채의 윤곽을 찾는다.
        contours = sorted(contours, key=cv2.contourArea) # 윤곽선을 올림차순으로 정렬한다.

        try:
            moments = cv2.moments(contours[-2]) # 뒤에서 두번째로 큰 윤곽선의 모멘트를 구한다.
            self.x = int(moments['m10'] / moments['m00'])
            self.y = int(moments['m01'] / moments['m00'])
        except (IndexError, ZeroDivisionError):
            pass
