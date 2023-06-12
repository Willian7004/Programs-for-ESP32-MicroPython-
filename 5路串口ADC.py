'''
接线: ADC-->(34)  
'''

#导入Pin模块
from machine import Pin
from machine import ADC
from machine import Timer

#定义ADC控制对象
adc1=ADC(Pin(32))
adc1.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc2=ADC(Pin(33))
adc2.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc3=ADC(Pin(34))
adc3.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc4=ADC(Pin(35))
adc4.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc5=ADC(Pin(39))
adc5.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V

#定时器0中断函数
def time0_irq(time0):
    print(adc1.read(),adc2.read(),adc3.read(),adc4.read(),adc5.read())
    
#程序入口
if __name__=="__main__":
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=10,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        pass
