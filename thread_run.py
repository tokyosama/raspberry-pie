import RPi.GPIO as GPIO
import record
import time
import csv
from myThread import MyThread
import sound
import snowboydecoder
import sys
import signal
import record_monitor as recordMonitor
import LED
import threading
# ===================================================
# 实验控制量
#
# ==============================================
# ==============================================
# 数据记录线程
def record_csv(dd):
    D11 = 17
    l = 22
    f = "/sys/bus/w1/devices/28-01201cd1596c/w1_slave"
    print("开始检测数据")
    i = 0
    a = {}
    try:
        while True:
            time.sleep(1)
            a['时间'] = time.strftime("%Y%m%d %X", time.localtime())
            result = record.D11_temp_humidity(D11)
            if result:
                a['温度1'] = record.temperature(f)
                x, y = result
                a['温度2'] = y
                a['湿度'] = x
                a['亮度'] = record.light(l)
            with open("htl.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                print(a)
                for i in a:
                    writer.writerow(i)
    except:
        GPIO.cleanup()
# ===================================================
# 语音对话模块
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def wake_up():

    global detector
    model = 'snowboy.pmdl'  #  唤醒词为 SnowBoy
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # 唤醒词检测函数，调整sensitivity参数可修改唤醒词检测的准确性
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    print('Listening... please say wake-up word:SnowBoy')
    # main loop
    # 回调函数 detected_callback=snowboydecoder.play_audio_file
    # 修改回调函数可实现我们想要的功能
    detector.start(detected_callback=callbacks,      # 自定义回调函数
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)
    # 释放资源
    detector.terminate()


def callbacks():
    global detector
    # 语音唤醒后，提示ding两声
    snowboydecoder.play_audio_file()
    snowboydecoder.play_audio_file()

    #  关闭snowboy功能
    detector.terminate()
    #  开启语音识别
    # recordMonitor.monitor()

    sound_result = s_sound(0)
    print("语音识别结果\n")
    print(sound_result)

    # 打开snowboy功能
    wake_up()    # wake_up —> monitor —> wake_up  递归调用

def s_sound(dd):
    flag = 'y'
    # while flag.lower() == 'y':
    # print('请输入数字选择语言：')
    # devpid = input('1536：普通话(简单英文),1537:普通话(有标点),1737:英语,1637:粤语,1837:四川话\n')
    devpid = 1536
    sound.my_record()
    TOKEN = sound.getToken(sound.HOST)
    speech = sound.get_audio(sound.FILEPATH)
    result = sound.speech2text(speech, TOKEN, int(devpid))
    print(result)
    return result
    # if type(result) == str:
    #     openbrowser(result.strip('，'))
    # flag = input('Continue?(y/n):')
# ==============================================
# 人脸识别模块

# ==============================================
# def loop(x):
#     time.sleep(x)
#     print("第一个进程，停止结束")
#
# def loop2(x):
#     for i in range(2):
#         time.sleep(x)
#         print("停止:", i)
#     print("第二个进程，停止结束")
# 线程控制
funcs = [s_sound,record_csv]

def main():
    nfuncs = range(len(funcs))
    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], 0, funcs[i].__name__)
        threads.append(t)
    for i in nfuncs:
        threads[i].start()
    # for i in nfuncs:
        # threads[i].join()
        # print(threads[i].getResult())
    print("all over!")

if __name__ == "__main__":
    main()