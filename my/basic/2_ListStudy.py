
"""
`list`（列表）是一种有序的可变序列，可以存储任意类型的元素。列表使用方括号`[]`来表示，元素之间用逗号`,`分隔。列表支持索引、切片、添加、删除、修改等操作，是Python中最常用的数据类型之一。

`tuple`（元组）是一种有序的不可变序列，可以存储任意类型的元素。元组使用圆括号`()`来表示，元素之间用逗号`,`分隔。元组支持索引、切片等操作，但不支持添加、删除、修改等操作。元组通常用于存储不可变的数据，如坐标、颜色等。

`dict`（字典）是一种无序的键值对集合，可以存储任意类型的键和值。字典使用花括号`{}`来表示，每个键值对之间用冒号`:`分隔，键值对之间用逗号`,`分隔。字典支持通过键来访问值，也支持添加、删除、修改等操作。字典通常用于存储具有映射关系的数据，如姓名和电话号码的对应关系。

`set`（集合）是一种无序的元素集合，可以存储任意类型的元素。集合使用花括号`{}`来表示，元素之间用逗号`,`分隔。集合支持添加、删除、交集、并集、差集等操作。集合通常用于去重、交集、并集等操作。

需要注意的是，`list`、`tuple`、`dict`和`set`是不同的数据类型，它们之间不能直接进行转换。如果需要将它们之间进行转换，需要使用相应的转换函数，如`list()`、`tuple()`、`dict()`和`set()`。

"""

## --------------------  3. list  --------------------
# list 是一个可变的有序表，所以，可以往list中追加元素到末尾：


print(""
      "------------- list -----------")

classmates = ['Michael', 'Bob', 'Tracy']

print(classmates[0])
print(classmates[1])
# 倒数第一个元素
print(classmates[-1])
# 追加元素
classmates.append('Adam')

# 删除末尾元素
classmates.pop()

# 删除指的元素
classmates.pop(1)

# 替换指定元素
classmates[1] = 'Sarah'

print(classmates)


print(""
      "")

## --------------------  4. tuple  --------------------
# 另一种有序列表叫元组：tuple。tuple和list非常类似，但是tuple一旦初始化就不能修改，比如同样是列出同学的名字：


print(""
      "------------- tuple -----------")

classmates2 = ('Michael', 'Bob', 'Tracy')

# 如果要定义一个空的tuple
t = ()

# 要定义一个只有1个元素的tuple，
t2 = (1,)

print(""
      "")



## --------------------  5. map  --------------------
# Python 内置了字典：dict 的支持，dict 全称 dictionary，在其他语言中也称为 map，使用键-值（key-value）存储，具有极快的查找速度。


print(""
      "------------- map -----------")

d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Michael'])

# 修改元素
d['Adam'] = 67

# 判断 key 是否存在
if 'Thomas' in d:
    print(d['Thomas'])
else:
    d['Thomas'] = 88
    print(d['Thomas'])

# 通过 get 方式获取，如果不存在，则使用后面的 默认值
d.get('Thomas', -1)

# 删除元素
d.pop('Bob')



## --------------------  5. set  --------------------
# set 和 dict 类似，也是一组 key 的集合，但不存储 value。由于 key 不能重复，所以，在 set 中，没有重复的 key。
# set 可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：

s = {1, 2, 3}
s2 = {1, 2, 3}
s.add(4)
s.remove(4)

# 做并集
a = s & s2
# 做交集
b = s | s2

