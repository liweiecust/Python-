#PC端 项目管理页面

# 项目列表
# isInternal: 1 -- 境内 2--境外
# projectStatus: 0 -- 竣工 1 --在建
get_projects_sql="""
select project.SysNo,project.ProjectCode,project.ProjectName,project.OrganizationCode,org.OrganizationName 
,project.projectStatus,project.isInternal,area.AreaCode,area.AreaName
from yz_ibuild.project project 
INNER JOIN yz_ibuild.systemorganization org on project.OrganizationSysNo=org.SysNo
LEFT JOIN yz_ibuild.systemarea area on area.SysNo=project.AreaSysNo

where 
project.CommonStatus=1
and project.OrganizationCode like '0001%'
"""