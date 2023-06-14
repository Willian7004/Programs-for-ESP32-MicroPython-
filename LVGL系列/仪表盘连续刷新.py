import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
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
        # 1. 创建仪表盘对象
        self.meter = lv.meter(scr)
        self.meter.center()  # 屏幕居中
        self.meter.set_size(200, 200)  # width: 200 height: 200
        
        # 2. 创建刻度线对象
        scale = self.meter.add_scale()
        # -------- 子刻度线 --------
        # 51:短线的个数
        # 2:短线宽度（单位像素）
        # 10:短线长度
        # 最后1个参数：颜色
        self.meter.set_scale_ticks(scale, 51, 2, 10, lv.palette_main(lv.PALETTE.GREY))
        
        # -------- 主刻度线 --------
        # 10: 多少个子刻度线显示1个主刻度线
        # 4: 宽度
        # 15: 长度
        # 下一个参数：颜色
        # 10: 文字与线的距离 10像素
        self.meter.set_scale_major_ticks(scale, 10, 4, 15, lv.color_black(), 10)

        # 3. 添加警示刻度线
        # 在起点添加蓝色弧
        blue_arc = self.meter.add_arc(scale, 2, lv.palette_main(lv.PALETTE.BLUE), 0)
        self.meter.set_indicator_start_value(blue_arc, 0)
        self.meter.set_indicator_end_value(blue_arc, 20)

        # 在刻度开始处使刻度线为蓝色
        blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
        self.meter.set_indicator_start_value(blue_arc_scale, 0)
        self.meter.set_indicator_end_value(blue_arc_scale, 20)

        # 在末端添加红色弧
        red_arc = self.meter.add_arc(scale, 2, lv.palette_main(lv.PALETTE.RED), 0)
        self.meter.set_indicator_start_value(red_arc, 80)
        self.meter.set_indicator_end_value(red_arc, 100)

        # 使刻度线在刻度末端变为红色
        red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
        self.meter.set_indicator_start_value(red_arc_scale, 80)
        self.meter.set_indicator_end_value(red_arc_scale, 100)


        # 4. 仪表指针
        # 4: 宽度
        # 下一参数：颜色
        # -10：指针与刻度线距离
        self.indic = self.meter.add_needle_line(scale, 4, lv.palette_main(lv.PALETTE.GREY), -10)
                      
        # 5. 创建动画对象
        a = lv.anim_t()
        a.init()
        a.set_var(self.indic)
        temp = self.timer_cb()
        a.set_values(0, temp)
        a.set_time(100)
        # a.set_repeat_delay(100)
        # a.set_playback_time(500)
        # a.set_playback_delay(100)
        # a.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        a.set_custom_exec_cb(self.set_value)
        lv.anim_t.start(a)
        
        # 6. 添加定时器
        lv.timer_create(self.timer_cb, 1000, None)  # 延时
        
    def set_value(self, anmi_obj, value):
        """动画回调函数"""
        self.meter.set_indicator_value(self.indic, value)
    
    def timer_cb(self, timer=None):
        """定时器回调函数"""
        ret=random.randint(0,100)
        self.meter.set_indicator_value(self.indic, ret)
        return ret
    

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
