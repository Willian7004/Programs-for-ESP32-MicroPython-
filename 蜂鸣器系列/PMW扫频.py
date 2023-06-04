#导入Pin模块
from machine import Pin
import time
from machine import PWM  

a=19
#程序入口
while a<100:
    a+=1
    beep=PWM(Pin(22),freq=a,duty=512)
    time.sleep_ms(50)
    beep=PWM(Pin(22),freq=a,duty=0)
    print(a)
while a<1000:
    a+=10
    beep=PWM(Pin(22),freq=a,duty=512)
    time.sleep_ms(50)
    beep=PWM(Pin(22),freq=a,duty=0)
    print(a)
while a<10000:
    a+=100
    beep=PWM(Pin(22),freq=a,duty=512)
    time.sleep_ms(50)
    beep=PWM(Pin(22),freq=a,duty=0)
    print(a)    
        