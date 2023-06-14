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
        self.bar.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
    
    def set_temp(self, anim_obj, value):
        self.bar.set_value(value, lv.ANIM.ON)


# 3. 创建要显示的组件
Widget1=MyWidget(scr,0,0,20,200,800,600)  #x轴偏移量，y轴偏移量，宽度，高度，上升时间，下降时间
Widget2=MyWidget(scr,-50,0,20,150,1500,1500)
Widget3=MyWidget(scr,50,0,20,250,1000,600)

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

