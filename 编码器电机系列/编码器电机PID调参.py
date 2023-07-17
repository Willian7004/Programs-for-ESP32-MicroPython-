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
pin17 = Pin(17, Pin.IN)
pin5 = Pin(5, Pin.IN)   
encoder = encoder(pin17, pin5, 0)   # 参数(编码器A相引脚，编码器B相引脚，定时器序号)

# 电机初始化
motor=PWM(Pin(15),freq=1000,duty=0)
duty=0
target=50
count=0
offset=0 #e(k)
offset1=0 #e(k-1)
offset2=0 #e(k-2)
p=10 #PID参数
i=2
d=0
  
while True:
    count+=1
    speed = encoder.read()
    offset2=offset1 #记录上一次偏差
    offset1=offset
    offset=target-speed
    adjustmentP=offset-offset1
    adjustmentP*=p
    adjustmentI=offset
    adjustmentI*=i
    adjustmentD=offset-offset1-offset1+offset2
    adjustmentD*=d
    adjustment=adjustmentP+adjustmentI+adjustmentD
    duty+=adjustment
    if duty<0:
        duty=0
    elif duty>1023:
        duty=1023
    motor.duty(duty)
    print(target,speed,offset,duty)
    time.sleep(0.05)
    if count==40:
        count=0
        target=random.randint(0,70)
