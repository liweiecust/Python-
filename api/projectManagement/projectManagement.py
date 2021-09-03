import requests
import os,sys
import json

sys.path.append(os.getcwd())
from common.login import addCookie
from common.environment import env

params={  
    'appSysNo':None,
    'areaCode': None,
    'expandIntelliApp': 'true',
    'followOrganizationCode': "0001",
    'isInternal': None, # null --全球 1--境内 2--境外
    'onlyImportant': None,
    'orderBy': "project.projectLevel DESC, project.SortIndex DESC, project.SysNo DESC",
    'overseaCountryCode': None, #
    'pageNum': 1,
    'pageSize': 10,
    'projectStatus': None,# null-- 所有 0-- 竣工 1-- 在建
    'relationship': 2, # 0-- 本级 2 --本下级
    'searchKeyword': ""
}
   
baseUrl=env['baseUrl']

class BaseObject_api:
    headers={
    'Content-Type':'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    url=None

    def __init__(self):
        
        if self.headers is None or 'Cookie' not in self.headers.keys():
            self.headers=addCookie(self.headers)

    def setUrl(self,path):
        self.url= (baseUrl+"%s") % path

    def get(self,path):  
        self.setUrl(path)
        res=requests.get(self.url,headers=self.headers)
        return res

    def post(self,path,params):
        self.setUrl(path)
        self.data=json.dumps(params)
        res=requests.post(self.url,data=self.data,headers=self.headers)
        return res


class projectMagagement_api(BaseObject_api):
    headers={
    'Content-Type':'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    
    #
    def __init__(self):     
        super().__init__()

    #
    # 查询出的项目包含我的项目
    def api_getProjects(self,path='api/project/queryProject',args=None):
        if not isinstance(args,dict):
            raise Exception('invalid type',args)
        for key in args.keys():
            if key not in params.keys():
                raise Exception('invalid input args',args)
        params.update(args)
        res=self.post(path,params)
        print(type(res.text))
        #print(json.dumps(res.text))
        res=(json.loads(res.text))['data']
       
        return res

    def api_queryMyProjects(self,path='api/project/queryMyProject',args=None):
        for key in args.keys():
            if key not in params.keys():
                raise Exception('invalid input args',args)
        params.update(args)
        res=self.post(path,params)
        data=(json.loads(res.text))['data']
        return data


     
        

# test=projectMagagement_api()
# test.api_getProjects()


