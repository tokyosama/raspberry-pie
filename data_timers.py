import time

import read  #导入传感器检测文件
import threading  #导入控制进程的库
import pymysql
import datetime

#连接数据库
db = pymysql.connect(host='192.168.1.102',user='root', password='123', port=3306, db='smp_db_01',autocommit=False)
cursor = db.cursor()


# 每隔100秒传感器记录一次数据并且插入到数据库中
def func_task():
    print('执行任务中...')
    note_time = datetime.datetime.now()
    flag = True
    while flag:
        hum, tem_1 = read.read_dht11_dat()
        tem_2 = read.read_DS18B20()
        light = read.read_light()
        if hum:
            time.sleep(0.3)
            flag = True
        flag = False
    #要插入到数据库的数据
    data = {
        'tem': tem_2,
        'hum': hum,
        'lit': light,
        'time': str(note_time)
    }
    table = 'smp_data'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    try:
        cursor.execute(sql, tuple(data.values()) * 2)
        print('插入到数据库成功')
        db.commit()
    except:
        print('插入失败')
        db.rollback()


def func_timer():
    func_task()
    global timer  # 定义全局变量
    # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    timer = threading.Timer(10, func_timer)   # 每隔100秒调用一次函数

    print("线程名称={},\n正在执行的线程列表:{},\n正在执行的线程数量={},\n当前激活线程={}\n".format(
        timer.getName(), threading.enumerate(), threading.active_count(), timer.is_alive())
    )

    timer.start()    #启用定时器

timer = threading.Timer(1, func_timer)
timer.start()
print('定时器启动成功-----')
