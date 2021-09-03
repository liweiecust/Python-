import pymongo
import time
import _thread
from dateutil import parser
import datetime
import random
import urllib
import threading
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor,as_completed


# password=urllib.parse.quote("yzw@123")
# client=pymongo.MongoClient("mongodb://admin:%s@172.16.0.137:20200/" % password)
# db=client.ibuild_data
# db=db["tower_crane"]





data={
    "warning" : "00000000000000000000000000000000",
    "override" : 0,
    "liftingCapacity" : 3.37,
    "safeLiftingCapacity" : 18.44,
    "ratedMoment" : 23.2,
    "momentPercent" : 79.46,
    "amplitude" : 0.72,
    "round" : 196.14,
    "height" : 137.32,
    "dipAngleX" : 69.54,
    "dipAngleY" : 97.26,
    "windSpeed" : 0.27,
    "driverId" : "210381197006269007",
    "driverName" : "钱强",
    "needWarning" : False,
    "projectSysNo" : 10078,
    "deviceId" : "201811201952",
    "deviceTime" : "2019-07-01T11:24:46.000Z"
   
}

def getDbInstance():
    password=urllib.parse.quote("yzw@123")
    client=pymongo.MongoClient("mongodb://admin:%s@172.16.0.137:20200/" % password)
    db=client.ibuild_data
    #db=db["tower_crane"]
    #db=db["liwei_test"]
    return db

def dataFactory(data,capacity,deviceId,driver,projectSysNo,deviceTime):
    data.update({"deviceId":deviceId})
    data.update({"projectSysNo":projectSysNo})
    data.update(driver)
    data.update({"liftingCapacity":capacity})
    data.update({"deviceTime":deviceTime})
    data.update({"_id":ObjectId()})
    return data
    
def getDriver(db):
   
    drivers=db["tower_crane"].find().limit(1000)
    index=random.choice(range(1000))
    driver=drivers[index]
    result={}
    try:
        result={"driverId":driver["driverId"],"driverName":driver["driverName"]}
    except Exception as e:
        print(index)
        print(driver)
        print(e)
    return result

def randStr(num):
    array="1234567890qazwsxedcrfvtgbyhnujmiklop"
    res=""
    for i in range(num):
        res+=random.choice(array)
    return res

def insert_data(db,data,capacity,deviceId,projectSysNo,deviceTime):
    
    driver=getDriver(db)
    #driver={"driverId":"12345","driverName":"liwei"}
    data=dataFactory(data,capacity,deviceId,driver,projectSysNo,deviceTime)
    try:
        db["liwei_test"].insert_one(data)
    except Exception as e:
        print(e)

def func(data,deviceId,projectSysNo,startTime):
    '''
    delTa 插入数据时间间隔，秒
    '''
    deltaT=1
    db=getDbInstance()
    N=int(2*3600/deltaT)
    capacity_array=[0,5,12,20]
    for i in range(N):
        deviceTime=startTime+datetime.timedelta(seconds=i*deltaT)
        capacity=capacity_array[i%4]
        insert_data(db,data,capacity,deviceId,projectSysNo,deviceTime)

if __name__ == "__main__":
   
    t1=time.time()
    day="2020-10-27 00:00:00"
    projectSysNo=10078
    deviceId="201811201952"
    startTime=datetime.datetime.strptime(day,"%Y-%m-%d %H:%M:%S")


    # for i in range(1):
    #     time.sleep(5)
    #     deltTa=datetime.timedelta(hours=i*2)
    #     threading._start_new_thread(func,(data,deviceId,projectSysNo,startTime+deltTa))
    thread_list=[]

    with ThreadPoolExecutor(max_workers=12) as t:
        for i in range(12):
            deltTa=datetime.timedelta(hours=i*2)
            task=t.submit(func,data,deviceId,projectSysNo,startTime+deltTa)
            thread_list.append(task)
           
        for future in as_completed(thread_list):
            res=future.result()
            print(res) 
        print('done')     
    t2=time.time()-t1





