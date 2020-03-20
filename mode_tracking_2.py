import cv2
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import pyautogui

# 스크린 사이즈
screen_width, screen_height = pyautogui.size()

class ShowVideo(QtCore.QObject):
    flag = 0
    camera = cv2.VideoCapture(0)
    ret, image = camera.read()

    # 카메라의 상하 좌,우 사이즈 구함
    height, width = image.shape[:2]

    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        global image

        run_video = True
        while run_video:
            ret, image = self.camera.read()
            image = cv2.flip(image, 1) # 좌우 반전
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                    self.width,
                                    self.height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)

            if self.flag:
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                img_canny = cv2.Canny(img_gray, 50, 100)

                qt_image2 = QtGui.QImage(img_canny.data,
                                         self.width,
                                         self.height,
                                         img_canny.strides[0],
                                         QtGui.QImage.Format_Grayscale8)

                self.VideoSignal2.emit(qt_image2)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    @QtCore.pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # 영상 출력 threading 처리
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    image_viewer1 = ImageViewer()
    image_viewer2 = ImageViewer()

    vid.VideoSignal1.connect(image_viewer1.setImage)
    vid.VideoSignal2.connect(image_viewer2.setImage)

    push_button1 = QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('Canny')
    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.canny)

    # vertical_layout = QtWidgets.QVBoxLayout()
    # horizontal_layout = QtWidgets.QHBoxLayout()
    # horizontal_layout.addWidget(image_viewer1)
    # horizontal_layout.addWidget(image_viewer2)
    # vertical_layout.addWidget(push_button1)
    # vertical_layout.addWidget(push_button2)
    # vertical_layout.addLayout(horizontal_layout)
    #
    # layout_widget = QtWidgets.QWidget()
    # layout_widget.setLayout(vertical_layout)
    # main_window.setCentralWidget(layout_widget)

    main_window = QtWidgets.QMainWindow() # main_window 할당...
    main_window.setGeometry(0,0,screen_width,screen_height) # main_window의 사이즈를 모니터 해상도에 맞게 설정
    main_window.setWindowTitle('mode_tracking')

    vid_widget = QtWidgets.QWidget(image_viewer1)
    main_window.setCentralWidget(vid_widget)

    main_window.showMaximized() # 처음 실행할때, 전체화면으로 연다.
    vid.startVideo()
    sys.exit(app.exec_())