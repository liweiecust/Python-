import time

def qq():
    f = {}
    d = []


    for x in range(5):
        f["a"]=x
      
        d.append(f)
        print(f)
        #time.sleep(3)

    return d



print(qq())
a=2
b=3
print("%s - %s" % (a,b))

user_list=[]
print(type({"User":'li',"PassWord":"ll"}))
user_list.append({"User":'li',"PassWord":"ll"})
print(user_list[0]["User"])
