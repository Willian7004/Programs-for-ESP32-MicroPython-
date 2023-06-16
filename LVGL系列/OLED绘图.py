import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
import onewire, ds18x20
from machine import SoftI2C
from ssd1306 import SSD1306_I2C  #I2C的oled选该方法

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

#创建软件I2C对象
i2c = SoftI2C(sda=Pin(2), scl=Pin(15))
#创建OLED对象，OLED分辨率、I2C接口
oled = SSD1306_I2C(128, 64, i2c)

X=0
Y=0
width=0
height=0
# 2. 封装要显示的组件
class CounterBtn1():
    def __init__(self, scr,x,y,w,h): #x轴偏移量，y轴偏移量，宽度，高度
        self.cnt = 0
        btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
        # btn.set_pos(20, 10)  # 相对于屏幕左上角 x为20，y为10
        btn.set_size(w, h)  # 设置按钮的宽度为120, 高度为50
        btn.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)  # 设置按钮被按下后的回调函数
        label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
        label.set_text("line")  # 设置文字内容
        label.center()  # 相对于父对象居中

    def btn_event_cb(self, evt):
        global X
        global Y
        global width
        global height
        code = evt.get_code()  # 获取点击事件类型码
        btn = evt.get_target()  # 获取被点击的对象，此时就是按钮
        if code == lv.EVENT.CLICKED:
            oled.line(X,Y,width,height,1)  #画指定坐标直线
            oled.show()  #执行显示
        # Get the first child of the button which is the label and change its text
        label = btn.get_child(0)
        label.set_text("line")  # 修改文字内容
        
class CounterBtn2():
    def __init__(self, scr,x,y,w,h): #x轴偏移量，y轴偏移量，宽度，高度
        self.cnt = 0
        btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
        # btn.set_pos(20, 10)  # 相对于屏幕左上角 x为20，y为10
        btn.set_size(w, h)  # 设置按钮的宽度为120, 高度为50
        btn.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)  # 设置按钮被按下后的回调函数
        label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
        label.set_text("rect")  # 设置文字内容
        label.center()  # 相对于父对象居中

    def btn_event_cb(self, evt):
        global X
        global Y
        global width
        global height
        code = evt.get_code()  # 获取点击事件类型码
        btn = evt.get_target()  # 获取被点击的对象，此时就是按钮
        if code == lv.EVENT.CLICKED:
            oled.rect(X,Y,width,height,1)  #画指定坐标直线
            oled.show()  #执行显示
        # Get the first child of the button which is the label and change its text
        label = btn.get_child(0)
        label.set_text("rect")  # 修改文字内容
        
class CounterBtn3():
    def __init__(self, scr,x,y,w,h): #x轴偏移量，y轴偏移量，宽度，高度
        self.cnt = 0
        btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
        # btn.set_pos(20, 10)  # 相对于屏幕左上角 x为20，y为10
        btn.set_size(w, h)  # 设置按钮的宽度为120, 高度为50
        btn.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)  # 设置按钮被按下后的回调函数
        label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
        label.set_text("fill_rect")  # 设置文字内容
        label.center()  # 相对于父对象居中

    def btn_event_cb(self, evt):
        global X
        global Y
        global width
        global height
        code = evt.get_code()  # 获取点击事件类型码
        btn = evt.get_target()  # 获取被点击的对象，此时就是按钮
        if code == lv.EVENT.CLICKED:
            oled.fill_rect(X,Y,width,height,1)  #画指定坐标直线
            oled.show()  #执行显示
        # Get the first child of the button which is the label and change its text
        label = btn.get_child(0)
        label.set_text("fill_rect")  # 修改文字内容
        
class CounterBtn4():
    def __init__(self, scr,x,y,w,h): #x轴偏移量，y轴偏移量，宽度，高度
        self.cnt = 0
        btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
        # btn.set_pos(20, 10)  # 相对于屏幕左上角 x为20，y为10
        btn.set_size(w, h)  # 设置按钮的宽度为120, 高度为50
        btn.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)  # 设置按钮被按下后的回调函数
        label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
        label.set_text("clear")  # 设置文字内容
        label.center()  # 相对于父对象居中

    def btn_event_cb(self, evt):
        global X
        global Y
        global width
        global height
        code = evt.get_code()  # 获取点击事件类型码
        btn = evt.get_target()  # 获取被点击的对象，此时就是按钮
        if code == lv.EVENT.CLICKED:
            oled.fill(0)  #清空屏幕
            oled.show()  #执行显示
        # Get the first child of the button which is the label and change its text
        label = btn.get_child(0)
        label.set_text("clear")  # 修改文字内容        
            
class Widget1():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(200)  # 设置滑块的宽度
        self.slider.set_range(0, 127)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,0)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("X: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变
        
    def slider_event_cb(self, evt):
        global X
        global Y
        global width
        global height
        slider = evt.get_target()
        X=slider.get_value()
        # 修改label的值
        self.label.set_text("X: "+str(X))

class Widget2():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(200)  # 设置滑块的宽度
        self.slider.set_range(0, 63)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,40)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数

        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("Y: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global X
        global Y
        global width
        global height
        slider = evt.get_target()
        Y=slider.get_value()
        # 修改label的值
        self.label.set_text("Y: "+str(Y))

class Widget3():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(200)  # 设置滑块的宽度
        self.slider.set_range(0, 127)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,80)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数
        
        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("width: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global X
        global Y
        global width
        global height
        slider = evt.get_target()
        width=slider.get_value()
        # 修改label的值
        self.label.set_text("width: "+str(width))
        
class Widget4():
    def __init__(self, scr):
        # 创建滑块slider组件
        self.slider = lv.slider(scr)
        self.slider.set_width(200)  # 设置滑块的宽度
        self.slider.set_range(0, 63)  # 默认值是0-100
        self.slider.align(lv.ALIGN.CENTER,0,120)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.slider.add_event_cb(self.slider_event_cb, lv.EVENT.VALUE_CHANGED, None)  # 添加回调函数
        
        # 创建一个标签label
        self.label = lv.label(scr)
        self.label.set_text("height: 0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global X
        global Y
        global width
        global height
        slider = evt.get_target()
        height=slider.get_value()
        # 修改label的值
        self.label.set_text("height: "+str(height))


# 3. 创建要显示的组件
counterBtn1 = CounterBtn1(scr,-60,-120,80,40) #x轴偏移量，y轴偏移量，宽度，高度
counterBtn2 = CounterBtn2(scr,60,-120,80,40)
counterBtn3 = CounterBtn3(scr,-60,-60,80,40)
counterBtn4 = CounterBtn4(scr,60,-60,80,40)
Widget1(scr)
Widget2(scr)
Widget3(scr)
Widget4(scr)

# 4. 显示screen对象中的内容
lv.scr_load(scr)

