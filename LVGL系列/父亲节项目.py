import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046


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
scr = lv.obj()

slider=0
m=0
d=0
# 2. 封装的需要显示的按钮
class CounterBtn():
    def __init__(self, scr,x,y,w,h): #x轴偏移量，y轴偏移量，宽度，高度
        self.cnt = 0
        btn = lv.btn(scr)  # 将当前按钮与screen对象进行关联
        # btn.set_pos(20, 10)  # 相对于屏幕左上角 x为20，y为10
        btn.set_size(w, h)  # 设置按钮的宽度为120, 高度为50
        btn.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)  # 设置按钮被按下后的回调函数
        label = lv.label(btn)  # 在按钮上创建一个标签Label，用来显示文字用
        label.set_text(" ")  # 设置文字内容
        label.center()  # 相对于父对象居中

    def btn_event_cb(self, evt):
        global slider
        code = evt.get_code()  # 获取点击事件类型码
        btn = evt.get_target()  # 获取被点击的对象，此时就是按钮
        if code == lv.EVENT.CLICKED:
            self.cnt += 1

        # Get the first child of the button which is the label and change its text
        label = btn.get_child(0)
        if self.cnt == 1:
          label.set_text("Happy")  # 修改文字内容
        if self.cnt == 2:
          label.set_text("Happy Father's")  # 修改文字内容
        if self.cnt == 3:
          label.set_text("Happy Father's Day")  # 修改文字内容
          slider=1

class WidgetM():
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
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global m
        slider = evt.get_target()
        # 修改label的值
        m=slider.get_value()
        self.label.set_text(str(m))

class WidgetD():
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
        self.label.align_to(self.slider, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向上15像素 x不变

    def slider_event_cb(self, evt):
        global d
        slider = evt.get_target()
        # 修改label的值
        d=slider.get_value()
        self.label.set_text(str(d))
        
class MyWidget():
    def __init__(self, scr,x,y,w,h,t1,t2): #x轴偏移量，y轴偏移量，宽度，高度，上升时间，下降时间
        # 1. 创建进度条对象
        self.bar = lv.bar(scr)
        
        # 2. 创建样式对象
        style_indic = lv.style_t()
        style_indic.init()
        style_indic.set_bg_opa(lv.OPA.COVER)
        style_indic.set_bg_color(lv.palette_main(lv.PALETTE.RED))
        style_indic.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
        style_indic.set_bg_grad_dir(lv.GRAD_DIR.VER)

        # 3. 给进度条设置样式
        self.bar.add_style(style_indic, lv.PART.INDICATOR)
        self.bar.set_size(w, h)
        self.bar.set_range(-50,50)

        # 4. 创建动画对象
        anim_obj = lv.anim_t()
        anim_obj.init()
        anim_obj.set_var(self.bar)
        anim_obj.set_values(-50, 50)
        anim_obj.set_time(t1)  # 设置从当前效果到指定效果的过度时间
        anim_obj.set_playback_time(t2)  # 设置从指定效果到之前效果的过度时间
        anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
        anim_obj.set_custom_exec_cb(self.set_temp)  # 设置动画回调函数
        lv.anim_t.start(anim_obj)
        
        # 5. 进度条放到中间
        self.bar.align(lv.ALIGN.BOTTOM_MID, x, y)  # 设置位置
    
    def set_temp(self, anim_obj, value):
        self.bar.set_value(value, lv.ANIM.ON)        
        
# 3. 创建按钮
counterBtn = CounterBtn(scr,0,-20,200,50) #x轴偏移量，y轴偏移量，宽度，高度

# 4. 显示screen对象中的内容
lv.scr_load(scr)

while True :
        if slider==1 :
            Widget1=WidgetM(scr,0,-120,200,0,12) #x轴偏移量，y轴偏移量，宽度，高度，最小值，最大值
            Widget2=WidgetD(scr,0,-80,200,0,30)
            break
        time.sleep(0.5)

while True :
        if m==6 and d==18 :
           Widget1=MyWidget(scr,-90,-10,20,120,500,500) #x轴偏移量，y轴偏移量，宽度，高度，上升时间，下降时间
           Widget3=MyWidget(scr,-30,-10,20,120,500,500)  
           Widget5=MyWidget(scr,30,-10,20,120,500,500)
           Widget7=MyWidget(scr,90,-10,20,120,500,500)
           time.sleep(0.5)
           Widget2=MyWidget(scr,-60,-10,20,120,500,500)
           Widget4=MyWidget(scr,0,-10,20,120,500,500)
           Widget6=MyWidget(scr,60,-10,20,120,500,500)
           break
        time.sleep(0.5)
