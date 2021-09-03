# class path(path='/api/queryUserList'):
#     def __init__(self, func):
#         self._func = func

#     def __call__(self,args):
#         print ('class decorator runing')
#         self._func(args)
#         print ('class decorator ending')

# @path(path='/api/queryUserList')
# def bar(args):
    
#     print ('bar',args)

global path
def path_deco(args):
    path=args
    def wrapper_func(func):
        print('2')
        def inner_func(*args):
            
            print('3')
            func()
        return inner_func
    return wrapper_func



@path_deco(args='/api/queryUserList')
def func_t():
    print('path:',path)



class TestDeco():
    
    @path_deco(args='/api/queryUserList')
    def func_a():
        print('4')
        print('path:')


a=TestDeco()
a.func_a()
#bar('iron')