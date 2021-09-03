import sys,os

from requests.api import head
sys.path.append(os.getcwd())
from common.login import getCookie, login
import requests
import json


def getOrganizationChildsPage(orgCode,headers):
    url="https://ibuild.yzw.cn/api/systemOrganization/getOrganizationChildsPage"
    params={"pageNum":1,"pageSize":100,"parentOrganizationCode":orgCode}
    
    res=requests.post(url,data=json.dumps(params),headers=headers)
    # print(res.status_code)
    # print(res.text)
    array=json.loads(res.text)["data"]["list"]
    code_array=[]
    sysNo_array=[]
    for item in array:
        code_array.append(item["organizationCode"])
        sysNo_array.append(item["sysNo"])
    return (code_array,sysNo_array)
    
def checkOrgRole(orgSysNo,headers):
    # 检查组织有管理员，一般用户角色
    url="https://ibuild.yzw.cn/api/role/organizationRoleList/%s" % orgSysNo
    res=requests.get(url,headers=headers)
    # print(res.status_code)
    # print(res.text)
    array=json.loads(res.text)["data"]
    if len(array)<2:
        print("组织orgSysNo: %s",orgSysNo)
        for i in array:
            print("角色：%s",i["roleName"])
 
def checkOrganizationMenu(roleSysNo,headers): 
    # 组织角色菜单权限检查 视频防疫-》人员配置
    Mgt_Anti_Risk_View="Mgt_Anti_Risk_View"
    Mgt_Anti_Risk_Edit="Mgt_Anti_Risk_Edit"
    Mgt_Antiepidemic_Report="Mgt_Antiepidemic_Report_View"
    url="https://ibuild.yzw.cn/api/role/organization/%s" % roleSysNo
    res=requests.post(url,data={},headers=headers)
    print(res.status_code)
    print(res.text)
    data=json.loads(res.text)["data"]
    temp=data[0]["children"][0]["children"]["functionList"]
    if temp[0]["fucntionkey"]==Mgt_Anti_Risk_View and temp[0]["selected"]==True:
        a=True
    if temp[1]["fucntionkey"]==Mgt_Anti_Risk_View and temp[1]["selected"]==True:
        b=True
    if a and b is not True:
        print('组织 %s 没有权限' % roleSysNo)




if __name__=="__main__":
    fangyibanOrgCode="0001iajk"
    orgCodeArray2=[]
    orgSysNoArray2=[]
    orgCodeArray3=[]
    orgSysNoArray3=[]
    #登录
    headers=getCookie()
    #获取二级单位列表
    # org_tuple=getOrganizationChildsPage(fangyibanOrgCode,headers)
    # for value in org_tuple[0]:
    #     orgCodeArray2.append(value)
    # for value in org_tuple[1]:
    #     orgSysNoArray2.append(value)
    
    # #获取三级单位列表
    # for item in orgCodeArray2:
    #     org_tuple=getOrganizationChildsPage(item,headers=headers)
    #     for value in org_tuple[0]:
    #         orgCodeArray3.append(value)
    #     for value in org_tuple[1]:
    #         orgSysNoArray3.append(value)
       

    # # for i in orgCodeArray3:
    # #     print(i)
    # # for i in orgSysNoArray3:
    # #     print(i)
    # print(len(orgSysNoArray2))
    # print(len(orgSysNoArray3))

    # # 二三级单位有管理员，一般用户角色
    # for i in orgSysNoArray2:
    #     checkOrgRole(i,headers=headers)
    # # checkOrgRole(-9687,headers)
    # for i in orgSysNoArray3:
    #     checkOrgRole(i,headers=headers)
    # print("finished")

    checkOrganizationMenu(1141042,headers=headers)