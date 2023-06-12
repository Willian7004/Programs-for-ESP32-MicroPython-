#导入Pin模块
from machine import Pin
import time
from machine import PWM   
#扬声器接13脚和GND，矩阵键盘接线如下
# 创建行的对象
row1 = Pin(15, Pin.OUT)
row2 = Pin(2, Pin.OUT)
row3 = Pin(4, Pin.OUT)
row4 = Pin(16, Pin.OUT)
row5 = Pin(12, Pin.OUT)
row6 = Pin(14, Pin.OUT)
row7 = Pin(27, Pin.OUT)
row8 = Pin(26, Pin.OUT)
row_list = [row1, row2, row3, row4,row5, row6, row7, row8]  # 将创建的行对象放到list里面
 
# 创建列的对象
col1 = Pin(19, Pin.IN, Pin.PULL_DOWN)
col2 = Pin(18, Pin.IN, Pin.PULL_DOWN)
col3 = Pin(5, Pin.IN, Pin.PULL_DOWN)
col4 = Pin(17, Pin.IN, Pin.PULL_DOWN)
col5 = Pin(21, Pin.IN, Pin.PULL_DOWN)
col6 = Pin(32, Pin.IN, Pin.PULL_DOWN)
col7 = Pin(33, Pin.IN, Pin.PULL_DOWN)
col8 = Pin(25, Pin.IN, Pin.PULL_DOWN)
col_list = [col1, col2, col3, col4,col5, col6, col7, col8]  # 将创建的列对象放到list里面
 


#程序入口
while True:
    e=10
    for i, row in enumerate(row_list):  # 遍历序号和对应的值 # 目的：只让某一行通电，其他的行都是0
        for temp in row_list:  # 遍历行对象
            temp.value(0)  # 给每一个行对象赋值
        row.value(1)
        time.sleep_ms(10)  # 键盘通电后，延迟一小会
        for j, col in enumerate(col_list):  # 遍历序号和对应的值
            if col.value() == 1:   # 给每一个列对象赋值
               print(i,j)
               if i==0 and j==0:
                   e=26
               elif i==0 and j==1:
                   e=27
               elif i==0 and j==2:
                   e=31
               elif i==0 and j==3:
                   e=32
               elif i==1 and j==0:
                   e=33
               elif i==1 and j==1:
                   e=34
               elif i==1 and j==2:
                   e=35
               elif i==1 and j==3:
                   e=36
               elif i==2 and j==0:
                   e=37
               elif i==2 and j==1:
                   e=41
               elif i==2 and j==2:
                   e=42
               elif i==2 and j==3:
                   e=43
               elif i==3 and j==0:
                   e=44
               elif i==3 and j==1:
                   e=45
               elif i==3 and j==2:
                   e=46
               elif i==3 and j==3:
                   e=47     
               elif i==4 and j==4:
                   e=51
               elif i==4 and j==5:
                   e=52
               elif i==4 and j==6:
                   e=53
               elif i==4 and j==7:
                   e=54
               elif i==5 and j==4:
                   e=55
               elif i==5 and j==5:
                   e=56
               elif i==5 and j==6:
                   e=57
               elif i==5 and j==7:
                   e=61
               elif i==6 and j==4:
                   e=62
               elif i==6 and j==5:
                   e=63
               elif i==6 and j==6:
                   e=64
               elif i==6 and j==7:
                   e=65
               elif i==7 and j==4:
                   e=66
               elif i==7 and j==5:
                   e=67
               elif i==7 and j==6:
                   e=71
               elif i==7 and j==7:
                   e=72            
               print(e)
    a=0
    t=0
    if e%10==1 :
      a=4186
    elif e%10==2 :
      a=4698
    elif e%10==3 :
      a=5274
    elif e%10==4 :
      a=5587
    elif e%10==5 :
      a=6272
    elif e%10==6 :
      a=7040
    elif e%10==7 :
      a=7901
    if e//10<9 :
      t=e//10
      f=9-t
      t=2**f
      a=round(a/t)
    if e<11 :
        a=1
    beep=PWM(Pin(13),freq=a,duty=512)
    time.sleep_ms(10)
            