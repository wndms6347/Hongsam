import cv2
import glob
import os.path
import os
import keyboard
import threading

next_image = 0 #이미지 인덱스 값
count = 0      #이미지 몇 장인지 카운트
num_count = 0  #시간 카운트

#폴더 내 모든 jpg 이미지 파일 이름 가져오기
images = glob.glob('./Gallery/*.jpg')

#이미지 몇 장인지 카운트
for fname in images:
    count += 1

def start_timer():

    global next_image
    global num_count
    global timer

    timer = threading.Timer(1,start_timer)
    num_count += 1
    print(num_count)

    if num_count % 10 is 0:
        num_count = 0
        next_image += 1
        timer.cancel()
        start_timer()


def gallery():

    global next_image
    global num_count

    while True:
        start_timer()

        # n 누르면 사진 넘기기
        if keyboard.is_pressed('n'):
            next_image += 1
            #timer.cancel()
            num_count = 0
            start_timer()

        # b 누르면 사진 뒤로 넘기기
        if keyboard.is_pressed('b'):
            next_image -= 1
            num_count = 0

        #일시정지
        #if keyboard.is_pressed('p'):


        #사진 처음으로 돌아가기
        if next_image == count:
            next_image = 0

        image =  cv2.imread(images[next_image],cv2.IMREAD_COLOR)
        reimage = cv2.resize(image,dsize=(1280,720), interpolation=cv2.INTER_AREA)
        cv2.imshow('Gallery',reimage)
        cv2.waitKey(1000)

        # q 누르면 갤러리 종료
        if keyboard.is_pressed('q'):
            cv2.destroyWindow('Gallery')
            break

if __name__ == '__main__':
    gallery()