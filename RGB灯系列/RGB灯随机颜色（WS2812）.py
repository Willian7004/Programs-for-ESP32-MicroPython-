#接线： WS-->(27)         

#导入Pin模块
from machine import Pin
from neopixel import NeoPixel
import time
import random

#定义RGB控制对象
#控制引脚为16，RGB灯串联5个
pin=27
rgb_num=5
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)  

#程序入口
if __name__=="__main__" :

    while True:        
            for i in range(rgb_num):
                a=random.randint(0,255)
                b=random.randint(0,255)
                c=random.randint(0,255)
                rgb_led[i]=(a, b, c)
                rgb_led.write()
                time.sleep_ms(100)