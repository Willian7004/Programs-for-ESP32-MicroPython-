'''
接线：SR04
         trigger-->12
         echo-->14         
      OLED(IIC)
         SCL-->(18)
         SDA-->(23)
      舵机   
         橙色(信号线)-->(17)
         红色(电源正)-->(5V)
         褐色(电源负)-->(GND) 
'''
from machine import Pin,SoftI2C,Timer
from time import sleep
from ssd1306 import SSD1306_I2C
from machine import RTC
from hcsr04 import HCSR04
from servo import Servo

#初始化OLED
i2c = SoftI2C(sda=Pin(23), scl=Pin(18))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=12, echo_pin=14)
#定义SG90舵机控制对象
my_servo = Servo(Pin(17))

a=-1
b=0
#中断回调函数
def fun(tim):
    global a
    global b
    while a<128 :
        a+=1
        distance=round(hcsr04.distance_cm()/1)
        b=64-distance
        c=154-a
        my_servo.write_angle(c)
        if b<0 :
          b=0
        #清除将要显示的列的像素
        oled.vline(a,0,64,0)  
        #距离图形化显示
        oled.vline(a,0,b,1)
        oled.show()
    while a>=0 :
        a-=1
        distance=round(hcsr04.distance_cm()/1)
        b=64-distance
        c=154-a
        my_servo.write_angle(c)
        if b<0 :
          b=0
        #清除将要显示的列的像素
        oled.vline(a,0,64,0) 
        #距离图形化显示
        oled.vline(a,0,b,1)
        oled.show()    

#开启RTOS定时器
tim = Timer(-1)
tim.init(period=1, mode=Timer.PERIODIC, callback=fun) 
