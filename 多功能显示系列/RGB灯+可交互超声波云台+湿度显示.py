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

#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=5, echo_pin=18)
#定义SG90舵机控制对象
servo = Servo(Pin(22))
#定义DHT22控制对象
dht22=dht.DHT22(Pin(27))
#定义RGB控制对象
#控制引脚为13，RGB灯串联5个
pin=13
rgb_num=5
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)
# LCD 1602 I2C 地址
DEFAULT_I2C_ADDR = 0x27
# 初始化GPIO口
# def setup():
# global lcd
i2c = I2C(1,sda=Pin(17),scl=Pin(16),freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)  # 初始化(设备地址, 背光设置)
#定义按键控制对象
key1=Pin(26,Pin.IN,Pin.PULL_UP)
key2=Pin(25,Pin.IN,Pin.PULL_UP)
key3=Pin(33,Pin.IN,Pin.PULL_UP)
key4=Pin(32,Pin.IN,Pin.PULL_UP)
#定义按键键值
KEY1_PRESS,KEY2_PRESS,KEY3_PRESS,KEY4_PRESS=1,2,3,4
key_en=1

#按键扫描函数
def key_scan():
    global key_en
    if key_en==1 and (key1.value()==0 or key2.value()==0 or
                      key3.value()==0 or key4.value()==0 ):
        time.sleep_ms(10)
        key_en=1
        if key1.value()==0:
            return KEY1_PRESS
        elif key2.value()==0:
            return KEY2_PRESS
        elif key3.value()==0:
            return KEY3_PRESS
        elif key4.value()==0:
            return KEY4_PRESS
    elif key1.value()==1 and key2.value()==1 and key3.value()==1 and key4.value()==1:
        key_en=1
    return 0

b=0
c=140
g=0
h=0
humi=99
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
    global humi
    key=key_scan()
    distance=hcsr04.distance_cm()
    if distance>20 and c<=140:  
        c+=2
        servo.write_angle(c)
    if distance<20 and distance>=0 and c>=50:
        c-=2
        servo.write_angle(c)
    g+=1
    m+=1
    if g==10 : #每10个周期RGB灯随机变色,屏幕刷新
        g=0
        for i in range(rgb_num):
            d=random.randint(0,255)
            e=random.randint(0,255)
            f=random.randint(0,255)
            while True :
                k=d-e
                if k<0 :
                    k=-k
                    l=e-f 
                    if l<0 :
                        l=-l
                if k+l>200 :
                    rgb_led[i]=(d, e, f)
                    break
                else :
                    d=random.randint(0,255)
                    e=random.randint(0,255)
                    f=random.randint(0,255)
            rgb_led.write()
            lcd.putstr("humidity=%.1f"%humi)       
            lcd.putstr("%  ")
            lcd.putstr("distance=%3d"%distance)
            lcd.putstr("cm  ")

    if m==45: #每45个周期测量湿度
        m=0
        dht22.measure()  #调用DHT类库中测量数据的函数
        humi = dht22.humidity()
        
#程序入口
if __name__=="__main__":
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=40,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        pass