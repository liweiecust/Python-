import pymysql
from collections.abc import Iterable
import os,sys

sys.path.append(os.getcwd())


connStr={"host":"172.16.0.130",
    "port":7301,
    "user":"dev_admin",
    "passwd":"zk.123456"}
from common.environment import mysql_QA
connStr=mysql_QA
conn = pymysql.connect(host=connStr["host"], port=connStr["port"], user=connStr["user"],
                            passwd=connStr["passwd"], db="yz_ibuild_video",charset='utf8')

query = """SELECT
                    IpcSerial,
                    OnLineStatus 
                FROM
                    video_ipc_info 
                WHERE
                    ProjectSysNo IN %s 
                    AND CommonStatus =1"""
args=([10277],)
cursor = conn.cursor()
cursor.execute(query,args)
row = cursor.fetchall()
print(row)

if isinstance(args,Iterable):
    tmp=([args],)
    print(tmp)
if isinstance(args,list):
    print("%s is type of lit" % args)


cursor.execute(query,args)
row = cursor.fetchall()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()

print(row)
#可变参数列表，参数被打包成元组
def func(*args): 
    print(args) 
    print(*args)

func([1,2,3])

