# 协程
import requests
from datetime import date, datetime
import asyncio



def time_elapsed(func,*args):
    # decorator: meassure time elapsed
    def inner_func(*args):
        t1=datetime.now()
        func()
        delta_t=(datetime.now()-t1).seconds
        print("%s seconds elapsed" % delta_t)
    return inner_func


async def invoke_request(url,method,headers,params=None):
    if method=="get":
        r= requests.get(url,headers=headers)
        # print(r.text)
       
    elif method=="post":
        r= requests.post(url,headers=headers,data=params)
        # print(r.text)

    else:
        Exception("method not supported")
    

@time_elapsed
def producer(): 
   
    url="http://www.baidu.com"
    # for i in range(100):
    #     ge=invoke_request(url,"get",headers={})
    #     next(ge)
        
    tasks=[invoke_request(url,"get",headers={}) for x in range(1000)]
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    print('finished')

producer()
            