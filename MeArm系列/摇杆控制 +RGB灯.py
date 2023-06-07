'''
  舵机1-->(17)
  舵机2-->(16)
  舵机3-->(22)         
'''

#导入Pin模块
from machine import Pin
import time
from servo import Servo
from machine import ADC
from machine import Timer
from neopixel import NeoPixel
import random

#定义RGB控制对象
#控制引脚为13，RGB灯串联5个
pin=13
rgb_num=5
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)  

#定义SG90舵机控制对象
servo1 = Servo(Pin(17))
servo2 = Servo(Pin(16))
servo3 = Servo(Pin(22))

#定义ADC控制对象
adc1=ADC(Pin(35))
adc1.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
#定义ADC控制对象
adc2=ADC(Pin(34))
adc2.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
#定义ADC控制对象
adc3=ADC(Pin(39))
adc3.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V

a=90
b=150
c=100
g=0

servo1.write_angle(a)
servo2.write_angle(b)
servo3.write_angle(c)
#定时器0中断函数
def time0_irq(time0):
    global a
    global b
    global c
    global g
    if adc1.read()>3000 and a<=179:
        a+=1
        servo1.write_angle(a)
    if adc1.read()<1000 and a>=1:
        a-=1
        servo1.write_angle(a)
    if adc2.read()>3000 and b<=170:
        b+=1
        servo2.write_angle(b)
    if adc2.read()<1000 and b>=0:
        b-=1
        servo2.write_angle(b)
    if adc3.read()>3000 and c<=180:
        c+=1
        servo3.write_angle(c)
    if adc3.read()<1000 and c>=25:
        c-=1
        servo3.write_angle(c)
    g+=1
    if g==10 :
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