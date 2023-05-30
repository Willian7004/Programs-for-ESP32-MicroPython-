#导入Pin模块
from machine import Pin
import time

#定义蜂鸣器控制对象
beep=Pin(25,Pin.OUT)   
    
#程序入口
if __name__=="__main__":
    i=0
    b=1
    a=int(input("输入频率（1到500000的整数）"))
    if 0<a<501 :
      b=a*2 #声音频率为开关频率的2倍
      b=round(1000/b) #频率换算为延时
      while True:
        i=not i  #非运算
        beep.value(i)  
        time.sleep_ms(b)
    if 500<a<500001 :
      b=a*2
      b/=1000 #延时改用微秒
      b=round(1000/b)
      while True:
        i=not i  #非运算
        beep.value(i)  
        time.sleep_us(b)
        
            


