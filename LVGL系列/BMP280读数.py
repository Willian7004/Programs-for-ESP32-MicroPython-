import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
from machine import ADC
from machine import SoftI2C
import bmp280

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
#定义ADC控制对象
adc1=ADC(Pin(32))
adc1.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc2=ADC(Pin(33))
adc2.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc3=ADC(Pin(34))
adc3.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
adc4=ADC(Pin(35))
adc4.atten(ADC.ATTN_11DB)  #开启衰减，量程增大到3.3V
#初始化BMP280，定义第二个I2C接口i2c2用于连接BMP280
i2c2 = SoftI2C(sda=Pin(22), scl=Pin(21))
BMP = bmp280.BMP280(i2c2)


# 1. 创建显示screen对象。将需要显示的组件添加到这个screen才能显示
scr = lv.obj()  # scr====> screen 屏幕
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
scr = lv.scr_act()
scr.clean()


# 2. 封装要显示的组件
class Widget1():
    def __init__(self, scr,s,x,y,r1,r2,v1,v2): #尺寸，x轴偏移量，y轴偏移量，动画起始值，动画结束值，开始处蓝色区域最大值，结尾处红色区域最小值
        # 1. 创建仪表盘对象
        self.meter = lv.meter(scr)
        self.meter.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.meter.set_size(s, s)  # width: s height: s

        # 2. 创建刻度线对象
        scale = self.meter.add_scale()
        # -------- 子刻度线 --------
        # 51:短线的个数
        # 1:短线宽度（单位像素）
        # 7:短线长度
        # 最后1个参数：颜色
        self.meter.set_scale_ticks(scale, 101, 1, 10, lv.palette_main(lv.PALETTE.GREY))
        # -------- 主刻度线 --------
        # 10: 多少个子刻度线显示1个主刻度线
        # 2: 宽度
        # 10: 长度
        # 下一个参数：颜色
        # 10: 文字与线的距离 10像素
        self.meter.set_scale_major_ticks(scale, 5, 2, 15, lv.color_black(), 5)

        # 3. 添加警示刻度线
        # 在起点添加蓝色弧
        blue_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.BLUE), 0)
        self.meter.set_indicator_start_value(blue_arc, r1)
        self.meter.set_indicator_end_value(blue_arc, v1)

        # 在刻度开始处使刻度线为蓝色
        blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
        self.meter.set_indicator_start_value(blue_arc_scale, r1)
        self.meter.set_indicator_end_value(blue_arc_scale, v1)

        # 在末端添加红色弧
        red_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.RED), 0)
        self.meter.set_indicator_start_value(red_arc, v2)
        self.meter.set_indicator_end_value(red_arc, r2)

        # 使刻度线在刻度末端变为红色
        red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
        self.meter.set_indicator_start_value(red_arc_scale, v2)
        self.meter.set_indicator_end_value(red_arc_scale, r2)

        # 4. 仪表指针
        # 4: 宽度
        # 下一参数：颜色
        # -10：指针与刻度线距离
        self.indic = self.meter.add_needle_line(scale, 2, lv.palette_main(lv.PALETTE.GREY), -5)
        
        # 5. 创建动画对象
        a = lv.anim_t()
        a.init()
        a.set_var(self.indic)
        temp = self.timer_cb()
        a.set_values(0, temp)
        a.set_time(200)
        # a.set_repeat_delay(100)
        # a.set_playback_time(200)
        # a.set_playback_delay(100)
        # a.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        a.set_custom_exec_cb(self.set_value)
        lv.anim_t.start(a)                

        # 6. 添加定时器
        lv.timer_create(self.timer_cb, 200, None)  # 延时
        
    def set_value(self, anmi_obj, value):
        """动画回调函数"""
        self.meter.set_indicator_value(self.indic, value)
    
    def timer_cb(self, timer=None):
        """定时器回调函数"""
        ret=round(BMP.getTemp()/1)
        self.meter.set_indicator_value(self.indic, ret)
        return ret
    
class Widget2():
    def __init__(self, scr,s,x,y,r1,r2,v1,v2): #尺寸，x轴偏移量，y轴偏移量，动画起始值，动画结束值，开始处蓝色区域最大值，结尾处红色区域最小值
        # 1. 创建仪表盘对象
        self.meter = lv.meter(scr)
        self.meter.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.meter.set_size(s, s)  # width: s height: s

        # 2. 创建刻度线对象
        scale = self.meter.add_scale()
        # -------- 子刻度线 --------
        # 51:短线的个数
        # 1:短线宽度（单位像素）
        # 7:短线长度
        # 最后1个参数：颜色
        self.meter.set_scale_ticks(scale, 11, 1, 7, lv.palette_main(lv.PALETTE.GREY))
        # -------- 主刻度线 --------
        # 10: 多少个子刻度线显示1个主刻度线
        # 2: 宽度
        # 10: 长度
        # 下一个参数：颜色
        # 10: 文字与线的距离 10像素
        self.meter.set_scale_major_ticks(scale, 5, 2, 10, lv.color_black(), 5)

        # 3. 添加警示刻度线
        # 在起点添加蓝色弧
        blue_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.BLUE), 0)
        self.meter.set_indicator_start_value(blue_arc, r1)
        self.meter.set_indicator_end_value(blue_arc, v1)

        # 在刻度开始处使刻度线为蓝色
        blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
        self.meter.set_indicator_start_value(blue_arc_scale, r1)
        self.meter.set_indicator_end_value(blue_arc_scale, v1)

        # 在末端添加红色弧
        red_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.RED), 0)
        self.meter.set_indicator_start_value(red_arc, v2)
        self.meter.set_indicator_end_value(red_arc, r2)

        # 使刻度线在刻度末端变为红色
        red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
        self.meter.set_indicator_start_value(red_arc_scale, v2)
        self.meter.set_indicator_end_value(red_arc_scale, r2)

        # 4. 仪表指针
        # 4: 宽度
        # 下一参数：颜色
        # -10：指针与刻度线距离
        self.indic = self.meter.add_needle_line(scale, 2, lv.palette_main(lv.PALETTE.GREY), -5)
        
        # 5. 创建动画对象
        a = lv.anim_t()
        a.init()
        a.set_var(self.indic)
        temp = self.timer_cb()
        a.set_values(0, temp)
        a.set_time(200)
        # a.set_repeat_delay(100)
        # a.set_playback_time(200)
        # a.set_playback_delay(100)
        # a.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        a.set_custom_exec_cb(self.set_value)
        lv.anim_t.start(a)
        
        # 6. 添加定时器
        lv.timer_create(self.timer_cb, 200, None)  # 延时
        
    def set_value(self, anmi_obj, value):
        """动画回调函数"""
        self.meter.set_indicator_value(self.indic, value)
    
    def timer_cb(self, timer=None):
        """定时器回调函数"""
        ret=round(BMP.getPress()/10000)-1
        ret*=10
        self.meter.set_indicator_value(self.indic, ret)
        return ret
    
class Widget3():
    def __init__(self, scr,s,x,y,r1,r2,v1,v2): #尺寸，x轴偏移量，y轴偏移量，动画起始值，动画结束值，开始处蓝色区域最大值，结尾处红色区域最小值
        # 1. 创建仪表盘对象
        self.meter = lv.meter(scr)
        self.meter.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.meter.set_size(s, s)  # width: s height: s

        # 2. 创建刻度线对象
        scale = self.meter.add_scale()
        # -------- 子刻度线 --------
        # 51:短线的个数
        # 1:短线宽度（单位像素）
        # 7:短线长度
        # 最后1个参数：颜色
        self.meter.set_scale_ticks(scale, 11, 1, 7, lv.palette_main(lv.PALETTE.GREY))
        # -------- 主刻度线 --------
        # 10: 多少个子刻度线显示1个主刻度线
        # 2: 宽度
        # 10: 长度
        # 下一个参数：颜色
        # 10: 文字与线的距离 10像素
        self.meter.set_scale_major_ticks(scale, 5, 2, 10, lv.color_black(), 5)

        # 3. 添加警示刻度线
        # 在起点添加蓝色弧
        blue_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.BLUE), 0)
        self.meter.set_indicator_start_value(blue_arc, r1)
        self.meter.set_indicator_end_value(blue_arc, v1)

        # 在刻度开始处使刻度线为蓝色
        blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
        self.meter.set_indicator_start_value(blue_arc_scale, r1)
        self.meter.set_indicator_end_value(blue_arc_scale, v1)

        # 在末端添加红色弧
        red_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.RED), 0)
        self.meter.set_indicator_start_value(red_arc, v2)
        self.meter.set_indicator_end_value(red_arc, r2)

        # 使刻度线在刻度末端变为红色
        red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
        self.meter.set_indicator_start_value(red_arc_scale, v2)
        self.meter.set_indicator_end_value(red_arc_scale, r2)

        # 4. 仪表指针
        # 4: 宽度
        # 下一参数：颜色
        # -10：指针与刻度线距离
        self.indic = self.meter.add_needle_line(scale, 2, lv.palette_main(lv.PALETTE.GREY), -5)
        
        # 5. 创建动画对象
        a = lv.anim_t()
        a.init()
        a.set_var(self.indic)
        temp = self.timer_cb()
        a.set_values(0, temp)
        a.set_time(200)
        # a.set_repeat_delay(100)
        # a.set_playback_time(200)
        # a.set_playback_delay(100)
        # a.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        a.set_custom_exec_cb(self.set_value)
        lv.anim_t.start(a)
        
        # 6. 添加定时器
        lv.timer_create(self.timer_cb, 200, None)  # 延时
        
    def set_value(self, anmi_obj, value):
        """动画回调函数"""
        self.meter.set_indicator_value(self.indic, value)
    
    def timer_cb(self, timer=None):
        """定时器回调函数"""
        ret=round(BMP.getPress()/1000)
        ret=ret%10
        ret*=10
        self.meter.set_indicator_value(self.indic, ret)
        return ret
    
class Widget4():
    def __init__(self, scr,s,x,y,r1,r2,v1,v2): #尺寸，x轴偏移量，y轴偏移量，动画起始值，动画结束值，开始处蓝色区域最大值，结尾处红色区域最小值
        # 1. 创建仪表盘对象
        self.meter = lv.meter(scr)
        self.meter.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.meter.set_size(s, s)  # width: s height: s

        # 2. 创建刻度线对象
        scale = self.meter.add_scale()
        # -------- 子刻度线 --------
        # 51:短线的个数
        # 1:短线宽度（单位像素）
        # 7:短线长度
        # 最后1个参数：颜色
        self.meter.set_scale_ticks(scale, 11, 1, 7, lv.palette_main(lv.PALETTE.GREY))
        # -------- 主刻度线 --------
        # 10: 多少个子刻度线显示1个主刻度线
        # 2: 宽度
        # 10: 长度
        # 下一个参数：颜色
        # 10: 文字与线的距离 10像素
        self.meter.set_scale_major_ticks(scale, 5, 2, 10, lv.color_black(), 5)

        # 3. 添加警示刻度线
        # 在起点添加蓝色弧
        blue_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.BLUE), 0)
        self.meter.set_indicator_start_value(blue_arc, r1)
        self.meter.set_indicator_end_value(blue_arc, v1)

        # 在刻度开始处使刻度线为蓝色
        blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
        self.meter.set_indicator_start_value(blue_arc_scale, r1)
        self.meter.set_indicator_end_value(blue_arc_scale, v1)

        # 在末端添加红色弧
        red_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.RED), 0)
        self.meter.set_indicator_start_value(red_arc, v2)
        self.meter.set_indicator_end_value(red_arc, r2)

        # 使刻度线在刻度末端变为红色
        red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
        self.meter.set_indicator_start_value(red_arc_scale, v2)
        self.meter.set_indicator_end_value(red_arc_scale, r2)

        # 4. 仪表指针
        # 4: 宽度
        # 下一参数：颜色
        # -10：指针与刻度线距离
        self.indic = self.meter.add_needle_line(scale, 2, lv.palette_main(lv.PALETTE.GREY), -5)
        
        # 5. 创建动画对象
        a = lv.anim_t()
        a.init()
        a.set_var(self.indic)
        temp = self.timer_cb()
        a.set_values(0, temp)
        a.set_time(200)
        # a.set_repeat_delay(100)
        # a.set_playback_time(200)
        # a.set_playback_delay(100)
        # a.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        a.set_custom_exec_cb(self.set_value)
        lv.anim_t.start(a)
        
        # 6. 添加定时器
        lv.timer_create(self.timer_cb, 200, None)  # 延时
        
    def set_value(self, anmi_obj, value):
        """动画回调函数"""
        self.meter.set_indicator_value(self.indic, value)
    
    def timer_cb(self, timer=None):
        """定时器回调函数"""
        ret=round(BMP.getPress()/100)
        ret=ret%10
        ret*=10
        self.meter.set_indicator_value(self.indic, ret)
        return ret    
       
class Widget5():
    def __init__(self, scr,s,x,y,r1,r2,v1,v2): #尺寸，x轴偏移量，y轴偏移量，动画起始值，动画结束值，开始处蓝色区域最大值，结尾处红色区域最小值
        # 1. 创建仪表盘对象
        self.meter = lv.meter(scr)
        self.meter.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.meter.set_size(s, s)  # width: s height: s

        # 2. 创建刻度线对象
        scale = self.meter.add_scale()
        # -------- 子刻度线 --------
        # 51:短线的个数
        # 1:短线宽度（单位像素）
        # 7:短线长度
        # 最后1个参数：颜色
        self.meter.set_scale_ticks(scale, 11, 1, 7, lv.palette_main(lv.PALETTE.GREY))
        # -------- 主刻度线 --------
        # 10: 多少个子刻度线显示1个主刻度线
        # 2: 宽度
        # 10: 长度
        # 下一个参数：颜色
        # 10: 文字与线的距离 10像素
        self.meter.set_scale_major_ticks(scale, 5, 2, 10, lv.color_black(), 5)

        # 3. 添加警示刻度线
        # 在起点添加蓝色弧
        blue_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.BLUE), 0)
        self.meter.set_indicator_start_value(blue_arc, r1)
        self.meter.set_indicator_end_value(blue_arc, v1)

        # 在刻度开始处使刻度线为蓝色
        blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
        self.meter.set_indicator_start_value(blue_arc_scale, r1)
        self.meter.set_indicator_end_value(blue_arc_scale, v1)

        # 在末端添加红色弧
        red_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.RED), 0)
        self.meter.set_indicator_start_value(red_arc, v2)
        self.meter.set_indicator_end_value(red_arc, r2)

        # 使刻度线在刻度末端变为红色
        red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
        self.meter.set_indicator_start_value(red_arc_scale, v2)
        self.meter.set_indicator_end_value(red_arc_scale, r2)

        # 4. 仪表指针
        # 4: 宽度
        # 下一参数：颜色
        # -10：指针与刻度线距离
        self.indic = self.meter.add_needle_line(scale, 2, lv.palette_main(lv.PALETTE.GREY), -5)
        
        # 5. 创建动画对象
        a = lv.anim_t()
        a.init()
        a.set_var(self.indic)
        temp = self.timer_cb()
        a.set_values(0, temp)
        a.set_time(200)
        # a.set_repeat_delay(100)
        # a.set_playback_time(200)
        # a.set_playback_delay(100)
        # a.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        a.set_custom_exec_cb(self.set_value)
        lv.anim_t.start(a)

        # 6. 添加定时器
        lv.timer_create(self.timer_cb, 200, None)  # 延时
        
    def set_value(self, anmi_obj, value):
        """动画回调函数"""
        self.meter.set_indicator_value(self.indic, value)
    
    def timer_cb(self, timer=None):
        """定时器回调函数"""
        ret=round(BMP.getPress()/10)
        ret=ret%10
        ret*=10
        self.meter.set_indicator_value(self.indic, ret)
        return ret
    
class Widget6():
    def __init__(self, scr,s,x,y,r1,r2,v1,v2): #尺寸，x轴偏移量，y轴偏移量，动画起始值，动画结束值，开始处蓝色区域最大值，结尾处红色区域最小值
        # 1. 创建仪表盘对象
        self.meter = lv.meter(scr)
        self.meter.align(lv.ALIGN.CENTER,x,y)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
        self.meter.set_size(s, s)  # width: s height: s

        # 2. 创建刻度线对象
        scale = self.meter.add_scale()
        # -------- 子刻度线 --------
        # 51:短线的个数
        # 1:短线宽度（单位像素）
        # 7:短线长度
        # 最后1个参数：颜色
        self.meter.set_scale_ticks(scale, 11, 1, 7, lv.palette_main(lv.PALETTE.GREY))
        # -------- 主刻度线 --------
        # 10: 多少个子刻度线显示1个主刻度线
        # 2: 宽度
        # 10: 长度
        # 下一个参数：颜色
        # 10: 文字与线的距离 10像素
        self.meter.set_scale_major_ticks(scale, 5, 2, 10, lv.color_black(), 5)

        # 3. 添加警示刻度线
        # 在起点添加蓝色弧
        blue_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.BLUE), 0)
        self.meter.set_indicator_start_value(blue_arc, r1)
        self.meter.set_indicator_end_value(blue_arc, v1)

        # 在刻度开始处使刻度线为蓝色
        blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
        self.meter.set_indicator_start_value(blue_arc_scale, r1)
        self.meter.set_indicator_end_value(blue_arc_scale, v1)

        # 在末端添加红色弧
        red_arc = self.meter.add_arc(scale, 1, lv.palette_main(lv.PALETTE.RED), 0)
        self.meter.set_indicator_start_value(red_arc, v2)
        self.meter.set_indicator_end_value(red_arc, r2)

        # 使刻度线在刻度末端变为红色
        red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
        self.meter.set_indicator_start_value(red_arc_scale, v2)
        self.meter.set_indicator_end_value(red_arc_scale, r2)

        # 4. 仪表指针
        # 4: 宽度
        # 下一参数：颜色
        # -10：指针与刻度线距离
        self.indic = self.meter.add_needle_line(scale, 2, lv.palette_main(lv.PALETTE.GREY), -5)
        
        # 5. 创建动画对象
        a = lv.anim_t()
        a.init()
        a.set_var(self.indic)
        temp = self.timer_cb()
        a.set_values(0, temp)
        a.set_time(200)
        # a.set_repeat_delay(100)
        # a.set_playback_time(200)
        # a.set_playback_delay(100)
        # a.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        a.set_custom_exec_cb(self.set_value)
        lv.anim_t.start(a)

        # 6. 添加定时器
        lv.timer_create(self.timer_cb, 200, None)  # 延时
        
    def set_value(self, anmi_obj, value):
        """动画回调函数"""
        self.meter.set_indicator_value(self.indic, value)
    
    def timer_cb(self, timer=None):
        """定时器回调函数"""
        ret=BMP.getPress()%10
        ret*=10
        self.meter.set_indicator_value(self.indic, ret)
        return ret
    
# 3. 创建要显示的组件
Widget1=Widget1(scr,200,0,0,0,100,10,60)#尺寸，x轴偏移量，y轴偏移量，动画起始值，动画结束值，开始处蓝色区域最大值，结尾处红色区域最小值
Widget2=Widget2(scr,80,-75,-115,0,100,0,100)
Widget3=Widget3(scr,80,75,-115,0,100,0,100)
Widget4=Widget4(scr,80,-75,100,0,100,0,100)
Widget5=Widget5(scr,80,0,120,0,100,0,100)
Widget6=Widget6(scr,80,75,100,0,100,0,100)

# 4. 显示screen对象中的内容
lv.scr_load(scr)


# ------------------------------ 看门狗，用来重启ESP32设备 --start------------------------
try:
    from machine import WDT
    wdt = WDT(timeout=2000)  # enable it with a timeout of 2s
    print("提示: 按下Ctrl+C结束程序")
    while True:
        wdt.feed()
        time.sleep(0.9)
except KeyboardInterrupt as ret:
    print("程序停止运行，ESP32已经重启...")
    time.sleep(10)
# ------------------------------ 看门狗，用来重启ESP32设备 --stop-------------------------

