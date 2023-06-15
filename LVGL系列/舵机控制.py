import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
import onewire, ds18x20
from servo import Servo
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

servo1 = Servo(Pin(12))
servo2 = Servo(Pin(13))
servo3 = Servo(Pin(4))
servo4 = Servo(Pin(15))
servo5 = Servo(Pin(22))
servo6 = Servo(Pin(21))

angle1=0 #舵机角度
angle2=0
angle3=0
angle4=0
angle5=0
angle6=0

# 2. 封装要显示的组件
class Save1():
    
    def __init__(self, scr):
        # 创建开关按钮
        btn = lv.btn(lv.scr_act())

        # 添加回调函数
        btn.add_event_cb(self.open_or_close_led, lv.EVENT.ALL, None)

        # 简单布局
        btn.align(lv.ALIGN.CENTER, -90,-130)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)
        btn.set_height(lv.SIZE_CONTENT)

        # 创建label
        self.label = lv.label(btn)
        self.label.set_text("Save") 
        self.label.center()
        
        # 定义变量用来存储存取状态
        self.led_status = False
        
    def open_or_close_led(self, evt):
        global angle1
        global angle2
        global angle3
        global angle4
        global angle5
        global angle6
        code = evt.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            if self.led_status is False:
                save1=angle1
                save2=angle2
                save3=angle3
                save4=angle4
                save5=angle5
                save6=angle6
                self.label.set_text("Load") 
            else:
                angle1=save1
                servo1.write_angle(angle1)
                angle2=save2
                servo2.write_angle(angle2)
                angle3=save3
                servo3.write_angle(angle3)
                angle4=save4
                servo4.write_angle(angle4)
                angle5=save5
                servo5.write_angle(angle5)
                angle6=save6
                servo6.write_angle(angle6) 
                self.label.set_text("Save")
                
            self.led_status = not self.led_status

class Save2():
    
    def __init__(self, scr):
        # 创建开关按钮
        btn = lv.btn(lv.scr_act())

        # 添加回调函数
        btn.add_event_cb(self.open_or_close_led, lv.EVENT.ALL, None)

        # 简单布局
        btn.align(lv.ALIGN.CENTER,-30,-130)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)
        btn.set_height(lv.SIZE_CONTENT)

        # 创建label
        self.label = lv.label(btn)
        self.label.set_text("Save")
        self.label.center()
        
        # 定义变量用来存储存取状态
        self.led_status = False
        
    def open_or_close_led(self, evt):
        global angle1
        global angle2
        global angle3
        global angle4
        global angle5
        global angle6
        code = evt.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            if self.led_status is False:
                save1=angle1
                save2=angle2
                save3=angle3
                save4=angle4
                save5=angle5
                save6=angle6
                self.label.set_text("Load")
            else:
                angle1=save1
                servo1.write_angle(angle1)
                angle2=save2
                servo2.write_angle(angle2)
                angle3=save3
                servo3.write_angle(angle3)
                angle4=save4
                servo4.write_angle(angle4)
                angle5=save5
                servo5.write_angle(angle5)
                angle6=save6
                servo6.write_angle(angle6)
                self.label.set_text("Save")
                
            self.led_status = not self.led_status
            
class Save3():
    
    def __init__(self, scr):
        # 创建开关按钮
        btn = lv.btn(lv.scr_act())

        # 添加回调函数
        btn.add_event_cb(self.open_or_close_led, lv.EVENT.ALL, None)

        # 简单布局
        btn.align(lv.ALIGN.CENTER,30,-130)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)
        btn.set_height(lv.SIZE_CONTENT)

        # 创建label
        self.label = lv.label(btn)
        self.label.set_text("Save")
        self.label.center()
        
        # 定义变量用来存储存取状态
        self.led_status = False
        
    def open_or_close_led(self, evt):
        global angle1
        global angle2
        global angle3
        global angle4
        global angle5
        global angle6
        code = evt.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            if self.led_status is False:
                save1=angle1
                save2=angle2
                save3=angle3
                save4=angle4
                save5=angle5
                save6=angle6
                self.label.set_text("Load")
            else:
                angle1=save1
                servo1.write_angle(angle1)
                angle2=save2
                servo2.write_angle(angle2)
                angle3=save3
                servo3.write_angle(angle3)
                angle4=save4
                servo4.write_angle(angle4)
                angle5=save5
                servo5.write_angle(angle5)
                angle6=save6
                servo6.write_angle(angle6)
                self.label.set_text("Save")
                
            self.led_status = not self.led_status
            
class Save4():
    
    def __init__(self, scr):
        # 创建开关按钮
        btn = lv.btn(lv.scr_act())

        # 添加回调函数
        btn.add_event_cb(self.open_or_close_led, lv.EVENT.ALL, None)

        # 简单布局
        btn.align(lv.ALIGN.CENTER,90,-130)
        btn.add_flag(lv.obj.FLAG.CHECKABLE)
        btn.set_height(lv.SIZE_CONTENT)

        # 创建label
        self.label = lv.label(btn)
        self.label.set_text("Save")
        self.label.center()
        
        # 定义变量用来存储存取状态
        self.led_status = False
        
    def open_or_close_led(self, evt):
        global angle1
        global angle2
        global angle3
        global angle4
        global angle5
        global angle6
        code = evt.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            if self.led_status is False:
                save1=angle1
                save2=angle2
                save3=angle3
                save4=angle4
                save5=angle5
                save6=angle6
                self.label.set_text("Load")
            else:
                angle1=save1
                servo1.write_angle(angle1)
                angle2=save2
                servo2.write_angle(angle2)
                angle3=save3
                servo3.write_angle(angle3)
                angle4=save4
                servo4.write_angle(angle4)
                angle5=save5
                servo5.write_angle(angle5)
                angle6=save6
                servo6.write_angle(angle6)
                self.label.set_text("Save")
                
            self.led_status = not self.led_status
            
class Widget1():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(180)  # 设置滑块的宽度
        self.slider.set_range(0, 180)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,-70)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("Servo1: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变
        
    def slider_event_cb(self, evt):
        global angle1
        slider = evt.get_target()
        angle1=slider.get_value()
        servo1.write_angle(angle1) 
        # 修改label的值
        self.label.set_text("Servo1: "+str(angle1))

class Widget2():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(180)  # 设置滑块的宽度
        self.slider.set_range(0, 180)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,-30)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("Servo2: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global angle2
        slider = evt.get_target()
        angle2=slider.get_value()
        servo2.write_angle(angle2) 
        # 修改label的值
        self.label.set_text("Servo2: "+str(angle2))

class Widget3():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(180)  # 设置滑块的宽度
        self.slider.set_range(0, 180)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,10)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数
        
        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("Servo3: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global angle3
        slider = evt.get_target()
        angle3=slider.get_value()
        servo3.write_angle(angle3) 
        # 修改label的值
        self.label.set_text("Servo3: "+str(angle3))

class Widget4():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(180)  # 设置滑块的宽度
        self.slider.set_range(0, 180)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,50)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("Servo4: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变
        
    def slider_event_cb(self, evt):
        global angle4
        slider = evt.get_target()
        angle4=slider.get_value()
        servo4.write_angle(angle4) 
        # 修改label的值
        self.label.set_text("Servo4: "+str(angle4))

class Widget5():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(180)  # 设置滑块的宽度
        self.slider.set_range(0, 180)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,90)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("Servo5: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global angle5
        slider = evt.get_target()
        angle5=slider.get_value()
        servo5.write_angle(angle5) 
        # 修改label的值
        self.label.set_text("Servo5: "+str(angle5))

class Widget6():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(180)  # 设置滑块的宽度
        self.slider.set_range(0, 180)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,130)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数
        
        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("Servo6: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global angle6
        slider = evt.get_target()
        angle6=slider.get_value()
        servo6.write_angle(angle6) 
        # 修改label的值
        self.label.set_text("Servo6: "+str(angle6))
        
# 3. 创建要显示的组件
Save1(scr)
Save2(scr)
Save3(scr)
Save4(scr)
Widget1(scr)
Widget2(scr)
Widget3(scr)
Widget4(scr)
Widget5(scr)
Widget6(scr)

# 4. 显示screen对象中的内容
lv.scr_load(scr)

