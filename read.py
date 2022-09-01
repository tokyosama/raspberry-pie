
# 温湿度传感器返回  湿度  与  温度
def read_dht11_dat():
    lengths = [2,3]
    if len(lengths) != 2:
        print ("Data not good, skip")
        return False

    the_bytes=[38,13,28,2]
    checksum = 2
    if the_bytes[3] != checksum:
        print ("Data not good, skip")
        return False

    return the_bytes[0]

# 光照传感器返回 是否明亮
def read_light():
    status=True
    if status == False:
        print('能见度正常')
        return 1
    else:
        print('哇塞，好黑')
        return 0


# 温度传感器返回 温度
def read_DS18B20():
    temperature = 29.25
    return temperature




if __name__ == '__main__':

    light = read_light()
    print(light)
    humidity_1, temperature_1 = read_dht11_dat()
    print("humidity: %s %%,  Temperature: %s C`" % (humidity_1, temperature_1))
    temperature_2 = read_DS18B20()
    print("Temperature_2: %s C`" % temperature_2)

