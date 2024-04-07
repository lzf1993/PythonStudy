# coding=utf-8
import time
import os

def reboot(cycle):
    for i in range(cycle):
        os.system("adb -s R58RA45JW1J shell am force-stop com.wejoy.weplay.ru")
        os.system("adb -s R58RA45JW1J shell am start -n com.wejoy.weplay.ru/com.wepie.wespy.module.login.start.StartActivity")
        print("app第%s轮重启中...请稍候!" % (i+1))
        time.sleep(40)
reboot(1000)

