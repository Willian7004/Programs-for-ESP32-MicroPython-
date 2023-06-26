import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
from machine import Pin
from machine import ADC
from machine import Timer

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
bar1.set_size(20, 200)
bar1.set_range(0, 4095)
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
bar1.align(lv.ALIGN.CENTER,-90,0)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label1 = lv.label(scr)
label1.set_text(str(0))  
label1.align_to(bar1, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
label_1 = lv.label(scr)
label_1.set_text('ADC_32')  
label_1.align_to(bar1, lv.ALIGN.OUT_TOP_MID, 0, -5)
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
bar2.set_size(20, 200)
bar2.set_range(0, 4095)
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
bar2.align(lv.ALIGN.CENTER,-30,0)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label2 = lv.label(scr)
label2.set_text(str(0))  
label2.align_to(bar2, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
label_2 = lv.label(scr)
label_2.set_text('ADC_33')  
label_2.align_to(bar2, lv.ALIGN.OUT_TOP_MID, 0, -5)
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
bar3.set_size(20, 200)
bar3.set_range(0, 4095)
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
bar3.align(lv.ALIGN.CENTER,30,0)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label3 = lv.label(scr)
label3.set_text(str(0))  
label3.align_to(bar3, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
label_3 = lv.label(scr)
label_3.set_text('ADC_34')  
label_3.align_to(bar3, lv.ALIGN.OUT_TOP_MID, 0, -5)
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
bar4.set_size(20, 200)
bar4.set_range(0, 4095)
# 创建动画对象
anim_obj = lv.anim_t()
anim_obj.init()
anim_obj.set_var(bar4)
anim_obj.set_values(0, 1)
anim_obj.set_time(200)  # 设置从当前效果到指定效果的过度时间
#anim_obj.set_playback_time(200)  # 设置从指定效果到之前效果的过度时间
# anim_obj.set_repeat_count(lv.ANIM_REPEAT_INFINITE)  # 设置重复
lv.anim_t.start(anim_obj)
# 设置位置
bar4.align(lv.ALIGN.CENTER,90,0)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
# 创建一个标签label
label4 = lv.label(scr)
label4.set_text(str(0))  
label4.align_to(bar4, lv.ALIGN.OUT_BOTTOM_MID, 0, 5)  # label的中间与滑块的上外边框中间对齐，然后y向下5像素 x不变
label_4 = lv.label(scr)
label_4.set_text('ADC_35')  
label_4.align_to(bar4, lv.ALIGN.OUT_TOP_MID, 0, -5)
#设置进度条数值
bar4.set_value(0, lv.ANIM.ON)

# 4. 显示screen对象中的内容
lv.scr_load(scr)

# ------------------------------ 看门狗，用来重启ESP32设备 --start------------------------
try:
    from machine import WDT
    wdt = WDT(timeout=1000)  # enable it with a timeout of 2s
    print("提示: 按下Ctrl+C结束程序")
    while True:
        wdt.feed()
        vol1=adc1.read()
        ad_vol1=round(3.3*vol1/4095,2)#保留2位小数
        bar1.set_value(vol1, lv.ANIM.ON)
        label1.set_text(str(ad_vol1))
        vol2=adc2.read()
        ad_vol2=round(3.3*vol2/4095,2)#保留2位小数
        bar2.set_value(vol2, lv.ANIM.ON)
        label2.set_text(str(ad_vol2))
        vol3=adc3.read()
        ad_vol3=round(3.3*vol3/4095,2)#保留2位小数
        bar3.set_value(vol3, lv.ANIM.ON)
        label3.set_text(str(ad_vol3))
        vol4=adc4.read()
        ad_vol4=round(3.3*vol4/4095,2)#保留2位小数
        bar4.set_value(vol4, lv.ANIM.ON)
        label4.set_text(str(ad_vol4))
        time.sleep(0.2)
except KeyboardInterrupt as ret:
    print("程序停止运行，ESP32已经重启...")
    time.sleep(10)
# ------------------------------ 看门狗，用来重启ESP32设备 --stop-------------------------

