#导入Pin模块
from machine import Pin
import time
from machine import PWM
from neopixel import NeoPixel
 
# 五向导航按键，COM引脚接GND
key1=Pin(12,Pin.IN,Pin.PULL_UP)
key2=Pin(14,Pin.IN,Pin.PULL_UP)
key3=Pin(26,Pin.IN,Pin.PULL_UP)
key4=Pin(25,Pin.IN,Pin.PULL_UP)
key5=Pin(33,Pin.IN,Pin.PULL_UP)
key6=Pin(32,Pin.IN,Pin.PULL_UP)
 
pin=13
rgb_num=64
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

key_en=1
#按键扫描函数
def key_scan():
    global key_en
    if key_en==1 and (key1.value()==0 or key2.value()==0 or key3.value()==0 or key4.value()==0 or
                      key5.value()==0 or key6.value()==0  ):
        time.sleep_ms(10)
        key_en=0
        if key1.value()==0:
            return 1
        elif key2.value()==0:
            return 2
        elif key3.value()==0:
            return 3
        elif key4.value()==0:
            return 4
        elif key5.value()==0:
            return 5
        elif key6.value()==0:
            return 6
    elif (key1.value()==1 and key2.value()==1 and key3.value()==1 and key4.value()==1 and
          key5.value()==1 and key6.value()==1  ) :
        key_en=1
    return 0

brightness=2
delay=40
mode=1
sleep=0
def key_get(): #获取键值并改变变量的值
    global brightness
    global delay
    global mode
    key=key_scan()
    if key==1 and brightness<7 :
        brightness+=1
    elif key==2 and brightness>1 :
        brightness-=1
    elif key==3 and delay<90 :
        delay+=10
    elif key==4 and delay>10 :
        delay-=10
    elif key==5 and mode<4 :
        mode+=1
    elif key==6 and mode>0 :
        mode-=1     

count=0
#程序入口
while True:
    key_get()
    full_brightness=brightness*8
    if count>=63 :
        count=0
    if mode==0 : #关灯
        for i in range(rgb_num):
            rgb_led[i]=(0, 0, 0)
            rgb_led.write()
    if mode==1 : #流水灯
        temp=0
        i=count
        count+=1
        repeat=0
        while repeat<2 : #重复
            repeat+=1
            temp=0
            while temp<8 :
                if i>63 :
                    i-=63
                rgb_led[i]=(0, full_brightness, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<8 :
                if i>63 :
                    i-=63
                rgb_led[i]=(full_brightness, 0, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<8 :
                if i>63 :
                    i-=63
                rgb_led[i]=(0, full_brightness, 0)
                i+=1
                temp+=1
            temp=0    
            while temp<8 :
                if i>63 :
                    i-=63
                rgb_led[i]=(0, 0, full_brightness)
                i+=1
                temp+=1    
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==2 : #渐变流水灯
        temp=0
        i=count
        count+=1
        repeat=0
        while repeat<2 : #重复
            repeat+=1
            temp=0
            g=8*brightness
            r=0
            while temp<8 :
                if i>63 :
                    i-=63
                rgb_led[i]=(r, g, 0)
                g-=brightness
                r+=brightness
                i+=1
                temp+=1
            temp=0
            r=8*brightness
            g=0
            while temp<8 :
                if i>63 :
                    i-=63
                rgb_led[i]=(r, g, 0)
                r-=brightness
                g+=brightness
                i+=1
                temp+=1
            temp=0
            g=8*brightness
            b=0
            while temp<8 :
                if i>63 :
                    i-=63
                rgb_led[i]=(0, g, b)
                g-=brightness
                b+=brightness
                i+=1
                temp+=1
            temp=0
            b=8*brightness
            g=0
            while temp<8 :
                if i>63 :
                    i-=63
                rgb_led[i]=(0, g, b)
                b-=brightness
                g+=brightness
                i+=1
                temp+=1    
        rgb_led.write()    
        time.sleep_ms(delay)
    if mode==3 : #滚动显示
        sleep+=1
        if sleep==5:
            sleep=0
            if count%8!=0 : #确保从一列的顶端开始显示
                count=0   
            temp=0
            i=count
            count+=8
            repeat=0
            while repeat<4 : #重复
                repeat+=1
                temp=0
                while temp<4 :
                    if i>63 :
                        i-=63   
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                    if i>63 :
                        i-=63
                    rgb_led[i]=(full_brightness, 0, 0)
                    i+=1
                    temp+=1
                temp=0    
                while temp<4 :
                    if i>63 :
                        i-=63
                    rgb_led[i]=(0, 0, full_brightness)
                    i+=1
                    if i>63 :
                        i-=63
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                    temp+=1   
            rgb_led.write()    
        time.sleep_ms(delay)
    if mode==4 : #同心矩形
        sleep+=1
        if sleep==5:
            sleep=0
            count+=1
            if count%4==0 :
                i=0
                while i<64:
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                i=9    
                while i<55:
                    rgb_led[i]=(full_brightness, 0, 0)
                    i+=1
                    if i%8==7:
                        i+=2
                i=18        
                while i<46:
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                    if i%8==6:
                        i+=4
                i=27        
                while i<37:
                    rgb_led[i]=(0, 0, full_brightness)
                    i+=1
                    if i%8==5:
                        i+=6
            if count%4==1 :
                i=0
                while i<64:
                    rgb_led[i]=(full_brightness, 0, 0)
                    i+=1
                i=9    
                while i<55:
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                    if i%8==7:
                        i+=2
                i=18        
                while i<46:
                    rgb_led[i]=(0, 0, full_brightness)
                    i+=1
                    if i%8==6:
                        i+=4
                i=27        
                while i<37:
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                    if i%8==5:
                        i+=6
            if count%4==2 :
                i=0
                while i<64:
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                i=9    
                while i<55:
                    rgb_led[i]=(0, 0, full_brightness)
                    i+=1
                    if i%8==7:
                        i+=2
                i=18        
                while i<46:
                    rgb_led[i]=(full_brightness, 0, 0)
                    i+=1
                    if i%8==6:
                        i+=4
                i=27        
                while i<37:
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                    if i%8==5:
                        i+=6
            if count%4==3 :
                i=0
                while i<64:
                    rgb_led[i]=(0, 0, full_brightness)
                    i+=1
                i=9    
                while i<55:
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                    if i%8==7:
                        i+=2
                i=18        
                while i<46:
                    rgb_led[i]=(full_brightness, 0, 0)
                    i+=1
                    if i%8==6:
                        i+=4
                i=27        
                while i<37:
                    rgb_led[i]=(0, full_brightness, 0)
                    i+=1
                    if i%8==5:
                        i+=6               
            rgb_led.write()    
        time.sleep_ms(delay)
