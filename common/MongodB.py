import pymongo
import urllib


password=urllib.parse.quote("yzw@123")
MongoDbClient=pymongo.MongoClient("mongodb://admin:%s@172.16.0.137:20200/" % password)