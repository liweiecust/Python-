# 类装饰器
def deco_wrapper(cls):
    def inner():
        print('deco')
        cls()
    return inner

@deco_wrapper
class testDeco():

    def __init__(self,args=None):
        if args is not None:
            self.path=args

    def test(self):
        print(self.path)

t=testDeco()
t.test()

    