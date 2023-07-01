'''
  舵机-->(22)
  (Trig)-->(5)
  (Echo)-->(18)
  SCL-->16
  SDA-->17
  DS-->27
   WS-->(13)
'''

#导入Pin模块
from machine import Pin
import time
from servo import Servo
from machine import Timer
from hcsr04 import HCSR04
from neopixel import NeoPixel
import random
from machine import ADC
from machine import Pin,I2C
from i2c_lcd import I2cLcd
import dht
import network
import socket

#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=5, echo_pin=18)
#定义SG90舵机控制对象
servo = Servo(Pin(22))
#定义DHT22控制对象
dht22=dht.DHT22(Pin(27))
#定义RGB控制对象
#控制引脚为13，RGB灯串联5个
pin=13
rgb_num=64
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)
# LCD 1602 I2C 地址
DEFAULT_I2C_ADDR = 0x27
# 初始化GPIO口
# def setup():
# global lcd
i2c = I2C(1,sda=Pin(17),scl=Pin(16),freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)  # 初始化(设备地址, 背光设置)
#定义按键控制对象
key1=Pin(12,Pin.IN,Pin.PULL_UP)
key2=Pin(14,Pin.IN,Pin.PULL_UP)
key3=Pin(26,Pin.IN,Pin.PULL_UP)
key4=Pin(25,Pin.IN,Pin.PULL_UP)
key5=Pin(33,Pin.IN,Pin.PULL_UP)
key6=Pin(32,Pin.IN,Pin.PULL_UP)

key_en=1
#按键扫描函数
def key_scan():
    global key_en
    if key_en==1 and (key1.value()==0 or key2.value()==0 or key3.value()==0 or key4.value()==0 or
                      key5.value()==0 or key6.value()==0  ):
        time.sleep_ms(10)
        key_en=0
        if key1.value()==0:
            return 1
        elif key2.value()==0:
            return 2
        elif key3.value()==0:
            return 3
        elif key4.value()==0:
            return 4
        elif key5.value()==0:
            return 5
        elif key6.value()==0:
            return 6
    elif (key1.value()==1 and key2.value()==1 and key3.value()==1 and key4.value()==1 and
          key5.value()==1 and key6.value()==1  ) :
        key_en=1
    return 0

brightness=12
delay=40
mode=1
def key_get(): #获取键值并改变变量的值
    global brightness
    global delay
    global mode
    key=key_scan()
    if key==1 and brightness<30 :
        brightness+=2
    elif key==2 and brightness>8 :
        brightness-=2
    elif key==3 and delay<90 :
        delay+=10
    elif key==4 and delay>10 :
        delay-=10
    elif key==5 and mode<1 :
        mode+=1
    elif key==6 and mode>0 :
        mode-=1     

#定义LED控制对象
led1=Pin(15,Pin.OUT,Pin.PULL_DOWN)

#定义DHT22控制对象
sensor=dht.DHT22(Pin(27))

#连接的WIFI账号和密码
ssid = "Mercury_X30G"
password = "Xu3328313"


def read_sensor():
    global temp, hum
    temp = hum = 99
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))

            # uncomment for Fahrenheit
            #temp = temp * (9/5) + 32.0

            hum = round(hum, 2)
            return(msg)
        else:
            return('Invalid sensor readings.')
    except OSError as e:
        return('Failed to read sensor.')
        
#WIFI连接
def wifi_connect():
    wlan=network.WLAN(network.STA_IF)  #STA模式
    wlan.active(True)  #激活
    
    if not wlan.isconnected():
        print("conneting to network...")
        wlan.connect(ssid,password)  #输入 WIFI 账号密码
        
        while not wlan.isconnected():
            led1.value(1)
            time.sleep_ms(300)
            led1.value(0)
            time.sleep_ms(300)
        led1.value(0)
        return False
    else:
        led1.value(0)
        print("network information:", wlan.ifconfig())
        return True

#网页数据
def web_page():
  html = """<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.2rem; }
    .dht-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>
<body>
  <h2>ESP32 DHT22 Acquisition</h2>
  <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="dht-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;C</sup>
  </p>
  <p>
    <i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="dht-labels">Humidity</span>
    <span>"""+str(hum)+"""</span>
    <sup class="units">%</sup>
  </p>
</body>
</html>"""
  return html

b=0
c=120
g=0
h=0
hum=99
k=0
l=0
m=0
servo.write_angle(c)
#定时器0中断函数
def time0_irq(time0):
    global b
    global c
    global g
    global h
    global k
    global l
    global m
    global temp, hum
    global brightness
    global delay
    global mode
    key_get()
    distance=hcsr04.distance_cm()
    if distance>15 and c<=120:  
        c+=5
        servo.write_angle(c)
    if distance<15 and distance>=0 and c>=40:
        c-=5
        servo.write_angle(c)
    g+=1
    m+=1
    if g==4 : #每4个周期RGB灯随机变色,屏幕刷新
        g=0
        if mode==1 :
            for i in range(rgb_num):
                d=random.randint(0,brightness)
                e=random.randint(0,brightness)
                f=random.randint(0,brightness)
                rgb_led[i]=(d, e, f)
            rgb_led.write()
        if mode==0 :
            for i in range(rgb_num):
                rgb_led[i]=(0, 0, 0)
            rgb_led.write()
        lcd.putstr("humidity=%.1f"%hum)       
        lcd.putstr("%  ")
        lcd.putstr("distance=%3d"%distance)
        lcd.putstr("cm  ")

    if m==30: #每30个周期测量湿度
        m=0
        read_sensor()
       
#程序入口
if __name__=="__main__":
    wifi_connect()
    #SOCK_STREAM表示的是TCP协议，SOCK_DGRAM表示的是UDP协议
    my_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建socket连接
    # 将socket对象绑定ip地址和端口号
    my_socket.bind(('', 80))
    # 相当于电话的开机 括号里的参数表示可以同时接收5个请求
    my_socket.listen(5)
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=100,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        try:
            # 进入监听状态，等待别人链接过来，有两个返回值，
            #一个是对方的socket对象，一个是对方的ip以及端口
            client, addr = my_socket.accept()
            print('Got a connection from %s' % str(addr))
            # recv表示接收，括号里是最大接收字节
            request = client.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            sensor_readings = read_sensor()
            print(sensor_readings)
            response = web_page()
            client.send('HTTP/1.1 200 OK\n')
            client.send('Content-Type: text/html\n')
            client.send('Connection: close\n\n')
            client.sendall(response)
            client.close()
        except OSError as e:
            conn.close()
            print('Connection closed')
