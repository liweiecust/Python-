import pymysql
from common.environment import env


class dbConnection:
    '''mysql connection object
    '''
    connStr=None
    conn=None
    def __init__(self):
        self.connStr=env['db']
        if self.conn is None:
            self.conn=self.getConnection(self.connStr)
      

    def getConnection(self,connStr):
        conn = pymysql.connect(host=connStr["host"], port=connStr["port"], user=connStr["user"],
                            db="yz_ibuild",passwd=connStr["passwd"],charset='utf8')
        return conn


    def executeQuery(self,query,args=None):
      
        # 创建游标
        cursor = self.conn.cursor()
        cursor.execute(query,args)
        row = cursor.fetchall()
        # 关闭游标
        cursor.close()
        return row

    # 关闭连接
    def close(self):
        self.conn.close()
