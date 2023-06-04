#导入Pin模块
from machine import Pin
import time
from machine import PWM  
    
#程序入口
while True:
    i=0
    b=1
    a=int(input("输入频率（1到500000的整数）"))
    beep=PWM(Pin(22),freq=a,duty=512)
    time.sleep_ms(500)
    beep=PWM(Pin(22),freq=a,duty=0)
        