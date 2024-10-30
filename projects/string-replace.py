# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import shutil
import sys
from xml.dom import minidom

# 目录文件夹
# source_dir = r'/Users/yuqiubo/Public/work/sgg-android-backup'
source_dir = r'/Users/yuqiubo/Public/work/sgg-android-backup'
# 已翻译的目标语言文件
str_file_my = r'/Users/yuqiubo/Public/work/sgg-android-backup/zh-strings.xml'
# 从哪种语言获取拷贝
old = "-ms"
# 新建何种语言
now = "-id"

def create_new_language():
    filenames_set = getFileList(old)
    copyFile(filenames_set, old, now)
    filenames_set_my = getFileList(now)
    reWriteStrings(filenames_set_my)
    delete_blank_lines(filenames_set_my)

# 找到工程下带有"langValue"标志的翻译文件，如"-th"、"-en"、"-ar"
def getFileList(langValue):
    filename_set = set()
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for file in filenames:
            if file.endswith(".xml") and file.__contains__("str") \
                    and not file.__contains__("hwpush") and dirpath.__contains__(langValue):
                filename_set.add(dirpath + '/' + file)
                # print("file = %s" % file)
    return filename_set

# 删除路径包含name的空文件夹
def delete_empty_folder(name):
    for dirpath, dirnames, filenames in os.walk(source_dir):
        if dirpath.__contains__(name) and len(os.listdir(dirpath)) == 0:
            os.removedirs(dirpath)


# 根据原有的翻译文件，复制得到新语音翻译的xml文件，为之后的替换翻译内容做准备（开新服时会用到）
def copyFile(filenames_set, original, now):
    copy_num = 0
    for filename in filenames_set:
        oldname = filename
        newname = filename.replace(original, now)
        # print("filename = %s" % oldname)
        # print("filename = %s" % newname)
        dir, strfile = os.path.split(newname)
        if not os.path.exists(dir):
            os.makedirs(dir)
        if os.path.exists(newname):
            print('%s already exist!' % newname)
            continue
        try:
            shutil.copyfile(oldname, newname)
            print('file %s %s!' % (newname, 'copy over'))
            copy_num = copy_num + 1
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            exit(1)
    print("copy over num = %s" % copy_num)


# 删除所给目录的文件
def delete_file(filenames_delete):
    for file_del in filenames_delete:
        os.remove(file_del)


# 根据需要替换的翻译文件路径，和已经翻译好的一个xml文件，得到所需新语言翻译
def reWriteStrings(filenames_set_my):
    dom_tree_total = minidom.parse(str_file_my)
    root_node_total = dom_tree_total.documentElement
    strings_total = root_node_total.getElementsByTagName("string")
    plurals_total = root_node_total.getElementsByTagName("plurals")
    string_arrays_total = root_node_total.getElementsByTagName("string-array")

    for filename in filenames_set_my:
        # filename = "/Users/wepie/Documents/project/os-dev/wejoy/wepie/res/values-my/strings_games.xml"
        print(filename)

        dom_tree = minidom.parse(filename)
        root_node = dom_tree.documentElement
        strings = root_node.getElementsByTagName("string")
        plurals = root_node.getElementsByTagName("plurals")
        string_arrays = root_node.getElementsByTagName("string-array")

        for str in strings:
            if str.hasAttribute("name"):
                print("string key:", str.getAttribute("name"), "len = ", len(str.childNodes))
                if str.getAttribute("name") == "snatch_song_result_dialog_2":
                    print("continue")
                    continue
                for str_total in strings_total:
                    if str_total.hasAttribute("name") and str_total.getAttribute("name") == str.getAttribute("name"):
                        print("string_total key:", str_total.getAttribute("name"))

                        if len(str.childNodes) > 0:
                            str.childNodes[0].data = str_total.childNodes[0].data

        for plur in plurals:
            if plur.hasAttribute("name"):
                print("plur key:", plur.getAttribute("name"))
                for plur_total in plurals_total:
                    if plur_total.hasAttribute("name") and plur_total.getAttribute("name") == plur.getAttribute("name"):
                        print("plur_total key:", plur_total.getAttribute("name"))
                        item = plur.getElementsByTagName("item")[0]
                        item_total = plur_total.getElementsByTagName("item")[0]
                        item.childNodes[0].data = item_total.childNodes[0].data
                        print("item.data = {}, item_total.data = {}", item.childNodes[0].data,
                              item_total.childNodes[0].data)

        for str_array in string_arrays:
            if str_array.hasAttribute("name"):
                print("str_array key:", str_array.getAttribute("name"))
                for str_array_total in string_arrays_total:
                    if str_array_total.hasAttribute("name") and str_array_total.getAttribute("name") == str_array.getAttribute("name"):
                        print("str_array key:", str_array_total.getAttribute("name"))
                        item = str_array.getElementsByTagName("item")
                        item_total = str_array_total.getElementsByTagName("item")
                        for idx, val in enumerate(item):
                            item[idx].childNodes[0].data = item_total[idx].childNodes[0].data
                            print("item.data = {}, item_total.data = {}", item[idx].childNodes[0].data,
                                  item_total[idx].childNodes[0].data)

        with open(filename, 'w', encoding='utf-8') as f:
            dom_tree.writexml(f, addindent='    ', newl='\n', encoding="utf-8")


# 规范xml文件格式，删除无用空行，内容每行开始默认空4个空格
def delete_blank_lines(filenames_set_my):
    for file in filenames_set_my:
        # file = '/Users/wepie/Documents/project/os-dev/lib/hwconstants/src/main/res/values-my/strings_games.xml'
        readfile = file.replace("str", "strr")
        writefile = file
        shutil.copyfile(file, readfile)

        with open(readfile, 'r', encoding='utf-8') as fr, open(writefile, 'w', encoding='utf-8') as fd:
            for text in fr.readlines():
                if text.split():
                    fd.write(text)
                    # print('write 成功....')
        os.remove(readfile)
        print('write 成功....')

if __name__ == '__main__':
    create_new_language()

