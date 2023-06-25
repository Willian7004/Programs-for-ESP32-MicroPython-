import lvgl as lv
import time
from espidf import VSPI_HOST
from ili9XXX import ili9341
from xpt2046 import xpt2046
from machine import Pin
from machine import SoftI2C
from machine import RTC
import DS1302
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

#定义RTC控制对象
rtc=RTC()
#定义DS1302控制对象
ds1302=DS1302.DS1302(clk=Pin(13),dio=Pin(12),cs=Pin(15))
#定义星期
week=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
#初始化BMP280，定义第二个I2C接口i2c2用于连接BMP280
i2c2 = SoftI2C(sda=Pin(22), scl=Pin(21))
BMP = bmp280.BMP280(i2c2)

rtc_time=rtc.datetime()
ds_time=ds1302.DateTime()
if rtc_time[0]==ds_time[0] : #在电脑启动时会自动校准RTC，判断RTC时间没有重置时同步校准DS1302
    ds1302.DateTime([rtc_time[0],rtc_time[1],rtc_time[2],rtc_time[3],rtc_time[4],rtc_time[5],rtc_time[6]])
if rtc_time[0]!=ds_time[0] : #如果程序上电启动，RTC会因断电重置，此时用DS1302校准RTC
    rtc.datetime((ds_time[0],ds_time[1],ds_time[2],ds_time[3],ds_time[4],ds_time[5],ds_time[6],0))    

# 1. 创建显示screen对象。将需要显示的组件添加到这个screen才能显示
scr = lv.obj()

# 2. 封装要显示的组件
class MyWidget():
    def __init__(self, scr):
        # Create an image from the png file
        try:
            with open('./image.jpg', 'rb') as f:
                png_data = f.read()
        except:
            print("找不到图片文件...")
            sys.exit()

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
        obj.align(lv.ALIGN.CENTER,0,-90)  # 距屏幕中心偏移量

btn1 = lv.btn(scr)  # 将当前按钮与screen对象进行关联
btn1.set_size(180, 30)  # 设置按钮的宽度为120, 高度为50
btn1.align(lv.ALIGN.CENTER,0,-10)  # 距屏幕中心偏移量
label1 = lv.label(btn1)  # 在按钮上创建一个标签Label，用来显示文字用
label1.set_text("Button")  # 设置文字内容
label1.center()  # 相对于父对象居中

btn2 = lv.btn(scr)  # 将当前按钮与screen对象进行关联
btn2.set_size(120, 30)  # 设置按钮的宽度为120, 高度为50
btn2.align(lv.ALIGN.CENTER,0,25)  # 距屏幕中心偏移量
label2 = lv.label(btn2)  # 在按钮上创建一个标签Label，用来显示文字用
label2.set_text("Button")  # 设置文字内容
label2.center()  # 相对于父对象居中

btn3 = lv.btn(scr)  # 将当前按钮与screen对象进行关联
btn3.set_size(180, 30)  # 设置按钮的宽度为120, 高度为50
btn3.align(lv.ALIGN.CENTER,0,65)  # 距屏幕中心偏移量
label3 = lv.label(btn3)  # 在按钮上创建一个标签Label，用来显示文字用
label3.set_text("Button")  # 设置文字内容
label3.center()  # 相对于父对象居中

btn4 = lv.btn(scr)  # 将当前按钮与screen对象进行关联
btn4.set_size(180, 30)  # 设置按钮的宽度为120, 高度为50
btn4.align(lv.ALIGN.CENTER,0,100)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
label4 = lv.label(btn4)  # 在按钮上创建一个标签Label，用来显示文字用
label4.set_text("Button")  # 设置文字内容
label4.center()  # 相对于父对象居中

btn5 = lv.btn(scr)  # 将当前按钮与screen对象进行关联
btn5.set_size(180, 30)  # 设置按钮的宽度为120, 高度为50
btn5.align(lv.ALIGN.CENTER,0,135)  # 居中（第1个0表示x的偏移量，第2个0表示相对于y的偏移量）
label5 = lv.label(btn5)  # 在按钮上创建一个标签Label，用来显示文字用
label5.set_text("Button")  # 设置文字内容
label5.center()  # 相对于父对象居中

# 3. 创建要显示的组件
MyWidget(scr)
# 4. 显示screen对象中的内容
lv.scr_load(scr)

try:
    from machine import WDT
    wdt = WDT(timeout=2000)  # enable it with a timeout of 2s
    print("提示: 按下Ctrl+C结束程序")
    while True:
        wdt.feed()
        rtc_time=rtc.datetime()
        label1.set_text(str(rtc_time[0])+'-'+str(rtc_time[1])+'-'+str(rtc_time[2])+'  '+str(week[rtc_time[3]]))  # 修改文字内容
        label2.set_text(str(rtc_time[4])+' : '+str(rtc_time[5])+' : '+str(rtc_time[6]))
        label3.set_text('Temperature: '+str(BMP.getTemp())+' C')
        label4.set_text('Pressure: '+str(BMP.getPress()) + ' Pa')
        label5.set_text('Altitude: '+str(BMP.getAltitude()) + ' M')
        time.sleep(0.9)
except KeyboardInterrupt as ret:
    print("程序停止运行，ESP32已经重启...")
