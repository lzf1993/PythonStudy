# coding=utf-8
import time
import os

def reboot(cycle):
    for i in range(cycle):
        os.system("adb -s R7AT31H833L shell am force-stop com.wejoy.weplay.ru")
        os.system("adb -s R7AT31H833L shell am start -n com.wejoy.weplay.ru/com.wepie.wespy.module.login.start.StartActivity")
        print("app第%s轮重启中...请稍候!" % (i+1))
        time.sleep(10)
reboot(1000)

