#导入Pin模块
from machine import Pin
import time
from machine import PWM
from neopixel import NeoPixel
 
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
mode=8
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
    elif key==5 and mode<9 :
        mode+=1
    elif key==6 and mode>0 :
        mode-=1     

count=0
#程序入口
while True:
    key_get()
    if count==23 :
        count=0
    if mode==0 : #关灯
        for i in range(rgb_num):
            rgb_led[i]=(0, 0, 0)
            rgb_led.write()
    if mode==1 : #三原色
        temp=0
        i=count
        count+=1
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, 0, 0)
            i+=1
            temp+=1
        temp=0    
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(0, brightness, 0)
            i+=1
            temp+=1
        temp=0    
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(0, 0, brightness)
            i+=1
            temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==2 : #三原色重复2次
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
                rgb_led[i]=(brightness, 0, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<4 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, brightness, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<4 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, 0, brightness)
                i+=1
                temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==3 : #三原色重复4次
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
                rgb_led[i]=(brightness, 0, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, brightness, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, 0, brightness)
                i+=1
                temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)        
    if mode==4 : #三间色
        temp=0
        i=count
        count+=1
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, brightness, 0)
            i+=1
            temp+=1
        temp=0    
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(0, brightness, brightness)
            i+=1
            temp+=1
        temp=0    
        while temp<8 :
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, 0, brightness)
            i+=1
            temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==5 : #三间色重复2次
        temp=0
        i=count
        count+=1
        repeat=0
        while repeat<2 :
            temp=0
            repeat+=1
            while temp<4 :
                if i>23 :
                    i-=24
                rgb_led[i]=(brightness, brightness, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<4 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, brightness, brightness)
                i+=1
                temp+=1
            temp=0    
            while temp<4 :
                if i>23 :
                    i-=24
                rgb_led[i]=(brightness, 0, brightness)
                i+=1
                temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==6 : #三间色重复4次
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
                rgb_led[i]=(brightness, brightness, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, brightness, brightness)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(brightness, 0, brightness)
                i+=1
                temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)     
    if mode==7 : #三原色+三间色
        temp=0
        i=count
        count+=1
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, 0, 0)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, brightness, 0)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(0, brightness, 0)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(0, brightness, brightness)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(0, 0, brightness)
            i+=1
            temp+=1
        temp=0    
        while temp<4 :
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, 0, brightness)
            i+=1
            temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==8 : #三原色+三间色重复2次
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
                rgb_led[i]=(brightness, 0, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(brightness, brightness, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, brightness, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, brightness, brightness)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(0, 0, brightness)
                i+=1
                temp+=1
            temp=0    
            while temp<2 :
                if i>23 :
                    i-=24
                rgb_led[i]=(brightness, 0, brightness)
                i+=1
                temp+=1
        rgb_led.write()    
        time.sleep_ms(delay)           
    if mode==9 : #三原色+三间色重复4次
        temp=0
        i=count
        count+=1
        repeat=0
        while repeat<4 :
            repeat+=1
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, 0, 0)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, brightness, 0)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(0, brightness, 0)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(0, brightness, brightness)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(0, 0, brightness)
            i+=1
            temp+=1
            if i>23 :
                i-=24
            rgb_led[i]=(brightness, 0, brightness)
            i+=1
            temp+=1
        rgb_led.write()    
        time.sleep_ms(delay) 
