import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
import onewire, ds18x20
from machine import PWM

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

PMW1=PWM(Pin(2),freq=4000,duty=0)

class Widget1():
    def __init__(self, scr,x,y,w,r1,r2): #x轴偏移量，y轴偏移量，宽度，高度，最小值，最大值
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(w)  # 设置滑块的宽度
        self.slider.set_range(r1, r2)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("1")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        slider = evt.get_target()
        # 修改label的值
        freq1=slider.get_value()
        PMW1.freq(freq1)
        self.label.set_text(str(freq1))
        
       

class Widget2():
    def __init__(self, scr,x,y,s):#x轴偏移量，y轴偏移量，尺寸
        # 创建圆弧对象
        arc = lv.arc(scr)
        # 设置角度
        arc.set_end_angle(135)  # 角度是 顺时针方向
        # 设置宽高
        arc.set_size(s, s)
        # 设置事件处理回调函数
        arc.add_event_cb(self.event_cb, lv.EVENT.VALUE_CHANGED, None)
        arc.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        
        # 创建文本
        self.label = lv.label(scr)
        self.label.set_text("0%")  # 设置文字内容
        # 居中显示
        self.label.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
    
    def event_cb(self, evt):
        arc = evt.get_target()
        current_value = arc.get_value()
        duty=current_value*10
        PMW1.duty(duty)
        self.label.set_text("%d%%" % current_value)
        
class CounterBtn():
    def __init__(self, scr,x,y,w,h): #x轴偏移量，y轴偏移量，宽度，高度
        self.cnt = 0
        btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
        # btn.set_pos(20, 10)  # 相对于屏幕左上角 x为20，y为10
        btn.set_size(w, h)  # 设置按钮的宽度为120, 高度为50
        btn.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)  # 设置按钮被按下后的回调函数
        label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
        label.set_text("always on")  # 设置文字内容
        label.center()  # 相对于父对象居中

    def btn_event_cb(self, evt):
        code = evt.get_code()  # 获取点击事件类型码
        btn = evt.get_target()  # 获取被点击的对象，此时就是按钮
        if code == lv.EVENT.CLICKED:
            self.cnt += 1
        if self.cnt==1:
            PMW1.freq(4000)
            self.cnt=0
        # Get the first child of the button which is the label and change its text
        label = btn.get_child(0)
        label.set_text("always on")  # 修改文字内容
        
# 3. 创建要显示的组件
Widget1=Widget1(scr,0,50,170,1,20) #x轴偏移量，y轴偏移量，宽度，高度，最小值，最大值
Widget2=Widget2(scr,0, -60,150) #x轴偏移量，y轴偏移量，尺寸
counterBtn= CounterBtn(scr,0,110,150,50) #x轴偏移量，y轴偏移量，宽度，高度
# 4. 显示screen对象中的内容
lv.scr_load(scr)

# ------------------------------ 看门狗，用来重启ESP32设备 --start------------------------
try:
    from machine import WDT
    wdt = WDT(timeout=2000)  # enable it with a timeout of 2s
    print("提示: 按下Ctrl+C结束程序")
    while True:
        wdt.feed()
        time.sleep(0.9)
except KeyboardInterrupt as ret:
    print("程序停止运行，ESP32已经重启...")
    time.sleep(10)
# ------------------------------ 看门狗，用来重启ESP32设备 --stop-------------------------