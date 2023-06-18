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

PMW1=PWM(Pin(12),freq=1,duty=1023)
PMW2=PWM(Pin(13),freq=1,duty=1023)
PMW3=PWM(Pin(15),freq=1,duty=1023)

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
        freq2=slider.get_value()
        PMW2.freq(freq2)
        self.label.set_text(str(freq2))
        
class Widget3():
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
        freq3=slider.get_value()
        PMW3.freq(freq3)
        self.label.set_text(str(freq3))        

class Widget4():
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
        PMW1.duty(1000-duty)
        self.label.set_text("%d%%" % current_value)
        
class Widget5():
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
        PMW2.duty(1000-duty)
        self.label.set_text("%d%%" % current_value)
        
class Widget6():
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
        PMW3.duty(1000-duty)
        self.label.set_text("%d%%" % current_value)
        
# 3. 创建要显示的组件
Widget1=Widget1(scr,-55,-35,95,1,20) #x轴偏移量，y轴偏移量，宽度，高度，最小值，最大值
Widget2=Widget2(scr,55,45,95,1,20)
Widget3=Widget3(scr,-55,125,95,1,20)
Widget4=Widget4(scr,-55,-100,90) #x轴偏移量，y轴偏移量，尺寸
Widget5=Widget5(scr,55,-20,90)
Widget6=Widget6(scr,-55,60,90)
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