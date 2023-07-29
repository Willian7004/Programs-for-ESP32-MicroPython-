import time
from machine import SoftI2C,Pin
from servo import Servos
i2c=SoftI2C(sda=Pin(9),scl=Pin(8),freq=10000)
servos=Servos(i2c,address=0x40)

servos.position(0,90)
servos.position(1,90)
servos.position(2,90)
servos.position(3,90)
servos.position(4,90)
servos.position(5,90)
servos.position(6,90)
servos.position(7,90)
servos.position(8,120)
servos.position(9,120)
servos.position(10,120)
servos.position(11,120)
time.sleep(1)

Height1=0 #前部高度，0为最高
Height2=0 #后部高度，0为最高

def straight(angle): #直行，给所有转向舵机写入相应角度以调整方向
    servos.position(0,angle)
    servos.position(1,angle)
    servos.position(2,angle)
    servos.position(3,angle)

def turn(angle): #倾斜
    servos.position(0,angle)
    servos.position(1,angle)
    servos.position(2,180-angle)
    servos.position(3,180-angle)

def tilt(height1,height2): #前后倾斜,局部变量与全局变量通过大小写区分
    servos.position(4,90-height1)
    servos.position(5,90-height1)
    servos.position(6,90-height2)
    servos.position(7,90-height2)
    servos.position(8,120-height1-height1) #底部舵机使用两倍偏置以确保平衡
    servos.position(9,120-height1-height1)
    servos.position(10,120-height2-height2)
    servos.position(11,120-height2-height2)
    
while True: #测试
    straight(30)
    time.sleep(0.5)
    straight(90)
    time.sleep(0.5)
    straight(120)
    time.sleep(0.5)
    straight(90)
    time.sleep(0.5)
    turn(30)
    time.sleep(0.5)
    turn(90)
    time.sleep(0.5)
    turn(120)
    time.sleep(0.5)
    turn(90)
    time.sleep(0.5)
    Height1=15
    tilt(Height1,Height2)
    time.sleep(1)
    Height1=0
    tilt(Height1,Height2)
    time.sleep(1)
    Height2=15
    tilt(Height1,Height2)
    time.sleep(1)
    Height2=0
    tilt(Height1,Height2)
    time.sleep(1)
    Height1=15
    Height2=15
    tilt(Height1,Height2)
    time.sleep(1)
    Height1=0
    Height2=0
    tilt(Height1,Height2)
    time.sleep(1)
    
