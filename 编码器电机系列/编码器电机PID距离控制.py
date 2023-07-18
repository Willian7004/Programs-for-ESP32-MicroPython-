from machine import *
import time
from moto import *
import random
'''
本程序使用增量式PID，公式为
Pwm+=Kp[e(k)-e(k-1)]+Ki*e(k)+Kd[e(k)-2e(k-1)+e(k-2)]
e(k)：本次偏差
e(k-1)：上一次的偏差
e(k-2)：上上次的偏差
Kp：比例项参数
Ki：积分项参数
Kd：微分项参数
Pwm：代表增量输出
'''
# 编码器初始化
pin18 = Pin(18, Pin.IN)
pin19 = Pin(19, Pin.IN)   
encoder = encoder(pin18, pin19, 0)   # 参数(编码器A相引脚，编码器B相引脚，定时器序号)

# 电机初始化
motor=Pin(15,Pin.OUT)
motor.value(0)
motor1=PWM(Pin(4),freq=1000,duty=0)
motor2=PWM(Pin(16),freq=1000,duty=0)
while True:
    speed = encoder.read() #测试时发现有时候占空比不能回0，就增加一项检测，确保占空比回零
    if speed>2 or speed<-2: 
        motor1.duty(0)    
        motor2.duty(0)
    else:
        break
duty=0
target=0
distance=0
offset=0 #e(k)
offset1=0 #e(k-1)
offset2=0 #e(k-2)
p=8 #PID参数
i=5
d=6
  
while True:
    motor1.duty(0)    
    motor2.duty(0)
    motor1.duty(0)    
    motor2.duty(0)
    target=int(input('target_distance'))
    while True:
        speed = encoder.read()
        distance+=speed
        offset2=offset1 #记录上一次偏差
        offset1=offset
        offset=target-distance
        adjustmentP=offset-offset1
        adjustmentP*=p
        adjustmentI=offset
        adjustmentI=round(adjustmentI*i)
        adjustmentD=offset-offset1-offset1+offset2
        adjustmentD*=d
        duty=adjustmentP+adjustmentI+adjustmentD
        if duty<-1023:
            duty=-1023
        elif duty>1023:
            duty=1023
        if duty>0:
            if duty<200:
                duty=200
            motor1.duty(duty)
            motor2.duty(0)
        if duty<0:
            if duty>-200:
                duty=-200
            motor1.duty(0)    
            motor2.duty(-duty)
        print(offset,duty)
        if offset<11 and offset>-11 and speed<11 and speed>-11: #误差的速度较小时停止
            motor1.duty(0)    
            motor2.duty(0)
            while True:
                speed = encoder.read() #测试时发现有时候占空比不能回0，就增加一项检测，确保占空比回零
                if speed>2 or speed<-2: 
                    motor1.duty(0)    
                    motor2.duty(0)
                else:
                    break
            distance=0 #不归零则可以控制距开始位置的角度
            break
        time.sleep(0.05)
    
