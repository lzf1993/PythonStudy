## 查找 values/string 存在 中文的 id 并进行输出


# coding=utf-8
import os
import re
import time  # 引入time模块
import xml.etree.ElementTree as ET

## 1. 查找所有的 string.xml 文件
## 2. 遍历每个 string.xml 文件内容，查找 源文件中是否 包括 R.String.xx + xml 中是否包括：@string/xx
## 3. 如果不包括，则记录下来进行输出。
## 4. 如果不包括，则进行删除
##     1.遍历匹配 "res/value**" 目录下面的 string.xml 文件
##     2.删除 <string name="xxx"> 行


# 需要过滤的文件
ignore_find_file = [
    'res/values',
]

# 需要过滤的模块
ignore_find_module = [
    '/build/intermediates',
    '/wejoy/.idea/',
    '/wejoy/.git/',

    '/wejoy/component/authcheck',
    '/wejoy/lib/alifaceid',
    '/wejoy/lib/android-fake',
    '/wejoy/lib/android-gif-drawable-1.1.6',
    '/wejoy/lib/cn-resources',
    '/wejoy/lib/cn-libshare',
    '/wejoy/lib/cocos1.6',
    '/wejoy/lib/libavatar',
    '/wejoy/lib/libbaidu',
    '/wejoy/lib/libcocossdk',
    '/wejoy/lib/libgoogle-pay',
    '/wejoy/lib/liblinkedme',
    '/wejoy/lib/liblocation-bdmap',
    '/wejoy/lib/libMiPush',
    '/wejoy/lib/libproto-game-mj',
    '/wejoy/lib/libsdk',
    '/wejoy/lib/libsecurity',
    '/wejoy/lib/liblinkedme',
    '/wejoy/lib/libsign',
    '/wejoy/lib/libstmobilejni',
    '/wejoy/lib/libthirdparty',
    '/wejoy/lib/libtrack-shence',
    '/wejoy/lib/libwpdid',
    '/wejoy/lib/talkingdata',

    '/wejoy/module/app',
    '/wejoy/module/bottle',
    '/wejoy/module/jar-loader-impl',
    '/wejoy/module/landlord',
    '/wejoy/module/test',
    '/wejoy/module/app',
    '/wejoy/module/app',

    '/wejoy/service/CustomerService',
    '/wejoy/service/VoiceServiceAgora',
]


## 中文 id
chinese_elements = []


## ======================== 1.查找所有的 string.xml 文件 ========================
def find_strings_xml(folder):
    print(f"\n============= 1.strings.xml 开始查找： =============")
    found_files = []
    ticks = time.time()
    # root：表示当前正在遍历的文件夹的路径  dirs：是一个包含当前文件夹中所有子文件夹名称的列表  files：是一个包含当前文件夹中所有文件名称的列表
    for root, dirs, files in os.walk(folder):
        if any(item in root for item in ignore_find_module):
            # 如果文件名在黑名单中，则跳过该文件
            continue
        for file in files:
            parent_path = os.path.basename(root)
            real_path = os.path.join(root, file)
            if "strings" in file and "values" == parent_path:
                found_files.append(real_path)

    spend = time.time() - ticks
    print(f"============= strings.xml 查找结束：{spend} =============\n")
    return found_files




## ======================== 2.开始查找中文字符 ========================

def contains_chinese(text):
    if text is None:
        return False
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False


def parse_xml_for_chinese_elements(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for element in root:
        name = element.get("name")
        text = element.text
        if name is not None and contains_chinese(text):
            chinese_elements.append(name)

    return chinese_elements



def find_chinese_id_string(string_xml_list):
    print(f"\n============= 2.开始查找中文 string.xml： =============")
    ticks = time.time()
    chinese_elements.clear()

    ## 检查 中文
    for file_name in string_xml_list:
        parse_xml_for_chinese_elements(file_name)

    ## 记录到文件中
    if len(chinese_elements) > 0:
        file_path = "find_chinese_string.txt"
        with open(file_path, 'w') as file_write:
            for chinese_id in chinese_elements:
                file_write.write(f"{chinese_id}\n")

    spd = time.time() - ticks
    print(f"============= 查找中文 string.xml 完成 {spd} =============")




## ======================== 3.入口函数，开始查找 ========================
def search_no_user_id(folder):
    ## 1.获取所有的 string.xml 文件
    string_xml_list = find_strings_xml(folder)

    ## 2.遍历所有的文件，如果该文件中存在中文，则记录 id
    find_chinese_id_string(string_xml_list)



## ======================== 4.启动程序 ========================
if __name__ == '__main__':
    # 使用示例
    folder_path = "/Users/lzf2/Documents/weipai/wejoy_us/wejoy"
    search_no_user_id(folder_path)
