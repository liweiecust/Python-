import os,sys
sys.path.append(os.getcwd())

from common.dbConnection import dbConnection
from pymysql.connections import Connection
from pymysql import Error

class organization():

    '''
    '''
    def __init__(self,conn):
        if not isinstance(conn,dbConnection):
            raise Error('invalid object conn')
        self.conn=conn

    def getOrgbyName(self,name):
        queryStr="""
            select OrganizationCode from systemorganization
            where organizationName=%s
            and commonstatus=1 """
        orgCode=self.conn.executeQuery(queryStr,name)
        return orgCode

if __name__=="__main__":
    conn=dbConnection()
    org=organization(conn)
    orgCode=org.getOrgbyName('中国建筑第五工程局有限公司1')[0][0]
    print(orgCode)
