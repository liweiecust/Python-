'''
生成器是返回迭代器的函数（使用yield关键字的函数）



yield返回一个值，并且记住这个返回的位置，下次迭代时，代码从yield的下一条语句开始执行
.send() 和next()一样，都能让生成器继续往下走一步（下次遇到yield停），但send()能传一个值，这个值作为yield表达式整体的结果
yield 表达式的值，作为send()函数的返回值

列表解析式：
li=[x*x for x in range(10)]
生成器表达式：
ge=(x*x for x in range(10))
'''

def generator():
    print("start")
    yield 2
    print("ite2")
    yield 1
print(type(generator())) #<class 'generator'>

ge=generator() # 生成生成器


# while True:
#     print(ge)
#     next()

# for循环遍历生成器返回的值
# for i in ge:
#     print(i)

