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
    
def crawl(step,angle): #爬行，第一个参数为步骤数,第二个参数为相比直立状态降低的角度，步长随第二个参数的增大而增大
    if step==1:
        servos.position(4,90-angle-angle)
    if step==2:
        servos.position(5,90-angle-angle)
    if step==3:
        servos.position(6,90-angle-angle)
    if step==4:
        servos.position(4,90-angle)
        servos.position(5,90-angle)
        servos.position(6,90-angle)
        servos.position(7,90-angle-angle)   
        
def walk(step,angle): #步行，第一个参数为步骤数,第二个参数为相比直立状态降低的角度，步长随第二个参数的增大而增大
    if step==1:
        servos.position(4,90-angle-angle)
        servos.position(5,90-angle)
        servos.position(6,90-angle)
        servos.position(7,90-angle-angle)
    if step==2:
        servos.position(4,90-angle)
        servos.position(5,90-angle-angle)
        servos.position(6,90-angle-angle)
        servos.position(7,90-angle)
    
while True: #测试
    tilt(25,25)
    time.sleep(0.6)
    crawl(1,25)
    time.sleep(0.3)
    crawl(2,25)
    time.sleep(0.3)
    crawl(3,25)
    time.sleep(0.3)
    crawl(4,25)
    time.sleep(0.3)
    crawl(1,25)
    time.sleep(0.3)
    crawl(2,25)
    time.sleep(0.3)
    crawl(3,25)
    time.sleep(0.3)
    crawl(4,25)
    time.sleep(0.3)
    tilt(25,25)
    time.sleep(0.6)
    walk(1,25)
    time.sleep(0.3)
    walk(2,25)
    time.sleep(0.3)
    walk(1,25)
    time.sleep(0.3)
    walk(2,25)
    time.sleep(0.3)
    walk(1,25)
    time.sleep(0.3)
    walk(2,25)
    time.sleep(0.3)
