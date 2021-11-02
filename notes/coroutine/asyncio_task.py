import asyncio
import os,sys
sys.path.append(os.getcwd())
from common.baseFunctions import time_elapsed
import time

# 函数定义时用async声明就定义了一个协程
async def say_after(delay,what):
    await asyncio.sleep(delay)
    print(what)

print(type(say_after))

# 等待一个协程
async def main1():
    print(f"started at {time.strftime('%X')}")
    await say_after(1,'hello')
    await say_after(2,'world')
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main1())

# 并发运行两个say_after协程

# @time_elapsed
async def main():   # main比main1快1秒
    print(f"started at {time.strftime('%X')}")
    task1=asyncio.create_task(
        say_after(1,'hello')
    )
    task2=asyncio.create_task(
        say_after(2,'world')
    )
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
    
