'''
列表去重：
1. 放入set
2.放入dictionary
3.clone列表，使用for循环遍历，删除重复元素

'''

'''
1. 不爱总结
2. 对任务所需时间有错误认识

多任务处理
4.总结，查漏补缺

'''
from collections.abc import Iterable,Iterator

my_list=[1,2,3]
print(isinstance(my_list,Iterator)) # return False
print(isinstance(my_list,Iterable)) # return True


'''
迭代器协议：
含有__iter__(), __next__()方法的就是迭代器

可迭代对象：
含有__iter__()方法（可以使用for循环）
'''
'''
迭代器：节省内存
'''
my_itor=iter([1,2,3]) # receive Iterable object,调用__iterator__()生成迭代器
while True:
    try:
        x=next(my_itor)
    except StopIteration:
        break
''' for 循环Iterable对象时，是先将其变为iterator,再调用next函数
'''
for i in my_itor:
    print(i)