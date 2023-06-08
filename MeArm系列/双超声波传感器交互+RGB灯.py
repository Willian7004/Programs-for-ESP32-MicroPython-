'''
  舵机1-->(17)
  舵机2-->(16)
  舵机3-->(22)
  (Trig)-->(5)
  (Echo)-->(18)
'''

#导入Pin模块
from machine import Pin
import time
from servo import Servo
from machine import Timer
from hcsr04 import HCSR04
from neopixel import NeoPixel
import random

#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=5, echo_pin=18)
hcsr04A=HCSR04A(trigger_pin=14, echo_pin=9)
#定义SG90舵机控制对象
servo1 = Servo(Pin(17))
servo2 = Servo(Pin(16))
servo3 = Servo(Pin(22))
#定义RGB控制对象
#控制引脚为13，RGB灯串联5个
pin=13
rgb_num=5
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)  

a=90
b=0
c=100
g=0
servo1.write_angle(a)
servo2.write_angle(160)
servo3.write_angle(c)
#定时器0中断函数
def time0_irq(time0):
    global a
    global b
    global c
    global g
    distance=hcsr04.distance_cm()//1
    if distance>15 and c<=180:  #机械臂跟随操作者
        c+=1
        servo3.write_angle(c)
    if distance<15 and c>=25:
        c-=1
        servo3.write_angle(c)
    if distance>30 : #暂停交互
        b=2
        c=100
        servo3.write_angle(c)
    if distance<20 and b==2: #恢复交互
        b=0    
    distanceA=hcsr04A.distance_cm()//1
    if distanceA>30 : #切换转向方向
        if b==0 :
            b=1
        if b==1 :
            b=0
    if distanceA<15 : #机械臂转向
        if b==0 and a>0:
            a-=1
            servo1.write_angle(a)
        if b==1 and a<180:
            a+=1
            servo1.write_angle(a)    
    g+=1
    if g==10 : #每10个周期RGB灯随机变色
        g=0
        for i in range(rgb_num):
            d=random.randint(0,255)
            e=random.randint(0,255)
            f=random.randint(0,255)
            rgb_led[i]=(d, e, f)
            rgb_led.write()     
        
#程序入口
if __name__=="__main__":
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=30,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        pass