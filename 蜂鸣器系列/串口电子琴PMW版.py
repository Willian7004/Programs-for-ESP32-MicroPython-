#导入Pin模块
from machine import Pin
import time
from machine import PWM   
    
#程序入口
while True:
    e=int(input("输入音调，第一位为升降调，其中5为中音；第二位（1到7）为音调"))
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
    if e//10<9 :
      t=e//10
      e=9-t
      t=2**e
      a=round(a/t)
    else :
        a=262
    beep=PWM(Pin(22),freq=a,duty=512)
    time.sleep_ms(250)
    beep=PWM(Pin(22),freq=a,duty=0)
            