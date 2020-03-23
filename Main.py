import sys, cv2, numpy, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from playsound import playsound
from gtts import gTTS
import test
import pandas as pd
from fbchat import Client, ThreadType
import mode_calibration

form_class = uic.loadUiType('MainUi.ui')[0]
cam = True

class main(QWidget, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Main")
        self.re_btn.clicked.connect(lambda state, button = self.re_btn : self.btn_clicked(state, button))
        self.pre_btn.clicked.connect(lambda state, button = self.pre_btn : self.btn_clicked(state, button))
        self.cal_btn.clicked.connect(lambda state, button = self.cal_btn : self.btn_clicked(state, button))
        self.register_btn.clicked.connect(lambda state, button = self.register_btn : self.btn_clicked(state, button))
        self.start_btn.clicked.connect(lambda state, button = self.start_btn : self.btn_clicked(state, button))
        self.search_btn.clicked.connect(lambda state, button = self.search_btn : self.btn_clicked(state, button))
        self.del_btn.clicked.connect(self.deleteFriend)
        self.fc = Client('fofo0623@naver.com', 'capstone12!')
        self.f = pd.read_csv('./friend.csv')
        self.friend_list = self.f['friend'].tolist()
        self.set_Main()


    def fillFriend(self):
        self.friendWidget.clear()
        for i in self.friend_list:
            tempItem = QListWidgetItem()
            tempItem.setText(self.fc.fetchThreadInfo(str(i))[str(i)].name)
            self.friendWidget.addItem(tempItem)

    def set_Main(self):
        self.register_widget.hide()
        self.lineEdit.setText('')
        self.label_3.setText('')
        self.re_btn.setEnabled(False)
        self.pre_btn.setEnabled(False)
        self.cal_btn.setEnabled(True)
        self.register_btn.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.search_btn.setEnabled(False)
        self.fillFriend()

    def set_Reg(self):
        self.register_widget.show()
        self.lineEdit.setText('')
        self.label_3.setText('')
        self.re_btn.setEnabled(True)
        self.pre_btn.setEnabled(True)
        self.cal_btn.setEnabled(False)
        self.register_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.search_btn.setEnabled(True)
        self.fillFriend()

    def btn_clicked(self, state, button):
        now_text = button.text()
        print(now_text)

        if now_text == '등록':
            if self.lineEdit.text().isdigit():
                thread = self.lineEdit.text()
                if not self.fc.fetchThreadInfo(self.lineEdit.text())[self.lineEdit.text()]:
                    print()
                else:
                    a = []
                    a.append(str(thread))
                    temp = pd.DataFrame({'friend' : thread}, index = [0])
                    self.f = pd.concat([self.f, temp])
                    print(self.f)
                    self.f.to_csv('./friend.csv')
                    self.friend_list = self.f['friend'].tolist()
                    print('성공적으로 등록되었습니다.')
                    self.fillFriend()
                    self.set_Main()
            else:
                self.lineEdit.setText('숫자 아이디를 입력하세요')

        elif now_text == 'X':
            self.set_Main()
            #self.friendWidget.clear()

        elif now_text == 'Register':
            self.set_Reg()

        elif now_text == 'Start':
            test.main(self.friend_list, self.fc)

        elif now_text == 'Calibration':
            mode_calibration.calibration()

        elif now_text == '검색':
            if not self.fc.fetchThreadInfo(self.lineEdit.text())[self.lineEdit.text()]:
                print()
            else:
                self.label_3.setText(self.fc.fetchThreadInfo(self.lineEdit.text())[self.lineEdit.text()].name)

    def btn_clear(self):
        self.textEdit.clear()

    def deleteFriend(self):
        row = self.friendWidget.currentRow()
        self.f = self.f.drop(row, 0).iloc[:, 1:]
        print(self.f)
        self.f.to_csv('./friend.csv')
        self.friend_list = self.f['friend'].tolist()
        self.fillFriend()


def go():
    w = main()
    w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = main()
    w.show()
    sys.exit(app.exec_())
    cv2.destroyAllWindows()
