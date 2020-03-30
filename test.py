import sys, cv2, numpy, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from playsound import playsound
from gtts import gTTS

form_class = uic.loadUiType('Ui.ui')[0]
cam = True      #캠 on/off
eye = True      #시선 on/off


class Exam(QWidget, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("tracking")
        self.initUI()

        # 모든 위젯 숨기기
        self.bed_widget.hide()
        self.eat_widget.hide()
        self.light_widget.hide()
        self.toilet_widget.hide()
        self.window_widget.hide()
        self.temperature_widget.hide()

        #mp3파일 생성
        '''self.save_narrator("창문 닫아주세요", "window_close_btn")
        self.save_narrator("침대 올려주세요", "bed_up_btn")
        self.save_narrator("침대 내려주세요", "bed_down_btn")
        self.save_narrator("안경 씌여주세요", "glasses_btn")
        self.save_narrator("잘 못 보냈어요", "mistake_btn")
        self.save_narrator("창문 열어주세요", "window_open_btn")
        self.save_narrator("불 켜주세요", "light_on_btn")
        self.save_narrator("불 꺼주세요", "light_off_btn")
        self.save_narrator("추워요", "cold_btn")
        self.save_narrator("더워요", "hot_btn")
        self.save_narrator("대변 하고싶어요", "big_btn")
        self.save_narrator("소변 하고싶어요", "small_btn")
        self.save_narrator("물 주세요", "water_btn")
        self.save_narrator("나가고 싶어요", "out_btn")
        self.save_narrator("배고파요", "hungry_btn")
        self.save_narrator("배불러요", "full_btn")
        self.save_narrator("비상호출", "emergency_btn")
        self.save_narrator("자세가 불편해요", "pose_btn")'''

        #버튼작동
        self.cam_btn.clicked.connect(self.cam_clicked)
        self.clear_btn.clicked.connect(self.btn_clear)
        self.eye_btn.clicked.connect(self.eye_clicked)
        self.bed_up_btn.clicked.connect(lambda state, button=self.bed_up_btn: self.btn_clicked(state, button))
        self.bed_down_btn.clicked.connect(lambda state, button=self.bed_down_btn: self.btn_clicked(state, button))
        self.window_open_btn.clicked.connect(lambda state, button=self.window_open_btn: self.btn_clicked(state, button))
        self.window_close_btn.clicked.connect(
            lambda state, button=self.window_close_btn: self.btn_clicked(state, button))
        self.light_on_btn.clicked.connect(lambda state, button=self.light_on_btn: self.btn_clicked(state, button))
        self.light_off_btn.clicked.connect(lambda state, button=self.light_off_btn: self.btn_clicked(state, button))
        self.emergency_btn.clicked.connect(lambda state, button=self.emergency_btn: self.btn_clicked(state, button))
        self.big_btn.clicked.connect(lambda state, button=self.big_btn: self.btn_clicked(state, button))
        self.small_btn.clicked.connect(lambda state, button=self.small_btn: self.btn_clicked(state, button))
        self.water_btn.clicked.connect(lambda state, button=self.water_btn: self.btn_clicked(state, button))
        self.out_btn.clicked.connect(lambda state, button=self.out_btn: self.btn_clicked(state, button))
        self.hungry_btn.clicked.connect(lambda state, button=self.hungry_btn: self.btn_clicked(state, button))
        self.full_btn.clicked.connect(lambda state, button=self.full_btn: self.btn_clicked(state, button))
        self.cold_btn.clicked.connect(lambda state, button=self.cold_btn: self.btn_clicked(state, button))
        self.hot_btn.clicked.connect(lambda state, button=self.hot_btn: self.btn_clicked(state, button))
        self.pose_btn.clicked.connect(lambda state, button=self.pose_btn: self.btn_clicked(state, button))

        #백 버튼
        self.eat_back_btn.clicked.connect(lambda state, button=self.eat_back_btn: self.back_btn_clicked(state, button))
        self.bed_back_btn.clicked.connect(lambda state, button=self.bed_back_btn: self.back_btn_clicked(state, button))
        self.light_back_btn.clicked.connect(
            lambda state, button=self.light_back_btn: self.back_btn_clicked(state, button))
        self.toilet_back_btn.clicked.connect(
            lambda state, button=self.toilet_back_btn: self.back_btn_clicked(state, button))
        self.window_back_btn.clicked.connect(
            lambda state, button=self.window_back_btn: self.back_btn_clicked(state, button))
        self.temperature_back_btn.clicked.connect(
            lambda state, button=self.temperature_back_btn: self.back_btn_clicked(state, button))

        #위젯 열기
        self.bed_btn.clicked.connect(lambda state, button=self.bed_btn: self.open_widget(state, button))
        self.eat_btn.clicked.connect(lambda state, button=self.eat_btn: self.open_widget(state, button))
        self.light_btn.clicked.connect(lambda state, button=self.light_btn: self.open_widget(state, button))
        self.toilet_btn.clicked.connect(lambda state, button=self.toilet_btn: self.open_widget(state, button))
        self.window_btn.clicked.connect(lambda state, button=self.window_btn: self.open_widget(state, button))
        self.temperature_btn.clicked.connect(lambda state, button=self.temperature_btn: self.open_widget(state, button))

    def eye_clicked(self):
        global eye
        if self.eye_btn.isChecked():
            eye = False
            print(eye)
        else:
            eye = True
            print(eye)

    def open_widget(self, state, button):
        if eye:
            if button.objectName() == "bed_btn":
                self.bed_widget.show()
            elif button.objectName() == "eat_btn":
                self.eat_widget.show()
            elif button.objectName() == "light_btn":
                self.light_widget.show()
            elif button.objectName() == "toilet_btn":
                self.toilet_widget.show()
            elif button.objectName() == "window_btn":
                self.window_widget.show()
            elif button.objectName() == "temperature_btn":
                self.temperature_widget.show()

    def back_btn_clicked(self, state, button):
        now_button = button.objectName()

        if now_button == "bed_back_btn":
            self.bed_widget.hide()
        elif now_button == "eat_back_btn":
            self.eat_widget.hide()
        elif now_button == "light_back_btn":
            self.light_widget.hide()
        elif now_button == "toilet_back_btn":
            self.toilet_widget.hide()
        elif now_button == "window_back_btn":
            self.window_widget.hide()
        elif now_button == "temperature_back_btn":
            self.temperature_widget.hide()

    def btn_clicked(self, state, button):
        if eye:
            exist_line_text = self.textEdit.toPlainText()
            now_text = button.text()
            now_button = button.objectName()

            print(now_text)
            self.textEdit.setText(exist_line_text + now_text + "\n")
            self.play_narrator(button)

            if now_button == "bed_up_btn" or now_button == "bed_down_btn":
                self.bed_widget.hide()
            elif now_button == "full_btn" or now_button == "hungry_btn":
                self.eat_widget.hide()
            elif now_button == "light_on_btn" or now_button == "light_off_btn":
                self.light_widget.hide()
            elif now_button == "big_btn" or now_button == "small_btn":
                self.toilet_widget.hide()
            elif now_button == "window_open_btn" or now_button == "window_close_btn":
                self.window_widget.hide()
            elif now_button == "cold_btn" or now_button == "hot_btn":
                self.temperature_widget.hide()

    def btn_clear(self):
        self.textEdit.clear()

    def cam_clicked(self):
        global cam
        if (cam is True):
            self.frame.hide()
            cam = False
        else:
            self.frame.show()
            cam = True

    def initUI(self):
        self.cpt = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.fps = 24

        self.frame = QLabel(self)
        self.frame.setGeometry(1380, 17, 448, 326)      #(캠위치 x좌표, 캠위치 y좌표, 캠크기 x축, 캠크기 y축)
        self.frame.setScaledContents(True)

        self.start()
        self.show()

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 / self.fps)

    def nextFrameSlot(self):
        _, cam = self.cpt.read()
        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
        cam = cv2.flip(cam, 1)
        img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix)
        self.frame.setGeometry(self.textEdit.geometry())        #(캠위치 x좌표, 캠위치 y좌표, 캠크기 x축, 캠크기 y축)

    def save_narrator(self, msg, file_name):
        engine = gTTS(text=msg, lang='ko')
        engine.save("./audio./" + file_name + "_audio.mp3")
        print(msg + '의 음성이 [' + file_name + '_audio.mp3] 파일로 저장 되었습니다.')

    def play_narrator(self, button):
        now_name = button.objectName()
        print(now_name)
        playsound("./audio./" + now_name + "_audio.mp3")
        print('파일명 : [' + now_name + '_audio.mp3]')


def main():
    w = Exam()
    w.ShowFullscreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Exam()
    w.show()
    sys.exit(app.exec_())
    cv2.destroyAllWindows()
