import time
from machine import SoftI2C,Pin
from servo import Servos
i2c=SoftI2C(sda=Pin(26),scl=Pin(27),freq=10000)
servos=Servos(i2c,address=0x40)

servos.position(0,90)
servos.position(1,90)
servos.position(2,90)
servos.position(3,90)
servos.position(4,90)
#while循环下面操作
while True:
    try:
       receive=int(input('input')) #从前到后输入5个舵机的角度，每个舵机的角度占3位
       a=receive//1000000000000
       servos.position(0,a)
       b=receive%1000000000000
       b=b//1000000000
       servos.position(1,b)
       c=receive%1000000000
       c=c//1000000
       servos.position(2,c)
       d=receive%1000000
       d=d//1000
       servos.position(3,d)
       e=receive%1000
       servos.position(4,e)
    except:
        pass
