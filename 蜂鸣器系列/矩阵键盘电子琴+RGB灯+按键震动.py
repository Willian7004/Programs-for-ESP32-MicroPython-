#导入Pin模块
from machine import Pin
import time
from machine import PWM
from neopixel import NeoPixel
import random

motor = Pin(23, Pin.OUT)
#扬声器接13脚和GND，矩阵键盘接线如下
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
d=0
#程序入口
while True:
    e=10
    d+=1
    if d==30:
        d=0
    a=random.randint(0,255)
    b=random.randint(0,255)
    c=random.randint(0,255)
    rgb_led[d]=(a, b, c)
    rgb_led.write()
    for i, row in enumerate(row_list):  # 遍历序号和对应的值 # 目的：只让某一行通电，其他的行都是0
        for temp in row_list:  # 遍历行对象
            temp.value(0)  # 给每一个行对象赋值
        row.value(1)
        time.sleep_ms(10)  # 键盘通电后，延迟一小会
        for j, col in enumerate(col_list):  # 遍历序号和对应的值
            if col.value() == 1:   # 给每一个列对象赋值
               if i==0 and j==0:
                   e=22
               elif i==1 and j==0:
                   e=23
               elif i==2 and j==0:
                   e=24
               elif i==3 and j==0:
                   e=25
               elif i==0 and j==1:
                   e=26
               elif i==1 and j==1:
                   e=27
               elif i==2 and j==1:
                   e=31
               elif i==3 and j==1:
                   e=32
               elif i==0 and j==2:
                   e=33
               elif i==1 and j==2:
                   e=34
               elif i==2 and j==2:
                   e=35
               elif i==3 and j==2:
                   e=36
               elif i==0 and j==3:
                   e=37
               elif i==1 and j==3:
                   e=41
               elif i==2 and j==3:
                   e=42
               elif i==3 and j==3:
                   e=43
               elif i==0 and j==4:
                   e=44
               elif i==1 and j==4:
                   e=45
               elif i==2 and j==4:
                   e=46
               elif i==3 and j==4:
                   e=47
               elif i==0 and j==5:
                   e=51
               elif i==1 and j==5:
                   e=52
               elif i==2 and j==5:
                   e=53
               elif i==3 and j==5:
                   e=54
               elif i==0 and j==6:
                   e=55
               elif i==1 and j==6:
                   e=56
               elif i==2 and j==6:
                   e=57
               elif i==3 and j==6:
                   e=61
               elif i==0 and j==7:
                   e=62
               elif i==1 and j==7:
                   e=63
               elif i==2 and j==7:
                   e=64
               elif i==3 and j==7:
                   e=65
               elif i==0 and j==8:
                   e=66
               elif i==1 and j==8:
                   e=67
               elif i==2 and j==8:
                   e=71
               elif i==3 and j==8:
                   e=72
               elif i==0 and j==9:
                   e=73
               elif i==1 and j==9:
                   e=74
               elif i==2 and j==9:
                   e=75
               elif i==3 and j==9:
                   e=76
               elif i==0 and j==10:
                   e=77
               elif i==1 and j==10:
                   e=81
               elif i==2 and j==10:
                   e=82
               elif i==3 and j==10:
                   e=83
               elif i==0 and j==11:
                   e=84
               elif i==1 and j==11:
                   e=85
               elif i==2 and j==11:
                   e=86
               elif i==3 and j==11:
                   e=87        
    if e>10 :
        motor.value(1)
    if e==10 :
        motor.value(0)     
    a=0
    t=0
    if e%10==1 :
      a=4186
    if e%10==2 :
      a=4698
    if e%10==3 :
      a=5274
    if e%10==4 :
      a=5587
    if e%10==5 :
      a=6272
    if e%10==6 :
      a=7040
    if e%10==7 :
      a=7901
    if e//10<9 :
      t=e//10
      f=9-t
      t=2**f
      a=round(a/t)
    if e<11 :
        a=1
    beep=PWM(Pin(13),freq=a,duty=512)
            