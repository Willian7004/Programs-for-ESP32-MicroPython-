import max7219
from machine import Pin, SPI
import time
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(0))
ss = Pin(4, Pin.OUT)
i=33
while True:
    display = max7219.Matrix8x8(spi, ss, 1)
    display.text(chr(i),0,0,1)
    display.show()
    print(i,chr(i))
    time.sleep(0.2)
    i+=1
    if i==127:
        i=33
    
