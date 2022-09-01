from flask import Flask, request, render_template, Response, url_for, redirect, session  # 导入flask框架所需要的包，模块
import cv2
from myThread import MyThread
import video_handler as vh
import pymysql
from flask import jsonify  # 数据转为json，并以字典的形式传回前端

# 固定写法
app = Flask(__name__)



#主界面
@app.route('/', methods=['GET', 'POST'])
def main():

    print('进入控制界面成功')
    return render_template("Web_Control.html")  # 返回网页


# 开灯
@app.route('/fopen', methods=['POST', 'GET'])
def fopen():
    print('灯光已开启')
    return "Open OK"


# 关灯
@app.route('/fclose', methods=['POST'])
def fclose():
    print('灯光已关闭')
    return "Close OK"


# 灯光闪烁
@app.route("/fshine", methods=['POST'])
def sansuo():
    print('正在闪烁')
    return "Shining OK"


#进入监控
@app.route('/video')
def mainv():
    print('进入监控界面成功')
    return render_template("index.html")  # 返回网页


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(vh.gen(vh.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_back', methods=['GET', 'POST'])
def mainvback():
    print('返回到控制界面成功')
    return redirect(url_for('main'))  # 返回网页

@app.route('/setData')  # 路由
def setData():
    db = pymysql.connect(host='192.168.1.102',
                         user='pai',
                         port=3306,
                         password='123123',
                         database='smp_db_01',
                         autocommit=True,
                         charset='utf8')
    # #连接对象获得一个普通cursor对象
    cursor = db.cursor()
    query = "SELECT * FROM smp_data"
    cursor.execute(query)  # 执行
    response = cursor.fetchall()
    #每次只在前端显示数据库最新插入的数据
    data = {'tem': response[-1][1], 'hum': response[-1][2],'lit':response[-1][3]}
    return jsonify(data)  # 将数据以字典的形式传回

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)  # 该地址为树莓派连接到wifi时分配得到的IP地址，端口任意设（也可以用本机的IP地址:127.0.0.2,port:8081）
