from ili934xnew import ILI9341, color565
from machine import Pin, SPI
import m5stack
import tt14
import glcdfont
import tt14
import tt24
import tt32

fonts = [glcdfont,tt14,tt24,tt32]

text = 'Happy Dragon Boat Festival!.'

power = Pin(m5stack.TFT_LED_PIN, Pin.OUT)
power.value(1)

spi = SPI(
    2,
    baudrate=60000000,
    miso=Pin(m5stack.TFT_MISO_PIN),
    mosi=Pin(m5stack.TFT_MOSI_PIN),
    sck=Pin(m5stack.TFT_CLK_PIN))

display = ILI9341(
    spi,
    cs=Pin(m5stack.TFT_CS_PIN),
    dc=Pin(m5stack.TFT_DC_PIN),
    rst=Pin(m5stack.TFT_RST_PIN),
    w=320,
    h=240,
    r=3)

display.erase()
display.set_pos(0,0)
for ff in fonts:
    display.set_font(ff)
    display.print(text)
for ff in fonts:
    display.set_font(ff)
    display.print(text)

