#导入Pin模块
from machine import Pin
import time
import network
import socket
from neopixel import NeoPixel
import _thread

led1=Pin(15,Pin.OUT)
# 五向导航按键，COM引脚接3.3V
key1 = Pin(21, Pin.IN, Pin.PULL_DOWN)
key2 = Pin(19, Pin.IN, Pin.PULL_DOWN)
key3 = Pin(18, Pin.IN, Pin.PULL_DOWN)
key4 = Pin(5, Pin.IN, Pin.PULL_DOWN)
key5 = Pin(17, Pin.IN, Pin.PULL_DOWN)
key6 = Pin(16, Pin.IN, Pin.PULL_DOWN)
 
pin=13
rgb_num=24
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

#连接的WIFI账号和密码
ssid = "Mercury_X30G"
password = "Xu3328313"

key_en=1
#按键扫描函数
def key_scan():
    global key_en
    if key_en==1 and (key1.value()==1 or key2.value()==1 or key3.value()==1 or key4.value()==1 or
                      key5.value()==1 or key6.value()==1  ):
        time.sleep_ms(10)
        key_en=0
        if key1.value()==1:
            return 1
        elif key2.value()==1:
            return 2
        elif key3.value()==1:
            return 3
        elif key4.value()==1:
            return 4
        elif key5.value()==1:
            return 5
        elif key6.value()==1:
            return 6
    elif (key1.value()==0 and key2.value()==0 and key3.value()==0 and key4.value()==0 and
          key5.value()==0 and key6.value()==0  ) :
        key_en=1
    return 0

brightness=6
delay=40
mode=1
def key_get(): #获取键值并改变变量的值
    global brightness
    global delay
    global mode
    key=key_scan()
    if key==1 and brightness<30 :
        brightness+=3
    elif key==2 and brightness>3 :
        brightness-=3
    elif key==3 and delay<90 :
        delay+=10
    elif key==4 and delay>10 :
        delay-=10
    elif key==5 and mode<2 :
        mode+=1
    elif key==6 and mode>0 :
        mode-=1     

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
    global brightness
    global mode
    global delay
  
    html = """<html><head> <title>ESP32 WS2812 Control</title> <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        h1{color: #0F3376; padding: 1vh;}p{font-size: 1rem;}.button{display: inline-block; background-color: #141414; border: none; 
        border-radius: 4px; color: white; padding: 8px 15px; text-decoration: none; font-size: 20px; margin: 2px; cursor: pointer;}
        .button2{background-color: #282828;}.button3{background-color: #3c3c3c;}.button4{background-color: #505050;}
        .button5{background-color: #646464;}.button6{background-color: #787878;}.button7{background-color: #8c8c8c;}
        .button8{background-color: #a0a0a0;}.button9{background-color: #b4b4b4;}.button10{background-color: #c8c8c8;}
        .button11{background-color: #f01010;}.button12{background-color: #10f010;}.button13{background-color: #1010f0;}
        .button14{background-color: #0000ff;}.button15{background-color: #0f0fe1;}.button16{background-color: #1e1ed2;}
        .button17{background-color: #2d2dc3;}.button18{background-color: #3c3cb4;}.button19{background-color: #4b4ba5;}
        .button20{background-color: #5a5a96;}.button21{background-color: #696987;}.button22{background-color: #787878;}
        a:link {text-decoration:none;}a:visited {text-decoration:none;}a:hover {text-decoration:none;}
        a:active {text-decoration:none;}  /* selected link */</style></head>
        <body> <h1>ESP32 WS2812 Control</h1> <p><a href="/?d1">Brightness: <strong>""" + str(brightness) + """</strong></a></p>
        <p><a href="/?b1"><button class="button">03</button></a><a href="/?b2"><button class="button button2">06</button></a>
        <a href="/?b3"><button class="button button3">09</button></a><a href="/?b4"><button class="button button4">12</button></a>
        <a href="/?b5"><button class="button button5">15</button></a><a href="/?b6"><button class="button button6">18</button></a>
        <a href="/?b7"><button class="button button7">21</button></a><a href="/?b8"><button class="button button8">24</button></a>
        <a href="/?b9"><button class="button button9">27</button></a><a href="/?b10"><button class="button button10">30</button></p></a>
        <p><a href="/?d2">Mode: <strong>""" + str(mode) + """</strong></a></p>
        <p><a href="/?b11"><button class="button button11">0</button></a>
        <a href="/?b12"><button class="button button12">1</button></a>
        <a href="/?b13"><button class="button button13">2</button></a></p>
        <p><a href="/?d3">Delay: <strong>""" + str(delay) + """</strong></a></p>
        <p><a href="/?b14"><button class="button button14">10</button></a><a href="/?b15"><button class="button button15">20</button></a>
        <a href="/?b16"><button class="button button16">30</button></a><a href="/?b17"><button class="button button17">40</button></a>
        <a href="/?b18"><button class="button button18">50</button></a><a href="/?b19"><button class="button button19">60</button></a>
        <a href="/?b20"><button class="button button20">70</button></a><a href="/?b21"><button class="button button21">80</button></a>
        <a href="/?b22"><button class="button button22">90</button></a></p></body></html>"""
    return html

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
        # 进入监听状态，等待别人链接过来，有两个返回值，
        #一个是对方的socket对象，一个是对方的ip以及端口
        client, addr = my_socket.accept()
        print('Got a connection from %s' % str(addr))
        # recv表示接收，括号里是最大接收字节
        request = client.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        b1 = request.find('/?b1')
        b2 = request.find('/?b2')
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
        b14 = request.find('/?b14')
        b15 = request.find('/?b15')
        b16 = request.find('/?b16')
        b17 = request.find('/?b17')
        b18 = request.find('/?b18')
        b19 = request.find('/?b19')
        b20 = request.find('/?b20')
        b21 = request.find('/?b21')
        b22 = request.find('/?b22')
        d1 = request.find('/?d1')
        d2 = request.find('/?d2')
        d3 = request.find('/?d3')
        if b1 == 6:
            brightness=3
        if b2 == 6:
            brightness=6
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
        if b14 == 6:
            delay=10
        if b15 == 6:
            delay=20
        if b16 == 6:
            delay=30
        if b17 == 6:
            delay=40
        if b18 == 6:
            delay=50
        if b19 == 6:
            delay=60
        if b20 == 6:
            delay=70
        if b21 == 6:
            delay=80
        if b22 == 6:
            delay=90
        if d1 == 6:
            brightness=6
        if d2 == 6:
            mode=1
        if d3 == 6:
            delay=40    
        response = web_page()
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(response)
        client.close()

def light(i1,i2):
    global brightness
    global mode
    global delay
    count=0
    count1=0
    count2=23
    while True:
        key_get()
        if count==23 :
            count=0
        if mode==0 : #关灯
            for i in range(rgb_num):
                rgb_led[i]=(0, 0, 0)
                rgb_led.write()
        if mode==1 : #非对称
            temp=0
            i=count
            count+=1
            r=8*brightness #红色渐变到绿色
            g=0
            while temp<8 :
                r-=brightness
                g+=brightness
                if i>23 :
                    i-=24
                rgb_led[i]=(r, g, 0)
                i+=1
                temp+=1
            temp=0
            g=8*brightness #绿色渐变到蓝色
            b=0
            while temp<8 :
                g-=brightness
                b+=brightness
                if i>23 :
                    i-=24
                rgb_led[i]=(0, g, b)
                i+=1
                temp+=1
            temp=0
            b=8*brightness #蓝色渐变到红色
            r=0
            while temp<8 :
                b-=brightness
                r+=brightness
                if i>23 :
                    i-=24
                rgb_led[i]=(r, 0, b)
                i+=1
                temp+=1
            rgb_led.write()    
            time.sleep_ms(delay)
        if count1==12 :
            count1=0
        if count2==11 :
            count2=23     
        if mode==2 : #对称
            temp=0  #前半部分
            i=count1
            count1+=1
            r=8*brightness #红色渐变到绿色
            g=0
            while temp<4 :
                r-=2*brightness
                g+=2*brightness
                if i>11 :
                    i-=12
                rgb_led[i]=(r, g, 0)
                i+=1
                temp+=1
            temp=0
            g=8*brightness #绿色渐变到蓝色
            b=0
            while temp<4 :
                g-=2*brightness
                b+=2*brightness
                if i>11 :
                    i-=12
                rgb_led[i]=(0, g, b)
                i+=1
                temp+=1
            temp=0
            b=8*brightness #蓝色渐变到红色
            r=0
            while temp<4 :
                b-=2*brightness
                r+=2*brightness
                if i>11 :
                    i-=12
                rgb_led[i]=(r, 0, b)
                i+=1
                temp+=1
            temp=0  #后半部分
            i=count2
            count2-=1
            r=8*brightness #红色渐变到绿色
            g=0
            while temp<4 :
                r-=2*brightness
                g+=2*brightness
                if i<12 :
                    i+=12
                rgb_led[i]=(r, g, 0)
                i-=1
                temp+=1
            temp=0
            g=8*brightness #绿色渐变到蓝色
            b=0
            while temp<4 :
                g-=2*brightness
                b+=2*brightness
                if i<12 :
                    i+=12
                rgb_led[i]=(0, g, b)
                i-=1
                temp+=1
            temp=0
            b=8*brightness #蓝色渐变到红色
            r=0
            while temp<4 :
                b-=2*brightness
                r+=2*brightness
                if i<12 :
                    i+=12
                rgb_led[i]=(r, 0, b)
                i-=1
                temp+=1    
            rgb_led.write()    
            time.sleep_ms(delay)

i1=0
i2=0
_thread.start_new_thread(server, (i1,i2))
_thread.start_new_thread(light, (i1, i2))