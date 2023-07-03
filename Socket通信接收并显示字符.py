#导入Pin模块
from machine import Pin
import time
import network
import usocket
from machine import Pin,I2C
from i2c_lcd import I2cLcd
import re

#定义LED控制对象
led1=Pin(15,Pin.OUT)
# LCD 1602 I2C 地址
DEFAULT_I2C_ADDR = 0x27
i2c = I2C(1,sda=Pin(14),scl=Pin(12),freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)  # 初始化(设备地址, 背光设置)

#路由器WIFI账号和密码
ssid="Mercury_X30G"
password="Xu3328313"

#服务器地址和端口
dest_ip="192.168.1.100"
dest_port=10000

#WIFI连接
def wifi_connect():
    wlan=network.WLAN(network.STA_IF)  #STA模式
    wlan.active(True)  #激活
    start_time=time.time()  #记录时间做超时判断
    
    if not wlan.isconnected():
        print("conneting to network...")
        wlan.connect(ssid,password)  #输入WIFI账号和密码
        
        while not wlan.isconnected():
            led1.value(1)
            time.sleep_ms(300)
            led1.value(0)
            time.sleep_ms(300)
            
            #超时判断,15 秒没连接成功判定为超时
            if time.time()-start_time>15:
                print("WIFI Connect Timeout!")
                break
        return False
    
    else:
        led1.value(0)
        print("network information:", wlan.ifconfig())
        return True

#程序入口
if __name__=="__main__":
    
    if wifi_connect():
        socket=usocket.socket()  #创建socket连接
        addr=(dest_ip,dest_port)  #服务器IP地址和端口
        socket.connect(addr)
        socket.send("Connected")
        while True:
            text=socket.recv(32)  #单次最多接收32字节，避免超出屏幕范围
            if text==None:
                pass
            
            elif len(text)<=16: #一行能显示则直接显示
                text=text.decode("utf-8")
                lcd.putstr("                \n")
                lcd.putstr("                \n") #清屏
                lcd.putstr(text)
                socket.send("I get:"+text)
            else: #需要用两行显示则分割字符串
                text=text.decode("utf-8")
                lcd.putstr("                \n")
                lcd.putstr("                \n") #清屏
                lcd.putstr(text[:17]) #显示第一行
                lcd.putstr('\n') #换行
                lcd.putstr(text[17:]) #显示第二行
                socket.send("I get:"+text)    
            time.sleep_ms(300)
        