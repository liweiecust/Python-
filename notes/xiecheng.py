# 协程只是程序调度的方式，
# 多线程和多进程由操作系统调度，而协程由程序自身即程序员调度，仅此而已。
# 异步io指的程序不会等待io操作返回结果，继续执行，
# 所以我们通过协程调度，然后让cup去执行别的代码，等io结束再切换回来，
# 其实就只是增加cup的利用。io不是cpu在干活，而是磁盘网络之类，
# 正是因为cpu的速度远高于磁盘及网络，所以我们通过异步的方式来io，
# 就是io的时候不让cpu傻站着等，io结束后，需要io结果的代码需要接着执行，
# 所以需要使用协程切换回来，协程只是可以让程序在某个地方停下来，
# 然后在需要的时候(io完成后)再接着执行。
def consumer():
    r = ''
    print("start consumer")
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)  # consumer代码执行到 n = yield r，遇到yield时返回，n未赋值
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)           #yield 表达式的值，作为send()函数的返回值
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)