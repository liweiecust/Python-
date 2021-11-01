sites=[
        'https://ibuild.yzw.cn/home/proprietary',
        'https://ibuild.yzw.cn/home/proprietary/10807',
       
    ]

# 不可变类型
for site in sites:
    # replace 不会改变sites列表
    site=site.replace('https://ibuild.yzw.cn','http://ibuild.yzw.cn.qa:81') 
    print(id(site))  

# 可以看出id不同
for site in sites:
    print(id(site))