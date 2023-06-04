#接线：(IR)-->(14)
#接线： WS-->(27)
'''
Pin15、2、0、4、17、5、18、19依次控制左前、右前、左后、右后轮正、反转
SR04:trigger-->12 echo-->14  舵机:橙色(信号线)-->(17)
'''
#导入Pin模块
from machine import Pin
from neopixel import NeoPixel
import time
from machine import Timer
import random
from hcsr04 import HCSR04
from servo import Servo

#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=12, echo_pin=14)
#定义SG90舵机控制对象
my_servo = Servo(Pin(17))

pin=13
rgb_num=5
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

led1=Pin(15,Pin.OUT)#构建led1对象，GPIO15输出
led2=Pin(2,Pin.OUT)
led3=Pin(0,Pin.OUT)
led4=Pin(4,Pin.OUT)
led5=Pin(17,Pin.OUT)
led6=Pin(5,Pin.OUT)
led7=Pin(18,Pin.OUT)
led8=Pin(19,Pin.OUT)    

def wheels(d,e,f,g,h,i,j,k) :
    led1.value(d)
    led2.value(e)
    led3.value(f)
    led4.value(g)
    led5.value(h)
    led6.value(i)
    led7.value(j)
    led8.value(k)
        
while True:
    my_servo.write_angle(105)
    distance=hcsr04.distance_cm()
    time.sleep_ms(100)
    if distance>20 :
          wheels(1,0,1,0,1,0,1,0)
    elif distance<=20 :
       while True :
          wheels(1,0,0,1,1,0,0,1)
          time.sleep_ms(100)
          wheels(0,0,0,0,0,0,0,0)
          distance=hcsr04.distance_cm()
          if distance>20 :
              break
    my_servo.write_angle(75)
    distance=hcsr04.distance_cm()
    time.sleep_ms(100)
    if distance>20 :
          wheels(1,0,1,0,1,0,1,0)
    if distance<=20 :
       while True :
          wheels(0,1,1,0,0,1,1,0)
          time.sleep_ms(50)
          wheels(0,0,0,0,0,0,0,0)
          distance=hcsr04.distance_cm()
          if distance>20 :
              break
    for i in range(rgb_num):
        a=random.randint(0,255)
        b=random.randint(0,255)
        c=random.randint(0,255)
        rgb_led[i]=(a, b, c)
        rgb_led.write()       
