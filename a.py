from flask import Flask, request, render_template, Response  # 导入flask框架所需要的包，模块
import RPi.GPIO as GPIO  # 导入RPi.GPIO包
import time  # 计时器

GPIO.setmode(GPIO.BCM)  # GPIO波特
GPIO.setup(26, GPIO.OUT)  # GPIO。26引脚为输出模式

# 固定写法
app = Flask(__name__)


# 进入的首个网页
@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("Web_Control.html")  # 返回网页


# 点击打开
@app.route('/on', methods=['GET'])
def on():
    GPIO.output(26, GPIO.HIGH)  # GPIO.26高电平
    time.sleep(3.5)  # 延时3.5s
    print("555")  # 打印555
    return render_template("Web_Control.html")  # 返回一开始的页面


# 点击关闭
@app.route("/off", methods=['GET'])
def off():
    GPIO.output(26, GPIO.LOW)  # GPIO.26低电平
    time.sleep(3.5)
    print("666")
    return render_template("Web_Control.html")  # #返回一开始的页面


@app.route("/sansuo", methods=['POST'])
def sansuo():
    i = 0
    while i < 5:
        GPIO.output(26, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(26, GPIO.LOW)
        time.sleep(0.5)
        i = i + 1
    return render_template("Web_Control.html")


if __name__ == "__main__":
    app.run(host='192.168.88.232', port=8087)  # 该地址为树莓派连接到wifi时分配得到的IP地址，端口任意设（也可以用本机的IP地址:127.0.0.2,port:8081）

GPIO.clearnup()

