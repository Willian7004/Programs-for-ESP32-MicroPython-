import time
from machine import SoftI2C,Pin
from servo import Servos
import _thread
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
mode=0
delay=300

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
        servos.position(7,90-angle)
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

i1=0
i2=0
def function(i1, i2): #功能函数，执行连续进行的动作
    global mode
    global delay
    global Height1
    global Height2
    while True:
        if Height1>45 and mode>0 and mode<7: #参数超出范围时设为最大值,但不处于功能函数内的模式时不更改数值
            Height1=45
        if Height2>45 and mode>0 and mode<7: #参数超出范围时设为最大值,但不处于功能函数内的模式时不更改数值
            Height2=45    
        if mode==0 or mode>6: #不执行功能
            Step=0 #步数复位            
        elif mode==1: #爬行功能
            if Step==0:
                tilt(Height1,Height1) #先降低高度
                Step=1 #改变变量的值以进入下一步骤
            elif Step==1:    
                crawl(1,Height1)
                Step=2
            elif Step==2:    
                crawl(2,Height1)
                Step=3
            elif Step==3:    
                crawl(3,Height1)
                Step=4
            elif Step==4:    
                crawl(4,Height1)
                Step=1
        elif mode==2: #爬行功能（反向）
            if Step==0:
                tilt(Height1,Height1) #先降低高度
                Step=4 #改变变量的值以进入下一步骤
            elif Step==4:    
                crawl(4,Height1)
                Step=3
            elif Step==3:    
                crawl(3,Height1)
                Step=2
            elif Step==2:    
                crawl(2,Height1)
                Step=1
            elif Step==1:    
                crawl(1,Height1)
                Step=4             
        elif mode==3: #步行功能（由于只有两个步骤，无正反向调节，可能不能正常使用，后续视实际测试情况进行调整）
            if Step>2:
                Step=0
            if Step==0:
                tilt(Height1,Height1) #先降低高度
                Step=1 #改变变量的值以进入下一步骤
            elif Step==1:    
                walk(1,Height1)
                Step=2
            elif Step==2:    
                walk(2,Height1)
                Step=1
        elif mode==4: #前后倾斜
            if Step>2:
                Step=0
            if Step==0:
                tilt(0,0) #回到直立状态
                Step=1 #改变变量的值以进入下一步骤
            elif Step==1:    
                tilt(Height1,Height2)
                Step=2
            elif Step==2:
                tilt(Height1,Height2) #向反方向倾斜
                Step=0
        elif mode==5: #蹲起动作
            if Step>1:
                Step=0
            if Step==0:
                tilt(0,0) #回到直立状态
                Step=1 #改变变量的值以进入下一步骤
            elif Step==1:    
                tilt(Height1,Height2)
                Step=0
        elif mode==6: #抬脚动作
            tilt(0,0) #回到直立状态
            if Step==1:
                servos.position(4,20)
                Step=2 #改变变量的值以进入下一步骤
            elif Step==2:    
                servos.position(4,90)
                Step=3
            elif Step==3:    
                servos.position(5,20)
                Step=4
            elif Step==4:    
                servos.position(5,90)
                Step=1    
        time.sleep_ms(delay)

#开启线程
_thread.start_new_thread(function, (i1, i2))
    
while True:
    try:    
        data=int(input('input')) #输入9位数字
        mode=data//100000000 #第一位为模式
        Height1=data%100000000 #第二、三位为前部高度或步长
        Height1=Height1//1000000
        Height2=data%1000000 #第四、五、六位为后部高度或旋转角度
        Height2=Height2//1000
        delay=data%1000 #最后三位为延时
        #非连续执行的功能在此处执行
        if mode==7: #直行功能
            if Height2<=180: #参数超出范围则不执行，下同
                straight(Height2)  
        elif mode==8: #转向功能
            if Height2<=180:
                turn(Height2)
        elif mode==9: #倾斜功能
            if Height1<=60 and Height2<=60:
                tilt(Height1,Height2)        
    except:
        pass
    
