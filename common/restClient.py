import requests


def get(url,params):
    res=requests.get(url,params)
    return res.content

def post(url,params):
    res=requests.post(url,params)
    return res.content
