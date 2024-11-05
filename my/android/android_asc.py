# 3rd party modules

# internal modules

# 相关文档 https://github.com/androguard/androguard

from androguard.core.axml import ARSCParser
from androguard.core.apk import APK
from lxml import etree


# 定义解析 arsc 文件的函数，实现：删除无用资源后的项目中，是否还有被删除的资源，有的话，则说明有第三方用到了
def parse_arsc(apk_path):

    apk = APK(apk_path)
    parser = apk.get_android_resources()

    # 获取所有的字符串资源
    all_strings = ['']

    # 获取包名
    package = parser.get_packages_names()[0]
    tree = etree.fromstring(parser.get_string_resources(package, "\x00\x00"))
    for elem in tree.iter():
        if elem.tag == 'string':
            res = elem.text
            name = elem.get("name")
            all_strings.append(name)

    # 将所有字符串写入文件
    output_file = '../files/android_strings_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for s in all_strings:
            f.write(f"{s} \n")

    print(f"\n 所有字符串已写入到 {output_file} ")



if __name__ == '__main__':
    # 调用解析函数
    parse_arsc("/Users/lzf2/Downloads/4720011.apk")








