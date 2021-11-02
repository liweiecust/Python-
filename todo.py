import requests
import json

# url="http://172.16.0.131:3302/api/orgVideo/project/build-relation"

url="https://ibuildreport.yzw.cn/org/api/orgVideo/project/build-relation"

data={"accessToken":"4d2c0977b5624a748c288602b4bd4a19","projects":"GCB201905070,20210409591,20190301291"}
header={"Content-Type":"application/json;charset=UTF-8"}
res=requests.post(url,data=json.dumps(data),headers=header)
# print(json.loads(res.text))
print(res)
# print(res.status_code)
print(res.text)