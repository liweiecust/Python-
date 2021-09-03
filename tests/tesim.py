import os,sys
sys.path.append(os.getcwd())
from common.environment import env

from common.A import afunc
from common.B import b_func

def cfunc():
    env["db"]="C"
afunc()
print(env["db"])
b_func()
print(env["db"])
cfunc()
print(env["db"])