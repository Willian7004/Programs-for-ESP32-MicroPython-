'''
接线: ADC-->(34)
      IN1-->(15)   
'''

#导入Pin模块
from machine import Pin
from machine import ADC
from machine import PWM
from machine import Timer
#定义LED1控制对象
led1=PWM(Pin(15),freq=10000,duty=0)

#定义ADC控制对象
adc=ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V


#定时器0中断函数
def time0_irq(time0):
    adc_vol=1023*adc.read()//4095
    led1.duty(adc_vol)
    print(adc_vol)
    
#程序入口
if __name__=="__main__":
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=50,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        pass
