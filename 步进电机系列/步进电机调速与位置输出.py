'''
接线说明：电机模块-->ESP32 IO
         (IN1-IN4)-->(15,2,0,4)
         
         电机模块输出-->28BYJ-48步进电机
         (5V)-->红线
         (O1)-->依次排序
         
         按键模块-->ESP32 IO
         (K1-K4)-->(26,25,33,32)
按键功能：KEY1切换正反转，KEY2加速，KEY3减速，KEY4切换高、低速模式
'''
#导入Pin模块
from machine import Pin
import time
from machine import Timer
import tm1637

#定义数码管控制对象
smg=tm1637.TM1637(clk=Pin(16),dio=Pin(17))

#定义按键控制对象
key1=Pin(26,Pin.IN,Pin.PULL_UP)
key2=Pin(25,Pin.IN,Pin.PULL_UP)
key3=Pin(33,Pin.IN,Pin.PULL_UP)
key4=Pin(32,Pin.IN,Pin.PULL_UP)

#定义步进电机控制对象
motor_a=Pin(15,Pin.OUT,Pin.PULL_DOWN)
motor_b=Pin(2,Pin.OUT,Pin.PULL_DOWN)
motor_c=Pin(0,Pin.OUT,Pin.PULL_DOWN)
motor_d=Pin(4,Pin.OUT,Pin.PULL_DOWN)


#定义按键键值
KEY1_PRESS,KEY2_PRESS,KEY3_PRESS,KEY4_PRESS=1,2,3,4
key_en=1
#按键扫描函数
def key_scan():
    global key_en
    if key_en==1 and (key1.value()==0 or key2.value()==0 or
                      key3.value()==0 or key4.value()==0 ):
        time.sleep_ms(10)
        key_en=0
        if key1.value()==0:
            return KEY1_PRESS
        elif key2.value()==0:
            return KEY2_PRESS
        elif key3.value()==0:
            return KEY3_PRESS
        elif key4.value()==0:
            return KEY4_PRESS
    elif key1.value()==1 and key2.value()==1 and key3.value()==1 and key4.value()==1:
        key_en=1
    return 0
    

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

def time0_irq(time0):
    global count
    if count>4095 :
        count-=4096
    if count<0 :
        count+=4096    
    print("位置",count)
    smg.show("%04d"%count)
    
#程序入口
if __name__=="__main__":
    count=0
    key=0
    fx1=1
    speed1=1
    step1=0
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=100,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
      if speed1<4:
        key=key_scan()
        if key==KEY1_PRESS:
            fx1=not fx1 
        elif key==KEY2_PRESS:
            if speed1>1:
                speed1-=1
        elif key==KEY3_PRESS:
                speed1+=1
        elif key==KEY4_PRESS:
                speed1=900        
        step_motor_send_pulse(step1,fx1)
        step1+=1
        if fx1==1 :
            count+=1
        if fx1==0 :
            count-=1    
        if step1==8:
            step1=0
        time.sleep_ms(speed1)
      elif 3<speed1<10:
        key=key_scan()
        if key==KEY1_PRESS:
            fx1=not fx1 
        elif key==KEY2_PRESS:
             speed1-=2
        elif key==KEY3_PRESS:
             speed1+=2
        elif key==KEY4_PRESS:
                speed1=900     
        step_motor_send_pulse(step1,fx1)
        step1+=1
        if fx1==1 :
            count+=1
        if fx1==0 :
            count-=1 
        if step1==8:
            step1=0
        time.sleep_ms(speed1)
      elif 9<speed1<22:
        key=key_scan()
        if key==KEY1_PRESS:
            fx1=not fx1 
        elif key==KEY2_PRESS:
             speed1-=4
        elif key==KEY3_PRESS:
             speed1+=4
        elif key==KEY4_PRESS:
                speed1=900     
        step_motor_send_pulse(step1,fx1)
        step1+=1
        if fx1==1 :
            count+=1
        if fx1==0 :
            count-=1 
        if step1==8:
            step1=0
        time.sleep_ms(speed1)
      elif 21<speed1<47:
        key=key_scan()
        if key==KEY1_PRESS:
            fx1=not fx1 
        elif key==KEY2_PRESS:
             speed1-=8
        elif key==KEY3_PRESS:
            if speed1<46:
              speed1+=8
        elif key==KEY4_PRESS:
                speed1=900     
        step_motor_send_pulse(step1,fx1)
        step1+=1
        if fx1==1 :
            count+=1
        if fx1==0 :
            count-=1 
        if step1==8:
            step1=0
        time.sleep_ms(speed1)
      elif speed1>599:
        key=key_scan()
        if key==KEY1_PRESS:
            fx1=not fx1 
        elif key==KEY2_PRESS:
            if speed1>600:
             speed1-=100
        elif key==KEY3_PRESS:
            if speed1<900:
             speed1+=100
        elif key==KEY4_PRESS:
                speed1=1     
        step_motor_send_pulse(step1,fx1)
        step1+=1
        if fx1==1 :
            count+=1
        if fx1==0 :
            count-=1 
        if step1==8:
            step1=0
        time.sleep_us(speed1)
        