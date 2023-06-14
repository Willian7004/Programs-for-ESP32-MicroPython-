import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
import fs_driver
from machine import Pin
import onewire, ds18x20

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
        
        # 创建文本框
        ta = lv.textarea(scr)
        ta.set_one_line(False)  # 关闭1行模式
        ta.set_size(240, 80)  # 设置宽高
        ta.align(lv.ALIGN.TOP_MID, 0, 5)  # 设置位置
        ta.add_event_cb(lambda e: self.textarea_event_handler(e, ta), lv.EVENT.READY, None)  # 添加回调函数
        ta.add_state(lv.STATE.FOCUSED)   # 设置光标

        # 定义数字键盘要显示的内容
        btnm_map = ["a", "b", "c","d", "e", "f", "\n",
                    "g", "h", "i","j", "k", "l", "\n",
                    "m", "n", "o","p", "q", "r", "\n",
                    "s", "t", "u","v", "w", "x", "\n",
                    "y", "z", "1","2", "3", "4", "\n",
                    "5", "6", "7","8", "9", "0", "\n",
                    ",", ".", "?","!",lv.SYMBOL.BACKSPACE, lv.SYMBOL.NEW_LINE, ""]

        # 按钮矩阵
        btnm = lv.btnmatrix(scr)
        btnm.set_size(230, 230)  # 设置宽高
        btnm.align(lv.ALIGN.BOTTOM_MID, 0, -5)  # 设置位置
        btnm.add_event_cb(lambda e: self.btnm_event_handler(e, ta), lv.EVENT.VALUE_CHANGED, None)
        btnm.clear_flag(lv.obj.FLAG.CLICK_FOCUSABLE)  # 设置为非活跃，即文本框中的光标一直聚焦
        btnm.set_map(btnm_map)  # 设置要显示的内容（数字键盘）
        
        # 设置有源蜂鸣器引脚
        self.p15 = Pin(15, Pin.OUT)
        self.p15.value(1)  # 不响
        
    def textarea_event_handler(self, e, ta):
        print("按下了回车键，当前的文本框内容是: " + ta.get_text())


    def btnm_event_handler(self, e, ta):
        obj = e.get_target()
        txt = obj.get_btn_text(obj.get_selected_btn())  # 获取被点击的按钮的内容，例如数字3
        if txt == lv.SYMBOL.BACKSPACE:  # 如果是退格键，那么就删除1个字符
            ta.del_char()
        elif txt == lv.SYMBOL.NEW_LINE:  # 如果是回车键，那么就触发事件
            lv.event_send(ta, lv.EVENT.READY, None)
        elif txt:
            ta.add_text(txt)  # 如果不是回车键，那么就将当前数字显示到文本框
            
        # 让蜂鸣器响1声
        self.p15.value(0)
        time.sleep(0.2)
        self.p15.value(1)  # 不响


# 3. 创建要显示的组件
MyWidget(scr)

# 4. 显示screen对象中的内容
lv.scr_load(scr)


