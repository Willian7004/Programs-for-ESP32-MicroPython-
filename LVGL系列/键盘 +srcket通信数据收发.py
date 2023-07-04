import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
import network
import usocket

i=0
# ------------------------------ 屏幕初始化操作 --start------------------------
# 屏幕宽高
WIDTH = 240
HEIGHT = 320


# 创建显示屏对象
disp = ili9341(miso=19, mosi=23, clk=18, cs=5, dc=26, rst=27, power=14, backlight=-1, backlight_on=0, power_on=0, rot=0x80,
        spihost=VSPI_HOST, mhz=60, factor=16, hybrid=True, width=WIDTH, height=HEIGHT,
        invert=False, double_buffer=True, half_duplex=False, initialize=True)

# 创建触摸屏对象
touch = xpt2046(cs=25, spihost=VSPI_HOST, mosi=-1, miso=-1, clk=-1, cal_y0 = 423, cal_y1=3948)
# ------------------------------ 屏幕初始化操作 --stop------------------------


# 1. 创建显示screen对象。将需要显示的组件添加到这个screen才能显示
scr = lv.obj()  # scr====> screen 屏幕
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
scr = lv.scr_act()
scr.clean()

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
            #超时判断,15 秒没连接成功判定为超时
            if time.time()-start_time>15:
                print("WIFI Connect Timeout!")
                break
        return False
    else:
        print("network information:", wlan.ifconfig())
        return True
    
# 2. 封装要显示的组件
class MyWidget():
    
    def __init__(self, scr):
        
        # 创建文本框
        ta = lv.textarea(scr)
        ta.set_one_line(False)  # 关闭1行模式
        ta.set_size(240, 60)  # 设置宽高
        ta.align(lv.ALIGN.TOP_MID, 0, 30)  # 设置位置
        ta.add_event_cb(lambda e: self.textarea_event_handler(e, ta), lv.EVENT.READY, None)  # 添加回调函数
        ta.add_state(lv.STATE.FOCUSED)   # 设置光标

        # 定义数字键盘要显示的内容
        btnm_map = ["a", "b", "c","d", "e", "f", "\n",
                    "g", "h", "i","j", "k", "l", "\n",
                    "m", "n", "o","p", "q", "r", "\n",
                    "s", "t", "u","v", "w", "x", "\n",
                    "y", "z", "1","2", "3", "4", "\n",
                    "5", "6", "7","8", "9", "0", "\n",
                    ",", ".", "?","!",lv.SYMBOL.BACKSPACE, lv.SYMBOL.NEW_LINE, ""]

        # 按钮矩阵
        btnm = lv.btnmatrix(scr)
        btnm.set_size(240, 230)  # 设置宽高
        btnm.align(lv.ALIGN.BOTTOM_MID, 0, 0)  # 设置位置
        btnm.add_event_cb(lambda e: self.btnm_event_handler(e, ta), lv.EVENT.VALUE_CHANGED, None)
        btnm.clear_flag(lv.obj.FLAG.CLICK_FOCUSABLE)  # 设置为非活跃，即文本框中的光标一直聚焦
        btnm.set_map(btnm_map)  # 设置要显示的内容（数字键盘）
        
        # 设置有源蜂鸣器引脚
        self.p15 = Pin(15, Pin.OUT)
        self.p15.value(1)  # 不响
        
    def textarea_event_handler(self, e, ta):
        try:
            socket.send(ta.get_text()) 
        except:
            pass
    def btnm_event_handler(self, e, ta):
        obj = e.get_target()
        txt = obj.get_btn_text(obj.get_selected_btn())  # 获取被点击的按钮的内容，例如数字3
        if txt == lv.SYMBOL.BACKSPACE:  # 如果是退格键，那么就删除1个字符
            ta.del_char()
        elif txt == lv.SYMBOL.NEW_LINE:  # 如果是回车键，那么就触发事件
            lv.event_send(ta, lv.EVENT.READY, None)
        elif txt:
            ta.add_text(txt)  # 如果不是回车键，那么就将当前数字显示到文本框
            
btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
btn.set_size(240, 30)  # 设置按钮尺寸
btn.align(lv.ALIGN.TOP_MID,0,0)  # 置于屏幕顶部
label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
label.set_text("connecting...")  # 设置文字内容
label.center()  # 相对于父对象居中

while i<10 :
    i+=1
    if wifi_connect():
        socket=usocket.socket()  #创建socket连接
        addr=(dest_ip,dest_port)  #服务器IP地址和端口
        socket.connect(addr)
        print("Connected")
        i=10      
    
# 3. 创建要显示的组件
MyWidget(scr)
# 4. 显示screen对象中的内容
lv.scr_load(scr)
label.set_text('connected')
while True:
    try:
        text=socket.recv(128)  #单次最多接收128字节
        if text==None:
            pass
        else: 
            text=text.decode("utf-8")
            label.set_text(text)   
        time.sleep_ms(300)
    except:
        pass
    