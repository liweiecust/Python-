import time
from datetime import datetime, timedelta
from re import L
import sys,os
sys.path.append(os.getcwd())
######################################################
import pymongo
import time
import urllib
from dateutil import parser
import calendar
from  dateutil.relativedelta import relativedelta
######################################################
from common.baseFunctions import today_time_str
import common.MongodB
######################################################

password=urllib.parse.quote("yzw@123")
client=pymongo.MongoClient("mongodb://admin:%s@172.16.0.137:20200/" % password)
db=client.ibuild_data
db=db["ai_event"]

# # 今日触发事件
# todayTimeStr=today_time_str()

# today_events=db.find({'fCapTime':{'$gt':todayTimeStr['0'],'$lt':todayTimeStr['24']}})

#print('today events number',today_events.count())

#最新数据

def get_latest_event_date():   
    latest_event_itor=db.find({}).sort('fCapTime',-1).limit(1)
    if latest_event_itor.count()>0:
        latest_event=latest_event_itor[0]
    else:
        latest_event=None
    latest_event_date=latest_event['fCapTime']# datetime object
    return latest_event_date

latest_event_date=get_latest_event_date()+timedelta(hours=8)
print(type(latest_event_date))
# latest_event_date=datetime(year=2021,month=6,day=5)

def get_month_start_end_date(date):
    # 闰年：普通年份，公历年份是4的倍数，且不是100的倍数，便为闰年；对于世纪闰年：若公历年份是整百数，则必须是400的倍数才是闰年
    ### date: lastest event date
    ### return start time and end time for each month within the statistic range
    ###
    month_start_end_dict={}
    
    start_time=date-relativedelta(years=1)
    for i in range(12):
        start_end_dict={}
        temp_day=start_time+relativedelta(months=i)
        month_last_day=calendar.monthrange(temp_day.year,temp_day.month)[1]
        
        if compare_datetime(start_time,datetime(year=temp_day.year,month=temp_day.month,day=1)):
            start_end_dict['start']=start_time
        else:
            start_end_dict['start']=datetime(year=temp_day.year,month=temp_day.month,day=1,hour=23,minute=59,second=59)
        
        if compare_datetime(date,datetime(year=temp_day.year,month=temp_day.month,day=month_last_day))>0:
            start_end_dict['end']=datetime(year=temp_day.year,month=temp_day.month,day=month_last_day,hour=23,minute=59,second=59)
        else:
            start_end_dict['end']=date
        month_start_end_dict[i]=start_end_dict
        
        print('%s - %s | month %s | %s days' % (start_end_dict['start'],start_end_dict['end'],temp_day.month,month_last_day))
    start_end_dict={} # 引用传递，需要清空object
    temp_day=start_time+relativedelta(months=11)
    if (start_time+relativedelta(months=11)).month<date.month:
        start_end_dict['start']=datetime(year=temp_day.year,month=date.month,day=1)
        start_end_dict['end']=date
        month_start_end_dict[12]=start_end_dict
        print('%s - %s | month %s | %s days' % (start_end_dict['start'],start_end_dict['end'],date.month,month_last_day))

    for value in month_start_end_dict.values():
        value['start']=value['start']-timedelta(hours=8)
        value['end']=value['end']-timedelta(hours=8)
    return month_start_end_dict

def compare_datetime(datetime1,datetime2):
    deltatime=time.mktime(datetime1.timetuple())-time.mktime(datetime2.timetuple())
    # print(deltatime.days)
    # print(deltatime.seconds)
    # print(deltatime.microseconds)
    # print(deltatime)
    # if deltatime.days>0 or deltatime.seconds>0 or deltatime.microseconds>0: # 坑！！
    #     return True
    # else:
    #     return False

    if deltatime>0:
        return True
    else:
        return False



# 查询事件总数，按事件类型分组，已去重
# history_events_total=db.aggregate([{"$group":{"_id":"$alertUuid","eventId":{"$first":"$eventId"}}},{"$group":{"_id":'$eventId',"count":{"$sum":1}}}])
# print('total',history_events_total.next())

def history_events_group_by_eventId(start_time,end_time):
    history_events={}
    # results=db.aggregate([{"$match":{'fCapTime':{"$gt":"ISODate('%s')" % start_time,"$lt":"ISODate('%s')" % end_time}}},{"$group":{"_id":"$alertUuid","eventId":{"$first":"$eventId"}}},{"$group":{"_id":'$eventId',"count":{"$sum":1}}}])
    results=db.aggregate([{"$match":{'fCapTime':{"$gte":start_time,"$lte":end_time}}},{"$group":{"_id":"$alertUuid","eventId":{"$first":"$eventId"}}},{"$group":{"_id":'$eventId',"count":{"$sum":1}}}])
    
    # results=db.aggregate([{"$match":{'fCapTime':{"$gt":start_time }}},{"$group":{"_id":"$alertUuid","eventId":{"$first":"$eventId"}}},{"$group":{"_id":'$eventId',"count":{"$sum":1}}}])
    
    # print(results.next())

    for i in results:
        # print(i) # {'_id': 2, 'count': 141}
        history_events[i['_id']]=i['count']
    return history_events

def history_events_group_by_ipcName(start_time,end_time):
    history_events={}
    results=db.aggregate([{"$match":{'fCapTime':{"$gt":start_time }}},{"$group":{"_id":"$alertUuid","eventId":{"$first":"$eventId"},"ipcName":{"$first":"$ipcName"}}},{"$group":{"_id":'$ipcName',"count":{"$sum":1}}}])

    for i in results:
        # print(i)
        history_events[i['_id']]=i['count']
    return history_events


def day_events_group_by_eventId(day):
    # day: typeof datetime object
    day_events={}
    start_time=datetime(year=day.year,month=day.month,day=day.day)
    end_time=start_time+timedelta(hours=23,minutes=59,seconds=59)
    results=db.aggregate([{"$match":{'fCapTime':{"$gt":start_time,"$lt":end_time}}},{"$group":{"_id":"$alertUuid","eventId":{"$first":"$eventId"}}},{"$group":{"_id":'$eventId',"count":{"$sum":1}}}])
    for i in results:
        day_events[i['_id']]=i['count']
    return day_events


def convert_query_results(desc,results):
    events_total=0
    for i in results:                # 为啥i是int呢
        events_total=events_total+results[i]

    print(desc)
    for i in results:
        # print('events_total %s' % events_total)
        print("eventId:%s,count:%s,ratio:%s" % (i,results[i],results[i]/events_total))

###################################################事件触发趋势###########################################################

def last_7days_event_trend():
    print('latest event date:',latest_event_date)
    start_time=datetime(year=latest_event_date.year,month=latest_event_date.month,day=latest_event_date.day)
    latest_7days_array=[]
    for i in range(7):
        latest_7days_array.append(start_time-timedelta(days=i))
    for i in latest_7days_array:
            
            results=day_events_group_by_eventId(i)
            convert_query_results('day events statistics: %s' % i,results)

def last_30days_event_trend():
    
    start_time=datetime(year=latest_event_date.year,month=latest_event_date.month,day=latest_event_date.day)
    end_time=start_time-timedelta(days=30)
    latest_30days_array=[]
    for i in range(6):
        latest_30days_array.append(start_time-timedelta(days=i*5))
    for i in latest_30days_array:    
        results=day_events_group_by_eventId(i)
        convert_query_results('day events statistics: %s' % i,results)
    
def last_1year_event_trend():
    
    # start_time=datetime(year=latest_event_date.year,month=latest_event_date.month,day=latest_event_date.day)
    # end_time=start_time-relativedelta(years=1)

    latest_1year_dict=get_month_start_end_date(latest_event_date)
    for value in latest_1year_dict.values():
        start=value['start']
        end=value['end']
        print('start:',start)
        print('end:',end)
        results=history_events_group_by_eventId(start,end)
        convert_query_results('day events statistics: %s' % value,results)


###################################################事件触发次数###########################################################
def events_number():
    latest_7days_date=latest_event_date-timedelta(days=7)

    latest_30days_date=latest_event_date-timedelta(days=30)

    latest_1year_date=latest_event_date-relativedelta(years=1) #?366

    results=history_events_group_by_eventId(latest_7days_date,latest_event_date)

    # 近七日触发事件 从最后一条记录往前追溯7天

    convert_query_results("近七日触发事件次数",results)

    # 近30日触发事件
    results=history_events_group_by_eventId(latest_30days_date,latest_event_date)
    convert_query_results("近30日触发事件次数",results)

    # 近1 year触发事件
    results=history_events_group_by_eventId(latest_1year_date,latest_event_date)
    convert_query_results("近1 year触发事件次数",results)

##############################################################################################################

#今日触发事件

def today_events_source():
    todayTimeStr=today_time_str()
    start_time=todayTimeStr['0']
    end_time=todayTimeStr['24']

    today_events=db.find({'fCapTime':{'$gt':todayTimeStr['0'],'$lt':todayTimeStr['24']}})
    # results=db.aggregate([{"$match":{'fCapTime':{"$gt":start_time }}},{"$group":{"_id":"$alertUuid","eventId":{"$first":"$eventId"}}},{"$group":{"_id":'$ipcName',"count":{"$sum":1}}}])
    results=history_events_group_by_ipcName(start_time,end_time)
    convert_query_results('今日触发事件来源',results)
    return results
##############################################################################################################
#AI事件触发来源
def events_source():
    latest_7days_date=latest_event_date-timedelta(days=7)

    latest_30days_date=latest_event_date-timedelta(days=30)

    latest_1year_date=latest_event_date-relativedelta(years=1) #?366

    results=history_events_group_by_ipcName(latest_7days_date,latest_event_date)

    # 近七日触发事件 从最后一条记录往前追溯7天

    convert_query_results("近七日触发事件次数",results)

    # 近30日触发事件
    results=history_events_group_by_ipcName(latest_30days_date,latest_event_date)
    convert_query_results("近30日触发事件次数",results)

    # 近1 year触发事件
    results=history_events_group_by_ipcName(latest_1year_date,latest_event_date)
    convert_query_results("近1 year触发事件次数",results)


##############################################################################################################

if __name__=='__main__':
    print(time.mktime(latest_event_date.timetuple()))
    # print(latest_event_date,today_time_str()['0'])
    # res=history_events_group_by_eventId(today_time_str()['0'],latest_event_date)
    # res=get_month_start_end_date(latest_event_date)
    # print(res)
    # latest_event_date=datetime(year=2020,month=2,day=29)   #20年2月29天；19年2月只有28天 2019-02-28 00:00:00
    # print(latest_event_date-relativedelta(years=1))
    print('aiBigScreen test')
    # if any(x is not None and x != int(x) for x in (years, months)):
    # print(compare_datetime(datetime(year=2021,month=6,day=5),datetime(year=2021,month=8,day=1)))
    # last_1year_event_trend()

    #last_7days_event_trend()
    
    # last_30days_event_trend()

    #last_1year_event_trend()
    
    # events_number()

    #today_events_source()

    events_source()