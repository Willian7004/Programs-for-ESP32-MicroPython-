import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
import random


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

x1=0
x2=0
y1=0
y2=0
flag=0
# 2. 封装要显示的组件
class MyWidget():
    def __init__(self, scr,x1,x2,y1,y2):
        # 创建 线 对象
        obj_line = lv.line(scr)
        
        # 创建样式
        style = lv.style_t()
        style.init()
        style.set_line_color(lv.palette_main(lv.PALETTE.GREY))
        style.set_line_width(2)
        style.set_line_rounded(True)
        
        # 添加样式
        obj_line.add_style(style, 0)
            
        point =  [{"x": x1, "y": y1}, {"x": x2, "y": y2}]

        obj_line.set_points(point, len(point))

        obj_line.center()

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
        self.label.set_text("0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, 0)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        slider = evt.get_target()
        global x2
        x2=slider.get_value()
        # 修改label的值
        self.label.set_text(str(x2))
        
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
        self.label.set_text("0")  # 默认值
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, 0)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        slider = evt.get_target()
        global y2
        y2=slider.get_value()
        # 修改label的值
        self.label.set_text(str(slider.get_value()))
        
class CounterBtn():
    def __init__(self, scr,x,y,w,h): #x轴偏移量，y轴偏移量，宽度，高度
        self.cnt = 0
        btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
        # btn.set_pos(20, 10)  # 相对于屏幕左上角 x为20，y为10
        btn.set_size(w, h)  # 设置按钮的宽度为120, 高度为50
        btn.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)  # 设置按钮被按下后的回调函数
        label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
        label.set_text("draw")  # 设置文字内容
        label.center()  # 相对于父对象居中

    def btn_event_cb(self, evt):
        global flag
        code = evt.get_code()  # 获取点击事件类型码
        btn = evt.get_target()  # 获取被点击的对象，此时就是按钮
        if code == lv.EVENT.CLICKED:
            flag=1

        # Get the first child of the button which is the label and change its text
        label = btn.get_child(0)
        label.set_text("draw")  # 修改文字内容        
        
# 3. 创建要显示的组件
Widget1=Widget1(scr,-25,-135,160,0,240) #x轴偏移量，y轴偏移量，宽度，高度，最小值，最大值
Widget2=Widget2(scr,-25,-100,160,0,310)
counterBtn1 = CounterBtn(scr,90,-125,50,50) #x轴偏移量，y轴偏移量，宽度，高度

# 4. 显示screen对象中的内容
lv.scr_load(scr)

while True:
    time.sleep(0.5)
    if flag==1 :
        flag=0
        Widget=MyWidget(scr,x1,x2,y1,y2)
        x1=x2
        y1=y2
        lv.scr_load(scr)
