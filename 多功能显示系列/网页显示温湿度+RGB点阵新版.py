'''
  舵机-->(22)
  (Trig)-->(5)
  (Echo)-->(18)
  SCL-->16
  SDA-->17
  DS-->27
   WS-->(13)
'''

#导入Pin模块
from machine import Pin
import time
from servo import Servo
from machine import Timer
from hcsr04 import HCSR04
from neopixel import NeoPixel
import random
from machine import ADC
import dht
import network
import socket
import _thread

#定义RGB控制对象
#控制引脚为13，RGB灯串联5个
pin=13
rgb_num=64
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

brightness=12
delay=400
mode=1

#定义LED控制对象
led1=Pin(15,Pin.OUT,Pin.PULL_DOWN)
relay=Pin(2,Pin.OUT,Pin.PULL_DOWN)
#定义DHT22控制对象
sensor=dht.DHT22(Pin(27))

#连接的WIFI账号和密码
ssid = "Mercury_X30G"
password = "Xu3328313"

temp = hum = 99
def read_sensor():
    global temp, hum
    try:
        sensor.measure()
        temp = round(sensor.temperature(),1)
        hum = round(sensor.humidity(),1)
        if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))

            # uncomment for Fahrenheit
            #temp = temp * (9/5) + 32.0           
            return(msg)
        else:
            return('Invalid sensor readings.')
    except OSError as e:
        return('Failed to read sensor.')
        
#WIFI连接
def wifi_connect():
    wlan=network.WLAN(network.STA_IF)  #STA模式
    wlan.active(True)  #激活
    
    if not wlan.isconnected():
        print("conneting to network...")
        wlan.connect(ssid,password)  #输入 WIFI 账号密码
        
        while not wlan.isconnected():
            led1.value(1)
            time.sleep_ms(300)
            led1.value(0)
            time.sleep_ms(300)
        led1.value(0)
        return False
    else:
        led1.value(0)
        print("network information:", wlan.ifconfig())
        return True

#网页数据
def web_page():
  html = """<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  
  
  <style>
    .button{display: inline-block; background-color: #141414; border: none; 
    border-radius: 4px; color: white; padding: 8px 15px; text-decoration: none; font-size: 20px; margin: 2px; cursor: pointer;}
    .button2{background-color: #282828;}.button3{background-color: #3c3c3c;}.button4{background-color: #505050;}
    .button5{background-color: #646464;}.button6{background-color: #787878;}.button7{background-color: #8c8c8c;}
    .button8{background-color: #a0a0a0;}.button9{background-color: #b4b4b4;}.button10{background-color: #c8c8c8;}
    .button11{background-color: #f01010;}.button12{background-color: #10f010;}.button13{background-color: #1010f0;}
    .button14{background-color: #0000ff;}.button15{background-color: #0f0fe1;}.button16{background-color: #1e1ed2;}
    .button17{background-color: #2d2dc3;}.button18{background-color: #3c3cb4;}.button19{background-color: #4b4ba5;}
    .button20{background-color: #5a5a96;}.button21{background-color: #696987;}.button22{background-color: #787878;}
    .button23{background-color: #f0f010;}
    a:link {text-decoration:none;}a:visited {text-decoration:none;}a:hover {text-decoration:none;}
    a:active {text-decoration:none;} 
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 1.5rem; }
    p { font-size: 1.5rem; }
    .units { font-size: 1rem; }
    .dht-labels{
      font-size: 1rem;
      vertical-align:middle;
      padding-bottom: 7px;
    }
  </style>
</head>
<body>
  <h2>ESP32 DHT22 Acquisition</h2>
  <p>
    
    <span class="dht-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;C</sup>
  </p>
  <p>
    
    <span class="dht-labels">Humidity</span>
    <span>"""+str(hum)+"""</span>
    <sup class="units">%</sup>
  </p>
  <h2>ESP32 WS2812 Control</h2> <p><a href="/?d1">Brightness: <strong>""" + str(brightness) + """</strong></a></p>
        <p><a href="/?b1">
        <a href="/?b3"><button class="button button3">09</button></a><a href="/?b4"><button class="button button4">12</button></a>
        <a href="/?b5"><button class="button button5">15</button></a><a href="/?b6"><button class="button button6">18</button></a>
        <a href="/?b7"><button class="button button7">21</button></a><a href="/?b8"><button class="button button8">24</button></a>
        <a href="/?b9"><button class="button button9">27</button></a><a href="/?b10"><button class="button button10">30</button></p></a>
        <p><a href="/?d2">Mode: <strong>""" + str(mode) + """</strong></a></p>
        <p><a href="/?b11"><button class="button button11">0</button></a>
        <a href="/?b12"><button class="button button12">1</button></a>
        <a href="/?b13"><button class="button button13">2</button></a>
        <a href="/?b23"><button class="button button23">3</button></a></p>
        <p><a href="/?d3">Delay: <strong>""" + str(delay) + """</strong></a></p>
        <p><a href="/?b15"><button class="button button15">200</button></a>
        <a href="/?b16"><button class="button button16">300</button></a><a href="/?b17"><button class="button button17">400</button></a>
        <a href="/?b18"><button class="button button18">500</button></a><a href="/?b19"><button class="button button19">600</button></a>
        <a href="/?b20"><button class="button button20">700</button></a><a href="/?b21"><button class="button button21">800</button></a>
        <a href="/?b22"><button class="button button22">900</button></a></p>
</body>
</html>"""
  return html

b=0
c=120
g=0
h=0
k=0
l=0
m=0
#定时器0中断函数
def time0_irq(i1,i2):
    global b
    global c
    global g
    global h
    global k
    global l
    global m
    global temp, hum
    global brightness
    global mode
    global delay
    while True:
        
        if mode==1 :
            i=0
            d1=random.randint(0,brightness)
            e1=random.randint(0,brightness)
            f1=random.randint(0,brightness)            
            d2=random.randint(0,brightness)
            e2=random.randint(0,brightness)
            f2=random.randint(0,brightness)
            while i<8 :
                rgb_led[i]=(d1,e1,f1)
                i+=1
            while i<16:
                rgb_led[i]=(d2,e2,f2)
                i+=1
            while i<24 :
                rgb_led[i]=(d1,e1,f1)
                i+=1
            while i<32:
                rgb_led[i]=(d2,e2,f2)
                i+=1
            while i<40 :
                rgb_led[i]=(d1,e1,f1)
                i+=1
            while i<48:
                rgb_led[i]=(d2,e2,f2)
                i+=1
            while i<56 :
                rgb_led[i]=(d1,e1,f1)
                i+=1
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=1
            rgb_led.write()    
            relay.value(1)
            time.sleep_ms(delay)
            i=0
            while i<64:
                rgb_led[i]=(d1,e1,f1)
                i+=8
            i=1
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=8
            i=2
            while i<64:
                rgb_led[i]=(d1,e1,f1)
                i+=8
            i=3
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=8
            i=4
            while i<64:
                rgb_led[i]=(d1,e1,f1)
                i+=8
            i=5
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=8
            i=6
            while i<64:
                rgb_led[i]=(d1,e1,f1)
                i+=8
            i=7
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=8    
            rgb_led.write()
        if mode==0 :
            relay.value(0)
            for i in range(rgb_num):
                rgb_led[i]=(0, 0, 0)
            rgb_led.write()
        if mode==2 : 
            relay.value(1)
            i=0
            repeat=0
            d1=random.randint(0,brightness)
            e1=random.randint(0,brightness)
            f1=random.randint(0,brightness)            
            d2=random.randint(0,brightness)
            e2=random.randint(0,brightness)
            f2=random.randint(0,brightness)
            d3=random.randint(0,brightness)
            e3=random.randint(0,brightness)
            f3=random.randint(0,brightness)            
            d4=random.randint(0,brightness)
            e4=random.randint(0,brightness)
            f4=random.randint(0,brightness)
            while i<4 :
                rgb_led[i]=(d1,e1,f1)
                i+=1
            while i<8:
                rgb_led[i]=(d2,e2,f2)
                i+=1
            while i<12 :
                rgb_led[i]=(d3,e3,f3)
                i+=1
            while i<16:
                rgb_led[i]=(d4,e4,f4)
                i+=1
            while i<20 :
                rgb_led[i]=(d1,e1,f1)
                i+=1
            while i<24:
                rgb_led[i]=(d2,e2,f2)
                i+=1
            while i<28 :
                rgb_led[i]=(d3,e3,f3)
                i+=1
            while i<32:
                rgb_led[i]=(d4,e4,f4)
                i+=1
            while i<36 :
                rgb_led[i]=(d1,e1,f1)
                i+=1
            while i<40:
                rgb_led[i]=(d2,e2,f2)
                i+=1
            while i<44 :
                rgb_led[i]=(d3,e3,f3)
                i+=1
            while i<48:
                rgb_led[i]=(d4,e4,f4)
                i+=1
            while i<52 :
                rgb_led[i]=(d1,e1,f1)
                i+=1
            while i<56:
                rgb_led[i]=(d2,e2,f2)
                i+=1
            while i<60 :
                rgb_led[i]=(d3,e3,f3)
                i+=1
            while i<64:
                rgb_led[i]=(d4,e4,f4)
                i+=1    
            rgb_led.write()    
            relay.value(1)
            time.sleep_ms(delay)
            i=0
            while i<64:
                rgb_led[i]=(d1,e1,f1)
                i+=8
            i=1
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=8
            i=2
            while i<64:
                rgb_led[i]=(d1,e1,f1)
                i+=8
            i=3
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=8
            i=4
            while i<64:
                rgb_led[i]=(d1,e1,f1)
                i+=8
            i=5
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=8
            i=6
            while i<64:
                rgb_led[i]=(d1,e1,f1)
                i+=8
            i=7
            while i<64:
                rgb_led[i]=(d2,e2,f2)
                i+=8    
            rgb_led.write()    
        if mode==3 : #同心矩形
            relay.value(1)
            d1=random.randint(0,brightness)
            e1=random.randint(0,brightness)
            f1=random.randint(0,brightness)            
            d2=random.randint(0,brightness)
            e2=random.randint(0,brightness)
            f2=random.randint(0,brightness)
            d3=random.randint(0,brightness)
            e3=random.randint(0,brightness)
            f3=random.randint(0,brightness)            
            d4=random.randint(0,brightness)
            e4=random.randint(0,brightness)
            f4=random.randint(0,brightness)
            i=0                
            while i<32:
                rgb_led[i]=(d1, e1, f1)
                i+=1
            while i<64:
                rgb_led[i]=(d2, e2, f2)
                i+=1    
            i=9
            while i<32:
                rgb_led[i]=(d3, e3, f3)
                i+=1
                if i%8==7:
                    i+=2
            while i<55:
                rgb_led[i]=(d4, e4, f4)
                i+=1
                if i%8==7:
                    i+=2
            i=18
            while i<32:
                rgb_led[i]=(d3, e3, f3)
                i+=1
                if i%8==6:
                    i+=4
            while i<46:
                rgb_led[i]=(d1, e1, f1)
                i+=1
                if i%8==6:
                    i+=4
            i=27
            while i<32:
                rgb_led[i]=(d4, e4, f4)
                i+=1
                if i%8==5:
                    i+=6
            while i<37:
                rgb_led[i]=(d2, e2, f2)
                i+=1
                if i%8==5:
                    i+=6
            rgb_led.write()
        time.sleep_ms(delay)
           
wifi_connect()
#SOCK_STREAM表示的是TCP协议，SOCK_DGRAM表示的是UDP协议
my_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建socket连接
# 将socket对象绑定ip地址和端口号
my_socket.bind(('', 80))
# 相当于电话的开机 括号里的参数表示可以同时接收5个请求
my_socket.listen(5)
def server(i1,i2):
    global brightness
    global mode
    global delay
    while True:
        try:
            read_sensor()
            # 进入监听状态，等待别人链接过来，有两个返回值，
            #一个是对方的socket对象，一个是对方的ip以及端口
            client, addr = my_socket.accept()
            print('Got a connection from %s' % str(addr))
            # recv表示接收，括号里是最大接收字节
            request = client.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            # 进入监听状态，等待别人链接过来，有两个返回值，
            #一个是对方的socket对象，一个是对方的ip以及端口
            client, addr = my_socket.accept()
            print('Got a connection from %s' % str(addr))
            # recv表示接收，括号里是最大接收字节
            request = client.recv(1024)
            request = str(request)
            print('Content = %s' % request)
           
            b3 = request.find('/?b3')
            b4 = request.find('/?b4')
            b5 = request.find('/?b5')
            b6 = request.find('/?b6')
            b7 = request.find('/?b7')
            b8 = request.find('/?b8')
            b9 = request.find('/?b9')
            b10 = request.find('/?b10')
            b11 = request.find('/?b11')
            b12 = request.find('/?b12')
            b13 = request.find('/?b13')
            
            b15 = request.find('/?b15')
            b16 = request.find('/?b16')
            b17 = request.find('/?b17')
            b18 = request.find('/?b18')
            b19 = request.find('/?b19')
            b20 = request.find('/?b20')
            b21 = request.find('/?b21')
            b22 = request.find('/?b22')
            b23 = request.find('/?b23')
            d1 = request.find('/?d1')
            d2 = request.find('/?d2')
            d3 = request.find('/?d3')
            
            if b3 == 6:
                brightness=9
            if b4 == 6:
                brightness=12
            if b5 == 6:
                brightness=15
            if b6 == 6:
                brightness=18
            if b7 == 6:
                brightness=21
            if b8 == 6:
                brightness=24
            if b9 == 6:
                brightness=27
            if b10 == 6:
                brightness=30
            if b11 == 6:
                mode=0
            if b12 == 6:
                mode=1
            if b13 == 6:
                mode=2
            
            if b15 == 6:
                delay=200
            if b16 == 6:
                delay=300
            if b17 == 6:
                delay=400
            if b18 == 6:
                delay=500
            if b19 == 6:
                delay=600
            if b20 == 6:
                delay=700
            if b21 == 6:
                delay=800
            if b22 == 6:
                delay=900
            if b23 == 6:
                mode=3    
            if d1 == 6:
                brightness=12
            if d2 == 6:
                mode=1
            if d3 == 6:
                delay=400    
        
            response = web_page()
            client.send('HTTP/1.1 200 OK\n')
            client.send('Content-Type: text/html\n')
            client.send('Connection: close\n\n')
            client.sendall(response)
            client.close()
        except OSError as e:
            pass
            print('Connection closed')

i1=0
i2=0
_thread.start_new_thread(server, (i1,i2))
_thread.start_new_thread(time0_irq, (i1, i2))