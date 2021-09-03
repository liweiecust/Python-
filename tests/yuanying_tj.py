##运营统计数据：上线项目数、企业用户数、设备数量

import pymysql

# PRD
mysql_sz={"host":"192.168.110.50",
    "port":3306,
    "user":"dev_zl_r_vice.c.zhu",
    "passwd":"ZhuChao@325325"}

def get_mysql_data(sttime,entime):

    # 上线项目数
    sql_1 = """SELECT
                    count(*) 
                FROM
                    yz_ibuild.project p 
                WHERE
                    p.CommonStatus = 1 
                    AND p.InDate BETWEEN %s
                    AND %s """
    # 企业用户数
    sql_2 = """SELECT
                      count(*) 
                  FROM
                      yz_ibuild.systemuser su 
                  WHERE
                      su.IBuildCommonStatus = 1 
                      AND su.CreateSource = 3 
                      AND su.InDate BETWEEN %s 
                      AND %s """
    # 设备数量
    sql_3 = """SELECT
                       count( pd.SysNo ) 
                   FROM
                       yz_ibuild.project p
                       INNER JOIN yz_ibuild.projectintellidevice pd ON p.SysNo = pd.ProjectSysNo 
                   WHERE
                       P.CommonStatus = 1 
                       AND pd.Status = 1 
                       AND P.InDate BETWEEN %s 
                       AND %s """

    sql_list = [sql_1,sql_2,sql_3]
    data_list = []

    conn = pymysql.connect(host=mysql_sz["host"], port=mysql_sz["port"], user=mysql_sz["user"],
                           passwd=mysql_sz["passwd"], db="yz_ibuild", charset='utf8')
    # 创建游标
    cursor = conn.cursor()

    for loop in sql_list:
        cursor.executemany(loop, [(sttime,entime)])
        row = cursor.fetchall()
        data_list.append(row[0][0])

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    print(f"项目数{data_list[0]},用户数{data_list[1]},设备数{data_list[2]}")

if __name__ == "__main__":
    get_mysql_data('1900-01-01','2020-10-31')