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


# 2. 封装要显示的组件
class MyWidget():
    def __init__(self, scr):
        # 创建 线 对象
        obj_line = lv.line(scr)
        
        # 创建样式
        style = lv.style_t()
        style.init()
        style.set_line_color(lv.palette_main(lv.PALETTE.GREY))
        style.set_line_width(6)
        style.set_line_rounded(True)
        
        # 添加样式
        obj_line.add_style(style, 0)
        x1=random.randint(0,240)
        y1=random.randint(0,320)
        x2=random.randint(0,240)
        y2=random.randint(0,320)
        x3=random.randint(0,240)
        y3=random.randint(0,320)
        x4=random.randint(0,240)
        y4=random.randint(0,320)
        x5=random.randint(0,240)
        y5=random.randint(0,320)
        x6=random.randint(0,240)
        y6=random.randint(0,320)
        x7=random.randint(0,240)
        y7=random.randint(0,320)
        x8=random.randint(0,240)
        y8=random.randint(0,320)
        x9=random.randint(0,240)
        y9=random.randint(0,320)
        point =  [{"x": x1, "y": y1}, {"x": x2, "y": y2}, {"x": x3, "y":y3}, {"x": x4, "y":y4}, {"x": x5, "y":y5}, {"x": x6, "y":y6}, {"x": x7, "y":y7}, {"x": x8, "y":y8}, {"x": x9, "y":y9}]

        obj_line.set_points(point, len(point))

        obj_line.center()


# 3. 创建要显示的组件
MyWidget(scr)

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

