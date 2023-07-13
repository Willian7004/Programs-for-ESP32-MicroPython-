#导入Pin模块
from machine import Pin
import time
from machine import PWM
from neopixel import NeoPixel
import random
 
# 五向导航按键，COM引脚接3.3V
key1 = Pin(21, Pin.IN, Pin.PULL_DOWN)
key2 = Pin(19, Pin.IN, Pin.PULL_DOWN)
key3 = Pin(18, Pin.IN, Pin.PULL_DOWN)
key4 = Pin(5, Pin.IN, Pin.PULL_DOWN)
key5 = Pin(17, Pin.IN, Pin.PULL_DOWN)
key6 = Pin(16, Pin.IN, Pin.PULL_DOWN)
 
pin=13
rgb_num=24
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

key_en=1
#按键扫描函数
def key_scan():
    global key_en
    if key_en==1 and (key1.value()==1 or key2.value()==1 or key3.value()==1 or key4.value()==1 or
                      key5.value()==1 or key6.value()==1  ):
        time.sleep_ms(10)
        key_en=0
        if key1.value()==1:
            return 1
        elif key2.value()==1:
            return 2
        elif key3.value()==1:
            return 3
        elif key4.value()==1:
            return 4
        elif key5.value()==1:
            return 5
        elif key6.value()==1:
            return 6
    elif (key1.value()==0 and key2.value()==0 and key3.value()==0 and key4.value()==0 and
          key5.value()==0 and key6.value()==0  ) :
        key_en=1
    return 0

brightness=51
delay=40
mode=4
def key_get(): #获取键值并改变变量的值
    global brightness
    global delay
    global mode
    key=key_scan()
    if key==1 and brightness<255 :
        brightness+=17
    elif key==2 and brightness>17 :
        brightness-=17
    elif key==3 and delay<90 :
        delay+=10
    elif key==4 and delay>10 :
        delay-=10
    elif key==5 and mode<6 :
        mode+=1
    elif key==6 and mode>0 :
        mode-=1     

r1=0
r2=0
r3=0
r4=0
r5=0
r6=0
g1=0
g2=0
g3=0
g4=0
g5=0
g6=0
b1=0
b2=0
b3=0
b4=0
b5=0
b6=0
def rand():
    global brightness
    global r1
    global r2
    global r3
    global r4
    global r5
    global r6
    global g1
    global g2
    global g3
    global g4
    global g5
    global g6
    global b1
    global b2
    global b3
    global b4
    global b5
    global b6
    r1=random.randint(0,brightness)
    r2=random.randint(0,brightness)
    r3=random.randint(0,brightness)
    r4=random.randint(0,brightness)
    r5=random.randint(0,brightness)
    r6=random.randint(0,brightness)
    g1=random.randint(0,brightness)
    g2=random.randint(0,brightness)
    g3=random.randint(0,brightness)
    g4=random.randint(0,brightness)
    g5=random.randint(0,brightness)
    g6=random.randint(0,brightness)
    b1=random.randint(0,brightness)
    b2=random.randint(0,brightness)
    b3=random.randint(0,brightness)
    b4=random.randint(0,brightness)
    b5=random.randint(0,brightness)
    b6=random.randint(0,brightness)
    
count=0
rand()
#程序入口
while True:
    key_get()
    if count==23 :
        count=0
        rand()
    if mode==0 : #关灯
        for i in range(rgb_num):
            rgb_led[i]=(0, 0, 0)
            rgb_led.write()
    if mode==1 : #三色
        temp=0
        i=count
        count+=1
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(r1,g1,b1)
            i+=1
            temp+=1
        temp=0    
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(r2,g2,b2)
            i+=1
            temp+=1
        temp=0    
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(r3,g3,b3)
            i+=1
            temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==2 : #三色重复2次
        temp=0
        i=count
        count+=1
        repeat=0
        while repeat<4 :
            temp=0
            repeat+=1
            while temp<4 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r1,g1,b1)
                i+=1
                temp+=1
            temp=0    
            while temp<4 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r2,g2,b2)
                i+=1
                temp+=1
            temp=0    
            while temp<4 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r3,g3,b3)
                i+=1
                temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==3 : #三色重复4次
        temp=0
        i=count
        count+=1
        repeat=0
        while repeat<4 :
            temp=0
            repeat+=1
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r1,g1,b1)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r2,g2,b2)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r3,g3,b3)
                i+=1
                temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)            
    if mode==4 : #三原色+三间色
        temp=0
        i=count
        count+=1
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(r1,g1,b1)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(r4,g4,b4)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(r2,g2,b2)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(r5,g5,b5)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(r3,g3,b3)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(r6,g6,b6)
            i+=1
            temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==5 : #三原色+三间色重复2次
        temp=0
        i=count
        count+=1
        repeat=0
        while repeat<2 :
            temp=0
            repeat+=1
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r1,g1,b1)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r4,g4,b4)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r2,g2,b2)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r5,g5,b5)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r3,g3,b3)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(r6,g6,b6)
                i+=1
                temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)           
    if mode==6 : #三原色+三间色重复4次
        temp=0
        i=count
        count+=1
        repeat=0
        while repeat<4 :
            repeat+=1
            if i>23 :
                i-=24
            rgb_led[i]=(r1,g1,b1)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(r4,g4,b4)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(r2,g2,b2)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(r5,g5,b5)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(r3,g3,b3)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(r6,g6,b6)
            i+=1
            temp+=1
        rgb_led.write()    
        time.sleep_ms(delay) 
