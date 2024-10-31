

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


def remove_element_by_string(xml_file, target_string):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for element in root.findall(".//string"):
        if target_string in element.attrib.get('name', ''):
            root.remove(element)

    tree.write(xml_file, encoding='utf-8', xml_declaration=True, method="xml")




if __name__ == '__main__':
     xml_file = "/Users/lzf2/Documents/weipai/wejoy_us/wejoy/module/rank/src/main/res/values-es/strings.xml"
     target_string = "couple_rank_item_love_value_x"
     remove_element_by_string(xml_file, target_string)



