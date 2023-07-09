#导入Pin模块
from machine import Pin
import time
import DS1302
from machine import RTC

#定义RTC控制对象
rtc=RTC()
#定义DS1302控制对象
ds1302=DS1302.DS1302(clk=Pin(13),dio=Pin(12),cs=Pin(15))

#定义星期
week=("星期一","星期二","星期三","星期四","星期五","星期六","星期天")

#程序入口
if __name__=="__main__":
    rtc_time=rtc.datetime()
    date_time=ds1302.DateTime()
    ds1302.DateTime([rtc_time[0],rtc_time[1],rtc_time[2],rtc_time[3],rtc_time[4],rtc_time[5],rtc_time[6]])
    while True:
        date_time=ds1302.DateTime()
        print("%d-%d-%d \t %02d:%02d:%02d \t %s" %(date_time[0],date_time[1],date_time[2],
                                                   date_time[4],date_time[5],date_time[6],
                                                   week[date_time[3]]))
        time.sleep(1)
        