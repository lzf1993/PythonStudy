
## 替换 csv 中某一列为 另一个的某一列

import pandas as pd

## 没改之前的文件
file1 = "in_app_products_com.wejoy.weplay.ru_old.csv"

## 改了之后的文件
file2 = "in_app_products_com.wejoy.weplay.ru_new.csv"
data1 = pd.read_csv(file1, encoding='utf-8')
data2 = pd.read_csv(file2, encoding='utf-8')

# 改了之后文件的 id 用 老文件 id 替换，因为 id 有问题
data2['Pricing Template ID'] = data1['Pricing Template ID']

data2.to_csv(file2, index=False, encoding='utf-8')
