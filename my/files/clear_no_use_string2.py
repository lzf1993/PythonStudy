# coding=utf-8
import os
import re
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
    'build/intermediates',
]

# 需要过滤的模块
ignore_find_module = [
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


## 1.查找所有的 string.xml 文件
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



## 2.从 string.xml 中提取 id 部分
def extract_string_name_from_line(line):
    match = re.search(r'<string name="([^"]+)', line)
    if match:
        return match.group(1)
    return ""



## 3.查询某个文件中的 id ，在项目中是否存在，如果不存在，则进行记录返回
def search_lines_in_directory(string_xml_file, directory_b):
    if not os.path.exists(string_xml_file) or not os.path.isdir(directory_b):
        print("File or directory not found.")
        return

    ## 读取文件中的每一行
    found_no_used_id = []
    ticks = time.time()
    print(f"\n=============  {string_xml_file} 开始查找：=============")
    with open(string_xml_file, 'r') as file:

        for id_string in file.readlines():
            ## 获取 string.xml 中的 id

            ## 如果找到 id 了，则进行查询
            find_result = False
            if len(id_string) != 0:
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
                ## id 没有找到则进行记录
                if not find_result:
                    print(f"没有找到 {id_string.strip()}")
                    found_no_used_id.append(id_string)

    spend = time.time() - ticks
    print(f"=============  {string_xml_file} 查找结束：{spend}=============\n")
    if len(found_no_used_id) > 0:
        return NoUserString(string_xml_file, found_no_used_id)
    else:
        return None



## 4.查找当前文件：如果是 .java 或者 .kt 文件，则查找是否存在 "R.String.a" ，如果是 .xml 文件，则查找是否存在 "@string/a"
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
    elif file_extension in ['.java', '.kt']:
        search_string = f"R.string.{string_id}"
    elif file_extension == '.xml':
        search_string = f"@string/{string_id}"
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


## 合并所有要查找的 string.xml 字符串
def merge_string_id(string_xml_list):
    print(f"\n============= 2.strings.xml 开始合并： =============")
    ticks = time.time()
    file_path = "string_find.txt"
    with open(file_path, 'w') as file_write:
        for file_name in string_xml_list:
            with open(file_name, 'r', encoding='utf-8') as file_read:
                for line in file_read:
                    id_str = extract_string_name_from_line(line.strip())
                    if len(id_str) > 0:
                        file_write.write(f"{id_str}\n")
    spd = time.time() - ticks
    print(f"============= 2.strings.xml 合并完成 {spd}： =============")
    return file_path



## 入口函数，开始查找
def search_no_user_id(folder):
    # 指定要写入的文件路径
    file_path = "record.txt"
    all_no_used_id = []

    ## 1.获取所有的 string.xml 文件
    string_xml_list = find_strings_xml(folder)

    ## 2.合并所有的 string.xml 到一个文件
    file_name = merge_string_id(string_xml_list)

    ## 3.读取这个文件，看文件里面内容，项目中是否存在
    no_use_string = search_lines_in_directory(file_name, folder)
    all_no_used_id.append(no_use_string)


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





