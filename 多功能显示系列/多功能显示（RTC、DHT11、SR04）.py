'''
接线:SCL-->25
     SDA-->26
     DS-->27
     (Trig)-->(12)
     (Echo)-->(14)
'''

from machine import Pin,I2C
import time
from i2c_lcd import I2cLcd
import dht
from machine import RTC
from hcsr04 import HCSR04

#定义DHT11控制对象
dht11=dht.DHT11(Pin(27))
#定义RTC控制对象
rtc=RTC()
# LCD 1602 I2C 地址
DEFAULT_I2C_ADDR = 0x27
#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=12, echo_pin=14)

# 初始化GPIO口
# def setup():
# global lcd
i2c = I2C(1,sda=Pin(26),scl=Pin(25),freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)  # 初始化(设备地址, 背光设置)

#定义星期
week=("Mon","Tue","Wed","Thu","Fri","Sat","Sun")

# 循环函数
def loop():    
    while True:
        dht11.measure()  #调用DHT类库中测量数据的函数
        temp = dht11.temperature()
        humi = dht11.humidity()
        date_time=rtc.datetime()
        distance=hcsr04.distance_cm()
        lcd.putstr("%d%02d%02d t%d h%d"%(date_time[0],date_time[1],date_time[2],temp,humi))       
        lcd.putstr("%02d:%02d:%02d %s %03d"%(date_time[4],date_time[5],date_time[6],week[date_time[3]],distance))
        time.sleep_ms(1000)  #如果延时时间过短，DHT11温湿度传感器不工作

# 程序入口
if __name__ == '__main__':    
#     setup()           # 初始化GPIO口
    loop()            # 循环函数