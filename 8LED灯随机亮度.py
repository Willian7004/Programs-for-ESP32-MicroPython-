#输出引脚：15、2、0、4、16、17、5、18
#导入Pin模块
from machine import Pin
from machine import PWM
import time
import random

#定义LED1控制对象
led1=PWM(Pin(15),freq=10000,duty=0)
led2=PWM(Pin(2),freq=10000,duty=0)
led3=PWM(Pin(0),freq=10000,duty=0)
led4=PWM(Pin(4),freq=10000,duty=0)
led5=PWM(Pin(16),freq=10000,duty=0)
led6=PWM(Pin(17),freq=10000,duty=0)
led7=PWM(Pin(5),freq=10000,duty=0)
led8=PWM(Pin(18),freq=10000,duty=0)

#程序入口
if __name__=="__main__":
   while True:
        duty_value1=random.randint(0,1023)
        duty_value2=random.randint(0,1023)
        duty_value3=random.randint(0,1023)
        duty_value4=random.randint(0,1023)
        duty_value5=random.randint(0,1023)
        duty_value6=random.randint(0,1023)
        duty_value7=random.randint(0,1023)
        duty_value8=random.randint(0,1023)
        led1.duty(duty_value1)
        time.sleep_ms(50)
        led2.duty(duty_value2)
        time.sleep_ms(50)
        led3.duty(duty_value3)
        time.sleep_ms(50)
        led4.duty(duty_value4)
        time.sleep_ms(50)
        led5.duty(duty_value5)
        time.sleep_ms(50)
        led6.duty(duty_value6)
        time.sleep_ms(50)
        led7.duty(duty_value7)
        time.sleep_ms(50)
        led8.duty(duty_value8)
        time.sleep_ms(50)
