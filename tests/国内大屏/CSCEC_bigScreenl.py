# py -m pip install virtualenv -i https://pypi.python.org/simple/

import sys,os 
cwd=os.getcwd()
print(cwd)
sys.path.append(os.getcwd())
print(sys.argv)
print(sys.path)

import model.check_bigScreen_guonei as model

pj_list = model.get_mysql_pj("0001")
if __name__=="__main__":
    pj_list = get_mysql_pj("0001")
    None