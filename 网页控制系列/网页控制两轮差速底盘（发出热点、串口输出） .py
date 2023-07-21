#导入Pin模块
from machine import Pin
import time
from machine import PWM
import network
import socket

#定义LED控制对象
led1=Pin(6,Pin.OUT,Pin.PULL_DOWN)
 
duty=0
speed=0
turn=0
angular=400
linear=400

#WIFI连接
def wifi_connect():
    ap = network.WLAN(network.AP_IF)  # 指定用ap模式
    ap.active(True)                   # 启用wifi前需要先激活接口
    ap.config(essid="ESP32_Motor_Control")      # 设置热点名称
    ap.config(authmode=0)  # 设置认证模式
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
    .button{display: inline-block; background-color: #8080f0; border: none; 
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
  <h2>ESP32 Motor Control</h2> <p><a href="/?d1">linear: <strong>""" + str(speed) + """</strong></a></p>
        <p><a href="/?w10"><button class="button">-3.00</button></a>
        <a href="/?w11"><button class="button">-2.75</button></a>
        <a href="/?w12"><button class="button">-2.50</button></a>
        <a href="/?w13"><button class="button">-2.25</button></a>
        <a href="/?w14"><button class="button">-2.00</button></a>
        <a href="/?w15"><button class="button">-1.75</button></a>
        <a href="/?w16"><button class="button">-1.50</button></a>
        <a href="/?w17"><button class="button">-1.25</button></a>
        <a href="/?w18"><button class="button">-1.00</button></a>
        <a href="/?w19"><button class="button">-0.75</button></a>
        <a href="/?w1a"><button class="button">-0.50</button></a>
        <a href="/?w1b"><button class="button">-0.25</button></a>
        <a href="/?w1c"><button class="button">0.00</button></a>
        <a href="/?w1d"><button class="button">0.25</button></a>
        <a href="/?w1e"><button class="button">0.50</button></a>
        <a href="/?w1f"><button class="button">0.75</button></a>
        <a href="/?w1g"><button class="button">1.00</button></a>
        <a href="/?w1h"><button class="button">1.25</button></a>
        <a href="/?w1i"><button class="button">1.50</button></a>
        <a href="/?w1j"><button class="button">1.75</button></a>
        <a href="/?w1k"><button class="button">2.00</button></a>
        <a href="/?w1l"><button class="button">2.25</button></a>
        <a href="/?w1m"><button class="button">2.50</button></a>
        <a href="/?w1n"><button class="button">2.75</button></a>
        <a href="/?w1o"><button class="button">3.00</button></a></p>
        <p><a href="/?d2">angular: <strong>""" + str(turn) + """</strong></a></p>
        <p><a href="/?w20"><button class="button">-3.00</button></a>
        <a href="/?w21"><button class="button">-2.75</button></a>
        <a href="/?w22"><button class="button">-2.50</button></a>
        <a href="/?w23"><button class="button">-2.25</button></a>
        <a href="/?w24"><button class="button">-2.00</button></a>
        <a href="/?w25"><button class="button">-1.75</button></a>
        <a href="/?w26"><button class="button">-1.50</button></a>
        <a href="/?w27"><button class="button">-1.25</button></a>
        <a href="/?w28"><button class="button">-1.00</button></a>
        <a href="/?w29"><button class="button">-0.75</button></a>
        <a href="/?w2a"><button class="button">-0.50</button></a>
        <a href="/?w2b"><button class="button">-0.25</button></a>
        <a href="/?w2c"><button class="button">0.00</button></a>
        <a href="/?w2d"><button class="button">0.25</button></a>
        <a href="/?w2e"><button class="button">0.50</button></a>
        <a href="/?w2f"><button class="button">0.75</button></a>
        <a href="/?w2g"><button class="button">1.00</button></a>
        <a href="/?w2h"><button class="button">1.25</button></a>
        <a href="/?w2i"><button class="button">1.50</button></a>
        <a href="/?w2j"><button class="button">1.75</button></a>
        <a href="/?w2k"><button class="button">2.00</button></a>
        <a href="/?w2l"><button class="button">2.25</button></a>
        <a href="/?w2m"><button class="button">2.50</button></a>
        <a href="/?w2n"><button class="button">2.75</button></a>
        <a href="/?w2o"><button class="button">3.00</button></a></p>
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
        # recv表示接收，括号里是最大接收字节
        request = client.recv(1024)
        request = str(request)
        w10 = request.find('/?w10')
        w11 = request.find('/?w11')
        w12 = request.find('/?w12')
        w13 = request.find('/?w13')
        w14 = request.find('/?w14')
        w15 = request.find('/?w15')
        w16 = request.find('/?w16')
        w17 = request.find('/?w17')
        w18 = request.find('/?w18')
        w19 = request.find('/?w19')
        w1a = request.find('/?w1a')
        w1b = request.find('/?w1b')
        w1c = request.find('/?w1c')
        w1d = request.find('/?w1d')
        w1e = request.find('/?w1e')
        w1f = request.find('/?w1f')
        w1g = request.find('/?w1g')
        w1h = request.find('/?w1h')
        w1i = request.find('/?w1i')
        w1j = request.find('/?w1j')
        w1k = request.find('/?w1k')
        w1l = request.find('/?w1l')
        w1m = request.find('/?w1m')
        w1n = request.find('/?w1n')
        w1o = request.find('/?w1o')
        w20 = request.find('/?w20')
        w21 = request.find('/?w21')
        w22 = request.find('/?w22')
        w23 = request.find('/?w23')
        w24 = request.find('/?w24')
        w25 = request.find('/?w25')
        w26 = request.find('/?w26')
        w27 = request.find('/?w27')
        w28 = request.find('/?w28')
        w29 = request.find('/?w29')
        w2a = request.find('/?w2a')
        w2b = request.find('/?w2b')
        w2c = request.find('/?w2c')
        w2d = request.find('/?w2d')
        w2e = request.find('/?w2e')
        w2f = request.find('/?w2f')
        w2g = request.find('/?w2g')
        w2h = request.find('/?w2h')
        w2i = request.find('/?w2i')
        w2j = request.find('/?w2j')
        w2k = request.find('/?w2k')
        w2l = request.find('/?w2l')
        w2m = request.find('/?w2m')
        w2n = request.find('/?w2n')
        w2o = request.find('/?w2o')
        d1 = request.find('/?d1')
        d2 = request.find('/?d2')
        if d1 == 6:
            speed=0.00
            linear=400
            print(str(angular)+str(linear))
        if d2 == 6:
            turn=0.00
            angular=400
            print(str(angular)+str(linear))    
        if w10 == 6:
            speed=-3.00
            linear=100
            print(str(angular)+str(linear))
        if w11 == 6:
            speed=-2.75
            linear=125
            print(str(angular)+str(linear))   
        if w12 == 6:
            speed=-2.50
            linear=150
            print(str(angular)+str(linear))
        if w13 == 6:
            speed=-2.25
            linear=175
            print(str(angular)+str(linear))
        if w14 == 6:
            speed=-2.00
            linear=200
            print(str(angular)+str(linear))
        if w15 == 6:
            speed=-1.75
            linear=225
            print(str(angular)+str(linear))   
        if w16 == 6:
            speed=-1.50
            linear=250
            print(str(angular)+str(linear))
        if w17 == 6:
            speed=-1.25
            linear=275
            print(str(angular)+str(linear))
        if w18 == 6:
            speed=-1.00
            linear=300
            print(str(angular)+str(linear))
        if w19 == 6:
            speed=-0.75
            linear=325
            print(str(angular)+str(linear))   
        if w1a == 6:
            speed=-0.50
            linear=350
            print(str(angular)+str(linear))
        if w1b == 6:
            speed=-0.25
            linear=375
            print(str(angular)+str(linear))
        if w1c == 6:
            speed=0.00
            linear=400
            print(str(angular)+str(linear))
        if w1d == 6:
            speed=0.25
            linear=425
            print(str(angular)+str(linear))   
        if w1e == 6:
            speed=0.50
            linear=450
            print(str(angular)+str(linear))
        if w1f == 6:
            speed=0.75
            linear=475
            print(str(angular)+str(linear))
        if w1g == 6:
            speed=1.00
            linear=500
            print(str(angular)+str(linear))
        if w1h == 6:
            speed=1.25
            linear=525
            print(str(angular)+str(linear))   
        if w1i == 6:
            speed=1.50
            linear=550
            print(str(angular)+str(linear))
        if w1j == 6:
            speed=1.75
            linear=575
            print(str(angular)+str(linear))
        if w1k == 6:
            speed=2.00
            linear=600
            print(str(angular)+str(linear))
        if w1l == 6:
            speed=2.25
            linear=625
            print(str(angular)+str(linear))   
        if w1m == 6:
            speed=2.50
            linear=650
            print(str(angular)+str(linear))
        if w1n == 6:
            speed=2.75
            linear=675
            print(str(angular)+str(linear))
        if w1o == 6:
            speed=3.00
            linear=700
            print(str(angular)+str(linear))
        if w20 == 6:
            turn=-3.00
            angular=100
            print(str(angular)+str(linear))
        if w21 == 6:
            turn=-2.75
            angular=125
            print(str(angular)+str(linear))   
        if w22 == 6:
            turn=-2.50
            angular=150
            print(str(angular)+str(linear))
        if w23 == 6:
            turn=-2.25
            angular=175
            print(str(angular)+str(linear))
        if w24 == 6:
            turn=-2.00
            angular=200
            print(str(angular)+str(linear))
        if w25 == 6:
            turn=-1.75
            angular=225
            print(str(angular)+str(linear))   
        if w26 == 6:
            turn=-1.50
            angular=250
            print(str(angular)+str(linear))
        if w27 == 6:
            turn=-1.25
            angular=275
            print(str(angular)+str(linear))
        if w28 == 6:
            turn=-1.00
            angular=300
            print(str(angular)+str(linear))
        if w29 == 6:
            turn=-0.75
            angular=325
            print(str(angular)+str(linear))   
        if w2a == 6:
            turn=-0.50
            angular=350
            print(str(angular)+str(linear))
        if w2b == 6:
            turn=-0.25
            angular=375
            print(str(angular)+str(linear))
        if w2c == 6:
            turn=0.00
            angular=400
            print(str(angular)+str(linear))
        if w2d == 6:
            turn=0.25
            angular=425
            print(str(angular)+str(linear))   
        if w2e == 6:
            turn=0.50
            angular=450
            print(str(angular)+str(linear))
        if w2f == 6:
            turn=0.75
            angular=475
            print(str(angular)+str(linear))
        if w2g == 6:
            turn=1.00
            angular=500
            print(str(angular)+str(linear))
        if w2h == 6:
            turn=1.25
            angular=525
            print(str(angular)+str(linear))   
        if w2i == 6:
            turn=1.50
            angular=550
            print(str(angular)+str(linear))
        if w2j == 6:
            turn=1.75
            angular=575
            print(str(angular)+str(linear))
        if w2k == 6:
            turn=2.00
            angular=600
            print(str(angular)+str(linear))
        if w2l == 6:
            turn=2.25
            angular=625
            print(str(angular)+str(linear))   
        if w2m == 6:
            turn=2.50
            angular=650
            print(str(angular)+str(linear))
        if w2n == 6:
            turn=2.75
            angular=675
            print(str(angular)+str(linear))
        if w2o == 6:
            turn=3.00
            angular=700
            print(str(angular)+str(linear))    
        response = web_page()
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(response)
        client.close()
      except:
          pass
