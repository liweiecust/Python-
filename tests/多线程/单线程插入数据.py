import pymongo
import time
import _thread
from dateutil import parser
import datetime
import random
import urllib
import threading
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor


password=urllib.parse.quote("yzw@123")
client=pymongo.MongoClient("mongodb://admin:%s@172.16.0.137:20200/" % password)
db=client.ibuild_data
db=db["tower_crane"]





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



def dataFactory(data,capacity,deviceId,driver,projectSysNo,deviceTime):

    #update deviceId
    data.update({"deviceId":deviceId})

    #update projectSysNo
    data.update({"projectSysNo":projectSysNo})

    #update driverName and driverId
    data.update(driver)

    #data.update({"dataId":randStr(32)})

    #update liftingCapacity
    data.update({"liftingCapacity":capacity})

    #update deviceTime
    data.update({"deviceTime":deviceTime})

    data.update({"_id":ObjectId()})
    return data
    
def getDriver():
   
    drivers=db.find().limit(6000)
    index=random.choice(range(6000))
    #print(index)
    driver=drivers[index]
    try:
        result={"driverId":driver["driverId"],"driverName":driver["driverName"]}
    except Exception:
        print(index)
        print(driver)

    return driver

def randStr(num):
    array="1234567890qazwsxedcrfvtgbyhnujmiklop"
    res=""
    for i in range(num):
        res+=random.choice(array)
    return res

# driver=getDriver()
# print(driver)

def insert_data(data,capacity,deviceId,projectSysNo,deviceTime):

    driver=getDriver()
    #driver={"driverId":"12345","driverName":"liwei"}
    data=dataFactory(data,capacity,deviceId,driver,projectSysNo,deviceTime)
    #print(data)
    db.insert_one(data)
    #print(data)
    

def func(data,deviceId,projectSysNo,startTime):
    # 插入24小时数据
    N=int(24*3600/5)
    capacity_array=[0,5,12,20]
    for i in range(N):
        deviceTime=startTime+datetime.timedelta(seconds=i*5)
        capacity=capacity_array[i%4]
        insert_data(data,capacity,deviceId,projectSysNo,deviceTime)
        print(i)

if __name__ == "__main__":
   

    day="2020-10-27 00:00:00"
    projectSysNo=10078
    deviceId="201811201952"
    startTime=datetime.datetime.strptime(day,"%Y-%m-%d %H:%M:%S")

    func(data,deviceId,projectSysNo,startTime)



    






