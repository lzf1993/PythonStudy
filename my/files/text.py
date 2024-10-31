

# -*- coding: utf-8 -*-
"""
@Time ： 2023/9/19 11:57 AM
@Auth ： liunian
@File ：return_card.py
@IDE ：PyCharm
@mail：1439503908@qq.com
"""
import xml.etree.ElementTree as ET
import re


if __name__ == '__main1__':
    fs1 = open("/Users/lzf2/PycharmProjects/PythonStudy/my/files/21.txt", 'r')
    fs2 = open("/Users/lzf2/PycharmProjects/PythonStudy/my/files/23.txt", 'w')
    try:
        for line in fs1:
            if r'\d+\r' in line:
                s = re.sub(r'\d+\r', "", line)
            else:
                s = re.sub(r'\d+', "", line)
            fs2.write(s)
    finally:
        if fs1:
            fs1.close()
        if fs2:
            fs2.close()






from lxml import etree

def remove_element_and_preserve_comments(xml_file, target_string):
    tree = etree.parse(xml_file)
    elements_to_remove = tree.xpath(f"//*[contains(text(), '{target_string}')]")
    for element in elements_to_remove:
        element.getparent().remove(element)

    # 将 XML 转换为字符串，保留特殊字符实体
    xml_str = etree.tostring(tree, encoding='unicode', method='xml', pretty_print=True)

    # 写入 XML 文件
    with open(xml_file, "w", encoding="utf-8") as file:
        file.write(xml_str)



def delete_lines_with_string(file_path, target_string):
    # 读取原始文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 构建要查找的字符串
    target_string = f'<string name="{target_string}">'

    # 查找包含目标字符串的行并删除包含该字符串的行及其所在的 <string> 开头 </string> 结尾的内容
    filtered_lines = []
    skip_line = False
    for line in lines:
        if target_string in line:
            skip_line = True
        if not skip_line and not line.strip().startswith("</string>"):
            filtered_lines.append(line)
        if skip_line and line.strip().endswith("</string>"):
            skip_line = False

    # 将修改后的内容写回文件
    with open(file_path, 'w') as file:
        file.writelines(filtered_lines)
    print(f"Lines containing '{target_string}' and surrounding <string> tags deleted successfully.")


if __name__ == '__main__':
     xml_file = "/Users/lzf2/Documents/weipai/wejoy_us/wejoy/wepie/res/values/strings.xml"
     target_string = "report_long_text_des1"

     # 删除文件中包含指定字符串的行
     delete_lines_with_string(xml_file, target_string)




