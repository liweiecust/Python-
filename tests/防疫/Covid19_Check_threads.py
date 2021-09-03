import requests
import json
import csv
from concurrent.futures import ThreadPoolExecutor,as_completed

headers={
    'Content-Type':'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}
login_url='https://ibuild.yzw.cn/api/auth/login/'
# payload=dict(captcha='',captchaToken='',loginName='Fiona_zh5',password='Newegg@1234',rememberMe='false')

def get_cookie(url):
    payload=dict(captcha='',captchaToken='',loginName='liwei_test',password='q1111111',rememberMe='false')
    res=requests.post(url,data=json.dumps(payload),headers=headers)
    return res

def login(func):
    login_url='https://ibuild.yzw.cn/api/auth/login/'
    headers=get_cookie(login_url).headers
    if 'Set-Cookie' not in headers.keys():
        raise Exception('login failed.')
    headers['Cookie']=headers['Set-Cookie']
    def addcookie(* args):
        print(args)
        func()
        
    return addcookie

@login
def queryUserList():
    params=dict(keyword='',level='false',organizationCode='0001',organizationSysNo=1,pageNum=1,pageSize=10,showValid='false')
    payload=json.dumps(params)
    data=requests.post("http://ibuild.yzw.cn.qa:81/api/systemUser/queryUserList",data=payload,headers=headers)
    print(data.status_code)
    print(data.text)


def addCookie(headers):
    cookie=get_cookie(login_url).headers['Set-Cookie']
    headers['Cookie']=cookie
    return headers

@login
def queryProjectList(userName,orgCode):
    project_list_url="https://ibuild.yzw.cn/api/project/queryProject"
    project_query_para={"areaCode":None,"expandIntelliApp":'true',"followOrganizationCode":orgCode,"onlyImportant":'false',"pageNum":1,"pageSize":10,"relationship":2,"searchKeyword":"","appSysNo":None,"projectStatus":1,"hasAppData":"","orderByScore":None,"isInternal":None,"overseaCountryCode":None,"orderBy":"project.projectLevel DESC, project.SortIndex DESC, project.SysNo DESC"}
    res=requests.post(project_list_url,data=json.dumps(project_query_para),headers=headers)
    projects=(json.loads(res.text))['data']

    project_count=projects['total']
    print('projects count:',project_count)
    if project_count<0:
        accounts_invalid.append("%s - %s" % (userName,"passWord"))
        print(userName,' - ',"passWord",'login failed')
        return False
    else :
        return False

accounts_invalid=[]



# queryProjectList("Fiona_zh5","0001")



def test_account(user,passWord,headers=headers):
    payload=dict(captcha='',captchaToken='',loginName=user,password=passWord,rememberMe='false')
    res=requests.post(login_url,data=json.dumps(payload),headers=headers)

    project_list_url="https://ibuild.yzw.cn/api/project/queryProject"
    project_query_para={"areaCode":None,"expandIntelliApp":'true',"followOrganizationCode":"0001","onlyImportant":'false',"pageNum":1,"pageSize":10,"relationship":2,"searchKeyword":"","appSysNo":None,"projectStatus":1,"hasAppData":"","orderByScore":None,"isInternal":None,"overseaCountryCode":None,"orderBy":"project.projectLevel DESC, project.SortIndex DESC, project.SysNo DESC"}

    # headers=addCookie(headers)
    # print(res.headers)
    if 'Set-Cookie' not in res.headers.keys():
        accounts_invalid.append("%s - %s" % (user,passWord))
        print(user,' - ',passWord,'login failed')
        return False
    cookie=res.headers['Set-Cookie']
    headers['Cookie']=cookie

    res=requests.post(project_list_url,data=json.dumps(project_query_para),headers=headers)
    projects=(json.loads(res.text))['data']

    project_count=projects['total']
    # print('projects count:',project_count)
    if project_count<0:
        accounts_invalid.append("%s - %s" % (user,passWord))
        print(user,' - ',passWord,'login failed')
        return False
    else :
        return False



# test_account('Fiona_zh5','Newegg@1234')
test_account('liwei_test','q1111111')





# user_list=[]

# with open('C:\\Users\\liwei\\Desktop\\Test.csv','r') as accounts:
#     lines=csv.reader(accounts)
#     for line in lines:
#         user_list.append({'User':line[0],"PassWord":line[1]})

# thread_list=[]    
# with ThreadPoolExecutor(max_workers=10) as t:
        
#         for user in user_list:
#             task=t.submit(test_account,user["User"],user["PassWord"],headers)
#             thread_list.append(task)
           
#         for future in as_completed(thread_list):
#             res=future.result()
#             print(res) 
#         print('done')     



# print('invalid:')
# print(accounts_invalid)

# with open('C:\\Users\\liwei\\Desktop\\Invalid.csv','w',encoding='utf-8',newline='') as AA:
#     csv_writer = csv.writer(AA)
#     for line in accounts_invalid:
#         # 2. 基于文件对象构建 csv写入对象
        
#         print(line)
#         # 3. 构建列表头
#         csv_writer.writerow([line,])


# 赵岩生15588815737
# 贺云飞15289399166
# 彭  凯15251856077

#[\u4e00-\u9fa5]  匹配汉字
