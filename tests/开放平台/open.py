
import os,sys
sys.path.append(os.getcwd())
import common.restClient as request
import common.environment as env

import json


data={
  "deviceId": "XW202000000010",
  "deviceTime": "2020-12-22 14:36:00",
  "pm25": 61.2,
  "pm10": 108.2,
  "tsp": 2.69,
  "noise": 75.8,
  "windDirect": 278.1,
  "windSpeed": 0.2,
  "temp": 20.2,
  "humid": 17.9,
  "atoms": 0.25,
  'method':'upload.envMonitorLiveData',
  "nonce":"Rnqget7gyxhjuDFO8fhDx6nXWEfBn0zh",
  "timestamp":"20201222153710"
}

baseUrl=env.env['baseUrl']
url=baseUrl+'/open.api/upload.envMonitorLiveData'
res=request.post(url=env.env['baseUrl'],params=json.dumps(data))
print(res)