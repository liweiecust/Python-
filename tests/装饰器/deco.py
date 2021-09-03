# 函数装饰器



# simple decorator
def outter_func(func):
    def inner_func():
        print('%s is called' % func.__name__)
        func()
        
    return inner_func

@outter_func
def sayHi():
    print("hi cava")

sayHi()  
# 装饰器是一个语法糖，等效于以下代码 
# sayHi=outter_func(sayHi)
# sayHi()


# decorate function which receives parameters
def outter_func2(func):
    def inner_func(greeting):
        print('%s is called' % func.__name__)
        func(greeting)
        
    return inner_func

@outter_func2
def sayHi2(greeting):
    print("hi cava:%s" % greeting)

#sayHi2=outter_func_2(sayHi2)
sayHi2("mm")


# decorator which receives parameters
def out_out_func(name):
   
    def outter_func(func):
        def inner_func(greeting):
            print(name)
            print('%s is called' % func.__name__)
            func(greeting)
            
        return inner_func
    return outter_func



@out_out_func("name2")
def sayHi3(greeting):
    print("hi cava:%s" % greeting)


sayHi3("xd")

# 
# @a
# @b
# @c
# def f ():
#     pass
#     它的执行顺序是从里到外，最先调用最里层的装饰器，最后调用最外层的装饰器，它等效于

# f = a(b(c(f)))

def login(func):
    def inner(orgCode,header=None):
        header="1"
        func(orgCode,header)
    return inner


@login
def queryProjectList(orgCode,header=None):
    print("queryProject")
    print("header in queryProjectLIst %s" % header)
    pass





# queryProjectList("0001")

def t():
    print("%s" % __name__ )
    header="12"
    queryProjectList("0001",header=header)
# t()

def login2(func):
    def inner(*args):
        header="1"
        func(*args)
    return inner
    

@login2
def queryProjectList2(*args):
    print("queryProject")
    print("header in queryProjectLIst %s" % header)
    pass

# queryProjectList2("0001")