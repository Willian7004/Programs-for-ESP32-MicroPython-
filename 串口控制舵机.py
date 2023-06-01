'''
         橙色(信号线)-->(17)
         红色(电源正)-->(5V)
         褐色(电源负)-->(GND)         
'''

#导入Pin模块
from machine import Pin
import time
from servo import Servo

#定义SG90舵机控制对象
my_servo = Servo(Pin(17))

#程序入口
if __name__=="__main__":

    while True:
        a=int(input("舵机角度（0-180）"))
        my_servo.write_angle(a)         
