import sys,os
sys.path.append(os.getcwd())


import pymysql
import datetime
from common.dbConnection import dbConnection

#在线率监控页面

conn=dbConnection()

#获取在建项目，org_type：2本下级，0本级
def get_project(Orgcode,org_type):
    if org_type == 2:
        code = Orgcode + "%"
    else:
        code = Orgcode

    sql = """SELECT
                project.SysNo,project.ProjectName,org.OrganizationName AS ConstructionOrganizationName
            FROM
                yz_ibuild.project AS project
                INNER JOIN yz_ibuild.systemorganization AS org ON project.OrganizationSysNo = org.SysNo 
            WHERE
                project.OrganizationCode LIKE %s 
                AND project.CommonStatus = 1 
                AND project.ProjectStatus = 1
                ORDER BY project.SortIndex DESC, project.SysNo DESC"""

    row=conn.executeQuery(sql,code)

    if len(row)>0:
        pj_id = []
        pj_na = []
        pj_org_na = []
        for loop in row:
            pj_id.append(loop[0])
            pj_na.append(loop[1])
            pj_org_na.append(loop[2])
        return [pj_id,pj_na,pj_org_na]
    else:
        return None

#通过项目编号，获取IPC接入数据
def project_ipc_num (prj):

    sql = """
    SELECT IpcSerial,OnLineStatus FROM yz_ibuild_video.video_ipc_info WHERE ProjectSysNo IN %s AND CommonStatus =1"""

    row=conn.executeQuery(sql,prj)

    if len(row)>0:
        ipc_num = len(row)
        online_num = 0
        for loop in row:
            if loop[1] == 1:
                online_num +=1
        return [ipc_num,online_num]
    else:
        return None

#通过项目编号、时间段，获取在线的IPC数量
def ipc_status_info (stdate,endate,*pjlist):

    sql = """SELECT
                    count(
                        DISTINCT ipcInfo.ProjectSysNo,
                        ipcStatus.IpcSerial,
                    DATE_FORMAT( ipcStatus.InDate,%s)) 
                FROM
                    ipc_status_info ipcStatus
                    INNER JOIN video_ipc_info ipcInfo ON ipcInfo.IpcSerial = ipcStatus.IpcSerial 
                WHERE
                    ipcInfo.CommonStatus = 1 
                    AND ipcStatus.OnLineStatus = 1 
                    AND ipcStatus.InDate BETWEEN %s 
                    AND % s 
                    AND ipcInfo.ProjectSysNo IN %s"""
    s1 = "%Y-%m-%d"
    row=conn.executeQuery(sql, [(s1,stdate,endate,*pjlist)])
    if len(row)>0:
        return row[0][0]
    else:
        return None

#统计总计在线率
def total_ipc_online_rate(orgcode,stdate,endate,org_type):

    st = datetime.datetime.strptime(stdate, '%Y-%m-%d %H:%M:%S')
    en = datetime.datetime.strptime(endate, '%Y-%m-%d %H:%M:%S')
    xx_days = (en - st).days + 1

    #获取组织下在建项目
    pj_list = get_project(orgcode,org_type)
    if pj_list != None:
        pj_id_list =pj_list[0]
        print(type(pj_id_list))
        # 获取组织下所有项目的监控点数
        pj_ipc_list = project_ipc_num(pj_id_list)
        if pj_ipc_list != None:
            # 接入IPC数量
            ipc_total = pj_ipc_list[0]
            # 当前在线IPC数量
            ipc_onnine_total = pj_ipc_list[1]
            # 时间段内，在线的IPC记录数
            ipc_info_online_total = ipc_status_info(stdate, endate, pj_id_list)
            if ipc_info_online_total != None:
                # 在线率
                online_rate = (ipc_info_online_total / (ipc_total * xx_days))
                # print(ipc_info_online_total,ipc_total,xx_days)
                return [len(pj_id_list), ipc_total, ipc_onnine_total, online_rate]
        else:
            return [len(pj_id_list),0,0,0]
    else:
        return [0,0,0,0]

#分别统计组织下属项目监控点在线率
def pj_ipc_online_rate(orgcode,stdate,endate,org_type):
    st = datetime.datetime.strptime(stdate, '%Y-%m-%d %H:%M:%S')
    en = datetime.datetime.strptime(endate, '%Y-%m-%d %H:%M:%S')
    xx_days = (en - st).days + 1

    # 获取组织下在建项目
    re_list = []
    pj_list = get_project(orgcode, org_type)
    if pj_list != None:
        pj_id_list = pj_list[0]
        pj_na_list = pj_list[1]
        pj_org_list = pj_list[2]

        # 获取组织下项目的监控点数
        number = 0
        for loop in pj_id_list:
            pj_id = [loop]
            pj_na = pj_na_list[number]
            pj_org = pj_org_list[number]
            number += 1

            pj_ipc_list = project_ipc_num(pj_id)
            if pj_ipc_list != None:
                # 接入IPC数量
                ipc_total = pj_ipc_list[0]
                # 当前在线IPC数量
                ipc_onnine_total = pj_ipc_list[1]
                # 时间段内，在线的IPC记录数
                ipc_info_online_total = ipc_status_info(stdate, endate, pj_id)
                if ipc_info_online_total != None:
                    # 在线率
                    online_rate = ipc_info_online_total/(ipc_total * xx_days)
                    online_day = round(online_rate*24,1)
                    pj_data = pj_na+"-"+pj_org+":"+str(ipc_total)+"-"+str(ipc_onnine_total)+"-"+str(online_day)+"-"+str((round(online_rate*100)))
                    re_list.append(pj_data)
                else:
                    pj_data = pj_na + "-" + pj_org + ":" + str(ipc_total) + "-" + str(ipc_onnine_total) + "-" + "0.0-0"
                    re_list.append(pj_data)
            else:
                pj_data = pj_na + "-" + pj_org + ":" + "0-0-0.0-0"
                re_list.append(pj_data)

        return re_list

    else:
        return ["该组织无数据"]

#获取各组织详情
def get_org(Orgcode,org_type):
    if org_type == 2:
        code = Orgcode + "%"
    else:
        code = Orgcode

    sql = """SELECT DISTINCT
                    org.OrganizationName,
                    org.OrganizationCode 
                FROM
                    systemorganization org
                    INNER JOIN project project ON project.OrganizationSysNo = org.SysNo 
                WHERE
                    project.CommonStatus = 1 
                    AND project.ProjectStatus = 1 
                    AND project.OrganizationCode LIKE %s 
                GROUP BY
                    org.SysNo;"""

    row=conn.executeQuery(sql, [(code,)])

    if len(row)>0:
        org_id = []
        org_na = []
        for loop in row:
            org_id.append(loop[1])
            org_na.append(loop[0])
        return [org_id,org_na]
    else:
        return None

#按不同组织统计在线率
def org_ipc_online_rate(orgcode,stdate,endate,org_type):
    org_list = get_org(orgcode,org_type)
    re_data = []
    if org_list!=None:
        org_id_list = org_list[0]
        org_na_list = org_list[1]
        num = 0
        for id in org_id_list:
            org_rate = total_ipc_online_rate(id,stdate,endate,org_type)
            org_data = org_na_list[num] +":"+ str(org_rate[0]) +"-"+ str(org_rate[1]) +"-"+ str(org_rate[2]) +"-"+ str(round(org_rate[3]*24,1)) +"-"+ str(round(org_rate[3]*100))
            re_data.append(org_data)
            num +=1
        return re_data
    else:
        return ["该组织无数据"]

if __name__=="__main__":
    # org_type：2本下级，0本级s
    #l=project_ipc_num([10277]) #'10265','10271'
    org_type =2
    orgcode = "0001"
    stdate = "2020-05-08 00:00:00"
    endate = "2020-05-08 23:59:59"

    # 总况数据：
    org_total = total_ipc_online_rate(orgcode, stdate, endate, org_type)
    print("总况数据：",org_total[0],org_total[1],org_total[2],round(org_total[3]*100))

    #按项目查询监控率
    print("项目详情：")
    pj_data = pj_ipc_online_rate(orgcode,stdate,endate,org_type)
    num = 0
    for x in pj_data:
        num +=1
        print(num,x)

    #按公司查询监控率
    print("公司详情：")
    org_data = org_ipc_online_rate(orgcode,stdate,endate,org_type)
    num = 0
    for x in org_data:
        num += 1
        print(num, x)