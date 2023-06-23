import max7219
from machine import Pin, SPI
import time
import random
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(0))
ss = Pin(4, Pin.OUT)
while True:
    display = max7219.Matrix8x8(spi, ss, 1)
    x=random.randint(0,7)
    y=random.randint(0,7)
    display.pixel(x,y,1)
    display.show()
    #time.sleep(0.1)
    time.sleep(0.005)
        