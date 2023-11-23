
## --------------------  1. 基本数据类型  --------------------


print(""
      "------------- 基本数据类型 -----------")

# 基本数据类型
a = 100 + 200 + 300
print(a)

# boolean
b = 3 > 7
print(b)

c = 'char'

# 大写表示
PI = 3.1415926


# 在Python中，有两种除法，
# 一种除法是/：除法计算结果是浮点数，即使是两个整数恰好整除，结果也是浮点数：
# 还有一种除法是//，称为地板除，两个整数的除法仍然是整数： 除法只取结果的整数部分



## --------------------  2. 字符串  --------------------


print(""
      "------------- 字符串 -----------")

# \ 表示转义符合
print('I\'m ok.')


# 直接换行
print('''line1
... line2
... line3''')




## --------------------  5.条件判断  --------------------


print(""
      "------------- 条件判断 -----------")

age = 3
if age >= 18:
    print('your age is', age)
    print('adult')
else:
    print('your age is', age)
    print('teenager')

print(""
      "")


## --------------------  6. 模式匹配  --------------------

"""
score = 'B'
match score:
    case 'A':
        print('score is A.')
    case 'B':
        print('score is B.')
    case 'C':
        print('score is C.')
    case _: # _表示匹配到其他任何情况
        print('score is ???.')
"""



## --------------------  7. 循环  --------------------
# Python的循环有两种，
# 一种是for...in循环，依次把list或tuple中的每个元素迭代出来，看例子：
# 第二种循环是while循环，只要条件满足，就不断循环，条件不满足时退出循环

print(""
      "------------- 循环 -----------")

names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)


sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)


n = 1
while n <= 100:
    if n > 10:  # 当n = 11时，条件满足，执行break语句
        break # break语句会结束当前循环
    print(n)
    n = n + 1
print('END')


n = 0
while n < 10:
    n = n + 1
    if n % 2 == 0: # 如果n是偶数，执行continue语句
        continue  # continue语句会直接继续下一轮循环，后续的print()语句不会执行
    print(n)

print(""
      "")









