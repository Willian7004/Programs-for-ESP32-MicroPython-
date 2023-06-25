#导入Pin模块
from machine import Pin
import time
from machine import PWM
from neopixel import NeoPixel

#定义RGB灯控制对象 
pin=22
rgb_num=30
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

i=0
flag=0
brightness1=255
#程序入口
while True:
    if brightness1>0 : 
        brightness1-=1
        brightness2=255-brightness1
    elif brightness1==0 : #每次渐变结束后切换颜色
        flag+=1
        brightness1=255
        brightness2=0
    if flag==3 :
        flag=0    
    if flag==0 :    
        while i<10 : #每10个灯显示不同颜色
            rgb_led[i]=(brightness1, brightness2, 0)
            i+=1
        while i<20 :
            rgb_led[i]=(0, brightness1, brightness2)
            i+=1
        while i<30 :
            rgb_led[i]=(brightness2, 0, brightness1)
            i+=1
        i=0
    if flag==1 :     
        while i<10 :
            rgb_led[i]=(0, brightness1, brightness2)
            i+=1
        while i<20 :
            rgb_led[i]=(brightness2, 0, brightness1)
            i+=1
        while i<30 :
            rgb_led[i]=(brightness1, brightness2, 0)
            i+=1
        i=0
    if flag==2 :     
        while i<10 :
            rgb_led[i]=(brightness2, 0, brightness1)
            i+=1
        while i<20 :
            rgb_led[i]=(brightness1, brightness2, 0)
            i+=1
        while i<30 :
            rgb_led[i]=(0, brightness1, brightness2)
            i+=1
        i=0  
    rgb_led.write()
