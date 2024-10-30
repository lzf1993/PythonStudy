# -*- coding: utf-8 -*-
"""
@Time ： 2023/9/18 4:15 PM
@Auth ： liunian
@File ：bingo_test.py
@IDE ：PyCharm
@mail：1439503908@qq.com
"""

import requests
import json
import time

def buy_card(uid):

  url = "http://43.157.137.145:14498/http_to_tcp?uid={}&rid=11317577&lang=en&app_version=4.3.2&command=20&type=403".format(uid)
  payload = json.dumps({
    "op_type": 1,
    "card_id": [
      1
    ]
  })
  headers = {
    'Content-Type': 'application/json',
  }
  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)

if __name__ == '__main__':
    num=400
    while num<495:
      buy_card(num)
      num+=1