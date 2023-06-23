import max7219
from machine import Pin, SPI
import time
import random
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(0))
ss = Pin(4, Pin.OUT)
while True:
    display = max7219.Matrix8x8(spi, ss, 1)
    x=random.randint(0,5)
    y=random.randint(0,5)
    w=random.randint(2,5)
    h=random.randint(2,5)
    #display.rect(x,y,w,h,1)
    display.fill_rect(x,y,w,h,1)
    display.show()
    time.sleep(0.2)
        