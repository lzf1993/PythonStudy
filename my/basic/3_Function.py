
import math

# ---------------------- 1.内置函数 -------------------------
# http://docs.python.org/3/library/functions.html#abs


a = abs(100)

# 取最大的
b = max(2, 3, 1, -5)

# 计算平方根可以调用math.sqrt()函数：
math.sqrt(2)


# ---------------------- 2.定义函数 -------------------------


# 1.定义函数
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x


# 2.定义空函数
# 比如现在还没想好怎么写函数的代码，就可以先放一个pass，让代码能运行起来。
def nop():
    pass


# 3.定义函数，判断类型
def my_abs2(x):

    ## 如果不是 int 、float 类型，则
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x


## 4.多个返回值， 返回的是 一个tuple
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny

x, y = move(100, 100, 60, math.pi / 6)
print(x, y)



## 5.默认参数
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s


## 6. 可变参数
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
calc(1, 2)


## 7. 关键字参数
# 可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。
# 而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。请看示例：

def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

person('Bob', 35, city='Beijing')





## 8. 命名关键字参数
# 对于关键字参数，函数的调用者可以传入任意不受限制的关键字参数。至于到底传入了哪些，就需要在函数内部通过kw检查。
# 仍以person()函数为例，我们希望检查是否有city和job参数：


def person(name, age, **kw):
    if 'city' in kw:
        # 有city参数
        pass
    if 'job' in kw:
        # 有job参数
        pass
    print('name:', name, 'age:', age, 'other:', kw)

person('Jack', 24, city='Beijing', addr='Chaoyang', zipcode=123456)



## 9. 参数组合
## 在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，这5种参数都可以组合使用。
# 但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。

def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

f1(1, 2, 3, 'a', 'b', x=99)



