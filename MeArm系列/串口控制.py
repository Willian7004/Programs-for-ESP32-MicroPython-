'''
  舵机1-->(17)
  舵机2-->(16)
  舵机3-->(22)
  舵机4-->(27)       
'''

#导入Pin模块
from machine import Pin
import time
from servo import Servo

#定义SG90舵机控制对象
servo1 = Servo(Pin(17))
servo2 = Servo(Pin(16))
servo3 = Servo(Pin(22))
servo4 = Servo(Pin(27))

#程序入口
if __name__=="__main__":

    while True:
        a=int(input("舵机1角度（0-180）")) #角度减小，顺时针转；角度增大，逆时针转 
        servo1.write_angle(a)
        a=int(input("舵机2角度（0-150）")) #角度越大，位置越高
        servo2.write_angle(a)
        a=int(input("舵机3角度（25-180）")) #角度越大，位置越低 
        servo3.write_angle(a)
        a=int(input("舵机4角度（12-30）")) #小角度闭合，大角度张开
        servo4.write_angle(a) 
