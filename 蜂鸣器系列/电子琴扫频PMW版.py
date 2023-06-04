#导入Pin模块
from machine import Pin
import time
from machine import PWM   

e=10
b=0
#程序入口
while True:
    e+=1
    if e%10==8 :
      e+=3
    if e>=101 :
      e=11
      time.sleep_ms(1000)
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
    if e//10<9 :
      t=e//10
      b=9-t
      t=2**b
    a=round(a/t)
    if a<1 :
        a=1
    print(e)    
    beep=PWM(Pin(22),freq=a,duty=512)
    time.sleep_ms(100)
    beep=PWM(Pin(22),freq=a,duty=0)
            