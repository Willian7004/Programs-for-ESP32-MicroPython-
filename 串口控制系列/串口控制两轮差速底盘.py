from machine import *
import time
from motos import *
import _thread
'''
底盘参数计算（最终结果保留3位有效数字）
(speed为编码器脉冲计数)
轮直径：0.065
轮周长：0.2041
每圈脉冲数：110
底盘周长：0.6908
底盘直径/每rad长：0.22
每次脉冲长度：0.001855
线速度：speed*10*0.001855=speed*0.0186
角速度：(speed1-speed2)*10*0.001855/0.22=(speed1-speed2)*0.0843
考虑丢步情况，大约只有63%的脉冲能被统计，因此公式改为：
线速度=speed/0.63*0.0186=speed*0.0295
角速度=(speed1-speed2)/0.63*0.0843=(speed1-speed2)*0.134
每旋转1度（一边轮静止，另一边旋转）所需脉冲数=0.22*2*3.14/360/0.00186*0.63=1.30
每行驶1米所需脉冲数：1/0.001855*0.63=340
'''
# 编码器初始化
pin17 = Pin(17, Pin.IN)
pin5 = Pin(5, Pin.IN)   
encoder1 = encoder1(pin17, pin5, 0)   # 参数(编码器A相引脚，编码器B相引脚，定时器序号)
pin19 = Pin(19, Pin.IN) 
pin18 = Pin(18, Pin.IN) 
encoder2 = encoder2(pin19, pin18, 2)

# 电机初始化
motor1=PWM(Pin(15),freq=1000,duty=0)
motor2=PWM(Pin(2),freq=1000,duty=0)
motor3=PWM(Pin(4),freq=1000,duty=0)
motor4=PWM(Pin(16),freq=1000,duty=0)
 
duty1=0
duty2=0
linear_velocity=0
angular_velocity=0
target1=0
target2=0
offset1=0
offset2=0
'''
distance=0
angle=0
target_distance=0
target_angle=0
flag=0
'''

def set_target(duty1,duty2):
    global linear_velocity
    global angular_velocity
    global target1
    global target2
    global target_distance
    global target_angle
    global flag
    while True:
        try:
            target=int(input("input"))
            ''' #控制底盘旋转一定角度并前进一定距离，实测不能正常运行，已弃用
            if target//1000>600: #前3位组成的数大于600时控制行驶距离和旋转角度
                target_distance=target%1000 #后三位为距离*100
                target_angle=target//1000-800 #前三位为旋转角度+800，角度为正时右转
                target_angle=round(target_angle*1.3)
                target_distance=round(target_distance*0.34)
                print(target_angle,target_distance)
                flag=1
                target=0
            elif target>0: #前3位组成的数小于600时控制线速度和角速度
            '''
            linear_velocity=target%1000-400 #前三位为角速度*100+400，角速度为正时右转，后三位为线速度*100+400
            angular_velocity=target//1000-400 #换算时数字放大1000倍，除法运算后结果不用缩小
            target_speed=linear_velocity/2.95 #计算每周期目标脉冲数
            target_offset=angular_velocity/26.8 #计算每周期目标脉冲数差并换算为每边车轮速度与平均速度的差
            target1=round(target_speed+target_offset) #左轮目标每周期脉冲数
            target2=round(target_speed-target_offset) #右轮目标每周期脉冲数
            target=0
        except:
            pass
_thread.start_new_thread(set_target, (duty1, duty2))

while True:
    speed1 = encoder1.read() #编码器读数
    speed2 = encoder2.read()
    Offset1=offset1 #记录上一次偏差
    Offset2=offset2
    offset1=target1-speed1 
    offset2=target2-speed2
    adujstment1=offset1*3-Offset1*2 #PID控制：P=3，I=1
    adujstment2=offset2*3-Offset2*2
    duty1+=adujstment1
    duty2+=adujstment2
    ''' #控制底盘旋转一定角度并前进一定距离，实测不能正常运行，已弃用
    if flag==1: #指定角度转向
        print(flag,angle)
        if 0<target_angle-angle<10 or 0>target_angle-angle>-10:
            target1=0
            target2=0
            flag=2
            angle=0
            target_angle=0
        if target_angle>0: #右转
            target1=20
            target2=0
            angle+=speed1
        if target_angle<0: #左转
            target1=0
            target2=20
            angle+=speed2
    if flag==2: #指定距离直行
        print(flag,distance)
        if target_distance-distance>400:
            target1=100
            target2=100
        elif target_distance-distance>100:
            target1=25
            target2=25
        elif target_distance-distance>40:
            target1=10
            target2=10
        elif target_distance-distance<15:
            target1=0
            target2=0
            flag=0
            distance=0
            target_distance=0
        distance+=speed1
        '''
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
