
## 替换 csv 中某一列为 另一个的某一列

import pandas as pd
file1 = "us.csv"
file2 = "ru.csv"
data1 = pd.read_csv(file1, encoding='utf-8')
data2 = pd.read_csv(file2, encoding='utf-8')

data2['Pricing Template ID'] = data1['Pricing Template ID']

data2.to_csv(file2, index=False, encoding='utf-8')
