import asyncio
import time

# 协程 通过 async/await 语法进行声明，是编写 asyncio 应用的推荐方式 需要python 3.7

# 在协程中如果要调用另一个协程就使用await。要注意await关键字要在async定义的函数中使用，而反过来async函数可以不出现await

# 运行协程的方式

# 1、asyncio.run()
# 2、事件循环

async def main():
    print('hell0')
    await asyncio.sleep(1)
    print('world')

async def test(): #仅仅调用test()不会执行
    print('1112')

# asyncio.run(main()) #asyncio.run将运行传入的协程，负责管理asyncio事件循环

# 当一个协程通过 asyncio.create_task() 等函数被封装为一个 任务，该协程会被自动调度执行:

# asyncio.run(test())


# 2、事件循环
# 其实翻阅源码可知asyncio.run()的实现也是封装了loop对象及其调用。而asyncio.run()每次都会创建一个新的事件循环对象用于执行协程。

task=[main() for i in range(5)] # 生成器生成多个协程对象
loop =asyncio.get_event_loop() # 获取事件循环对象
loop.run_until_complete(asyncio.wait(task)) # 事件循环中执行task
loop.close()

# 可等待对象awaitable
# 协程coroutine,任务task,future, 这些对象可以使用await关键字进行调用
# 使用await关键字才会执行一个协程函数返回的协程对象

# Task 并发执行协程。asyncio.create_task()将一个协程对象封装成任务，该任务会被排入调度队列并执行

