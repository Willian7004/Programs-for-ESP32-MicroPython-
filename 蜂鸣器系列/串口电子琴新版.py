#接线：蜂鸣器-->(22)

#导入Pin模块
from machine import Pin
import time

#定义蜂鸣器控制对象
beep=Pin(22,Pin.OUT)   
    
#程序入口
while True:
    i=0
    b=1
    e=int(input("输入音调（1-40）"))
    a=50
    if e==1 :
        a=50
    elif e==2 :
        a=100
    elif e==3 :
        a=150
    elif e==4 :
        a=200
    elif e==5 :
        a=350
    elif e==6 :
        a=550
    elif e==7 :
        a=600
    elif e==8 :
        a=650
    elif e==9 :
        a=700
    elif e==10 :
        a=750
    elif e==11 :
        a=800
    elif e==12 :
        a=850
    elif e==13 :
        a=900
    elif e==14 :
        a=950
    elif e==15 :
        a=1000
    elif e==16 :
        a=1050
    elif e==17 :
        a=1100
    elif e==18 :
        a=1150
    elif e==19 :
        a=1200
    elif e==20 :
        a=1250
    elif e==21 :
        a=1300
    elif e==22 :
        a=1350
    elif e==23 :
        a=1400
    elif e==24 :
        a=1450
    elif e==25 :
        a=1500
    elif e==26 :
        a=1650
    elif e==27 :
        a=1700
    elif e==28 :
        a=1750
    elif e==29 :
        a=1800
    elif e==30 :
        a=1850
    elif e==31 :
        a=1900
    elif e==32 :
        a=2000
    elif e==33 :
        a=2100
    elif e==34 :
        a=2200
    elif e==35 :
        a=2300
    elif e==36 :
        a=2400
    elif e==37 :
        a=2500
    elif e==38 :
        a=2600
    elif e==39 :
        a=2700
    elif e==40 :
        a=2800    
    else :
        a=100
    d=a/2
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
        
            


