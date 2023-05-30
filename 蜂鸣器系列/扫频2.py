#导入Pin模块
from machine import Pin
import time

#定义蜂鸣器控制对象
beep=Pin(25,Pin.OUT)   
    
#程序入口
if __name__=="__main__":
    i=0
    a=1
    while True:
        i=not i  #非运算
        beep.value(i)  
        time.sleep_us(a)  #脉冲频率为2KHz
        a+=1
        if a==1000 :
            a=0