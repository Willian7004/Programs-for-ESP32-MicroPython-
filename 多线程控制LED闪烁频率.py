import _thread
import time
from machine import Pin

LED1=Pin(15,Pin.OUT)
LED2=Pin(2,Pin.OUT)
LED3=Pin(4,Pin.OUT)
LED4=Pin(16,Pin.OUT)
LED5=Pin(17,Pin.OUT)
LED6=Pin(5,Pin.OUT)
LED7=Pin(18,Pin.OUT)
LED8=Pin(19,Pin.OUT)
LED9=Pin(21,Pin.OUT)

i=0
f1=int(input("输入LED1开关频率"))
d1=round(500/f1)
f2=int(input("输入LED2开关频率"))
d2=round(500/f2)
f3=int(input("输入LED3开关频率"))
d3=round(500/f3)
f4=int(input("输入LED4开关频率"))
d4=round(500/f4)
f5=int(input("输入LED5开关频率"))
d5=round(500/f5)
f6=int(input("输入LED6开关频率"))
d6=round(500/f6)
f7=int(input("输入LED7开关频率"))
d7=round(500/f7)
f8=int(input("输入LED8开关频率"))
d8=round(500/f8)
f9=int(input("输入LED9开关频率"))
d9=round(500/f9)

def th1(d1,i):
    print(i)
    while True:
        LED1.value(1)
        time.sleep_ms(d1)
        LED1.value(0)

def th2(d2,i):
   print(i)
   while True:
        LED2.value(1)
        time.sleep_ms(d2)
        LED2.value(0)
        
def th3(d3,i):
    print(i)
    while True:
        LED3.value(1)
        time.sleep_ms(d3)
        LED3.value(0)
        
def th4(d4,i):
    print(i)
    while True:
        LED4.value(1)
        time.sleep_ms(d4)
        LED4.value(0)
        
def th5(d5,i):
     print(i)
     while True:
        LED5.value(1)
        time.sleep_ms(d5)
        LED5.value(0)
        
def th6(d6,i):
   print(i)
   while True:
        LED6.value(1)
        time.sleep_ms(d6)
        LED6.value(0)
        
def th7(d7,i):
    print(i)
    while True:
        LED7.value(1)
        time.sleep_ms(d7)
        LED7.value(0)
        
def th8(d8,i):
    print(i)
    while True:
        LED8.value(1)
        time.sleep_ms(d8)
        LED8.value(0)
        
def th9(d9,i):
    print(i)
    while True:
        LED9.value(1)
        time.sleep_ms(d9)
        LED9.value(0)
        
_thread.start_new_thread(th1, (d1, i))
_thread.start_new_thread(th2, (d2, i))
_thread.start_new_thread(th3, (d3, i))
_thread.start_new_thread(th4, (d4, i))
_thread.start_new_thread(th5, (d5, i))
_thread.start_new_thread(th6, (d6, i))
_thread.start_new_thread(th7, (d7, i))
_thread.start_new_thread(th8, (d8, i))
_thread.start_new_thread(th9, (d9, i))        
        
 