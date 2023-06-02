'''
深圳市普中科技有限公司（PRECHIN 普中）
技术支持：www.prechin.net
PRECHIN
 普中

实验名称：超声波测距实验
接线说明：HC-SR04超声波模块-->ESP32 IO
         (VCC)-->(5V)
         (Trig)-->(4)
         (Echo)-->(27)
         (GND)-->(GND)
         
实验现象：程序下载成功后，软件shell控制台间隔一段时间输出超声波模块测量距离
         
注意事项：

'''

#导入Pin模块
from machine import Pin
import time
from hcsr04 import HCSR04

#定义HCSR04控制对象
hcsr04=HCSR04(trigger_pin=12, echo_pin=14)

#程序入口
if __name__=="__main__":
    
    while True:
        distance=hcsr04.distance_cm()
        print("distance=%.2fCM" %distance)
        time.sleep(0.1)
