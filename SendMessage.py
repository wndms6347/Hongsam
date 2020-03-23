from fbchat import Client, ThreadType

def sendMessage(btn_name, fc, friend):
    msg = '.'

    if btn_name == 'bed_up_btn':
        msg = "침대 올려주세요"

    elif btn_name == 'bed_down_btn':
        msg = "침대 내려주세요"

    elif btn_name == 'glasses_btn':
        msg = "안경 씌여주세요"

    elif btn_name == 'mistake_btn':
        msg = "잘 못 보냈어요"

    elif btn_name == 'window_btn':
        msg = "창문 열어주세요"

    elif btn_name == 'light_on_btn':
        msg = "불 켜주세요"
    elif btn_name == 'ligth_off_btn':
        msg = "불 꺼주세요"
    elif btn_name == 'cold_btn':
        msg = "추워요"
    elif btn_name == 'hot_btn':
        msg = "더워요"

    elif btn_name == 'big_btn':
        msg = "대변 하고싶어요"
    elif btn_name == 'small_btn':
        msg = "소변 하고싶어요"
    elif btn_name == 'water_btn':
        msg = "물 주세요"
    elif btn_name == 'out_btn':
        msg = "나가고 싶어요"
    elif btn_name == 'hungry_btn':
        msg = "배고파요"
    elif btn_name == 'full_btn':
        msg = "배불러요"
    elif btn_name == 'emergency_btn':
        msg = "긴급상황"

    for i in friend:
        sent = fc.sendMessage(msg, thread_id=str(i), thread_type=ThreadType.USER)
        if sent:
            print("Message sent successfully!")

if __name__ == '__main__':
    sendMessage()