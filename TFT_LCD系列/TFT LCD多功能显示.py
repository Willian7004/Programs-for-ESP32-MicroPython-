from ili934xnew import ILI9341, color565
from machine import Pin, SPI
import m5stack
import tt14
import glcdfont
import tt14
import tt24
import tt32
from machine import RTC
import time
from machine import SoftI2C
import bmp280
from machine import Timer
from machine import PWM

#定义RTC控制对象
rtc=RTC()
#定义星期
week=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
#初始化BMP280，定义第二个I2C接口i2c2用于连接BMP280
i2c2 = SoftI2C(sda=Pin(22), scl=Pin(21))
BMP = bmp280.BMP280(i2c2)

power = Pin(m5stack.TFT_LED_PIN, Pin.OUT)
power.value(1)

spi = SPI(
    2,
    baudrate=80000000,
    miso=Pin(m5stack.TFT_MISO_PIN),
    mosi=Pin(m5stack.TFT_MOSI_PIN),
    sck=Pin(m5stack.TFT_CLK_PIN))

display = ILI9341(
    spi,
    cs=Pin(m5stack.TFT_CS_PIN),
    dc=Pin(m5stack.TFT_DC_PIN),
    rst=Pin(m5stack.TFT_RST_PIN),
    w=320,
    h=240,
    r=3)

led=PWM(Pin(2),freq=4000,duty=20)
duty=0
flag=0
#定时器0中断函数
def time0_irq(time0):
    global duty
    global flag
    if duty==20 :
        flag=0
    if duty==1020 :
        flag=1    
    if flag==0 :
        duty+=1
        led.duty(duty)
    if flag==1 :
        duty-=1
        led.duty(duty)
        
time0=Timer(0)  #创建time0定时器对象
time0.init(period=1,mode=Timer.PERIODIC,callback=time0_irq)

fonts = [tt32]
display.erase()
while True:
    display.set_pos(20,20)
    for ff in fonts:
        date_time=rtc.datetime()
        text = str(date_time[0])+'-'+str(date_time[1])+'-'+str(date_time[2])+'  '+str(week[date_time[3]])+'\n'+'---< '+str(date_time[4])+' : '+str(date_time[5])+' : '+str(date_time[6])+' >---'+'\n\n'+'Temperature: '+str(BMP.getTemp()) + ' C'+'\n'+'Pressure: '+str(BMP.getPress()) + ' Pa'+'\n'+'Altitude: '+str(BMP.getAltitude()) + ' m'
        display.set_font(ff)
        display.print(text)
    time.sleep(0.9)
    display.erase()
