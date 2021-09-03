import os,sys
sys.path.append(os.getcwd())
import csv
import pandas
import json

from common.dbConnection import dbConnection

#############运营项目数据统计-导出############# 

query_keyProjects="""SELECT p.sysNO,p.ProjectName,
org.organizationName,p.startDate,planCompleteDate,coverImageUrl
from project as p
inner JOIN systemorganization org on p.OrganizationSysNo=org.SysNo
where p.CommonStatus=1 and org.CommonStatus=1
and p.OrganizationCode like %s"""



def isNVR(projSysNo,appCode,connection):
    queryStr="""SELECT
            `projectintelliapp`.`SysNo`,
            `projectintelliapp`.`ProjectSysNo`,
            `projectintelliapp`.`AppSysNo`,
            `projectintelliapp`.`Status`,
            `projectintelliapp`.`ContactMan`,
            `projectintelliapp`.`ContactMobilePhone`,
            `projectintelliapp`.`AppConfig`,
            `intelliapp`.`AppName`,
            `intelliapp`.`AppCode`,
            `auth`.`AuthStatus`
        FROM `yz_ibuild`.`projectintelliapp`
            INNER JOIN yz_ibuild.intelliapp ON projectintelliapp.AppSysNo = intelliapp.SysNo
            LEFT JOIN yz_ibuild.project_intelliapp_authorization auth
                ON projectintelliapp.ProjectSysNo=auth.ProjectSysNo AND projectintelliapp.AppSysNo=auth.AppSysNo
        WHERE `projectintelliapp`.ProjectSysNo = %s
              AND `intelliapp`.AppName = %s
              AND `projectintelliapp`.Status = 1
        ORDER BY `projectintelliapp`.`AppSysNo` ASC"""
    b=connection.executeQuery(queryStr,(projSysNo,appCode))
    if(len(b)>0):
        return "已接入"
    else:
        return "未接入"

def getLaowuSysNo(projSysNo,appCode,connection):
    queryStr="""SELECT
            `projectintelliapp`.`SysNo`,
            `projectintelliapp`.`ProjectSysNo`,
            `projectintelliapp`.`AppSysNo`,
            `projectintelliapp`.`Status`,
            `projectintelliapp`.`ContactMan`,
            `projectintelliapp`.`ContactMobilePhone`,
            `projectintelliapp`.`AppConfig`,
            `intelliapp`.`AppName`,
            `intelliapp`.`AppCode`,
            `auth`.`AuthStatus`
        FROM `yz_ibuild`.`projectintelliapp`
            INNER JOIN yz_ibuild.intelliapp ON projectintelliapp.AppSysNo = intelliapp.SysNo
            LEFT JOIN yz_ibuild.project_intelliapp_authorization auth
                ON projectintelliapp.ProjectSysNo=auth.ProjectSysNo AND projectintelliapp.AppSysNo=auth.AppSysNo
        WHERE `projectintelliapp`.ProjectSysNo = %s
              AND `intelliapp`.AppName = %s
              AND `projectintelliapp`.Status = 1
        ORDER BY `projectintelliapp`.`AppSysNo` ASC"""
    b=connection.executeQuery(queryStr,(projSysNo,appCode))
    if(len(b)>0):
        appConfig=b[0][6]
        sysNo=appConfig.split(":")[1]
        sysNo=sysNo.split("}")[0]
    else:
        sysNo=""
    return sysNo

def shouyanhuoSysNo(projSysNo,appCode,connection):
    queryStr="""SELECT
            `projectintelliapp`.`SysNo`,
            `projectintelliapp`.`ProjectSysNo`,
            `projectintelliapp`.`AppSysNo`,
            `projectintelliapp`.`Status`,
            `projectintelliapp`.`ContactMan`,
            `projectintelliapp`.`ContactMobilePhone`,
            `projectintelliapp`.`AppConfig`,
            `intelliapp`.`AppName`,
            `intelliapp`.`AppCode`,
            `auth`.`AuthStatus`
        FROM `yz_ibuild`.`projectintelliapp`
            INNER JOIN yz_ibuild.intelliapp ON projectintelliapp.AppSysNo = intelliapp.SysNo
            LEFT JOIN yz_ibuild.project_intelliapp_authorization auth
                ON projectintelliapp.ProjectSysNo=auth.ProjectSysNo AND projectintelliapp.AppSysNo=auth.AppSysNo
        WHERE `projectintelliapp`.ProjectSysNo = %s
              AND `intelliapp`.AppName = %s
              AND `projectintelliapp`.Status = 1
        ORDER BY `projectintelliapp`.`AppSysNo` ASC"""
    b=connection.executeQuery(queryStr,(projSysNo,appCode))
    if(len(b)>0):
        appConfig=b[0][6]
        sysNo=appConfig.split(":")[1]
        sysNo=sysNo.split("}")[0]
    else:
        sysNo=""    
    return sysNo

def financialSysNo(projectSysNo,db):
    queryStr="""
      SELECT r.mdm_project_code
        FROM yz_ibuild.project p
                 INNER JOIN yz_ibuild.cscec_mdm_project_relation r on p.SystemProjectSysNo = r.sys_project_sysno
        WHERE p.SysNo = %s
        limit 1"""
    res=db.executeQuery(queryStr,(projectSysNo))
    if(len(res)>0):
        return res[0]
    else:
        return ""

def schedulePictures(projectSysNo,db):
    queryStr="""
    SELECT
            SysNo,
            ProjectSysNo,
            ScheduleDate
        FROM dronestrikeschedule
        WHERE Status = 1
              AND ProjectSysNo = %s
        ORDER BY ScheduleDate DESC"""
    res=db.executeQuery(queryStr,(projectSysNo))
    if(len(res)>0):
        return "已上传"
    else:
        return "未上传"

def countIPC(projectSysNo,db):
    queryStr="""select * from yz_ibuild_video.video_ipc_info info_db
    inner JOIN yz_ibuild.project  project ON info_db.ProjectSysNo=project.sysNo 
    where projectsysno =%s
    and info_db.CommonStatus=1
    and info_db.OnLineStatus=1"""
    res=db.executeQuery(queryStr,(projectSysNo))
    return len(res)

def wirte_data(data):
    write_file = "path_to_file.xlsx"
    df = pd.DataFrame(data)
    writer =  pd.ExcelWriter(write_file)
    df.to_excel(writer,index=False,startrow=0)
    writer.save()


# data=['sf','sdf','df']
# csvfile=open("G:\测试记录\exportP.csv","wb")
# writer=csv.writer(csvfile)
# writer.writerows(data)
# csvfile.close()


if __name__=="__main__":
    # nvr=isNVR("10218","5",db)
    # print(nvr)

    db=dbConnection()
    db_projects=db.executeQuery(query_keyProjects,("000101000002%"))
    columns=["所属组织","所属公司","项目编号","项目名称","是否接入视频","劳务系统编号","收获系统编号","财务系统编号","摄像头添加数量","形象进度照片数量","开工日期","竣工日期","封面图片"]

    projects=[]
    projects.append(columns)
    db_name=[]
    for p in db_projects:
        i=[]
        #所属公司
        i.append(p[2])
        #项目编号
        i.append(str(p[0]))
        #项目名称
        i.append(p[1])

        projectSysNo=p[0]
        #是否接入视频
        nvr=isNVR(projectSysNo,"视频监控",db)
        i.append(nvr)

        #劳务系统编号
        laowuSysNo=getLaowuSysNo(projectSysNo,"劳务管理",db)
        i.append(laowuSysNo)

        #收获系统编号
        shouyanhuo=shouyanhuoSysNo(projectSysNo,"收验货",db)
        i.append(shouyanhuo)

        #财务系统编号
        financialSysNO=financialSysNo(projectSysNo,db)
        i.append(financialSysNO)

        #摄像头添加数量
        ipcCount=countIPC(projectSysNo,db)
        i.append(ipcCount)

        #形象进度照片数量
        prictures=schedulePictures(projectSysNo,db)
        i.append(prictures)

        startDate=p[3]
        endDate=p[4]
        if startDate is None:
            startDate=""
        else:
            startDate=p[3].strftime("%Y-%m-%d %H:%M:%S")
        if endDate is None:
            endDate=""
        else:
            endDate=p[4].strftime("%Y-%m-%d %H:%M:%S")
        i.append(startDate)
        i.append(endDate)
        coverageImag=p[5]

        #封面图片
        i.append(len(coverageImag))
        projects.append(i)

    db.close()
    print("count:%s"%(len(projects)))
    for p in projects:
        print(p)
        print("------------------------------------------------------")