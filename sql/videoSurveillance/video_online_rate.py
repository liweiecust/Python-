# 监控数量

video_number="""
    select * from yz_ibuild_video.video_ipc_info
    where projectsysno in
    (
        select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
        inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
    INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
        where a.organizationCode like "0001%"
        and a.status=1
        and p.projectStatus=1
        and p.commonStatus=1 
        and o.commonStatus=1 # 有些组织被删除掉了
    )
    and CommonStatus=1
    and OnLineStatus=1
"""
# or 
"""

"""

# 项目数量
project_number="""
    SELECT DISTINCT
    p.*
    FROM
    yz_ibuild.project p
    INNER JOIN yz_ibuild.systemorganization org ON p.OrganizationSysNo = org.SysNo
    INNER JOIN yz_ibuild.projectorganizationrelation por ON por.ProjectSysNo = p.SysNo 
    WHERE
    p.CommonStatus = 1 
    AND p.ProjectStatus = 1 
    AND por.OrganizationCode LIKE CONCAT( '0001', '%' )
    and org.commonstatus=1;
"""

# 已接入项目数
project_using_video="""
    select i.ProjectSysNo,Count(1) from yz_ibuild_video.video_ipc_info i
    where projectsysno in
    (
        select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
        inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
    INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
        where a.organizationCode like "0001%"
        and a.status=1
        and p.projectStatus=1
        and p.commonStatus=1 
        and o.commonStatus=1 # 有些组织被删除掉了
    )
    and CommonStatus=1
    and i.onlineStatus=1
    GROUP BY i.ProjectSysNo
    order by i.ProjectSysNo
"""
# 在线时长
online_rate="""
    select i.ProjectSysNo,i.ProjectName,Count(1) from yz_ibuild_video.video_ipc_info i
    where projectsysno in
    (
        select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
        inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
    INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
        where a.organizationCode like "0001%"
        and a.status=1
        and p.projectStatus=1
        and p.commonStatus=1 
        and o.commonStatus=1 # 有些组织被删除掉了
    )
    and CommonStatus=1
    and i.onlineStatus=1
    GROUP BY i.ProjectSysNo
    order by i.ProjectSysNo
"""
# 监控数量
select * from yz_ibuild_video.video_ipc_info info_db
inner JOIN yz_ibuild.project  project ON info_db.ProjectSysNo=project.sysNo 
where projectsysno in
(
	select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
	inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
  INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
	where a.organizationCode like "0001%"
	and a.status=1
	and p.projectStatus=1
	and p.commonStatus=1 
	and o.commonStatus=1 # 有些组织被删除掉了
)
and info_db.CommonStatus=1
and info_db.OnLineStatus=1
and project.ProjectStatus=1

# 项目数量
SELECT DISTINCT
  p.*
FROM
  yz_ibuild.project p
  INNER JOIN yz_ibuild.systemorganization org ON p.OrganizationSysNo = org.SysNo
  INNER JOIN yz_ibuild.projectorganizationrelation por ON por.ProjectSysNo = p.SysNo 
WHERE
  p.CommonStatus = 1 
  AND p.ProjectStatus = 1 
  #AND por.OrganizationCode LIKE CONCAT( '0001', '%' )
  AND por.OrganizationCode ='0001'
and org.commonstatus=1;

# 已接入项目数
SELECT DISTINCT
  p.sysNo
FROM
  yz_ibuild.project p
  INNER JOIN yz_ibuild.systemorganization org ON p.OrganizationSysNo = org.SysNo
  INNER JOIN yz_ibuild.projectorganizationrelation por ON por.ProjectSysNo = p.SysNo 
	INNER JOIN yz_ibuild_video.video_ipc_info i on i.ProjectSysNo=p.SysNo
WHERE
  p.CommonStatus = 1 
  AND p.ProjectStatus = 1 
  AND por.OrganizationCode LIKE CONCAT( '0001', '%' )
and org.commonstatus=1;
and i.commonStatus=1
#--
select i.ProjectSysNo,Count(1) from yz_ibuild_video.video_ipc_info i
where projectsysno in
(
	select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
	inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
  INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
	where a.organizationCode like "0001%"
	and a.status=1
	and p.projectStatus=1
	and p.commonStatus=1 
	and o.commonStatus=1 # 有些组织被删除掉了
)
and CommonStatus=1
and i.onlineStatus=1
GROUP BY i.ProjectSysNo
order by i.ProjectSysNo

# 在线时长

select i.ProjectSysNo,p.ProjectName,Count(1) from yz_ibuild_video.video_ipc_info i
where projectsysno in
(
	select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
	inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
  INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
	where a.organizationCode like "0001%"
	and a.status=1
	and p.projectStatus=1
	and p.commonStatus=1 
	and o.commonStatus=1 # 有些组织被删除掉了
)
and CommonStatus=1
and i.onlineStatus=1
GROUP BY i.ProjectSysNo
order by i.ProjectSysNo


SELECT
			count(
					DISTINCT ipcInfo.ProjectSysNo,
					ipcStatus.IpcSerial,
			DATE_FORMAT( ipcStatus.InDate,'%Y-%m-%d %H:%M:%S')) 
	FROM
			ipc_status_info ipcStatus
			INNER JOIN video_ipc_info ipcInfo ON ipcInfo.IpcSerial = ipcStatus.IpcSerial 
	WHERE
			ipcInfo.CommonStatus = 1 
			AND ipcStatus.OnLineStatus = 1 
			AND ipcStatus.InDate BETWEEN "2020-07-31 00:00:00" 
			AND "2020-08-06 00:00:00" 

select IpcSerial,count(1) from yz_ibuild_video.ipc_status_info s
where DATE_FORMAT(s.inDate,"%Y-%m-%d")="2020-07-31"
and IpcSerial="fffda211b1884bcc935ee975fd1a6762"
GROUP BY s.IpcSerial
having count(1)>1

create TEMPORARY table temp_ipc_status(
IpcSerial 
)

select * from yz_ibuild_video.ipc_status_info
where IpcSerial=a.IpcSerial
(
select IpcSerial,max(InDate) from yz_ibuild_video.ipc_status_info s
where DATE_FORMAT(s.inDate,"%Y-%m-%d")="2020-08-06"
and IpcSerial="fffda211b1884bcc935ee975fd1a6762"
GROUP BY s.IpcSerial
) a


select info_db.IpcSerial,s_db.onLineStatus,s_db.InDate from yz_ibuild_video.video_ipc_info info_db
inner JOIN yz_ibuild.project  project ON info_db.ProjectSysNo=project.sysNo 
inner JOIN yz_ibuild_video.ipc_status_info s_db on info_db.ipcSysCode=s_db.ipcSysCode
where projectsysno in
(
	select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
	inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
  INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
	where a.organizationCode like "0001%"
	and a.status=1
	and p.projectStatus=1
	and p.commonStatus=1 
	and o.commonStatus=1 # 有些组织被删除掉了
)
and info_db.CommonStatus=1
and info_db.OnLineStatus=1
and project.ProjectStatus=1
and project.projectName="厦门英蓝国际金融中心项目"
and DATE_FORMAT(info_db.inDate,"%Y-%m-%d")=Date("2020-07-02") 


#######################################################################################################################

# 项目首页项目统计 8921 （包含项目所属组织已删除的项目）
select DISTINCT project.sysno from yz_ibuild.project as project
INNER JOIN yz_ibuild.systemorganization org on project.OrganizationSysNo=org.sysNO
where project.CommonStatus=1 and project.OrganizationCode like "0001%" and project.IsInternal=1

# 业务中心

###  在建项目数 8462 （没有包含项目所属组织已删除的项目）
    select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
        inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
        INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
        where a.organizationCode like "0001%"
        and a.status=1
        and p.projectStatus=1
        and p.commonStatus=1 
        and o.commonStatus=1 # 有些组织被删除掉了

###  在线摄像头统计 13968 onlineStatus=1 （没有包含项目所属组织已删除的项目）
    select * from yz_ibuild_video.video_ipc_info
    where projectsysno in
    (
        select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
        inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
        INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
        where a.organizationCode like "0001%"
        and a.status=1
        and p.projectStatus=1
        and p.commonStatus=1 
        and o.commonStatus=1 # 有些组织被删除掉了
    )
    and CommonStatus=1
    and OnLineStatus=1

### 接入摄像头 17480 （没有包含项目所属组织已删除的项目）

select * from yz_ibuild_video.video_ipc_info
    where projectsysno in
    (
        select DISTINCT ProjectSysNo from yz_ibuild.projectorganizationrelation a
        inner JOIN yz_ibuild.project p on a.ProjectSysNo=p.SysNo # 关联时要用主键关联
        INNER JOIN yz_ibuild.systemorganization o on p.organizationSysNo = o.sysNo
        where a.organizationCode like "0001%"
        and a.status=1
        and p.projectStatus=1
        and p.commonStatus=1 
        and o.commonStatus=1 # 有些组织被删除掉了
    )
    and CommonStatus=1




