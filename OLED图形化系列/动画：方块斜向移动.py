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
i2c = SoftI2C(sda=Pin(2), scl=Pin(15))
#创建OLED对象，OLED分辨率、I2C接口
oled = SSD1306_I2C(128, 64, i2c)

a=0
#程序入口
if __name__=="__main__":
   while True:
            x=random.randint(1,100)
            y=random.randint(1,40)
            oled.rect(x,y,9,9,1)  #画矩形
            oled.fill_rect(x+3,y+3,3,3,1)
            oled.show()  #执行显示
            oled.hline(0,0,128,0)  #清除移动前显示区
            oled.vline(0,0,64,0)  #清除移动前显示区
            oled.scroll(1,1)  #指定像素X轴移动
            time.sleep_ms(2)
