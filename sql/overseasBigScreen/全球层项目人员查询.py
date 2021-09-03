# 全球层 人员总数查询
xmry_query="""
select sum(中方管理人员),sum(中方人员总数),sum(外方管理人员),sum(外方人员总数),sum(xmry_total)
FROM
(
select 
a.xmcode,
zfxmry_qmzwgl,
zfxmry_qmzwlw,
sdxmry_qmsdgl,
sdxmry_qmsdlw,
dsgxmry,
IFNULL(zfxmry_qmzwgl,0) 中方管理人员,
IFNULL(zfxmry_qmzwgl,0) +IFNULL(zfxmry_qmzwlw,0) 中方人员总数,
IFNULL(sdxmry_qmsdgl,0) 外方管理人员,
IFNULL(sdxmry_qmsdgl,0)+IFNULL(sdxmry_qmsdlw,0)+IFNULL(dsgxmry,0) 外方人员总数,
IFNULL(zfxmry_qmzwgl,0) +IFNULL(zfxmry_qmzwlw,0)+IFNULL(sdxmry_qmsdgl,0)+IFNULL(sdxmry_qmsdlw,0)+IFNULL(dsgxmry,0) xmry_total
from cscec_ds_xmry a 
INNER JOIN cscec_ds_gwdpsjdjmxb b on a.xmcode=b.xmcode

where b.id in
(
	SELECT id FROM
	cscec_ds_gwdpsjdjmxb
	WHERE 
	STR_TO_DATE(CONCAT_ws('-',nd,yf,'01'),'%Y-%m-%d')
	=
	(select 
	max(STR_TO_DATE(CONCAT_ws('-',nd,yf,'01'),'%Y-%m-%d'))
	from cscec_ds_gwdpsjdjmxb )
	and xmzt=1 and status=1
)
and a.nd=b.nd and a.yf=b.yf
and b.xmzt=1 and b.`status`=1 and a.`status`=1
) c
"""

