import os,sys
sys.path.append(os.getcwd())
import operator

from dbConnection import dbConnection

# compare object

class project():

    def __init__(self,sysNo):
        self.conn=None
        if self.conn is None:
            self.conn=dbConnection()
        queryStr="""
            select project.SysNo,project.ProjectCode,project.ProjectName,project.OrganizationCode,org.OrganizationName 
            ,project.projectStatus,project.isInternal,area.AreaCode,area.AreaName
            from yz_ibuild.project project 
            INNER JOIN yz_ibuild.systemorganization org on project.OrganizationSysNo=org.SysNo
            LEFT JOIN yz_ibuild.systemarea area on area.SysNo=project.AreaSysNo

            where 
            project.CommonStatus=1
            and project.OrganizationCode like '0001%'
        """
        self.row=self.conn.executeQuery(queryStr,sysNo)

    def getSysNo(self):
        return self.row[0]
    
    def getProjectCode(self):
        return self.row[1]
