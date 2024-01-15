

# -*- coding: utf-8 -*-
"""
@Time ： 2023/9/19 11:57 AM
@Auth ： liunian
@File ：return_card.py
@IDE ：PyCharm
@mail：1439503908@qq.com
"""

import re


if __name__ == '__main__':
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


