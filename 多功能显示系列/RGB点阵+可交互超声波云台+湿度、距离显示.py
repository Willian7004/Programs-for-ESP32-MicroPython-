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

brightness=18
delay=40
mode=1
def key_get(): #获取键值并改变变量的值
    global brightness
    global delay
    global mode
    key=key_scan()
    if key==1 and brightness<60 :
        brightness+=6
    elif key==2 and brightness>6 :
        brightness-=6
    elif key==3 and delay<90 :
        delay+=10
    elif key==4 and delay>10 :
        delay-=10
    elif key==5 and mode<1 :
        mode+=1
    elif key==6 and mode>0 :
        mode-=1     

b=0
c=120
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
    global brightness
    global delay
    global mode
    key_get()
    distance=hcsr04.distance_cm()
    if distance>15 and c<=120:  
        c+=2
        servo.write_angle(c)
    if distance<15 and distance>=0 and c>=60:
        c-=2
        servo.write_angle(c)
    g+=1
    m+=1
    if g==8 : #每8个周期RGB灯随机变色,屏幕刷新
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