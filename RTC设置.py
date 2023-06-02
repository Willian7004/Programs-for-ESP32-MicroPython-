#导入Pin模块
from machine import Pin
from machine import RTC
import time


#定义RTC控制对象
rtc=RTC() 

#定义星期
week=("星期一","星期二","星期三","星期四","星期五","星期六","星期天")

#程序入口
if __name__=="__main__":
    print("设置时间")
    a=int(input("年"))
    b=int(input("月"))
    c=int(input("日"))
    d=int(input("星期（0-6）"))
    e=int(input("时"))
    f=int(input("分"))
    g=int(input("秒"))
    rtc.datetime((a,b,c,d,e,f,g,0))
    while True:
        date_time=rtc.datetime()
        print("%d-%d-%d \t %02d:%02d:%02d \t %s" %(date_time[0],date_time[1],date_time[2],
                                                   date_time[4],date_time[5],date_time[6],
                                                   week[date_time[3]]))
        time.sleep(1)
