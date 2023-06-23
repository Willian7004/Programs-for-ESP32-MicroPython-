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
import DS1302

#定义RTC控制对象
rtc=RTC()
#定义DS1302控制对象
ds1302=DS1302.DS1302(clk=Pin(13),dio=Pin(12),cs=Pin(15))
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

rtc_time=rtc.datetime()
ds_time=ds1302.DateTime()
if rtc_time[0]==ds_time[0] : #在电脑启动时会自动校准RTC，判断RTC时间没有重置时同步校准DS1302
    ds1302.DateTime([rtc_time[0],rtc_time[1],rtc_time[2],rtc_time[3],rtc_time[4],rtc_time[5],rtc_time[6]])
if rtc_time[0]!=ds_time[0] : #如果程序上电启动，RTC会因断电重置，此时用DS1302校准RTC
    rtc.datetime((ds_time[0],ds_time[1],ds_time[2],ds_time[3],ds_time[4],ds_time[5],ds_time[6],0))    
fonts = [tt32]
display.erase()
while True:
    display.set_pos(20,20)
    for ff in fonts:
        rtc_time=rtc.datetime()
        ds_time=ds1302.DateTime()
        text = str(rtc_time[0])+'-'+str(rtc_time[1])+'-'+str(rtc_time[2])+'  '+str(week[rtc_time[3]])+'\n'+'---< '+str(rtc_time[4])+' : '+str(rtc_time[5])+' : '+str(rtc_time[6])+' >---'+'\n\n'+'Temperature: '+str(BMP.getTemp()) + ' C'+'\n'+'Pressure: '+str(BMP.getPress()) + ' Pa'+'\n'+'Altitude: '+str(BMP.getAltitude()) + ' m'
        display.set_font(ff)
        display.print(text)
    time.sleep(0.9)
    display.erase()
