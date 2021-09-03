import os,sys
sys.path.append(os.getcwd())
from common.dbConnection import dbConnection
import unittest
from collections import UserDict
connection=dbConnection()

query = """SELECT
                    IpcSerial,
                    OnLineStatus 
                FROM
                    yz_ibuild_video.video_ipc_info 
                WHERE
                    ProjectSysNo IN %s 
                    AND CommonStatus =1"""
get_projects_sql="""
SELECT 
  p.ProjectCode,
	p.ProjectName,
	p.ProjectCategory,
	p.TotalContractAmt,
	org.OrganizationCode,
	p.ConstructionOrganizationCode,
	district.AreaName,
	district.AreaCode,
	p.LocationX,
	p.LocationY,
	p.StartDate,
	p.PlanCompleteDate,
	p.ProjectLevel,
	p.ProjectStatus,

	district.areaName district,
	city.areaName city,
	province.areaName province
FROM
  yz_ibuild.project p
	LEFT JOIN yz_ibuild.systemarea district on p.AreaSysNo=district.SysNo
	left JOIN yz_ibuild.systemarea city on district.parentsysno=city.sysno
	left JOIN yz_ibuild.systemarea province on province.sysno=city.parentsysno	
 INNER JOIN yz_ibuild.systemorganization org ON p.OrganizationSysNo = org.SysNo
 
WHERE
	org.CommonStatus=1
  and p.CommonStatus = 1 
  AND p.ProjectStatus =%s
	and p.IsInternal=%s
	AND p.OrganizationCode LIKE %s # 本下级
  and (district.areaname=%s or city.AreaName=%s or province.areaName=%s)
order by p.ProjectLevel desc,p.SortIndex desc,p.SysNo desc

"""                    
class projectManagement(unittest.TestCase):

    def test_getProjects(self,projectStatus=1,isInternal=1,orgCode='0001%',areaName="北京"):
        from sql.projectManagement.projectManagement import get_projects_sql as query
        args=(projectStatus,isInternal,orgCode,areaName,areaName,areaName)
        #projects= connection.executeQuery(get_projects_sql,args)
        projects= connection.executeQuery(query,args)
        print(projects)

        

args=([10277],)
# row=connection.executeQuery(query,args)
# print(row)

if __name__ == "__main__":
    # suite=unittest.TestLoader.loadTestsFromTestCase(type(projectManagement))
    # suite.run()
    unittest.main()