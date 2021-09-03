def func(*args):
    '''receives anry number of input argument, and converted to a tuple
    '''
    print('type of args: ',type(args))
    print(args)

    #print('type of *args: ',type(*args))
    print(*args)
  


def func2(**args):
    '''receive any number of map object, and converted to a dictionary object
    '''
    print('type of args: ',type(args)) 
    print(args)
    for key in args.keys():
        print(args[key])

    #print('type of *args: ',type(**args))
    #print(**args)


# func(1,2,3)

# func2(a=1,b=2,c=3)

func('1','2','3')
func2(a='1',b='2',c='3')


