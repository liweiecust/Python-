import os,sys
sys.path.append(os.getcwd())

from sql.projectManagement.projectManagement import get_projects_sql
from common.dbConnection import dbConnection
from pymysql.connections import Connection
from pymysql import Error


class ProjectManagement():
    """
    项目管理页面
    """
    def __init__(self,conn):
        if not isinstance(conn,dbConnection):
            raise Error('invalid object conn')
        self.conn=conn
    
    def getProjects(self):
        """
        all valid projects
        """
        rows= self.conn.executeQuery(get_projects_sql)
        return rows

    def getProjectsSysNo(self,projects):
        """
        return projects sysNo
        """
        sysNo=[]
        #rows=self.getProjects()
        for r in projects:
            sysNo.append(r[0])
        return sysNo

    
    def internalProjects(self,projects):
        """internal projects
        """
        query="select * from yz_ibuild.project where isInternal=1 and sysNo in %s and commonStatus=1"
        sysNo=self.getProjectsSysNo(projects)
        return self.conn.executeQuery(query,(sysNo,))

    
    def overseaProjects(self,projects,overseaCountryCode=None):
        """overseas projects
        """
        query="select * from yz_ibuild.project where isInternal=2 and sysNo in %s"
        sysNo=self.getProjectsSysNo(projects)
        if overseaCountryCode:
            'to do: query country projects'
        return self.conn.executeQuery(query,(sysNo,))

    def filterByOrgCode(self,organizationCode,level,projects):
        """
            level 0 -- 本级 1 -- 本下级
        """
        if level==1:
            organizationCode= '%s%%' % organizationCode
        query="select * from yz_ibuild.project where organizationCode like %s and sysNo in %s"
        #sysNo=self.getProjectsSysNo()
        print('orgcode',organizationCode)
        sysNo=self.getProjectsSysNo(projects)
        return self.conn.executeQuery(query,(organizationCode,sysNo))

    def filterByStatus(self,projectStatus,projects):
        """
        0 -- 竣工
        1 -- 在建
        2 -- 停工
        """
        query="""select * from yz_ibuild.project where projectStatus=%s and sysNo in %s"""
        sysNo=self.getProjectsSysNo(projects)
        return self.conn.executeQuery(query,(projectStatus,sysNo))

    def filterByName(self,projectName,projects):
        query="""select * from yz_ibuild.project where projectName like %%%s%% and commonStatus=1"""
        sysNo=self.getProjectsSysNo(projects)
        return self.conn.executeQuery(query,(projectName,sysNo)) 

    def queryProjects(self,areaCode=None,orgCode='0001',isInternal=None,overseaCountryCode=None,projectStatus=None,relationShip=2,searchKeyword=None):
        '''
        '''
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
        projects=self.getProjects()
        if areaCode:
           projects=self.areaFilter(areaCode,projects)

        if orgCode!='0001' or relationShip!=2:
           projects=self.filterByOrgCode(orgCode,relationShip,projects) 

        if isInternal:
            if isInternal==1:
                projects=self.overseaProjects(projects,overseaCountryCode)
            elif isInternal==2:
                projects=self.internalProjects(projects)
            else:
                raise Exception('invalid args ',isInternal)

        if projectStatus:
            projects=self.filterByStatus(projectStatus,projects)
        return projects

    def appFilter(self,projects,appName):
        """
        projects using appplications
        """
        sysNo="""
        select projectSysNo from projectIntelliapp as proj inner join intelliapp as app on proj.appSysNo=app.sysNo 
        where app.appName='%s' and app.status=1 and proj.status=1 and projectSysNo in %s"""
        
        projects=self.conn.executeQuery(sysNo,(appName,projects))
        return projects

    def areaFilter(self,projects,areaName):
        """
        project area
        """
        queryStr="""select * from project LEFT JOIN yz_ibuild.systemarea district on project.AreaSysNo=district.sysno
                LEFT JOIN yz_ibuild.systemarea city on district.ParentSysNo=city.sysno
                LEFT JOIN yz_ibuild.systemarea province on city.ParentSysNo=province.sysNo
                where district.commonStatus=1 and city.commonStatus=1 and province.commonStatus=1
                and areaCode like (select areaCode from yz_ibuild.systemarea where areaName=%s and commonStatus=1)%
                and project.CommonStatus=1
                and project.sysNo in %s
               """
        projects=self.getProjects()
        projects=self.getProjectsSysNo(projects)
        projects=self.conn.executeQuery(queryStr,(areaName,projects))
        return projects

    def queryUserProjects(self,user):
        """
        query my projects
        """
        queryStr="""select p.projectName,p.projectStatus from userproject usp
                inner JOIN systemuser u on usp.usersysno=u.SysNo
                INNER JOIN project p on usp.projectsysno=p.sysno
                where p.commonstatus=1 and usp.status=1 
                and u.loginname=%s
        """
        projects=self.conn.executeQuery(queryStr,user)
        return projects

        



# conn=dbConnection()
# p=ProjectManagement(conn)
# projects=p.getProjectsSysNo(p.getProjects())
# # projects=p.appFilter(projects,'视频监控')
# projects=p.areaFilter(projects,'北京')
# print(len(projects))
# #projects=p.organizationProjects('0001',0)
# projects=p.areaProjects('10051031',projects)
# conn.close()

# print(len(projects))
# for p in projects:
#     print(p[2])


