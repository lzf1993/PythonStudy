# -*- coding: utf-8 -*-
"""
@Time ： 2023/9/19 11:57 AM
@Auth ： liunian
@File ：return_card.py
@IDE ：PyCharm
@mail：1439503908@qq.com
"""
#退卡

import requests
import json

def return_card(uid):

  url = "http://43.157.137.145:14498/http_to_tcp?lang=&command=20&type=403&app_version=4.3.2&uid={}&rid=11171456".format(uid)

  payload = "{\n    \"op_type\": 2\n}"
  headers = {
    'Content-Type': 'text/plain'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)

if __name__ == '__main__':
    num=400
    while num<495:
      return_card(num)
      num+=1