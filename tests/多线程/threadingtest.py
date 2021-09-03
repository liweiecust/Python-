import _thread
import random
import time
import threading

lock=threading.Lock()

def fun():
    for i in range(3600):
        None
        #lock.acquire()
        #print(i)  #print 时could not acquire lock for <_io.BufferedWriter name='<stdout>'> at interpreter shutdown
        #lock.release()
    time.sleep(1)
    print(threading.current_thread().name,time.time())

# for i in range(12):
#     time.sleep(1)
#     _thread.start_new_thread(fun,("thread %s:" % i,))

# # 为线程定义一个函数
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# # 创建两个线程
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print ("Error: 无法启动线程")

# while 1:
#    pass

for i in range(10):
    thread_list=[]
    t=threading.Thread(target=fun)
    t._started.wait()
    #thread_list.append(t)
    #t.start()
 

for t in thread_list:
    
    t.start()
    
time.sleep(10)


######################################################## correct ! 各线程正常启动
def fun():
    for i in range(3600):
        None
    time.sleep(1)
    print(threading.current_thread().name,time.time())


for i in range(10):
    t=threading.Thread(target=fun)
    t.start()
 

#################################################################################


######################################################## wrong !

for i in range(10):
    thread_list=[]
    t=threading.Thread(target=fun)
    thread_list.append(t)

for t in thread_list:
    
    t.start()

#################################################################################
