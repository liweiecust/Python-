import time
# from dateutil import parser
import datetime
from datetime import date



# deltaT=100
# newDate=(datetime.datetime.now()+datetime.timedelta(seconds=deltaT))

# print(newDate)



# timeStr=time.strftime("%Y-%m-%d %H:%M:%S",(newDate.year,newDate.month,newDate.day))
# print(timeStr)
start=datetime.datetime.now()
time.sleep(5)
end=datetime.datetime.now()
print((end-start).seconds)
