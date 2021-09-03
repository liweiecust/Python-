class base():

    def __init__(self):
        print('base')
        self.b=1
        print(self.b)

class sub(base):

    def __init__(self):
        print('sub')
        self.b=2
        super().__init__()
        print(self.b)



d={'k1':'0','k2':1,'k3':None}

def func(**args):
    args=dict(*args)
    d.update(args)
    print(d)

args={'k2':'k','k3':'a','k4':4}
d={'k1':'0','k2':1,'k3':None}
#ret_list = list(set(args)^set(d))

#print(ret_list)
n=[{'a':1},{'b':23}]
n.remove({'a':10})
print(n)
