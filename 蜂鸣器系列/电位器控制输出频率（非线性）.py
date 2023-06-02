'''
接线：CLK-->(16)
      DIO-->(17)
      ADC-->(34)
      蜂鸣器-->(22)
'''

#导入Pin模块
from machine import Pin
import time
import tm1637
from machine import ADC
from machine import Timer

#定义蜂鸣器控制对象
beep=Pin(22,Pin.OUT)
#定义ADC控制对象
adc=ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
#定义数码管控制对象
smg=tm1637.TM1637(clk=Pin(16),dio=Pin(17))

#定时器0中断函数
def time0_irq(time0):
    adc_vol=200*adc.read()/4095+1
    i=0
    b=1
    a=round(10000/adc_vol)
    d=a/10
    c=0
    smg.show("%04d"%a)
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
    
#程序入口
if __name__=="__main__":
   time0=Timer(0)  #创建time0定时器对象
   time0.init(period=50,mode=Timer.PERIODIC,callback=time0_irq)
   while True:
     pass
    