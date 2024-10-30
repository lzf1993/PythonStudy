import os
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom


def extract_strings_from_xml(xml_path):
    """从XML文件中提取字符串资源，返回所有<string>, <string-array>和<plurals>标签"""
    with open(xml_path, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        all_strings = {}

        # 提取<string>标签
        for string_elem in root.findall('string'):
            all_strings[string_elem.attrib['name']] = string_elem

        # 提取<string-array>标签
        for array_elem in root.findall('string-array'):
            all_strings[array_elem.attrib['name']] = array_elem

        # 提取<plurals>标签
        for plurals_elem in root.findall('plurals'):
            all_strings[plurals_elem.attrib['name']] = plurals_elem

        return all_strings


def pretty_xml(element):
    """返回格式化的XML字符串，同时保持原始文本内容"""
    raw_string = ET.tostring(element, 'utf-8')
    reparsed = xml.dom.minidom.parseString(raw_string)
    return reparsed.toxml().replace('&quot;', '"')


def main():
    project_dir = "/Users/lzf2/Documents/weipai/wejoy_ar/wejoy"  # 请替换为你的项目目录
    excluded_directories = {'build', 'libsdk'}  # 添加不想扫描的目录
    zh_strings = {}
    ja_strings = {}

    # 遍历项目目录，提取values-zh和values-ja中的字符串资源
    for subdir, _, files in os.walk(project_dir):
        # 如果路径中有排除的目录名，跳过
        if any(excluded_dir in subdir for excluded_dir in excluded_directories):
            continue

        for file in files:
            if file.endswith('.xml'):
                xml_path = os.path.join(subdir, file)
                if 'values-ja' in subdir:
                    zh_strings.update(extract_strings_from_xml(xml_path))
                elif 'values-ms' in subdir:
                    ja_strings.update(extract_strings_from_xml(xml_path))

    # 找到在values-zh中存在，但在values-ja中不存在的字符串资源
    missing_strings = {key: val for key, val in zh_strings.items()
                       if key not in ja_strings or
                       (key in ja_strings and (ja_strings[key].text is None or not ja_strings[key].text.strip()))}

    # 创建新的XML资源文件
    output_root = ET.Element('resources')
    for key, elem in missing_strings.items():
        # 检查并确保string元素的文本没有日文字符
        if elem.tag == 'string' and elem.text:
            output_root.append(elem)
        # 对于string-array和plurals，检查每个item
        elif elem.tag in {'string-array', 'plurals'}:
            if list(elem):  # 如果还有元素，添加到输出
                output_root.append(elem)

    # 格式化XML并保存到文件
    with open("ja_without_ms.xml", 'w', encoding='utf-8') as f:
        f.write(pretty_xml(output_root))


if __name__ == '__main__':
    main()
