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

debug = True
## 使用的 string_id map
string_id_use_size_map = {}

## 未使用的 string_id list
no_string_id_use_size_list = []

## 所有的 string.xml 文件
all_string_file_list = []


## ======================== 1.查找所有的 string.xml 文件 ========================
def find_strings_xml(folder):
    print(f"\n============= 1.strings.xm 开始查找： =============")
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
                all_string_file_list.append(real_path)
            if "strings" in file and "values-es" == parent_path:
                all_string_file_list.append(real_path)
            if "strings" in file and "values-ru" == parent_path:
                all_string_file_list.append(real_path)
            if "strings" in file and "values-fr" == parent_path:
                all_string_file_list.append(real_path)
            if "strings" in file and "values-zh" == parent_path:
                all_string_file_list.append(real_path)
            if "strings" in file and "values-pt" == parent_path:
                all_string_file_list.append(real_path)

    spend = time.time() - ticks
    # for id_str in found_files:
    #     print(f"目标文件：{id_str}")
    print(f"============= strings.xm 查找结束：{spend} =============\n")
    return found_files


## ======================== 2.从 string.xml 中提取 id 部分 ========================
def extract_string_name_from_line(line):
    match = re.search(r'<string name="([^"]+)', line)
    if match:
        return match.group(1)
    return ""


## ========================  3.查询某个文件中的 id ，在项目中是否存在，如果不存在，则进行记录返回 ========================
def search_lines_in_directory(directory_b):
    if not os.path.isdir(directory_b):
        print("File or directory not found.")
        return None

    ## 读取文件中的每一行
    all_id_string_size = len(string_id_use_size_map)
    ticks = time.time()
    print(f"\n============= 3.总数 {all_id_string_size} 开始查找：=============")

    ## 开始遍历项目文件
    for root, dirs, files in os.walk(directory_b):

        # 黑名单文件，不进行查询
        if any(item in root for item in ignore_find_module):
            # 如果文件名在黑名单中，则跳过该文件
            # print(f"跳过 {root}")
            continue

        # 开始源代码中查询
        for file_name in files:
            # 查找结果
            file_path = os.path.join(root, file_name)
            find_string_in_file(file_path)

    ## 所有的 id_key 没有找到
    spend = time.time() - ticks
    print(f"============= 3.查找结束：{spend}=============\n")


## ========================  4.查找当前文件：如果是 .java 或者 .kt 文件，则查找是否存在 "R.String.a" ，如果是 .xml 文件，则查找是否存在 "@string/a" ========================
def find_string_in_file(file_path):
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        # print(f"文件 {file_path} 不存在.")
        return False

    # 获取文件扩展名
    _, file_extension = os.path.splitext(file_path)

    # 是否是需要过滤的文件
    is_ignore_file = any(string in file_path for string in ignore_find_file)

    if is_ignore_file:
        # print(f"{file_path} 过滤")
        return False
    elif file_extension in ['.java', '.kt']:
        search_string = "R.string."
    elif file_extension == '.xml':
        search_string = "@string/"
    else:
        return False

    # 打开文件并查找字符串
    # print(f"{file_path} 查找：" + search_string)
    found = False
    with open(file_path, 'r', encoding='utf-8') as file:

        # 遍历每一行
        for line in file:

            # 条件过滤
            res = line.strip()
            if len(res) <= 0: continue
            if search_string not in res: continue

            # 遍历 map ，看该行数据 是否 map 里面存在
            for id_key in string_id_use_size_map:
                # 拼接结果
                s_result = f"{search_string}{id_key}"
                # 存在，则更新 value
                if s_result in line:
                    # print(f"{s_result} 在文件中：" + file_path)
                    id_value = string_id_use_size_map[f"{id_key}"]
                    id_value += 1
                    string_id_use_size_map[f"{id_key}"] = id_value

    # if not found:
    #     print(f"{file_path}【没有找到】: {search_string}")
    # else:
    #     print(f"{file_path}【找到了】: '{search_string}'")
    return found


## ======================== 5.合并所有要查找的 string.xml 字符串 ========================

def merge_string_id(string_xml_list):
    print(f"\n============= 2.strings.xml 开始合并： =============")
    ticks = time.time()
    string_id_use_size_map.clear()
    file_path = "string_find.txt"
    with open(file_path, 'w') as file_write:
        for file_name in string_xml_list:
            with open(file_name, 'r', encoding='utf-8') as file_read:
                for line in file_read:
                    id_str = extract_string_name_from_line(line.strip())
                    if len(id_str) > 0:
                        file_write.write(f"{id_str}\n")
                        # 添加到 map 集合
                        string_id_use_size_map[f'{id_str}'] = 0

    # for s_key in string_id_use_size_map:
    #     print(f"key = {s_key} value = 0")

    s_size = len(string_id_use_size_map)
    spd = time.time() - ticks
    print(f"============= strings.xml 合并完成 {spd} 总数：{s_size} =============")


## ======================== 6.将结果写入文件 ========================
def remove_empty_lines(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    # 过滤掉空行
    non_empty_lines = [line for line in lines if line.strip() != '']
    with open(output_file, 'w') as file:
        file.writelines(non_empty_lines)


def print_result_to_file(string_xml_list):
    # 指定要写入的文件路径
    ticks = time.time()
    print(f"\n============= 4.开始将结果写入文件：=============")
    file_path = "record_4.txt"
    file_path_last = "record_4_last.txt"
    with open(file_path, 'w') as file:

        file.write("\n========= 1.查询的 string.xml 列表：===========\n")
        for id_xml in string_xml_list:
            file.write(f"{id_xml} \n")

        file.write("\n========= 2.未使用 string 列表：===========\n")
        for id_key in string_id_use_size_map:
            id_value = string_id_use_size_map[f"{id_key}"]
            # print(f"key = {id_key} value = {id_value}")
            ## 说明没有使用
            if id_value == 0:
                no_string_id_use_size_list.append(id_key)
                file.write(f"{id_key}\n")
    ## 去掉空行
    remove_empty_lines(file_path, file_path_last)
    spd = time.time() - ticks
    print(f"============= 4.结果写入完成：{spd}=============")


## ======================== 6.遍历所有的目标 string.xml 文件 ========================

# 处理包含特殊字符的文本内容
def handle_special_characters(element):
    if element.text is not None and "&quot;" in element.text:
        element.text = ET.CDATA(element.text)
    for child in element:
        handle_special_characters(child)

def remove_element_by_string(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    print(f"==== 开始检查 {xml_file} ====")
    for element in root.findall(".//string"):
        find_result = False
        for no_use_str in no_string_id_use_size_list:
            ## 没有使用的
            if no_use_str == element.attrib.get('name', 'None_Xml'):
                try:
                    root.remove(element)
                    find_result = True
                    print(f"移除 {no_use_str}")
                except Exception as e:
                    print(f"移除 {no_use_str} 异常，{e}")

                ## 找到了，则开始读取文件下一行
                if find_result: break

    # 处理特殊字符
    tree.write(xml_file, encoding='utf-8', xml_declaration=True, method="xml")


def clear_no_use_string():
    ticks = time.time()
    clear_str_size = len(no_string_id_use_size_list)
    print(f"\n============= 5.开始清除资源：{clear_str_size}=============")

    if clear_str_size > 0:
        for string_file in all_string_file_list:
            remove_element_by_string(string_file)

    spend = time.time() - ticks
    print(f"============= 5.清除资源结束：{spend}=============")


## ======================== 7.入口函数，开始查找 ========================
def search_no_user_id(folder):
    ## 1.获取所有的 string.xml 文件
    string_xml_list = find_strings_xml(folder)

    ## 2.合并所有的 string.xml 并存入 map 中
    merge_string_id(string_xml_list)

    ## 3.遍历 map，看项目中是否有 未使用 key
    search_lines_in_directory(folder)

    ## 4.最后一步：打开文件并写将结果写入
    print_result_to_file(string_xml_list)
    # 清除无用内存
    string_id_use_size_map.clear()

    ## 5.开始清除项目无用资源
    clear_no_use_string()


## ======================== 7.启动程序 ========================
if __name__ == '__main__':
    # 使用示例
    folder_path = "/Users/lzf2/Documents/weipai/wejoy_us/wejoy"
    search_no_user_id(folder_path)
