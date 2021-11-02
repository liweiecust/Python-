# 协程
import requests
from datetime import date, datetime

def time_elapsed(func,*args):
    # decorator: meassure time elapsed
    def inner_func(*args):
        t1=datetime.now()
        func()
        delta_t=(datetime.now()-t1).seconds
        print("%s seconds elapsed" % delta_t)
    return inner_func


def invoke_request(url,method,headers,params=None):
    if method=="get":
        r= yield requests.get(url,headers=headers)
        print(r.text)
       
    elif method=="post":
        r= yield requests.post(url,headers=headers,data=params)
        print(r.text)

    else:
        Exception("method not supported")
    

@time_elapsed
def producer(): 
   
    url="http://www.baidu.com"
    # for i in range(100):
    #     ge=invoke_request(url,"get",headers={})
    #     next(ge)
  
    ge=(invoke_request(url,"get",headers={}) for x in range(100))
    for i in ge:
        next(ge)
    print('finished')

producer()
            