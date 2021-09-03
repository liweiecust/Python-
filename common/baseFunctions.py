import time,datetime



# print('(time.localtime() 获取当前时间元组)',time.localtime())

# print('datetime.date.today() 获取今日0点的时间元组?? 多了4秒？',datetime.date.today().strftime("%Y-%m-%d %H:%M:%d"))

# print('datetime.datetime.today() 获取当前时间的元组',datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%d"))

def today_time_str():
    time_array={}
    time_tuple=(datetime.date.today()-datetime.timedelta(hours=8)).timetuple()
    start_time=datetime.datetime(year=time_tuple.tm_year,month=time_tuple.tm_mon,day=time_tuple.tm_mday)
    end_time=datetime.timedelta(hours=23,minutes=59,seconds=59)+start_time
    time_array['0']=start_time
    time_array['24']=end_time
    return time_array





if __name__=='_main':
    print("0",today_time_str()['0'])
    print('24',today_time_str()['24'])