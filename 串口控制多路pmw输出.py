#导入Pin模块
from machine import Pin
from machine import PWM
import time

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
        duty_value1=int(input("输入占空比1（1-1023）"))
        duty_value2=int(input("输入占空比2（1-1023）"))
        duty_value3=int(input("输入占空比3（1-1023）"))
        duty_value4=int(input("输入占空比4（1-1023）"))
        duty_value5=int(input("输入占空比5（1-1023）"))
        duty_value6=int(input("输入占空比6（1-1023）"))
        duty_value7=int(input("输入占空比7（1-1023）"))
        duty_value8=int(input("输入占空比8（1-1023）"))
        led1.duty(duty_value1)
        time.sleep_ms(10)
        led2.duty(duty_value2)
        time.sleep_ms(10)
        led3.duty(duty_value3)
        time.sleep_ms(10)
        led4.duty(duty_value4)
        time.sleep_ms(10)
        led5.duty(duty_value5)
        time.sleep_ms(10)
        led6.duty(duty_value6)
        time.sleep_ms(10)
        led7.duty(duty_value7)
        time.sleep_ms(10)
        led8.duty(duty_value8)
        time.sleep_ms(10)
