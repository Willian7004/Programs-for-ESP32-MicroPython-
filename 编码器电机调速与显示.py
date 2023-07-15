from machine import *
import time
from moto import *
import random

# 编码器初始化
pin27 = Pin(27, Pin.IN)
pin14 = Pin(14, Pin.IN)   
encoder = encoder(pin27, pin14, 0)   # 参数(编码器A相引脚，编码器B相引脚，定时器序号)

# 电机初始化
motor=PWM(Pin(15),freq=1000,duty=0)
duty=0
target=50
count=0
  
while True:
    count+=1
    speed = encoder.read()
    offset=target-speed
    adjustment=offset*2
    duty+=offset
    if duty<0:
        duty=0
    elif duty>1023:
        duty=1023
    motor.duty(duty)
    print(target,speed,offset,duty)
    time.sleep(0.05)
    if count==100:
        count=0
        target=random.randint(0,70)
