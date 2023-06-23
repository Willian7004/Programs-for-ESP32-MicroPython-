import max7219
from machine import Pin, SPI
import time
import random
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(0))
ss = Pin(4, Pin.OUT)
while True:
    display = max7219.Matrix8x8(spi, ss, 1)
    x1=random.randint(0,7)
    y1=random.randint(0,7)
    x2=random.randint(0,7)
    y2=random.randint(0,7)
    display.line(x1, y1,x2,y2, 1)
    display.show()
    time.sleep(0.2)
        