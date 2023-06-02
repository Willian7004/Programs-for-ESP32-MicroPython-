'''
接线：OLED(IIC)
       SCL-->(18)
       SDA-->(23)
      摇杆
       X轴-->(32)
       Y轴-->(33)
       SW-->(35)
'''

#导入Pin模块
from machine import Pin
import time
from machine import SoftI2C
from ssd1306 import SSD1306_I2C  #I2C的oled选该方法
from machine import ADC
from machine import Timer

#创建硬件I2C对象
#i2c=I2C(0,sda=Pin(19), scl=Pin(18), freq=400000)

#创建软件I2C对象
i2c = SoftI2C(sda=Pin(23), scl=Pin(18))
#创建OLED对象，OLED分辨率、I2C接口
oled = SSD1306_I2C(128, 64, i2c)
#定义ADC控制对象
adc1=ADC(Pin(32))
adc1.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc2=ADC(Pin(33))
adc2.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc3=ADC(Pin(35))
adc3.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V

a=64
b=32

#定时器0中断函数
def time0_irq(time0):
    global a
    global b
    t1=a
    t2=b
    if adc1.read()>2500 :
        a+=1
    if adc1.read()<1500 :
        a-=1
    if adc2.read()>2500 :
        b+=1
    if adc2.read()<1500 :
        b-=1    
    if adc3.read()>5 :  #预览绘制点
        oled.pixel(t1,t2,0)  #去除上一个像素点 
        oled.pixel(a,b,1)  #显示一个像素点
    if adc3.read()<=5 :  #按下摇杆时进行绘制
        oled.pixel(a,b,1)  #显示一个像素点    
    oled.show()  #执行显示
    
#程序入口
if __name__=="__main__":
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=1,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        pass
                