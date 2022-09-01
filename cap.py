from flask import Flask, render_template, Response
import cv2

#
# class VideoCamera(object):
#     def __init__(self):
#         # 通过opencv获取实时视频流
#         self.video = cv2.VideoCapture(0)
#
#     def __del__(self):
#         self.video.release()
#
#     def get_frame(self):
#         success, image = self.video.read()
#         # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()
#
#
# app = Flask(__name__)
#
#
# @app.route('/')  # 主页
# def index():
#     # jinja2模板，具体格式保存在index.html文件中
#     return render_template('index.html')
#
#
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
#
# @app.route('/video_feed')  # 这个地址返回视频流响应
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', debug=True, port = 8080)

    # #coding:utf-8
# from flask import Flask,render_template,Response
# import cv2
#
# app = Flask(__name__)
# camera = cv2.VideoCapture(0) #use 0 for web camera
#
# # Use Ip Camera/CCTV/RTSP Link
# # cv2.VideoCapture('rtsp://username:password@camera_ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp')
# ### Example RTSP Link
# # cv2.VideoCapture('rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=0_stream=0.sdp') ```
#
# def gen_frames(): #generate frame by frame from camera
#     while True:
#         #capture frame-by-frame
#         success,frame = camera.read()
#         print('==frame.shape',frame.shape)
#         if not success:
#              break
#         else:
#             ret,buffer = cv2.imencode('.jpg',frame)
#             frame = buffer.tobytes()
#
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
#
# @app.route('/', methods=['GET', 'POST'])
# def main():
#     print('进入控制界面成功')
#     return render_template("index.html")  # 返回网页
#
# @app.route('/video_feed')
# def video_feed():
#     # Video streaming route. Put this in the src attribute of an img tag
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# @app.route('/video', methods=["get"])
# def index():
#     """Video streaming home page."""
#     return render_template('index.html')
#
#
# if __name__ == '__main__':
#     # app.run(debug=True, port=6006)
#     app.run(host="127.0.0.1", port=8080)




import cv2

cap = cv2.VideoCapture(0)  # 调用摄像头‘0’一般是打开电脑自带摄像头，‘1’是打开外部摄像头（只有一个摄像头的情况）
width = 480
height = 600
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # 设置图像宽度
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 设置图像高度
# 显示图像
while True:
    ret, frame = cap.read()  # 读取图像(frame就是读取的视频帧，对frame处理就是对整个视频的处理)
    # print(ret)#
    #######例如将图像灰度化处理，
    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转灰度图
    #cv2.imshow("img", img)
    ########图像不处理的情况
    cv2.imshow("frame", frame)

    input = cv2.waitKey(20)
    if input == ord('q'):  # 如过输入的是q就break，结束图像显示，鼠标点击视频画面输入字符
        break

cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 销毁窗口
