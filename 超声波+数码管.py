'''
接线：CLK-->(16)
      DIO-->(17)
      (Trig)-->(12)
      (Echo)-->(14)
'''

#导入Pin模块
from machine import Pin
import time
import tm1637
from hcsr04 import HCSR04

#定义数码管控制对象
smg=tm1637.TM1637(clk=Pin(16),dio=Pin(17))
#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=12, echo_pin=14)

#程序入口
if __name__=="__main__":
    #smg.numbers(1,24)  #显示小数01.24
    #smg.hex(123)  #将十进制数转换十六进制显示
    #smg.brightness(0)  #亮度调节
    #smg.temperature(25)  #显示带温度符号°C，整数温度值
    #smg.show("1314")  #字符串显示，显示整数
    #smg.scroll("1314-520",500)  #字符串滚动显示，速度调节
    #time.sleep(5)
    a=0
    while True:
        distance=hcsr04.distance_mm()
        a=distance//1
        smg.show("%04d"%a)
        time.sleep(0.1)
