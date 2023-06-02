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

a=0
b=0
e=0

#程序入口
if __name__=="__main__":
   while True:
        a=random.randint(0,127)
        b=random.randint(0,63)
        e=random.randint(0,1)
        oled.pixel(a,b,1)  #显示一个像素点
        oled.show()  #执行显示
        