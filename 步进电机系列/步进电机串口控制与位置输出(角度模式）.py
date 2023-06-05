'''
接线说明：电机模块-->ESP32 IO
         (IN1-IN4)-->(15,2,0,4)
         
         电机模块输出-->28BYJ-48步进电机
         (5V)-->红线
         (O1)-->依次排序                  
'''
#导入Pin模块
from machine import Pin
import time
import tm1637

#定义数码管控制对象
smg=tm1637.TM1637(clk=Pin(16),dio=Pin(17))

#定义步进电机控制对象
motor_a=Pin(15,Pin.OUT,Pin.PULL_DOWN)
motor_b=Pin(2,Pin.OUT,Pin.PULL_DOWN)
motor_c=Pin(0,Pin.OUT,Pin.PULL_DOWN)
motor_d=Pin(4,Pin.OUT,Pin.PULL_DOWN)
    
#步进电机发送脉冲函数
def step_motor_send_pulse(step,fx):
    temp=step
    if fx==0:
        temp=7-step
    if temp==0:
        motor_a.value(1)
        motor_b.value(0)
        motor_c.value(0)
        motor_d.value(0)
    elif temp==1:
        motor_a.value(1)
        motor_b.value(1)
        motor_c.value(0)
        motor_d.value(0)
    elif temp==2:
        motor_a.value(0)
        motor_b.value(1)
        motor_c.value(0)
        motor_d.value(0)
    elif temp==3:
        motor_a.value(0)
        motor_b.value(1)
        motor_c.value(1)
        motor_d.value(0)
    elif temp==4:
        motor_a.value(0)
        motor_b.value(0)
        motor_c.value(1)
        motor_d.value(0)
    elif temp==5:
        motor_a.value(0)
        motor_b.value(0)
        motor_c.value(1)
        motor_d.value(1)
    elif temp==6:
        motor_a.value(0)
        motor_b.value(0)
        motor_c.value(0)
        motor_d.value(1)
    elif temp==7:
        motor_a.value(1)
        motor_b.value(0)
        motor_c.value(0)
        motor_d.value(1)

count=0
while True:
    print("位置",count)
    smg.show("%04d"%count)
    fx1=0
    step1=0
    s=0  
    i=int(input("输入角度（步数为正时顺时针转，反之逆时针转）"))
    count=count+i
    if count<0 :
        count+=360
    if count>359 :
        count-=360
    if i<0 :
        fx1=1
        i=-i
    i=i/365*4096    
    while True:
        step_motor_send_pulse(step1,fx1)
        step1+=1
        s+=1
        if s>=i :
            break
        if step1==8:
            step1=0
        time.sleep_ms(1)
    
