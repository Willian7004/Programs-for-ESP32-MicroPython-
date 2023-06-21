'''
  舵机1-->(17)
  舵机2-->(16)
  舵机3-->(22)
  (Trig)-->(5)
  (Echo)-->(18)
  SCL-->19
  SDA-->21
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
import dht
from machine import RTC

#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=5, echo_pin=18)
#定义SG90舵机控制对象
servo1 = Servo(Pin(17))
servo2 = Servo(Pin(16))
servo3 = Servo(Pin(22))
#定义RGB控制对象
#控制引脚为13，RGB灯串联5个
pin=13
rgb_num=5
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)
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

a=100
b=0
c=130
g=0
h=0
j=150
temp=0
humi=0
k=0
l=0
servo1.write_angle(a)
servo2.write_angle(j)
servo3.write_angle(c)
#定时器0中断函数
def time0_irq(time0):
    global a
    global b
    global c
    global g
    global h
    global j
    global k
    global l
    global temp
    global humi
    key=key_scan()
    if key==KEY1_PRESS and a<=120:
        a+=1
        servo1.write_angle(a)
    if key==KEY2_PRESS and a>=60:
        a-=1
        servo1.write_angle(a)
    if key==KEY3_PRESS and j<=170:
        j+=1
        servo2.write_angle(j)
    if key==KEY4_PRESS and j>=130:
        j-=1
        servo2.write_angle(j)    
    distance=hcsr04.distance_cm()//1
    if distance>13 and c<=150:  #机械臂跟随操作者
        c+=2
        servo3.write_angle(c)
    if distance<13 and distance>=0 and c>=25:
        c-=2
        servo3.write_angle(c)
    g+=1
    h+=1
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
        
#程序入口
if __name__=="__main__":
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=40,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        pass