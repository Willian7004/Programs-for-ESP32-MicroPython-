import time
from machine import SoftI2C,Pin
from servo import Servos
i2c=SoftI2C(sda=Pin(9),scl=Pin(8),freq=10000)
servos=Servos(i2c,address=0x40)

servos.position(0,90)
servos.position(1,90)
servos.position(2,90)
servos.position(3,90)
servos.position(4,90)
servos.position(5,90)
servos.position(6,90)
servos.position(7,90)
servos.position(8,120)
servos.position(9,120)
servos.position(10,120)
servos.position(11,120)
