'''
接线：OLED(IIC)
       SCL-->(18)
       SDA-->(23)         
'''

#导入Pin模块
from machine import Pin
import time
from machine import SoftI2C
from ssd1306 import SSD1306_I2C  #I2C的oled选该方法
import random

#创建硬件I2C对象
#i2c=I2C(0,sda=Pin(19), scl=Pin(18), freq=400000)

#创建软件I2C对象
i2c = SoftI2C(sda=Pin(23), scl=Pin(18))
#创建OLED对象，OLED分辨率、I2C接口
oled = SSD1306_I2C(128, 64, i2c)

#程序入口
if __name__=="__main__":
 while True:
    a=60
    b=30
    c=8
    d=4
    e=60
    f=30
    g=8
    h=4
    oled.rect(a,b,c,d,1)  #画矩形
    oled.show()  #执行显示
    while a>50 :
        e-=2
        f-1
        g+=4
        h+=2
        oled.fill(0)  #清空屏幕
        while a>2 :    
            a-=8
            b-=4
            c+=16
            d+=8
            oled.rect(a,b,c,d,1)  #画矩形
            oled.show()  #执行显示
        a=e
        b=f
        c=g
        d=h
