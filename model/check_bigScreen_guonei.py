#!/usr/bin/env python3
import pymysql
import datetime

###检查国内企业大屏-中屏展示数据

# QA
mysql_sz={"host":"172.16.0.130",
    "port":7301,
    "user":"dev_admin",
    "passwd":"zk.123456"}

# PRD
# mysql_sz={"host":"192.168.110.50",
#     "port":3306,
#     "user":"dev_zl_r_vice.c.zhu",
#     "passwd":"zc@325325"}


nowyear = "2020"

#通过组织、区域获取项目
def get_mysql_pj(org,are=None):
    strorg = org + "%"
    # 创建连接
    conn = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                           passwd=mysql_sz["passwd"], db="yz_ibuild",charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    if are ==None:
        sql = """SELECT
                    project.BuildingVolume,
                    project.BuildingVolumeType,
                    project.TotalContractAmt,
                    project.StartDate,
                    project.ProjectStatus,
                    project.ProjectCategory,
                    project.SysNo,
                    project.ProjectName,
                    project.AreaSysNo,
                    project.InDate	
                FROM
                    yz_ibuild.`project` AS project
                    INNER JOIN yz_ibuild.systemorganization AS org ON project.OrganizationSysNo = org.SysNo
                WHERE
                    project.OrganizationCode LIKE %s 
                    AND project.CommonStatus = 1 
                    AND project.IsInternal = 1
                    ORDER BY project.ProjectLevel DESC, project.TotalContractAmt DESC"""
        cursor.executemany(sql, [(strorg,)])
    else:
        strare = are + "%"
        sql = """SELECT
                    project.BuildingVolume,
                    project.BuildingVolumeType,
                    project.TotalContractAmt,
                    project.StartDate,
                    project.ProjectStatus,
                    project.ProjectCategory,
                    project.SysNo,
                    project.ProjectName,
                    project.AreaSysNo,
                    project.InDate
                FROM
                    yz_ibuild.`project` AS project
                    INNER JOIN yz_ibuild.systemorganization AS org ON project.OrganizationSysNo = org.SysNo
                    INNER JOIN yz_ibuild.systemarea AS ares ON project.AreaSysNo = ares.SysNo
                WHERE
                    project.OrganizationCode LIKE %s
                    AND ares.LevelAreaCode LIKE %s	
                    AND project.CommonStatus = 1 
                    AND project.IsInternal = 1
                    ORDER BY project.ProjectLevel DESC, project.TotalContractAmt DESC"""
        cursor.executemany(sql, [(strorg,strare)])
    row = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return row

#项目总况数据检查
def check_xmzk(data):
    # jldata = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d')
    jztl_1 = 0
    jztl_2 = 0
    htze = 0
    zjxm = 0
    jlxz = 0
    for x in data:
        BuildingVolume = x[0]
        BuildingVolumeType = x[1]
        TotalContractAmt = x[2]
        StartDate = x[3]
        ProjectStatus = x[4]
        InDate = x[9]
        if ProjectStatus ==1:
            if BuildingVolume != None:
                if BuildingVolumeType == 0:
                    jztl_1 += BuildingVolume
                elif BuildingVolumeType == 1:
                    jztl_2 += BuildingVolume
            if TotalContractAmt != None:
                htze += TotalContractAmt
            zjxm += 1
        if StartDate != None:
            if StartDate.strftime('%Y') ==  nowyear:
                jlxz += 1
        else:
            if InDate.strftime('%Y') == nowyear:
                jlxz += 1

    print("-------项目总况数据检查---------")
    print(f"建筑体量万平方米：{round(jztl_1 / 10000, 1)}")
    print(f"建筑体量万延米：{round(jztl_2 / 10000, 1)}")
    print(f"合同总额亿：{round(htze / 10000, 1)}")
    print(f"在建项目：{zjxm}")
    print(f"今年新增项目：{jlxz}")
    # return [round(jztl_1 / 10000, 1), round(jztl_2 / 10000, 1), round(htze / 10000, 1), zjxm, jlxz]

#项目类型数据检查
def check_xmlx(data):
    num = len(data)
    lx_dict_1={1:"房屋建筑工程",2:"市政公用工程",3:"机电安装工程",4:"铁路工程",5:"公路工程",6:"港口与航道工程",
             7:"水利水电工程",8:"电力工程",9:"矿山工程",10:"冶炼工程",11:"化工石油工程",12:"通信工程",
             13:"其他",14:"公共建筑"}
    lx_dict_2= {"房屋建筑工程":0, "市政公用工程":0, "机电安装工程":0, "铁路工程":0, "公路工程":0, "港口与航道工程":0,
               "水利水电工程":0, "电力工程":0, "矿山工程":0, "冶炼工程":0, "化工石油工程":0, "通信工程":0,
               "其他":0, "公共建筑":0}
    for x in data:
        ProjectCategory = x[5]
        keyname = lx_dict_1[ProjectCategory]
        lx_dict_2[keyname] +=1
    data_list = sorted(lx_dict_2.items(), key=lambda item:item[1],reverse=True)

    print("----------项目类型数据检查------------")
    for y in data_list:
        print(f"{y[0]}:{y[1]} / {round((y[1]/num)*100,1)}")

#智能监测数据检查
def check_zljc(data):

    print("----------智能监测设备检查--------------")
    appcode_list = [["env_monitor", "环境监测"], ["tower_crane", "塔吊"], ["energy_conserve", "水电表"], ["smoke_detector", "智能烟感"],
               ["soil_temp", "养护室监控"], ["construction_elevator", "施工电梯"], ["unloading_platform", "卸料平台"]]

    pjsys_list = []
    for x1 in data:
        pjsys_list.append(x1[6])

    #检查视频监控设备
    # 创建连接
    conn = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                           passwd=mysql_sz["passwd"], db="yz_ibuild_video",charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    sql = """SELECT OnLineStatus FROM `video_ipc_info` WHERE ProjectSysNo IN %s AND CommonStatus=1"""
    cursor.executemany(sql, [(pjsys_list,)])
    row = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    online_video = 0
    video_num = len(row)
    for x2 in row:
        if x2[0] == 1:
            online_video +=1
    print(f"视频监控：{online_video}/{video_num}")

    #检查其他监控设备
    for y in appcode_list:
        appcode = y[0]
        appname = y[1]
        if appcode != "energy_conserve":
            # 创建连接
            conn1 = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                                   passwd=mysql_sz["passwd"], db="yz_ibuild", charset='utf8')
            # 创建游标
            cursor1 = conn1.cursor()
            sql1 = """SELECT
                             pjde.DeviceSysNo,pjde.DeviceType
                        FROM
                            projectintellidevice AS pjde
                            INNER JOIN intelliapp AS inap ON pjde.AppSysNo = inap.SysNo 
                        WHERE
                            pjde.`Status` = 1 
                            AND inap.AppCode = %s
                            AND inap.`Status` = 1
                            AND pjde.ProjectSysNo IN %s"""
            cursor1.executemany(sql1, [(appcode,pjsys_list)])
            row1 = cursor1.fetchall()
            # 关闭游标
            cursor1.close()
            # 关闭连接
            conn1.close()

            device_num = len(row1)
            online_device = 0
            device_sys = []
            for z in row1:
                disys = z[0]
                if disys !=None:
                    device_sys.append(disys)
                else:
                    online_device += 1

            #检查检查设备在线状态
            conn2 = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                                    passwd=mysql_sz["passwd"], db="yz_ibuild_open", charset='utf8')
            # 创建游标
            cursor2 = conn2.cursor()
            sql2 = """SELECT COUNT(*) FROM `sp_product_device_status` WHERE  OnlineStatus=1 AND DeviceSysNo IN %s"""
            cursor2.executemany(sql2, [(device_sys,)])
            row2 = cursor2.fetchall()
            # 关闭游标
            cursor2.close()
            # 关闭连接
            conn2.close()
            online_device += row2[0][0]
            print(f"{appname}:{online_device}/{device_num}")

        #检查水电设备
        else:
            # 创建连接
            conn1 = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                                    passwd=mysql_sz["passwd"], db="yz_ibuild", charset='utf8')
            # 创建游标
            cursor1 = conn1.cursor()
            sql1 = """SELECT
                                         pjde.DeviceSysNo,pjde.DeviceType
                                    FROM
                                        projectintellidevice AS pjde
                                        INNER JOIN intelliapp AS inap ON pjde.AppSysNo = inap.SysNo 
                                    WHERE
                                        pjde.`Status` = 1 
                                        AND inap.AppCode = %s
                                        AND inap.`Status` = 1
                                        AND pjde.ProjectSysNo IN %s"""
            cursor1.executemany(sql1, [(appcode, pjsys_list)])
            row1 = cursor1.fetchall()
            # 关闭游标
            cursor1.close()
            # 关闭连接
            conn1.close()

            sb_num = 0
            sb_on_num =0
            sb_list = []
            db_num = 0
            db_on_num = 0
            db_list = []
            for p in row1:
                if p[1] == 0:
                    sb_num +=1
                    if p[0] !=None:
                        sb_list.append(p[0])
                    else:
                        sb_on_num +=1
                elif p[1] == 1:
                    db_num +=1
                    if p[0] !=None:
                        db_list.append(p[0])
                    else:
                        db_on_num +=1
            data_list = [["水表",sb_num,sb_list,sb_on_num],["电表",db_num,db_list,db_on_num]]

            for b in data_list:
                appname = b[0]
                device_num = b[1]
                device_sys = b[2]
            # 检查检查设备在线状态
                conn2 = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                                        passwd=mysql_sz["passwd"], db="yz_ibuild_open", charset='utf8')
                # 创建游标
                cursor2 = conn2.cursor()
                sql2 = """SELECT COUNT(*) FROM `sp_product_device_status` WHERE  OnlineStatus=1 AND DeviceSysNo IN %s"""
                cursor2.executemany(sql2, [(device_sys,)])
                row2 = cursor2.fetchall()
                # 关闭游标
                cursor2.close()
                # 关闭连接
                conn2.close()
                online_device = row2[0][0] + b[3]
                print(f"{appname}:{online_device}/{device_num}")

#前10重点项目检查
def check_zdxm(data):
    print("--------重点项目检查--------------")
    # for x in data[0:10]:
    #     print(x[7])
    # 创建连接
    conn = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                           passwd=mysql_sz["passwd"], db="yz_ibuild",charset='utf8')
    # 创建游标
    cursor = conn.cursor()

    sql = """SELECT
                    pj.ProjectName 
                FROM
                    `project_excellent` AS pj_ex
                    INNER JOIN project AS pj ON pj_ex.ProjectSysNo = pj.SysNo 
                ORDER BY
                    pj_ex.SysNo DESC"""
    cursor.execute(sql)
    row = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

    for x in  row:
        print(x[0])

#中间全国地图数据统计
def check_qgdt(data):

    print("-------------全国级地图检查-----------")
    # 创建连接
    conn = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                           passwd=mysql_sz["passwd"], db="yz_ibuild",charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    sql = """SELECT AreaName,LevelAreaCode FROM systemarea WHERE  LENGTH(LevelAreaCode) = 12 AND AreaType=1"""
    cursor.execute(sql)
    row = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

    for x in row:
        sj_name = x[0]
        print(f"{sj_name}：")

        sj_code = x[1]
        LevelAreaCode = sj_code + "%"
        # 创建连接
        conn1 = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                               passwd=mysql_sz["passwd"], db="yz_ibuild", charset='utf8')
        # 创建游标
        cursor1 = conn1.cursor()
        sql1 = """SELECT SysNo FROM systemarea WHERE LevelAreaCode LIKE %s"""
        cursor1.executemany(sql1, [(LevelAreaCode,)])
        row1 = cursor1.fetchall()
        # 关闭游标
        cursor1.close()
        # 关闭连接
        conn1.close()

        are_sys = []
        for y in row1:
            are_sys.append(y[0])

        pj_num = 0
        pj_zjxm = 0
        pj_bnxkxm = 0
        pj_jztl_pfm = 0
        pj_jztl_ym = 0
        pj_htze = 0

        for z in data:
            aresys = z[8]
            if aresys !=None:
                if aresys in are_sys:
                    pj_num +=1
                    BuildingVolume = z[0]
                    BuildingVolumeType = z[1]
                    TotalContractAmt = z[2]
                    StartDate = z[3]
                    ProjectStatus = z[4]
                    InDate = z[9]

                    if ProjectStatus == 1:
                        pj_zjxm +=1
                    if StartDate !=None:
                        if StartDate.strftime('%Y') ==  nowyear:
                            pj_bnxkxm +=1
                    else:
                        if InDate.strftime('%Y') ==  nowyear:
                            pj_bnxkxm += 1
                    if BuildingVolume !=None:
                        if BuildingVolumeType == 0:
                            pj_jztl_pfm += BuildingVolume
                        elif BuildingVolumeType == 1:
                            pj_jztl_ym += BuildingVolume
                    if TotalContractAmt !=None:
                        pj_htze += TotalContractAmt

        print(f"项目数：{pj_num},在建项目数{pj_zjxm},今年新开项目数{pj_bnxkxm},建筑体量万平方米{round(pj_jztl_pfm/10000,1)},建筑体量万延米{round(pj_jztl_ym/10000,1)},合同金额亿{round(pj_htze/10000,1)}")

if __name__ == "__main__":
    #get_mysql_pj 入参组织编号、区域编号
    # pj_list = get_mysql_pj("00010100", "09991000")
    # 平台编码 0001
    pj_list = get_mysql_pj("0001")
    check_xmzk(pj_list)
    check_xmlx(pj_list)
    check_zljc(pj_list)
    check_zdxm(pj_list)
    check_qgdt(pj_list)