'''
深圳市普中科技有限公司（PRECHIN 普中）
技术支持：www.prechin.net
PRECHIN
 普中

实验名称：BMP280气压传感器实验
接线说明：BMP280气压传感器模块-->ESP32 IO
         SCL-->25
         SDA-->26
         VCC-->3V3
         GND-->GND
         
         OLED(IIC)液晶模块-->ESP32 IO
         GND-->(GND)
         VCC-->(5V)
         SCL-->(18)
         SDA-->(23)
         
实验现象：程序下载成功后，间隔一段时间在Shell控制台输出传感器检测的温度及压力值

注意事项：

'''

from machine import Pin,SoftI2C,Timer
from time import sleep
import bmp280
from ssd1306 import SSD1306_I2C
import onewire
import ds18x20
from machine import RTC
from hcsr04 import HCSR04

#初始化OLED
i2c = SoftI2C(sda=Pin(23), scl=Pin(18))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
#定义DS18B20控制对象
ds18b20=ds18x20.DS18X20(onewire.OneWire(Pin(27)))
roms = ds18b20.scan()  #扫描是否存在DS18B20设备
#初始化BMP280，定义第二个I2C接口i2c2用于连接BMP280
i2c2 = SoftI2C(sda=Pin(26), scl=Pin(25))
BMP = bmp280.BMP280(i2c2)
#定义RTC控制对象
rtc=RTC()
#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=12, echo_pin=14)

#定义星期
week=("Mon","Tue","Wed","Thu","Fri","Sat","Sun")

#中断回调函数
def fun(tim):

    oled.fill(0)  # 清屏,背景黑色
    ds18b20.convert_temp()
    date_time=rtc.datetime()
    distance=hcsr04.distance_cm()
    for rom in roms:
      # 温度显示
      oled.text("%.2f C" %ds18b20.read_temp(rom), 0, 35)
    #时间显示
    oled.text(str(date_time[0])+'-'+str(date_time[1])+'-'+str(date_time[2])+' '+str(week[date_time[3]]), 0, 0)
    oled.text(str(date_time[4])+':'+str(date_time[5])+':'+str(date_time[6]), 0, 10) 
    #距离显示
    oled.text("%.2f cm"%distance, 0, 25)
    # 湿度显示
    oled.text(str(BMP.getPress()) + ' Pa', 0, 45)
    # 海拔显示
    oled.text(str(BMP.getAltitude()) + ' m', 0, 55)

    oled.show()

#开启RTOS定时器
tim = Timer(-1)
tim.init(period=200, mode=Timer.PERIODIC, callback=fun) #周期1s
