#导入Pin模块
from machine import Pin
import time
from machine import PWM
import network
import socket

#定义LED控制对象
led1=Pin(12,Pin.OUT,Pin.PULL_DOWN)
# 电机初始化
motor1=PWM(Pin(15),freq=1000,duty=0)
motor2=PWM(Pin(2),freq=1000,duty=0)
motor3=PWM(Pin(4),freq=1000,duty=0)
motor4=PWM(Pin(16),freq=1000,duty=0)
 
duty=0
speed=0
turn=0

#连接的WIFI账号和密码
ssid = "Mercury_X30G"
password = "Xu3328313"

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
    global a1
    global a2
    global a3
    global a4
  
    html = """<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  
  <style>
    .button{display: inline-block; background-color: #808080; border: none; 
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
  <h2>ESP32 Servo Control</h2> <p><a href="/?d1">speed: <strong>""" + str(speed) + """</strong></a></p>
        <p><a href="/?b10"><button class="button">-9</button></a>
        <a href="/?b11"><button class="button">-8</button></a>
        <a href="/?b12"><button class="button">-7</button></a>
        <a href="/?b13"><button class="button">-6</button></a>
        <a href="/?b14"><button class="button">-5</button></a>
        <a href="/?b15"><button class="button">-4</button></a>
        <a href="/?b16"><button class="button">-3</button></a>
        <a href="/?b17"><button class="button">-2</button></a>
        <a href="/?b18"><button class="button">-1</button></a>
        <a href="/?b19"><button class="button">0</button></a>
        <a href="/?b1a"><button class="button">1</button></a>
        <a href="/?b1b"><button class="button">2</button></a>
        <a href="/?b1c"><button class="button">3</button></a>
        <a href="/?b1d"><button class="button">4</button></a>
        <a href="/?b1e"><button class="button">5</button></a>
        <a href="/?b1f"><button class="button">6</button></a>
        <a href="/?b1g"><button class="button">7</button></a>
        <a href="/?b1h"><button class="button">8</button></a>
        <a href="/?b1i"><button class="button">9</button></a></p>
        <p><a href="/?d2">turn: <strong>""" + str(turn) + """</strong></a></p>
        <a href="/?b21"><button class="button">-5</button></a>
        <a href="/?b22"><button class="button">-4</button></a>
        <a href="/?b23"><button class="button">-3</button></a>
        <a href="/?b24"><button class="button">-2</button></a>
        <a href="/?b25"><button class="button">-1</button></a>
        <a href="/?b26"><button class="button">0</button></a>
        <a href="/?b27"><button class="button">1</button></a>
        <a href="/?b28"><button class="button">2</button></a>
        <a href="/?b29"><button class="button">3</button></a>
        <a href="/?b2a"><button class="button">4</button></a>
        <a href="/?b2b"><button class="button">5</button></a>
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
        if b10 == 6:
            motor1.duty(0)
            motor2.duty(1000)
            motor3.duty(0)
            motor4.duty(1000)
            speed=-9
            duty=-1000
        if b11 == 6:
            motor1.duty(0)
            motor2.duty(900)
            motor3.duty(0)
            motor4.duty(900)
            speed=-8
            duty=-900
        if b12 == 6:
            motor1.duty(0)
            motor2.duty(800)
            motor3.duty(0)
            motor4.duty(800)
            speed=-7
            duty=-800
        if b13 == 6:
            motor1.duty(0)
            motor2.duty(700)
            motor3.duty(0)
            motor4.duty(700)
            speed=-6
            duty=-700
        if b14 == 6:
            motor1.duty(0)
            motor2.duty(600)
            motor3.duty(0)
            motor4.duty(600)
            speed=-5
            duty=-600
        if b15 == 6:
            motor1.duty(0)
            motor2.duty(500)
            motor3.duty(0)
            motor4.duty(500)
            speed=-4
            duty=-500
        if b16 == 6:
            motor1.duty(0)
            motor2.duty(400)
            motor3.duty(0)
            motor4.duty(400)
            speed=-3
            duty=-400
        if b17 == 6:
            motor1.duty(0)
            motor2.duty(300)
            motor3.duty(0)
            motor4.duty(300)
            speed=-2
            duty=-300
        if b18 == 6:
            motor1.duty(0)
            motor2.duty(200)
            motor3.duty(0)
            motor4.duty(200)
            speed=-1
            duty=-200
        if b19 == 6:
            motor1.duty(0)
            motor2.duty(0)
            motor3.duty(0)
            motor4.duty(0)
            speed=0
            duty=0
        if b1a == 6:
            motor1.duty(200)
            motor2.duty(0)
            motor3.duty(200)
            motor4.duty(0)
            speed=1
            duty=200
        if b1b == 6:
            motor1.duty(300)
            motor2.duty(0)
            motor3.duty(300)
            motor4.duty(0)
            speed=2
            duty=300
        if b1c == 6:
            motor1.duty(400)
            motor2.duty(0)
            motor3.duty(400)
            motor4.duty(0)
            speed=3
            duty=400
        if b1d == 6:
            motor1.duty(500)
            motor2.duty(0)
            motor3.duty(500)
            motor4.duty(0)
            speed=4
            duty=500
        if b1e == 6:
            motor1.duty(600)
            motor2.duty(0)
            motor3.duty(600)
            motor4.duty(0)
            speed=5
            duty=600
        if b1f == 6:
            motor1.duty(700)
            motor2.duty(0)
            motor3.duty(700)
            motor4.duty(0)
            speed=6
            duty=700
        if b1g == 6:
            motor1.duty(800)
            motor2.duty(0)
            motor3.duty(800)
            motor4.duty(0)
            speed=7
            duty=800
        if b1h == 6:
            motor1.duty(900)
            motor2.duty(0)
            motor3.duty(900)
            motor4.duty(0)
            speed=8
            duty=900
        if b1i == 6:
            motor1.duty(1000)
            motor2.duty(0)
            motor3.duty(1000)
            motor4.duty(0)
            speed=9
            duty=1000
        if b21 == 6:
            if duty<1000 and duty>-1000:
                turn=-5
                if duty>200:
                    motor1.duty(duty-100)
                    motor2.duty(0)
                    motor3.duty(duty+100)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty-100)
                    motor3.duty(0)
                    motor4.duty(-duty+100)
                if duty==200:
                    motor1.duty(300)
                    motor2.duty(0)
                    motor3.duty(200)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(300)
                    motor3.duty(0)
                    motor4.duty(200)
                if duty==0:
                    motor1.duty(0)
                    motor2.duty(300)
                    motor3.duty(300)
                    motor4.duty(0)
        if b22 == 6:
            if duty<1000 and duty>-1000:
                turn=-4
                if duty>200:
                    motor1.duty(duty-80)
                    motor2.duty(0)
                    motor3.duty(duty+80)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty-80)
                    motor3.duty(0)
                    motor4.duty(-duty+80)
                if duty==200:
                    motor1.duty(280)
                    motor2.duty(0)
                    motor3.duty(200)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(280)
                    motor3.duty(0)
                    motor4.duty(200)
                if duty==0:
                    motor1.duty(0)
                    motor2.duty(280)
                    motor3.duty(280)
                    motor4.duty(0)
        if b23 == 6:
            if duty<1000 and duty>-1000:
                turn=-3
                if duty>200:
                    motor1.duty(duty-60)
                    motor2.duty(0)
                    motor3.duty(duty+60)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty-60)
                    motor3.duty(0)
                    motor4.duty(-duty+60)
                if duty==200:
                    motor1.duty(260)
                    motor2.duty(0)
                    motor3.duty(200)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(260)
                    motor3.duty(0)
                    motor4.duty(200)
                if duty==0:
                    motor1.duty(0)
                    motor2.duty(260)
                    motor3.duty(260)
                    motor4.duty(0)
        if b24 == 6:
            if duty<1000 and duty>-1000:
                turn=-2
                if duty>200:
                    motor1.duty(duty-40)
                    motor2.duty(0)
                    motor3.duty(duty+40)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty-40)
                    motor3.duty(0)
                    motor4.duty(-duty+40)
                if duty==200:
                    motor1.duty(240)
                    motor2.duty(0)
                    motor3.duty(200)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(240)
                    motor3.duty(0)
                    motor4.duty(200)
                if duty==0:
                    motor1.duty(0)
                    motor2.duty(240)
                    motor3.duty(240)
                    motor4.duty(0)
        if b25 == 6:
            if duty<1000 and duty>-1000:
                turn=-1
                if duty>200:
                    motor1.duty(duty-20)
                    motor2.duty(0)
                    motor3.duty(duty+20)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty-20)
                    motor3.duty(0)
                    motor4.duty(-duty+20)
                if duty==200:
                    motor1.duty(220)
                    motor2.duty(0)
                    motor3.duty(200)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(220)
                    motor3.duty(0)
                    motor4.duty(200)
                if duty==0:
                    motor1.duty(0)
                    motor2.duty(220)
                    motor3.duty(220)
                    motor4.duty(0)
        if b26 == 6:
            turn=0
            if duty>=0:
                motor1.duty(duty)
                motor2.duty(0)
                motor3.duty(duty)
                motor4.duty(0)
            if duty<0:
                motor1.duty(0)
                motor2.duty(-duty)
                motor3.duty(0)
                motor4.duty(-duty)
        if b27 == 6:
            if duty<1000 and duty>-1000:
                turn=1
                if duty>200:
                    motor1.duty(duty+20)
                    motor2.duty(0)
                    motor3.duty(duty-20)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty+20)
                    motor3.duty(0)
                    motor4.duty(-duty-20)
                if duty==200:
                    motor1.duty(200)
                    motor2.duty(0)
                    motor3.duty(220)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(200)
                    motor3.duty(0)
                    motor4.duty(220)
                if duty==0:
                    motor1.duty(220)
                    motor2.duty(0)
                    motor3.duty(0)
                    motor4.duty(220)
        if b28 == 6:
            if duty<1000 and duty>-1000:
                turn=2
                if duty>200:
                    motor1.duty(duty+40)
                    motor2.duty(0)
                    motor3.duty(duty-40)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty+40)
                    motor3.duty(0)
                    motor4.duty(-duty-40)
                if duty==200:
                    motor1.duty(200)
                    motor2.duty(0)
                    motor3.duty(240)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(200)
                    motor3.duty(0)
                    motor4.duty(240)
                if duty==0:
                    motor1.duty(240)
                    motor2.duty(0)
                    motor3.duty(0)
                    motor4.duty(240)
        if b29 == 6:
            if duty<1000 and duty>-1000:
                turn=3
                if duty>200:
                    motor1.duty(duty+60)
                    motor2.duty(0)
                    motor3.duty(duty-60)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty+60)
                    motor3.duty(0)
                    motor4.duty(-duty-60)
                if duty==200:
                    motor1.duty(200)
                    motor2.duty(0)
                    motor3.duty(260)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(200)
                    motor3.duty(0)
                    motor4.duty(260)
                if duty==0:
                    motor1.duty(260)
                    motor2.duty(0)
                    motor3.duty(0)
                    motor4.duty(260)
        if b2a == 6:
            if duty<1000 and duty>-1000:
                turn=4
                if duty>200:
                    motor1.duty(duty+80)
                    motor2.duty(0)
                    motor3.duty(duty-80)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty+80)
                    motor3.duty(0)
                    motor4.duty(-duty-80)
                if duty==200:
                    motor1.duty(200)
                    motor2.duty(0)
                    motor3.duty(280)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(200)
                    motor3.duty(0)
                    motor4.duty(280)
                if duty==0:
                    motor1.duty(280)
                    motor2.duty(0)
                    motor3.duty(0)
                    motor4.duty(280)
        if b2b == 6:
            if duty<1000 and duty>-1000:
                turn=5
                if duty>200:
                    motor1.duty(duty+100)
                    motor2.duty(0)
                    motor3.duty(duty-100)
                    motor4.duty(0)
                if duty<-200:
                    motor1.duty(0)
                    motor2.duty(-duty+100)
                    motor3.duty(0)
                    motor4.duty(-duty-100)
                if duty==200:
                    motor1.duty(200)
                    motor2.duty(0)
                    motor3.duty(300)
                    motor4.duty(0)
                if duty==-200:
                    motor1.duty(0)
                    motor2.duty(200)
                    motor3.duty(0)
                    motor4.duty(300)
                if duty==0:
                    motor1.duty(300)
                    motor2.duty(0)
                    motor3.duty(0)
                    motor4.duty(300)
        response = web_page()
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(response)
        client.close()
      except:
          pass
