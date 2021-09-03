from locust import HttpUser,between,task
import os
# from open_performance_test.openApi import post_data
import time


# HttpLocust 这个类的作用是用来发送http请求的
# between   这个类是定义用户行为的，相当于loadrunnerhttp协议的脚本，jmeter里面的http请求一样
# task   这个task是一个装饰器，它用来把一个函数，装饰成一个任务，也可以指定他们的先后执行顺序

class BestTest(HttpUser):
    # wait_time=between(1,5)
    def on_start(self):
        pass

    def on_stop(self):
        pass

    # 压测开放平台接口
    @task
    def search(self):
        req = self.client.post(url='/open.api',
                               data={},
                               headers={"Content-Type": "application/x-www-form-urlencoded"})
        if req.status_code != 200:
            # print(f"请求异常：{req.json()}")
            print("request finished")
        time.sleep(1)



# class BestTestIndexUser(HttpUser):
#     task_set = BestTest
#     host = "https://ibuildapi.yzw.cn"
#     min_wait = 1000
#     max_wait = 3000


if __name__ == "__main__":
    # os.system("py -m locust -f locust_run.py -H https://ibuildapi.yzw.cn -u 100 -r 10 --web-host=127.0.0.1")
    os.system("py -m locust -f locust_run.py -H https://ibuildapi.yzw.cn --web-host=127.0.0.1")