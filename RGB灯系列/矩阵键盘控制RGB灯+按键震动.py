#导入Pin模块
from machine import Pin
import time
from machine import PWM
from neopixel import NeoPixel

motor = Pin(23, Pin.OUT) #23引脚接振动马达，高电平触发

#矩阵键盘（4x12）
# 创建行的对象
row1 = Pin(12, Pin.OUT)
row2 = Pin(14, Pin.OUT)
row3 = Pin(27, Pin.OUT)
row4 = Pin(26, Pin.OUT)
row_list = [row1, row2, row3, row4]  # 将创建的行对象放到list里面
 
# 创建列的对象
col1 = Pin(15, Pin.IN, Pin.PULL_DOWN)
col2 = Pin(2, Pin.IN, Pin.PULL_DOWN)
col3 = Pin(4, Pin.IN, Pin.PULL_DOWN)
col4 = Pin(16, Pin.IN, Pin.PULL_DOWN)
col5 = Pin(17, Pin.IN, Pin.PULL_DOWN)
col6 = Pin(5, Pin.IN, Pin.PULL_DOWN)
col7 = Pin(18, Pin.IN, Pin.PULL_DOWN)
col8 = Pin(19, Pin.IN, Pin.PULL_DOWN)
col9 = Pin(25, Pin.IN, Pin.PULL_DOWN)
col10 = Pin(33, Pin.IN, Pin.PULL_DOWN)
col11 = Pin(32, Pin.IN, Pin.PULL_DOWN)
col12 = Pin(21, Pin.IN, Pin.PULL_DOWN)
col_list = [col1, col2, col3, col4,col5, col6, col7, col8,col9, col10, col11, col12]  # 将创建的列对象放到list里面
 
pin=22
rgb_num=30
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num) 
r=0
g=0
b=0
#程序入口
while True:
    m=0
    for a in range(rgb_num): 
        rgb_led[a]=(r, g, b)
        rgb_led.write()
    for i, row in enumerate(row_list):  # 遍历序号和对应的值 # 目的：只让某一行通电，其他的行都是0
        for temp in row_list:  # 遍历行对象
            temp.value(0)  # 给每一个行对象赋值
        row.value(1)
        time.sleep_ms(10)  # 键盘通电后，延迟一小会
        for j, col in enumerate(col_list):  # 遍历序号和对应的值
            if col.value() == 1:   # 给每一个列对象赋值
               if i==0 and j==0:
                   r=0
                   m=1
               elif i==1 and j==0:
                   r=17
                   m=1
               elif i==2 and j==0:
                   r=34
                   m=1
               elif i==3 and j==0:
                   r=51
                   m=1
               elif i==0 and j==1:
                   r=68
                   m=1
               elif i==1 and j==1:
                   r=85
                   m=1
               elif i==2 and j==1:
                   r=102
                   m=1
               elif i==3 and j==1:
                   r=119
                   m=1
               elif i==0 and j==2:
                   r=136
                   m=1
               elif i==1 and j==2:
                   r=153
                   m=1
               elif i==2 and j==2:
                   r=170
                   m=1
               elif i==3 and j==2:
                   r=187
                   m=1
               elif i==0 and j==3:
                   r=204
                   m=1
               elif i==1 and j==3:
                   r=221
                   m=1
               elif i==2 and j==3:
                   r=238
                   m=1
               elif i==3 and j==3:
                   r=255
                   m=1
               elif i==0 and j==4:
                   g=0
                   m=1
               elif i==1 and j==4:
                   g=17
                   m=1
               elif i==2 and j==4:
                   g=34
                   m=1
               elif i==3 and j==4:
                   g=51
                   m=1
               elif i==0 and j==5:
                   g=68
                   m=1
               elif i==1 and j==5:
                   g=85
                   m=1
               elif i==2 and j==5:
                   g=102
                   m=1
               elif i==3 and j==5:
                   g=119
                   m=1
               elif i==0 and j==6:
                   g=136
                   m=1
               elif i==1 and j==6:
                   g=153
                   m=1
               elif i==2 and j==6:
                   g=170
                   m=1
               elif i==3 and j==6:
                   g=187
                   m=1
               elif i==0 and j==7:
                   g=204
                   m=1
               elif i==1 and j==7:
                   g=221
                   m=1
               elif i==2 and j==7:
                   g=238
                   m=1
               elif i==3 and j==7:
                   g=255
                   m=1
               elif i==0 and j==8:
                   b=0
                   m=1
               elif i==1 and j==8:
                   b=17
                   m=1
               elif i==2 and j==8:
                   b=34
                   m=1
               elif i==3 and j==8:
                   b=51
                   m=1
               elif i==0 and j==9:
                   b=68
                   m=1
               elif i==1 and j==9:
                   b=85
                   m=1
               elif i==2 and j==9:
                   b=102
                   m=1
               elif i==3 and j==9:
                   b=119
                   m=1
               elif i==0 and j==10:
                   b=136
                   m=1
               elif i==1 and j==10:
                   b=153
                   m=1
               elif i==2 and j==10:
                   b=170
                   m=1
               elif i==3 and j==10:
                   b=187
                   m=1
               elif i==0 and j==11:
                   b=204
                   m=1
               elif i==1 and j==11:
                   b=221
                   m=1
               elif i==2 and j==11:
                   b=238
                   m=1
               elif i==3 and j==11:
                   b=255
                   m=1        
    if m==1 :
        motor.value(1)
    if m==0 :
        motor.value(0)
            