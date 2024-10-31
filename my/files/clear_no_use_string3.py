# coding=utf-8
import os
import re
import threading
import time  # 引入time模块



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
            if "strings" in file and "values" == os.path.basename(root):
                found_files.append(os.path.join(root, file))

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




## ======================== 3.查询某个文件中的 string_id ，在项目中是否存在，如果不存在，则进行记录返回  ========================
# 创建锁和结果列表
lock = threading.Lock()
all_no_used_id = []

def search_lines_in_directory(string_xml_file, directory_b):
    if not os.path.exists(string_xml_file) or not os.path.isdir(directory_b):
        print("File or directory not found.")
        return

    ## 读取文件中的每一行
    found_no_used_id = []
    found_no_use_size = 0
    cur_string_index = 0
    ticks = time.time()
    print(f"\n============= 3.{string_xml_file} 总数 {all_id_string_size} 开始查找：=============")
    with open(string_xml_file, 'r') as file:

        for id_string in file.readlines():
            ## 获取 string.xml 中的 id

            ## 开始遍历项目文件
            cur_string_index = cur_string_index + 1
            find_result = False
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
                    # 找到了则结束
                    if find_result:
                        break
                    else:
                        find_result = find_string_in_file(id_string, file_path)
                if find_result:
                    break

            ## 查找结束 id 没有找到则进行记录
            if not find_result:
                spend1 = (time.time() - ticks) / 1000
                found_no_use_size = found_no_use_size + 1
                found_no_used_id.append(id_string)
                print(f"没有找到 {id_string.strip()} 当前位置 {cur_string_index} 总数 {found_no_use_size} 耗时 {spend1}")

    spend = time.time() - ticks
    print(f"============= 3.{string_xml_file} 查找结束：{spend}=============\n")
    if len(found_no_used_id) > 0:
        with lock:
           result_data = NoUserString(string_xml_file, found_no_used_id)
           all_no_used_id.append(result_data)




## ======================== 4.查找当前文件：如果是 .java 或者 .kt 文件，则查找是否存在 "R.String.a" ，如果是 .xml 文件，则查找是否存在 "@string/a"  ========================
def find_string_in_file(string_id, file_path):
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"文件 {file_path} 不存在.")
        return False

    # 获取文件扩展名
    _, file_extension = os.path.splitext(file_path)
    # 是否是需要过滤的文件
    is_ignore_file = any(string in file_path for string in ignore_find_file)

    if is_ignore_file:
        return False
    if file_extension in ['.java', '.kt']:
        search_string = f"R.string.{string_id.strip()}"
    elif file_extension == '.xml':
        search_string = f"@string/{string_id.strip()}"
    else:
        return False

    # 打开文件并查找字符串
    # print(f"{file_path} 查找：" + search_string)
    found = False
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if search_string in line:
                found = True
                break
    # if not found:
    #     print(f"{file_path}【没有找到】: {search_string}")
    # else:
    #     print(f"{file_path}【找到了】: '{search_string}'")
    return found




## ========================  5. 合并所有要查找的 string.xml 字符串, 返回一个文件 list ========================
all_id_string_size = 0
def merge_string_id(string_xml_list):

    print(f"\n============= 2.strings.xml 开始合并： =============")
    global all_id_string_size
    all_id_string_size = 0
    ticks = time.time()

    # 定义输出文件名模板
    output_all_string_path = "string_id_all.txt"
    output_file_list = []
    output_template = "string_id_output_{}.txt"
    output_file_count = 1
    output_file_line_count = 0
    output_file = open(output_template.format(output_file_count), 'w')
    output_all_file = open(output_all_string_path, 'w')
    output_file_list.append(output_file)

    for file_name in string_xml_list:
        ## 打开一个文件
        with open(file_name, 'r', encoding='utf-8') as file_read:
            for line in file_read:
                id_str = extract_string_name_from_line(line.strip())
                # 写入一个文件
                output_all_file.write(id_str)
                output_file.write(id_str)
                output_file_line_count += 1
                if output_file_line_count >= 100:
                    output_file.close()
                    output_file_count += 1
                    output_file = open(output_template.format(output_file_count), 'w')
                    output_file_line_count = 0
                    all_id_string_size = all_id_string_size + 1
                    output_file_list.append(output_file)

    spd = time.time() - ticks
    output_file.close()
    output_all_file.close()
    print(f"============= 2.strings.xml 合并完成 {spd}： =============")
    return output_file_list



## ========================  6.入口函数，开始查找 ========================
def search_no_user_id(folder):

    # 指定要写入的文件路径
    file_path = "record.txt"

    ## 1.获取所有的 string.xml 文件
    string_xml_list = find_strings_xml(folder)

    ## 2.合并所有的 string.xml 到一个文件列表
    file_name_list = merge_string_id(string_xml_list)


    ## 3.读取这个文件，看文件里面内容，项目中是否存在
    threads = []
    for file_name in file_name_list:
        thread = threading.Thread(target=search_lines_in_directory, args=(file_name,folder,))
        threads.append(thread)
        thread.start()

        no_use_string = search_lines_in_directory(file_name, folder)
        all_no_used_id.append(no_use_string)

    # 等待所有线程完成
    for thread in threads:
        thread.join()


    ## 4.最后一步：打开文件并写入文本
    with open(file_path, 'w') as file:

        file.write("\n========= 1.查询的 string.xml 列表：===========\n")
        for id_xml in string_xml_list:
            file.write(f"{id_xml} \n")

        if len(all_no_used_id) >0:
            file.write("\n========= 1.查询的 string.xml 列表：===========\n")
            for ids in all_no_used_id:
                file.write(f"=== {ids.fileName} ===\n")
                for strings in ids.all_no_used_id:
                    file.write(f"{strings}\n")

    print(all_no_used_id)



class NoUserString:

    fileName = ''
    all_no_used_id = ['']
    def __init__(self, name, all_no_used_id):
        self.fileName = name
        self.all_no_used_id = all_no_used_id


if __name__ == '__main__':
    # 使用示例
    folder_path1 = '/Users/lzf2/Documents/weipai/wejoy_us/wejoy/'
    folder_path = "/Users/lzf2/Documents/weipai/wejoy_us/wejoy"
    search_no_user_id(folder_path)





