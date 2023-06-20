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


#程序入口
if __name__=="__main__":
    x=20 #记录坐标
    y=1
    fx=20 #记录上一个坐标
    fy=1
    flag=0    
    oled.rect(20,1,9,9,1)  #画矩形
    oled.fill_rect(23,4,3,3,1)
    oled.show()  #执行显示    
    while True:
        if flag==0:
            oled.scroll(1,1) #向右下方移动 
            oled.show()  #执行显示 
            fx=x
            fy=y
            x+=1
            y+=1
        if flag==1:
            oled.scroll(1,-1) #向右上方移动 
            oled.show()  #执行显示
            fx=x
            fy=y
            x+=1
            y-=1
        if flag==2:
            oled.scroll(-1,-1) #向左上方移动 
            oled.show()  #执行显示
            fx=x
            fy=y
            x-=1
            y-=1       
        if flag==3:
            oled.scroll(-1,1) #向左下方移动 
            oled.show()  #执行显示
            fx=x
            fy=y
            x-=1
            y+=1
        if y==53 and x-fx==1 : 
            flag=1
        if y==53 and x-fx==-1 :
            flag=2
        if x==117 and y-fy==1 :
            flag=2
        if x==117 and y-fy==-1 :
            flag=3
        if y==1 and x-fx==1 :
            flag=0
        if y==1 and x-fx==-1 :
            flag=3
        if x==1 and y-fy==1 :
            flag=0
        if x==1 and y-fy==-1 :
            flag=1
        if x==1 and y==1:
            flag=0
        if x==117 and y==53:
            flag=2
        if x==117 and y==1:
            flag=3
        if x==1 and y==53:
            flag=1    
            
            
