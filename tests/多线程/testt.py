import _thread
import random
import time
import threading

def fun():
    time.sleep(1)
    print(threading.current_thread().name,time.time())


 
thread_list=[]

for i in range(10):
    
    t=threading.Thread(target=fun)
    thread_list.append(t)

for t in thread_list:
    print(t)   
    #t.start()

# for i in range(10):
#     t=threading.Thread(target=fun)
#     t.start()

