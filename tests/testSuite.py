import os,sys
import HTMLTestRunner
import unittest

sys.path.append(os.path.dirname(__name__))

def func(args):
    a=['ld']
    for t in a:
        print(m)
    print(args)
m='l'
v=map(func,('a','n','c'))
# for a in v:
#     print(a)
print(v)
func('d')


class test(unittest.TestCase):
    a=3
    def __init__(self,methodName='runTest'):
        super().__init__(methodName)
    
    def test_f(self):
        print(test.a)

def getpath(file):
    return os.path.join(os.getcwd().split("\testcase")[0],"reports\\"+file+".html")

if __name__=='__main__':  
    testPlan=unittest.defaultTestLoader.loadTestsFromTestCase(test)
    fp=open(getpath("test_algorithm"),"wb")
    HTMLTestRunner.HTMLTestRunner(fp,title='test report').run(testPlan)
    fp.close()



if __name__=='__main__':
    #unittest.main()
    suite=unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test))
    runner=unittest.TextTestRunner()
    runner.run(suite)
