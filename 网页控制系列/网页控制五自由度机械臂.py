#导入Pin模块
from machine import Pin
import time
from machine import SoftI2C
from servo import Servos
import network
import socket

#定义LED控制对象
led1=Pin(15,Pin.OUT,Pin.PULL_DOWN)
i2c=SoftI2C(sda=Pin(26),scl=Pin(27),freq=10000)
servos=Servos(i2c,address=0x40)

#连接的WIFI账号和密码
ssid = "Mercury_X30G"
password = "Xu3328313"

#舵机默认角度
servos.position(0,90)
servos.position(1,90)
servos.position(2,90)
servos.position(3,90)
servos.position(4,90)

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

a0=90
a1=90
a2=90
a3=90
a4=90
#网页数据
def web_page():
    global a0
    global a1
    global a2
    global a3
    global a4
  
    html = """<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  
  <style>
    .button{display: inline-block; background-color: #971080; border: none; 
    border-radius: 4px; color: white; padding: 8px 15px; text-decoration: none; font-size: 20px; margin: 2px; cursor: pointer;}
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
  <h2>ESP32 Servo Control</h2>
        <p><a href="/?d0">Servo0: <strong>""" + str(a0) + """</strong></a></p>
        <p><a href="/?b00"><button class="button">0</button></a>
        <a href="/?b01"><button class="button">10</button></a>
        <a href="/?b02"><button class="button">20</button></a>
        <a href="/?b03"><button class="button">30</button></a>
        <a href="/?b04"><button class="button">40</button></a>
        <a href="/?b05"><button class="button">50</button></a>
        <a href="/?b06"><button class="button">60</button></a>
        <a href="/?b07"><button class="button">70</button></a>
        <a href="/?b08"><button class="button">80</button></a>
        <a href="/?b09"><button class="button">90</button></a>
        <a href="/?b0a"><button class="button">100</button></a>
        <a href="/?b0b"><button class="button">110</button></a>
        <a href="/?b0c"><button class="button">120</button></a>
        <a href="/?b0d"><button class="button">130</button></a>
        <a href="/?b0e"><button class="button">140</button></a>
        <a href="/?b0f"><button class="button">150</button></a>
        <a href="/?b0g"><button class="button">160</button></a>
        <a href="/?b0h"><button class="button">170</button></a>
        <a href="/?b0i"><button class="button">180</button></a></p>
        <p><a href="/?d1">Servo1: <strong>""" + str(a1) + """</strong></a></p>
        <p><a href="/?b10"><button class="button">0</button></a>
        <a href="/?b11"><button class="button">10</button></a>
        <a href="/?b12"><button class="button">20</button></a>
        <a href="/?b13"><button class="button">30</button></a>
        <a href="/?b14"><button class="button">40</button></a>
        <a href="/?b15"><button class="button">50</button></a>
        <a href="/?b16"><button class="button">60</button></a>
        <a href="/?b17"><button class="button">70</button></a>
        <a href="/?b18"><button class="button">80</button></a>
        <a href="/?b19"><button class="button">90</button></a>
        <a href="/?b1a"><button class="button">100</button></a>
        <a href="/?b1b"><button class="button">110</button></a>
        <a href="/?b1c"><button class="button">120</button></a>
        <a href="/?b1d"><button class="button">130</button></a>
        <a href="/?b1e"><button class="button">140</button></a>
        <a href="/?b1f"><button class="button">150</button></a>
        <a href="/?b1g"><button class="button">160</button></a>
        <a href="/?b1h"><button class="button">170</button></a>
        <a href="/?b1i"><button class="button">180</button></a></p>
        <p><a href="/?d2">Servo2: <strong>""" + str(a2) + """</strong></a></p>
        <p><a href="/?b10"><button class="button">0</button></a>
        <a href="/?b21"><button class="button">10</button></a>
        <a href="/?b22"><button class="button">20</button></a>
        <a href="/?b23"><button class="button">30</button></a>
        <a href="/?b24"><button class="button">40</button></a>
        <a href="/?b25"><button class="button">50</button></a>
        <a href="/?b26"><button class="button">60</button></a>
        <a href="/?b27"><button class="button">70</button></a>
        <a href="/?b28"><button class="button">80</button></a>
        <a href="/?b29"><button class="button">90</button></a>
        <a href="/?b2a"><button class="button">100</button></a>
        <a href="/?b2b"><button class="button">110</button></a>
        <a href="/?b2c"><button class="button">120</button></a>
        <a href="/?b2d"><button class="button">130</button></a>
        <a href="/?b2e"><button class="button">140</button></a>
        <a href="/?b2f"><button class="button">150</button></a>
        <a href="/?b2g"><button class="button">160</button></a>
        <a href="/?b2h"><button class="button">170</button></a>
        <a href="/?b2i"><button class="button">180</button></a></p>
        <p><a href="/?d3">Servo3: <strong>""" + str(a3) + """</strong></a></p>
        <p><a href="/?b30"><button class="button">0</button></a>
        <a href="/?b31"><button class="button">10</button></a>
        <a href="/?b32"><button class="button">20</button></a>
        <a href="/?b33"><button class="button">30</button></a>
        <a href="/?b34"><button class="button">40</button></a>
        <a href="/?b35"><button class="button">50</button></a>
        <a href="/?b36"><button class="button">60</button></a>
        <a href="/?b37"><button class="button">70</button></a>
        <a href="/?b38"><button class="button">80</button></a>
        <a href="/?b39"><button class="button">90</button></a>
        <a href="/?b3a"><button class="button">100</button></a>
        <a href="/?b3b"><button class="button">110</button></a>
        <a href="/?b3c"><button class="button">120</button></a>
        <a href="/?b3d"><button class="button">130</button></a>
        <a href="/?b3e"><button class="button">140</button></a>
        <a href="/?b3f"><button class="button">150</button></a>
        <a href="/?b3g"><button class="button">160</button></a>
        <a href="/?b3h"><button class="button">170</button></a>
        <a href="/?b3i"><button class="button">180</button></a></p>
        <p><a href="/?d4">Servo4: <strong>""" + str(a4) + """</strong></a></p>
        <p><a href="/?b30"><button class="button">0</button></a>
        <a href="/?b41"><button class="button">10</button></a>
        <a href="/?b42"><button class="button">20</button></a>
        <a href="/?b43"><button class="button">30</button></a>
        <a href="/?b44"><button class="button">40</button></a>
        <a href="/?b45"><button class="button">50</button></a>
        <a href="/?b46"><button class="button">60</button></a>
        <a href="/?b47"><button class="button">70</button></a>
        <a href="/?b48"><button class="button">80</button></a>
        <a href="/?b49"><button class="button">90</button></a>
        <a href="/?b4a"><button class="button">100</button></a>
        <a href="/?b4b"><button class="button">110</button></a>
        <a href="/?b4c"><button class="button">120</button></a>
        <a href="/?b4d"><button class="button">130</button></a>
        <a href="/?b4e"><button class="button">140</button></a>
        <a href="/?b4f"><button class="button">150</button></a>
        <a href="/?b4g"><button class="button">160</button></a>
        <a href="/?b4h"><button class="button">170</button></a>
        <a href="/?b4i"><button class="button">180</button></a></p>
</body>
</html>"""
    return html

#程序入口
if __name__=="__main__":
    wifi_connect()
    #SOCK_STREAM表示的是TCP协议，SOCK_DGRAM表示的是UDP协议
    my_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建socket连接
    # 将socket对象绑定ip地址和端口号
    my_socket.bind(('', 80))
    # 相当于电话的开机 括号里的参数表示可以同时接收5个请求
    my_socket.listen(5)
    while True:
      try:    
        # 进入监听状态，等待别人链接过来，有两个返回值，
        #一个是对方的socket对象，一个是对方的ip以及端口
        client, addr = my_socket.accept()
        print('Got a connection from %s' % str(addr))
        # recv表示接收，括号里是最大接收字节
        request = client.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        b00 = request.find('/?b00')
        b01 = request.find('/?b01')
        b02 = request.find('/?b02')
        b03 = request.find('/?b03')
        b04 = request.find('/?b04')
        b05 = request.find('/?b05')
        b06 = request.find('/?b06')
        b07 = request.find('/?b07')
        b08 = request.find('/?b08')
        b09 = request.find('/?b09')
        b0a = request.find('/?b0a')
        b0b = request.find('/?b0b')
        b0c = request.find('/?b0c')
        b0d = request.find('/?b0d')
        b0e = request.find('/?b0e')
        b0f = request.find('/?b0f')
        b0g = request.find('/?b0g')
        b0h = request.find('/?b0h')
        b0i = request.find('/?b0i')
        b10 = request.find('/?b10')
        b11 = request.find('/?b11')
        b12 = request.find('/?b12')
        b13 = request.find('/?b13')
        b14 = request.find('/?b14')
        b15 = request.find('/?b15')
        b16 = request.find('/?b16')
        b17 = request.find('/?b17')
        b18 = request.find('/?b18')
        b19 = request.find('/?b19')
        b1a = request.find('/?b1a')
        b1b = request.find('/?b1b')
        b1c = request.find('/?b1c')
        b1d = request.find('/?b1d')
        b1e = request.find('/?b1e')
        b1f = request.find('/?b1f')
        b1g = request.find('/?b1g')
        b1h = request.find('/?b1h')
        b1i = request.find('/?b1i')
        b20 = request.find('/?b10')
        b21 = request.find('/?b21')
        b22 = request.find('/?b22')
        b23 = request.find('/?b23')
        b24 = request.find('/?b24')
        b25 = request.find('/?b25')
        b26 = request.find('/?b26')
        b27 = request.find('/?b27')
        b28 = request.find('/?b28')
        b29 = request.find('/?b29')
        b2a = request.find('/?b2a')
        b2b = request.find('/?b2b')
        b2c = request.find('/?b2c')
        b2d = request.find('/?b2d')
        b2e = request.find('/?b2e')
        b2f = request.find('/?b2f')
        b2g = request.find('/?b2g')
        b2h = request.find('/?b2h')
        b2i = request.find('/?b2i')
        b30 = request.find('/?b30')
        b31 = request.find('/?b31')
        b32 = request.find('/?b32')
        b33 = request.find('/?b33')
        b34 = request.find('/?b34')
        b35 = request.find('/?b35')
        b36 = request.find('/?b36')
        b37 = request.find('/?b37')
        b38 = request.find('/?b38')
        b39 = request.find('/?b39')
        b3a = request.find('/?b3a')
        b3b = request.find('/?b3b')
        b3c = request.find('/?b3c')
        b3d = request.find('/?b3d')
        b3e = request.find('/?b3e')
        b3f = request.find('/?b3f')
        b3g = request.find('/?b3g')
        b3h = request.find('/?b3h')
        b3i = request.find('/?b3i')
        b40 = request.find('/?b40')
        b41 = request.find('/?b41')
        b42 = request.find('/?b42')
        b43 = request.find('/?b43')
        b44 = request.find('/?b44')
        b45 = request.find('/?b45')
        b46 = request.find('/?b46')
        b47 = request.find('/?b47')
        b48 = request.find('/?b48')
        b49 = request.find('/?b49')
        b4a = request.find('/?b4a')
        b4b = request.find('/?b4b')
        b4c = request.find('/?b4c')
        b4d = request.find('/?b4d')
        b4e = request.find('/?b4e')
        b4f = request.find('/?b4f')
        b4g = request.find('/?b4g')
        b4h = request.find('/?b4h')
        b4i = request.find('/?b4i')
        if b00 == 6:
            servos.position(0,0)
            a0=0
        if b11 == 6:
            servos.position(0,10)
            a0=10
        if b02 == 6:
            servos.position(0,20)
            a0=20
        if b03 == 6:
            servos.position(0,30)
            a0=30
        if b04 == 6:
            servos.position(0,40)
            a0=40
        if b05 == 6:
            servos.position(0,50)
            a0=50
        if b06 == 6:
            servos.position(0,60)
            a0=60
        if b07 == 6:
            servos.position(0,70)
            a0=70
        if b08 == 6:
            servos.position(0,80)
            a0=80
        if b09 == 6:
            servos.position(0,90)
            a0=90
        if b0a == 6:
            servos.position(0,100)
            a0=100
        if b0b == 6:
            servos.position(0,110)
            a0=110
        if b0c == 6:
            servos.position(0,120)
            a0=120
        if b0d == 6:
            servos.position(0,130)
            a0=130
        if b0e == 6:
            servos.position(0,140)
            a0=140
        if b0f == 6:
            servos.position(0,150)
            a0=150
        if b0g == 6:
            servos.position(0,160)
            a0=160
        if b0h == 6:
            servos.position(0,170)
            a0=170
        if b0i == 6:
            servos.position(0,180)
            a0=180
        if b10 == 6:
            servos.position(1,0)
            a1=0
        if b11 == 6:
            servos.position(1,10)
            a1=10
        if b12 == 6:
            servos.position(1,20)
            a1=20
        if b13 == 6:
            servos.position(1,30)
            a1=30
        if b14 == 6:
            servos.position(1,40)
            a1=40
        if b15 == 6:
            servos.position(1,50)
            a1=50
        if b16 == 6:
            servos.position(1,60)
            a1=60
        if b17 == 6:
            servos.position(1,70)
            a1=70
        if b18 == 6:
            servos.position(1,80)
            a1=80
        if b19 == 6:
            servos.position(1,90)
            a1=90
        if b1a == 6:
            servos.position(1,100)
            a1=100
        if b1b == 6:
            servos.position(1,110)
            a1=110
        if b1c == 6:
            servos.position(1,120)
            a1=120
        if b1d == 6:
            servos.position(1,130)
            a1=130
        if b1e == 6:
            servos.position(1,140)
            a1=140
        if b1f == 6:
            servos.position(1,150)
            a1=150
        if b1g == 6:
            servos.position(1,160)
            a1=160
        if b1h == 6:
            servos.position(1,170)
            a1=170
        if b1i == 6:
            servos.position(1,180)
            a1=180
        if b20 == 6:
            servos.position(2,0)
            a2=0
        if b21 == 6:
            servos.position(2,10)
            a2=10
        if b22 == 6:
            servos.position(2,20)
            a2=20
        if b23 == 6:
            servos.position(2,30)
            a2=30
        if b24 == 6:
            servos.position(2,40)
            a2=40
        if b25 == 6:
            servos.position(2,50)
            a2=50
        if b26 == 6:
            servos.position(2,60)
            a2=60
        if b27 == 6:
            servos.position(2,70)
            a2=70
        if b28 == 6:
            servos.position(2,80)
            a2=80
        if b29 == 6:
            servos.position(2,90)
            a2=90
        if b2a == 6:
            servos.position(2,100)
            a2=100
        if b2b == 6:
            servos.position(2,110)
            a2=110
        if b2c == 6:
            servos.position(2,120)
            a2=120
        if b2d == 6:
            servos.position(2,130)
            a2=130
        if b2e == 6:
            servos.position(2,140)
            a2=140
        if b2f == 6:
            servos.position(2,150)
            a2=150
        if b2g == 6:
            servos.position(2,160)
            a2=160
        if b2h == 6:
            servos.position(2,170)
            a2=170
        if b2i == 6:
            servos.position(2,180)
            a2=180
        if b30 == 6:
            servos.position(3,0)
            a3=0
        if b31 == 6:
            servos.position(3,10)
            a3=10
        if b32 == 6:
            servos.position(3,20)
            a3=20
        if b33 == 6:
            servos.position(3,30)
            a3=30
        if b34 == 6:
            servos.position(3,40)
            a3=40
        if b35 == 6:
            servos.position(3,50)
            a3=50
        if b36 == 6:
            servos.position(3,60)
            a3=60
        if b37 == 6:
            servos.position(3,70)
            a3=70
        if b38 == 6:
            servos.position(3,80)
            a3=80
        if b39 == 6:
            servos.position(3,90)
            a3=90
        if b3a == 6:
            servos.position(3,100)
            a3=100
        if b3b == 6:
            servos.position(3,110)
            a3=110
        if b3c == 6:
            servos.position(3,120)
            a3=120
        if b3d == 6:
            servos.position(3,130)
            a3=130
        if b3e == 6:
            servos.position(3,140)
            a3=140
        if b3f == 6:
            servos.position(3,150)
            a3=150
        if b3g == 6:
            servos.position(3,160)
            a3=160
        if b3h == 6:
            servos.position(3,170)
            a3=170
        if b3i == 6:
            servos.position(3,180)
            a3=180
        if b40 == 6:
            servos.position(4,0)
            a4=0
        if b41 == 6:
            servos.position(4,10)
            a4=10
        if b42 == 6:
            servos.position(4,20)
            a4=20
        if b43 == 6:
            servos.position(4,30)
            a4=30
        if b44 == 6:
            servos.position(4,40)
            a4=40
        if b45 == 6:
            servos.position(4,50)
            a4=50
        if b46 == 6:
            servos.position(4,60)
            a4=60
        if b47 == 6:
            servos.position(4,70)
            a4=70
        if b48 == 6:
            servos.position(4,80)
            a4=80
        if b49 == 6:
            servos.position(4,90)
            a4=90
        if b4a == 6:
            servos.position(4,100)
            a4=100
        if b4b == 6:
            servos.position(4,110)
            a4=110
        if b4c == 6:
            servos.position(4,120)
            a4=120
        if b4d == 6:
            servos.position(4,130)
            a4=130
        if b4e == 6:
            servos.position(4,140)
            a4=140
        if b4f == 6:
            servos.position(4,150)
            a4=150
        if b4g == 6:
            servos.position(4,160)
            a4=160
        if b4h == 6:
            servos.position(4,170)
            a4=170
        if b4i == 6:
            servos.position(4,180)
            a4=180    
        response = web_page()
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(response)
        client.close()
      except:
          pass
