import sys,os
sys.path.append(os.getcwd())
import common.restClient as request
import common.dbConnection as dbConection
from sql.海外企业大屏.全球层项目人员查询 import xmry_query
import json

#params
baseurl="http://ibuild.yzw.cn.qa:82/org/api"
api="/aboardOrgBigScreen/overseasProfile?stateCode=&countryCode="
url=baseurl+api
print(url)

#request
res=request.get(url,None)
rowData=json.loads(res)['data']
print(rowData)


zf_xmry_total_api=rowData['totalChinaEmployees']


### Test

# 中方人员总数


print("query db")
xmry_total=dbConection.executeQuery(xmry_query,None)[0]

zf_xmry_total=xmry_total[0]
wf_xmry_total=xmry_total[1]

assert zf_xmry_total==zf_xmry_total_api,"数据不一致"


class xmry(unittest.TestCase):

    """
    """
    def
    def setUp(self):
        None

    def test_global_xmry(self):
        None

if __name__=="__main__"