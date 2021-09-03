import os,sys
sys.path.append(os.getcwd())
import unittest
from model.projectManagement import ProjectManagement as projects_model
from api.projectManagement.projectManagement import projectMagagement_api as projects_api
from common.dbConnection import dbConnection
from common.environment import env
import HTMLTestRunner
import logging







  




def getpath(file):
    return os.path.join(os.getcwd().split("\testcase")[0],"reports\\"+file+".html")

class projectManagement(unittest.TestCase):
    ''' projects query test
    '''
    conn=dbConnection()
    projects_model=projects_model(conn)
    projects_api=projects_api()

    # @classmethod
    # def setUpClass(cls,self):
    #     self.conn=dbConnection()
    #     self.projects_model=projects_model(self.conn)
    #     self.projects_api=projects_api()   

    @classmethod
    def tearDownClass(cls):
        if cls.conn:
            cls.conn.close()

    # 查询到的项目中包含我的项目,因此项目数=组织项目数+我的项目数
    def test_queryProjects_001(self):
        ''' query all projects
        '''
        orgCode=['000101000049','000100010004','000100010003','000100010006','000101000050','000101000048','000100010007']
        for org in orgCode:
            params={'followOrganizationCode':org}
            projects_db=self.projects_model.queryProjects(orgCode=org,relationShip=1)
            projects_api=self.projects_api.api_getProjects(args=params)
            myProjects=self.projects_model.queryUserProjects(env['user'])
            projects=list(set(projects_db+myProjects))

            self.assertEqual(projects_api['total'],len(projects))
            #print(len(projects_db),len(projects_api))
        
    # 查询到的项目中包含我的项目
    def test_queryProjects_002(self):
        ''' query projects 本级
        '''
        org='0001'
        params={'followOrganizationCode':org,'relationship':0}
        projects_db=self.projects_model.queryProjects(orgCode=org,relationShip=0)

        projects_api=self.projects_api.api_getProjects(args=params)
        print('request result %s' % projects_api)
        myProjects_api=self.projects_api.api_queryMyProjects(args=params)
        self.assertEqual(projects_api['total']-myProjects_api['total'],len(projects_db))
        

            
if __name__=='__main__':
    # unittest.main()
    # suite=unittest.TestSuite()
    # suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(projectManagement))
    # runner=unittest.TextTestRunner()
    # runner.run(suite)


    testPlan=unittest.defaultTestLoader.loadTestsFromTestCase(projectManagement)
    #fp=open(getpath('projectManagement'),'wb')
    with open(getpath('projectManagement'),'wb') as fp:
        HTMLTestRunner.HTMLTestRunner(fp,title='query projects').run(testPlan)
            