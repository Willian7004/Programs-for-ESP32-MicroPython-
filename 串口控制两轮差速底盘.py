from machine import *
import time
from motos import *
import _thread

# 编码器初始化
pin17 = Pin(17, Pin.IN)
pin5 = Pin(5, Pin.IN)   
encoder1 = encoder1(pin17, pin5, 0)   # 参数(编码器A相引脚，编码器B相引脚，定时器序号)
pin19 = Pin(19, Pin.IN) 
pin18 = Pin(18, Pin.IN) 
encoder2 = encoder2(pin19, pin18, 2)

# 电机初始化
motor1=PWM(Pin(15),freq=1000,duty=1023)
motor2=PWM(Pin(2),freq=1000,duty=0)
motor3=PWM(Pin(4),freq=1000,duty=1023)
motor4=PWM(Pin(16),freq=1000,duty=0)
 
duty1=0
duty2=0
linear_velocity=0
angular_velocity=0

def set_target(duty1,duty2):
    global linear_velocity
    global angular_velocity
    while True:
        try:
            target=int(input("前2位为角速度+40，后三位为线速度+100"))
            linear_velocity=target%1000-100
            angular_velocity=target//1000-40
        except:
            pass
_thread.start_new_thread(set_target, (duty1, duty2))

while True:
    target1=linear_velocity
    target2=linear_velocity
    target1+=angular_velocity
    target2-=angular_velocity
    speed1 = encoder1.read()
    speed2 = encoder2.read()
    offset1=target1-speed1
    offset2=target2-speed2
    duty1+=offset1
    duty2+=offset2
    if target1<0: #由于实测发现电机反向时不能正常测速，这部分改为开环控制
        duty1=10*target1
    if target2<0:
        duty2=10*target2    
    if duty1<-1023:
        duty1=-1023
    if duty1>1023:
        duty1=1023
    if duty2<-1023:
        duty2=-1023
    if duty2>1023:
        duty2=1023
    if duty1>0:
       motor1.duty(duty1)
       motor2.duty(0)
    if duty1<0:
       motor1.duty(0) 
       motor2.duty(-duty1)
    if duty2>0:
       motor3.duty(duty2)
       motor4.duty(0)
    if duty2<0:
       motor3.duty(0) 
       motor4.duty(-duty2)   
    time.sleep(0.1)
