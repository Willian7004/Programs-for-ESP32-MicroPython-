import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver


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


# 2. 封装要显示的组件
class Widget():
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
        print()
        self.label.set_text("%d%%" % current_value)


# 3. 创建要显示的组件
W1=Widget(scr,0,-80,120) #x轴偏移量，y轴偏移量，尺寸
W2=Widget(scr,0,80,120)

# 4. 显示screen对象中的内容
lv.scr_load(scr)


# ------------------------------ 看门狗，用来重启ESP32设备 --start------------------------
try:
    from machine import WDT
    wdt = WDT(timeout=1000)  # enable it with a timeout of 2s
    print("提示: 按下Ctrl+C结束程序")
    while True:
        wdt.feed()
        time.sleep(0.9)
except KeyboardInterrupt as ret:
    print("程序停止运行，ESP32已经重启...")
    time.sleep(10)
# ------------------------------ 看门狗，用来重启ESP32设备 --stop-------------------------

