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

with open('./1.jpg', 'rb') as f:
    png_data = f.read()
img = lv.img_dsc_t({"data_size": len(png_data),"data": png_data})
# 创建样式
img_style = lv.style_t()
img_style.init()
# 设置背景颜色，圆角
img_style.set_radius(5)
img_style.set_bg_opa(lv.OPA.COVER)
img_style.set_bg_color(lv.palette_lighten(lv.PALETTE.GREY, 3))
# 设置边框以及颜色
img_style.set_border_width(2)
img_style.set_border_color(lv.palette_main(lv.PALETTE.BLUE))
# 创建lvgl中的图片组件
obj = lv.img(scr)
# 添加图片数据
obj.set_src(img)
# 添加样式
obj.add_style(img_style, 0)
# 设置图片位置
obj.align(lv.ALIGN.CENTER,0,-80)  # 距屏幕中心偏移量
lv.scr_load(scr)

with open('./2.jpg', 'rb') as f:
    png_data = f.read()
img = lv.img_dsc_t({"data_size": len(png_data),"data": png_data})    
# 创建lvgl中的图片组件
obj = lv.img(scr)
# 添加图片数据
obj.set_src(img)
# 添加样式
img_style = lv.style_t()
img_style.init()
# 设置图片位置
obj.align(lv.ALIGN.CENTER,0,80)  # 距屏幕中心偏移量
lv.scr_load(scr)

from machine import WDT
wdt = WDT(timeout=1000)  # enable it with a timeout of 2s
while True:
    wdt.feed()
    time.sleep(0.8)
