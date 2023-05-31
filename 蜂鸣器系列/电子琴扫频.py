#导入Pin模块
from machine import Pin
import time

#定义蜂鸣器控制对象
beep=Pin(25,Pin.OUT)   
    
#程序入口
e=10
while True:
    i=0
    b=1
    e+=1
    if e%10==8 :
      e+=3
    if e==91 :
      e==11  
    a=0
    t=0
    if e%10==1 :
      a=4186
    elif e%10==2 :
      a=4698
    elif e%10==3 :
      a=5274
    elif e%10==4 :
      a=5587
    elif e%10==5 :
      a=6272
    elif e%10==6 :
      a=7040
    elif e%10==7 :
      a=7901
    elif e//10<9 :
      t=e//10
      e=9-t
      t=2**e
      a=round(a/t)
    d=a/5
    c=0
    if 0<a<501 :
      b=a*2 #声音频率为开关频率的2倍
      b=round(1000/b) #频率换算为延时
      while True:
        i=not i  #非运算
        beep.value(i)  
        time.sleep_ms(b)
        c+=1
        if c>=d :
            break
    if 500<a<500001 :
      b=a*2
      b/=1000 #延时改用微秒
      b=round(1000/b)
      while True:
        i=not i  #非运算
        beep.value(i)  
        time.sleep_us(b)
        c+=1
        if c>=d :
            break
        
            


