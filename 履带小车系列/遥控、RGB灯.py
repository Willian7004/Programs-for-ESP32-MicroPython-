#接线：(IR)-->(14)
#接线： WS-->(27)
'''
Pin15、2、0、4依次控制左、右轮正、反转
'''
         
#导入Pin模块
from machine import Pin
from neopixel import NeoPixel
import time
from machine import Timer
import random

pin=27
rgb_num=5
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

#定义IRED控制对象
ired=Pin(14,Pin.IN,Pin.PULL_UP)
led1=Pin(15,Pin.OUT)#构建led1对象，GPIO15输出
led2=Pin(2,Pin.OUT)
led3=Pin(0,Pin.OUT)
led4=Pin(4,Pin.OUT)

#存储红外遥控器键值
gired_data=[0,0,0,0]
#定时器0中断函数
def time0_irq(time0):
     led1.value(0)
     led2.value(0)
     led3.value(0)
     led4.value(0)
     gired_data[2]=0x40
     time1.init(period=500,mode=Timer.PERIODIC,callback=time1_irq)
time0=Timer(0)  #创建time0定时器对象

a=0
b=0
c=0
def time1_irq(time1):
            for i in range(rgb_num):
                a=random.randint(0,255)
                b=random.randint(0,255)
                c=random.randint(0,255)
                rgb_led[i]=(a, b, c)
                rgb_led.write()  
time1=Timer(0)  #创建time1定时器对象
time1.init(period=500,mode=Timer.PERIODIC,callback=time1_irq)

#外部中断函数
def ired_irq(ired):
    ired_high_time=0  #保存高电平时间，鉴别数据1还是0
    
    if ired.value()==0:
        time_cnt=1000
        while (not ired.value()) and time_cnt:  #等待引导信号9ms低电平结束，若超过10ms强制退出
            time.sleep_us(10)
            time_cnt-=1
            if time_cnt==0:
                return
        
        if ired.value()==1:  #引导信号9ms低电平已过，进入4.5ms高电平
            time_cnt=500
            while ired.value() and time_cnt:  #等待引导信号4.5ms高电平结束，若超过5ms强制退出
                time.sleep_us(10)
                time_cnt-=1
                if time_cnt==0:
                    return
            for i in range(4):  #循环4次，读取4个字节数据
                for j in range(8):  #循环8次读取每位数据即一个字节
                    time_cnt=600
                    while (ired.value()==0) and time_cnt:  #等待数据1或0前面的0.56ms结束，若超过6ms强制退出
                        time.sleep_us(10)
                        time_cnt-=1
                        if time_cnt==0:
                            return
                    time_cnt=20
                    while ired.value()==1:  #等待数据1或0后面的高电平结束，若超过2ms强制退出
                        time.sleep_us(100)
                        ired_high_time+=1
                        if ired_high_time>20:
                            return
                    gired_data[i]>>=1  #先读取的为低位，然后是高位
                    if ired_high_time>=8:  #如果高电平时间大于0.8ms，数据则为1，否则为0
                        gired_data[i]|=0x80
                    ired_high_time=0  #重新清零，等待下一次计算时间
        if gired_data[2]!=~gired_data[3]:  #校验控制码与反码，错误则返回
            for i in range(4):
                gired_data[i]=0
                return
    
    def tracks(d,e,f,g) :
       led1.value(d)
       led2.value(e)
       led3.value(f)
       led4.value(g)
       
    print("红外遥控器操作码：0x%02X"%gired_data[2])
    if gired_data[2]==0x45 :
          tracks(0,0,1,0)
          time0.init(period=200,mode=Timer.ONE_SHOT,callback=time0_irq)
    elif gired_data[2]==0x46 :
          tracks(1,0,1,0)
    elif gired_data[2]==0x47 :
          tracks(1,0,0,0)
          time0.init(period=200,mode=Timer.ONE_SHOT,callback=time0_irq)
    elif gired_data[2]==0x44 :
          tracks(0,1,1,0)
          time0.init(period=200,mode=Timer.ONE_SHOT,callback=time0_irq)
    elif gired_data[2]==0x40 :
          tracks(0,0,0,0)
    elif gired_data[2]==0x43 :
         tracks(1,0,0,1)
         time0.init(period=200,mode=Timer.ONE_SHOT,callback=time0_irq)
    elif gired_data[2]==0x07 :
          tracks(0,0,0,1)
          time0.init(period=200,mode=Timer.ONE_SHOT,callback=time0_irq)
    elif gired_data[2]==0x15 :
          tracks(0,1,0,1)
    elif gired_data[2]==0x09 :
         tracks(0,1,0,0)
         time0.init(period=200,mode=Timer.ONE_SHOT,callback=time0_irq)

#程序入口
if __name__=="__main__":
    ired.irq(ired_irq,Pin.IRQ_FALLING)
    
    while True:
        pass
