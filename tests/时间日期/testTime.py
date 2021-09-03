import time
# from dateutil import parser
import datetime
from datetime import date


print(datetime.datetime.now())
# ticks=time.time()
# deltaT=100
# newDate=(datetime.datetime.now()+datetime.timedelta(seconds=deltaT))



# timeStr=newDate.strftime("%Y-%m-%d %H:%M:%S")
# newTime=parser.parse(timeStr)
# print(newTime)
# print(type(newTime))
# print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
# dateStr = time.localtime().strft("%Y-%m-%dT%H:%M:%S.%fZ")
# dateISODate = time.localtime(dateStr, "%Y-%m-%dT%H:%M:%S.%fZ")

timeStr=datetime.datetime.strptime("2020-10-28 00:00:00","%Y-%m-%d %H:%M:%S")
print(timeStr)
print(type(timeStr))

day="2020-10-22 00:00:00"
deltaT=5
if day:
    startTime=datetime.datetime.strptime(day,"%Y-%m-%d %H:%M:%S")
else:
    startTime=datetime.datetime.now()
newDate=(startTime+datetime.timedelta(seconds=deltaT))
# timeStr=datetime.datetime.strptime(newDate,"%Y-%m-%d %H:%M:%S")
# newTime=parser.parse(timeStr)
print(newDate)


