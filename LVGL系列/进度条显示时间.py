import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
from machine import RTC
import DS1302

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
#定义RTC控制对象
rtc=RTC()
#定义DS1302控制对象
ds1302=DS1302.DS1302(clk=Pin(13),dio=Pin(12),cs=Pin(15))
#定义星期
week=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

rtc_time=rtc.datetime()
ds_time=ds1302.DateTime()
if rtc_time[0]==ds_time[0] : #在电脑启动时会自动校准RTC，判断RTC时间没有重置时同步校准DS1302
    ds1302.DateTime([rtc_time[0],rtc_time[1],rtc_time[2],rtc_time[3],rtc_time[4],rtc_time[5],rtc_time[6]])
if rtc_time[0]!=ds_time[0] : #如果程序上电启动，RTC会因断电重置，此时用DS1302校准RTC
    rtc.datetime((ds_time[0],ds_time[1],ds_time[2],ds_time[3],ds_time[4],ds_time[5],ds_time[6],0))
    
# 1. 创建显示screen对象。将需要显示的组件添加到这个screen才能显示
scr = lv.obj()  # scr====> screen 屏幕
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
scr = lv.scr_act()
scr.clean()
        
# 创建进度条对象
bar1 = lv.bar(scr)
# 创建样式对象
style_indic = lv.style_t()
style_indic.init()
style_indic.set_bg_opa(lv.OPA.COVER)
style_indic.set_bg_color(lv.palette_main(lv.PALETTE.RED))
style_indic.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
style_indic.set_bg_grad_dir(lv.GRAD_DIR.VER)
# 给进度条设置样式
bar1.add_style(style_indic, lv.PART.INDICATOR)
bar1.set_size(20, 150)
bar1.set_range(0, 23)
# 创建动画对象
anim_obj = lv.anim_t()
anim_obj.init()
anim_obj.set_var(bar1)
anim_obj.set_values(0, 1)
anim_obj.set_time(150)  # 设置从当前效果到指定效果的过度时间
#anim_obj.set_playback_time(200)  # 设置从指定效果到之前效果的过度时间
# anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
lv.anim_t.start(anim_obj)
# 设置位置
bar1.align(lv.ALIGN.CENTER,-60,30)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label1 = lv.label(scr)
label1.set_text(str(0))  
label1.align_to(bar1, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
#设置进度条数值
bar1.set_value(0, lv.ANIM.ON)
        
# 创建进度条对象
bar2 = lv.bar(scr)
# 创建样式对象
style_indic = lv.style_t()
style_indic.init()
style_indic.set_bg_opa(lv.OPA.COVER)
style_indic.set_bg_color(lv.palette_main(lv.PALETTE.RED))
style_indic.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
style_indic.set_bg_grad_dir(lv.GRAD_DIR.VER)
# 给进度条设置样式
bar2.add_style(style_indic, lv.PART.INDICATOR)
bar2.set_size(20, 150)
bar2.set_range(0, 59)
# 创建动画对象
anim_obj = lv.anim_t()
anim_obj.init()
anim_obj.set_var(bar2)
anim_obj.set_values(0, 1)
anim_obj.set_time(200)  # 设置从当前效果到指定效果的过度时间
#anim_obj.set_playback_time(200)  # 设置从指定效果到之前效果的过度时间
# anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
lv.anim_t.start(anim_obj)
# 设置位置
bar2.align(lv.ALIGN.CENTER,0,30)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label2 = lv.label(scr)
label2.set_text(str(0))  
label2.align_to(bar2, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
#设置进度条数值
bar2.set_value(0, lv.ANIM.ON)

# 创建进度条对象
bar3 = lv.bar(scr)
# 创建样式对象
style_indic = lv.style_t()
style_indic.init()
style_indic.set_bg_opa(lv.OPA.COVER)
style_indic.set_bg_color(lv.palette_main(lv.PALETTE.RED))
style_indic.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
style_indic.set_bg_grad_dir(lv.GRAD_DIR.VER)
# 给进度条设置样式
bar3.add_style(style_indic, lv.PART.INDICATOR)
bar3.set_size(20, 150)
bar3.set_range(0, 59)
# 创建动画对象
anim_obj = lv.anim_t()
anim_obj.init()
anim_obj.set_var(bar1)
anim_obj.set_values(0, 1)
anim_obj.set_time(200)  # 设置从当前效果到指定效果的过度时间
#anim_obj.set_playback_time(200)  # 设置从指定效果到之前效果的过度时间
# anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
lv.anim_t.start(anim_obj)
# 设置位置
bar3.align(lv.ALIGN.CENTER,60,30)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label3 = lv.label(scr)
label3.set_text(str(0))  
label3.align_to(bar3, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
#设置进度条数值
bar3.set_value(0, lv.ANIM.ON)

# 创建进度条对象
bar4 = lv.bar(scr)
# 创建样式对象
style_indic = lv.style_t()
style_indic.init()
style_indic.set_bg_opa(lv.OPA.COVER)
style_indic.set_bg_color(lv.palette_main(lv.PALETTE.RED))
style_indic.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
style_indic.set_bg_grad_dir(lv.GRAD_DIR.VER)
# 给进度条设置样式
bar4.add_style(style_indic, lv.PART.INDICATOR)
bar4.set_size(20, 150)
bar4.set_range(1900, 2100)
# 创建动画对象
anim_obj = lv.anim_t()
anim_obj.init()
anim_obj.set_var(bar4)
anim_obj.set_values(0, 1)
anim_obj.set_time(150)  # 设置从当前效果到指定效果的过度时间
#anim_obj.set_playback_time(200)  # 设置从指定效果到之前效果的过度时间
# anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
lv.anim_t.start(anim_obj)
# 设置位置
bar4.align(lv.ALIGN.CENTER,-90,-30)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label4 = lv.label(scr)
label4.set_text(str(0))  
label4.align_to(bar4, lv.ALIGN.OUT_TOP_MID, -10, -5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
#设置进度条数值
bar4.set_value(2000, lv.ANIM.ON)

# 创建进度条对象
bar5 = lv.bar(scr)
# 创建样式对象
style_indic = lv.style_t()
style_indic.init()
style_indic.set_bg_opa(lv.OPA.COVER)
style_indic.set_bg_color(lv.palette_main(lv.PALETTE.RED))
style_indic.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
style_indic.set_bg_grad_dir(lv.GRAD_DIR.VER)
# 给进度条设置样式
bar5.add_style(style_indic, lv.PART.INDICATOR)
bar5.set_size(20, 150)
bar5.set_range(1, 12)
# 创建动画对象
anim_obj = lv.anim_t()
anim_obj.init()
anim_obj.set_var(bar5)
anim_obj.set_values(0, 1)
anim_obj.set_time(150)  # 设置从当前效果到指定效果的过度时间
#anim_obj.set_playback_time(200)  # 设置从指定效果到之前效果的过度时间
# anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
lv.anim_t.start(anim_obj)
# 设置位置
bar5.align(lv.ALIGN.CENTER,-30,-30)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label5 = lv.label(scr)
label5.set_text(str(0))  
label5.align_to(bar5, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
#设置进度条数值
bar5.set_value(1, lv.ANIM.ON)

# 创建进度条对象
bar6 = lv.bar(scr)
# 创建样式对象
style_indic = lv.style_t()
style_indic.init()
style_indic.set_bg_opa(lv.OPA.COVER)
style_indic.set_bg_color(lv.palette_main(lv.PALETTE.RED))
style_indic.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
style_indic.set_bg_grad_dir(lv.GRAD_DIR.VER)
# 给进度条设置样式
bar6.add_style(style_indic, lv.PART.INDICATOR)
bar6.set_size(20, 150)
bar6.set_range(1, 31)
# 创建动画对象
anim_obj = lv.anim_t()
anim_obj.init()
anim_obj.set_var(bar4)
anim_obj.set_values(0, 1)
anim_obj.set_time(150)  # 设置从当前效果到指定效果的过度时间
#anim_obj.set_playback_time(200)  # 设置从指定效果到之前效果的过度时间
# anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
lv.anim_t.start(anim_obj)
# 设置位置
bar6.align(lv.ALIGN.CENTER,30,-30)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label6 = lv.label(scr)
label6.set_text(str(0))  
label6.align_to(bar6, lv.ALIGN.OUT_TOP_MID, 0, -5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
#设置进度条数值
bar6.set_value(1, lv.ANIM.ON)

# 创建进度条对象
bar7 = lv.bar(scr)
# 创建样式对象
style_indic = lv.style_t()
style_indic.init()
style_indic.set_bg_opa(lv.OPA.COVER)
style_indic.set_bg_color(lv.palette_main(lv.PALETTE.RED))
style_indic.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
style_indic.set_bg_grad_dir(lv.GRAD_DIR.VER)
# 给进度条设置样式
bar7.add_style(style_indic, lv.PART.INDICATOR)
bar7.set_size(20, 150)
bar7.set_range(0, 6)
# 创建动画对象
anim_obj = lv.anim_t()
anim_obj.init()
anim_obj.set_var(bar6)
anim_obj.set_values(0, 1)
anim_obj.set_time(150)  # 设置从当前效果到指定效果的过度时间
#anim_obj.set_playback_time(200)  # 设置从指定效果到之前效果的过度时间
# anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
lv.anim_t.start(anim_obj)
# 设置位置
bar7.align(lv.ALIGN.CENTER,90,-30)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label7 = lv.label(scr)
label7.set_text(str(0))  
label7.align_to(bar7, lv.ALIGN.OUT_TOP_MID, -25, -5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
#设置进度条数值
bar7.set_value(0, lv.ANIM.ON)

# 4. 显示screen对象中的内容
lv.scr_load(scr)

# ------------------------------ 看门狗，用来重启ESP32设备 --start------------------------
try:
    from machine import WDT
    wdt = WDT(timeout=2000)  # enable it with a timeout of 2s
    print("提示: 按下Ctrl+C结束程序")
    while True:
        wdt.feed()
        rtc_time=rtc.datetime()
        bar1.set_value(rtc_time[4], lv.ANIM.ON)
        label1.set_text(str(rtc_time[4]))
        bar2.set_value(rtc_time[5], lv.ANIM.ON)
        label2.set_text(str(rtc_time[5]))
        bar3.set_value(rtc_time[6], lv.ANIM.ON)
        label3.set_text(str(rtc_time[6]))
        bar4.set_value(rtc_time[0], lv.ANIM.ON)
        label4.set_text(str(rtc_time[0]))
        bar5.set_value(rtc_time[1], lv.ANIM.ON)
        label5.set_text(str(rtc_time[1]))
        bar6.set_value(rtc_time[2], lv.ANIM.ON)
        label6.set_text(str(rtc_time[2]))
        bar7.set_value(rtc_time[3], lv.ANIM.ON)
        label7.set_text(str(week[rtc_time[3]]))
        time.sleep(1)
except KeyboardInterrupt as ret:
    print("程序停止运行，ESP32已经重启...")
    time.sleep(10)
# ------------------------------ 看门狗，用来重启ESP32设备 --stop-------------------------

