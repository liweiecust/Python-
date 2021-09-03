import os,sys

sys.path.append(os.getcwd())

# from common.restClient import post
import json

headers={
    'Content-Type':'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'

}


import requests
def login():
    url='https://ibuild.yzw.cn:8081/api/auth/login/'
    payload=dict(captcha='',captchaToken='',loginName='Fiona_zh5',password='Newegg@12345',rememberMe='false')
    # print(payload.values())
    # print(type(payload.values()))
    res=requests.post(url,data=json.dumps(payload),headers=headers2)
    return res
res=login()

cookies=requests.utils.dict_from_cookiejar(res.cookies)
for header in cookies:
    print(header)
    
#headers['Cookie']='web.auth.yzw'+':'+cookies['web.auth.yzw'] #  只使用cookie的value是无法登录的
headers['Cookie']=res.headers['Set-Cookie']
headers['projectSysNo']='17693'                      # 项目级接口需要在HEADER里加上 projectSysNo，不然会报没有权限的错误
print(headers)
payload=dict(aiSysNo='1',projectSysNo='17693',ipcSysCode='E73694704_3')


print(json.dumps(payload))
payload=json.dumps(payload) # server demands application/json format input
data=requests.post("https://ibuild.yzw.cn:8081/api/admin/ai/init/aiIpcEvent",data=payload,headers=headers)
print(data.status_code)
print(data.text)
