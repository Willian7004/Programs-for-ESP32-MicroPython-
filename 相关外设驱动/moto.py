from machine import *
import time


class moto:
    def __init__(self, pwm0, pwm1):
        self.pwm0 = pwm0
        self.pwm1 = pwm1
        
    def setPwm(self, pwm):
        pwm = int(pwm)
        if pwm < 0:
            self.pwm0.duty(-pwm)
            self.pwm1.duty(0)
        else:
            self.pwm0.duty(0)
            self.pwm1.duty(pwm)
            
            
class encoder:
    def __init__(self, pin0, pin1, i):
        self.pin0 = pin0
        self.pin0.irq(trigger=Pin.IRQ_RISING, handler=self.handler0)
        self.pin1 = pin1
        self.pin0.irq(trigger=Pin.IRQ_RISING, handler=self.handler1)
        self.counter = 0
        self.speed = 0
        
        self.tim = Timer(i)
        self.tim.init(period=50, callback=self.timHandler)
    
    def handler0(self, a):
        if self.pin0.value():
            self.counter += 1
        else:
            self.counter -= 1
    
    def handler1(self, a):
        if not self.pin1.value():
            self.counter += 1
        else:
            self.counter -= 1
                
    def timHandler(self, t):
        self.speed = self.counter
        self.counter = 0
                
    def read(self):
        return self.speed

