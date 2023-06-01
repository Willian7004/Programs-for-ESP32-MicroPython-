'''
         橙色(信号线)-->(17)
         红色(电源正)-->(5V)
         褐色(电源负)-->(GND)         
'''

#导入Pin模块
from machine import Pin
import time
from servo import Servo
from machine import ADC
from machine import Timer

#定义SG90舵机控制对象
my_servo = Servo(Pin(17))
adc=ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V

b=0
def time0_irq(time0):
    b=180*adc.read()//4095
    my_servo.write_angle(b) 

#程序入口
if __name__=="__main__":
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=20,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        pass