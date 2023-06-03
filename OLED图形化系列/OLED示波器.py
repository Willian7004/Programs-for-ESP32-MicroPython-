'''
接线：OLED(IIC)
       SCL-->(18)
       SDA-->(23)
      待测信号-->(32)
屏幕底部从左到右依次显示当前值、最大值、最小值和平均值      
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
adc=ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V

a=-1
b=0
d=0
e=3.3
total=0
count=0
oled.hline(0,54,128,1)#分割线
oled.show()  #执行显示

#定时器0中断函数
def time0_irq(time0):
    global a
    global b
    global d
    global e
    global total
    global count
    adc_vol=53*adc.read()//4095
    b=53-adc_vol
    c=3.3*adc.read()/4095
    if c>d :
        d=c
    if c<e :
        e=c
    a+=1
    count+=1
    total+=c
    avg=total/count
    if a==127 :
        a=126
        oled.vline(0,0,53,0)  #清除移动前显示区
        oled.scroll(-1,0)  #指定像素X轴移动
    oled.pixel(a,b,1)
    oled.fill_rect(0,55,128,9,0)  #清空数据
    oled.text("%.2f"%c, 0, 56) #当前值
    oled.vline(34,55,9,1) #分割线
    oled.text("%.1f"%d, 36, 56) #最大值
    oled.vline(63,55,9,1) #分割线
    oled.text("%.1f"%e, 65, 56) #最小值
    oled.vline(92,55,9,1) #分割线
    oled.text("%.2f"%avg, 94, 56) #平均值
    oled.show()  #执行显示
    
    
#程序入口
if __name__=="__main__":
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=1,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        pass
                