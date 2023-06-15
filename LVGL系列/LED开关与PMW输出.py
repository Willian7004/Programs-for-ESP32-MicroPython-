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

PMW1=PWM(Pin(12),freq=4000,duty=1023)
PMW2=PWM(Pin(13),freq=4000,duty=1023)
PMW3=PWM(Pin(15),freq=4000,duty=1023)

# 2. 封装要显示的组件
class LED1():
    
    def __init__(self, scr):
        # 创建开关按钮
        btn = lv.btn(lv.scr_act())

        # 添加回调函数
        btn.add_event_cb(self.open_or_close_led, lv.EVENT.ALL, None)

        # 简单布局
        btn.align(lv.ALIGN.CENTER, -55,-130)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)
        btn.set_height(lv.SIZE_CONTENT)

        # 创建label
        self.label = lv.label(btn)
        self.label.set_text("LED1 ON")
        self.label.center()
        
        # 创建LED对应引脚对象
        self.led = Pin(2, Pin.OUT)
        self.led.value(0)  # 默认不亮
        # 定义变量用来存储led的亮灭状态
        self.led_status = False
        
    def open_or_close_led(self, evt):
        code = evt.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            if self.led_status is False:
                self.led.value(1)
                self.label.set_text("LED1 OFF")
            else:
                self.led.value(0)
                self.label.set_text("LED1 ON")
                
            self.led_status = not self.led_status

class LED2():
    
    def __init__(self, scr):
        # 创建开关按钮
        btn = lv.btn(lv.scr_act())

        # 添加回调函数
        btn.add_event_cb(self.open_or_close_led, lv.EVENT.ALL, None)

        # 简单布局
        btn.align(lv.ALIGN.CENTER,55,-130)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)
        btn.set_height(lv.SIZE_CONTENT)

        # 创建label
        self.label = lv.label(btn)
        self.label.set_text("LED2 ON")
        self.label.center()
        
        # 创建LED对应引脚对象
        self.led = Pin(4, Pin.OUT)
        self.led.value(1)  # 默认不亮
        # 定义变量用来存储led的亮灭状态
        self.led_status = False
        
    def open_or_close_led(self, evt):
        code = evt.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            if self.led_status is False:
                self.led.value(0)
                self.label.set_text("LED2 OFF")
            else:
                self.led.value(1)
                self.label.set_text("LED2 ON")
                
            self.led_status = not self.led_status
            
class LED3():
    
    def __init__(self, scr):
        # 创建开关按钮
        btn = lv.btn(lv.scr_act())

        # 添加回调函数
        btn.add_event_cb(self.open_or_close_led, lv.EVENT.ALL, None)

        # 简单布局
        btn.align(lv.ALIGN.CENTER,-55,-80)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)
        btn.set_height(lv.SIZE_CONTENT)

        # 创建label
        self.label = lv.label(btn)
        self.label.set_text("LED3 ON")
        self.label.center()
        
        # 创建LED对应引脚对象
        self.led = Pin(21, Pin.OUT)
        self.led.value(1)  # 默认不亮
        # 定义变量用来存储led的亮灭状态
        self.led_status = False
        
    def open_or_close_led(self, evt):
        code = evt.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            if self.led_status is False:
                self.led.value(0)
                self.label.set_text("LED3 OFF")
            else:
                self.led.value(1)
                self.label.set_text("LED3 ON")
                
            self.led_status = not self.led_status
            
class LED4():
    
    def __init__(self, scr):
        # 创建开关按钮
        btn = lv.btn(lv.scr_act())

        # 添加回调函数
        btn.add_event_cb(self.open_or_close_led, lv.EVENT.ALL, None)

        # 简单布局
        btn.align(lv.ALIGN.CENTER,55,-80)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)
        btn.set_height(lv.SIZE_CONTENT)

        # 创建label
        self.label = lv.label(btn)
        self.label.set_text("LED4 ON")
        self.label.center()
        
        # 创建LED对应引脚对象
        self.led = Pin(22, Pin.OUT)
        self.led.value(1)  # 默认不亮
        # 定义变量用来存储led的亮灭状态
        self.led_status = False
        
    def open_or_close_led(self, evt):
        code = evt.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            if self.led_status is False:
                self.led.value(0)
                self.label.set_text("LED4 OFF")
            else:
                self.led.value(1)
                self.label.set_text("LED4 ON")
                
            self.led_status = not self.led_status
            
class Widget1():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(200)  # 设置滑块的宽度
        self.slider.set_range(0, 1023)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,0)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("PMW1: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -15)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变
        
    def slider_event_cb(self, evt):
        slider = evt.get_target()
        duty_value1=slider.get_value()
        PMW1.duty(1023-duty_value1)
        # 修改label的值
        self.label.set_text("PMW1: "+str(duty_value1))

class Widget2():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(200)  # 设置滑块的宽度
        self.slider.set_range(0, 1023)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,50)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("PMW2: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -15)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        slider = evt.get_target()
        duty_value2=slider.get_value()
        PMW2.duty(1023-duty_value2)
        # 修改label的值
        self.label.set_text("PMW2: "+str(duty_value2))

class Widget3():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(200)  # 设置滑块的宽度
        self.slider.set_range(0, 1023)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,100)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数
        
        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("PMW3: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -15)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        slider = evt.get_target()
        duty_value3=slider.get_value()
        PMW3.duty(1023-duty_value3)
        # 修改label的值
        self.label.set_text("PMW3: "+str(duty_value3))


# 3. 创建要显示的组件
LED1(scr)
LED2(scr)
LED3(scr)
LED4(scr)
Widget1(scr)
Widget2(scr)
Widget3(scr)

# 4. 显示screen对象中的内容
lv.scr_load(scr)

