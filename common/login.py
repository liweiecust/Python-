import requests
import json
from requests.api import head
from common.environment import env

headers={
    'Content-Type':'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}
# login_url='http://ibuild.yzw.cn.qa:81/api/auth/login/'

payload=dict(captcha='',captchaToken='',loginName='liwei_test',password='q1111111',rememberMe='false')

def get_cookie(url):
    res=requests.post(url,data=json.dumps(payload),headers=headers)
    return res

def login(func):
    # 为接口添加Cookie
    headers=get_cookie(env["host"]).headers
    if 'Set-Cookie' not in headers.keys():
        raise Exception('login failed.')
    if 'Cookie' not in headers.keys():
        headers['Cookie']=headers['Set-Cookie']
    def addcookie(*args):
        func(headers)        
    return addcookie


def addCookie(headers):
    cookie=get_cookie(env["host"]).headers['Set-Cookie']
    headers['Cookie']=cookie
    return headers

def getCookie():
    res=requests.post(env["host"],data=json.dumps(payload),headers=headers)
    headers['Cookie']=res.headers['Set-Cookie']
    return headers
